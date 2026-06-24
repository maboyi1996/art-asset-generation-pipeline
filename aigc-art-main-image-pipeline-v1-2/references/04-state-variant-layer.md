# 04 State Variant Layer

This layer decides when one base asset must become multiple main-image state assets.

Always apply this layer together with [04-state-variant-standard.md](04-state-variant-standard.md). The standard is the source of truth for state boundaries, examples, naming, prompt scope, and audit checks.

## Goal

Prevent generic assets from erasing visual changes that matter to art consistency, while preventing over-splitting based on plot events, emotions, actions, props, or locations.

## Core Concept

A base asset is the stable identity:
- Character identity: the person.
- Scene identity: the location or spatial unit.
- Prop identity: the object.

A state asset is a visually distinct production target for the same identity. It must pass all three tests:
- Visible: the difference can be seen in a static main image.
- Stable: the difference is not only a momentary action, expression, or camera angle.
- Necessary: not splitting would mix visually different versions in downstream image generation.

For characters, splitting states does not mean generating a new independent person. Apply [07-character-identity-anchor-layer.md](07-character-identity-anchor-layer.md): the base character owns the locked face/casting identity, and each character state owns only the visible state delta.

## Mandatory State Boundaries

Character states are only visible character-body / appearance changes:
- age appearance
- face or grooming changes
- hair style or hair color
- makeup
- clothing category, silhouette, uniform, disguise, formal wear, workwear
- injury, illness, fatigue, dirt, blood, wet hair, pregnancy, visible body condition
- class/status presentation when it changes the character's visible styling
- flashback / past-period visible appearance, such as childhood, youth, older version, past workwear, past poverty, past elite styling

Character states are not:
- sitting near cash
- holding a contract, wine bowl, phone, tool, or other prop
- standing in a winery, living room, forum, field, office, or other location
- arguing, dividing money, signing, reporting, being humiliated, winning, losing
- a relationship with another character
- a temporary emotion with no stable appearance change

Scene states are only visible spatial-condition changes:
- day/night or lighting condition that changes spatial identity
- power outage, emergency lighting, sealed/closed status
- event setup, opening ceremony, forum stage, banquet layout
- before/after destruction, smashing, fire, flood, contamination, accident
- construction/build state
- crowd/empty or stocked/cleared state when it changes spatial function
- flashback / past-period spatial condition, such as past intact home, past operating shop, childhood school setting, present abandoned version

Prop states are only visible object-condition changes:
- new/old, intact/broken, clean/dirty, wet/burned/moldy/bloodied
- sealed/opened when inner structure or content matters
- label, stamp, signature, fingerprint, seal, liquid level, visible content changes
- altered, hidden, weaponized, contaminated, or transferred with visible marks

## Naming Rules

Use these formats:
- Character: `角色名--外观（XX）状态`
- Scene: `场景名--初始（XX）状态`
- Prop: `道具名--初始（XX）状态`

`XX` must be short, concrete, and visually meaningful.

Good character examples:
- `陈有财--外观（中年乡镇老板）状态`
- `陈有财--外观（乱发浮肿醉态）状态`
- `陈北--外观（研发白大褂）状态`
- `陈北--外观（朴素正装）状态`

Bad character examples:
- `陈有财--外观（坐在120万现金中间）状态`
- `陈北--外观（拒绝五千万收购）状态`
- `钱万里--外观（论坛被打脸）状态`

Good scene examples:
- `陈北酒厂--初始（日间抽检）状态`
- `陈有财酒坊门口--初始（查封围堵）状态`
- `行业论坛现场--初始（公开对质）状态`

Good prop examples:
- `2万与60万现金--初始（分红对比）状态`
- `工业酒精瓶--初始（半瓶投毒）状态`
- `陈记酒坊转让协议--初始（血红指印）状态`

## State Grouping

Every state variant must point back to a base asset:
- `base_asset_id`
- `state_asset_id`
- `state_name`
- `state_basis_type`: `外观`, `空间`, or `物体条件`
- `state_trigger_scene_ids`
- `state_evidence`
- `evidence_strength`: `strong`, `medium`, `weak`, or `conflict`
- `visual_difference`
- `split_reason`
- `merge_or_exclusion_reason`
- `prompt_scope`
- `main_image_need`

For character states, also record:
- `identity_anchor_task_id`
- `identity_reference_image`: approved anchor image reference, `pending`, or `blocked`
- `generation_mode`: usually `image_edit_from_identity_anchor`
- `locked_identity_prompt`: reused from the Main Character Master List
- `state_delta_summary`: the state-specific visible changes only
- `identity_change_allowed`: `false` unless script evidence changes face/body identity
- `identity_change_reason`: required when identity change is allowed

If multiple scenes show the same visible state, group them under one state asset.

If states are narratively different but visually equivalent, do not split. Keep the plot distinction in evidence or review focus.

For every scene with `timeline_period` other than `present`, decide one of:
- split a character appearance state
- split a scene spatial state
- split a prop condition state
- intentionally merge with a current state and record why the visible state is equivalent

Do not leave flashback / past-period evidence only in notes.

If a state clue is weak or contradictory, mark `待人工确认` or `信息冲突`; do not hide the uncertainty in the prompt.

## Default State

Every S/A base asset should have one default state when appropriate:
- Character: `角色名--外观（日常/首次出场/职业外观/身份外观）状态`
- Scene: `场景名--初始（正常使用/日间生产/首次出现）状态`
- Prop: `道具名--初始（正常使用/完整/封存）状态`

Choose a script-specific visible label, not a generic label, whenever evidence allows it.

## Production Restraint

Not every recorded state clue becomes a main-image task.

State assets usually need main images when:
- the state changes visual identity
- it appears in a key scene
- it affects later art consistency
- it is S/A priority
- the user specifically asks for it

Minor B/C states can remain in the registry without prompt generation.

For S-level characters, recurring A-level characters, and user-requested key characters, the first production task should be the `text_to_image_identity_anchor` from the Main Character Master List. Later state assets should default to `image_edit_from_identity_anchor`. If the approved identity reference image does not exist yet, block or manual-review the state task instead of producing a separate text-to-image prompt.

## What This Layer May Change

Allowed:
- split base assets into valid state assets
- merge visually equivalent state clues
- reject invalid state splits and move the information to evidence, scene assets, or prop assets
- mark uncertain state variants
- add missing state evidence from scene coverage

Not allowed:
- writing final image prompts
- detailed visual design beyond evidence
- assigning final S/A/B/C without the Priority layer
- deleting base assets silently
- putting props or scenes into character state names

## Output

Produce:
- base-to-state map
- state asset list
- rejected / merged state notes
- state omission risks
- state evidence table

Pass valid state assets to Priority Rating.

## Acceptance Checklist

Before leaving this layer:
- [04-state-variant-standard.md](04-state-variant-standard.md) has been applied.
- [07-character-identity-anchor-layer.md](07-character-identity-anchor-layer.md) has been applied to recurring/key characters.
- all recorded state clues have been considered.
- every non-present `timeline_period` scene has been reviewed for character, scene, and prop state variants.
- flashback / past-period variants are split or intentionally merged with visible-equivalence reasons.
- character states are based only on visible appearance changes.
- prop, location, action, emotion, and plot-event clues are not used as character states.
- scene states are based only on visible spatial changes.
- prop states are based only on visible object-condition changes.
- visually meaningful state changes are split or intentionally merged with a reason.
- every state asset has scene evidence or `待人工确认`.
- every recurring/key character state points to an identity anchor or is blocked/manual-review.
- no recurring/key character state is treated as an independent text-to-image character unless explicitly marked `text_to_image_manual_exception`.
- naming format is consistent.
