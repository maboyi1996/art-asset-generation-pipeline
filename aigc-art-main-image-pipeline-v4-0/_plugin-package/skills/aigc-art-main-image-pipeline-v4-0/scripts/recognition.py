#!/usr/bin/env python3
"""Module 2: automated three-type mention, entity, and evidence closure."""
from __future__ import annotations

import argparse
import sys
from collections import Counter, defaultdict
from pathlib import Path

SCRIPTS=Path(__file__).resolve().parent; sys.path.insert(0,str(SCRIPTS))
from core.errors import IntegrityError
from core.execution import execute_node
from core.ids import stable_id
from core.model_gateway import load_model_rows
from core.storage import artifact_path, file_hashes, read_jsonl, write_json, write_jsonl
from core.validator import gate_result, index_by, require_foreign_keys, require_unique

ASSET_EVIDENCE_ARTIFACT={"character":"character-evidence","scene":"scene-evidence","prop":"prop-evidence"}

def mention_scan(manifest_path: Path) -> None:
    blocks=read_jsonl(artifact_path(manifest_path,"source-blocks",must_exist=True)); scenes=read_jsonl(artifact_path(manifest_path,"scenes",must_exist=True))
    block_ids={r["block_id"] for r in blocks}; scene_by_id=index_by(scenes,"scene_id",artifact_id="scenes")
    factors=load_model_rows(manifest_path,"mention-scan")["mention-scan-facts"]
    rows=[]; seen=set()
    for index,f in enumerate(factors):
        if f["block_id"] not in block_ids: raise IntegrityError(f"mention scan references unknown block {f['block_id']}")
        if f["scene_id"] not in scene_by_id or f["block_id"] not in scene_by_id[f["scene_id"]]["block_ids"]: raise IntegrityError("mention scan scene/block relationship invalid")
        key=(f["block_id"],f["scene_id"],f["asset_type"],f["raw_text"],f["source_quote"])
        if key in seen: continue
        seen.add(key)
        rows.append({"mention_id":stable_id("mention",*key),"block_id":f["block_id"],"scene_id":f["scene_id"],"asset_type":f["asset_type"],"raw_text":f["raw_text"].strip(),"normalized_hint":f["normalized_hint"].strip(),"presence_type":f["presence_type"].strip(),"is_visible":bool(f["is_visible"]),"source_quote":f["source_quote"].strip()})
    write_jsonl(artifact_path(manifest_path,"raw-asset-mentions"),rows)

def mention_confirmation(manifest_path: Path) -> None:
    mentions=read_jsonl(artifact_path(manifest_path,"raw-asset-mentions",must_exist=True)); by_id=index_by(mentions,"mention_id",artifact_id="raw-asset-mentions")
    factors=load_model_rows(manifest_path,"mention-confirmation")["mention-confirmation-facts"]
    factor_by_id=index_by(factors,"mention_id",artifact_id="mention-confirmation-facts")
    if set(factor_by_id)!=set(by_id):
        raise IntegrityError(f"mention confirmation must cover every raw mention; missing={sorted(set(by_id)-set(factor_by_id))[:20]}, extra={sorted(set(factor_by_id)-set(by_id))[:20]}")
    rows=[]
    for mention_id,mention in by_id.items():
        factor=factor_by_id[mention_id]; accepted=bool(factor["accepted"])
        if accepted and not factor["normalized_label"].strip(): raise IntegrityError(f"accepted mention missing normalized_label: {mention_id}")
        if not accepted and not factor["exclusion_reason"].strip(): raise IntegrityError(f"excluded mention missing exclusion_reason: {mention_id}")
        rows.append({"mention_id":mention_id,"status":"accepted" if accepted else "excluded","asset_type":factor["asset_type"],"normalized_label":factor["normalized_label"].strip(),"presence_type":factor["presence_type"].strip(),"exclusion_reason":factor["exclusion_reason"].strip(),"evidence_note":factor["evidence_note"].strip(),"scene_id":mention["scene_id"],"block_id":mention["block_id"]})
    write_jsonl(artifact_path(manifest_path,"mention-dispositions"),rows)

def entity_resolution(manifest_path: Path) -> None:
    dispositions=read_jsonl(artifact_path(manifest_path,"mention-dispositions",must_exist=True)); accepted={r["mention_id"]:r for r in dispositions if r["status"]=="accepted"}
    raw=index_by(read_jsonl(artifact_path(manifest_path,"raw-asset-mentions",must_exist=True)),"mention_id",artifact_id="raw-asset-mentions")
    scenes=index_by(read_jsonl(artifact_path(manifest_path,"scenes",must_exist=True)),"scene_id",artifact_id="scenes")
    factors=load_model_rows(manifest_path,"entity-resolution")["entity-relation-factors"]; factor_by=index_by(factors,"mention_id",artifact_id="entity-relation-factors")
    if set(factor_by)!=set(accepted): raise IntegrityError(f"entity relation factors must cover accepted mentions exactly; missing={sorted(set(accepted)-set(factor_by))[:20]}")
    groups=defaultdict(list)
    for mention_id,f in factor_by.items():
        if f["asset_type"]!=accepted[mention_id]["asset_type"]: raise IntegrityError(f"entity factor type mismatch: {mention_id}")
        groups[(f["asset_type"],f["canonical_name"].strip(),f["scope_key"].strip())].append(mention_id)
    entities=[]; aliases=[]
    for (asset_type,name,scope),mention_ids in sorted(groups.items()):
        entity_id=stable_id("entity",asset_type,name,scope)
        scene_ids=sorted({accepted[mid]["scene_id"] for mid in mention_ids}); episode_ids=sorted({scenes[sid]["episode_id"] for sid in scene_ids})
        entities.append({"entity_id":entity_id,"asset_type":asset_type,"canonical_name":name,"scope_key":scope,"mention_ids":sorted(mention_ids),"scene_ids":scene_ids,"episode_ids":episode_ids,"source_evidence":[raw[mid]["source_quote"] for mid in sorted(mention_ids)]})
        alias_groups=defaultdict(list)
        for mid in mention_ids:
            alias=raw[mid]["raw_text"].strip()
            if alias and alias!=name: alias_groups[alias].append(mid)
        for alias,mids in sorted(alias_groups.items()): aliases.append({"alias_id":stable_id("alias",entity_id,alias),"entity_id":entity_id,"alias":alias,"canonical_name":name,"mention_ids":sorted(mids)})
    write_jsonl(artifact_path(manifest_path,"asset-entities"),entities); write_jsonl(artifact_path(manifest_path,"asset-aliases"),aliases)

def evidence_ledger(manifest_path: Path) -> None:
    dispositions=read_jsonl(artifact_path(manifest_path,"mention-dispositions",must_exist=True)); accepted={r["mention_id"]:r for r in dispositions if r["status"]=="accepted"}
    entities=read_jsonl(artifact_path(manifest_path,"asset-entities",must_exist=True)); mention_entity={mid:e for e in entities for mid in e["mention_ids"]}
    scenes=index_by(read_jsonl(artifact_path(manifest_path,"scenes",must_exist=True)),"scene_id",artifact_id="scenes")
    factors=load_model_rows(manifest_path,"evidence-ledger")["evidence-facts"]; covered=Counter(); outputs={k:[] for k in ASSET_EVIDENCE_ARTIFACT}
    for index,f in enumerate(factors):
        mid=f["mention_id"]
        if mid not in accepted or mid not in mention_entity: raise IntegrityError(f"evidence factor references non-accepted mention: {mid}")
        covered[mid]+=1; disp=accepted[mid]; entity=mention_entity[mid]; scene=scenes[disp["scene_id"]]
        row={"evidence_id":stable_id("evidence",entity["asset_type"],entity["entity_id"],mid,index,f["source_evidence"]),"entity_id":entity["entity_id"],"mention_id":mid,"asset_type":entity["asset_type"],"canonical_name":entity["canonical_name"],"episode_id":scene["episode_id"],"scene_id":disp["scene_id"],"block_id":disp["block_id"],"source_evidence":f["source_evidence"].strip(),"visible_facts":f["visible_facts"],"design_clues":f["design_clues"],"state_clues":f["state_clues"]}
        outputs[entity["asset_type"]].append(row)
    missing=sorted(set(accepted)-set(covered))
    if missing: raise IntegrityError(f"accepted mentions missing evidence factors: {', '.join(missing[:20])}")
    for asset_type,artifact_id in ASSET_EVIDENCE_ARTIFACT.items(): write_jsonl(artifact_path(manifest_path,artifact_id),outputs[asset_type])

def recognition_closure(manifest_path: Path) -> None:
    mentions=read_jsonl(artifact_path(manifest_path,"raw-asset-mentions",must_exist=True)); dispositions=read_jsonl(artifact_path(manifest_path,"mention-dispositions",must_exist=True)); entities=read_jsonl(artifact_path(manifest_path,"asset-entities",must_exist=True)); aliases=read_jsonl(artifact_path(manifest_path,"asset-aliases",must_exist=True))
    evidence=[r for aid in ASSET_EVIDENCE_ARTIFACT.values() for r in read_jsonl(artifact_path(manifest_path,aid,must_exist=True))]
    errors=[]; mention_ids={r["mention_id"] for r in mentions}; disp_ids={r["mention_id"] for r in dispositions}; accepted={r["mention_id"] for r in dispositions if r["status"]=="accepted"}; entity_mentions={mid for e in entities for mid in e["mention_ids"]}; evidence_mentions={r["mention_id"] for r in evidence}; entity_ids={e["entity_id"] for e in entities}
    if mention_ids!=disp_ids: errors.append("raw mentions and dispositions differ")
    if accepted!=entity_mentions: errors.append("accepted mentions and entity mention sets differ")
    if accepted!=evidence_mentions: errors.append("accepted mentions and evidence mention sets differ")
    unknown_alias={a["entity_id"] for a in aliases}-entity_ids
    if unknown_alias: errors.append(f"aliases reference unknown entities: {sorted(unknown_alias)[:20]}")
    unknown_evidence={r["entity_id"] for r in evidence}-entity_ids
    if unknown_evidence: errors.append(f"evidence references unknown entities: {sorted(unknown_evidence)[:20]}")
    result=gate_result("recognition-closure-gate",errors,[],file_hashes(manifest_path,["raw-asset-mentions","mention-dispositions","asset-entities","asset-aliases","character-evidence","scene-evidence","prop-evidence"]),{},accepted_mentions=len(accepted),entities=len(entities),evidence_rows=len(evidence))
    write_json(artifact_path(manifest_path,"recognition-closure"),result)
    if errors: raise IntegrityError("; ".join(errors))

NODE_HANDLERS={"mention-scan":mention_scan,"mention-confirmation":mention_confirmation,"entity-resolution":entity_resolution,"evidence-ledger":evidence_ledger,"recognition-closure-gate":recognition_closure}
ACTION_TO_NODE={"mention-scan":"mention-scan","mention-confirmation":"mention-confirmation","entity-resolution":"entity-resolution","evidence-ledger":"evidence-ledger","recognition-closure":"recognition-closure-gate"}
def main(argv=None):
    parser=argparse.ArgumentParser(); parser.add_argument("--run-manifest",required=True,type=Path); parser.add_argument("--action",required=True,choices=sorted(ACTION_TO_NODE)); args=parser.parse_args(argv); node=ACTION_TO_NODE[args.action]; return execute_node(args.run_manifest.resolve(),node,NODE_HANDLERS[node])
if __name__=="__main__": raise SystemExit(main())
