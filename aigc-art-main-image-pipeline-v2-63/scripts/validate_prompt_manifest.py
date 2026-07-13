#!/usr/bin/env python3
"""Validate Seedance prompt-manifest.json with V2.63 hard checks."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List


SCHEMA_VERSION = "seedance-element-extract-manifest.v1"
VALID_TEMPLATE_TYPES = {"ROLE", "SCENE", "PROP"}
VALID_PRIORITIES = {"S", "A", "B", "C"}
VALID_METHODS = {"text_to_image", "image_to_image", "image_text_edit"}
VALID_STATUSES = {"ready", "manual_review_required"}
LEGACY_TOP_LEVEL_KEYS = {"items", "main_image_tasks", "asset_state_tasks", "roleList", "sceneList", "propList"}


class ValidationError(Exception):
    pass


def expect(condition: bool, message: str, errors: List[str]) -> None:
    if not condition:
        errors.append(message)


def validate_manifest(data: Any) -> List[str]:
    errors: List[str] = []
    if not isinstance(data, dict):
        return ["Root must be a JSON object"]

    expect(data.get("schemaVersion") == SCHEMA_VERSION, "schemaVersion must be seedance-element-extract-manifest.v1", errors)
    legacy = sorted(key for key in LEGACY_TOP_LEVEL_KEYS if key in data)
    expect(not legacy, f"Legacy top-level keys are not allowed: {', '.join(legacy)}", errors)
    if "contentId" in data:
        expect(isinstance(data["contentId"], str) and bool(data["contentId"]), "contentId must be a non-empty string", errors)

    assets = data.get("assets")
    expect(isinstance(assets, list) and len(assets) > 0, "assets must be a non-empty array", errors)
    if not isinstance(assets, list):
        return errors

    asset_ids = set()
    state_ids = set()
    manual_review_count = 0

    for asset_index, asset in enumerate(assets):
        prefix = f"assets[{asset_index}]"
        expect(isinstance(asset, dict), f"{prefix} must be an object", errors)
        if not isinstance(asset, dict):
            continue

        asset_id = asset.get("assetId")
        if asset_id:
            expect(isinstance(asset_id, str), f"{prefix}.assetId must be string", errors)
            expect(asset_id not in asset_ids, f"Duplicate assetId: {asset_id}", errors)
            asset_ids.add(asset_id)

        template_name = asset.get("templateName")
        expect(isinstance(template_name, str) and bool(template_name), f"{prefix}.templateName is required", errors)
        template_type = asset.get("templateType")
        expect(template_type in VALID_TEMPLATE_TYPES, f"{prefix}.templateType must be ROLE/SCENE/PROP", errors)

        appearance = asset.get("appearance")
        expect(isinstance(appearance, dict), f"{prefix}.appearance must be an object", errors)
        if not isinstance(appearance, dict):
            continue
        appearances = appearance.get("appearances")
        expect(isinstance(appearances, list) and len(appearances) > 0, f"{prefix}.appearance.appearances must be non-empty", errors)
        if not isinstance(appearances, list):
            continue

        asset_priorities = set()
        for state_index, state in enumerate(appearances):
            state_prefix = f"{prefix}.appearance.appearances[{state_index}]"
            expect(isinstance(state, dict), f"{state_prefix} must be an object", errors)
            if not isinstance(state, dict):
                continue

            state_id = state.get("stateId")
            if state_id:
                expect(isinstance(state_id, str), f"{state_prefix}.stateId must be string", errors)
                expect(state_id not in state_ids, f"Duplicate stateId: {state_id}", errors)
                state_ids.add(state_id)

            expect(isinstance(state.get("name"), str) and bool(state.get("name")), f"{state_prefix}.name is required", errors)
            expect(isinstance(state.get("imagePrompt"), str) and bool(state.get("imagePrompt")), f"{state_prefix}.imagePrompt is required", errors)

            priority = state.get("priority")
            if priority is not None:
                expect(priority in VALID_PRIORITIES, f"{state_prefix}.priority must be S/A/B/C", errors)
                asset_priorities.add(priority)

            status = state.get("status", "ready")
            expect(status in VALID_STATUSES, f"{state_prefix}.status must be ready/manual_review_required", errors)
            if status == "manual_review_required":
                manual_review_count += 1
                has_review_focus = bool(state.get("reviewFocus"))
                metadata = asset.get("metadata") if isinstance(asset.get("metadata"), dict) else {}
                has_review_reason = bool(metadata.get("reviewReason"))
                expect(has_review_focus or has_review_reason, f"{state_prefix} manual review missing reviewFocus/reviewReason", errors)

            generation = state.get("generation")
            expect(isinstance(generation, dict), f"{state_prefix}.generation must be an object", errors)
            if isinstance(generation, dict):
                method = generation.get("method")
                expect(method in VALID_METHODS, f"{state_prefix}.generation.method invalid", errors)
                if method in {"text_to_image", "image_text_edit"}:
                    expect(isinstance(state.get("negativePrompt"), str) and bool(state.get("negativePrompt")), f"{state_prefix}.negativePrompt is required", errors)
                if method == "image_text_edit":
                    expect(isinstance(generation.get("referenceTaskId"), str) and bool(generation.get("referenceTaskId")), f"{state_prefix}.generation.referenceTaskId is required for image_text_edit", errors)

            episodes = state.get("episodes")
            if episodes is not None:
                expect(isinstance(episodes, list), f"{state_prefix}.episodes must be an array", errors)
                if isinstance(episodes, list):
                    for episode in episodes:
                        expect(isinstance(episode, int) and episode > 0, f"{state_prefix}.episodes values must be positive integers", errors)

        if asset_priorities & {"B", "C"}:
            expect(len(appearances) == 1, f"{prefix} B/C asset must not have multiple appearances", errors)
            for state in appearances:
                generation = state.get("generation") if isinstance(state, dict) else {}
                if isinstance(generation, dict):
                    expect(generation.get("method") != "image_text_edit", f"{prefix} B/C asset must not use image_text_edit", errors)

    summary = data.get("summary")
    if isinstance(summary, dict):
        if "totalItems" in summary:
            expect(summary["totalItems"] == len(assets), "summary.totalItems must equal assets.length", errors)
        if "manualReviewItems" in summary:
            expect(summary["manualReviewItems"] == manual_review_count, "summary.manualReviewItems must equal manual_review_required appearance count", errors)

    return errors


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate prompt-manifest.json")
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args(argv)

    try:
        data = json.loads(args.manifest.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        print(f"ERROR: invalid JSON: {exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    errors = validate_manifest(data)
    if args.format == "json":
        print(json.dumps({"valid": not errors, "errors": errors}, ensure_ascii=False, indent=2))
    else:
        if errors:
            for error in errors:
                print(f"ERROR: {error}", file=sys.stderr)
        else:
            print("prompt-manifest.json valid")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
