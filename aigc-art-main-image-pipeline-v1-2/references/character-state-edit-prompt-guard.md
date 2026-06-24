# Character State Edit Prompt Guard

Use this guard whenever a character already has an approved identity/reference image and a later task must generate a new visible state from that image.

This applies to:
- key characters with an identity anchor from the Key Character Identity Anchor Table
- non-key characters whose first generated character image becomes the reference image for later states
- identity-sensitive states that still need continuity from an existing person

## Core Rule

A character state edit prompt is not a new character design prompt.

It must combine:
- `identity_reference_image`: the approved image that defines the same person
- `locked_identity_prompt`: the stable identity text copied from the anchor or first generated reference
- `state_delta_prompt`: only the visible changes required for this state
- `edit_instruction`: a short instruction to preserve identity and apply only the state delta

Do not use similar full text-to-image prompts as a substitute for the reference image. Even copied text can sample a different face.

## State Delta Scope

`state_delta_prompt` may include only visible character-state changes supported by script evidence:

- clothing category, silhouette, uniform, disguise, formal wear, workwear, poverty/wealth styling
- hairstyle, grooming, beard, hair condition, wet hair, messy hair
- makeup, bare face, tired makeup, ceremonial makeup
- injury, illness, fatigue, dirt, blood, sweat, wetness, pregnancy, visible body condition
- age-state when the script supports youth, childhood, older age, flashback, or future appearance
- class/status styling when it changes visible presentation

Keep the delta concrete and compact. Prefer physical, visible details over abstract mood words.

## Forbidden Content

Do not put these into `state_delta_prompt`:

- redesigned face, new facial structure, new ethnicity/region, new body type, new age band
- broad personality rewrite or generic casting rewrite
- location, room, street, battlefield, vehicle, or other scene content
- props held by the character, unless the prop is permanently worn and changes the character's appearance
- momentary action, camera angle, plot event, relationship, victory/loss, humiliation, argument, or dialogue content
- temporary emotion unless it leaves a visible stable state such as crying marks, exhaustion, or illness
- beauty retouching, luxury fashion ad language, waxy skin, plastic skin, or commercial portrait polish

If the script truly requires face/body identity change, use `image_edit_identity_sensitive_state`, set `identity_change_allowed: true`, and provide `identity_change_reason`.

## Normal Edit Pattern

Use this structure for normal state edits:

```text
Use the approved identity reference image as the source of truth for the same person.
Preserve the same face, facial proportions, bone structure, eye spacing, nose, mouth, skin undertone, age band, body type, and core gaze quality.
Change only the visible state details: [state_delta_prompt].
Keep a single-character portrait on a plain neutral background. No props, no scene, no other characters.
Do not redesign the face, beautify, de-age, change ethnicity/region, change body type, or create a new person.
```

## Field Writing Rules

`locked_identity_prompt`:
- copied from the approved key-character anchor, or from the first generated character reference for non-key characters
- describes stable face/casting identity only
- does not change across normal wardrobe, grooming, injury, illness, dirt, wetness, or class-state edits

`state_delta_prompt`:
- written fresh for each valid state
- contains only the state-specific visible changes
- should be empty or marked `reuse_existing` when there is no visible state change from an existing generated state

`edit_instruction`:
- says what image to use as identity reference
- says what to change
- says what must not change

## Reuse vs Edit

Do not create a new state edit task when the later appearance is visually the same as an already generated state.

Use:
- `reuse_existing` when the same character state can reuse an existing image
- `image_edit_from_identity_anchor` when the same person needs a new wardrobe, grooming, injury, illness, dirt, wetness, age, or class/status state
- `image_edit_identity_sensitive_state` when the script-supported state may visibly alter identity continuity

## Quality Gate

Fail the task if:

- a later character state is written as an independent full text-to-image prompt without an approved reference image
- `state_delta_prompt` repeats or redesigns the stable face identity
- the reference image is missing and the task is not blocked/manual-review
- props, scenes, actions, plot events, or relationships are treated as character-state deltas
- a visually identical later appearance is generated again instead of marked `reuse_existing`
- a non-key character reappears with a new state but does not reference the first generated image or another approved identity reference
