# 07 Audit Layer

This layer independently checks for missing assets, duplicates, conflicts, and state omissions.

It must also run the state-boundary audit from [04-state-variant-standard.md](04-state-variant-standard.md). If a state split violates that standard, return to State Variant before any prompt generation.

## Goal

Reduce the risk that a long script loses characters, scenes, props, or visually meaningful states.

Audit is not a rewrite pass. It is a verification pass.

## Inputs

Use:
- scene coverage table
- asset registry
- alias map
- base-to-state map
- timeline_period map
- episode asset usage candidate list
- exclusion notes
- parse uncertainty list

## Audit Permissions

Audit may:
- identify missing assets
- identify duplicate assets
- identify alias conflicts
- identify state omissions
- identify invalid state splits
- identify character state boundary violations
- identify missing flashback / past-period variants
- identify episode asset usage omissions
- identify prompt-scope leakage risks
- identify weak or missing evidence
- identify rating inconsistencies
- identify items needing human confirmation

Audit may not:
- rewrite biographies
- write prompts
- invent missing visual design
- silently merge conflicts
- delete assets without reporting

## Scene-By-Scene Coverage Audit

For every scene:
1. Read present characters.
2. Check whether each visually relevant character exists in registry or exclusion notes.
3. Read location.
4. Check whether the location exists as scene asset, state asset, or covered-by-higher-scene note.
5. Read props.
6. Check whether plot-relevant props exist in registry or exclusion notes.
7. Read state clues.
8. Check whether state variants exist or are intentionally not split.

Every scene should end in one of:
- `covered`
- `covered_with_notes`
- `missing_asset`
- `missing_state`
- `missing_timeline_variant`
- `missing_episode_usage`
- `manual_review_needed`

## Timeline / Flashback Audit

For every scene where `timeline_period` is not `present`:
1. Check whether every physically present character has an appropriate appearance state or an explicit visible-equivalence merge note.
2. Check whether the location has a past-period / flashback scene state or an explicit visible-equivalence merge note.
3. Check whether props have period-specific condition states when visible.
4. Check whether the final episode usage list includes the flashback states, not only the present-day base assets.

Flag `missing_timeline_variant` if:
- childhood / youth / older appearance is present but no character state exists
- past-period clothing, school uniform, workwear, poverty/wealth styling, illness, injury, or age change is present but no state exists
- a flashback location differs by era, decor, damage, crowd, business status, or material condition but no scene state exists
- the asset is only mentioned in notes and not carried into registry or usage outputs

Return all `missing_timeline_variant` findings to State Variant. If the base character/location is absent, return to Asset Extraction first.

## Missing Asset Criteria

Flag a missing character if:
- named and physically present but absent from registry/exclusion
- has dialogue/action and no registry/exclusion entry
- has appearance/costume/body-state description but no registry/exclusion entry
- is visually represented through portrait/body/reflection/screen and omitted

Flag a missing scene if:
- location carries plot function but absent
- recurring location omitted
- location state changes but no state entry
- location is only hidden inside notes but should be production asset

Flag a missing prop if:
- used in plot but absent
- causes reveal/conflict/intimacy/threat but absent
- condition matters but no state entry
- prop appears in scene coverage repeatedly but registry lacks it

## Duplicate Audit

Flag duplicates when:
- two registry items share aliases/evidence
- same scene/location appears under different names
- same prop appears as type name and story name
- state asset duplicates default asset without visual difference

Audit should recommend merge candidates but not perform unsupported merges.

## State Omission Audit

Check all state clues:
- costume
- wetness/bathing/rain
- injury/blood/dirt/sickness
- disguise/status
- day/night/event/destruction
- prop damage/contamination/opened/used
- flashback / childhood / youth / past-period appearance
- past-period location condition

For each state clue, mark:
- `state_asset_exists`
- `state_in_prompt_only`
- `intentionally_not_split`
- `missing_state`
- `manual_review`

## Episode Usage Audit

For every episode, compare scene coverage against the final output's `episode_asset_usage`.

Flag `missing_episode_usage` if:
- a present character state is used in the episode but not listed
- a scene/location state is used in the episode but not listed
- a plot-relevant prop state is used in the episode but not listed
- a reused asset is omitted because it was generated in an earlier episode

This audit is separate from generation-task audit. Reused assets do not need duplicate prompts, but they must still appear in the episode usage list.

## State Boundary Audit

Run this audit after the state omission audit and before prompt generation.

Flag an invalid character state if the state name, state evidence, or planned prompt is based on:
- a prop, e.g. cash, contract, wine bowl, phone, testing report, vehicle
- a location, e.g. living room, winery, forum, office, field
- an action, e.g. sitting, holding, signing, kneeling, shouting
- a plot event, e.g. dividing money, rejecting acquisition, being exposed, winning
- a relationship or conflict with another character
- a temporary emotion with no stable appearance change

For every invalid character state:
- move prop information to a prop asset or prop evidence.
- move location information to a scene asset or scene evidence.
- move plot/event information to evidence or review focus.
- rename the character state using visible appearance only.

Example:
- Wrong: `陈有财--外观（坐在120万现金中间）状态`
- Correct character state: `陈有财--外观（中年乡镇老板）状态`
- Separate assets/evidence: `2万与60万现金--初始（分红对比）状态`, `客厅分钱场景--初始（现金堆放）状态`

Flag an invalid scene state if it is only dialogue, emotion, character conflict, camera angle, or temporary blocking without visible spatial-condition change.

Flag an invalid prop state if it is only the holder, placement, camera angle, symbolic meaning, or plot reaction without visible object-condition change.

For character prompt scope, flag leakage if the final image prompt contains:
- Chinese plot evidence or scene IDs inside the English prompt text
- props or prop interactions
- scene/location description
- multiple characters
- action-scene staging

Character prompt leakage must return to the Character Main Image layer. If the leakage comes from a bad state split, return to State Variant first.

## Rating Audit

Flag rating issues:
- S/A asset with `needs_main_image: false`
- C asset with major plot function
- repeated B asset that should be A
- key state under-rated
- generic background item over-rated

Rating audit recommendations must return to Priority Rating.

## Evidence Audit

Flag weak evidence:
- no scene ID
- only inferred with no explanation
- visual design unsupported by script
- prompt likely depends on invented details
- conflicting source evidence

Prompt generation must not proceed for S/A items with unresolved evidence gaps unless marked `待人工确认`.

## Audit Report Format

Use this structure:

```markdown
# Main Image Asset Audit Report

## 1. Coverage Summary
- Total scenes checked:
- Covered:
- Missing asset:
- Missing state:
- Manual review:

## 2. Suspected Missing Assets
| scene_id | asset_type | raw_name | reason | required_return_layer |

## 3. Suspected Duplicate Assets
| asset_id_a | asset_id_b | reason | recommendation |

## 4. State Omission Risks
| base_asset | state_clue | scene_id | recommendation |

## 5. Timeline / Flashback Issues
| scene_id | timeline_period | missing_variant | recommendation |

## 6. Episode Usage Omissions
| episode_id | scene_id | asset_or_state | issue | recommendation |

## 7. State Boundary Issues
| asset_id | invalid_state_or_prompt_scope | issue | required_return_layer |

## 8. Evidence / Conflict Issues
| asset_id | issue | affected_fields | recommendation |

## 9. Rating Issues
| asset_id | current_rating | suggested_review | reason |

## 10. Manual Confirmation List
| item | reason | blocking_prompt_generation |
```

## Return Rules

If missing asset:
- return to Asset Extraction

If missing state:
- return to State Variant

If missing timeline variant:
- return to Asset Extraction if the base asset is missing
- otherwise return to State Variant

If invalid state split:
- return to State Variant

If missing episode asset usage:
- return to Scene Coverage or Output Contracts, depending on whether the omission is in source coverage or final output mapping

If character prompt includes props, scenes, Chinese plot evidence, or action-scene staging:
- return to Character Main Image layer, or State Variant first if the prompt leakage comes from an invalid state name

If rating issue:
- return to Priority Rating

If alias/duplicate issue:
- return to Asset Registry

If prompt evidence is weak:
- return to Asset Registry or Main Image layer depending on source of issue

## Output

Produce:
- internal audit notes
- audit status per scene
- return-layer action list

Do not deliver a separate audit report by default. Compress unresolved audit issues into the `Manual Review / Blocked Items` section of `main-image-production-table.md`.

## Acceptance Checklist

Before leaving this layer:
- every scene has audit status
- missing assets are explicitly resolved or queued
- state omissions are explicitly resolved or queued
- flashback / past-period variant omissions are resolved or queued
- episode asset usage omissions are resolved or queued
- invalid state splits are explicitly corrected, merged, or queued
- character prompt-scope leakage has been checked
- no S/A prompt proceeds with hidden evidence gaps
- rerun requirements are documented
