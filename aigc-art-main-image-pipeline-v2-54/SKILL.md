---
name: aigc-art-main-image-pipeline-v2-54
description: "Use this skill when Codex needs to read Chinese screenplays, novel drafts, episodic drama scripts, or project script files and produce story-faithful AIGC art main-image assets for characters, scenes, and props. V2.54 extends V2.53 by tightening scene-heading parsing, preventing character names from absorbing action/emotion/speech modifiers, preventing scene-level state clues from spreading to every character, and preserving B/C task coverage without changing middle-platform fields."
---

# AIGC Art Main Image Pipeline V2.54

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
| Asset identification | `script-intake` through `asset-registry` | Build scene facts, candidate assets, state variants, continuity ratings, global task drafts, character disposition ledger, and episode usage mapping drafts. |
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
- Every retained production asset must enter `global-task-draft` or have a visible exclusion record before prompt generation.
- Every character candidate admitted by `asset-candidate-list` must appear in `character-disposition-ledger`.
- B/C characters must not disappear because they do not need project-level face anchors.
- B/C visual characters retained as production assets must have `text_to_image` tasks; a disposition record alone is not sufficient.
- Character B/C rating uses single-episode segment continuity, not only scene count: a confirmed same person who appears only in one episode is `B` unless there is positive evidence that the role is single-segment, single-shot, background, group, generic, mention-only, or not a confirmed same person.
- Cross-episode character continuity only counts confirmed visible face-production appearances of the same concrete person. Dialogue mentions, VO, memorial objects, tombs, tablets, coffins, or ancestry references do not upgrade a character to project-level A/S.
- Character asset names must not contain action, emotion, speech-tone, or transient expression modifiers. If a phrase has a valid subject, normalize it to the subject; otherwise block it during audit.
- Character state variants must have explicit subject-level visible-state evidence. Scene-level keywords must not be copied to every character in the scene.
- Generic or group characters must be templated, grouped, excluded, or sent to review with visible reasons; repeated generic labels must not create many independent single-person face tasks without same-person evidence.
- Any unresolved character candidate disposition is a blocking delivery issue.
- The human review table is derived from the completed machine table and must never change machine-table tasks, states, ratings, review statuses, prompts, or episode mappings.

## Delivery Contract

`main-image-production-table.md` must preserve all production tasks, states, prompts, edit instructions, review statuses, evidence, episode usage references, and the character candidate disposition audit section.

`main-image-review-table.md` contains only:

- project overview
- short character identity anchor table
- episode usage mapping

Do not output JSON by default. Do not deliver internal process files unless the user explicitly asks for them.
