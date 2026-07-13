#!/usr/bin/env python3
"""Validate core-prompt-slots.md without writing rendered outputs."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import List

from artifact_manifest import ManifestError, resolve_artifact
from render_core_prompts import SLOT_SECTION_KEYWORDS, SlotError, extract_first_table, load_render_templates, render_tasks


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate core-prompt-slots.md")
    parser.add_argument("--artifact-manifest", required=True, type=Path)
    parser.add_argument(
        "--templates",
        default=Path(__file__).resolve().parents[1] / "references" / "templates" / "core-prompt-render-templates.json",
        type=Path,
    )
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args(argv)

    errors: List[str] = []
    try:
        slots_path = resolve_artifact(
            args.artifact_manifest,
            "core-prompt-slots",
            expected_role="production_source",
            expected_type="markdown_table",
            must_exist=True,
        )
        rows = extract_first_table(slots_path.read_text(encoding="utf-8-sig").splitlines(), SLOT_SECTION_KEYWORDS)
        rendered = render_tasks(rows, load_render_templates(args.templates))
        if len(rendered) != len({row["task_id"] for row in rendered}):
            errors.append("rendered prompt row count does not match unique task count")
    except (SlotError, ManifestError, OSError) as exc:
        errors.append(str(exc))

    if args.format == "json":
        print(json.dumps({"valid": not errors, "errors": errors}, ensure_ascii=False, indent=2))
    else:
        if errors:
            for error in errors:
                print(f"ERROR: {error}", file=sys.stderr)
        else:
            print("core-prompt-slots.md valid")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
