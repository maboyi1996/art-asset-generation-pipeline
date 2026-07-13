"""Versioned deterministic policies for V4 planning and delivery."""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from .contract_registry import SKILL_ROOT
from .errors import ContractError

POLICY_FILES = {
    "admission": "admission.json", "rating": "rating.json", "state": "state.json",
    "disposition": "disposition.json", "task": "task.json",
}

@lru_cache(maxsize=None)
def load_policy(name: str) -> dict:
    if name not in POLICY_FILES:
        raise ContractError(f"Unknown policy: {name}")
    return json.loads((SKILL_ROOT / "policies" / POLICY_FILES[name]).read_text(encoding="utf-8-sig"))


def admission_result(factor: dict) -> tuple[str, str]:
    if factor["is_polluted"]:
        return "polluted_exclusion", factor.get("explicit_exclusion_reason") or "污染标签不构成资产主体"
    if factor["is_nonvisual_only"] or not factor["is_visual"]:
        return "evidence_only", factor.get("explicit_exclusion_reason") or "没有独立可见视觉形态"
    if factor.get("explicit_exclusion_reason") and not factor["is_stable_subject"]:
        return "visible_exclusion", factor["explicit_exclusion_reason"]
    return "admitted", "明确可见主体按召回优先政策保留"


def rating_level(asset_type: str, factor: dict) -> tuple[str, str]:
    policy = load_policy("rating")
    episodes = sorted(set(factor.get("visible_episode_ids", [])))
    high = factor.get("mainline_dependency") == "high" or factor.get("appearance_frequency") == "high" or bool(factor.get("strong_design_need"))
    if asset_type == "character":
        if len(episodes) >= policy["character"]["cross_episode_minimum"]:
            return ("S", "跨集且主线/频次/设计需求高") if high else ("A", "跨集可见人物")
        max_seconds = factor.get("max_segment_seconds")
        if factor.get("all_visible_one_segment") and max_seconds is not None and float(max_seconds) <= policy["character"]["character_c_max_segment_seconds"]:
            return "C", "单集且全部可见戏份有最长15秒单片段正证据"
        return "B", "单集人物缺少最长15秒单片段正证据，保守评B"
    type_policy = policy[asset_type]
    if len(episodes) >= 2:
        return ("S", "跨集且生产依赖高") if high else ("A", "跨集复用资产")
    return ("B", "单集但具有独立设计或剧情需求") if high or factor.get("mainline_dependency") == "medium" else ("C", "单集低复用资产")


def state_result(priority: str, factor: dict) -> tuple[str, str]:
    policy = load_policy("state")
    if priority not in policy["eligible_priorities"]:
        return "base_only", "B/C资产不拆状态"
    if factor.get("non_state"):
        return "excluded_non_state", "动作、情绪或瞬时变化不构成状态"
    if not factor.get("visible_stable_difference"):
        return "excluded_weak", "缺少稳定可见差异"
    if factor.get("evidence_strength") not in policy["create_when"]["evidence_strength"]:
        return "excluded_weak", "状态证据强度不足"
    return "created", "稳定可见差异满足状态拆分政策"


def disposition_result(factor: dict) -> tuple[str, str, str]:
    if factor.get("is_alias"):
        target = factor.get("alias_to_base_asset_id", "")
        if not target:
            raise ContractError("Alias disposition requires alias_to_base_asset_id")
        return "alias_to", target, "别名自动归入已有资产"
    if factor.get("is_generic") and factor.get("group_target_base_asset_id"):
        return "grouped_into", factor["group_target_base_asset_id"], "泛称主体由目标资产覆盖"
    if factor.get("is_nonvisual"):
        return "not_visual_candidate", "", factor.get("explicit_exclusion_reason") or "无独立视觉形态"
    if not factor.get("has_independent_visual_need"):
        return "excluded", "", factor.get("explicit_exclusion_reason") or "无独立主图生产需求"
    return "production_task", "", "明确可见且具有独立视觉需求"


def task_policy() -> dict:
    return load_policy("task")
