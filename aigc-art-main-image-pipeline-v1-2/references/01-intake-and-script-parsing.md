# 01 Intake And Script Parsing

This layer turns source material into reliable analysis units. It does not judge asset value and does not generate prompts.

## Goal

Create a clean, traceable script structure that later layers can reference without guessing:
- episodes
- scenes
- scene headings
- locations
- time of day
- characters
- action descriptions
- dialogue
- prop mentions
- state change clues

## Accepted Inputs

Supported sources:
- PDF
- DOCX
- TXT
- MD
- pasted text
- mixed project notes plus script excerpts

When files are provided, extract text before analysis. If extraction is visibly garbled, stop and report the extraction problem rather than analyzing corrupted text.

## Parsing Units

Prefer this hierarchy:
1. project
2. episode
3. scene
4. beat / paragraph
5. line / action / dialogue

If the script lacks formal episode labels, infer blocks from file names or headings and mark the inference.

If the script lacks formal scene headings, split by location, time, character group, or major action transition and mark the split as inferred.

## What To Preserve

Preserve exactly when possible:
- character names
- alternate names and titles
- scene headings
- location names
- time labels
- direct dialogue
- action descriptions involving appearance, costume, injury, props, or environment
- any explicit visual adjectives

Do not normalize away culturally meaningful wording. For example, “娘娘”, “少爷”, “掌事”, “太医”, “王府”, and similar role/location terms may carry asset identity.

## Cleaning Rules

Allowed cleaning:
- remove page numbers
- remove repeated headers/footers
- normalize obvious OCR line breaks
- group fragmented dialogue lines
- mark unreadable fragments

Not allowed:
- rewriting the script into a summary
- changing dialogue wording
- merging scenes only because they feel similar
- deleting repeated visual mentions as “redundant” before coverage is built
- translating names unless requested

## Segment Record Format

For every parsed scene or inferred scene, create a record with:
- `episode_id`
- `scene_id`
- `source_range`
- `raw_heading`
- `location_raw`
- `time_raw`
- `characters_raw`
- `action_text`
- `dialogue_text`
- `prop_mentions_raw`
- `visual_state_clues_raw`
- `parse_confidence`
- `parse_notes`

Use stable IDs even when labels are inferred:
- `E01-S001`
- `E01-S002`
- `UNK-E01-S001` if episode is unknown

## State Clue Detection During Parsing

Do not split state assets here, but preserve clues such as:
- clothing change
- wet hair / bathing / rain / sweat
- blood / injury / illness
- disguise / identity reveal
- makeup / no makeup / ruined makeup
- age change / flashback
- lighting state
- scene dressing change
- prop damage / contamination / wear

These clues feed the State Variant layer.

## Uncertainty Handling

Mark `parse_confidence`:
- `high`: explicit heading and clear scene boundaries
- `medium`: scene inferred from location/time/action break
- `low`: OCR, messy prose, missing speaker labels, or unclear boundaries

Low-confidence chunks must be flagged for audit.

## Output

Produce:
- parsed script map
- per-scene source references
- parse uncertainty list
- extraction quality notes

This layer passes structured script units to Scene Coverage. It must not output final asset tables or image prompts.

## Acceptance Checklist

Before leaving this layer:
- every analyzable part of the source belongs to a scene or chunk
- every scene/chunk has a stable ID
- source evidence can be traced back
- obvious OCR or extraction problems are reported
- state clues are preserved for later layers
