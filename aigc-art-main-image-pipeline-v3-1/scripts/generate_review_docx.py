#!/usr/bin/env python3
"""Generate main-image-review-table.docx from the V3.1 production source.

This script is intentionally read-only for Markdown inputs. It derives a human
review DOCX from the completed machine table and never repairs task data.
"""

from __future__ import annotations

import argparse
import re
import sys
import zipfile
from collections import OrderedDict, defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Tuple
from xml.sax.saxutils import escape

from artifact_manifest import ManifestError, required_output_parent, resolve_artifact

VALID_ASSET_TYPES = {"character", "scene", "prop"}
INCLUDED_REVIEW_STATUSES = {"ready", "manual_review_required"}
FORBIDDEN_TEXT = {"基础提示词", "prompt", "edit_instruction", "negative_prompt", "{{include"}


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
    return rows


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


def priority_label(value: str) -> str:
    value = value.strip().upper()
    if value in {"S", "A", "B", "C"}:
        return f"{value}级"
    if value.endswith("级"):
        return value
    return value


def compact_join(parts: Iterable[str]) -> str:
    seen = []
    for part in parts:
        part = clean_cell(part)
        if part and part not in seen:
            seen.append(part)
    return "\n".join(seen)


def table_cell_text(row: Dict[str, str], *keys: str) -> str:
    return compact_join(row.get(key, "") for key in keys)


def ensure_no_forbidden_output_text(rows: List[List[str]]) -> None:
    for row in rows:
        for value in row:
            lower = value.lower()
            for forbidden in FORBIDDEN_TEXT:
                if forbidden.lower() in lower:
                    fail(f"DOCX output would contain forbidden prompt text marker: {forbidden}")


def derive_review_rows(production_md: Path) -> "OrderedDict[int, Dict[str, List[List[str]]]]":
    text = production_md.read_text(encoding="utf-8-sig")
    lines = text.splitlines()

    task_rows = extract_first_table(lines, ["全局生产任务表"])
    mapping_rows = extract_first_table(lines, ["分集使用映射表"])

    require_columns(
        task_rows,
        [
            "task_id",
            "base_asset_id",
            "asset_type",
            "asset_name",
            "state_name",
            "priority_level",
            "task_type",
            "review_status",
            "episode_id",
            "source_evidence",
            "prompt",
            "edit_instruction",
            "negative_prompt",
            "review_focus",
        ],
        "全局生产任务表",
    )
    require_columns(
        mapping_rows,
        [
            "episode_id",
            "asset_type",
            "asset_name",
            "state_name",
            "priority_level",
            "task_id",
            "review_status",
            "episode_function",
            "notes",
        ],
        "分集使用映射表",
    )

    tasks = {row["task_id"]: row for row in task_rows if row.get("task_id")}
    if len(tasks) != len([row for row in task_rows if row.get("task_id")]):
        fail("Duplicate task_id in 全局生产任务表")

    episodes: "OrderedDict[int, Dict[str, List[List[str]]]]" = OrderedDict()
    seen_episode_task: set[Tuple[int, str]] = set()

    def ensure_episode(ep: int) -> Dict[str, List[List[str]]]:
        if ep not in episodes:
            episodes[ep] = {"character": [], "scene": [], "prop": []}
        return episodes[ep]

    def add_task(ep: int, task: Dict[str, str], mapping: Dict[str, str] | None = None) -> None:
        task_id = task.get("task_id", "")
        if (ep, task_id) in seen_episode_task:
            return
        seen_episode_task.add((ep, task_id))

        review_status = mapping.get("review_status", "") if mapping else task.get("review_status", "")
        review_status = review_status or task.get("review_status", "")
        if review_status == "excluded":
            return
        if review_status not in INCLUDED_REVIEW_STATUSES:
            fail(f"Task {task_id} has unsupported review_status for DOCX: {review_status}")

        asset_type = task.get("asset_type", "")
        if asset_type not in VALID_ASSET_TYPES:
            fail(f"Task {task_id} has invalid asset_type: {asset_type}")

        state_name = mapping.get("state_name", "") if mapping else task.get("state_name", "")
        evidence_text = compact_join(
            [
                state_name,
                mapping.get("episode_function", "") if mapping else "",
                mapping.get("notes", "") if mapping else "",
                task.get("source_evidence", ""),
                task.get("review_focus", ""),
            ]
        )

        asset_name = mapping.get("asset_name", "") if mapping else task.get("asset_name", "")
        priority = mapping.get("priority_level", "") if mapping else task.get("priority_level", "")
        row_base = [asset_name or task.get("asset_name", ""), evidence_text, priority_label(priority or task.get("priority_level", ""))]
        if asset_type == "character":
            output_row = row_base + ["", ""]
        elif asset_type == "scene":
            output_row = row_base + ["", ""]
        else:
            output_row = row_base + [""]
        ensure_no_forbidden_output_text([output_row])
        ensure_episode(ep)[asset_type].append(output_row)

    for mapping in mapping_rows:
        task_id = mapping.get("task_id", "")
        if not task_id:
            continue
        if task_id not in tasks:
            fail(f"分集使用映射表 references missing task_id: {task_id}")
        task = tasks[task_id]
        episodes_for_row = parse_episode_numbers(mapping.get("episode_id", ""))
        if not episodes_for_row:
            fail(f"Mapping row for task {task_id} missing parseable episode_id")
        for ep in episodes_for_row:
            add_task(ep, task, mapping)

    for task in task_rows:
        if task.get("review_status") == "excluded":
            continue
        task_id = task.get("task_id", "")
        if any(seen_task_id == task_id for _, seen_task_id in seen_episode_task):
            continue
        episodes_for_task = parse_episode_numbers(task.get("episode_id", ""))
        if not episodes_for_task:
            fail(f"Task {task_id} is not connected to a parseable episode")
        for ep in episodes_for_task:
            add_task(ep, task, None)

    if not episodes:
        fail("No reviewable episode rows found")

    return OrderedDict(sorted(episodes.items(), key=lambda item: item[0]))


def w_text(text: str) -> str:
    lines = str(text).splitlines() or [""]
    runs = []
    for i, line in enumerate(lines):
        if i:
            runs.append("<w:r><w:br/></w:r>")
        space = ' xml:space="preserve"' if line.startswith(" ") or line.endswith(" ") else ""
        runs.append(f"<w:r><w:t{space}>{escape(line)}</w:t></w:r>")
    return "".join(runs)


def paragraph(text: str, style: str | None = None) -> str:
    ppr = f"<w:pPr><w:pStyle w:val=\"{style}\"/></w:pPr>" if style else ""
    return f"<w:p>{ppr}{w_text(text)}</w:p>"


def table_xml(headers: List[str], rows: List[List[str]]) -> str:
    all_rows = [headers] + rows
    cells_xml = []
    for row in all_rows:
        row_cells = []
        for cell in row:
            row_cells.append(
                "<w:tc><w:tcPr><w:tcW w:w=\"2400\" w:type=\"dxa\"/></w:tcPr>"
                f"{paragraph(cell)}</w:tc>"
            )
        cells_xml.append(f"<w:tr>{''.join(row_cells)}</w:tr>")
    return (
        "<w:tbl>"
        "<w:tblPr><w:tblStyle w:val=\"TableGrid\"/><w:tblW w:w=\"0\" w:type=\"auto\"/>"
        "<w:tblBorders><w:top w:val=\"single\" w:sz=\"4\"/><w:left w:val=\"single\" w:sz=\"4\"/>"
        "<w:bottom w:val=\"single\" w:sz=\"4\"/><w:right w:val=\"single\" w:sz=\"4\"/>"
        "<w:insideH w:val=\"single\" w:sz=\"4\"/><w:insideV w:val=\"single\" w:sz=\"4\"/>"
        "</w:tblBorders></w:tblPr>"
        f"{''.join(cells_xml)}</w:tbl>"
    )


def empty_rows(asset_type: str) -> List[List[str]]:
    if asset_type == "character":
        return [["本集无新增/使用项", "", "", "", ""]]
    if asset_type == "scene":
        return [["本集无新增/使用项", "", "", "", ""]]
    return [["本集无新增/使用项", "", "", ""]]


def build_document_xml(episodes: "OrderedDict[int, Dict[str, List[List[str]]]]") -> str:
    body: List[str] = []
    body.append(paragraph("主图资产人审表", "Title"))
    for ep, groups in episodes.items():
        body.append(paragraph(f"第{ep}集", "Heading1"))
        body.append(paragraph("人物表", "Heading2"))
        body.append(table_xml(["人物", "本集状态与外貌", "评级", "人设图", "5视图"], groups["character"] or empty_rows("character")))
        body.append(paragraph("场景表", "Heading2"))
        body.append(table_xml(["场景", "描述", "评级", "", ""], groups["scene"] or empty_rows("scene")))
        body.append(paragraph("道具表", "Heading2"))
        body.append(table_xml(["道具", "描述与归属", "评级", ""], groups["prop"] or empty_rows("prop")))
    body.append("<w:sectPr><w:pgSz w:w=\"11906\" w:h=\"16838\"/><w:pgMar w:top=\"1440\" w:right=\"1440\" w:bottom=\"1440\" w:left=\"1440\"/></w:sectPr>")
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        f"<w:body>{''.join(body)}</w:body></w:document>"
    )


def write_docx(output: Path, document_xml: str) -> None:
    content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>"""
    rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""
    styles = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>
  <w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/><w:pPr><w:jc w:val="center"/></w:pPr><w:rPr><w:b/><w:sz w:val="32"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:rPr><w:b/><w:sz w:val="28"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:rPr><w:b/><w:sz w:val="24"/></w:rPr></w:style>
  <w:style w:type="table" w:styleId="TableGrid"><w:name w:val="Table Grid"/></w:style>
</w:styles>"""
    required_output_parent(output)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as docx:
        docx.writestr("[Content_Types].xml", content_types)
        docx.writestr("_rels/.rels", rels)
        docx.writestr("word/document.xml", document_xml)
        docx.writestr("word/styles.xml", styles)


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate main-image-review-table.docx from manifest-routed production source")
    parser.add_argument("--artifact-manifest", required=True, type=Path, help="Path to artifact-manifest.json")
    parser.add_argument("--output", default=None, type=Path, help="Optional output path; must match manifest deliverable path")
    args = parser.parse_args(argv)

    try:
        production_path = resolve_artifact(
            args.artifact_manifest,
            "main-image-production-table",
            expected_role="production_source",
            expected_type="markdown_table",
            must_exist=True,
        )
        docx_output = resolve_artifact(
            args.artifact_manifest,
            "main-image-review-table",
            expected_role="deliverable",
            expected_type="docx",
            must_exist=False,
        )
        output_path = args.output.resolve() if args.output else docx_output
        if output_path != docx_output:
            fail(f"Output path must match artifact manifest deliverable: {docx_output}")
        episodes = derive_review_rows(production_path)
        write_docx(output_path, build_document_xml(episodes))
    except (ContractError, ManifestError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
