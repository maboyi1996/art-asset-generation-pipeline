#!/usr/bin/env python3
"""Render prompted-production-task-table.md from core-prompt-slots.md.

This script is deterministic and read-only for upstream inputs. It fails on
missing slots, invalid enums, or forbidden free-text prompt markers.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import OrderedDict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

from artifact_manifest import ManifestError, required_output_parent, resolve_artifact


VALID_ASSET_TYPES = {"character", "scene", "prop"}
VALID_TASK_TYPES = {"text_to_image", "image_text_edit"}
VALID_SLOT_STATUSES = {"ready", "missing_evidence", "manual_review_required"}
FORBIDDEN_SLOT_MARKERS = [
    "{{include",
    "【A. 题材世界】",
    "【B. 画法】",
    "real portrait photograph",
    "photographic realism",
    "raw portrait photography",
    "realistic pores",
    "PBR asset look",
]
NEGATIVE_WORDS = ["不要", "不能", "避免", "不得", "不加入"]
NEGATIVE_SLOT_PATTERNS = [
    re.compile(pattern)
    for pattern in [
        r"无[^，。；;、]{1,12}设定",
        r"无人物",
        r"无环境",
        r"无其他",
        r"无道具",
        r"无文字",
    ]
]
ABSTRACT_SLOT_PATTERNS = [
    (re.compile(pattern), label)
    for pattern, label in [
        (r"身份由.*确定", "identity is explained by naming instead of visible detail"),
        (r"由称谓.*确定", "identity is explained by title instead of visible detail"),
        (r"与.*身份.*一致", "slot says it matches identity instead of describing visible detail"),
        (r"与.*气质.*一致", "slot says it matches temperament instead of describing visible detail"),
        (r"符合.*身份", "slot says it fits identity instead of describing visible detail"),
        (r"符合.*阶层", "slot says it fits class instead of describing visible detail"),
        (r"与.*阶层.*相符", "slot says it fits class instead of describing visible detail"),
        (r"与.*身份.*相符", "slot says it fits identity instead of describing visible detail"),
        (r"古典盘发或长发造型", "slot gives broad hairstyle options instead of one concrete hairstyle"),
        (r"核心气质清楚", "slot uses abstract temperament wording"),
        (r"核心气质明确", "slot uses abstract temperament wording"),
        (r"有角色辨识度", "slot uses abstract distinctiveness wording"),
        (r"有辨识度", "slot uses abstract distinctiveness wording"),
        (r"空间布局清楚", "slot uses abstract layout wording"),
        (r"道具状态.*明确", "slot uses abstract prop condition wording"),
        (r"道具状态.*清楚", "slot uses abstract prop condition wording"),
    ]
]
SLOT_SECTION_KEYWORDS = ["槽位表", "core-prompt-slots"]


class SlotError(Exception):
    pass


def fail(message: str) -> None:
    raise SlotError(message)


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
    return re.sub(r"^\d+[.、\s]+", "", title)


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
        fail(f"Slot table is empty in section: {'/'.join(keywords)}")
    return rows


def require_columns(rows: List[Dict[str, str]], columns: Iterable[str]) -> None:
    header = set(rows[0].keys()) if rows else set()
    missing = [column for column in columns if column not in header]
    if missing:
        fail(f"core-prompt-slots missing columns: {', '.join(missing)}")


def contains_cjk(value: str) -> bool:
    return any("\u4e00" <= char <= "\u9fff" for char in value)


def validate_slot_text(task_id: str, slot_name: str, value: str) -> None:
    lowered = value.lower()
    for marker in FORBIDDEN_SLOT_MARKERS:
        if marker.lower() in lowered:
            fail(f"Task {task_id} slot {slot_name} contains forbidden marker: {marker}")
    if slot_name not in {"identity_reference_image"} and value and not contains_cjk(value):
        fail(f"Task {task_id} slot {slot_name} must be Chinese evidence-derived text")
    if slot_name not in {"identity_reference_image", "composition_preservation"}:
        for word in NEGATIVE_WORDS:
            if word in value:
                fail(f"Task {task_id} slot {slot_name} contains negative or exclusion wording: {word}")
        for pattern in NEGATIVE_SLOT_PATTERNS:
            if pattern.search(value):
                fail(f"Task {task_id} slot {slot_name} contains negative or exclusion wording: {pattern.pattern}")
    if slot_name not in {"identity_reference_image"}:
        for pattern, label in ABSTRACT_SLOT_PATTERNS:
            if pattern.search(value):
                fail(
                    f"Task {task_id} slot {slot_name} is too abstract for visual generation: "
                    f"{label}; value: {value}; owner layer: prompt-generation.md; "
                    "fix slot_value with concrete visible details from core-prompt-slots规则.md"
                )


def group_slots(rows: List[Dict[str, str]]) -> "OrderedDict[str, Dict[str, Any]]":
    require_columns(
        rows,
        [
            "task_id",
            "asset_type",
            "task_type",
            "base_asset_id",
            "state_asset_id",
            "slot_name",
            "slot_value",
            "slot_status",
            "source_evidence_ids",
            "source_locator",
            "slot_issue",
        ],
    )
    tasks: "OrderedDict[str, Dict[str, Any]]" = OrderedDict()
    for row in rows:
        task_id = row.get("task_id", "")
        if not task_id:
            fail("Slot row missing task_id")
        asset_type = row.get("asset_type", "")
        task_type = row.get("task_type", "")
        if asset_type not in VALID_ASSET_TYPES:
            fail(f"Task {task_id} has invalid asset_type: {asset_type}")
        if task_type not in VALID_TASK_TYPES:
            fail(f"Task {task_id} has invalid task_type: {task_type}")
        if task_type == "image_text_edit" and asset_type != "character":
            fail(f"Task {task_id} image_text_edit is only supported for character assets")
        status = row.get("slot_status", "")
        if status not in VALID_SLOT_STATUSES:
            fail(f"Task {task_id} slot {row.get('slot_name')} has invalid slot_status: {status}")
        slot_name = row.get("slot_name", "")
        if not slot_name:
            fail(f"Task {task_id} has empty slot_name")
        slot_value = row.get("slot_value", "")
        if status == "missing_evidence":
            fail(
                f"Task {task_id} slot {slot_name} is missing evidence; "
                f"owner layer: prompt-generation.md; issue: {row.get('slot_issue', '')}"
            )
        validate_slot_text(task_id, slot_name, slot_value)
        task = tasks.setdefault(
            task_id,
            {
                "task_id": task_id,
                "asset_type": asset_type,
                "task_type": task_type,
                "base_asset_id": row.get("base_asset_id", ""),
                "state_asset_id": row.get("state_asset_id", ""),
                "slots": OrderedDict(),
                "evidence_ids": [],
            },
        )
        for key in ["asset_type", "task_type", "base_asset_id", "state_asset_id"]:
            if task[key] != row.get(key, ""):
                fail(f"Task {task_id} has inconsistent {key} across slot rows")
        if slot_name in task["slots"]:
            fail(f"Task {task_id} has duplicate slot_name: {slot_name}")
        task["slots"][slot_name] = slot_value
        for evidence_id in row.get("source_evidence_ids", "").split(","):
            evidence_id = evidence_id.strip()
            if evidence_id and evidence_id not in task["evidence_ids"]:
                task["evidence_ids"].append(evidence_id)
    return tasks


def load_render_templates(path: Path) -> Dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        fail(f"invalid render template JSON: {exc}")
    if not isinstance(data, dict):
        fail("render template root must be an object")
    if data.get("schema_version") != "core-prompt-render-templates.v1":
        fail("render template schema_version must be core-prompt-render-templates.v1")
    if not isinstance(data.get("templates"), dict):
        fail("render template missing templates object")
    if not isinstance(data.get("negative_prompts"), dict):
        fail("render template missing negative_prompts object")
    return data


def render_tasks(slot_rows: List[Dict[str, str]], templates_data: Dict[str, Any]) -> List[Dict[str, str]]:
    tasks = group_slots(slot_rows)
    rendered_rows: List[Dict[str, str]] = []
    templates = templates_data["templates"]
    negative_prompts = templates_data["negative_prompts"]
    for task_id, task in tasks.items():
        asset_type = task["asset_type"]
        task_type = task["task_type"]
        template_key = f"{asset_type}:{task_type}"
        if template_key not in templates:
            fail(f"Task {task_id} has no render template: {template_key}")
        template = templates[template_key]
        required_slots = template.get("required_slots")
        if not isinstance(required_slots, list) or not required_slots:
            fail(f"Render template {template_key} missing required_slots")
        slots = task["slots"]
        missing = [slot for slot in required_slots if slot not in slots or not slots[slot]]
        if missing:
            fail(f"Task {task_id} missing required slots: {', '.join(missing)}")
        negative_key = "image_text_edit" if task_type == "image_text_edit" else asset_type
        negative_prompt = negative_prompts.get(negative_key, "")
        if not negative_prompt:
            fail(f"Missing negative prompt template for {negative_key}")
        format_values = dict(slots)
        format_values["negative_prompt"] = negative_prompt
        try:
            rendered_text = template["text"].format(**format_values)
        except KeyError as exc:
            fail(f"Render template {template_key} references missing slot: {exc}")
        if not contains_cjk(rendered_text):
            fail(f"Task {task_id} rendered text must contain Chinese")
        prompt = rendered_text if template.get("target_field") == "prompt" else ""
        edit_instruction = rendered_text if template.get("target_field") == "edit_instruction" else ""
        rendered_rows.append(
            {
                "task_id": task_id,
                "base_asset_id": task["base_asset_id"],
                "state_asset_id": task["state_asset_id"],
                "asset_type": asset_type,
                "task_type": task_type,
                "prompt": prompt,
                "edit_instruction": edit_instruction,
                "negative_prompt": negative_prompt,
                "slot_source_evidence_ids": ",".join(task["evidence_ids"]),
            }
        )
    return rendered_rows


def md_cell(value: str) -> str:
    value = str(value).replace("|", "／")
    return value.replace("\r\n", "\n").replace("\r", "\n").replace("\n", "<br>")


def write_prompted_table(rows: List[Dict[str, str]], output: Path) -> None:
    headers = [
        "task_id",
        "base_asset_id",
        "state_asset_id",
        "asset_type",
        "task_type",
        "prompt",
        "edit_instruction",
        "negative_prompt",
        "slot_source_evidence_ids",
    ]
    lines = ["# prompted-production-task-table", "", "## 全局生产任务提示词表", ""]
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("|" + "|".join("---" for _ in headers) + "|")
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(header, "")) for header in headers) + " |")
    required_output_parent(output)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render prompted-production-task-table.md from core-prompt-slots.md")
    parser.add_argument("--artifact-manifest", required=True, type=Path, help="Path to artifact-manifest.json")
    parser.add_argument(
        "--templates",
        default=Path(__file__).resolve().parents[1] / "references" / "templates" / "core-prompt-render-templates.json",
        type=Path,
        help="Path to core-prompt-render-templates.json",
    )
    args = parser.parse_args(argv)

    try:
        slots_path = resolve_artifact(
            args.artifact_manifest,
            "core-prompt-slots",
            expected_role="production_source",
            expected_type="markdown_table",
            must_exist=True,
        )
        output_path = resolve_artifact(
            args.artifact_manifest,
            "prompted-production-task-table",
            expected_role="production_source",
            expected_type="markdown_table",
            must_exist=False,
        )
        rows = extract_first_table(slots_path.read_text(encoding="utf-8-sig").splitlines(), SLOT_SECTION_KEYWORDS)
        rendered_rows = render_tasks(rows, load_render_templates(args.templates))
        if len(rendered_rows) != len({row["task_id"] for row in rendered_rows}):
            fail("Rendered prompt row count does not match unique task count")
        write_prompted_table(rendered_rows, output_path)
    except (SlotError, ManifestError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
