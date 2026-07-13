#!/usr/bin/env python3
"""Module 4: evidence-bound anchors, slots, deterministic prompts, and production source."""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

SCRIPTS=Path(__file__).resolve().parent
sys.path.insert(0,str(SCRIPTS))
from core.contract_registry import SKILL_ROOT
from core.errors import IntegrityError
from core.execution import execute_node
from core.ids import stable_id
from core.model_gateway import load_model_rows
from core.storage import artifact_path, file_hashes, read_jsonl, write_json, write_jsonl
from core.validator import gate_result, index_by

EVIDENCE_ARTIFACTS=["character-evidence","scene-evidence","prop-evidence"]

def _evidence_ids(manifest_path):
    return {row["evidence_id"] for artifact_id in EVIDENCE_ARTIFACTS for row in read_jsonl(artifact_path(manifest_path,artifact_id,must_exist=True))}

def _template():
    return json.loads((SKILL_ROOT/"templates"/"prompt-render.json").read_text(encoding="utf-8-sig"))

def _key(asset_type,task_type):
    return f"{asset_type}:{task_type}"

def asset_anchor(manifest_path: Path) -> None:
    tasks=read_jsonl(artifact_path(manifest_path,"production-tasks",must_exist=True))
    registry=index_by(read_jsonl(artifact_path(manifest_path,"base-asset-registry",must_exist=True)),"base_asset_id",artifact_id="base-asset-registry")
    evidence_ids=_evidence_ids(manifest_path)
    factors=load_model_rows(manifest_path,"asset-anchor")["anchor-facts"]
    factor_by=index_by(factors,"base_asset_id",artifact_id="anchor-facts")
    production_bases={task["base_asset_id"] for task in tasks}
    if set(factor_by)!=production_bases:
        raise IntegrityError(f"anchor factors must cover production bases exactly; missing={sorted(production_bases-set(factor_by))[:20]}")
    base_tasks={task["base_asset_id"]:task for task in tasks if not task["state_asset_id"]}
    rows=[]
    for base_id in sorted(production_bases):
        factor=factor_by[base_id]
        if not set(factor["evidence_ids"]).issubset(evidence_ids):
            raise IntegrityError(f"anchor references unknown evidence: {base_id}")
        rows.append({"anchor_id":stable_id("anchor",base_id),"base_asset_id":base_id,"asset_type":registry[base_id]["asset_type"],"anchor_task_id":base_tasks[base_id]["task_id"],"anchor_summary":factor["anchor_summary"].strip(),"identity_or_structure":factor["identity_or_structure"].strip(),"evidence_ids":factor["evidence_ids"],"constraints":factor["constraints"]})
    write_jsonl(artifact_path(manifest_path,"asset-anchors"),rows)

def prompt_slots(manifest_path: Path) -> None:
    tasks=index_by(read_jsonl(artifact_path(manifest_path,"production-tasks",must_exist=True)),"task_id",artifact_id="production-tasks")
    index_by(read_jsonl(artifact_path(manifest_path,"asset-anchors",must_exist=True)),"base_asset_id",artifact_id="asset-anchors")
    evidence_ids=_evidence_ids(manifest_path); template=_template()
    factors=load_model_rows(manifest_path,"prompt-slots")["prompt-slot-facts"]
    factor_by=index_by(factors,"task_id",artifact_id="prompt-slot-facts")
    if set(factor_by)!=set(tasks):
        raise IntegrityError(f"prompt slot factors must cover tasks exactly; missing={sorted(set(tasks)-set(factor_by))[:20]}")
    rows=[]
    for task_id,task in tasks.items():
        factor=factor_by[task_id]
        if not set(factor["evidence_ids"]).issubset(evidence_ids):
            raise IntegrityError(f"prompt slots reference unknown evidence: {task_id}")
        key=_key(task["asset_type"],task["task_type"]); definition=template["templates"].get(key)
        if not definition: raise IntegrityError(f"No prompt template for {key}")
        slots=dict(factor["slots"])
        if task["task_type"]=="image_text_edit": slots["identity_reference_image"]=task["anchor_task_id"]
        missing=[name for name in definition["required_slots"] if not str(slots.get(name,"")).strip()]
        if missing: raise IntegrityError(f"task {task_id} missing prompt slots: {', '.join(missing)}")
        rows.append({"task_id":task_id,"base_asset_id":task["base_asset_id"],"state_asset_id":task["state_asset_id"],"asset_type":task["asset_type"],"task_type":task["task_type"],"slots":slots,"evidence_ids":factor["evidence_ids"],"quality_focus":factor["quality_focus"].strip()})
    write_jsonl(artifact_path(manifest_path,"prompt-slots"),rows)

def prompt_render(manifest_path: Path) -> None:
    slots=read_jsonl(artifact_path(manifest_path,"prompt-slots",must_exist=True)); template=_template(); rows=[]
    for row in slots:
        key=_key(row["asset_type"],row["task_type"]); definition=template["templates"][key]
        negative_key="image_text_edit" if row["task_type"]=="image_text_edit" else row["asset_type"]
        negative=template["negative_prompts"][negative_key]
        values={**row["slots"],"negative_prompt":negative}
        try: rendered=definition["text"].format(**values)
        except KeyError as exc: raise IntegrityError(f"task {row['task_id']} missing render slot: {exc}") from exc
        rows.append({"task_id":row["task_id"],"prompt":rendered if definition["target_field"]=="prompt" else "","edit_instruction":rendered if definition["target_field"]=="edit_instruction" else "","negative_prompt":negative,"template_key":key,"evidence_ids":row["evidence_ids"]})
    write_jsonl(artifact_path(manifest_path,"rendered-prompts"),rows)

def production_source(manifest_path: Path) -> None:
    tasks=index_by(read_jsonl(artifact_path(manifest_path,"production-tasks",must_exist=True)),"task_id",artifact_id="production-tasks")
    registry=index_by(read_jsonl(artifact_path(manifest_path,"base-asset-registry",must_exist=True)),"base_asset_id",artifact_id="base-asset-registry")
    prompts=index_by(read_jsonl(artifact_path(manifest_path,"rendered-prompts",must_exist=True)),"task_id",artifact_id="rendered-prompts")
    slots=index_by(read_jsonl(artifact_path(manifest_path,"prompt-slots",must_exist=True)),"task_id",artifact_id="prompt-slots")
    usage=read_jsonl(artifact_path(manifest_path,"episode-usage-map",must_exist=True))
    usage_by=defaultdict(list)
    for row in usage: usage_by[row["task_id"]].append(row)
    if set(tasks)!=set(prompts) or set(tasks)!=set(slots): raise IntegrityError("task/prompt/slot task_id sets differ")
    rows=[]
    for task_id,task in tasks.items():
        base=registry[task["base_asset_id"]]; prompt=prompts[task_id]; slot=slots[task_id]
        episode_ids=sorted({row["episode_id"] for row in usage_by[task_id] if row["episode_id"]}) or task["episode_ids"]
        scene_ids=sorted({scene for row in usage_by[task_id] for scene in row["scene_ids"]}) or task["scene_ids"]
        evidence_ids=sorted(set(task["evidence_ids"])|set(prompt["evidence_ids"]))
        rows.append({"task_id":task_id,"base_asset_id":task["base_asset_id"],"state_asset_id":task["state_asset_id"],"asset_type":task["asset_type"],"asset_name":task["asset_name"],"state_name":task["state_name"],"priority_level":task["priority_level"],"task_type":task["task_type"],"anchor_task_id":task["anchor_task_id"],"status":"ready","episode_ids":episode_ids,"scene_ids":scene_ids,"evidence_ids":evidence_ids,"prompt":prompt["prompt"],"edit_instruction":prompt["edit_instruction"],"negative_prompt":prompt["negative_prompt"],"quality_focus":slot["quality_focus"]})
    write_jsonl(artifact_path(manifest_path,"main-image-production-source"),rows)

def prompt_closure(manifest_path: Path) -> None:
    tasks=read_jsonl(artifact_path(manifest_path,"production-tasks",must_exist=True)); anchors=read_jsonl(artifact_path(manifest_path,"asset-anchors",must_exist=True)); slots=read_jsonl(artifact_path(manifest_path,"prompt-slots",must_exist=True)); prompts=read_jsonl(artifact_path(manifest_path,"rendered-prompts",must_exist=True)); source=read_jsonl(artifact_path(manifest_path,"main-image-production-source",must_exist=True))
    errors=[]; task_ids={r["task_id"] for r in tasks}; slot_ids={r["task_id"] for r in slots}; prompt_ids={r["task_id"] for r in prompts}; source_ids={r["task_id"] for r in source}; base_ids={r["base_asset_id"] for r in tasks}; anchor_bases={r["base_asset_id"] for r in anchors}
    if not (task_ids==slot_ids==prompt_ids==source_ids): errors.append("task/slot/render/source task_id sets differ")
    if base_ids!=anchor_bases: errors.append("production base/anchor sets differ")
    policy=task_policy(); ratios=policy["image_ratios"]
    for row in source:
        if row["task_type"]=="image_text_edit":
            anchor=next((task for task in tasks if task["task_id"]==row["anchor_task_id"]),None)
            if not anchor or anchor["base_asset_id"]!=row["base_asset_id"] or anchor["asset_type"]!="character": errors.append(f"invalid edit anchor: {row['task_id']}")
        if not row["prompt"] and not row["edit_instruction"]: errors.append(f"empty rendered content: {row['task_id']}")
    result=gate_result("prompt-closure-gate",errors,[],file_hashes(manifest_path,["production-tasks","asset-anchors","prompt-slots","rendered-prompts","main-image-production-source"]),{},task_count=len(tasks),prompt_count=len(prompts),source_count=len(source))
    write_json(artifact_path(manifest_path,"prompt-closure"),result)
    if errors: raise IntegrityError("; ".join(errors))

from core.policy_engine import task_policy
NODE_HANDLERS={"asset-anchor":asset_anchor,"prompt-slots":prompt_slots,"prompt-render":prompt_render,"production-source":production_source,"prompt-closure-gate":prompt_closure}
ACTION_TO_NODE={"asset-anchor":"asset-anchor","prompt-slots":"prompt-slots","prompt-render":"prompt-render","production-source":"production-source","prompt-closure":"prompt-closure-gate"}
def main(argv=None):
    parser=argparse.ArgumentParser(); parser.add_argument("--run-manifest",required=True,type=Path); parser.add_argument("--action",required=True,choices=sorted(ACTION_TO_NODE)); args=parser.parse_args(argv); node=ACTION_TO_NODE[args.action]; return execute_node(args.run_manifest.resolve(),node,NODE_HANDLERS[node])
if __name__=="__main__": raise SystemExit(main())
