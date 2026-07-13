#!/usr/bin/env python3
"""Validate V3.1.1 production-source/main-image-production-table.md."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import List

from artifact_manifest import ManifestError, resolve_artifact
from generate_prompt_manifest import ContractError, build_manifest


FORBIDDEN_AUDIT_SECTIONS = [
    "人物评级前证据账本",
    "场景评级前证据账本",
    "道具评级前证据账本",
    "人物候选去向审计表",
    "泛称/群体模板覆盖表",
    "污染标签清洗记录表",
    "状态线索去向表",
]


def validate_lean_source(path: Path) -> List[str]:
    errors: List[str] = []
    text = path.read_text(encoding="utf-8-sig")
    for forbidden in FORBIDDEN_AUDIT_SECTIONS:
        if forbidden in text:
            errors.append(f"production source must not contain full audit section: {forbidden}")
    try:
        build_manifest(path, content_id=None, project_title=None, skill_id="aigc-art-main-image-pipeline-v3-1-1", skill_version="3.1.1")
    except ContractError as exc:
        errors.append(str(exc))
    return errors


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate V3.1.1 production source table")
    parser.add_argument("--artifact-manifest", required=True, type=Path)
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args(argv)

    try:
        production_path = resolve_artifact(
            args.artifact_manifest,
            "main-image-production-table",
            expected_role="production_source",
            expected_type="markdown_table",
            must_exist=True,
        )
        errors = validate_lean_source(production_path)
    except (ManifestError, OSError) as exc:
        errors = [str(exc)]

    if args.format == "json":
        print(json.dumps({"valid": not errors, "errors": errors}, ensure_ascii=False, indent=2))
    else:
        if errors:
            for error in errors:
                print(f"ERROR: {error}", file=sys.stderr)
        else:
            print("main-image-production-table.md valid")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
