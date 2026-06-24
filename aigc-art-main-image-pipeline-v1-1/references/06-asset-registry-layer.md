# 06 Asset Registry Layer

This layer creates the single source of truth for all downstream analysis and prompts.

## Goal

Merge candidates into a global asset registry with stable IDs, aliases, states, evidence, ratings, and production flags.

No main image analysis or prompt should be generated from loose notes. It must come from the registry.

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
- production-oriented: `needs_main_image` is explicit
- audit-ready: unresolved conflicts are visible

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
- `asset_type`
- `display_name`
- `state_name`
- `full_state_display_name`
- `aliases`
- `priority`
- `needs_main_image`
- `manual_override`
- `first_seen`
- `episode_list`
- `scene_list`
- `state_trigger_scene_ids`
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

Recommended `status` values:
- `ready_for_prompt`
- `record_only`
- `待人工确认`
- `信息冲突`
- `deferred`

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

State asset stores production target:
- `state_name`
- visual state
- prompt target
- state evidence
- main image need

Main image prompts should usually target state assets, not vague base assets.

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
- internal asset registry
- alias map
- base-to-state map
- unresolved conflicts list
- record-only asset list

Do not deliver the internal registry as a separate final file by default. Its selected fields should feed the final `main-image-production-table.md` and optional `prompt-manifest.json`.

## Acceptance Checklist

Before leaving this layer:
- no loose production asset exists outside registry
- every S/A item has evidence and `needs_main_image: true`
- aliases are preserved
- state assets point to base assets
- conflicts are visible, not hidden
