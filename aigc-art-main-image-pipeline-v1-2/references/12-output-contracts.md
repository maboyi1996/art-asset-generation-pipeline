# 12 Output Contracts

This layer defines what the workflow finally gives to the art team.

The pipeline may create internal coverage, registry, audit, and biography material while reasoning. Those are process artifacts. They are not the default final deliverable.

## Goal

Produce two final files:
- a human-facing markdown production table for art review
- a machine-facing JSON manifest for image generation and asset tracking

The two files must stay aligned.

The output must separate:
- `main_image_tasks`: assets/states that need a new main image and prompt.
- `episode_asset_usage`: every character, scene, and prop state used by every episode, including reused assets that do not need a new prompt.
- character identity anchors: approved base-character image tasks used by later state edit tasks.

This distinction is mandatory. Art staff need both the generation task list and the per-episode usage map.

## Final Outputs

Always produce:
- `main-image-production-table.md`
- `prompt-manifest.json`

Only produce additional internal files when the user explicitly asks for them or when debugging the pipeline.

## Internal Artifacts

These may exist during execution but are not final by default:
- scene coverage
- candidate asset tables
- state variant maps
- priority tables
- asset registry
- audit report
- full character/scene/prop biographies

They should inform the final table, not burden the art team.

## Human-Facing Final File

Filename:
- `main-image-production-table.md`

This file should read like a structured spreadsheet in markdown.

Required top-level sections:
1. Project summary
2. Key Character Identity Anchor Table / Main character master list
3. Episode asset usage lists
4. Main image generation tasks
5. Manual review / blocked items
6. Generation notes

## Project Summary

Keep short. Include:
- project title
- source scope
- total episodes/scenes processed
- total new main image tasks
- total episode usage rows
- counts by asset type
- counts by priority
- unresolved manual review count

Example:

```markdown
# 主图生产总表

## 项目概览
| 项目 | 剧集范围 | 新主图任务 | 使用清单行 | 人物 | 场景 | 道具 | 待人工确认 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 项目名 | E01-E40 | 36 | 214 | 12 | 12 | 12 | 3 |
```

## Main Character Master List

At the top of the output, include the main recurring characters before episode tables.

This section is for the art owner to understand the major cast without reading all prompt tasks.

This section is also a required workflow gate. Build it before writing any episode-by-episode character/scene/prop production rows. It must come from the global registry after character extraction, deduplication, state detection, rating, and registry merge, not from one episode's task list.

Include only major characters:
- S-level characters
- recurring A-level characters
- user-requested key characters

Columns:
- `角色`
- `等级`
- `主要状态`
- `精简人物小传`
- `核心视觉识别`
- `主图提示词`
- `负面提示词`
- `审核重点`

The biography here must be compact. Use the PDF character biography as internal reasoning, but compress final display to a few precise lines.

Do not paste the full character biography unless the user asks.

For S-level characters, recurring A-level characters, and user-requested key characters, this section is also the downstream identity source of truth. Include these additional fields even if the human-facing column names are localized:
- `base_asset_id`
- `identity_anchor_task_id`
- `identity_anchor_prompt`
- `identity_negative_prompt`
- `identity_reference_image`: approved image path/URL/task reference, or `pending`
- `identity_lock_status`: `pending`, `generated`, `approved`, `manual_review`, or `blocked`
- `stable_face_identity`
- `variable_state_axes`

Later episode state rows must reference this identity anchor instead of rewriting an independent full character prompt.

Episode tables are invalid if they contain key-character state prompts before the corresponding key-character identity anchor row exists.

## Episode Asset Usage Lists

This section is mandatory. It answers: "What character, scene, and prop states does each episode use?"

It must include reused assets even when no new image prompt is generated.

For each episode, list:
- all character states used
- all scene/location states used
- all prop states used
- whether each item is `new_main_image`, `reuse`, `blocked`, or `manual_review`
- `first_generated_in` when reusing an earlier task
- `reuse_from_task_id` when available

Recommended columns:
- `资产类型`
- `资产 / 状态`
- `使用场次`
- `使用方式`
- `首次生成集/场`
- `reuse_from_task_id`
- `本集功能`
- `备注`

Use compact rows. Do not paste full prompts in this section.

Example:

```markdown
### E06 资产使用清单
| 资产类型 | 资产 / 状态 | 使用场次 | 使用方式 | 首次生成集/场 | reuse_from_task_id | 本集功能 | 备注 |
|---|---|---|---|---|---|---|---|
| character | 陈北--外观（朴素正装）状态 | E06-S001,E06-S003 | reuse | E02-S006 | CH-E02-001 | 延续主角身份 | 不重复生成 |
| scene | 陈北酒厂--初始（日间生产）状态 | E06-S002 | reuse | E03-S004 | SC-E03-002 | 生产空间 | 不重复生成 |
| prop | 转让协议--初始（盖章签字）状态 | E06-S001 | new_main_image | E06-S001 | PR-E06-001 | 剧情证据 | 需生成 |
```

## Main Image Generation Tasks

After usage lists, organize only the tasks that need new main images by episode.

For each episode:
- list character state tasks first needed in that episode
- list scene state tasks first needed in that episode
- list prop state tasks first needed in that episode

Use this section order inside each episode:
1. 人物主图
2. 场景主图
3. 道具主图

Recommended columns:
- `资产类型`
- `资产 / 状态`
- `等级`
- `首次场次`
- `剧情依据 / 功能`
- `材质重点`
- `画幅`
- `主图提示词`
- `负面提示词`
- `审核重点`
- `状态`

Use compact wording in evidence. Do not paste long script passages.

For character generation tasks, also include these fields in the row or block format:
- `generation_mode`
- `identity_anchor_task_id`
- `identity_reference_image`
- `locked_identity_prompt`
- `state_delta_prompt`
- `edit_instruction`
- `identity_change_allowed`
- `identity_change_reason`

The first key-character task is usually `text_to_image_identity_anchor`. Later state tasks for the same key character are usually `image_edit_from_identity_anchor`.

## Asset Duplication Rules

Avoid repeating the same exact generation task in every episode where it appears.

Default rule:
- place the prompt task in the first episode where the main image is needed
- later episodes must reference it in the Episode Asset Usage Lists as `reuse`
- for recurring/key characters, first create or reference the character identity anchor, then create later visual states as image-edit tasks from that anchor

Create a new generation task in a later episode only if:
- a new state variant appears
- the asset was not previously generated
- the new appearance, spatial condition, or object condition changes production need
- the user wants per-episode full repetition

Do not omit reused assets from the final output. Omit only duplicate prompts, not usage rows.

For recurring/key characters, a later visual state should be a new edit task, not a new independent text-to-image task. If the approved identity anchor image is unavailable, mark the task blocked/manual-review instead of generating a separate face.

## Prompt Cell Rules

Prompt cells must contain final, copy-ready prompts.

They may be long, but should not include:
- unresolved bracket placeholders
- full biography text
- audit commentary
- pipeline notes

If markdown table cells become too hard to read, use block format inside each episode.

Prefer readability over forcing huge prompts into a single wide table.

## Manual Review / Blocked Items

Include a compact section for items that should not silently proceed.

Columns:
- `资产 / 状态`
- `问题`
- `影响`
- `建议处理`

Use for:
- evidence gaps
- conflicts
- uncertain aliases
- uncertain state splits
- flashback / timeline uncertainty
- prompts blocked by missing facts

## Generation Notes

Add only practical notes:
- image ratios used
- B/C asset handling
- that `prompt-manifest.json` was produced from the same task set
- whether `episode_asset_usage` includes reused assets
- any known limitations

Do not include long pipeline explanations.

## Machine Manifest

Filename:
- `prompt-manifest.json`

This file is always produced. It is the machine-readable twin of `main-image-production-table.md`.

Top-level structure:

```json
{
  "project": {
    "title": "",
    "source_scope": "",
    "human_table": "main-image-production-table.md"
  },
  "generation_scope": "main_image_only",
  "items": [],
  "episode_asset_usage": []
}
```

Each `items` entry is a new main-image generation task:

```json
{
  "task_id": "",
  "episode_id": "",
  "scene_id": "",
  "asset_id": "",
  "asset_type": "character",
  "display_name": "",
  "state_name": "",
  "priority": "S",
  "generation_mode": "text_to_image_identity_anchor",
  "identity_anchor_task_id": "",
  "identity_reference_image": "pending",
  "locked_identity_prompt": "",
  "state_delta_prompt": "",
  "edit_instruction": "",
  "identity_change_allowed": false,
  "identity_change_reason": "",
  "main_image_only": true,
  "image_ratio": "9:16",
  "prompt": "",
  "negative_prompt": "",
  "story_evidence_summary": "",
  "review_focus": [],
  "status": "ready_for_generation"
}
```

For character tasks, allowed `generation_mode` values:
- `text_to_image_identity_anchor`
- `image_edit_from_identity_anchor`
- `image_edit_identity_sensitive_state`
- `text_to_image_manual_exception`

Scene and prop tasks can omit character identity fields or set them to empty values.

Each `episode_asset_usage` entry records usage, including reused assets:

```json
{
  "episode_id": "",
  "scene_ids": [],
  "asset_id": "",
  "asset_type": "character",
  "display_name": "",
  "state_name": "",
  "usage_status": "reuse",
  "first_generated_in": {
    "episode_id": "",
    "scene_id": "",
    "task_id": ""
  },
  "reuse_from_task_id": "",
  "episode_function": "",
  "notes": ""
}
```

Allowed `asset_type`:
- `character`
- `scene`
- `prop`

Allowed `usage_status`:
- `new_main_image`
- `reuse`
- `blocked`
- `manual_review`

Character state usage should preserve the relevant `identity_anchor_task_id` and `reuse_from_task_id` when a later episode uses an already generated state edit.

Recommended image ratios:
- Character: `9:16`
- Scene: `16:9`
- Prop: `1:1` or `4:3`, unless the project requires otherwise

## Language Rules

Use Chinese for:
- table labels
- evidence summaries
- review focus
- manual review notes
- compact biographies

Use English for final image prompts when it improves model output.

Do not leave Chinese bracket placeholders inside English prompts unless the user specifically wants template prompts instead of final prompts.

## API Readiness

`prompt-manifest.json` must not include:
- API keys
- private endpoint secrets
- cookies
- user credentials

Add API fields only after the API contract is known.

## Output Validation

Before final delivery:
- final output includes both required files
- `main-image-production-table.md` is readable as the human review surface
- `prompt-manifest.json` is valid JSON
- every new generation task appears in the production table
- every production table generation task appears in manifest `items` unless blocked/manual-review
- every episode has an asset usage list
- every used character, scene, and prop state appears in `episode_asset_usage`, including reused assets
- generation task rows are not duplicated just to show episode reuse
- major characters appear in the master list
- key character master-list rows include identity anchor fields
- recurring/key character state tasks reference the identity anchor instead of independent text-to-image prompts
- episode sections are clear
- final prompts have no unresolved placeholders
- manual review items are compact and actionable
- manifest `items` and `episode_asset_usage` match the human table
- no secrets are included

## Acceptance Checklist

Before leaving this layer:
- final output does not expose process artifacts as deliverables
- human table is readable and complete
- machine manifest is valid and aligned
- prompts are copy-ready
- every episode has usage rows
- reused assets are visible without duplicate prompts
- no secrets are included
