#!/usr/bin/env python3
"""Validate V3.1.1 main-image-review-table.docx structure."""

from __future__ import annotations

import argparse
import json
import sys
import zipfile
from pathlib import Path
from typing import List
from xml.etree import ElementTree as ET


NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
FORBIDDEN = ["基础提示词", "prompt", "edit_instruction", "negative_prompt", "{{include"]


def collect_text(element: ET.Element) -> str:
    parts: List[str] = []
    for node in element.iter():
        if node.tag == f"{{{NS['w']}}}t" and node.text:
            parts.append(node.text)
    return "".join(parts)


def validate_docx(path: Path) -> List[str]:
    errors: List[str] = []
    if not path.exists():
        return [f"Missing DOCX file: {path}"]

    try:
        with zipfile.ZipFile(path) as docx:
            names = set(docx.namelist())
            if "word/document.xml" not in names:
                return ["DOCX missing word/document.xml"]
            xml = docx.read("word/document.xml")
    except zipfile.BadZipFile:
        return ["File is not a valid DOCX zip package"]
    except OSError as exc:
        return [str(exc)]

    try:
        root = ET.fromstring(xml)
    except ET.ParseError as exc:
        return [f"Invalid document.xml: {exc}"]

    full_text = collect_text(root)
    lower_text = full_text.lower()
    for forbidden in FORBIDDEN:
        if forbidden.lower() in lower_text:
            errors.append(f"DOCX contains forbidden text marker: {forbidden}")

    for required in ["人物表", "场景表", "道具表", "人设图", "5视图"]:
        if required not in full_text:
            errors.append(f"DOCX missing required text: {required}")

    tables = root.findall(".//w:tbl", NS)
    if not tables:
        errors.append("DOCX contains no tables")

    has_character_header = False
    for table in tables:
        rows = table.findall("./w:tr", NS)
        if not rows:
            continue
        first_cells = rows[0].findall("./w:tc", NS)
        headers = [collect_text(cell) for cell in first_cells]
        if headers == ["人物", "本集状态与外貌", "评级", "人设图", "5视图"]:
            has_character_header = True
        if "基础提示词" in headers:
            errors.append("DOCX table still contains 基础提示词 header")
    if not has_character_header:
        errors.append("DOCX missing character review table header")

    return errors


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate main-image-review-table.docx")
    parser.add_argument("docx", type=Path)
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args(argv)

    errors = validate_docx(args.docx)
    if args.format == "json":
        print(json.dumps({"valid": not errors, "errors": errors}, ensure_ascii=False, indent=2))
    else:
        if errors:
            for error in errors:
                print(f"ERROR: {error}", file=sys.stderr)
        else:
            print("main-image-review-table.docx valid")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
