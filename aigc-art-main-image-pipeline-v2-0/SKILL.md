---
name: aigc-art-main-image-pipeline-v2-0
description: "Use this skill when the user wants Codex to read Chinese screenplays, novel drafts, episodic drama scripts, or project script files and produce story-faithful AIGC art main-image assets for characters, scenes, and props. V2.0 uses a hybrid workflow: identify assets by episode/scene, produce prompts by global asset state, then deliver two MD outputs by default: a machine/source-of-truth production table and a human-readable Markdown review table."
---

# AIGC Art Main Image Pipeline V2.0

This skill converts scripts into production-ready **main image** tasks for art review.

V2.0 uses a hybrid architecture:
- Identification reads by episode and scene so assets are not missed.
- Production works from one global asset-state task map so each asset/state is defined once.
- Delivery returns to episode tables by mapping each episode usage row back to the global task ID.

It stops at main image production:
- Characters: main portrait / character reference only. No three-view sheet, proportion correction, or final turnaround.
- Scenes: main scene reference only. No multi-angle expansion, lighting polish package, or final scene design.
- Props: main prop reference only. Usually isolated clean-background prop images.

## Non-Negotiables

1. Plot fit is the first core requirement.
2. Image material quality is the second core requirement.
3. Every asset judgment must be traceable to script evidence.
4. Never generate prompts before scene coverage, asset extraction, state detection, rating, registry merge, and audit are complete.
5. Step 9 asset analysis and Step 10 main image prompts must use the PDF-verified templates referenced by the relevant asset layer.
6. If a later layer finds an upstream error, return to the owning layer, fix it there, and rerun downstream checks.
7. Do not invent unsupported visuals. Mark `待人工确认` or `信息冲突` when evidence is insufficient or contradictory.
8. Character state variants must be based on visible character appearance only. Do not treat props, locations, actions, emotions, relationships, or plot events as character states.
9. Character main-image prompts must be single-character, English-only image prompts with a plain solid/neutral background, no props, no scene, and no Chinese plot evidence inside the prompt text.
10. Flashback / past-period scenes must be explicitly tracked with `timeline_period`; characters and scenes in a flashback must be audited for age, clothing, class/status, and spatial-condition variants.
11. Scene main-image prompts default to empty or near-empty spaces. Do not generate crowds or recognizable people unless the scene asset itself is an event/crowd-state reference.
12. Separate global asset-state tasks from episode usage. The global task table defines each character, scene, and prop state once; episode usage rows map back to that global `task_id`.
13. Final delivery is MD-only by default, but it must include two Markdown files: one machine/source-of-truth production table and one human review table. Do not produce `prompt-manifest.json` unless the user explicitly asks for a separate technical conversion artifact.
14. The human review table is a derived view of the completed machine table. Never let `main-image-review-table.md` requirements reduce, merge, block, omit, rename, or otherwise change global asset-state tasks, state variants, prompts, or episode mapping rows in `main-image-production-table.md`.

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
- [references/07-character-identity-anchor-layer.md](references/07-character-identity-anchor-layer.md)
- [references/08-audit-layer.md](references/08-audit-layer.md)
- [references/12-output-contracts.md](references/12-output-contracts.md)
- [references/13-quality-checklist.md](references/13-quality-checklist.md)
- [references/photographic-realism-style-guard.md](references/photographic-realism-style-guard.md)

Read the asset-specific layer before producing analysis or prompts:
- Character assets: [references/09-character-main-image-layer.md](references/09-character-main-image-layer.md), [references/pdf-character-templates.md](references/pdf-character-templates.md), and [references/character-state-edit-prompt-guard.md](references/character-state-edit-prompt-guard.md)
- Scene assets: [references/10-scene-main-image-layer.md](references/10-scene-main-image-layer.md) and [references/pdf-scene-templates.md](references/pdf-scene-templates.md)
- Prop assets: [references/11-prop-main-image-layer.md](references/11-prop-main-image-layer.md) and [references/pdf-prop-templates.md](references/pdf-prop-templates.md)

## Execution Contract

Use the layered workflow exactly:
1. Intake and parse the script.
2. Build scene coverage.
3. Extract candidate assets.
4. Detect state variants.
5. Rate priority.
6. Build the global asset-state registry and global asset-state task map.
7. Build the Key Character Identity Anchor Table from the global registry before producing dependent character state tasks.
8. Run audit.
9. Write PDF-verified asset analysis for global asset-state tasks.
10. Generate PDF-verified main image prompts or edit instructions for global asset-state tasks.
11. Produce the MD output contract with the machine production table and the human review table.
12. Run the final quality checklist.

For long scripts, process in chunks, but maintain one cumulative registry and one cumulative audit trail.

File numbers are still meaningful execution order:
- `01-06`: identification stage.
- `07-11`: production stage.
- `12-13`: delivery and acceptance stage.
- Unnumbered guard/template files are called by the numbered layers that need them.

The Key Character Identity Anchor Table is a workflow gate, not only a final-output section. For S-level characters, recurring A-level characters, and user-requested key characters, establish the locked face/casting identity there before generating character state prompts. Character state rows must inherit the key character identity anchor, or a non-key character's first approved/generated reference image, and add only state-specific deltas unless script evidence requires an identity-sensitive change.

## Primary Deliverables

Always produce two final Markdown outputs by default:
- `main-image-production-table.md`: machine/source-of-truth production table for AI models, prompt generation, and downstream technical parsing.
- `main-image-review-table.md`: human-readable Markdown review table for art review.

`main-image-production-table.md` is the complete machine table. It must include:
- project-level main character summary at the top
- Key Character Identity Anchor Table before episode-by-episode tables
- Global Asset State Task Table, where each asset/state is defined once
- episode-by-episode asset usage mapping tables, including reused character, scene, and prop states
- stable `task_id`, `task_type`, reference, reuse, and status fields
- priority rating
- state name
- character identity anchor and state-editing fields when the task is a character edit task
- compact evidence
- final main image prompt or edit instruction
- negative prompt
- review focus

`main-image-review-table.md` is the human audit table. Keep it compact and readable in ordinary Markdown previewers. It must include only:
- `项目概览`
- `角色身份锚点（短表）`
- `分集使用映射`

Create `main-image-review-table.md` only after `main-image-production-table.md` is complete and validated. Derive it from the completed machine table. Do not re-run asset extraction, state merging, priority rating, blocking decisions, or prompt generation for the review file.

Do not include a `全局资产状态任务（短表）` section in `main-image-review-table.md`. Do not include full prompts, negative prompts, locked identity prompts, edit instructions, or long global task rows in the human review file. The human review file may include `task_id`, `state_asset_id`, and compact notes so reviewers can reference the machine table when needed.

Intermediate artifacts such as scene coverage, registry, audit report, and full biographies are internal working materials. Do not deliver them as separate final files unless the user asks to inspect/debug the pipeline.

Do not store API secrets in the skill or generated files.
