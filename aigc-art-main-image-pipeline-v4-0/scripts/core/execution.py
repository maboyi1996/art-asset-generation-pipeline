"""Uniform node execution and manifest state transitions."""
from __future__ import annotations

from pathlib import Path
from typing import Callable

from .contract_registry import artifact_schema, node_by_id
from .errors import PipelineError, ValidationError
from .model_gateway import load_model_rows
from .storage import (
    artifact_path, assert_dependencies, begin_node, finish_node, load_manifest,
    read_json, read_jsonl, refresh_artifact,
)
from .validator import require_rows_valid, require_valid


def validate_artifact(manifest_path: Path, artifact_id: str) -> None:
    path = artifact_path(manifest_path, artifact_id, must_exist=True)
    manifest = load_manifest(manifest_path)
    artifact_type = manifest["artifacts"][artifact_id]["artifact_type"]
    schema, resolver = artifact_schema(artifact_id)
    if artifact_type == "jsonl":
        require_rows_valid(read_jsonl(path), schema, artifact_id=artifact_id, resolver=resolver)
    elif artifact_type == "json":
        require_valid(read_json(path), schema, name=artifact_id, resolver=resolver)


def execute_node(manifest_path: Path, node_id: str, handler: Callable[[Path], None]) -> int:
    node = node_by_id(node_id)
    assert_dependencies(manifest_path, node)
    begin_node(manifest_path, node_id)
    try:
        if node.get("model_produces"):
            load_model_rows(manifest_path, node_id)
            for artifact_id in node["model_produces"]:
                refresh_artifact(manifest_path, artifact_id)
        handler(manifest_path)
        for artifact_id in node.get("python_produces", []):
            validate_artifact(manifest_path, artifact_id)
            refresh_artifact(manifest_path, artifact_id)
        finish_node(
            manifest_path, node_id,
            inputs=node.get("inputs", []),
            outputs=[*node.get("model_produces", []), *node.get("python_produces", [])],
            status="passed",
        )
        return 0
    except (PipelineError, OSError, ValueError, KeyError) as exc:
        finish_node(
            manifest_path, node_id,
            inputs=node.get("inputs", []),
            outputs=[], status="failed", error=str(exc),
        )
        print(f"ERROR [{node_id}]: {exc}")
        return 1
