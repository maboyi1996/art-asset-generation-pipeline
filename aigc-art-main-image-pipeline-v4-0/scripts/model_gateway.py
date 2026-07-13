#!/usr/bin/env python3
"""Merge and validate chunked model factor parts for long scripts."""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
SCRIPTS=Path(__file__).resolve().parent; sys.path.insert(0,str(SCRIPTS))
from core.contract_registry import node_by_id
from core.errors import ContractError,IntegrityError,PipelineError
from core.model_gateway import load_model_rows
from core.storage import artifact_path,read_jsonl,write_jsonl

KEYS={
"scene-segmentation":lambda r:tuple(r["block_ids"]),
"mention-scan":lambda r:json.dumps(r,ensure_ascii=False,sort_keys=True),
"mention-confirmation":lambda r:r["mention_id"],
"entity-resolution":lambda r:r["mention_id"],
"evidence-ledger":lambda r:(r["mention_id"],r["source_evidence"]),
"candidate-admission":lambda r:r["entity_id"],
"asset-rating":lambda r:r["candidate_id"],
"state-variant":lambda r:(r["base_asset_id"],r["state_name"],r["reuse_state_key"]),
"asset-disposition":lambda r:r["base_asset_id"],
"asset-anchor":lambda r:r["base_asset_id"],
"prompt-slots":lambda r:r["task_id"],
}

def merge(manifest:Path,node_id:str,parts_dir:Path)->None:
    node=node_by_id(node_id); outputs=node.get("model_produces",[])
    if len(outputs)!=1: raise ContractError(f"node {node_id} must declare exactly one model factor artifact")
    files=sorted(parts_dir.glob("*.jsonl"))
    if not files: raise IntegrityError(f"no factor part files in {parts_dir}")
    key_fn=KEYS[node_id]; merged=[]; seen={}
    for file in files:
        for row in read_jsonl(file):
            key=key_fn(row)
            if key in seen and seen[key]!=row: raise IntegrityError(f"conflicting factor rows for key {key} in {file.name}")
            if key not in seen: seen[key]=row; merged.append(row)
    write_jsonl(artifact_path(manifest,outputs[0]),merged)
    load_model_rows(manifest,node_id)
    print(f"merged {len(files)} parts into {outputs[0]} ({len(merged)} rows)")

def main(argv=None)->int:
    parser=argparse.ArgumentParser(); sub=parser.add_subparsers(dest="command",required=True)
    m=sub.add_parser("merge"); m.add_argument("--run-manifest",required=True,type=Path); m.add_argument("--node",required=True,choices=sorted(KEYS)); m.add_argument("--parts-dir",required=True,type=Path)
    v=sub.add_parser("validate"); v.add_argument("--run-manifest",required=True,type=Path); v.add_argument("--node",required=True,choices=sorted(KEYS))
    args=parser.parse_args(argv)
    try:
        if args.command=="merge": merge(args.run_manifest.resolve(),args.node,args.parts_dir.resolve())
        else: load_model_rows(args.run_manifest.resolve(),args.node); print("model factors valid")
        return 0
    except (PipelineError,OSError,ValueError,KeyError) as exc:
        print(f"ERROR: {exc}",file=sys.stderr); return 1
if __name__=="__main__": raise SystemExit(main())
