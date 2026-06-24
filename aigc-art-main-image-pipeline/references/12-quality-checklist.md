# 12 Quality Checklist

This layer is the final acceptance gate.

## Goal

Catch failures before the output reaches art staff or an image API:
- plot drift
- missed states
- unsupported visual invention
- weak material prompts
- generic AI image drift
- invalid output structure

## Checklist Order

Run checks in this order:
1. Source traceability
2. Scene coverage
3. Asset registry
4. State variants
5. Rating
6. Audit resolution
7. PDF template compliance
8. Prompt content
9. Material quality
10. Output contract

## 1. Source Traceability

Pass criteria:
- every S/A asset has script evidence
- every state asset has state evidence or `待人工确认`
- every prompt-critical visual detail has source support or conservative inference
- evidence includes scene IDs

Fail if:
- an S/A asset has no evidence
- prompt contains unsupported exact costume/material/status
- conflict is hidden

Return layer:
- Asset Registry
- relevant Main Image layer

## 2. Scene Coverage

Pass criteria:
- every parsed scene has coverage
- no-new-asset scenes are explicitly marked
- present and referenced characters are separated
- props and state clues are captured

Fail if:
- scenes were skipped
- state clues appear in source but not coverage
- important prop use is absent

Return layer:
- Scene Coverage

## 3. Asset Registry

Pass criteria:
- no loose production asset outside registry
- aliases are preserved
- base/state relationship is clear
- `needs_main_image` is explicit
- blocked assets are visible

Fail if:
- prompt exists for unregistered asset
- duplicate names create ambiguity
- state prompt has no base asset

Return layer:
- Asset Registry

## 4. State Variants

Pass criteria:
- visually meaningful costume, hair, body, scene, and prop changes are split or intentionally not split
- state names follow `角色名--外观（XX）状态`, `场景名--初始（XX）状态`, or `道具名--初始（XX）状态`
- character states are based only on visible character appearance changes
- scene states are based only on visible spatial-condition changes
- prop states are based only on visible object-condition changes
- props, locations, actions, emotions, relationships, and plot events are not used as character states
- emotional-only changes are not over-split

Fail if:
- wet hair/bathing/injury/costume change is missing as state
- scene day/night/event/destruction state is ignored
- prop broken/bloodied/opened state is ignored
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
- duplicate/conflict issues are visible
- downstream reruns were performed when needed

Fail if:
- audit found missing asset but prompt generation continued
- unresolved conflict affects prompt

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

Fail if:
- prompt could generate a generic attractive person/room/object
- state is missing from prompt
- scene prompt lacks layout
- prop prompt lacks exact object type
- character prompt includes cash, contracts, wine bowls, phones, vehicles, reports, furniture, or other props
- character prompt includes living room, winery, forum, office, field, or other scene/location descriptions
- character prompt includes Chinese scene IDs or Chinese plot sentences inside the image prompt
- character prompt stages a plot event instead of a clean portrait reference

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

## 10. Output Contract

Pass criteria:
- final output includes `main-image-production-table.md`
- final output includes `prompt-manifest.json`
- output is readable as a production table, not a pile of process files
- manifest is valid JSON and machine-readable
- major characters are summarized at the top
- episode sections list character, scene, and prop main image tasks
- human table and manifest contain the same ready generation tasks
- no final placeholders remain
- no API secrets are included

Fail if:
- final delivery exposes internal coverage/registry/audit files by default
- `prompt-manifest.json` is missing
- art staff must read full biographies to find prompts
- missing table rows for S/A generated tasks
- invalid JSON in manifest
- human table and manifest disagree
- secrets are embedded

Return layer:
- Output Contracts

## Final Pass Statement

At final delivery, include a compact quality statement:
- number of main image tasks by type and priority
- unresolved manual review count
- whether the human production table is ready for art review
- whether the machine manifest is valid and aligned

Do not claim zero risk for long scripts. Say what was checked and what remains for human review.
