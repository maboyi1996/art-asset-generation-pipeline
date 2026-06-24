# 05 Priority Rating Layer

This layer decides production priority. Rating is a production decision, not a taste judgment.

## Goal

Assign `S/A/B/C` and `needs_main_image` to every base or state asset so the project can be handled by one art owner without wasting image generation on low-value assets.

## Inputs

Use:
- candidate assets from Asset Extraction
- state assets from State Variant
- scene coverage
- source evidence
- story function notes
- visual function notes

Do not rate from memory or because an asset “feels important”.

## Rating Meaning

`S` means must produce main image.

Use for:
- core protagonist
- core love interest
- core antagonist
- recurring identity-defining location
- iconic world/faction location
- plot-turning prop
- state variant that is visually central to an iconic or decisive scene

`A` means should produce main image.

Use for:
- important supporting character
- recurring supporting location
- relationship-defining location
- important prop used in conflict, reveal, intimacy, or threat
- state variant that appears in an important sequence and changes visual identity

`B` means optional main image.

Use for:
- low-frequency but visually specific character
- one-off location with strong design need
- prop with clear visual identity but limited plot weight
- useful reference asset if schedule allows

`C` means record only, no main image by default.

Use for:
- generic background characters
- generic rooms or roads
- ordinary props with no plot function
- assets covered by a higher-level scene design
- mentioned-only items with no production need

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

Rate `A` when:
- recurring and relationship-relevant
- strong power/status function
- visually distinct from leads
- likely appears across multiple scenes

Rate `B` when:
- visually specific but low frequency
- appears in a meaningful one-off scene
- supports a world/faction but does not drive story

Rate `C` when:
- nameless or generic
- no visual continuity need
- exists only to fill background

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

## Needs Main Image

Default:
- S: `true`
- A: `true`
- B: `scope-dependent`
- C: `false`

Episode-local repeated minor characters or props do not automatically require a main image. Rate them by story and visual function, usually `B` or `C`, but they must still be carried into `episode_asset_usage` when they appear more than once in the same episode.

If a B asset is not generated, record why.

If a C asset is generated because the user requests it, keep rating C but set `needs_main_image: true` and `manual_override: true`.

## Rationale Requirements

Every rating must include:
- `rating`
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
- production priority table
- B/C exclusion or defer list
- manual review list for uncertain ratings

Pass rated assets to Asset Registry.

## Acceptance Checklist

Before leaving this layer:
- every asset/state has S/A/B/C
- every S/A asset has `needs_main_image: true`
- every rating has a reason and evidence
- B/C handling is explicit
- state variants are rated independently
