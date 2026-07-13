---
name: aigc-art-main-image-pipeline-v2-63
description: "Use this skill when Codex needs to read Chinese screenplays, novel drafts, episodic drama scripts, or project script files and produce story-faithful AIGC art main-image assets for characters, scenes, and props, then deliver a Seedance prompt-manifest.json plus Markdown audit/review tables. V2.63 keeps V2.62 evidence-ledger, hard S/A/B/C rating, and S/A-only state rules, adds JSON as the middle-platform primary deliverable, and generates JSON only from the completed machine production table."
---

# AIGC Art Main Image Pipeline V2.63

This skill converts Chinese scripts into main-image production tasks for characters, scenes, and props, then projects the completed machine table into a Seedance element-library JSON manifest.

Default final outputs:

- `main-image-production-table.md`: complete machine/source-of-truth production table and audit ledger.
- `prompt-manifest.json`: Seedance middle-platform import JSON, schema `seedance-element-extract-manifest.v1`.
- `main-image-review-table.md`: compact human review table.

## Required Read Order

1. Read `framework/workflow.md` first.
2. Follow the module and layer order defined in the workflow.
3. For each layer, load only the rules, templates, guards, contracts, and scripts listed by that layer.

## Modules

| Module | Layer range | Purpose |
|---|---|---|
| Asset identification | `script-intake` through `episode-usage-map` | Build scene facts, three lossless pre-rating evidence ledgers through one ledger layer, candidate assets, polluted-label cleanup at candidate admission, hard S/A/B/C ratings, pure base-asset registry, state variants, character candidate disposition, task drafts, and episode usage mapping drafts. |
| Production generation | `character-anchor` through `prompt-generation` | Build character anchors, audit production readiness, and generate prompts or edit instructions. |
| Delivery quality | `output-contracts` through `final-quality` | Deliver the complete machine table, derive the Seedance JSON manifest from that machine table, deliver the human review table, then validate final output contracts. |

## Non-Negotiables

- `script-intake.md` owns scene boundaries; downstream layers must not recut scenes or invent new scene IDs.
- `scene-coverage.md` records facts only; it does not admit candidates, normalize final assets, rate, or generate tasks.
- `asset-evidence-ledger.md` is the only evidence-ledger workflow layer. It outputs `character-evidence-ledger`, `scene-evidence-ledger`, and `prop-evidence-ledger`.
- Evidence ledgers are lossless pre-rating records. They keep raw text, normalized subjects, visibility, same-asset clues, state clues, uncertainty, `source_locator`, and `source_evidence`; they do not admit candidates, write cleanup ledgers, rate, register, generate tasks, or decide production value.
- Evidence normalization is not candidate cleanup. `character-evidence-ledger.raw_label` may keep `三夫人害怕` while `normalized_subject` is `三夫人`; whether this creates a cleanup-ledger row is decided only by `asset-candidate-admission.md`.
- `asset-candidate-admission.md` admits candidate assets from the three evidence ledgers and outputs `asset-candidate-list` plus `polluted-label-cleanup-ledger`.
- `polluted-label-cleanup-ledger` records only candidate-admission events: polluted raw labels blocked from candidate names, split combinations, unresolved labels, manual-review needs, and high-risk contamination. It must not duplicate ordinary evidence normalization.
- Ratings happen before state splitting. `asset-rating.md` is the only S/A/B/C rating layer and must not read `state-variant-result`.
- Ratings use the matching evidence ledger as primary input, `asset-candidate-list` as candidate handoff, `scene-coverage-table` as context, and source text only to verify evidence. Ratings must not rescan PDFs, recut scenes, silently invent candidates, or repair candidate names.
- If a rating layer finds visible evidence missing from an evidence ledger or candidate list, it must block and point back to the owning evidence or candidate-admission layer instead of silently patching downstream.
- `asset-registry.md` is pure base-asset registry: it outputs only `global-asset-registry` and `alias-resolution-map`. It does not create state IDs.
- Each base asset has exactly one `priority_level`; states inherit it.
- `state-variant.md` runs after registry. It outputs `state-variant-result` and `state-clue-disposition-ledger`; state splitting and state-clue disposition are scoped to S/A assets only. B/C assets must not enter state splitting, state-clue disposition, manual state review, or state task generation.
- `character-candidate-disposition.md` owns `character-disposition-ledger` and `generic-template-coverage-ledger` for admitted character candidates only. Rejected polluted labels must not appear there.
- `task-manifest-generation.md` owns `global-task-draft`; downstream layers must not create tasks.
- `episode-usage-map.md` owns `episode-usage-map-draft`; it maps scene usage to existing task IDs or explicit exclusion/disposition references only.
- `character-anchor-result` is not the complete character inventory; it only records face-anchor relationships.
- B/C characters must not disappear because they do not need project-level face anchors.
- B/C visual characters retained as production assets must have `text_to_image` tasks; a disposition record alone is not sufficient.
- Character S/A/B/C rating must use the hard route in `人物评级规则.md`: confirmed same concrete person across episodes is `S/A`; confirmed same concrete person only in one episode is `C` only when all visible appearances are proven to fit one maximum 15-second segment, otherwise `B`; candidates that cannot be confirmed as the same concrete person are `C`.
- Cross-episode character continuity only counts confirmed visible face-production appearances of the same concrete person. Dialogue mentions, VO, memorial objects, tombs, tablets, coffins, or ancestry references do not upgrade a character to project-level A/S.
- Do not block only because a long project has low aggregate B/C/template counts. Blocking requires a concrete fact, candidate, state, task, mapping, ledger, or evidence-chain break.
- Polluted labels such as `皇帝点头`、`棠宁喃喃`、`皇后拍桌`、`二夫人三夫人一起` may be recorded only in evidence ledger raw fields, `polluted-label-cleanup-ledger.raw_label`, or source evidence. They must not enter `asset-candidate-list`, `character-disposition-ledger`, asset names, state names, task names, episode mappings, or JSON element names.
- Character asset names must not contain action, emotion, speech-tone, sound, transient expression, or combination modifiers. If a phrase has a valid subject, normalize it to the subject; otherwise block or review it during candidate admission.
- Dialogue speaker prefixes such as `皇帝点头：` or `棠宁喃喃：` must be normalized to the real speaker before candidate admission; the modifier may remain only in evidence, not in structured asset, state, task, mapping, or JSON names.
- Combination labels such as `两人一起` or `二夫人三夫人一起` must not become a single character asset. Split them into concrete subjects when evidence is clear; otherwise keep them as action or scene evidence.
- Transferable titles such as `四夫人` must be tied to a concrete person and timeframe. If the title refers to a prior/dead role, use a disambiguated name such as `前任四夫人` or `遇害四夫人`; do not merge it with another character's later title usage.
- Character state variants must have explicit S/A subject-level visible-state evidence. Scene-level keywords must not be copied to every character in the scene. B/C character state clues are out of scope and must not be retained in state ledgers.
- Generic or group characters must be templated, grouped, excluded, or sent to review with visible reasons; repeated generic labels must not create many independent single-person face tasks without same-person evidence.
- Any unresolved character candidate disposition is a blocking delivery issue.
- Middle-platform production task types are only `text_to_image` and `image_text_edit`.
- `review_status` is separate from `task_type`.
- The machine table `全局生产任务表` must include stable `base_asset_id` and `state_asset_id` fields for JSON projection.
- `prompt-generation.md` only uses templates and guards.
- `production-audit.md` only audits consistency and readiness.
- `output-contracts.md` outputs only `main-image-production-table.md` and `main-image-review-table.md`; it must not directly output JSON.
- `json-manifest-generation.md` reads the completed machine table and outputs only `prompt-manifest.json`; it must not create, rename, merge, rate, split, exclude, repair, or rewrite assets, states, tasks, prompts, review statuses, or episode mappings.
- `final-quality.md` only checks final file and output contracts.
- The human review table is derived from the completed machine table and must never change machine-table tasks, states, ratings, review statuses, prompts, JSON fields, or episode mappings.
- JSON import assets use one element per base asset. Multiple visual states for the same role, scene, or prop must appear under that element's `appearance.appearances[]`, not as duplicate JSON assets.
- JSON `templateType` values are only `ROLE`, `SCENE`, and `PROP`, mapped from character, scene, and prop assets.
- JSON must be a real `.json` file with no Markdown fences, comments, JSON5 syntax, or numeric large IDs.

## Delivery Contract

`main-image-production-table.md` must preserve all production tasks, states, prompts, edit instructions, review statuses, evidence, episode usage references, the three pre-rating evidence ledgers, the global asset registry, alias map, state index, state-clue disposition table, character candidate disposition audit section, generic template coverage section, polluted-label cleanup section, and production audit summary.

`prompt-manifest.json` must conform to `references/json-contracts/seedance-element-extract-manifest.v1.schema.json`, use `assets` as the canonical top-level element list, and be derived only from `main-image-production-table.md`.

`main-image-review-table.md` contains only:

- project overview
- character identity anchor summary
- episode usage mapping summary
- blocking summary when needed

Do not deliver internal process files unless the user explicitly asks for them. The JSON schema, contract files, and scripts are bundled resources, not final deliverables.
