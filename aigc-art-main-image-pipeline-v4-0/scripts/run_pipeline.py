#!/usr/bin/env python3
"""V4 run bootstrap, status, and node dispatcher."""
from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))
from core.contract_registry import CONTRACT_PATH, artifact_schema, load_contract, node_by_id, resource_hashes, validate_contract_data
from core.errors import ContractError, InputError
from core.execution import execute_node
from core.ids import make_run_id
from core.storage import atomic_write_text, load_manifest, save_manifest, sha256_file, utc_now
from core.validator import require_valid


def initialize(args) -> Path:
    source = args.source.resolve()
    if not source.is_file():
        raise InputError(f"Source file does not exist: {source}")
    output = args.output_dir.resolve()
    manifest_path = output / "run-manifest.json"
    if manifest_path.exists():
        raise InputError(f"Run manifest already exists: {manifest_path}")
    output.mkdir(parents=True, exist_ok=True)
    contract = load_contract()
    errors = validate_contract_data(contract)
    if errors:
        raise ContractError("Invalid pipeline contract: " + "; ".join(errors))
    source_hash = sha256_file(source)
    run_id = make_run_id(args.project_id, source_hash)
    artifacts = {}
    for artifact_id, artifact in contract["artifacts"].items():
        artifacts[artifact_id] = {
            "path": artifact["path"], "artifact_type": artifact["artifact_type"], "role": artifact["role"],
            "schema": artifact["schema"], "producer": artifact["producer"], "consumers": artifact["consumers"],
            "required": artifact["required"], "status": "pending", "sha256": "", "bytes": 0,
        }
        (output / artifact["path"]).parent.mkdir(parents=True, exist_ok=True)
    nodes = {node["id"]: {"status": "pending", "input_hashes": {}, "output_hashes": {}, "error": ""} for node in contract["nodes"]}
    nodes["run-bootstrap"].update({"status": "passed", "completed_at": utc_now()})
    artifacts["run-manifest"]["status"] = "ready"
    manifest = {
        "schema_version": "aigc-main-image-run.v4", "run_id": run_id, "project_id": args.project_id,
        "created_at": utc_now(),
        "source": {"path": str(source), "sha256": source_hash},
        "skill": {"id": contract["skill_id"], "version": contract["skill_version"]},
        "contract": {"path": str(CONTRACT_PATH), "sha256": sha256_file(CONTRACT_PATH)},
        "resources": resource_hashes(),
        "options": {"include_human_views": bool(args.include_human_views), "project_title": args.project_title or "", "content_id": args.content_id or ""},
        "artifacts": artifacts, "nodes": nodes,
    }
    schema, resolver = artifact_schema("run-manifest")
    require_valid(manifest, schema, name="run-manifest", resolver=resolver)
    atomic_write_text(manifest_path, json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print(manifest_path)
    return manifest_path


def dispatch(manifest_path: Path, node_id: str) -> int:
    if node_id == "run-bootstrap":
        print("run-bootstrap already completed by init")
        return 0
    from ingest import NODE_HANDLERS as INGEST
    from recognition import NODE_HANDLERS as RECOGNITION
    from planning import NODE_HANDLERS as PLANNING
    from visual import NODE_HANDLERS as VISUAL
    from delivery import NODE_HANDLERS as DELIVERY
    handlers = {**INGEST, **RECOGNITION, **PLANNING, **VISUAL, **DELIVERY}
    if node_id not in handlers:
        raise ContractError(f"No handler registered for node: {node_id}")
    return execute_node(manifest_path.resolve(), node_id, handlers[node_id])


def show_status(manifest_path: Path) -> None:
    manifest = load_manifest(manifest_path)
    contract = load_contract()
    for node in contract["nodes"]:
        state = manifest["nodes"][node["id"]]
        print(f"{node['order']:02d} {node['mode']:4} {state['status']:8} {node['id']}")


def show_next(manifest_path: Path) -> None:
    manifest = load_manifest(manifest_path); contract = load_contract()
    for node in contract["nodes"]:
        if manifest["nodes"][node["id"]]["status"] != "pending":
            continue
        if all(manifest["nodes"][dep]["status"] == "passed" for dep in node["depends_on"]):
            print(json.dumps({"node": node["id"], "mode": node["mode"], "inputs": node["inputs"], "model_produces": node["model_produces"], "rules": node.get("rules", [])}, ensure_ascii=False, indent=2))
            return
    print("No executable pending node")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(); sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init"); init.add_argument("--source", required=True, type=Path); init.add_argument("--output-dir", required=True, type=Path); init.add_argument("--project-id", required=True); init.add_argument("--project-title", default=""); init.add_argument("--content-id", default=""); init.add_argument("--include-human-views", action="store_true")
    run = sub.add_parser("run-node"); run.add_argument("--run-manifest", required=True, type=Path); run.add_argument("--node", required=True)
    status = sub.add_parser("status"); status.add_argument("--run-manifest", required=True, type=Path)
    nxt = sub.add_parser("next"); nxt.add_argument("--run-manifest", required=True, type=Path)
    sub.add_parser("validate-contract")
    args = parser.parse_args(argv)
    try:
        if args.command == "init": initialize(args); return 0
        if args.command == "run-node": return dispatch(args.run_manifest, args.node)
        if args.command == "status": show_status(args.run_manifest); return 0
        if args.command == "next": show_next(args.run_manifest); return 0
        errors = validate_contract_data()
        if errors:
            for error in errors: print(f"ERROR: {error}", file=sys.stderr)
            return 1
        print("pipeline contract valid"); return 0
    except (ContractError, InputError, OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr); return 1

if __name__ == "__main__": raise SystemExit(main())
