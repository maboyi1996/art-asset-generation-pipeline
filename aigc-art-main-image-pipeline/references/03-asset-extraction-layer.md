# 03 Asset Extraction Layer

This layer extracts candidate characters, scenes, and props from scene coverage. It does not write final prompts.

## Goal

Build a candidate asset list that is broad enough to avoid missing important production assets, but disciplined enough not to turn every background detail into a main image task.

## Inputs

Use:
- scene coverage table
- parsed source evidence
- visual state clues
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
- character is visually represented through portrait, corpse, reflection, memory image, photograph, or screen

Usually do not extract:
- unnamed passerby
- generic crowd members
- one-line servants/guards unless visually distinctive or plot-relevant
- purely mentioned offscreen figures with no visual production need

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

Usually do not extract:
- generic cups, bowls, chairs, curtains, plants, books, phones, bags, or furniture unless story-specific
- environmental dressing already covered by scene design
- common items with no narrative function

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
- `first_seen`
- `evidence`
- `story_function`
- `visual_function`
- `state_clues`
- `possible_priority`
- `extraction_confidence`
- `notes`

## Boundary Between Asset And State

This layer extracts the base entity. It may record state clues but should not decide final state assets.

Example:
- Base character candidate: `Luna`
- State clues: `晚宴礼服`, `洗澡后湿发`, `受伤虚弱`
- Final state assets are created in State Variant layer.

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

Pass candidates and exclusions to State Variant.

## Acceptance Checklist

Before leaving this layer:
- all scene coverage rows have been considered
- every candidate has evidence
- uncertain candidates are flagged, not silently deleted
- ordinary background details are controlled
- state clues are preserved for the next layer
