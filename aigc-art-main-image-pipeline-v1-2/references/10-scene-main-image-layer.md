# 10 Scene Main Image Layer

This layer writes scene analysis and main image prompts. It must use the PDF-verified scene templates.

## Required Template Reference

Before working in this layer, read:
- [pdf-scene-templates.md](pdf-scene-templates.md)
- [photographic-realism-style-guard.md](photographic-realism-style-guard.md)

Do not replace the PDF-verified scene biography or prompt structure with a shorter custom prompt.

## Goal

Generate scene main image prompts that help art staff judge:
- accurate space identity
- spatial layout
- class/world/function
- material quality
- lighting and atmosphere
- story-specific visual anchors

The goal is not multi-angle expansion.

## Inputs

Use registry items with:
- `asset_type: scene`
- `needs_main_image: true`
- `status: ready_for_prompt` or user-approved `待人工确认`

Required fields:
- scene display name
- state name
- location hierarchy
- time/lighting state
- world/class
- story function
- spatial function
- evidence
- required elements
- material focus
- wrong-space risks
- review focus

## Main Image Scope

Scene main image should usually be:
- readable spatial layout
- one strong visual anchor
- empty or near-empty space by default
- no recognizable characters unless the scene asset itself is an event/crowd-state reference
- enough architecture and set dressing to show identity
- detailed but not cluttered
- 16:9 unless the project requires another ratio

Do not generate:
- generic interior design render
- stock photo
- empty pretty room with no story function
- action still with messy character blocking
- crowd documentary photos
- busy public-service photos filled with many people unless the asset is explicitly a crowd/event state
- random luxury space when script demands specificity

## Character / Crowd Control

Scene main images are environment references, not action stills.

Default rule:
- no people
- no close faces
- no named characters
- no crowd
- no foreground body blocking the spatial layout

Allowed only when required for scale or function:
- one or two tiny, non-identifiable silhouettes
- distant backs or blurred figures
- staff silhouettes without readable faces

Event/crowd exception:
- If the scene state is explicitly an event or crowd state, e.g. registration queue, public forum, banquet, opening ceremony, protest, or crowded marketplace, people may appear only as layout-scale crowd dressing.
- Do not design individual faces, portraits, costumes, or named-character blocking inside the scene prompt.
- Prompt must still prioritize architecture, layout, signage shapes, desks, queue lanes, tables, stage, lighting, and material conditions.

Negative prompts for normal scenes must include:
- crowd, many people, recognizable faces, portrait, close-up people, action scene, documentary crowd photo

## Accurate Space Identity Rule

Always state:
- what the scene is
- what it is not

Example:
- “top-tier fashion photography studio, not a small portrait room, not a wedding studio, not an amateur rental space”

This is mandatory because scene prompts often drift into familiar generic locations.

## Spatial Layout Rule

Prompt must define:
- camera position
- entry relationship
- main space
- visual center
- background structure
- adjacent space only if needed

The image should help later angle expansion, but it is only the main reference.

## Material Quality Rules

For scenes, material quality means:
- believable wall, floor, ceiling, furniture, metal, glass, wood, fabric, stone, paper, plastic, dirt, reflections
- scale consistency
- non-plastic surfaces
- no fake CGI look
- no random glossy luxury if not scripted
- light reveals material texture

Use material descriptions tied to story:
- old palace wood should not look like a hotel lobby
- elite fashion studio should not look like a cheap rental room
- poor bedroom should not look like a styled catalog set

## Lighting Rules

Lighting must support:
- time
- plot mood
- material readability
- class/status
- scene state

Avoid:
- nightclub lighting unless scripted
- gloomy low-key lighting that hides materials
- beauty-ad lighting for non-ad spaces
- random cinematic rim light
- over-saturated fantasy color unless project style requires it

## Photographic Realism Guard

Scene assets are the highest-risk layer for game-CG drift. Every scene main image prompt must include controls for:
- real photograph / practical set / real location, not concept art or a game environment
- exposure based on script evidence and any provided reference image brightness, not a mechanically forced clock time
- limited camera dynamic range, local overexposure only where physically justified, and dark or low-contrast areas where detail would be lost
- restrained texture density, low-information large surfaces, natural dirt/wear, and no all-over micro-detail
- physically local light falloff for windows, sky, fire, lamps, neon, or candles
- imperfect composition and natural camera limitations rather than poster symmetry or level-entrance staging

Avoid style language that pushes CG, including:
- cinematic fantasy, epic, masterpiece, high-end production design, game environment, environment concept art
- high production value as a style phrase
- sharp but natural detail when applied to the whole frame
- immersive scene quality if it encourages polished render aesthetics

Negative prompts for scene assets must also block:
- Unreal Engine, Blender/Octane render, PBR asset look
- dense repeated cracks, repeated stains, procedural noise, every surface equally detailed
- mirror-like CG floor, uniform wet shader, decorative light effects
- UI elements, watermark, icon, avatar, sticker, modern interface artifact, readable modern text

## Scene State Rules

Use state name explicitly.

If state is `夜间空场`, prompt must control:
- empty space
- night light source
- quieter mood
- no crowd unless script requires it

If state is a queue / office / registration / public-service scene, prompt must control:
- readable spatial layout
- desks, counters, queue lanes, wall boards, signage shapes
- at most sparse non-identifiable scale figures unless the state specifically requires a crowd
- avoid news-photo crowd drift

If state is `宴会布置`, prompt must control:
- event layout
- decor density
- service elements
- class markers
- avoid random wedding/banquet hall drift

If state is `打斗后破坏`, prompt must control:
- specific damage
- debris placement
- material breakage
- avoid generic disaster scene

## Analysis Output

Use the full scene biography template from `pdf-scene-templates.md`.

Every scene analysis must include:
- script evidence
- core function
- spatial positioning
- element list
- material and lighting
- role relationship
- art execution focus

## Prompt Output

Use the full scene main image prompt template from `pdf-scene-templates.md`.

Prompt may be in English for model performance, but keep Chinese labels and review notes.

## Negative Prompt

Include negative controls for:
- wrong location
- wrong class
- wrong material
- wrong lighting
- wrong era/region
- unrelated props
- random clutter
- crowd or many people unless the state explicitly requires it
- recognizable faces
- named characters
- portrait-like people
- action-scene blocking
- low-quality texture
- plastic surfaces
- fake CGI
- cartoon/anime
- watermark/readable text/visible brand logos

Add project-specific negatives for common drift.

## What This Layer May Change

Allowed:
- refine scene visual language based on registry evidence
- choose camera position for main reference
- add wrong-space negatives
- mark missing details as `待人工确认`

Not allowed:
- creating new scene assets
- creating new states
- changing rating
- adding characters without need
- adding crowds without an explicit event/crowd-state need
- ignoring PDF template
- turning scene into pure mood art

## Output

Produce:
- scene analysis blocks
- scene prompt blocks
- scene manifest items

## Acceptance Checklist

Before leaving this layer:
- every prompt uses the PDF-verified scene structure
- scene identity and wrong-space warning are explicit
- layout is readable
- materials are specific
- lighting reveals material quality
- no unnecessary characters are included
- no crowds or recognizable people are included unless explicitly required by the scene state
