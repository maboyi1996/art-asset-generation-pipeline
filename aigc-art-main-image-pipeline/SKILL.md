---
name: aigc-art-main-image-pipeline
description: "Use this skill when the user wants Codex to read Chinese screenplays, novel drafts, episodic drama scripts, or project script files and produce story-faithful AIGC art main-image assets for characters, scenes, and props. The workflow is layered: script parsing, scene coverage, asset extraction, state variant detection, priority rating, registry merging, audit, PDF-verified main-image analysis, PDF-verified prompt generation, output contracts, and final quality checks."
---

# AIGC Art Main Image Pipeline

This skill converts scripts into production-ready **main image** tasks for art review.

It stops at main image production:
- Characters: main portrait / character reference only. No three-view sheet, proportion correction, or final turnaround.
- Scenes: main scene reference only. No multi-angle expansion, lighting polish package, or final scene design.
- Props: main prop reference only. Usually isolated clean-background prop images.

## Non-Negotiables

1. Plot fit is the first core requirement.
2. Image material quality is the second core requirement.
3. Every asset judgment must be traceable to script evidence.
4. Never generate prompts before scene coverage, asset extraction, state detection, rating, registry merge, and audit are complete.
5. Step 8 asset analysis and Step 9 main image prompts must use the PDF-verified templates referenced by the relevant asset layer.
6. If a later layer finds an upstream error, return to the owning layer, fix it there, and rerun downstream checks.
7. Do not invent unsupported visuals. Mark `待人工确认` or `信息冲突` when evidence is insufficient or contradictory.
8. Character state variants must be based on visible character appearance only. Do not treat props, locations, actions, emotions, relationships, or plot events as character states.
9. Character main-image prompts must be single-character, English-only image prompts with a plain solid/neutral background, no props, no scene, and no Chinese plot evidence inside the prompt text.

## Required Read Order

Always read these first:
- [references/00-pipeline.md](references/00-pipeline.md)
- [references/01-intake-and-script-parsing.md](references/01-intake-and-script-parsing.md)
- [references/02-scene-coverage-layer.md](references/02-scene-coverage-layer.md)
- [references/03-asset-extraction-layer.md](references/03-asset-extraction-layer.md)
- [references/04-state-variant-layer.md](references/04-state-variant-layer.md)
- [references/04-state-variant-standard.md](references/04-state-variant-standard.md)
- [references/05-priority-rating-layer.md](references/05-priority-rating-layer.md)
- [references/06-asset-registry-layer.md](references/06-asset-registry-layer.md)
- [references/07-audit-layer.md](references/07-audit-layer.md)
- [references/11-output-contracts.md](references/11-output-contracts.md)
- [references/12-quality-checklist.md](references/12-quality-checklist.md)

Read the asset-specific layer before producing analysis or prompts:
- Character assets: [references/08-character-main-image-layer.md](references/08-character-main-image-layer.md) and [references/pdf-character-templates.md](references/pdf-character-templates.md)
- Scene assets: [references/09-scene-main-image-layer.md](references/09-scene-main-image-layer.md) and [references/pdf-scene-templates.md](references/pdf-scene-templates.md)
- Prop assets: [references/10-prop-main-image-layer.md](references/10-prop-main-image-layer.md) and [references/pdf-prop-templates.md](references/pdf-prop-templates.md)

## Execution Contract

Use the layered workflow exactly:
1. Intake and parse the script.
2. Build scene coverage.
3. Extract candidate assets.
4. Detect state variants.
5. Rate priority.
6. Build the asset registry.
7. Run audit.
8. Write PDF-verified asset analysis for selected assets.
9. Generate PDF-verified main image prompts.
10. Produce the output contract files.
11. Run the final quality checklist.

For long scripts, process in chunks, but maintain one cumulative registry and one cumulative audit trail.

## Primary Deliverables

Always produce two final outputs:
- `main-image-production-table.md`
- `prompt-manifest.json`

`main-image-production-table.md` is the art-facing production table. It must be readable like a spreadsheet and include:
- project-level main character summary at the top
- episode-by-episode character, scene, and prop main image tasks
- priority rating
- state name
- compact evidence
- final main image prompt
- negative prompt
- review focus

`prompt-manifest.json` is the machine-facing production manifest. It must contain the same task set and prompts as the human table, but in stable JSON fields suitable for image API use or model reading.

Intermediate artifacts such as scene coverage, registry, audit report, and full biographies are internal working materials. Do not deliver them as separate final files unless the user asks to inspect/debug the pipeline.

Do not store API secrets in the skill or generated files.
