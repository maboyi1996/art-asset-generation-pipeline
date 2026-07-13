#!/usr/bin/env python3
"""Generate Seedance prompt-manifest.json from the V3.1.1 production source.

This script is intentionally read-only for Markdown inputs. It fails on broken
contracts instead of repairing or guessing missing asset/task data.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import OrderedDict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

from artifact_manifest import ManifestError, required_output_parent, resolve_artifact

SCHEMA_VERSION = "seedance-element-extract-manifest.v1"
DEFAULT_SKILL_ID = "aigc-art-main-image-pipeline-v3-1-1"
DEFAULT_SKILL_VERSION = "3.1.1"
ASSET_TYPE_TO_TEMPLATE = {
    "character": "ROLE",
    "scene": "SCENE",
    "prop": "PROP",
}
TEMPLATE_TO_RATIO = {
    "ROLE": "9:16",
    "SCENE": "16:9",
    "PROP": "1:1",
}
VALID_PRIORITIES = {"S", "A", "B", "C"}
VALID_TASK_TYPES = {"text_to_image", "image_text_edit"}
INCLUDED_REVIEW_STATUSES = {"ready", "manual_review_required"}
FORBIDDEN_PROMPT_MARKERS = [
    "{{include",
    "【A. 题材世界】",
    "【B. 画法】",
    "real portrait photograph",
    "photographic realism",
    "raw portrait photography",
    "realistic pores",
    "PBR asset look",
]


class ContractError(Exception):
    pass


def fail(message: str) -> None:
    raise ContractError(message)


def clean_cell(value: str) -> str:
    value = value.strip()
    if value.startswith("`") and value.endswith("`") and len(value) >= 2:
        value = value[1:-1]
    value = value.replace("<br />", "\n").replace("<br/>", "\n").replace("<br>", "\n")
    if value in {"-", "—", "N/A", "n/a", "无", "空", "null", "None"}:
        return ""
    return value.strip()


def split_md_row(line: str) -> List[str]:
    line = line.strip()
    if not (line.startswith("|") and line.endswith("|")):
        return []
    return [clean_cell(cell) for cell in line.strip("|").split("|")]


def is_separator_row(cells: List[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell.strip()) for cell in cells)


def heading_title(line: str) -> str | None:
    match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
    if not match:
        return None
    title = match.group(2).strip()
    title = re.sub(r"^\d+[.、\s]+", "", title)
    return title


def extract_first_table(lines: List[str], title_keywords: Iterable[str]) -> List[Dict[str, str]]:
    keywords = list(title_keywords)
    start = None
    for i, line in enumerate(lines):
        title = heading_title(line)
        if title and any(keyword in title for keyword in keywords):
            start = i + 1
            break
    if start is None:
        fail(f"Missing required section: {'/'.join(keywords)}")

    table_lines: List[str] = []
    in_table = False
    for line in lines[start:]:
        if heading_title(line) and in_table:
            break
        if line.strip().startswith("|") and line.strip().endswith("|"):
            in_table = True
            table_lines.append(line)
        elif in_table and line.strip():
            break

    if len(table_lines) < 2:
        fail(f"Missing markdown table in section: {'/'.join(keywords)}")

    header = split_md_row(table_lines[0])
    rows: List[Dict[str, str]] = []
    for raw_line in table_lines[1:]:
        cells = split_md_row(raw_line)
        if is_separator_row(cells):
            continue
        if len(cells) != len(header):
            fail(f"Malformed row in section {'/'.join(keywords)}: {raw_line}")
        rows.append(dict(zip(header, cells)))
    if not rows:
        empty = {column: "" for column in header}
        empty["__empty__"] = "true"
        return [empty]
    return rows


def section_text(lines: List[str], title_keywords: Iterable[str]) -> str:
    keywords = list(title_keywords)
    start = None
    for i, line in enumerate(lines):
        title = heading_title(line)
        if title and any(keyword in title for keyword in keywords):
            start = i + 1
            break
    if start is None:
        return ""
    captured: List[str] = []
    for line in lines[start:]:
        if heading_title(line):
            break
        captured.append(line)
    return "\n".join(captured)


def require_columns(rows: List[Dict[str, str]], columns: Iterable[str], section: str) -> None:
    if not rows:
        fail(f"{section} table is empty")
    header = set(rows[0].keys())
    missing = [column for column in columns if column not in header]
    if missing:
        fail(f"{section} missing columns: {', '.join(missing)}")


def parse_episode_numbers(*values: str) -> List[int]:
    episodes = set()
    for value in values:
        if not value:
            continue
        for match in re.finditer(r"(?:E|EP|第)?\s*0*(\d+)\s*(?:集)?", value, flags=re.IGNORECASE):
            episodes.add(int(match.group(1)))
    return sorted(ep for ep in episodes if ep > 0)


def build_episode_index(mapping_rows: List[Dict[str, str]]) -> Dict[str, List[int]]:
    index: Dict[str, set[int]] = {}
    for row in mapping_rows:
        task_id = row.get("task_id", "")
        if not task_id:
            continue
        index.setdefault(task_id, set()).update(parse_episode_numbers(row.get("episode_id", "")))
    return {task_id: sorted(values) for task_id, values in index.items()}


def is_default_state_name(value: str) -> bool:
    return value in {"", "默认状态", "基础状态", "基础形象", "默认", "base", "Base"}


def contains_cjk(value: str) -> bool:
    return any("\u4e00" <= char <= "\u9fff" for char in value)


def validate_core_prompt_text(task_id: str, field_name: str, value: str) -> None:
    if not value:
        fail(f"Task {task_id} missing {field_name}")
    if not contains_cjk(value):
        fail(f"Task {task_id} {field_name} must be Chinese core prompt text")
    lowered = value.lower()
    for marker in FORBIDDEN_PROMPT_MARKERS:
        if marker.lower() in lowered:
            fail(f"Task {task_id} {field_name} contains forbidden prompt marker: {marker}")


def status_is_blocking(rows: List[Dict[str, str]], raw_text: str) -> bool:
    for row in rows:
        for key, value in row.items():
            if key.lower() == "severity" and value == "blocking":
                return True
    return "severity: blocking" in raw_text or "`blocking`" in raw_text


def build_manifest(
    production_md: Path,
    *,
    content_id: str | None,
    project_title: str | None,
    skill_id: str,
    skill_version: str,
) -> Dict[str, object]:
    text = production_md.read_text(encoding="utf-8-sig")
    lines = text.splitlines()

    registry_rows = extract_first_table(lines, ["全局资产注册表"])
    state_rows = extract_first_table(lines, ["状态索引表"])
    task_rows = extract_first_table(lines, ["全局生产任务表"])
    mapping_rows = extract_first_table(lines, ["分集使用映射表"])
    audit_rows = extract_first_table(lines, ["生产审计摘要"])
    audit_text = section_text(lines, ["生产审计摘要"])

    require_columns(
        registry_rows,
        ["base_asset_id", "asset_type", "asset_name", "priority_level"],
        "全局资产注册表",
    )
    require_columns(
        state_rows,
        ["base_asset_id", "state_asset_id", "state_name"],
        "状态索引表",
    )
    require_columns(
        task_rows,
        [
            "task_id",
            "base_asset_id",
            "state_asset_id",
            "asset_type",
            "asset_name",
            "state_name",
            "priority_level",
            "task_type",
            "anchor_task_id",
            "review_status",
            "episode_id",
            "prompt",
            "edit_instruction",
            "negative_prompt",
            "review_focus",
        ],
        "全局生产任务表",
    )

    if status_is_blocking(audit_rows, audit_text):
        fail("production-audit summary still contains blocking issues")

    registry = {row["base_asset_id"]: row for row in registry_rows if row.get("base_asset_id")}
    if len(registry) != len([row for row in registry_rows if row.get("base_asset_id")]):
        fail("Duplicate base_asset_id in 全局资产注册表")

    state_index = {row["state_asset_id"]: row for row in state_rows if row.get("state_asset_id")}
    if len(state_index) != len([row for row in state_rows if row.get("state_asset_id")]):
        fail("Duplicate state_asset_id in 状态索引表")

    episode_index = build_episode_index(mapping_rows)
    assets: "OrderedDict[str, Dict[str, object]]" = OrderedDict()
    state_ids_seen = set()

    for row in task_rows:
        review_status = row.get("review_status", "")
        if review_status == "excluded":
            continue
        if review_status not in INCLUDED_REVIEW_STATUSES:
            fail(f"Task {row.get('task_id')} has unsupported review_status: {review_status}")

        task_id = row.get("task_id", "")
        base_asset_id = row.get("base_asset_id", "")
        state_asset_id = row.get("state_asset_id", "")
        asset_type = row.get("asset_type", "")
        priority = row.get("priority_level", "")
        task_type = row.get("task_type", "")
        anchor_task_id = row.get("anchor_task_id", "")

        if not task_id:
            fail("Production task row missing task_id")
        if not base_asset_id:
            fail(f"Task {task_id} missing base_asset_id")
        if base_asset_id not in registry:
            fail(f"Task {task_id} base_asset_id not found in registry: {base_asset_id}")
        if state_asset_id and state_asset_id not in state_index:
            fail(f"Task {task_id} state_asset_id not found in state index: {state_asset_id}")
        if asset_type not in ASSET_TYPE_TO_TEMPLATE:
            fail(f"Task {task_id} has invalid asset_type: {asset_type}")
        if priority not in VALID_PRIORITIES:
            fail(f"Task {task_id} has invalid priority_level: {priority}")
        if task_type not in VALID_TASK_TYPES:
            fail(f"Task {task_id} has invalid task_type: {task_type}")
        if priority in {"B", "C"} and state_asset_id:
            fail(f"B/C task {task_id} must not have state_asset_id")
        if priority in {"B", "C"} and task_type == "image_text_edit":
            fail(f"B/C task {task_id} must not use image_text_edit")

        image_prompt = row.get("prompt", "") if task_type == "text_to_image" else (row.get("prompt", "") or row.get("edit_instruction", ""))
        validate_core_prompt_text(task_id, "image prompt source", image_prompt)
        validate_core_prompt_text(task_id, "negative_prompt", row.get("negative_prompt", ""))
        if task_type == "image_text_edit" and not anchor_task_id:
            fail(f"Task {task_id} image_text_edit missing anchor_task_id")

        registry_row = registry[base_asset_id]
        template_type = ASSET_TYPE_TO_TEMPLATE[asset_type]
        if base_asset_id not in assets:
            asset_name = registry_row.get("asset_name") or row.get("asset_name", "")
            if not asset_name:
                fail(f"Asset {base_asset_id} missing asset_name")
            assets[base_asset_id] = {
                "assetId": base_asset_id,
                "templateName": asset_name,
                "templateType": template_type,
                "description": registry_row.get("registry_note", "") or row.get("source_evidence", ""),
                "appearance": {
                    "description": registry_row.get("registry_note", "") or asset_name,
                    "appearances": [],
                },
                "metadata": {
                    "source": "agent",
                    "taskIds": [],
                    "evidenceSummary": row.get("source_evidence", ""),
                },
            }

        state_id = state_asset_id or task_id
        if state_id in state_ids_seen:
            fail(f"Duplicate JSON appearance stateId: {state_id}")
        state_ids_seen.add(state_id)

        episodes = sorted(set(parse_episode_numbers(row.get("episode_id", "")) + episode_index.get(task_id, [])))
        generation = {"method": task_type}
        if task_type == "image_text_edit":
            generation["referenceTaskId"] = anchor_task_id

        appearance = {
            "stateId": state_id,
            "name": row.get("state_name", "") or "默认状态",
            "imageRatio": TEMPLATE_TO_RATIO[template_type],
            "imagePrompt": image_prompt,
            "negativePrompt": row.get("negative_prompt", ""),
            "priority": priority,
            "status": review_status,
            "generation": generation,
            "reviewFocus": row.get("review_focus", ""),
        }
        if episodes:
            appearance["episodes"] = episodes

        asset = assets[base_asset_id]
        asset["appearance"]["appearances"].append(appearance)  # type: ignore[index]
        asset["metadata"]["taskIds"].append(task_id)  # type: ignore[index]
        if review_status == "manual_review_required":
            asset["metadata"]["reviewReason"] = row.get("review_reason", "")

    for asset_id, asset in assets.items():
        appearances = asset["appearance"]["appearances"]  # type: ignore[index]
        if not appearances:
            fail(f"Asset {asset_id} has no JSON appearances")
        priorities = {item.get("priority") for item in appearances}
        if priorities & {"B", "C"} and len(appearances) > 1:
            fail(f"B/C asset {asset_id} must not have multiple JSON appearances")

    manifest: Dict[str, object] = {
        "schemaVersion": SCHEMA_VERSION,
        "manifestVersion": "1.0",
        "generationScope": "main_image_only",
        "source": {
            "skillId": skill_id,
            "skillVersion": skill_version,
            "generatedAt": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
            "promptMode": "core_prompt_requires_style_prefix",
            "stylePrefixOwner": "middle_platform",
            "stylePrefixRequired": True,
        },
        "summary": {
            "totalItems": len(assets),
            "manualReviewItems": sum(
                1
                for asset in assets.values()
                for item in asset["appearance"]["appearances"]  # type: ignore[index]
                if item.get("status") == "manual_review_required"
            ),
        },
        "assets": list(assets.values()),
    }
    if content_id:
        manifest["contentId"] = str(content_id)
    if project_title:
        manifest["project"] = {"title": project_title}
    return manifest


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate prompt-manifest.json from manifest-routed production source")
    parser.add_argument("--artifact-manifest", required=True, type=Path, help="Path to artifact-manifest.json")
    parser.add_argument("--output", default=None, type=Path, help="Optional output path; must match manifest deliverable path")
    parser.add_argument("--content-id", default=None, help="Optional Seedance contentId; emitted as a string")
    parser.add_argument("--project-title", default=None, help="Optional project title")
    parser.add_argument("--skill-id", default=DEFAULT_SKILL_ID)
    parser.add_argument("--skill-version", default=DEFAULT_SKILL_VERSION)
    args = parser.parse_args(argv)

    try:
        production_path = resolve_artifact(
            args.artifact_manifest,
            "main-image-production-table",
            expected_role="production_source",
            expected_type="markdown_table",
            must_exist=True,
        )
        manifest_output = resolve_artifact(
            args.artifact_manifest,
            "prompt-manifest",
            expected_role="deliverable",
            expected_type="json",
            must_exist=False,
        )
        output_path = args.output.resolve() if args.output else manifest_output
        if output_path != manifest_output:
            fail(f"Output path must match artifact manifest deliverable: {manifest_output}")
        manifest = build_manifest(
            production_path,
            content_id=args.content_id,
            project_title=args.project_title,
            skill_id=args.skill_id,
            skill_version=args.skill_version,
        )
        manifest["source"]["artifactManifest"] = str(args.artifact_manifest)
        required_output_parent(output_path)
        output_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except (ContractError, ManifestError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
