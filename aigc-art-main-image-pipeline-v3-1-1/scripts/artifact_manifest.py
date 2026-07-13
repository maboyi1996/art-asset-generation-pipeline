#!/usr/bin/env python3
"""Shared artifact-manifest helpers for V3.1.1 scripts."""

from __future__ import annotations

import json
from pathlib import Path, PurePosixPath
from typing import Any, Dict, Iterable, List, Tuple


SCHEMA_VERSION = "aigc-artifact-manifest.v1"
SKILL_ID = "aigc-art-main-image-pipeline-v3-1-1"
SKILL_VERSION = "3.1.1"
VALID_ROLES = {"audit", "production_source", "deliverable", "validation_report"}
VALID_ARTIFACT_TYPES = {"markdown", "markdown_table", "json", "docx", "directory", "report"}
VALID_READ_POLICIES = {
    "audit_only",
    "production_source_only",
    "deliverable_only",
    "validation_only",
}
REQUIRED_ARTIFACT_IDS = {
    "core-prompt-slots",
    "prompted-production-task-table",
    "main-image-production-table",
    "prompt-manifest",
    "main-image-review-table",
    "final-quality-report",
}


class ManifestError(Exception):
    pass


def _is_relative_safe(path_text: str) -> bool:
    if not path_text:
        return False
    pure = PurePosixPath(path_text.replace("\\", "/"))
    if pure.is_absolute():
        return False
    return ".." not in pure.parts


def _parts(path_text: str) -> Tuple[str, ...]:
    return tuple(part.lower() for part in PurePosixPath(path_text.replace("\\", "/")).parts)


def _resolved_child(base: Path, path_text: str) -> Path:
    if not _is_relative_safe(path_text):
        raise ManifestError(f"artifact path must be a safe relative path: {path_text}")
    resolved = (base / path_text).resolve()
    try:
        resolved.relative_to(base.resolve())
    except ValueError as exc:
        raise ManifestError(f"artifact path escapes project output directory: {path_text}") from exc
    return resolved


def load_manifest(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise ManifestError(f"artifact manifest not found: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        raise ManifestError(f"invalid artifact manifest JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise ManifestError("artifact manifest root must be an object")
    errors = validate_manifest_data(data, path)
    if errors:
        raise ManifestError("; ".join(errors))
    return data


def validate_manifest_data(data: Dict[str, Any], manifest_path: Path) -> List[str]:
    errors: List[str] = []
    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION}")
    if data.get("skill_id") != SKILL_ID:
        errors.append(f"skill_id must be {SKILL_ID}")
    if data.get("skill_version") != SKILL_VERSION:
        errors.append(f"skill_version must be {SKILL_VERSION}")
    if not isinstance(data.get("project_id"), str) or not data.get("project_id"):
        errors.append("project_id must be a non-empty string")
    if not isinstance(data.get("created_at"), str) or not data.get("created_at"):
        errors.append("created_at must be a non-empty string")

    artifacts = data.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        errors.append("artifacts must be a non-empty array")
        return errors

    ids = set()
    base = manifest_path.parent
    for index, item in enumerate(artifacts):
        prefix = f"artifacts[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix} must be an object")
            continue
        artifact_id = item.get("id")
        if not isinstance(artifact_id, str) or not artifact_id:
            errors.append(f"{prefix}.id must be a non-empty string")
        elif artifact_id in ids:
            errors.append(f"duplicate artifact id: {artifact_id}")
        else:
            ids.add(artifact_id)
        if item.get("role") not in VALID_ROLES:
            errors.append(f"{prefix}.role is invalid: {item.get('role')}")
        if item.get("artifact_type") not in VALID_ARTIFACT_TYPES:
            errors.append(f"{prefix}.artifact_type is invalid: {item.get('artifact_type')}")
        if item.get("read_policy") not in VALID_READ_POLICIES:
            errors.append(f"{prefix}.read_policy is invalid: {item.get('read_policy')}")
        if not isinstance(item.get("producer"), str) or not item.get("producer"):
            errors.append(f"{prefix}.producer must be a non-empty string")
        if not isinstance(item.get("consumers"), list):
            errors.append(f"{prefix}.consumers must be an array")
        if not isinstance(item.get("required"), bool):
            errors.append(f"{prefix}.required must be boolean")

        path_text = item.get("path")
        if not isinstance(path_text, str) or not path_text:
            errors.append(f"{prefix}.path must be a non-empty string")
            continue
        try:
            _resolved_child(base, path_text)
        except ManifestError as exc:
            errors.append(f"{prefix}: {exc}")
            continue

        parts = _parts(path_text)
        role = item.get("role")
        if role == "audit" and (not parts or parts[0] != "audit"):
            errors.append(f"{prefix}.path for audit role must live under audit/: {path_text}")
        if role == "production_source":
            if not parts or parts[0] != "production-source":
                errors.append(f"{prefix}.path for production_source role must live under production-source/: {path_text}")
            if "audit" in parts:
                errors.append(f"{prefix}.path for production_source must not live under audit/: {path_text}")
        if role == "deliverable" and (not parts or parts[0] != "deliverables"):
            errors.append(f"{prefix}.path for deliverable role must live under deliverables/: {path_text}")
        if role == "validation_report" and path_text != "deliverables/final-quality-report.md":
            errors.append(f"{prefix}.path for validation_report must be deliverables/final-quality-report.md")

    missing = sorted(REQUIRED_ARTIFACT_IDS - ids)
    if missing:
        errors.append(f"missing required artifact registrations: {', '.join(missing)}")
    return errors


def artifact_by_id(data: Dict[str, Any], artifact_id: str) -> Dict[str, Any]:
    for item in data.get("artifacts", []):
        if isinstance(item, dict) and item.get("id") == artifact_id:
            return item
    raise ManifestError(f"artifact id not found in manifest: {artifact_id}")


def resolve_artifact(
    manifest_path: Path,
    artifact_id: str,
    *,
    expected_role: str | None = None,
    expected_type: str | None = None,
    must_exist: bool = False,
) -> Path:
    data = load_manifest(manifest_path)
    artifact = artifact_by_id(data, artifact_id)
    if expected_role and artifact.get("role") != expected_role:
        raise ManifestError(
            f"artifact {artifact_id} role mismatch: expected {expected_role}, got {artifact.get('role')}"
        )
    if expected_type and artifact.get("artifact_type") != expected_type:
        raise ManifestError(
            f"artifact {artifact_id} type mismatch: expected {expected_type}, got {artifact.get('artifact_type')}"
        )
    path_text = artifact.get("path", "")
    parts = _parts(path_text)
    if expected_role == "production_source" and "audit" in parts:
        raise ManifestError(f"production source must not be read from audit/: {path_text}")
    if expected_role == "deliverable" and (not parts or parts[0] != "deliverables"):
        raise ManifestError(f"deliverable must be written under deliverables/: {path_text}")
    path = _resolved_child(manifest_path.parent, path_text)
    if must_exist and not path.exists():
        raise ManifestError(f"artifact file does not exist: {path}")
    return path


def required_output_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
