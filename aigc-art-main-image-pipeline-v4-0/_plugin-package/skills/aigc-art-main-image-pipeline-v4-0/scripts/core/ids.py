"""Deterministic identifiers for every V4 machine fact."""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PREFIXES = {
    "block": "BLK", "episode": "EP", "scene": "SC", "mention": "MEN",
    "entity": "ENT", "alias": "ALS", "evidence": "EVD", "candidate": "CAN",
    "base": "AST", "state": "STA", "task": "TSK", "usage": "USG", "anchor": "ANC",
}

def normalize(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): normalize(value[k]) for k in sorted(value)}
    if isinstance(value, (list, tuple, set)):
        return [normalize(v) for v in value]
    if isinstance(value, Path):
        return value.as_posix()
    if value is None:
        return ""
    return str(value).strip()

def stable_digest(*parts: Any, length: int = 16) -> str:
    payload = json.dumps(normalize(parts), ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:length]

def stable_id(kind: str, *parts: Any) -> str:
    prefix = PREFIXES.get(kind, re.sub(r"[^A-Za-z0-9]", "", kind).upper()[:4] or "ID")
    return f"{prefix}-{stable_digest(kind, *parts, length=12).upper()}"

def make_run_id(project_id: str, source_sha256: str) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"RUN-{stamp}-{stable_digest(project_id, source_sha256, length=8).upper()}"
