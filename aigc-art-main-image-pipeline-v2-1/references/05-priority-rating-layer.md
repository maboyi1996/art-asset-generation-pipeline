# 05 Priority Rating Layer

This layer decides production priority. Rating is a production decision, not a taste judgment.

## Goal

Assign two separate decisions to every base or state asset:
- `priority_level`: `S`, `A`, `B`, `C`, or `D`
- `production_handling`: `main_task`, `deferred_task`, `record_only_mapping`, `exclude_with_reason`, or `manual_review`

Do not mix importance, generation need, and episode mapping. `priority_level` says how important the asset is. `production_handling` says what happens to it. Episode usage mapping says where it appears.

## Inputs

Use:
- candidate assets from Asset Extraction
- state assets from State Variant
- scene coverage
- source evidence
- story function notes
- visual function notes

Do not rate from memory or because an asset “feels important”.

## Priority Level Meaning

`S` means project-level core asset and must produce a main image task.

Use for:
- core protagonist
- core love interest
- core antagonist
- recurring identity-defining location
- iconic world/faction location
- plot-turning prop
- state variant that is visually central to an iconic or decisive scene

`A` means key supporting asset or important antagonist/support function. It defaults to a main image task unless a downgrade reason is explicit.

Use for:
- important supporting character
- recurring supporting location
- relationship-defining location
- important prop used in conflict, reveal, intimacy, or threat
- state variant that appears in an important sequence and changes visual identity

`B` means locally important asset. It is often deferred or record-only, but it must not silently disappear.

Use for:
- low-frequency but visually specific character
- one-off location with strong design need
- prop with clear visual identity but limited plot weight
- useful reference asset if schedule allows

`C` means lightweight functional asset. It usually does not get a main image, but physical appearances that affect episode understanding must remain in episode mapping or be excluded with a reason.

Use for:
- generic background characters
- generic rooms or roads
- ordinary props with no plot function
- assets covered by a higher-level scene design
- mentioned-only items with no production need

`D` means pure background or mentioned-only. It defaults to exclusion with a logged reason.

Use for:
- no physical appearance
- crowd/passersby/generic group labels
- offscreen-only or mentioned-only figures with no visual production need
- generic objects or locations with no continuity, plot, or review function

## Production Handling

Allowed `production_handling` values:
- `main_task`: create or edit a global main-image task.
- `deferred_task`: keep a global task row for later scheduling; do not drop it.
- `record_only_mapping`: keep registry and episode mapping, but do not create a prompt now.
- `exclude_with_reason`: exclude from registry/task table only with an explicit exclusion reason.
- `manual_review`: keep visible for human decision when rating, evidence, identity, or handling is uncertain.

Default handling by priority:

| priority_level | default production_handling |
|---|---|
| S | `main_task` |
| A | `main_task`, unless a downgrade reason is explicit |
| B | `deferred_task` or `record_only_mapping` |
| C | `record_only_mapping` or `exclude_with_reason` |
| D | `exclude_with_reason` |

Hard handling rules:
- S must be `main_task`.
- A defaults to `main_task`; if not, write the downgrade reason.
- B does not mean deletion. B must have a destination: `deferred_task`, `record_only_mapping`, or `exclude_with_reason` with a reason.
- C defaults to no main image, but if the asset physically appears and affects scene understanding, keep it in episode mapping. If it is not mapped, explain why in the exclusion log.
- D defaults to `exclude_with_reason`; do not promote D unless source evidence creates a visible production need.

## Rating Dimensions

Evaluate each asset across these dimensions:
- story centrality
- recurrence
- visual specificity
- state uniqueness
- continuity risk
- art production dependency
- audience recognition
- plot-turn function
- character/world identity value
- material/design complexity

Rating should reflect the combined production need, not a single dimension.

## Character Rating Rules

Rate `S` when:
- the character leads the story
- the character needs stable face identity
- later images depend on this identity
- state variants define key scenes
- the character is a core protagonist, core love interest, main antagonist, final antagonist, or plot-spanning identity that must keep a stable face

Rate `A` when:
- recurring and relationship-relevant
- strong power/status function
- visually distinct from leads
- likely appears across multiple scenes
- the character repeatedly drives conflict, death, truth reveal, marriage, trial, revenge, or a strong tie to an S-level character

Rate `B` when:
- visually specific but low frequency
- appears in a meaningful one-off scene
- supports a world/faction but does not drive story
- the character has a name or stable role label but mainly serves one story segment

Rate `C` when:
- nameless or generic
- no visual continuity need
- exists only to fill background
- the character is a light scene-function role with one or two appearances, such as a normal physician, messenger guard, or temporary maid

Rate `D` when:
- the figure has no physical appearance
- the figure is only mentioned
- the figure is pure crowd/background with no visual production need

## Scene Rating Rules

Rate `S` when:
- it is a recurring core world location
- it visually defines class, institution, faction, or family
- it hosts major story turns
- later scene angles depend on a strong main reference

Rate `A` when:
- it recurs or carries important relationship/power shifts
- it has specific material, class, or mood requirements
- art production needs a reference to keep consistency

Rate `B` when:
- one-off but visually specific
- supports a set piece
- has unique material or atmosphere

Rate `C` when:
- generic transit or background space
- no special design need
- fully covered inside another scene asset

## Prop Rating Rules

Rate `S` when:
- the prop drives a major plot turn
- the prop is iconic to a character
- the prop appears repeatedly and must stay consistent
- the prop condition/state is story-critical

Rate `A` when:
- it affects relationship, conflict, threat, or reveal
- it has distinctive material/status/ownership
- it may need close-up reference

Rate `B` when:
- visually specific but low impact
- useful for art continuity but not central

Rate `C` when:
- generic or replaceable
- no close-up or identity need
- just environmental dressing

## State Variant Rating

Rate state variants separately from base assets.

Example:
- `Luna--原始（日常素颜）状态`: S
- `Luna--原始（晚宴礼服）状态`: S or A
- `Luna--原始（雨中湿发）状态`: A if plot-important, B if brief

A base asset can be S while a minor state is B.

A B base asset can have an A state if that state appears in a key scene.

## Needs Main Image Compatibility

`needs_main_image` may be kept as a derived compatibility field, but it must not replace `priority_level` or `production_handling`.

Default derived values:
- `production_handling: main_task` -> `needs_main_image: true`
- `production_handling: deferred_task` -> `needs_main_image: scope-dependent / deferred`
- `production_handling: record_only_mapping` -> `needs_main_image: false`
- `production_handling: exclude_with_reason` -> `needs_main_image: false`
- `production_handling: manual_review` -> `needs_main_image: pending`

Episode-local repeated minor characters or props do not automatically require a main image. Rate them by story and visual function, usually `B` or `C`, but they must still be carried into `episode_asset_usage` when they appear more than once in the same episode.

`needs_main_image` controls whether a global asset-state task needs a new image prompt or edit instruction. It does not control whether the asset/state appears in episode usage mapping.

If a B asset is not generated, record its `production_handling` and reason.

B/C handling must not become omission. A B/C asset or state that is production-relevant, reused, continuity-relevant, or episode-mapped must still carry forward into the registry and episode usage mapping as `record_only`, `reuse_existing`, `manual_review`, or another explicit non-prompt status. Only exclude it completely when it is truly generic/background/mentioned-only and the exclusion reason is logged.

If a C asset is generated because the user requests it, keep `priority_level: C`, set `production_handling: main_task`, set `needs_main_image: true`, and set `manual_override: true`.

## Rationale Requirements

Every rating must include:
- `priority_level`
- `production_handling`
- `handling_reason`
- `rating_reason`
- `evidence_scene_ids`
- `main_image_need_reason`
- `risk_if_not_generated`

Bad rationale:
- “重要”
- “好看”
- “出现过”

Good rationale:
- “E03-S014 首次出现并直接推动误会，后续 E08、E12 重复使用，且需要保持磨损和归属感一致。”

## What This Layer May Change

Allowed:
- assign or revise rating
- set `needs_main_image`
- mark borderline assets for human review
- downgrade generic assets
- upgrade state variants when story function justifies it

Not allowed:
- deleting assets without registry/audit trail
- merging aliases
- generating prompts
- inventing visual details to justify rating

## Output

Produce:
- rated asset list
- production handling table
- production priority table
- B/C exclusion or defer list
- record-only but mapped usage list
- D exclusion log
- manual review list for uncertain ratings

Pass rated assets to Asset Registry.

## Acceptance Checklist

Before leaving this layer:
- every asset/state has `priority_level: S/A/B/C/D`
- every asset/state has `production_handling`
- every S asset has `production_handling: main_task`
- every A asset is `main_task` unless a downgrade reason is explicit
- every rating has a reason and evidence
- B/C/D handling is explicit
- state variants are rated independently
- assets/states that do not need main images still keep mapping data when they are used in episodes
