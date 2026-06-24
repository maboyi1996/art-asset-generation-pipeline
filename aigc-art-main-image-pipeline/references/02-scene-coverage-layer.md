# 02 Scene Coverage Layer

This is the anti-omission backbone. Every later asset must be traceable to scene coverage.

## Goal

Create a scene-by-scene visual coverage index that records what art-relevant things appear in every scene, before deciding final assets.

This layer answers:
- Who appears?
- Where does it happen?
- What objects matter?
- What visual states change?
- What must the art team understand about this scene?

## Inputs

Use parsed scene records from Intake:
- scene IDs
- raw headings
- action text
- dialogue text
- prop mentions
- visual state clues
- parse notes

## Scene Coverage Fields

Every scene record must include:
- `scene_id`
- `episode_id`
- `source_heading`
- `location`
- `time_or_lighting`
- `present_characters`
- `referenced_characters`
- `character_state_clues`
- `scene_state_clues`
- `props_present`
- `props_referenced`
- `relationship_or_power_shift`
- `plot_function`
- `visual_function`
- `material_or_texture_mentions`
- `main_image_asset_candidates`
- `no_new_asset_reason`
- `coverage_confidence`
- `coverage_notes`

## Character Coverage Rules

Record a character if:
- they appear physically
- they speak
- they perform an action
- others react to them visually
- they are described in appearance, clothing, injury, or posture
- they are not present but their portrait/photograph/body/trace appears

Separate `present_characters` from `referenced_characters`.

Do not convert every mentioned name into a production asset yet. That belongs to Asset Extraction.

## Scene Coverage Rules

Record the scene/location if:
- it has a heading
- it is implied by action
- characters move into or out of it
- it carries class, power, danger, intimacy, or plot function
- it changes state in a visually meaningful way

If the exact location is unclear, keep the raw wording and mark `待人工确认`.

## Prop Coverage Rules

Record props if:
- a character uses, holds, hides, breaks, gives, finds, wears, reads, opens, steals, loses, photographs, points at, or reacts to it
- the prop triggers conflict, misunderstanding, memory, desire, threat, or reveal
- the prop helps identify class, profession, world, relationship, or secret
- the prop has visible condition such as blood, damage, dirt, age, shine, wear, or luxury finish

Do not record every generic chair, cup, wall, tree, or door unless it has story or visual function.

## State Coverage Rules

Record possible state changes but do not decide final state assets here.

Common state clues:
- costume: uniform, formalwear, sleepwear, bathrobe, armor, disguise, mourning clothes
- hair/makeup: wet hair, loose hair, ruined makeup, no makeup, heavy makeup
- body: injured, sick, sweating, dirty, crying, drugged, pregnant, aged, exhausted
- scene: day/night, ceremony, aftermath, destroyed, empty, crowded, rain, fire, luxury setup
- prop: new, worn, broken, bloodied, wet, burned, hidden, opened, locked, contaminated

## Visual Function Rules

For each scene, identify why it matters visually:
- introduces a key asset
- shows a state variant
- establishes a recurring location
- reveals class/worldview
- contains a plot-driving prop
- creates a power relationship
- only advances dialogue with no new visual asset

## No-New-Asset Rule

If a scene has no new or changed assets, still create a coverage row and set:
- `main_image_asset_candidates`: `none`
- `no_new_asset_reason`: e.g. “existing character and existing location, no visible state change”

This prevents silent gaps in long projects.

## What This Layer May Change

Allowed:
- clarify scene visual content
- add missed mentions from source text
- separate present vs referenced entities
- flag unclear location or state

Not allowed:
- final S/A/B/C rating
- final asset merging
- final state split
- prompt generation
- unsupported visual design

## Output

Produce an internal scene coverage table.

This table must be detailed enough that Audit can re-scan every scene against the asset registry.

Do not deliver this table as a separate final file by default. Its contents should be compressed into the final `main-image-production-table.md`.

## Acceptance Checklist

Before leaving this layer:
- every parsed scene has a coverage row
- scenes with no new assets are explicitly marked
- every visible state clue is recorded
- every plot-relevant prop mention is captured
- coverage confidence is marked for unclear scenes
