"""Manifest-routed, atomic JSON/JSONL storage for V4."""
from __future__ import annotations

import hashlib
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from .errors import ContractError, IntegrityError


def utc_now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def ensure_within(root: Path, target: Path) -> Path:
    root = root.resolve()
    target = target.resolve()
    try:
        target.relative_to(root)
    except ValueError as exc:
        raise ContractError(f"Path escapes run root: {target}") from exc
    return target


def atomic_write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, path)
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)


def atomic_write_text(path: Path, text: str) -> None:
    atomic_write_bytes(path, text.encode("utf-8"))


def write_json(path: Path, value: Any) -> None:
    atomic_write_text(path, json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def write_jsonl(path: Path, rows: Iterable[dict]) -> None:
    text = "".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in rows)
    atomic_write_text(path, text)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def read_jsonl(path: Path, *, allow_missing: bool = False) -> list[dict]:
    if not path.exists():
        if allow_missing:
            return []
        raise IntegrityError(f"Required JSONL does not exist: {path}")
    rows: list[dict] = []
    for index, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise IntegrityError(f"Invalid JSONL {path.name} line {index}: {exc}") from exc
        if not isinstance(value, dict):
            raise IntegrityError(f"JSONL row must be an object: {path.name} line {index}")
        rows.append(value)
    return rows


def load_manifest(manifest_path: Path) -> dict:
    manifest_path = manifest_path.resolve()
    if manifest_path.name != "run-manifest.json":
        raise ContractError("Run manifest file name must be run-manifest.json")
    value = read_json(manifest_path)
    if value.get("schema_version") != "aigc-main-image-run.v4":
        raise ContractError("Unsupported run manifest schema")
    if value.get("skill", {}).get("id") != "aigc-art-main-image-pipeline-v4-0":
        raise ContractError("Run manifest belongs to a different skill")
    if value.get("skill", {}).get("version") != "4.0.0":
        raise ContractError("Run manifest belongs to a different skill version")
    return value


def save_manifest(manifest_path: Path, manifest: dict) -> None:
    manifest["updated_at"] = utc_now()
    write_json(manifest_path.resolve(), manifest)


def run_root(manifest_path: Path) -> Path:
    return manifest_path.resolve().parent


def artifact_entry(manifest: dict, artifact_id: str) -> dict:
    try:
        return manifest["artifacts"][artifact_id]
    except KeyError as exc:
        raise ContractError(f"Unknown artifact id: {artifact_id}") from exc


def artifact_path(manifest_path: Path, artifact_id: str, *, must_exist: bool = False) -> Path:
    manifest = load_manifest(manifest_path)
    entry = artifact_entry(manifest, artifact_id)
    rel = Path(entry["path"])
    if rel.is_absolute() or ".." in rel.parts:
        raise ContractError(f"Artifact path must be relative: {artifact_id}")
    target = ensure_within(run_root(manifest_path), run_root(manifest_path) / rel)
    if must_exist and not target.exists():
        raise IntegrityError(f"Required artifact missing: {artifact_id} -> {target}", artifact_id=artifact_id)
    return target


def refresh_artifact(manifest_path: Path, artifact_id: str, *, status: str = "ready") -> None:
    manifest = load_manifest(manifest_path)
    entry = artifact_entry(manifest, artifact_id)
    target = ensure_within(run_root(manifest_path), run_root(manifest_path) / entry["path"])
    if not target.exists():
        raise IntegrityError(f"Cannot refresh missing artifact: {artifact_id}", artifact_id=artifact_id)
    entry["status"] = status
    entry["sha256"] = sha256_file(target)
    entry["bytes"] = target.stat().st_size
    entry["updated_at"] = utc_now()
    save_manifest(manifest_path, manifest)


def file_hashes(manifest_path: Path, artifact_ids: Iterable[str]) -> dict[str, str]:
    manifest = load_manifest(manifest_path)
    result: dict[str, str] = {}
    root = run_root(manifest_path)
    for artifact_id in artifact_ids:
        entry = artifact_entry(manifest, artifact_id)
        target = ensure_within(root, root / entry["path"])
        if target.exists():
            result[artifact_id] = sha256_file(target)
    return result


def begin_node(manifest_path: Path, node_id: str) -> None:
    manifest = load_manifest(manifest_path)
    state = manifest["nodes"].get(node_id)
    if state is None:
        raise ContractError(f"Unknown node: {node_id}")
    state.update({"status": "running", "started_at": utc_now(), "error": ""})
    save_manifest(manifest_path, manifest)


def finish_node(manifest_path: Path, node_id: str, *, inputs: Iterable[str], outputs: Iterable[str], status: str = "passed", error: str = "") -> None:
    manifest = load_manifest(manifest_path)
    state = manifest["nodes"][node_id]
    state.update({
        "status": status,
        "completed_at": utc_now(),
        "input_hashes": file_hashes(manifest_path, inputs),
        "output_hashes": file_hashes(manifest_path, outputs),
        "error": error,
    })
    save_manifest(manifest_path, manifest)


def assert_dependencies(manifest_path: Path, node: dict) -> None:
    manifest = load_manifest(manifest_path)
    failed = []
    for dep in node.get("depends_on", []):
        if manifest["nodes"].get(dep, {}).get("status") != "passed":
            failed.append(dep)
    if failed:
        raise IntegrityError(f"Node {node['id']} dependencies not passed: {', '.join(failed)}")
