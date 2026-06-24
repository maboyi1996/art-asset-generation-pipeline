# 00 Pipeline

This file defines the full execution order and the handoff rules between layers. It is the control layer for the whole skill.

## Objective

Transform a script into a verified main-image production package:
- complete enough to reduce missed characters, scenes, props, and state variants
- traceable enough that art staff can see why an asset exists
- specific enough that the generated main image fits the plot
- material-aware enough to avoid low-quality AI textures, cheap CGI, or generic beauty/style drift

The final goal is not a general story summary. The final goal is a production queue for main images.

## V2.1 Hybrid Architecture

V2.1 separates the work into three stages:

1. Identification stage (`01-06`): read by episode and scene to avoid missed characters, scenes, props, and visual states.
2. Production stage (`07-11`): produce from the global asset-state task map so each asset/state is defined once.
3. Delivery and acceptance stage (`12-13`): map the global tasks back into per-episode usage tables for review and downstream technical parsing.

Do not use one-pass global guessing as a substitute for scene coverage. Do not generate prompts independently inside each episode after the global task map exists.

V2.1 adds an output-separation guard: the complete machine production table is the source of truth, and the human review table is only a compact projection derived after validation. Human readability requirements must never change extraction breadth, state splitting, task typing, blocked/manual-review status, prompt/edit rows, or episode mapping rows.

## Global Priority

When rules compete, obey this order:
1. Script truth
2. Asset identity and state accuracy
3. Material quality and realistic image texture
4. Main-image usefulness for art review
5. Beauty, mood, and cinematic polish
6. Prompt brevity

If a visually attractive choice conflicts with the script, reject it.

## Layer Sequence

Run layers in this order:
1. `01-intake-and-script-parsing`
2. `02-scene-coverage-layer`
3. `03-asset-extraction-layer`
4. `04-state-variant-layer`
5. `05-priority-rating-layer`
6. `06-asset-registry-layer`
7. `07-character-identity-anchor-layer` for the Key Character Identity Anchor Table before any character state task is produced
8. `08-audit-layer`
9. one or more asset-specific main image layers for PDF-format analysis and global task prompt writing:
   - `09-character-main-image-layer`
   - `10-scene-main-image-layer`
   - `11-prop-main-image-layer`
10. `12-output-contracts`
11. `13-quality-checklist`

The file numbers after layer 09 remain asset-type numbers, not separate execution steps. In the execution contract, Step 9 writes selected asset analysis using the relevant 09/10/11 layer, Step 10 generates prompts using those same asset-specific layers, Step 11 runs `12-output-contracts`, and Step 12 runs `13-quality-checklist`.

Numbered files keep execution order. Unnumbered guard/template files are not workflow layers; they are called only by the numbered layers that need them.

No layer may be skipped for long-form projects unless the user explicitly narrows the task to a single known asset.

## Layer Ownership

Each layer owns a narrow responsibility:
- Intake owns source extraction and segmentation.
- Scene Coverage owns per-scene indexing.
- Asset Extraction owns candidate asset discovery.
- State Variant owns visual state separation.
- Priority Rating owns `priority_level` and `production_handling`.
- Asset Registry owns dedupe, aliases, global normalization, and the Global Asset State Task Map.
- Character Identity Anchor owns the key-character face/casting source of truth before character state production.
- Audit owns omission detection and conflict marking.
- Main Image layers own PDF-format analysis and prompt/edit-instruction generation for global asset-state tasks.
- Output Contracts owns the MD-only production files and episode mapping tables.
- Quality Checklist owns final acceptance.

Do not let a downstream layer silently rewrite upstream logic.

## Required Artifacts By Stage

After Intake:
- normalized text or chunk list
- episode/scene map
- parsing uncertainties

After Scene Coverage:
- scene coverage table
- list of scenes with no new production assets
- high-risk visual notes

After Asset Extraction:
- candidate character assets
- candidate scene assets
- candidate prop assets
- excluded background/generic items with brief reason when relevant

After State Variant:
- state variants added to candidates
- state grouping notes
- possible missed states marked for audit

After Priority Rating:
- `priority_level: S/A/B/C/D` for every asset candidate
- `production_handling` for every asset candidate
- rating and handling rationale
- derived `needs_main_image` recommendation

After Asset Registry:
- global asset-state registry
- Global Asset State Task Map
- alias map
- per-state `task_id` candidates
- per-state `task_type` candidates
- episode/scene usage index for each state
- duplicate merge notes
- unresolved conflict notes

After Character Identity Anchor:
- Key Character Identity Anchor Table / Main Character Master List
- identity anchor task IDs for S-level, recurring A-level, and user-requested key characters
- locked identity prompts or approved external reference image links
- variable state axes for later episode-level character states
- blocked/manual-review notes when identity references are missing

After Audit:
- missing asset report
- duplicate asset report
- state omission report
- manual confirmation list
- downstream rerun requirements

After Main Image Layers:
- selected global asset-state task analysis in PDF format
- main image prompts or edit instructions in PDF format
- negative prompts
- review focus for art staff

After Output Contracts:
- `main-image-production-table.md`
- `main-image-review-table.md`
- Key Character Identity Anchor Table
- Global Asset State Task Table
- Episode Asset Usage Mapping Tables
- coverage-regression note when final counts are sharply lower than prior/baseline/expected script density

After Quality Checklist:
- pass/fail status
- remaining risks
- required human review points

## Reflow Rules

If Audit finds a missing character, scene, or prop:
1. return to Asset Extraction
2. run State Variant for the new asset
3. run Priority Rating
4. update Asset Registry
5. rerun Audit
6. generate analysis and prompts only after the rerun passes

If Audit finds a missing state:
1. return to State Variant
2. rerun Priority Rating if the state changes production priority
3. update Asset Registry
4. update Character Identity Anchor if the missing state belongs to a recurring/key character
5. rerun Audit
6. regenerate only affected analysis/prompts

If a Main Image layer finds weak evidence:
1. return to Asset Registry
2. add `待人工确认` or evidence references
3. regenerate affected prompt only after the registry is corrected

If Quality Checklist finds prompt drift:
1. return to the relevant Main Image layer
2. revise using the PDF template
3. rerun Output Contracts and Quality Checklist

If Quality Checklist finds key-character identity drift:
1. return to Character Identity Anchor if the anchor table is missing, post-hoc, or not inherited downstream
2. return to Asset Registry if state rows lack identity anchor fields
3. return to Character Main Image layer if the edit prompt rewrites the face instead of applying a state delta
4. rerun Output Contracts and Quality Checklist

If Quality Checklist finds a missing episode mapping:
1. return to Scene Coverage if the episode usage was never recorded
2. return to Asset Registry if the usage row lacks a stable `state_asset_id` or `task_id`
3. return to Output Contracts if the global task exists but was not mapped into the episode table
4. rerun Quality Checklist

## Long Script Strategy

For 60-70 episode scripts:
- process by episode or episode groups
- build scene coverage per chunk
- append to a cumulative registry
- run local audit per chunk
- run global audit after all chunks
- produce prompts only from the cumulative Global Asset State Task Map

Do not attempt one-pass asset extraction over the entire project unless the text is short enough to keep reliable scene-level evidence.

Do not compress long-script output into a synopsis. The final machine table may be long. If context limits prevent complete generation in one pass, continue in chunks or report the incomplete range explicitly; do not deliver a shortened table as if it were complete.

## Completion Standard

The workflow is complete only when:
- every scene has a coverage record
- every S/A asset has script evidence
- every retained asset has `priority_level`, `production_handling`, and `handling_reason`
- every S asset is `main_task`
- every A asset is `main_task` unless a downgrade reason is explicit
- every visually meaningful state has been considered
- every key character has an identity anchor row before character state production
- every global asset-state task has a stable `task_id` and `task_type`
- every episode usage row maps to a global `task_id`
- blocked/manual-review/pending-reference states remain visible in both the global task table and episode usage mapping
- production-relevant or episode-mapped B/C assets remain visible as record-only/reuse/manual-review rows when they do not receive prompts
- audit report has no unresolved high-risk missing assets
- prompt files use the PDF-verified formats
- `main-image-production-table.md` contains the global task table and per-episode mapping tables
- `main-image-review-table.md` contains only project overview, short character identity anchors, and per-episode usage mapping for human review
