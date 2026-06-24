# 03 Asset Extraction Layer

This layer extracts candidate characters, scenes, and props from scene coverage. It does not write final prompts.

## Goal

Build a candidate asset list that is broad enough to avoid missing important production assets, but disciplined enough not to turn every background detail into a main image task.

## Inputs

Use:
- scene coverage table
- parsed source evidence
- visual state clues
- timeline_period / flashback clues
- episode_asset_usage_candidates
- plot function notes

Do not extract assets directly from memory or global impressions. Start from coverage.

## Candidate Asset Types

Allowed asset classes:
- `character`
- `scene`
- `prop`

Do not create asset classes such as mood, theme, relationship, color, or camera. Those may become fields inside assets, not assets themselves.

## Character Candidate Rules

Extract a character candidate when one or more applies:
- named character appears physically
- character has recurring appearances
- character has important dialogue or action
- character drives a conflict, relationship, reveal, or emotional turn
- character has specific appearance, costume, class, profession, or body-state description
- character must be visually consistent across scenes
- character appears more than once within the same episode, even if minor, unnamed, or low-importance in the full project
- character is visually represented through portrait, corpse, reflection, memory image, photograph, or screen
- character appears in a flashback, childhood, youth, past-period, future, dream, or memory scene with visibly different age, clothing, hair, body condition, or class/status presentation

Usually do not extract:
- unnamed passerby with only one pass-by appearance
- generic crowd members
- one-line servants/guards unless visually distinctive, plot-relevant, or repeated within the same episode
- purely mentioned offscreen figures with no visual production need

Do not exclude a minor or generic character when the same role/person appears multiple times within one episode. Treat it as an episode-local consistency asset and carry it into `episode_asset_usage_candidates`.

Mark as `candidate_only` when uncertain.

## Scene Candidate Rules

Extract a scene candidate when one or more applies:
- location appears repeatedly
- location introduces a world, class, institution, family, faction, or power structure
- location hosts a major plot turn
- location needs visual consistency
- location has specific architecture, dressing, light, material, or atmosphere
- location contrasts with a character
- location will likely need a main reference for later art production
- location appears in a flashback, past period, memory, childhood, or future timeline with different era markers, layout, decor, damage, crowd condition, or material state

Usually do not extract:
- generic roads, corridors, doorways, empty rooms, or outdoor background unless story-specific
- transient locations with no distinct visual identity
- locations mentioned only in dialogue

## Prop Candidate Rules

Extract a prop candidate when one or more applies:
- used directly in action
- exchanged, hidden, stolen, broken, opened, read, worn, pointed at, photographed, or weaponized
- triggers plot movement, misunderstanding, threat, intimacy, memory, or reveal
- belongs strongly to a character or world
- has specific material, condition, class, age, or symbolic value
- must remain visually consistent
- appears more than once within the same episode and needs visual continuity, even if it is not important to the full project

Usually do not extract:
- generic cups, bowls, chairs, curtains, plants, books, phones, bags, or furniture unless story-specific or repeated within the same episode
- environmental dressing already covered by scene design
- common items with no narrative function

For props, a fully one-shot pass-by object can be excluded when it has no plot function, no close-up need, and no continuity need. Do not use this exclusion for props that recur within the same episode.

## Evidence Requirements

Every candidate must include:
- `evidence_scene_id`
- short source quote or paraphrased evidence
- evidence type:
  - appearance
  - action
  - dialogue
  - relation
  - location
  - prop use
  - state clue

If evidence is implied but not explicit, mark `inferred` and explain why.

## Candidate Fields

Each candidate should include:
- `candidate_id`
- `asset_type`
- `raw_name`
- `normalized_name`
- `possible_aliases`
- `source_scene_ids`
- `source_episode_ids`
- `first_seen`
- `evidence`
- `story_function`
- `visual_function`
- `state_clues`
- `episode_usage_refs`: the episode/scene usage rows carried forward from scene coverage
- `possible_priority`
- `extraction_confidence`
- `notes`

## Boundary Between Asset And State

This layer extracts the base entity. It may record state clues but should not decide final state assets.

Example:
- Base character candidate: `Luna`
- State clues: `晚宴礼服`, `洗澡后湿发`, `受伤虚弱`
- Final state assets are created in State Variant layer.

For timeline variants:
- Base character candidate: `陈北`
- State clues: `childhood`, `youth`, `present-day plain suit`, `older exhausted`
- Base scene candidate: `陈家老屋`
- State clues: `past intact family home`, `present abandoned damaged home`

Do not discard flashback candidates merely because the present-day base asset already exists. Preserve the timeline clue for State Variant and Audit.

## Exclusion Logging

For borderline items, log why they are excluded:
- `generic_background`
- `covered_by_scene_asset`
- `mentioned_only`
- `no_visual_identity`
- `no_plot_function`
- `duplicate_candidate`

This helps Audit understand that the item was considered.

## What This Layer May Change

Allowed:
- add missing candidates from coverage
- remove obvious non-assets with reason
- split candidate classes correctly
- attach evidence

Not allowed:
- final rating
- final prompt writing
- PDF analysis template writing
- detailed visual invention not supported by evidence

## Output

Produce three candidate lists:
- character candidates
- scene candidates
- prop candidates

Also produce:
- episode asset usage candidate list by episode
- candidate-to-episode-usage crosswalk
- flashback / non-present timeline candidate list

Pass candidates and exclusions to State Variant.

## Acceptance Checklist

Before leaving this layer:
- all scene coverage rows have been considered
- all `episode_asset_usage_candidates` have been carried forward or explicitly excluded
- every extracted candidate keeps its episode/scene usage references for Asset Registry mapping
- all flashback / past-period character and scene candidates have been carried forward or explicitly excluded
- every candidate has evidence
- uncertain candidates are flagged, not silently deleted
- ordinary background details are controlled
- state clues are preserved for the next layer
