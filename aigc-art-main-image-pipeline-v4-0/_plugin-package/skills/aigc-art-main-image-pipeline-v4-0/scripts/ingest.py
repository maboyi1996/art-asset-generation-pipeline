#!/usr/bin/env python3
"""Module 1: document intake, deterministic scene IDs, and source coverage."""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))
from core.errors import InputError, IntegrityError
from core.execution import execute_node
from core.ids import stable_digest, stable_id
from core.model_gateway import load_model_rows
from core.storage import artifact_path, file_hashes, load_manifest, read_jsonl, write_json, write_jsonl
from core.validator import gate_result, require_unique


def _source_kind(text: str) -> str:
    value = text.strip()
    if re.match(r"^第s*[0-9一二三四五六七八九十百千]+s*集", value) or re.match(r"^(EP|E)s*d+", value, re.I):
        return "heading"
    if len(value) <= 60 and any(mark in value for mark in ["场", "内", "外", "日", "夜"]):
        return "heading"
    return "paragraph"


def _docx_blocks(path: Path):
    from docx import Document
    from docx.document import Document as DocType
    from docx.table import Table
    from docx.text.paragraph import Paragraph
    from docx.oxml.table import CT_Tbl
    from docx.oxml.text.paragraph import CT_P
    document = Document(path)
    for child in document.element.body.iterchildren():
        if isinstance(child, CT_P):
            paragraph = Paragraph(child, document)
            text = paragraph.text.strip()
            if text:
                yield _source_kind(text), text
        elif isinstance(child, CT_Tbl):
            table = Table(child, document)
            for row in table.rows:
                text = " | ".join(cell.text.strip() for cell in row.cells if cell.text.strip())
                if text:
                    yield "table_row", text


def _pdf_blocks(path: Path):
    from pypdf import PdfReader
    reader = PdfReader(str(path))
    for page_index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        for part in re.split(r"\n\s*\n|\n", text):
            part = part.strip()
            if part:
                yield "pdf_text", f"[page {page_index}] {part}"


def _text_blocks(path: Path):
    text = path.read_text(encoding="utf-8-sig")
    for line in text.splitlines():
        value = line.strip()
        if value:
            yield ("heading" if _source_kind(value) == "heading" else "text_line"), value


def document_read(manifest_path: Path) -> None:
    manifest = load_manifest(manifest_path)
    source = Path(manifest["source"]["path"])
    suffix = source.suffix.lower()
    if suffix == ".docx": iterator = _docx_blocks(source)
    elif suffix == ".pdf": iterator = _pdf_blocks(source)
    elif suffix in {".txt", ".md"}: iterator = _text_blocks(source)
    else: raise InputError(f"Unsupported source format: {suffix}")
    rows = []
    for index, (kind, text) in enumerate(iterator, start=1):
        block_id = stable_id("block", manifest["source"]["sha256"], index, text)
        rows.append({"block_id": block_id, "block_index": index, "kind": kind, "text": text, "source_locator": f"{source.name}#block-{index}", "sha256": stable_digest(text, length=64)})
    if not rows: raise InputError("Source document contains no readable text blocks")
    write_jsonl(artifact_path(manifest_path, "source-blocks"), rows)


def scene_segmentation(manifest_path: Path) -> None:
    blocks = read_jsonl(artifact_path(manifest_path, "source-blocks", must_exist=True))
    block_by_id = {row["block_id"]: row for row in blocks}
    factors = load_model_rows(manifest_path, "scene-segmentation")["scene-boundary-factors"]
    if not factors: raise IntegrityError("scene-boundary-factors must not be empty")
    used = []
    ordered = sorted(factors, key=lambda row: (min(block_by_id[x]["block_index"] for x in row["block_ids"]), row["scene_order_hint"]))
    episode_labels = []
    for factor in ordered:
        for block_id in factor["block_ids"]:
            if block_id not in block_by_id: raise IntegrityError(f"Scene factor references unknown block: {block_id}")
            used.append(block_id)
        label = factor["episode_label"].strip() or "未标集"
        if label not in episode_labels: episode_labels.append(label)
    counts = Counter(used)
    duplicates = [key for key, count in counts.items() if count > 1]
    missing = sorted(set(block_by_id) - set(used))
    if duplicates or missing:
        raise IntegrityError(f"Scene factors must assign every block exactly once; duplicates={duplicates[:10]}, missing={missing[:10]}")
    scene_counters = Counter(); rows = []
    for factor in ordered:
        label = factor["episode_label"].strip() or "未标集"
        episode_number = episode_labels.index(label) + 1
        episode_id = f"E{episode_number:02d}"
        scene_counters[episode_id] += 1
        scene_id = f"{episode_id}-S{scene_counters[episode_id]:03d}"
        selected = sorted((block_by_id[x] for x in factor["block_ids"]), key=lambda row: row["block_index"])
        text = "\n".join(row["text"] for row in selected)
        rows.append({"scene_id": scene_id, "episode_id": episode_id, "scene_index": scene_counters[episode_id], "block_ids": [row["block_id"] for row in selected], "heading": factor["scene_heading"], "location": factor["location"], "time_of_day": factor["time_of_day"], "text": text, "source_sha256": stable_digest([row["sha256"] for row in selected], length=64)})
    write_jsonl(artifact_path(manifest_path, "scenes"), rows)


def source_coverage(manifest_path: Path) -> None:
    blocks = read_jsonl(artifact_path(manifest_path, "source-blocks", must_exist=True)); scenes = read_jsonl(artifact_path(manifest_path, "scenes", must_exist=True))
    all_ids = {row["block_id"] for row in blocks}; assigned = [item for scene in scenes for item in scene["block_ids"]]; counts = Counter(assigned)
    duplicates = sorted(key for key, count in counts.items() if count > 1); missing = sorted(all_ids - set(assigned)); unknown = sorted(set(assigned) - all_ids)
    errors = []
    if duplicates: errors.append(f"duplicate source block assignments: {', '.join(duplicates[:20])}")
    if missing: errors.append(f"unassigned source blocks: {', '.join(missing[:20])}")
    if unknown: errors.append(f"unknown source blocks: {', '.join(unknown[:20])}")
    result = gate_result("source-coverage-gate", errors, [], file_hashes(manifest_path,["source-blocks","scenes"]), {}, total_blocks=len(blocks), assigned_blocks=len(set(assigned)), duplicate_blocks=duplicates, missing_blocks=missing)
    write_json(artifact_path(manifest_path, "source-coverage"), result)
    if errors: raise IntegrityError("; ".join(errors))

NODE_HANDLERS={"document-read":document_read,"scene-segmentation":scene_segmentation,"source-coverage-gate":source_coverage}
ACTION_TO_NODE={"document-read":"document-read","scene-segmentation":"scene-segmentation","source-coverage":"source-coverage-gate"}

def main(argv=None):
    parser=argparse.ArgumentParser(); parser.add_argument("--run-manifest",required=True,type=Path); parser.add_argument("--action",required=True,choices=sorted(ACTION_TO_NODE)); args=parser.parse_args(argv)
    node_id=ACTION_TO_NODE[args.action]; return execute_node(args.run_manifest.resolve(),node_id,NODE_HANDLERS[node_id])
if __name__=="__main__": raise SystemExit(main())
