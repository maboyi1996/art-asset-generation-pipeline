"""Canonical pipeline contract and schema registry."""
from __future__ import annotations

import json
from collections import Counter, defaultdict, deque
from functools import lru_cache
from pathlib import Path
from typing import Callable

from .errors import ContractError
from .storage import sha256_file

SKILL_ROOT = Path(__file__).resolve().parents[2]
CONTRACT_PATH = SKILL_ROOT / "framework" / "pipeline-contract.json"


@lru_cache(maxsize=1)
def load_contract() -> dict:
    value = json.loads(CONTRACT_PATH.read_text(encoding="utf-8-sig"))
    if value.get("skill_id") != "aigc-art-main-image-pipeline-v4-0" or value.get("skill_version") != "4.0.0":
        raise ContractError("Pipeline contract skill identity mismatch")
    return value


def node_by_id(node_id: str) -> dict:
    for node in load_contract()["nodes"]:
        if node["id"] == node_id:
            return node
    raise ContractError(f"Unknown pipeline node: {node_id}")


def artifact_contract(artifact_id: str) -> dict:
    try:
        return load_contract()["artifacts"][artifact_id]
    except KeyError as exc:
        raise ContractError(f"Unknown contract artifact: {artifact_id}") from exc


@lru_cache(maxsize=None)
def _load_schema(path_text: str) -> dict:
    path = Path(path_text)
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _pointer(value: dict, fragment: str) -> dict:
    current = value
    if fragment.startswith("/"):
        for part in fragment.lstrip("/").split("/"):
            part = part.replace("~1", "/").replace("~0", "~")
            current = current[part]
    return current


def schema_and_resolver(ref: str, *, base_file: Path | None = None) -> tuple[dict, Callable[[str], dict]]:
    file_part, sep, fragment = ref.partition("#")
    if file_part:
        schema_file = (SKILL_ROOT / file_part).resolve() if not Path(file_part).is_absolute() else Path(file_part).resolve()
    elif base_file:
        schema_file = base_file.resolve()
    else:
        raise ContractError(f"Schema reference lacks a file: {ref}")
    if not schema_file.exists():
        raise ContractError(f"Schema file does not exist: {schema_file}")
    document = _load_schema(str(schema_file))
    selected = _pointer(document, fragment) if sep and fragment else document

    def resolver(child_ref: str) -> dict:
        return schema_and_resolver(child_ref, base_file=schema_file)[0]

    return selected, resolver


def artifact_schema(artifact_id: str) -> tuple[dict, Callable[[str], dict]]:
    return schema_and_resolver(artifact_contract(artifact_id)["schema"])


def validate_contract_data(contract: dict | None = None) -> list[str]:
    contract = contract or load_contract()
    errors: list[str] = []
    nodes = contract.get("nodes", [])
    artifacts = contract.get("artifacts", {})
    ids = [node.get("id") for node in nodes]
    if len(nodes) != 26:
        errors.append(f"node count must be 26, got {len(nodes)}")
    if len(set(ids)) != len(ids):
        errors.append("duplicate node ids")
    modes = Counter(node.get("mode") for node in nodes)
    expected = {"P": 15, "M→P": 6, "M+P": 5}
    if dict(modes) != expected:
        errors.append(f"mode counts must be {expected}, got {dict(modes)}")
    if any(node.get("mode") not in expected for node in nodes):
        errors.append("model-only or unknown node mode exists")
    known = set(ids)
    producers: dict[str, str] = {}
    actual_consumers: dict[str, set[str]] = defaultdict(set)
    for node in nodes:
        for dep in node.get("depends_on", []):
            if dep not in known:
                errors.append(f"{node['id']} depends on unknown node {dep}")
        for artifact_id in node.get("inputs", []):
            if artifact_id not in artifacts:
                errors.append(f"{node['id']} reads unknown artifact {artifact_id}")
            else:
                actual_consumers[artifact_id].add(node["id"])
        for artifact_id in [*node.get("model_produces", []), *node.get("python_produces", [])]:
            if artifact_id not in artifacts:
                errors.append(f"{node['id']} writes unknown artifact {artifact_id}")
            if artifact_id in producers:
                errors.append(f"artifact {artifact_id} has duplicate producers")
            producers[artifact_id] = node["id"]
        if node.get("mode") != "P" and not node.get("model_produces"):
            errors.append(f"model-assisted node lacks model factor artifact: {node['id']}")
        if node.get("mode") == "P" and node.get("model_produces"):
            errors.append(f"P node unexpectedly declares model output: {node['id']}")
    for artifact_id, artifact in artifacts.items():
        if producers.get(artifact_id) != artifact.get("producer"):
            errors.append(f"artifact {artifact_id} producer mismatch")
        declared = set(artifact.get("consumers", []))
        if declared != actual_consumers.get(artifact_id, set()):
            errors.append(f"artifact {artifact_id} consumer mismatch")
        if not declared and not artifact.get("audit_only") and not artifact.get("terminal"):
            errors.append(f"artifact {artifact_id} is orphaned")
        rel = Path(artifact.get("path", ""))
        if rel.is_absolute() or ".." in rel.parts:
            errors.append(f"artifact {artifact_id} path is not safe relative path")
        try:
            schema_and_resolver(artifact["schema"])
        except Exception as exc:
            errors.append(f"artifact {artifact_id} schema invalid: {exc}")
    indegree = {node_id: 0 for node_id in known}
    edges: dict[str, list[str]] = defaultdict(list)
    for node in nodes:
        for dep in node.get("depends_on", []):
            edges[dep].append(node["id"])
            indegree[node["id"]] += 1
    queue = deque(sorted([node_id for node_id, degree in indegree.items() if degree == 0]))
    visited = 0
    while queue:
        current = queue.popleft(); visited += 1
        for nxt in edges[current]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    if visited != len(known):
        errors.append("pipeline DAG contains a cycle")
    if (SKILL_ROOT / "framework" / "pipeline.yaml").exists():
        errors.append("pipeline.yaml must not coexist with pipeline-contract.json")
    forbidden_terms = {"manual_review_required", "blocking_review", "review_queue", "apply_review_decisions"}
    raw = json.dumps(contract, ensure_ascii=False)
    for term in forbidden_terms:
        if term in raw:
            errors.append(f"runtime human-review term forbidden in V4 contract: {term}")
    return errors


def resource_hashes() -> dict[str, str]:
    paths = [CONTRACT_PATH]
    for folder in ["contracts", "policies", "templates", "rules", "guards"]:
        paths.extend(sorted(path for path in (SKILL_ROOT / folder).rglob("*") if path.is_file()))
    return {path.relative_to(SKILL_ROOT).as_posix(): sha256_file(path) for path in paths}
