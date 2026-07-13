"""Dependency-free structural validation used by all V4 modules."""
from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from .errors import ValidationError

TYPE_MAP = {
    "object": dict,
    "array": list,
    "string": str,
    "integer": int,
    "number": (int, float),
    "boolean": bool,
    "null": type(None),
}


def _type_ok(value: Any, expected: str) -> bool:
    target = TYPE_MAP[expected]
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    return isinstance(value, target)


def validate_value(value: Any, schema: dict, *, path: str = "$", resolver=None) -> list[str]:
    errors: list[str] = []
    if "$ref" in schema:
        if resolver is None:
            return [f"{path}: unresolved schema ref {schema['$ref']}"]
        schema = resolver(schema["$ref"])
    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: must equal {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: invalid enum {value!r}")
    expected = schema.get("type")
    if expected:
        choices = expected if isinstance(expected, list) else [expected]
        if not any(_type_ok(value, choice) for choice in choices):
            return [f"{path}: expected {'/'.join(choices)}, got {type(value).__name__}"]
    if isinstance(value, str) and len(value) < schema.get("minLength", 0):
        errors.append(f"{path}: string is shorter than minLength")
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{path}: array is shorter than minItems")
        item_schema = schema.get("items")
        if item_schema:
            for index, item in enumerate(value):
                errors.extend(validate_value(item, item_schema, path=f"{path}[{index}]", resolver=resolver))
    if isinstance(value, dict):
        properties = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in value:
                errors.append(f"{path}: missing required field {key}")
        if schema.get("additionalProperties") is False:
            for key in value:
                if key not in properties:
                    errors.append(f"{path}: unexpected field {key}")
        for key, child_schema in properties.items():
            if key in value:
                errors.extend(validate_value(value[key], child_schema, path=f"{path}.{key}", resolver=resolver))
    return errors


def require_valid(value: Any, schema: dict, *, name: str, resolver=None) -> None:
    errors = validate_value(value, schema, path=name, resolver=resolver)
    if errors:
        raise ValidationError("; ".join(errors[:50]))


def require_rows_valid(rows: list[dict], schema: dict, *, artifact_id: str, resolver=None) -> None:
    errors: list[str] = []
    for index, row in enumerate(rows):
        errors.extend(validate_value(row, schema, path=f"{artifact_id}[{index}]", resolver=resolver))
        if len(errors) >= 50:
            break
    if errors:
        raise ValidationError("; ".join(errors), artifact_id=artifact_id)


def require_unique(rows: Iterable[dict], field: str, *, artifact_id: str) -> None:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for row in rows:
        value = str(row.get(field, ""))
        if not value:
            raise ValidationError(f"{artifact_id} missing {field}", artifact_id=artifact_id)
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    if duplicates:
        raise ValidationError(f"{artifact_id} duplicate {field}: {', '.join(sorted(duplicates)[:20])}", artifact_id=artifact_id)


def index_by(rows: Iterable[dict], field: str, *, artifact_id: str) -> dict[str, dict]:
    rows = list(rows)
    require_unique(rows, field, artifact_id=artifact_id)
    return {str(row[field]): row for row in rows}


def require_foreign_keys(rows: Iterable[dict], field: str, valid: set[str], *, artifact_id: str, allow_empty: bool = False) -> None:
    missing: set[str] = set()
    for row in rows:
        value = row.get(field, "")
        values = value if isinstance(value, list) else [value]
        for item in values:
            item = str(item)
            if not item and allow_empty:
                continue
            if item not in valid:
                missing.add(item or "<empty>")
    if missing:
        raise ValidationError(f"{artifact_id}.{field} references unknown ids: {', '.join(sorted(missing)[:20])}", artifact_id=artifact_id)


def gate_result(gate_id: str, errors: list[str], warnings: list[str], input_hashes: dict, output_hashes: dict, **metrics: Any) -> dict:
    return {
        "gate_id": gate_id,
        "status": "failed" if errors else "passed",
        **metrics,
        "blocking_errors": errors,
        "warnings": warnings,
        "input_hashes": input_hashes,
        "output_hashes": output_hashes,
    }
