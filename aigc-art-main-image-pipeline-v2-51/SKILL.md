---
name: aigc-art-main-image-pipeline-v2-51
description: "Use this skill when the user wants Codex to read Chinese screenplays, novel drafts, episodic drama scripts, or project script files and produce story-faithful AIGC art main-image assets for characters, scenes, and props. V2.51 extends V2.5 with a character disposition ledger that prevents B/C character candidates from disappearing just because they do not need project-level face anchors, while preserving explicit layer contracts and the machine/review Markdown outputs."
---

# AIGC Art Main Image Pipeline V2.51

This skill converts Chinese scripts into main-image production tasks for characters, scenes, and props.

Default final outputs:

- `main-image-production-table.md`: complete machine/source-of-truth production table.
- `main-image-review-table.md`: compact human review table.

## Required Read Order

1. Read `framework/workflow.md` first.
2. Follow the module and layer order defined in the workflow.
3. For each layer, load only the rules, templates, and guards listed by that layer.

## Modules

| Module | Layer range | Purpose |
|---|---|---|
| Asset identification | `script-intake` through `asset-registry` | Build scene facts, candidate assets, state variants, continuity ratings, task drafts, character disposition ledger, and episode usage mapping drafts. |
| Production generation | `character-anchor` through `prompt-generation` | Build character anchors, audit production readiness, and generate prompts or edit instructions. |
| Delivery quality | `output-contracts` through `final-quality` | Deliver the two Markdown files and validate final quality. |

## Non-Negotiables

- Downstream layers read upstream outputs; they do not rerun upstream judgment rules.
- `asset-extraction.md` only admits candidate assets.
- `prompt-generation.md` only uses templates and guards.
- `production-audit.md` only audits consistency and readiness.
- Middle-platform production task types are only `text_to_image` and `image_text_edit`.
- `review_status` is separate from `task_type`.
- Each base asset has exactly one `priority_level`; states inherit it.
- `character-anchor-result` is not the complete character inventory; it only records face-anchor relationships.
- Every character candidate admitted by `asset-candidate-list` must appear in `character-disposition-ledger`.
- B/C characters must not disappear because they do not need project-level face anchors.
- Any unresolved character candidate disposition is a blocking delivery issue.
- The human review table is derived from the completed machine table and must never change machine-table tasks, states, ratings, review statuses, prompts, or episode mappings.

## Delivery Contract

`main-image-production-table.md` must preserve all production tasks, states, prompts, edit instructions, review statuses, evidence, episode usage references, and the character candidate disposition audit section.

`main-image-review-table.md` contains only:

- project overview
- short character identity anchor table
- episode usage mapping

Do not output JSON by default. Do not deliver internal process files unless the user explicitly asks for them.
