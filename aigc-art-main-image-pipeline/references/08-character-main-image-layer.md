# 08 Character Main Image Layer

This layer writes character analysis and main image prompts. It must use the PDF-verified character templates.

This layer must obey the character-state and prompt-scope boundaries in [04-state-variant-standard.md](04-state-variant-standard.md).

## Required Template Reference

Before working in this layer, read:
- [pdf-character-templates.md](pdf-character-templates.md)

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

## Inputs

Use registry items with:
- `asset_type: character`
- `needs_main_image: true`
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
- props, including cash, contracts, wine bowls, tools, phones, vehicles, reports, weapons, or furniture
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

Keep these fields in Chinese outside the prompt text:
- asset name
- state name
- evidence notes
- review checklist

The English image prompt must not contain:
- Chinese scene IDs or Chinese plot sentences
- props
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
- empty eyes
- wide-angle distortion
- unrealistic head/shoulder proportions

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
- character manifest items

## Acceptance Checklist

Before leaving this layer:
- every prompt uses the PDF-verified character structure
- state name is explicit
- state name describes visible appearance, not plot/event/prop/location
- image prompt text is English-only
- image prompt is single-character only
- image prompt uses a plain solid or neutral background
- image prompt contains no props, scene, location, other characters, or Chinese plot evidence
- story role is explicit
- material quality controls are present
- negative prompt blocks common drift
- review checklist is included
