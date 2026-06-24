# 11 Prop Main Image Layer

This layer writes prop analysis and main image prompts. It must use the PDF-verified prop templates.

## Required Template Reference

Before working in this layer, read:
- [pdf-prop-templates.md](pdf-prop-templates.md)
- [photographic-realism-style-guard.md](photographic-realism-style-guard.md)

Do not replace the PDF-verified prop biography or prompt structure with a shorter custom prompt.

## Goal

Generate prop main image prompts that help art staff judge:
- exact object type
- story state
- ownership or world identity
- structure and visible components
- material quality
- wear, damage, contamination, or maintenance state

For most props, the main image is the end of this skill's responsibility.

## Inputs

Use registry items with:
- `asset_type: prop`
- `needs_main_image: true`
- `status: ready_for_prompt` or user-approved `待人工确认`

Required fields:
- prop display name
- state name
- owner/user
- associated scene
- story function
- evidence
- object type
- visible components
- material focus
- condition/state
- wrong-type risks
- review focus

## Main Image Scope

Prop main image should usually be:
- isolated prop reference
- clean white or neutral background
- single object only
- no environment
- no people
- no hands
- no readable text
- no visible brand logos
- full object visible
- clear material texture

Exceptions require user or script need.

## Exact Type Rule

Always state:
- what the prop is
- what it is not

Example:
- “professional full-frame fashion photography camera, not casual camera, not amateur gear, not showroom product”

This prevents type drift.

## Story State Rule

Prop prompt must preserve:
- ownership
- usage state
- condition
- class/status
- story-specific marks
- visible components required by action

Do not generate generic product photography if the prop is used, damaged, old, hidden, threatening, intimate, or plot-specific.

## Material Quality Rules

For props, material quality means:
- realistic scale
- believable surface detail
- correct reflection behavior
- no plastic surface unless the prop is plastic
- visible wear when scripted
- metal/glass/leather/paper/wood/fabric treated specifically
- no fake CGI look

Examples:
- metal: cold highlights, brushed edges, scratches
- glass: layered reflections, transparency, thickness
- leather: grain, creasing, worn corners
- paper: fibers, folds, stains, age
- fabric: weave, wrinkles, softness
- plastic: molded edges, subtle scuffs, correct sheen

## Condition Rules

Condition must match the story:
- new
- used but maintained
- old
- damaged
- dirty
- bloodied
- wet
- burned
- broken
- opened
- sealed
- modified

Avoid catalog-perfect condition unless the script demands it.

## Composition Rules

Default:
- centered product-reference composition
- three-quarter angle if object structure matters
- full object visible
- enough padding
- natural shadow underneath allowed
- no environment reflection

If the prop's important detail is hidden from a three-quarter view, choose the angle that best reveals the required component.

## Analysis Output

Use the full prop biography template from `pdf-prop-templates.md`.

Every prop analysis must include:
- script evidence
- story function
- owner/user relationship
- appearance design
- scene relationship
- camera expression
- art execution focus

## Prompt Output

Use the full prop main image prompt template from `pdf-prop-templates.md`.

Prompt may be in English for model performance, but keep Chinese labels and review notes.

## Negative Prompt

Include negative controls for:
- original environment if isolated
- people/hands
- text/watermark/brand logo
- wrong object type
- wrong material
- wrong condition
- wrong era/style/use
- random extra objects
- dramatic scene lighting
- environment reflections
- fake CGI
- PBR product render
- luxury catalog polish unless scripted
- cartoon/anime
- unreadable shape

## What This Layer May Change

Allowed:
- refine prop visual language based on registry evidence
- choose reference angle
- add material and condition details
- add wrong-type negatives
- mark missing details as `待人工确认`

Not allowed:
- creating new prop assets
- creating new states
- changing rating
- adding hands or environment unless required
- ignoring PDF template
- turning prop into a luxury ad unless scripted

## Output

Produce:
- prop analysis blocks
- prop prompt blocks
- prop manifest items

## Acceptance Checklist

Before leaving this layer:
- every prompt uses the PDF-verified prop structure
- exact object type is clear
- condition matches story
- material details are concrete
- composition is isolated unless required otherwise
- negative prompt blocks product/catalog/style drift
