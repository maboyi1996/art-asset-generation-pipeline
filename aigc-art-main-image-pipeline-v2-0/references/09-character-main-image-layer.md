# 09 Character Main Image Layer

This layer writes character analysis, main image prompts, and character state edit instructions for global asset-state tasks. It must use the PDF-verified character templates.

This layer must obey the character-state and prompt-scope boundaries in [04-state-variant-standard.md](04-state-variant-standard.md).

## Required Template Reference

Before working in this layer, read:
- [pdf-character-templates.md](pdf-character-templates.md)
- [photographic-realism-style-guard.md](photographic-realism-style-guard.md)
- [07-character-identity-anchor-layer.md](07-character-identity-anchor-layer.md)
- [character-state-edit-prompt-guard.md](character-state-edit-prompt-guard.md)

Do not replace the PDF-verified character biography or prompt structure with a shorter custom prompt.

## Goal

Generate story-faithful, high-quality character main image prompts that help art staff judge:
- face identity
- age feeling
- class/status
- core emotion
- costume/state
- body language
- material realism

The goal is not a final character package. Do not generate three-view sheets.

For recurring/key characters, the first goal is to create or reference a stable identity anchor. Later state prompts must preserve that anchor and describe only the state delta. For non-key characters, the first generated character image can become the later reference image when that character reappears with a new valid state.

This layer works from the Global Asset State Task Map. Do not create character prompts directly from episode tables.

## Inputs

Use registry items with:
- `asset_type: character`
- `task_type`: `text_to_image`, `image_text_edit`, `reuse_existing`, `blocked`, or `manual_review`
- `needs_main_image: true` unless the task is `reuse_existing` or `record_only`
- `status: ready_for_prompt` or user-approved `待人工确认`

Required fields:
- display name
- state name
- age or age range
- identity / occupation
- class / world
- story function
- evidence
- visual identity
- state evidence
- relationship notes
- material focus
- review focus

Required task-map fields:
- `task_id`
- `task_type`
- `state_asset_id`
- `first_needed_episode`
- `first_needed_scene`
- `used_in_episodes`
- `used_in_scenes`

For recurring/key characters, also require:
- `generation_mode`
- `identity_anchor_task_id`
- `identity_reference_image`
- `locked_identity_prompt`
- `state_delta_prompt` when this is not the anchor task
- `identity_lock_status`

## Main Image Scope

Character main image must be:
- a single character only
- portrait or bust portrait
- plain solid or clean neutral background
- eye-level camera
- natural portrait lens
- face and upper-body readable
- costume/state visible enough for art review
- no props
- no scene or location
- no other characters
- no action-scene staging

Avoid:
- full action scene
- complex environment
- multiple characters
- props, including cash, contracts, wine bowls, tools, phones, vehicles, reports, weapons, furniture, bags, backpacks, schoolbags, handbags, briefcases, or handheld items
- cinematic action still
- over-posed fashion campaign
- Chinese plot evidence inside the English image prompt

If a source beat depends on a prop or location, keep that information in evidence, review focus, or separate scene/prop assets. Do not move it into the character prompt.

## Evidence-To-Visual Rule

Every key visual choice should come from:
- direct evidence
- repeated behavior
- role/class/world inference
- state evidence

If a visual choice is inferred, make it conservative and mark it as inferred in analysis notes.

## Character Identity Rules

The prompt must protect:
- age accuracy
- face uniqueness
- story role
- class/status
- emotional restraint or intensity as scripted
- difference from similar characters

Always specify what the character is **not** if there is common drift:
- not generic attractive person
- not influencer beauty
- not fashion model unless the role demands it
- not wrong age
- not wrong class/status
- not seductive if not scripted

For recurring/key characters, do not create a new full face/casting prompt for each state. Use the Main Character Master List as the identity source of truth:
- `text_to_image_identity_anchor` creates the first approved portrait for the base character.
- `image_edit_from_identity_anchor` uses the approved image plus a state delta for later wardrobe/grooming/body-condition states.
- `image_edit_identity_sensitive_state` still starts from the approved image when script evidence changes face/body identity.

If `identity_reference_image` is missing or not approved, later state tasks must be `blocked_identity_anchor_required` or `manual_review`. Do not silently fall back to independent text-to-image.

For task typing:
- `text_to_image` writes a full character main-image prompt.
- `image_text_edit` writes `locked_identity_prompt`, `state_delta_prompt`, and `edit_instruction`; it must include `reference_image`.
- `reuse_existing` writes no new prompt and must point to `reuse_from_task_id`.
- `blocked` and `manual_review` must explain what is missing or uncertain.

## Material Quality Rules

For characters, material quality means:
- realistic skin pores and translucency
- non-plastic skin
- non-waxy face
- natural skin color variation
- believable hairline and flyaway hair
- fabric texture and wrinkles
- natural makeup finish unless script requires polish
- controlled highlights
- no oily/sweaty gloss unless state requires it

For special states:
- wet hair must look physically wet but not glossy plastic
- injuries must fit the script and avoid gore drift unless required
- dirt/blood/sweat must be state-specific, not random decoration
- formal clothing must show fabric and tailoring, not luxury ad polish

## Character State Rules

Use state name explicitly in analysis and prompt.

The state name must describe visible character appearance only:
- age appearance
- hair / grooming
- makeup
- clothing category
- illness, injury, fatigue, dirt, wetness, or other visible body condition
- visible class/status styling

Do not use plot events, props, locations, or actions as character states.

The state prompt must not rewrite stable face identity as if designing a new person. For recurring/key characters, copy the locked identity into `locked_identity_prompt`. For non-key characters that already have a generated reference image, copy the stable identity from the first approved/generated task. Put only costume, grooming, hair condition, makeup, illness, injury, fatigue, dirt, blood, wetness, or other script-supported visible changes in `state_delta_prompt`, following [character-state-edit-prompt-guard.md](character-state-edit-prompt-guard.md).

Examples:
- Correct: `陈有财--外观（中年乡镇老板）状态`
- Wrong: `陈有财--外观（坐在120万现金中间）状态`

For the wrong example, create or use separate scene/prop tasks for cash and the room, while the character prompt remains a clean single-character portrait.

If state is `洗澡后湿发`, the prompt must control:
- wet hair
- skin finish
- clothing/bathrobe/towel if applicable
- vulnerability or privacy tone if script supports it
- avoid eroticized framing unless script explicitly requires it

If state is `晚宴礼服`, the prompt must control:
- dress silhouette
- fabric material
- class/status
- makeup level
- event identity
- avoid generic red carpet celebrity drift unless scripted

## Analysis Output

Use the full character biography template from `pdf-character-templates.md`.

Do not omit sections unless the user explicitly asks for a compressed output.

If information is missing:
- write `待人工确认`
- do not fill with invented facts

## Prompt Output

Use the full character main image prompt template from `pdf-character-templates.md`.

The image-generation prompt itself must be English-only.

Use the identity anchor template for a first key-character portrait. Use the state edit template for later states of the same character.

Keep these fields in Chinese outside the prompt text:
- asset name
- state name
- evidence notes
- review checklist

The English image prompt must not contain:
- Chinese scene IDs or Chinese plot sentences
- props
- bags, backpacks, schoolbags, handbags, briefcases, or handheld items
- room/location/environment descriptions
- multiple-character relations
- plot-event labels such as dividing money, signing, rejecting acquisition, being humiliated, or revenge

Use story evidence to choose age, class/status, grooming, clothing, expression restraint, and material realism, not to stage a full scene.

## Negative Prompt

Include negative controls for:
- wrong age
- too young / too old
- generic attractive person
- AI beauty face
- influencer makeup
- K-pop idol beauty if inappropriate
- commercial beauty lighting
- plastic/waxy/CGI skin
- over-retouched face
- CG render face
- AI beauty face
- commercial campaign polish
- empty eyes
- wide-angle distortion
- unrealistic head/shoulder proportions

For state-edit tasks, also include identity-continuity negatives:
- different person
- changed face shape
- changed eye spacing
- changed nose or mouth
- changed jawline
- changed skin undertone
- changed age band
- beautified redesign
- de-aged face
- generic replacement face

Add project-specific negatives when needed:
- wrong costume period
- wrong class
- wrong ethnicity/region if specified
- wrong hairstyle
- wrong emotional tone

## What This Layer May Change

Allowed:
- refine character visual language based on registry evidence
- choose prompt wording
- add negative prompt protections
- mark missing details as `待人工确认`

Not allowed:
- creating new character assets
- creating new state assets
- changing priority
- ignoring PDF template
- adding unsupported beauty or fashion elements

## Output

Produce:
- character analysis blocks
- character prompt blocks
- character global task rows

For recurring/key characters, character global task rows must include identity anchor/edit fields from [07-character-identity-anchor-layer.md](07-character-identity-anchor-layer.md).

## Acceptance Checklist

Before leaving this layer:
- every prompt uses the PDF-verified character structure
- recurring/key character identity anchor tasks are separated from later state edit tasks
- later states of the same key character use `image_edit_from_identity_anchor` unless explicitly blocked/manual-review/manual exception
- later states of a non-key character use the first approved/generated character image as the reference image when available
- later state prompts preserve the same approved person and change only the state delta
- no recurring/key character has multiple independent full text-to-image prompts for different episode states
- each character production row has `task_id` and `task_type`
- `reuse_existing` rows do not contain new prompts
- state name is explicit
- state name describes visible appearance, not plot/event/prop/location
- image prompt text is English-only
- image prompt is single-character only
- image prompt uses a plain solid or neutral background
- image prompt contains no props, scene, location, other characters, or Chinese plot evidence
- image prompt contains no bags, backpacks, schoolbags, handbags, briefcases, or handheld items
- story role is explicit
- material quality controls are present
- negative prompt blocks common drift
- review checklist is included
