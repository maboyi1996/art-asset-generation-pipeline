# 02 Scene Coverage Layer

This is the anti-omission backbone. Every later asset must be traceable to scene coverage.

## Goal

Create a scene-by-scene visual coverage index that records what art-relevant things appear in every scene before deciding final assets.

This layer answers:
- What timeline period is this scene in?
- Who appears?
- Where does it happen?
- What objects matter?
- What visual states change?
- What assets does this episode use, even if no new main image is needed?
- What must the art team understand about this scene?

## Inputs

Use parsed scene records from Intake:
- scene IDs
- episode IDs
- raw headings
- action text
- dialogue text
- prop mentions
- visual state clues
- timeline clues
- parse notes

## Scene Coverage Fields

Every scene record must include:
- `scene_id`
- `episode_id`
- `timeline_period`: `present`, `flashback`, `past`, `childhood`, `future`, `dream`, `memory`, or a script-specific label
- `timeline_evidence`
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
- `episode_asset_usage_candidates`
- `no_new_asset_reason`
- `coverage_confidence`
- `coverage_notes`

## Timeline / Flashback Coverage Rules

Every scene must be assigned a timeline period before asset extraction.

Use `timeline_period: present` only when the scene belongs to the story's current timeline.

Use `flashback`, `past`, `childhood`, `memory`, or a script-specific label when the source indicates:
- 回忆, 闪回, 当年, 多年前, 小时候, 童年, 年轻时
- old photographs, archive footage, remembered scenes, dream-like recollection
- a character appears at a visibly different age or life stage
- the same location appears in an earlier era or visibly different period

For every non-present timeline scene, record:
- which characters physically appear in that period
- whether each character's age, clothing, hair, makeup, body condition, or class/status appearance differs from the present timeline
- whether the location's architecture, decor, damage, crowd level, era markers, or material condition differs from the present timeline
- whether props have period-specific condition or ownership marks

Do not treat flashback as a vague note. It must become auditable evidence for State Variant and Audit.

## Character Coverage Rules

Record a character if:
- they appear physically
- they speak
- they perform an action
- others react to them visually
- they are described in appearance, clothing, injury, or posture
- they appear through portrait, photograph, body, reflection, memory image, archive footage, or screen

Separate `present_characters` from `referenced_characters`.

For flashbacks, record the visible period-specific version, not only the present-day character name.

Do not convert every mentioned name into a production asset yet. That belongs to Asset Extraction.

## Scene Coverage Rules

Record the scene/location if:
- it has a heading
- it is implied by action
- characters move into or out of it
- it carries class, power, danger, intimacy, memory, or plot function
- it changes state in a visually meaningful way
- it appears in a flashback or past timeline with different spatial condition

If the exact location is unclear, keep the raw wording and mark `待人工确认`.

## Prop Coverage Rules

Record props if:
- a character uses, holds, hides, breaks, gives, finds, wears, reads, opens, steals, loses, photographs, points at, or reacts to it
- the prop triggers conflict, misunderstanding, memory, desire, threat, or reveal
- the prop helps identify class, profession, world, relationship, or secret
- the prop has visible condition such as blood, damage, dirt, age, shine, wear, or luxury finish

Do not record every generic chair, cup, wall, tree, or door unless it has story or visual function.

For character main-image purposes, record carried bags, phones, tools, contracts, cash, and similar objects as props or evidence only. Do not let them become part of the character portrait prompt.

## State Coverage Rules

Record possible state changes but do not decide final state assets here.

Common state clues:
- costume: uniform, formalwear, sleepwear, bathrobe, armor, disguise, mourning clothes
- hair/makeup: wet hair, loose hair, ruined makeup, no makeup, heavy makeup
- body: injured, sick, sweating, dirty, crying, drugged, pregnant, aged, exhausted
- scene: day/night, ceremony, aftermath, destroyed, empty, crowded, rain, fire, luxury setup
- prop: new, worn, broken, bloodied, wet, burned, hidden, opened, locked, contaminated
- timeline: childhood, youth, old age, past-period clothing, past-period location, flashback room condition

## Visual Function Rules

For each scene, identify why it matters visually:
- introduces a key asset
- uses an existing asset
- shows a state variant
- establishes a recurring location
- reveals class/worldview
- contains a plot-driving prop
- creates a power relationship
- only advances dialogue with no new visual asset

## Episode Asset Usage Rule

Every scene must record which asset states are used by the episode, even when no new main image should be generated.

`episode_asset_usage_candidates` must include:
- all present character states used in the scene
- the active scene/location state
- all plot-relevant prop states used in the scene
- reused assets, marked as reuse candidates when already generated earlier

This is not the same as `main_image_asset_candidates`.

Use:
- `main_image_asset_candidates` for new images or newly required state variants.
- `episode_asset_usage_candidates` for the full per-episode art usage map.

## No-New-Asset Rule

If a scene has no new or changed assets, still create a coverage row and set:
- `main_image_asset_candidates`: `none`
- `episode_asset_usage_candidates`: all reused character, scene, and prop states used in the scene
- `no_new_asset_reason`: e.g. `沿用已生成主图，无新外观/空间/物体状态`

This prevents silent gaps in long projects and lets the final output show each episode's actual asset usage.

## What This Layer May Change

Allowed:
- clarify scene visual content
- add missed mentions from source text
- separate present vs referenced entities
- flag unclear location, state, or timeline
- record usage of reused assets

Not allowed:
- final S/A/B/C rating
- final asset merging
- final state split
- prompt generation
- unsupported visual design

## Output

Produce an internal scene coverage table.

This table must be detailed enough that Audit can re-scan every scene against the asset registry and every episode against the usage list.

Do not deliver this table as a separate final file by default. Its contents should feed the final `main-image-production-table.md` and `prompt-manifest.json`.

## Acceptance Checklist

Before leaving this layer:
- every parsed scene has a coverage row
- every scene has `timeline_period` and `timeline_evidence`
- every flashback / past-period scene records character and scene state clues
- scenes with no new assets are explicitly marked
- scenes with no new assets still list `episode_asset_usage_candidates`
- every visible state clue is recorded
- every plot-relevant prop mention is captured
- coverage confidence is marked for unclear scenes
