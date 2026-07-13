#!/usr/bin/env python3
"""Validate the single V4 pipeline contract."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))
from core.contract_registry import SKILL_ROOT, load_contract, validate_contract_data

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--json", action="store_true"); args = parser.parse_args(argv)
    errors = validate_contract_data(); contract = load_contract()
    for node in contract["nodes"]:
        for relative in {node["executor"].split(":",1)[0], node["validator"].split(":",1)[0]}:
            if relative.endswith(".py") and not (SKILL_ROOT / relative).exists(): errors.append(f"missing executable: {relative}")
    result = {"valid": not errors, "node_count": len(contract["nodes"]), "mode_counts": contract["architecture"]["mode_counts"], "artifact_count": len(contract["artifacts"]), "errors": errors}
    if args.json: print(json.dumps(result, ensure_ascii=False, indent=2))
    elif errors:
        for error in errors: print(f"ERROR: {error}", file=sys.stderr)
    else: print("pipeline contract valid: 26 nodes, 15 P / 6 M→P / 5 M+P / 0 model-only")
    return 1 if errors else 0
if __name__ == "__main__": raise SystemExit(main())
