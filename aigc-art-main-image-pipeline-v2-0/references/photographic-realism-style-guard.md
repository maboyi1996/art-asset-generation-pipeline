# Photographic Realism Style Guard

Use this guard when writing main image prompts. It keeps assets from drifting into game CG, concept art, PBR asset renders, and over-designed production stills.

## Global Rule

Main image prompts must produce practical photographic references, not "better CG." Preserve plot evidence and asset identity, but describe the image as a real camera photograph with realistic exposure limits, natural material behavior, restrained texture density, and imperfect composition.

Do not mechanically assign a clock time unless the script explicitly states one. Derive brightness, time-of-day feel, and exposure from script evidence and any provided reference image. If evidence is only "night," "dawn," "interior," or "storm," describe the visible lighting relationship rather than forcing a precise hour.

## Exposure Reference

State the exposure reference in the prompt:
- "using the brightness already present in the input/reference as the exposure guide" when an image reference exists
- "based on the script's stated lighting and time" when only script evidence exists
- "do not force a different time of day" when the scene is easy to overcorrect

Real photographic exposure should include:
- limited dynamic range
- local overexposure only where physically justified, such as windows, sky gaps, fire, neon, or practical lamps
- dark or low-contrast areas where the camera would not recover detail
- distance, haze, smoke, rain, dust, or interior air reducing clarity
- no all-over HDR clarity or evenly lifted shadows

## Scene Guard

Scenes are the highest CG-risk asset type. Scene prompts must prefer:
- real photograph, practical set, real location, location scouting photo, documentary set reference
- natural camera limitations, imperfect framing, slight edge softness, finite lens resolution
- restrained texture density, low-information large surfaces, believable wear and dirt
- light sources that decay physically and affect only plausible areas
- messy but not decorative set dressing when the script supports damage, age, use, or battle aftermath

Avoid scene language that pushes concept art:
- cinematic fantasy, epic, masterpiece, high-end production design, game environment, environment concept art
- high production value as a visual style phrase
- sharp but natural detail when applied to the whole frame
- immersive scene quality if it encourages polished CG
- perfect symmetry, level entrance, hero vista, poster composition

Scene prompts must explicitly control:
- no Unreal Engine / Blender / Octane / PBR asset look
- no dense repeated cracks, repeated stains, procedural noise, or every surface equally detailed
- no mirror-like CG floor, uniform wet shader, over-clean reflections, or material showcase
- no decorative fire/window/moon/sky light that ignores real falloff
- no UI, watermark, icon, avatar, sticker, readable text, or modern interface artifact

## Character Guard

Characters have lower CG drift than scenes, but still need photographic portrait controls:
- realistic skin pores, translucency, slight color variation, tiny blemishes, asymmetry
- natural eye moisture and emotionally present eyes
- believable hairline, flyaway hair, uneven strand separation
- fabric wrinkles and material behavior tied to class/status/state
- plain solid or neutral background, no props, no scene

Avoid:
- AI beauty face, waxy/plastic skin, over-retouched glamour, fashion-campaign perfection
- commercial beauty lighting unless scripted
- excessive sharpness, doll face, perfect symmetry, empty eyes

## Prop Guard

Props usually perform well. Keep controls concise:
- isolated real product/reference photograph, not catalog luxury advertising
- correct scale, material thickness, reflection behavior, wear, dirt, damage, or maintenance state
- natural shadow under the object, no environment reflection unless required

Avoid:
- PBR product render, showroom gloss, dramatic scene lighting, clean luxury ad polish
- extra objects, hands, people, brand logos, readable text, watermark

## Prompt Add-On Blocks

For scene prompts, include a compact block equivalent to:

```text
Photographic realism guard:
This should look like an imperfect real photograph of a practical set or real location, using the brightness already present in the input/reference as the exposure guide. Use limited camera dynamic range, natural lens softness, restrained texture density, low-information large surfaces, realistic old materials, physically local light falloff, and imperfect composition. Avoid game CG, Unreal Engine, Blender/Octane render, PBR asset look, concept art, poster composition, HDR clarity, over-sharpening, dense repeated surface noise, mirror-like CG floors, uniform wet shader, UI artifacts, watermarks, icons, avatars, stickers, and readable modern text.
```

For character prompts, include a compact block equivalent to:

```text
Photographic realism guard:
Real portrait photograph, natural camera limitations, realistic skin pores and color variation, subtle asymmetry, natural hairline and flyaways, fabric wrinkles, emotionally present eyes, no AI beauty face, no waxy/plastic skin, no over-retouched glamour, no commercial beauty campaign polish.
```

For prop prompts, include a compact block equivalent to:

```text
Photographic realism guard:
Real isolated prop reference photograph, believable scale and material thickness, correct reflection behavior, natural wear or condition, soft neutral lighting, natural shadow, no PBR product render, no luxury catalog polish, no environment reflections, no hands, no extra objects, no readable text, no watermark.
```
