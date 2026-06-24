# 07 Character Identity Anchor Layer

Use this guard for recurring and key characters. It prevents the same character from becoming different people across costume, injury, age, or episode states. For the writing standard of later image-edit state prompts, also apply [character-state-edit-prompt-guard.md](character-state-edit-prompt-guard.md).

## Core Rule

Character face identity and character state must be separated.

- `identity_anchor`: the stable face, age band, facial structure, gaze quality, class impression, and core casting identity of the character.
- `state_delta`: the visible change for one episode/state, such as wardrobe, grooming, hair condition, makeup, injury, illness, fatigue, dirt, blood, wetness, pregnancy, or age-state when supported by script evidence.

Do not regenerate a full independent text-to-image character prompt for every state of the same person. Similar text prompts are not enough to preserve the same face. Image models can sample a different face even when the prompt is copied exactly.

## Required Workflow

For S-level characters, recurring A-level characters, and user-requested key characters:

1. Build the `Key Character Identity Anchor Table` from the global character registry before any episode-by-episode character/scene/prop production table is written.
2. This table is built after global character extraction, deduplication, state detection, rating, and registry merge, not inside a specific episode.
3. For each key character, create one `text_to_image_identity_anchor` task or attach an already approved external reference image.
4. The anchor task produces or selects the approved `identity_reference_image`.
5. Lock the character's `identity_anchor_prompt` after approval.
6. Every later episode-level character state for that same base character must default to `image_edit_from_identity_anchor`.
7. State prompts must reuse the approved reference image and add only the state delta.

If no approved identity image exists yet, mark later state tasks as `blocked_identity_anchor_required` or `manual_review`, not as independent text-to-image tasks.

## Master List Requirements

The Key Character Identity Anchor Table / Main Character Master List is not only an art-review summary. It is the identity source of truth for downstream character state generation and must exist before episode-level production rows are generated.

Each key character row must include:

- `base_asset_id`
- `display_name`
- `priority`
- `identity_anchor_task_id`
- `identity_anchor_prompt`
- `identity_negative_prompt`
- `identity_reference_image`: approved image path/URL/task reference, or `pending`
- `identity_lock_status`: `pending`, `generated`, `approved`, `manual_review`, or `blocked`
- `stable_face_identity`: concise locked face/casting description
- `variable_state_axes`: clothing, grooming, injury, illness, wetness, makeup, age-state, class styling, etc.
- `review_focus`

Wardrobe in the master list is only auxiliary unless it is the character's permanent identity costume. Do not let master-list wardrobe become the only source of identity. The locked identity is primarily the face/casting identity.

## State Task Requirements

Every character state asset for a key character must include:

- `base_asset_id`
- `state_asset_id`
- `identity_anchor_task_id`
- `identity_reference_image`
- `generation_mode`: usually `image_edit_from_identity_anchor`
- `locked_identity_prompt`: copied from the approved master-list identity anchor
- `state_delta_prompt`: only the visible state changes for this state
- `edit_instruction`: preserve identity while changing state details
- `identity_change_allowed`: `false` by default
- `identity_change_reason`: required if `identity_change_allowed` is `true`

## Generation Modes

Allowed character generation modes:

- `text_to_image_identity_anchor`: first approved identity/casting portrait for a base character.
- `image_edit_from_identity_anchor`: normal mode for wardrobe, grooming, injury, illness, fatigue, dirt, blood, wetness, makeup, class styling, and most episode state variants.
- `image_edit_identity_sensitive_state`: for script-supported face/body changes that affect identity, such as serious illness, disfigurement, major injury, significant aging, pregnancy, or youth/old-age versions.
- `text_to_image_manual_exception`: only when the user explicitly requests independent generation or when no reference image can exist yet; must be marked for manual review.

Do not use `text_to_image_manual_exception` as a convenience fallback.

## Face-Lock Rules

For normal state edits:

- Preserve the exact same person from the reference image.
- Preserve face shape, bone structure, facial proportions, eye spacing, nose structure, mouth shape, skin undertone, age band, and core gaze quality.
- Do not beautify, de-age, slim the face, change ethnicity/region, change jawline, change eye shape, change nose, change lips, or make the character more generic.
- Change only the state-supported visual layer: clothes, hair styling, makeup, visible fatigue, injury, dirt, wetness, illness, or class styling.

For identity-sensitive states:

- Still start from the approved identity image.
- State exactly what may change and why.
- Keep recognizable continuity unless the script requires an unrecognizable transformation.
- Add `manual_review` if the transformation is likely to break identity continuity.

## State Delta Prompt Pattern

Use [character-state-edit-prompt-guard.md](character-state-edit-prompt-guard.md) as the source of truth for state edit text. The compact pattern below is only the default normal-state structure.

Use this pattern for normal state edits:

```text
Use the provided approved identity reference image as the source of truth for the character's face and casting identity. Preserve the same person: same face shape, bone structure, eye spacing, nose, mouth, skin undertone, age band, and core gaze quality.

Edit only the visible state details for this episode/state: [wardrobe / grooming / hair condition / makeup / injury / illness / fatigue / dirt / wetness / class styling].

Do not redesign the face, do not make a new person, do not beautify, do not de-age, do not change facial proportions, do not change ethnicity or regional features, do not change body type unless the state evidence requires it. Keep a single-character portrait on a plain neutral background, no props, no scene, no other characters.
```

## Manifest Fields

Character `items` in `prompt-manifest.json` must include:

```json
{
  "generation_mode": "image_edit_from_identity_anchor",
  "identity_anchor_task_id": "",
  "identity_reference_image": "",
  "locked_identity_prompt": "",
  "state_delta_prompt": "",
  "edit_instruction": "",
  "identity_change_allowed": false,
  "identity_change_reason": ""
}
```

For the identity anchor task itself:

```json
{
  "generation_mode": "text_to_image_identity_anchor",
  "identity_anchor_task_id": "",
  "identity_reference_image": "pending",
  "locked_identity_prompt": "",
  "state_delta_prompt": "",
  "edit_instruction": "Generate the first identity anchor portrait for approval."
}
```

## Quality Gate

Fail the output if:

- the same key character has multiple independent text-to-image state prompts
- a later state prompt rewrites the full face/casting description instead of referencing the locked identity anchor
- a state task lacks `identity_anchor_task_id`
- a state task lacks `identity_reference_image` and is not blocked/manual-review
- wardrobe, location, prop, emotion, or plot event is treated as a new face identity
- master-list identity is missing, vague, or not used downstream
- a normal wardrobe/state edit allows face redesign
