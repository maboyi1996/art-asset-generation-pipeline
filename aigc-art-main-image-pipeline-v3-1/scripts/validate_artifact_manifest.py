#!/usr/bin/env python3
"""Validate artifact-manifest.json for V3.1 project outputs."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import List

from artifact_manifest import load_manifest, validate_manifest_data


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate artifact-manifest.json")
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args(argv)

    try:
        data = json.loads(args.manifest.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        errors = [f"invalid JSON: {exc}"]
    except OSError as exc:
        errors = [str(exc)]
    else:
        if not isinstance(data, dict):
            errors = ["manifest root must be an object"]
        else:
            errors = validate_manifest_data(data, args.manifest)

    if args.format == "json":
        print(json.dumps({"valid": not errors, "errors": errors}, ensure_ascii=False, indent=2))
    else:
        if errors:
            for error in errors:
                print(f"ERROR: {error}", file=sys.stderr)
        else:
            print("artifact-manifest.json valid")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
