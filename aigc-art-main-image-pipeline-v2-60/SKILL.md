---
name: aigc-art-main-image-pipeline-v2-60
description: "Use this skill when Codex needs to read Chinese screenplays, novel drafts, episodic drama scripts, or project script files and produce story-faithful AIGC art main-image assets for characters, scenes, and props. V2.60 extends V2.56 by splitting the overburdened asset registry into pure registration, candidate disposition, task manifest generation, and episode usage mapping layers; moving polluted-label cleanup to asset extraction; adding state-clue disposition; and preserving hard S/A/B/C character routing without aggregate-count blocking rules."
---

# AIGC Art Main Image Pipeline V2.60

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
| Asset identification | `script-intake` through `episode-usage-map` | Build scene facts, candidate assets, polluted-label cleanup, state variants, state-clue disposition, continuity ratings, pure asset registry, candidate disposition, task drafts, and episode usage mapping drafts. |
| Production generation | `character-anchor` through `prompt-generation` | Build character anchors, audit production readiness, and generate prompts or edit instructions. |
| Delivery quality | `output-contracts` through `final-quality` | Deliver the complete machine table and derived human review table, then validate final output contracts. |

## Non-Negotiables

- Downstream layers read upstream outputs; they do not rerun upstream judgment rules.
- `script-intake.md` owns scene boundaries; downstream layers must not recut scenes.
- `scene-coverage.md` records facts only; it does not admit candidates, normalize assets, rate, or generate tasks.
- `asset-extraction.md` admits candidate assets and outputs `polluted-label-cleanup-ledger`.
- `state-variant.md` outputs both `state-variant-result` and `state-clue-disposition-ledger`.
- `asset-rating.md` is the only S/A/B/C rating layer.
- `asset-registry.md` is pure registry: only `global-asset-registry` and `alias-resolution-map`.
- `candidate-disposition.md` owns `character-disposition-ledger` and `generic-template-coverage-ledger`.
- `task-manifest-generation.md` owns `global-task-draft`.
- `episode-usage-map.md` owns `episode-usage-map-draft`.
- `prompt-generation.md` only uses templates and guards.
- `production-audit.md` only audits consistency and readiness.
- `final-quality.md` only checks final file and output contracts.
- Middle-platform production task types are only `text_to_image` and `image_text_edit`.
- `review_status` is separate from `task_type`.
- Each base asset has exactly one `priority_level`; states inherit it.
- `character-anchor-result` is not the complete character inventory; it only records face-anchor relationships.
- Every retained production asset must enter `global-task-draft` or have a visible exclusion record before prompt generation.
- Every character candidate admitted by `asset-candidate-list` must appear in `character-disposition-ledger`; rejected polluted labels must not appear there.
- B/C characters must not disappear because they do not need project-level face anchors.
- B/C visual characters retained as production assets must have `text_to_image` tasks; a disposition record alone is not sufficient.
- Character S/A/B/C rating must use the hard route in `人物评级规则.md`: confirmed same concrete person across episodes is `S/A`; confirmed same concrete person only in one episode is `C` only when all visible appearances are proven to fit one maximum 15-second segment, otherwise `B`; candidates that cannot be confirmed as the same concrete person are `C`.
- Cross-episode character continuity only counts confirmed visible face-production appearances of the same concrete person. Dialogue mentions, VO, memorial objects, tombs, tablets, coffins, or ancestry references do not upgrade a character to project-level A/S.
- Do not block only because a long project has low aggregate B/C/template counts. Blocking requires a concrete fact, candidate, state, task, mapping, or ledger break.
- Polluted labels such as `皇帝点头`、`棠宁喃喃`、`皇后拍桌`、`二夫人三夫人一起` may be recorded only in `polluted-label-cleanup-ledger.raw_label` or source evidence. They must not enter `asset-candidate-list`, `character-disposition-ledger`, asset names, state names, task names, or episode mappings.
- Character asset names must not contain action, emotion, speech-tone, or transient expression modifiers. If a phrase has a valid subject, normalize it to the subject; otherwise block it during audit.
- Dialogue speaker prefixes such as `皇帝点头：` or `棠宁喃喃：` must be normalized to the real speaker before candidate admission; the modifier may remain only in evidence, not in structured asset, state, task, or mapping names.
- Combination labels such as `两人一起` or `二夫人三夫人一起` must not become a single character asset. Split them into concrete subjects when evidence is clear; otherwise keep them as action or scene evidence.
- Transferable titles such as `四夫人` must be tied to a concrete person and timeframe. If the title refers to a prior/dead role, use a disambiguated name such as `前任四夫人` or `遇害四夫人`; do not merge it with another character's later title usage.
- Character state variants must have explicit subject-level visible-state evidence. Scene-level keywords must not be copied to every character in the scene.
- Generic or group characters must be templated, grouped, excluded, or sent to review with visible reasons; repeated generic labels must not create many independent single-person face tasks without same-person evidence.
- Any unresolved character candidate disposition is a blocking delivery issue.
- The human review table is derived from the completed machine table and must never change machine-table tasks, states, ratings, review statuses, prompts, or episode mappings.

## Delivery Contract

`main-image-production-table.md` must preserve all production tasks, states, prompts, edit instructions, review statuses, evidence, episode usage references, the global asset registry, alias map, state index, state-clue disposition table, character candidate disposition audit section, generic template coverage section, polluted-label cleanup record section, and production audit summary.

`main-image-review-table.md` contains only:

- project overview
- character identity anchor summary
- episode usage mapping summary
- blocking summary when needed

Do not output JSON by default. Do not deliver internal process files unless the user explicitly asks for them.
