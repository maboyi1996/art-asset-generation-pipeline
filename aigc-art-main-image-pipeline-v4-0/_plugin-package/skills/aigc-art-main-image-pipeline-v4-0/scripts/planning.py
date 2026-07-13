#!/usr/bin/env python3
"""Module 3: deterministic admission, rating, registration, state, disposition, tasks, and usage."""
from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path

SCRIPTS=Path(__file__).resolve().parent; sys.path.insert(0,str(SCRIPTS))
from core.errors import IntegrityError
from core.execution import execute_node
from core.ids import stable_id
from core.model_gateway import load_model_rows
from core.policy_engine import admission_result, disposition_result, rating_level, state_result, task_policy
from core.storage import artifact_path, file_hashes, read_jsonl, write_json, write_jsonl
from core.validator import gate_result, index_by

EVIDENCE_ARTIFACTS=["character-evidence","scene-evidence","prop-evidence"]
def _evidence(manifest_path): return [r for aid in EVIDENCE_ARTIFACTS for r in read_jsonl(artifact_path(manifest_path,aid,must_exist=True))]

def candidate_admission(manifest_path: Path) -> None:
    entities=index_by(read_jsonl(artifact_path(manifest_path,"asset-entities",must_exist=True)),"entity_id",artifact_id="asset-entities"); evidence=_evidence(manifest_path); evidence_by=defaultdict(list)
    for row in evidence: evidence_by[row["entity_id"]].append(row)
    factors=load_model_rows(manifest_path,"candidate-admission")["admission-factors"]; factor_by=index_by(factors,"entity_id",artifact_id="admission-factors")
    if set(factor_by)!=set(entities): raise IntegrityError(f"admission factors must cover every entity; missing={sorted(set(entities)-set(factor_by))[:20]}")
    candidates=[]; dispositions=[]; polluted=[]
    for entity_id,entity in entities.items():
        factor=factor_by[entity_id]; result,reason=admission_result(factor); candidate_id=""
        if result=="admitted":
            candidate_id=stable_id("candidate",entity_id)
            ev=evidence_by[entity_id]
            candidates.append({"candidate_id":candidate_id,"entity_id":entity_id,"asset_type":entity["asset_type"],"asset_name":entity["canonical_name"],"candidate_scope":factor["candidate_scope"],"scene_ids":entity["scene_ids"],"episode_ids":entity["episode_ids"],"evidence_ids":[r["evidence_id"] for r in ev],"admission_result":"admitted","admission_reason":reason})
        dispositions.append({"entity_id":entity_id,"result":result,"reason":reason,"candidate_id":candidate_id})
        if result=="polluted_exclusion": polluted.append({"entity_id":entity_id,"asset_type":entity["asset_type"],"raw_label":entity["canonical_name"],"reason":reason})
    write_jsonl(artifact_path(manifest_path,"asset-candidates"),candidates); write_jsonl(artifact_path(manifest_path,"admission-dispositions"),dispositions); write_jsonl(artifact_path(manifest_path,"polluted-labels"),polluted)

def asset_rating(manifest_path: Path) -> None:
    candidates=index_by(read_jsonl(artifact_path(manifest_path,"asset-candidates",must_exist=True)),"candidate_id",artifact_id="asset-candidates")
    factors=load_model_rows(manifest_path,"asset-rating")["rating-factors"]; factor_by=index_by(factors,"candidate_id",artifact_id="rating-factors")
    if set(factor_by)!=set(candidates): raise IntegrityError(f"rating factors must cover every candidate; missing={sorted(set(candidates)-set(factor_by))[:20]}")
    rows=[]
    for candidate_id,candidate in candidates.items():
        factor=factor_by[candidate_id]
        if not set(factor["evidence_ids"]).issubset(set(candidate["evidence_ids"])): raise IntegrityError(f"rating factor references evidence outside candidate: {candidate_id}")
        level,reason=rating_level(candidate["asset_type"],factor)
        rows.append({"candidate_id":candidate_id,"asset_type":candidate["asset_type"],"asset_name":candidate["asset_name"],"priority_level":level,"evidence_ids":factor["evidence_ids"],"episode_ids":sorted(set(factor["visible_episode_ids"])),"scene_ids":sorted(set(factor["scene_ids"])),"rating_reason":reason})
    write_jsonl(artifact_path(manifest_path,"asset-ratings"),rows)

def base_registration(manifest_path: Path) -> None:
    candidates=index_by(read_jsonl(artifact_path(manifest_path,"asset-candidates",must_exist=True)),"candidate_id",artifact_id="asset-candidates"); ratings=index_by(read_jsonl(artifact_path(manifest_path,"asset-ratings",must_exist=True)),"candidate_id",artifact_id="asset-ratings")
    if set(candidates)!=set(ratings): raise IntegrityError("candidate and rating sets differ")
    rows=[]
    for candidate_id,c in candidates.items():
        r=ratings[candidate_id]; rows.append({"base_asset_id":stable_id("base",c["asset_type"],c["entity_id"]),"candidate_id":candidate_id,"entity_id":c["entity_id"],"asset_type":c["asset_type"],"asset_name":c["asset_name"],"priority_level":r["priority_level"],"evidence_ids":c["evidence_ids"],"episode_ids":r["episode_ids"] or c["episode_ids"],"scene_ids":r["scene_ids"] or c["scene_ids"]})
    write_jsonl(artifact_path(manifest_path,"base-asset-registry"),rows)

def state_variant(manifest_path: Path) -> None:
    registry=index_by(read_jsonl(artifact_path(manifest_path,"base-asset-registry",must_exist=True)),"base_asset_id",artifact_id="base-asset-registry"); evidence={r["evidence_id"]:r for r in _evidence(manifest_path)}
    factors=load_model_rows(manifest_path,"state-variant")["state-factors"]
    states=[]; dispositions=[]; seen=set()
    for factor in factors:
        base_id=factor["base_asset_id"]
        if base_id not in registry: raise IntegrityError(f"state factor references unknown base asset: {base_id}")
        key=(base_id,factor["state_name"].strip(),factor["reuse_state_key"].strip())
        if key in seen: raise IntegrityError(f"duplicate state factor: {key}")
        seen.add(key)
        if not set(factor["source_evidence_ids"]).issubset(evidence): raise IntegrityError(f"state factor references unknown evidence: {base_id}")
        result,reason=state_result(registry[base_id]["priority_level"],factor); state_id=""
        if result=="created":
            state_id=stable_id("state",base_id,factor["reuse_state_key"] or factor["state_name"])
            episode_ids=sorted({evidence[eid]["episode_id"] for eid in factor["source_evidence_ids"]})
            states.append({"state_asset_id":state_id,"base_asset_id":base_id,"asset_type":registry[base_id]["asset_type"],"state_name":factor["state_name"].strip(),"source_evidence_ids":factor["source_evidence_ids"],"scene_ids":sorted(set(factor["scene_ids"])),"episode_ids":episode_ids,"visual_difference":factor["visual_difference"].strip(),"state_basis_type":factor["state_basis_type"].strip()})
        dispositions.append({"base_asset_id":base_id,"state_name":factor["state_name"].strip(),"result":result,"reason":reason,"state_asset_id":state_id})
    write_jsonl(artifact_path(manifest_path,"asset-states"),states); write_jsonl(artifact_path(manifest_path,"state-dispositions"),dispositions)

def asset_disposition(manifest_path: Path) -> None:
    registry=index_by(read_jsonl(artifact_path(manifest_path,"base-asset-registry",must_exist=True)),"base_asset_id",artifact_id="base-asset-registry")
    factors=load_model_rows(manifest_path,"asset-disposition")["disposition-factors"]; factor_by=index_by(factors,"base_asset_id",artifact_id="disposition-factors")
    if set(factor_by)!=set(registry): raise IntegrityError(f"disposition factors must cover registry exactly; missing={sorted(set(registry)-set(factor_by))[:20]}")
    rows=[]
    for base_id,base in registry.items():
        result,target,reason=disposition_result(factor_by[base_id])
        if target and target not in registry: raise IntegrityError(f"disposition target does not exist: {target}")
        rows.append({"base_asset_id":base_id,"asset_type":base["asset_type"],"priority_level":base["priority_level"],"final_disposition":result,"target_base_asset_id":target,"reason":reason})
    write_jsonl(artifact_path(manifest_path,"asset-dispositions"),rows)

def task_generation(manifest_path: Path) -> None:
    registry=index_by(read_jsonl(artifact_path(manifest_path,"base-asset-registry",must_exist=True)),"base_asset_id",artifact_id="base-asset-registry"); dispositions=index_by(read_jsonl(artifact_path(manifest_path,"asset-dispositions",must_exist=True)),"base_asset_id",artifact_id="asset-dispositions"); states=read_jsonl(artifact_path(manifest_path,"asset-states",must_exist=True)); states_by=defaultdict(list)
    for state in states: states_by[state["base_asset_id"]].append(state)
    rows=[]; base_task={}
    for base_id,base in registry.items():
        if dispositions[base_id]["final_disposition"]!="production_task": continue
        task_id=stable_id("task",base_id,"base"); base_task[base_id]=task_id
        rows.append({"task_id":task_id,"base_asset_id":base_id,"state_asset_id":"","asset_type":base["asset_type"],"asset_name":base["asset_name"],"state_name":"默认状态","priority_level":base["priority_level"],"task_type":"text_to_image","anchor_task_id":"","status":"ready","evidence_ids":base["evidence_ids"],"scene_ids":base["scene_ids"],"episode_ids":base["episode_ids"]})
    for base_id,items in states_by.items():
        if base_id not in base_task: continue
        base=registry[base_id]
        if base["priority_level"] in {"B","C"}: raise IntegrityError(f"B/C asset must not contain states: {base_id}")
        for state in items:
            method="image_text_edit" if base["asset_type"]=="character" else "text_to_image"
            rows.append({"task_id":stable_id("task",base_id,state["state_asset_id"]),"base_asset_id":base_id,"state_asset_id":state["state_asset_id"],"asset_type":base["asset_type"],"asset_name":base["asset_name"],"state_name":state["state_name"],"priority_level":base["priority_level"],"task_type":method,"anchor_task_id":base_task[base_id] if method=="image_text_edit" else "","status":"ready","evidence_ids":state["source_evidence_ids"],"scene_ids":state["scene_ids"],"episode_ids":state["episode_ids"]})
    write_jsonl(artifact_path(manifest_path,"production-tasks"),rows)

def episode_usage_map(manifest_path: Path) -> None:
    tasks=read_jsonl(artifact_path(manifest_path,"production-tasks",must_exist=True)); rows=[]
    for task in tasks:
        episodes=task["episode_ids"] or [""]
        for episode_id in episodes:
            rows.append({"usage_id":stable_id("usage",task["task_id"],episode_id),"task_id":task["task_id"],"episode_id":episode_id,"scene_ids":task["scene_ids"],"evidence_ids":task["evidence_ids"]})
    write_jsonl(artifact_path(manifest_path,"episode-usage-map"),rows)

def planning_closure(manifest_path: Path) -> None:
    candidates=read_jsonl(artifact_path(manifest_path,"asset-candidates",must_exist=True)); ratings=read_jsonl(artifact_path(manifest_path,"asset-ratings",must_exist=True)); registry=read_jsonl(artifact_path(manifest_path,"base-asset-registry",must_exist=True)); states=read_jsonl(artifact_path(manifest_path,"asset-states",must_exist=True)); dispositions=read_jsonl(artifact_path(manifest_path,"asset-dispositions",must_exist=True)); tasks=read_jsonl(artifact_path(manifest_path,"production-tasks",must_exist=True)); usage=read_jsonl(artifact_path(manifest_path,"episode-usage-map",must_exist=True)); admission=read_jsonl(artifact_path(manifest_path,"admission-dispositions",must_exist=True))
    evidence_ids={r["evidence_id"] for r in _evidence(manifest_path)}
    errors=[]; candidate_ids={r["candidate_id"] for r in candidates}; rating_ids={r["candidate_id"] for r in ratings}; registry_candidates={r["candidate_id"] for r in registry}; base_ids={r["base_asset_id"] for r in registry}; state_ids={r["state_asset_id"] for r in states}; disp_ids={r["base_asset_id"] for r in dispositions}; task_ids={r["task_id"] for r in tasks}; usage_task_ids={r["task_id"] for r in usage}
    if candidate_ids!=rating_ids or candidate_ids!=registry_candidates: errors.append("candidate/rating/registry candidate sets differ")
    if base_ids!=disp_ids: errors.append("registry/disposition base sets differ")
    for row in candidates:
        if not set(row["evidence_ids"]).issubset(evidence_ids): errors.append(f"candidate references unknown evidence: {row['candidate_id']}")
    for row in ratings:
        if not set(row["evidence_ids"]).issubset(evidence_ids): errors.append(f"rating references unknown evidence: {row['candidate_id']}")
    for row in registry:
        if not set(row["evidence_ids"]).issubset(evidence_ids): errors.append(f"registry references unknown evidence: {row['base_asset_id']}")
    for task in tasks:
        if task["base_asset_id"] not in base_ids: errors.append(f"task references unknown base: {task['task_id']}")
        if task["state_asset_id"] and task["state_asset_id"] not in state_ids: errors.append(f"task references unknown state: {task['task_id']}")
        if task["task_type"]=="image_text_edit":
            anchor=next((x for x in tasks if x["task_id"]==task["anchor_task_id"]),None)
            if not anchor or anchor["base_asset_id"]!=task["base_asset_id"] or anchor["task_type"]!="text_to_image": errors.append(f"invalid image_text_edit anchor: {task['task_id']}")
    production_bases={r["base_asset_id"] for r in dispositions if r["final_disposition"]=="production_task"}; task_bases={r["base_asset_id"] for r in tasks}
    if production_bases!=task_bases: errors.append("production disposition/task base sets differ")
    if task_ids-usage_task_ids: errors.append(f"tasks missing usage rows: {sorted(task_ids-usage_task_ids)[:20]}")
    if any(r["result"] not in {"admitted","evidence_only","visible_exclusion","polluted_exclusion"} for r in admission): errors.append("invalid admission disposition")
    result=gate_result("planning-closure-gate",errors,[],file_hashes(manifest_path,["asset-candidates","asset-ratings","base-asset-registry","asset-states","state-dispositions","asset-dispositions","production-tasks","episode-usage-map","admission-dispositions","polluted-labels"]),{},candidate_count=len(candidates),registry_count=len(registry),task_count=len(tasks))
    write_json(artifact_path(manifest_path,"planning-closure"),result)
    if errors: raise IntegrityError("; ".join(errors))

NODE_HANDLERS={"candidate-admission":candidate_admission,"asset-rating":asset_rating,"base-asset-registration":base_registration,"state-variant":state_variant,"asset-disposition":asset_disposition,"task-generation":task_generation,"episode-usage-map":episode_usage_map,"planning-closure-gate":planning_closure}
ACTION_TO_NODE={"candidate-admission":"candidate-admission","asset-rating":"asset-rating","base-registration":"base-asset-registration","state-variant":"state-variant","asset-disposition":"asset-disposition","task-generation":"task-generation","episode-usage-map":"episode-usage-map","planning-closure":"planning-closure-gate"}
def main(argv=None):
    parser=argparse.ArgumentParser(); parser.add_argument("--run-manifest",required=True,type=Path); parser.add_argument("--action",required=True,choices=sorted(ACTION_TO_NODE)); args=parser.parse_args(argv); node=ACTION_TO_NODE[args.action]; return execute_node(args.run_manifest.resolve(),node,NODE_HANDLERS[node])
if __name__=="__main__": raise SystemExit(main())
