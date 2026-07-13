#!/usr/bin/env python3
"""Generate human-readable docs from pipeline-contract.json."""
from __future__ import annotations
import sys
from collections import defaultdict
from pathlib import Path
SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))
from core.contract_registry import SKILL_ROOT, load_contract
from core.storage import atomic_write_text
MODULE_LABELS={"global":"全局建档","ingest":"模块一：剧本接入","recognition":"模块二：资产识别","planning":"模块三：资产规划","visual":"模块四：视觉生产","delivery":"模块五：交付"}

def generate() -> None:
    contract=load_contract(); groups=defaultdict(list)
    for node in contract["nodes"]: groups[node["module"]].append(node)
    workflow=["# V4 自动化生产 Workflow","","> 本文件由 framework/pipeline-contract.json 自动生成，请勿手工维护节点合同。","","- 运行中无人介入、无 review queue、无动态规则修改。","- 默认正式交付为 deliverables/prompt-manifest.json。","- runtime gate 只检查机器结构，不评价语义精准性。",""]
    details=["# V4 Node Contracts","","> 自动生成文件。唯一事实源为 pipeline-contract.json。",""]
    for module in ["global","ingest","recognition","planning","visual","delivery"]:
        workflow += [f"## {MODULE_LABELS[module]}","","| # | Node | Mode | Inputs | Outputs |","|---:|---|---|---|---|"]
        for node in groups[module]:
            outputs=[*node.get("model_produces",[]),*node.get("python_produces",[])]
            workflow.append(f"| {node['order']} | {node['id']} | {node['mode']} | {', '.join(node['inputs']) or '-'} | {', '.join(outputs)} |")
            details += [f"## {node['order']}. {node['id']}","",f"- Module: {node['module']}",f"- Mode: {node['mode']}",f"- Depends on: {', '.join(node['depends_on']) or '-'}",f"- Inputs: {', '.join(node['inputs']) or '-'}",f"- Model factors: {', '.join(node.get('model_produces',[])) or '-'}",f"- Python outputs: {', '.join(node.get('python_produces',[])) or '-'}",f"- Executor: {node['executor']}",f"- Validator: {node['validator']}",f"- Rules: {', '.join(node.get('rules',[])) or '-'}",""]
        workflow.append("")
    atomic_write_text(SKILL_ROOT/"framework"/"workflow.md","\n".join(workflow)+"\n")
    atomic_write_text(SKILL_ROOT.parents[1]/"docs"/"maintainers"/"NODE_CONTRACTS.md","\n".join(details)+"\n")
if __name__ == "__main__": generate(); print("contract docs generated")
