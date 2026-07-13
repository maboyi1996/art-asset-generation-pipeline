"""Validate model factor snapshots; this module never calls a human reviewer."""
from __future__ import annotations

from pathlib import Path

from .contract_registry import artifact_schema, node_by_id
from .errors import ValidationError
from .storage import artifact_path, read_jsonl
from .validator import require_rows_valid

FORBIDDEN_RUNTIME_TERMS = {"manual_review_required", "blocking_review", "review_queue"}


def load_model_rows(manifest_path: Path, node_id: str) -> dict[str, list[dict]]:
    node = node_by_id(node_id)
    outputs: dict[str, list[dict]] = {}
    forbidden = set(node.get("forbidden_model_fields", []))
    for artifact_id in node.get("model_produces", []):
        path = artifact_path(manifest_path, artifact_id, must_exist=True)
        rows = read_jsonl(path)
        schema, resolver = artifact_schema(artifact_id)
        require_rows_valid(rows, schema, artifact_id=artifact_id, resolver=resolver)
        violations: list[str] = []
        for index, row in enumerate(rows):
            bad = forbidden.intersection(row)
            if bad:
                violations.append(f"row {index} contains forbidden fields: {', '.join(sorted(bad))}")
            raw = str(row)
            terms = [term for term in FORBIDDEN_RUNTIME_TERMS if term in raw]
            if terms:
                violations.append(f"row {index} contains forbidden review terms: {', '.join(terms)}")
        if violations:
            raise ValidationError(f"{artifact_id}: " + "; ".join(violations[:20]), artifact_id=artifact_id)
        outputs[artifact_id] = rows
    return outputs
