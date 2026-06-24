# 11 Output Contracts

This layer defines what the workflow finally gives to the art team.

The pipeline may create internal coverage, registry, audit, and biography material while reasoning. Those are process artifacts. They are not the default final deliverable.

## Goal

Produce two final views of the same production task set:
- a human-facing markdown production table for art review
- a machine-facing JSON manifest for image generation / model reading

The two files must stay aligned. They are not separate analyses.

The human-facing table should:
- easy for a human art owner to scan
- organized by project and episode
- contains final prompts ready for copy/API use
- preserves enough evidence and review focus to catch obvious mistakes
- does not force art staff to read long biographies or audit logs

The machine-facing manifest should:
- expose stable fields
- avoid markdown formatting noise
- include the same prompts and negative prompts
- preserve task IDs, asset IDs, episode IDs, priority, ratio, and review focus
- be ready for later API scripts

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
2. Main character master list
3. Episode production tables
4. Manual review / blocked items
5. Generation notes

## Project Summary

Keep short. Include:
- project title
- source scope
- total episodes/scenes processed
- total main image tasks
- counts by asset type
- counts by priority
- unresolved manual review count

Example:

```markdown
# 主图生产总表

## 项目概览
| 项目 | 剧集范围 | 主图任务数 | 人物 | 场景 | 道具 | 待人工确认 |
|---|---:|---:|---:|---:|---:|---:|
| 项目名 | E01-E12 | 86 | 24 | 31 | 31 | 5 |
```

## Main Character Master List

At the top of the output, include the main recurring characters before episode tables.

This section is for the art owner to understand the major cast without reading all prompt tasks.

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

## Episode Production Tables

After the main character list, organize production tasks by episode.

For each episode:
- list all character state tasks appearing or first needed in that episode
- list all scene state tasks appearing or first needed in that episode
- list all prop state tasks appearing or first needed in that episode

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

## Asset Duplication In Episode Tables

Avoid repeating the same exact task in every episode where it appears.

Default rule:
- place the task in the first episode where the main image is needed
- later episodes may reference it as `沿用 E02 已生成主图`

Create a new row in a later episode only if:
- a new state variant appears
- the asset was not previously generated
- the new appearance changes production need
- the user wants per-episode full repetition

## Prompt Cell Rules

Prompt cells must contain final, copy-ready prompts.

They may be long, but should not include:
- unresolved bracket placeholders
- full biography text
- audit commentary
- pipeline notes

If markdown table cells become too hard to read, use this block format inside each episode:

```markdown
### E03 人物主图

#### [S] Luna--原始（晚宴礼服）状态
| 字段 | 内容 |
|---|---|
| 首次场次 | E03-S014 |
| 剧情依据 / 功能 | 首次进入高奢晚宴，被权力场凝视，体现格格不入和被唤醒。 |
| 材质重点 | 皮肤真实、礼服织物、低调珠光、非广告精修。 |
| 画幅 | 9:16 |
| 主图提示词 | ... |
| 负面提示词 | ... |
| 审核重点 | 年龄、礼服状态、眼神克制、避免网红脸。 |
| 状态 | ready |
```

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
- prompts blocked by missing facts

## Generation Notes

Add only practical notes:
- image ratios used
- B/C asset handling
- that `prompt-manifest.json` was produced from the same task set
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
  "items": []
}
```

Each item:

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
  "main_image_only": true,
  "image_ratio": "9:16",
  "prompt": "",
  "negative_prompt": "",
  "story_evidence_summary": "",
  "review_focus": [],
  "status": "ready_for_generation"
}
```

Allowed `asset_type`:
- `character`
- `scene`
- `prop`

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
- every S/A generated task appears in the production table
- every production table task appears in the manifest unless its status is blocked/manual-review
- major characters appear in the master list
- episode sections are clear
- final prompts have no unresolved placeholders
- manual review items are compact and actionable
- manifest matches the human table

## Acceptance Checklist

Before leaving this layer:
- final output does not expose process artifacts as deliverables
- human table is readable and complete
- machine manifest is valid and aligned
- prompts are copy-ready
- no secrets are included
