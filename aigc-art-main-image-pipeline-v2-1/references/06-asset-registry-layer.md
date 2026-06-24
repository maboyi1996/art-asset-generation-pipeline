# 06 Asset Registry Layer

This layer creates the single source of truth for all downstream analysis, prompts, and episode mapping.

## Goal

Merge candidates into a global asset-state registry with stable IDs, aliases, states, evidence, ratings, production flags, and task-map fields.

No main image analysis, prompt, edit instruction, or episode delivery row should be generated from loose notes. It must come from the registry and the Global Asset State Task Map.

## Inputs

Use:
- rated candidate assets
- state variant map
- evidence records
- scene coverage
- exclusion notes
- rating rationale

## Registry Principles

The registry must be:
- stable: IDs do not change randomly
- traceable: evidence links back to scene IDs
- deduplicated: aliases are grouped
- state-aware: visual states are preserved
- production-oriented: `priority_level`, `production_handling`, `needs_main_image`, `task_id`, and `task_type` are explicit
- audit-ready: unresolved conflicts are visible
- identity-anchored for recurring/key characters: the approved face/casting identity is stored once and reused by state tasks
- mappable: every used state can be joined back to episode/scene usage rows

## ID Rules

Use stable lowercase ASCII IDs when possible:
- `char_luna_original_banquet_dress`
- `scene_wildo_studio_original_day_work`
- `prop_matthew_camera_original_used`

For Chinese names, use readable pinyin or a stable transliteration if available. If not, use a numbered ID plus display name:
- `char_001`
- `scene_003`
- `prop_012`

Never use unstable IDs based only on list order if the project is long. If order IDs are necessary, keep a mapping table.

## Registry Fields

Every registry item must include:
- `asset_id`
- `base_asset_id`
- `state_asset_id`
- `asset_type`
- `display_name`
- `state_name`
- `full_state_display_name`
- `aliases`
- `priority`
- `priority_level`: `S`, `A`, `B`, `C`, or `D`
- `production_handling`: `main_task`, `deferred_task`, `record_only_mapping`, `exclude_with_reason`, or `manual_review`
- `handling_reason`
- `needs_main_image`
- `manual_override`
- `first_seen`
- `episode_list`
- `scene_list`
- `first_needed_episode`
- `first_needed_scene`
- `used_in_episodes`
- `used_in_scenes`
- `state_trigger_scene_ids`
- `episode_usage_refs`
- `story_function`
- `visual_function`
- `visual_identity`
- `material_quality_focus`
- `script_evidence`
- `rating_reason`
- `uncertainties`
- `conflicts`
- `review_focus`
- `status`

Every production-relevant state item must also include Global Asset State Task Map fields:
- `task_id`
- `task_type`: `text_to_image`, `image_text_edit`, `reuse_existing`, `blocked`, or `manual_review`
- `generation_source`: `new_prompt`, `identity_anchor`, `first_generated_reference`, `existing_state`, `none`, or `manual`
- `reference_task_id`
- `reference_image`
- `reuse_from_task_id`
- `prompt`
- `negative_prompt`
- `edit_instruction`
- `delivery_status`: `ready`, `pending_reference`, `blocked`, `manual_review`, or `record_only`

For character base assets that appear in the Main Character Master List, also include:
- `identity_anchor_task_id`
- `identity_anchor_prompt`
- `identity_negative_prompt`
- `identity_reference_image`: approved image path/URL/task reference, `pending`, or `blocked`
- `identity_lock_status`: `pending`, `generated`, `approved`, `manual_review`, or `blocked`
- `stable_face_identity`
- `variable_state_axes`

For character state assets attached to those base assets, also include:
- `generation_mode`: usually `image_edit_from_identity_anchor`, `image_edit_identity_sensitive_state`, or `reuse_existing`
- `identity_anchor_task_id`
- `identity_reference_image`
- `locked_identity_prompt`
- `state_delta_prompt`
- `edit_instruction`
- `identity_change_allowed`
- `identity_change_reason`

For non-key character state assets that already have a first generated character image, use that first generated image as `reference_image` and the first generated task as `reference_task_id` when later visible states require image editing.

## Global Asset State Task Map

The Global Asset State Task Map is the production source of truth. It is built from registry state items after dedupe, state grouping, and rating.

One `state_asset_id` should normally have one `task_id`.

Completeness guard:
- Every production-relevant or episode-mapped character, scene, and prop state must have a row here, even when it is blocked, manual-review, pending-reference, record-only, or reused.
- `blocked`, `manual_review`, `pending_reference`, and `blocked_identity_anchor_required` are delivery/status values, not deletion reasons.
- If a state has episode usage but does not need prompt generation, keep it as `record_only` or `reuse_existing` with a stable `state_asset_id`, `task_id`, and join path.
- Do not shrink this map to match the compact human review table.
- Do not infer deletion from `priority_level`. Use `production_handling` to decide the destination.
- `priority_level: S` must be `production_handling: main_task`.
- `priority_level: A` defaults to `main_task`; if downgraded, preserve the downgrade reason in `handling_reason`.
- `priority_level: B` must be `deferred_task`, `record_only_mapping`, or `exclude_with_reason` with a reason.
- `priority_level: C` may be `record_only_mapping` or `exclude_with_reason`; if physically present and useful for episode review, keep it mapped.
- `priority_level: D` usually remains in the exclusion log as `exclude_with_reason`.

Allowed `task_type` values:
- `text_to_image`: create the first image for a character, scene, or prop state from text.
- `image_text_edit`: create a new character state from an approved identity/reference image plus state delta text.
- `reuse_existing`: do not generate a new image; reuse an existing task/image for this state or episode usage.
- `blocked`: cannot proceed because required evidence or reference image is missing.
- `manual_review`: evidence, identity, state split, or production choice needs human confirmation.

Task type rules:
- Use `text_to_image` for identity anchors, first non-key character images, first scene states, and first prop states that need main images.
- Use `image_text_edit` for later character states that need visible changes from an existing character image.
- Use `reuse_existing` when a later episode uses a visually identical state.
- Use `blocked` when the task requires a reference image that is not approved or available.
- Use `manual_review` when evidence conflicts or the state boundary is uncertain.

When `blocked` is used, still preserve the state row, blocking reason, evidence, first-needed episode/scene, and all episode usage rows. Do not convert a blocked state into an omitted state.

The map must preserve the join path:
- `state_asset_id` joins the global task table to episode usage rows.
- `task_id` identifies the production task.
- `reference_task_id` identifies the anchor or first generated image used by edit tasks.
- `reuse_from_task_id` identifies the already generated task/image used by reuse rows.

Recommended `status` values:
- `ready_for_prompt`
- `record_only`
- `待人工确认`
- `信息冲突`
- `deferred`

Recommended mapping from `production_handling`:
- `main_task` -> create a global task row with `text_to_image`, `image_text_edit`, `reuse_existing`, `blocked`, or `manual_review`.
- `deferred_task` -> create a global task row with `delivery_status: deferred` or `manual_review`, keeping evidence and mapping.
- `record_only_mapping` -> create a registry row and episode mapping row; use a stable `task_id` when the episode table must join to the global table.
- `exclude_with_reason` -> keep only in the exclusion log unless the user asks to inspect excluded candidates.
- `manual_review` -> create a visible row with the decision needed.

## Alias Merge Rules

Merge when references clearly point to the same entity:
- full name and first name
- title and name
- nickname and formal name
- role label and revealed identity
- translated or romanized variants
- typo/OCR variants when evidence supports it

Do not merge when:
- two people share a title
- a role changes holder
- two locations have similar names but different geography
- props are same type but different ownership or story function

If unsure, keep separate and mark `possible_duplicate`.

## Base Asset vs State Asset

Base asset stores identity:
- `display_name`
- aliases
- broad story function
- recurring evidence
- for key characters: locked face/casting identity, identity anchor prompt, and approved reference image

State asset stores production target:
- `state_name`
- visual state
- prompt target
- state evidence
- main image need
- for key characters: state delta and image-edit instructions, not a new independent face description

Main image prompts should usually target state assets, not vague base assets.

For recurring/key characters, state assets must inherit the base character identity anchor. Do not allow later episode states to create independent text-to-image prompts unless they are explicitly marked `text_to_image_manual_exception` and routed to manual review.

For non-key characters, if the same character appears again with a new valid visible state after a first image exists, the later state should use `image_text_edit` from the first generated reference image rather than a new independent `text_to_image` task.

## Scene Merge Rules

Merge scenes when:
- same location with same visual identity
- different headings refer to the same space
- repeated use of same set with no meaningful state change

Keep separate states when:
- day/night or lighting changes identity
- event setup changes dressing
- destruction/aftermath changes appearance
- public/private function changes layout or mood

## Prop Merge Rules

Merge props when:
- same object appears across scenes
- different names refer to same owned object
- condition is unchanged or minor

Keep separate states when:
- damage, blood, contamination, opening, burning, or modification changes visual target
- ownership transfer changes marks, packaging, or condition
- same type appears as multiple distinct story props

## Conflict Handling

Do not resolve major contradictions silently.

Use `conflicts` for:
- inconsistent age
- conflicting costume/condition
- impossible location continuity
- duplicate names for different characters
- prop condition mismatch
- scene identity ambiguity

Mark the item `信息冲突` if conflict affects prompt generation.

## What This Layer May Change

Allowed:
- assign stable IDs
- merge duplicates
- preserve aliases
- attach state assets to base assets
- mark conflicts and uncertainties
- set registry status

Not allowed:
- creating new major assets without sending them back to Extraction
- creating new states without sending them back to State Variant
- changing ratings without sending back to Priority Rating
- writing prompts

## Output

Produce:
- internal global asset-state registry
- Global Asset State Task Map
- alias map
- base-to-state map
- state-to-episode usage map
- unresolved conflicts list
- record-only asset list

Do not deliver the internal registry as a separate final file by default. Its selected fields should feed the final `main-image-production-table.md`.

## Acceptance Checklist

Before leaving this layer:
- no loose production asset exists outside registry
- every production-relevant state has one stable `task_id`
- every production-relevant state has an explicit `task_type`
- every retained state has `priority_level`, `production_handling`, and `handling_reason`
- every episode-mapped state is retained even if it is B/C, blocked, manual-review, pending-reference, record-only, or reused
- every used state preserves episode/scene mapping data
- every S item has `production_handling: main_task`
- every A item is `main_task` unless a downgrade reason is explicit
- aliases are preserved
- state assets point to base assets
- recurring/key character base assets have identity anchor fields
- recurring/key character state assets inherit `identity_anchor_task_id` and `identity_reference_image`, or are blocked/manual-review
- non-key character later states reference the first generated character image when available
- conflicts are visible, not hidden
