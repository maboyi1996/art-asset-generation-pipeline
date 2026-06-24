# 13 Quality Checklist

This layer is the final acceptance gate.

## Goal

Catch failures before the output reaches art staff or an image API:
- plot drift
- missed states
- missed flashback / past-period variants
- omitted per-episode asset usage
- unsupported visual invention
- weak material prompts
- generic AI image drift
- invalid output structure
- broken global-task-to-episode mapping

## Checklist Order

Run checks in this order:
1. Source traceability
2. Scene coverage
3. Asset registry and global task map
4. State variants
5. Rating
6. Audit resolution
7. PDF template compliance
8. Prompt content
9. Material quality
10. Photographic realism / anti-CG guard
11. Character identity anchor / state editing
12. Episode asset usage
13. Output contract

## 1. Source Traceability

Pass criteria:
- every S/A asset has script evidence
- every state asset has state evidence or `待人工确认`
- every prompt-critical visual detail has source support or conservative inference
- evidence includes scene IDs
- flashback / past-period states include timeline evidence

Fail if:
- an S/A asset has no evidence
- prompt contains unsupported exact costume/material/status
- conflict is hidden
- flashback / past-period states lack timeline evidence

Return layer:
- Asset Registry
- relevant Main Image layer

## 2. Scene Coverage

Pass criteria:
- every parsed scene has coverage
- every scene has `timeline_period`
- every flashback / past-period scene has state clues or visible-equivalence notes
- every scene has episode asset usage candidates
- no-new-asset scenes are explicitly marked
- present and referenced characters are separated
- props and state clues are captured

Fail if:
- scenes were skipped
- a scene lacks `timeline_period`
- flashback / past-period clues appear in source but not coverage
- state clues appear in source but not coverage
- no-new-asset scenes lack usage candidates
- important prop use is absent

Return layer:
- Scene Coverage

## 3. Asset Registry / Global Task Map

Pass criteria:
- no loose production asset outside registry
- aliases are preserved
- base/state relationship is clear
- `needs_main_image` is explicit
- every production-relevant state has stable `state_asset_id`, `task_id`, and `task_type`
- every global task row has allowed `task_type`
- every used state preserves episode/scene mapping data
- blocked assets are visible
- reused assets can be referenced by stable IDs

Fail if:
- prompt exists for unregistered asset
- duplicate names create ambiguity
- state prompt has no base asset
- episode usage references an unknown asset
- a production-relevant state lacks `task_id` or `task_type`
- a global task row lacks episode/scene mapping data

Return layer:
- Asset Registry

## 4. State Variants

Pass criteria:
- visually meaningful costume, hair, body, scene, and prop changes are split or intentionally not split
- state names follow `角色名--外观（XX）状态`, `场景名--初始（XX）状态`, or `道具名--初始（XX）状态`
- character states are based only on visible character appearance changes
- scene states are based only on visible spatial-condition changes
- prop states are based only on visible object-condition changes
- flashback / past-period appearance and scene changes are split or intentionally merged with visible-equivalence reasons
- props, locations, actions, emotions, relationships, and plot events are not used as character states
- emotional-only changes are not over-split

Fail if:
- wet hair/bathing/injury/costume change is missing as state
- scene day/night/event/destruction state is ignored
- prop broken/bloodied/opened state is ignored
- a childhood/youth/older/past-period character appearance is missing as a state
- a visibly different flashback/past-period location is missing as a scene state
- a character state is named after cash, contracts, wine bowls, vehicles, phones, reports, or other props
- a character state is named after a room, winery, forum, field, office, or other location
- a character state is named after a plot event such as dividing money, signing, refusing acquisition, being humiliated, reporting, or revenge
- a state split would not be visible in a static main image

Return layer:
- State Variant

## 5. Rating

Pass criteria:
- every asset has S/A/B/C
- every rating has reason
- every S/A item usually has `needs_main_image: true`
- B/C exceptions are explicit

Fail if:
- rating is unexplained
- core asset is B/C without reason
- background item is S/A without production reason

Return layer:
- Priority Rating

## 6. Audit Resolution

Pass criteria:
- audit report exists
- missing assets/states are resolved, deferred, or manual-review marked
- flashback / past-period variant omissions are resolved
- episode usage omissions are resolved
- duplicate/conflict issues are visible
- downstream reruns were performed when needed

Fail if:
- audit found missing asset but prompt generation continued
- unresolved conflict affects prompt
- timeline audit found missing variants but output proceeded
- episode usage audit found missing rows but output proceeded

Return layer:
- Audit or upstream owner layer

## 7. PDF Template Compliance

Pass criteria:
- character analysis uses character biography template
- character prompt uses character main image template
- scene analysis uses scene biography template
- scene prompt uses scene main image template
- prop analysis uses prop biography template
- prop prompt uses prop main image template

Fail if:
- prompt is a short custom paragraph
- analysis skips required sections without user instruction
- asset-specific template is mixed up

Return layer:
- relevant Main Image layer

## 8. Prompt Content

Pass criteria:
- prompt states asset identity
- prompt states story function
- prompt states state name visually
- prompt includes what to avoid
- prompt supports main image review
- character image prompts are English-only image-generation text
- character image prompts show one character only
- character image prompts use a plain solid or neutral background
- character image prompts contain no props, scenes, other characters, action staging, or Chinese plot evidence
- scene image prompts are empty or near-empty by default
- scene image prompts contain no crowd or recognizable people unless the asset is explicitly an event/crowd-state reference

Fail if:
- prompt could generate a generic attractive person/room/object
- state is missing from prompt
- scene prompt lacks layout
- prop prompt lacks exact object type
- character prompt includes cash, contracts, wine bowls, phones, vehicles, reports, furniture, bags, backpacks, or other props
- character prompt includes living room, winery, forum, office, field, or other scene/location descriptions
- character prompt includes Chinese scene IDs or Chinese plot sentences inside the image prompt
- character prompt stages a plot event instead of a clean portrait reference
- scene prompt creates a crowd documentary photo when the task is a scene reference
- scene prompt contains many people, recognizable faces, named-character blocking, or foreground action without an explicit event/crowd-state reason

Return layer:
- relevant Main Image layer
- State Variant first if prompt leakage comes from an invalid state name

## 9. Material Quality

Pass criteria:
- character prompts control skin, hair, fabric, light
- scene prompts control wall/floor/furniture/material/lighting
- prop prompts control surface, scale, reflection, wear/condition
- negative prompts block plastic, waxy, fake CGI, low-quality texture

Fail if:
- material language is vague
- prompt only describes mood
- prompt over-indexes on beauty/luxury without texture
- no negative controls for common AI artifacts

Return layer:
- relevant Main Image layer

## 10. Photographic Realism / Anti-CG Guard

Pass criteria:
- every main image prompt includes photographic realism controls appropriate to the asset type
- prompts use script evidence and any input/reference image brightness as the exposure reference instead of mechanically forcing a clock time
- scenes do not read as game levels, environment concept art, PBR asset showcases, or poster compositions
- scenes include limited camera dynamic range, physical light falloff, restrained texture density, low-information large surfaces, and natural camera limitations
- large surfaces are not filled with dense repeated cracks, repeated stains, procedural noise, or equal micro-detail everywhere
- wet floors, stone, metal, glass, fabric, and wood have physically plausible reflection behavior, not mirror-like CG floors or uniform wet shaders
- fire, candles, windows, sky, lamps, neon, or other light sources affect only plausible local areas unless evidence supports broader illumination
- UI elements, watermarks, stickers, avatars, icons, modern interface artifacts, readable modern text, and visible brand logos are explicitly blocked
- character prompts block AI beauty face, waxy/plastic skin, over-retouched glamour, and commercial campaign polish
- prop prompts block PBR product render, luxury catalog polish, environment reflections, hands, extra objects, readable text, and watermark

Fail if:
- a scene prompt still leans on cinematic fantasy, epic concept art, high-end production design, high production value, or all-over sharp detail as style drivers
- a prompt forces dawn/night/day/clock time without source support or reference brightness support
- a scene would likely generate a game screenshot, Unreal Engine / Blender / Octane render, PBR asset look, mirror-like CG floor, or uniform wet shader
- all materials are equally crisp, glossy, ornate, or texture-dense
- light sources behave decoratively instead of physically
- prompt does not block UI/watermark/icon/avatar artifacts for image editing tasks

Return layer:
- relevant Main Image layer
- Scene Main Image layer first when the failure is environmental or lighting related

## 11. Character Identity Anchor / State Editing

Pass criteria:
- S-level characters, recurring A-level characters, and user-requested key characters appear in the Main Character Master List before dependent character state tasks
- the Key Character Identity Anchor Table is built from the global registry before any dependent character state production rows are written
- the anchor table is not derived from a single episode and is not filled after episode tables as a presentation-only summary
- each key character has an `identity_anchor_task_id`, `identity_anchor_prompt`, `identity_reference_image`, `identity_lock_status`, `stable_face_identity`, and `variable_state_axes`
- the first key-character image task is `text_to_image_identity_anchor` unless an approved external reference image already exists
- later states of the same key character use `image_edit_from_identity_anchor` or `image_edit_identity_sensitive_state`
- later state prompts preserve the approved identity image and change only wardrobe, grooming, hair condition, makeup, injury, illness, fatigue, dirt, blood, wetness, class styling, or other script-supported visible state details
- state edit tasks include `locked_identity_prompt`, `state_delta_prompt`, `edit_instruction`, `identity_change_allowed`, and `identity_change_reason`
- missing or unapproved identity reference images block later state edits or route them to manual review
- normal wardrobe/state edits explicitly prevent face redesign, beautification, de-aging, changed ethnicity/region, changed facial proportions, and generic replacement faces

Fail if:
- dependent character state production rows are generated before the Key Character Identity Anchor Table exists
- the key-character anchor table is treated as a post-hoc summary instead of a workflow gate
- a key-character anchor is sourced from one episode's state prompt instead of the global character registry
- the same key character has multiple independent full text-to-image prompts for different episode states
- a later state prompt rewrites the whole face/casting description instead of referencing the identity anchor
- a later state task lacks `identity_anchor_task_id` or `identity_reference_image`
- an unavailable identity reference image is ignored and the task proceeds as independent text-to-image
- wardrobe, prop, location, emotion, or plot event is treated as a new face identity
- a state edit allows face redesign without script-supported `identity_change_reason`
- the Main Character Master List is treated only as review text and not used downstream

Return layer:
- Character Main Image layer
- Asset Registry
- Output Contracts

## 12. Episode Asset Usage

Pass criteria:
- every episode has an Episode Asset Usage Mapping Table
- every used character, scene, and prop state appears in episode mapping
- every episode mapping row has `state_asset_id`, `task_id`, `task_type`, and `usage_type`
- every episode mapping row joins to exactly one Global Asset State Task Table row by `task_id`
- reused assets are listed as `reuse_existing`, not omitted
- `reference_task_id` and `reuse_from_task_id` are filled when known
- episode-local repeated minor characters and props are listed in episode mapping even when they do not receive new main-image prompts

Fail if:
- an episode only lists newly generated assets and omits reused characters/scenes/props
- a minor character or prop appears multiple times within one episode but is treated as a one-shot background detail
- reused assets are duplicated as new prompt tasks only to show usage
- flashback assets are missing from usage lists
- an episode mapping row lacks `task_id` or `state_asset_id`
- an episode mapping row points to no global task row
- a global task row is re-created inside an episode table instead of referenced

Return layer:
- Scene Coverage
- Asset Registry
- Output Contracts

## 13. Output Contract

Pass criteria:
- final output includes `main-image-production-table.md`
- final output includes `main-image-review-table.md`
- final output is Markdown-only by default
- output is readable as a production table, not a pile of process files
- major characters are summarized at the top
- key character identity anchor fields are present in the master list
- Global Asset State Task Table exists
- Episode Asset Usage Mapping Tables exist
- `main-image-production-table.md` is the complete machine/source-of-truth table with global task rows and prompts/edit instructions
- `main-image-review-table.md` is the human review table and includes only `项目概览`, `角色身份锚点（短表）`, and `分集使用映射`
- `main-image-review-table.md` does not include `全局资产状态任务（短表）`, full prompts, negative prompts, or long edit-instruction fields
- `main-image-review-table.md` is derived from the completed machine table and has not changed task counts, state splits, task types, blocked statuses, or episode mapping row counts
- recurring/key character states use identity-anchor edit fields instead of independent full text-to-image prompts
- every global task row has `task_id`, `task_type`, `asset_type`, `state_asset_id`, status, and evidence/review fields
- every episode section maps used assets to global `task_id`s
- task rows use allowed `task_type` values: `text_to_image`, `image_text_edit`, `reuse_existing`, `blocked`, `manual_review`
- `image_text_edit` rows include reference image and state delta fields
- `reuse_existing` rows do not contain new prompts
- no final placeholders remain
- no API secrets are included

Fail if:
- final delivery exposes internal coverage/registry/audit files by default
- output requires `prompt-manifest.json` by default
- art staff must read full biographies to find prompts
- art staff must inspect the machine long table to perform ordinary episode/asset review
- the human review Markdown contains a global task table or prompt columns
- creating the human review Markdown changes or reduces the machine table's global tasks, state variants, task types, blocked statuses, or episode mappings
- missing table rows for S/A generated tasks
- Global Asset State Task Table is missing or incomplete
- Episode Asset Usage Mapping Tables are missing or incomplete
- an episode mapping row cannot join to a global task row
- a reused asset is regenerated only to show episode usage
- secrets are embedded

Return layer:
- Output Contracts

## Final Pass Statement

At final delivery, include a compact quality statement:
- number of global asset-state tasks by `task_type` and priority
- number of episode mapping rows
- unresolved manual review count
- whether the machine production table is ready for AI/downstream parsing
- whether the human review Markdown is ready for art review
- whether every episode mapping row joins to a global task

Do not claim zero risk for long scripts. Say what was checked and what remains for human review.
