# 00 Pipeline

This file defines the full execution order and the handoff rules between layers. It is the control layer for the whole skill.

## Objective

Transform a script into a verified main-image production package:
- complete enough to reduce missed characters, scenes, props, and state variants
- traceable enough that art staff can see why an asset exists
- specific enough that the generated main image fits the plot
- material-aware enough to avoid low-quality AI textures, cheap CGI, or generic beauty/style drift

The final goal is not a general story summary. The final goal is a production queue for main images.

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
7. `07-audit-layer`
8. one or more asset-specific main image layers:
   - `08-character-main-image-layer`
   - `09-scene-main-image-layer`
   - `10-prop-main-image-layer`
9. `11-output-contracts`
10. `12-quality-checklist`

No layer may be skipped for long-form projects unless the user explicitly narrows the task to a single known asset.

## Layer Ownership

Each layer owns a narrow responsibility:
- Intake owns source extraction and segmentation.
- Scene Coverage owns per-scene indexing.
- Asset Extraction owns candidate asset discovery.
- State Variant owns visual state separation.
- Priority Rating owns S/A/B/C production priority.
- Asset Registry owns dedupe, aliases, and global normalization.
- Audit owns omission detection and conflict marking.
- Main Image layers own PDF-format analysis and prompt generation.
- Output Contracts owns stable production files.
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
- S/A/B/C rating for every asset candidate
- rating rationale
- `needs_main_image` recommendation

After Asset Registry:
- global asset registry
- alias map
- duplicate merge notes
- unresolved conflict notes

After Audit:
- missing asset report
- duplicate asset report
- state omission report
- manual confirmation list
- downstream rerun requirements

After Main Image Layers:
- selected asset analysis in PDF format
- main image prompts in PDF format
- negative prompts
- review focus for art staff

After Output Contracts:
- stable filenames and machine-readable manifest

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
4. rerun Audit
5. regenerate only affected analysis/prompts

If a Main Image layer finds weak evidence:
1. return to Asset Registry
2. add `待人工确认` or evidence references
3. regenerate affected prompt only after the registry is corrected

If Quality Checklist finds prompt drift:
1. return to the relevant Main Image layer
2. revise using the PDF template
3. rerun Output Contracts and Quality Checklist

## Long Script Strategy

For 60-70 episode scripts:
- process by episode or episode groups
- build scene coverage per chunk
- append to a cumulative registry
- run local audit per chunk
- run global audit after all chunks

Do not attempt one-pass asset extraction over the entire project unless the text is short enough to keep reliable scene-level evidence.

## Completion Standard

The workflow is complete only when:
- every scene has a coverage record
- every S/A asset has script evidence
- every visually meaningful state has been considered
- audit report has no unresolved high-risk missing assets
- prompt files use the PDF-verified formats
- `prompt-manifest.json` can drive batch generation later
