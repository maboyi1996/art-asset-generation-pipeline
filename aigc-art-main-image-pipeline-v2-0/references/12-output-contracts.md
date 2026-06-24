# 12 Output Contracts

This layer defines the final MD-only production files.

The pipeline may create internal coverage, registry, audit, and biography material while reasoning. Those are process artifacts. They are not default deliverables.

## Goal

Produce two final Markdown files by default:
- `main-image-production-table.md`: the complete machine/source-of-truth production table for AI models and downstream technical parsing.
- `main-image-review-table.md`: the compact human-readable Markdown review table for art staff.

Do not produce `prompt-manifest.json` unless the user explicitly asks for a separate technical conversion artifact.

The machine MD must support downstream technical parsing and prompt reuse. The human review MD must support ordinary art review in a Markdown previewer without forcing reviewers to inspect long prompt cells.

Critical separation rule:
- Build and validate `main-image-production-table.md` first.
- Derive `main-image-review-table.md` from the completed machine table.
- Never let human review table formatting requirements reduce, merge, block, omit, rename, or otherwise change global asset-state tasks, state variants, prompts/edit instructions, or episode usage rows in `main-image-production-table.md`.
- Do not rerun asset extraction, state variant detection, priority rating, registry merging, blocking decisions, or prompt generation just to create `main-image-review-table.md`.

## V2.0 Output Architecture

The final outputs must preserve the hybrid workflow:

1. Identification by episode/scene.
2. Production by global asset state.
3. Delivery by episode mapping.

`main-image-production-table.md` required top-level sections:
1. Project Summary
2. Key Character Identity Anchor Table
3. Global Asset State Task Table
4. Episode Asset Usage Mapping Tables
5. Manual Review / Blocked Items
6. Generation Notes

`main-image-review-table.md` required top-level sections:
1. 项目概览
2. 角色身份锚点（短表）
3. 分集使用映射

Do not include `全局资产状态任务（短表）` in `main-image-review-table.md`.
Do not include full prompts, negative prompts, locked identity prompts, state delta prompts, edit instructions, or long global task rows in `main-image-review-table.md`.
Use the machine table as the source of truth for those fields.
The review table is a projection, not a second production pass.

## Project Summary

Keep short. Include:
- project title
- source scope
- total episodes/scenes processed
- total global asset-state tasks
- total episode mapping rows
- counts by asset type
- counts by `task_type`
- unresolved manual review count

Example:

```markdown
# 主图生产总表

## 项目概览
| 项目 | 剧集范围 | 全局任务数 | 每集映射行 | 人物 | 场景 | 道具 | 待人工确认 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 项目名 | E01-E40 | 36 | 214 | 12 | 12 | 12 | 3 |
```

In `main-image-review-table.md`, this section is the same concept but may use fewer columns. Keep it short enough to read without horizontal scrolling.

## Key Character Identity Anchor Table

This table must appear before any character state task that depends on it.

It is not only an art-review summary. It is the identity source of truth for downstream character state generation.

Include only:
- S-level characters
- recurring A-level characters
- user-requested key characters

Required fields:
- `base_asset_id`
- `display_name`
- `priority`
- `identity_anchor_task_id`
- `identity_anchor_prompt`
- `identity_negative_prompt`
- `identity_reference_image`: approved image path/URL/task reference, or `pending`
- `identity_lock_status`: `pending`, `generated`, `approved`, `manual_review`, or `blocked`
- `stable_face_identity`
- `variable_state_axes`
- `review_focus`

Wardrobe in this table is auxiliary unless it is a permanent identity costume. The locked identity is primarily face/casting identity.

For `main-image-review-table.md`, use a short-form identity anchor table. Include only review fields such as:
- `角色`
- `等级`
- `anchor_task_id`
- `身份锚点`
- `可变状态轴`
- `审核重点`

Do not include `identity_anchor_prompt` or `identity_negative_prompt` in the human review file.

## Global Asset State Task Table

This is the production source of truth.

Every production-relevant character, scene, and prop state must appear here once. Do not repeat the same `state_asset_id` as multiple independent generation tasks unless the split is explicit and justified.

Required columns:
- `task_id`
- `task_type`
- `asset_type`
- `base_asset_id`
- `state_asset_id`
- `资产 / 状态`
- `等级`
- `首次需求集/场`
- `使用集数`
- `使用场次`
- `生成来源`
- `reference_task_id`
- `reference_image`
- `reuse_from_task_id`
- `主图提示词 / 编辑指令`
- `负面提示词`
- `剧情依据 / 功能`
- `材质重点`
- `审核重点`
- `状态`

Allowed `task_type` values:
- `text_to_image`: create the first image for a character, scene, or prop state from text.
- `image_text_edit`: create a new character state from an approved identity/reference image plus state delta text.
- `reuse_existing`: do not generate a new image; reuse an existing task/image.
- `blocked`: cannot proceed because required evidence or reference image is missing.
- `manual_review`: evidence, identity, state split, or production choice needs human confirmation.

For character edit tasks, also include:
- `generation_mode`
- `identity_anchor_task_id`
- `locked_identity_prompt`
- `state_delta_prompt`
- `edit_instruction`
- `identity_change_allowed`
- `identity_change_reason`

Task field rules:
- `text_to_image` rows must include copy-ready `prompt` and `negative_prompt`.
- `image_text_edit` rows must include `reference_image`, `locked_identity_prompt`, `state_delta_prompt`, and `edit_instruction`.
- `reuse_existing` rows must not contain a new prompt; they must include `reuse_from_task_id`.
- `blocked` rows must state the blocking reason.
- `manual_review` rows must state what needs human confirmation.

## Episode Asset Usage Mapping Tables

This section answers: "What character, scene, and prop states does each episode use?"

It is produced by joining episode usage rows to the Global Asset State Task Table through `state_asset_id` and `task_id`.

Every episode usage row must include:
- `episode_id`
- `scene_ids`
- `asset_type`
- `asset_state`
- `state_asset_id`
- `task_id`
- `task_type`
- `usage_type`: `new_generation`, `image_text_edit`, `reuse_existing`, `blocked`, or `manual_review`
- `reference_task_id`
- `reuse_from_task_id`
- `episode_function`
- `notes`

Recommended columns:
- `资产类型`
- `资产 / 状态`
- `使用场次`
- `state_asset_id`
- `task_id`
- `task_type`
- `usage_type`
- `reference_task_id`
- `reuse_from_task_id`
- `本集功能`
- `备注`

Example:

```markdown
### E06 资产使用映射表
| 资产类型 | 资产 / 状态 | 使用场次 | state_asset_id | task_id | task_type | usage_type | reference_task_id | reuse_from_task_id | 本集功能 | 备注 |
|---|---|---|---|---|---|---|---|---|---|---|
| character | 陈北--外观（朴素正装）状态 | E06-S001,E06-S003 | char_chenbei_plain_suit | CH-CHENBEI-002 | reuse_existing | reuse_existing | CH-CHENBEI-ANCHOR | CH-CHENBEI-002 | 延续主角身份 | 不重复生成 |
| scene | 陈北酒厂--初始（日间生产）状态 | E06-S002 | scene_winery_day_work | SC-WINERY-001 | reuse_existing | reuse_existing |  | SC-WINERY-001 | 生产空间 | 复用已生成场景 |
| prop | 转让协议--初始（盖章签字）状态 | E06-S001 | prop_transfer_contract_signed | PR-CONTRACT-003 | text_to_image | new_generation |  |  | 剧情证据 | 需生成 |
```

Do not create prompts in episode mapping rows by rethinking the episode. Copy or reference fields from the Global Asset State Task Table.

If a later episode uses the same visual state, map it to the existing `task_id` and mark `usage_type: reuse_existing`.

If a later episode needs a new visible character state, map it to a global `image_text_edit` task and include the reference task/image from the global table.

For `main-image-review-table.md`, this is the main review section. Keep only human-checkable mapping fields, such as:
- `场次`
- `资产类型`
- `资产 / 状态`
- `state_asset_id`
- `task_id`
- `usage_type`
- `备注`

Do not add prompt columns to episode mapping rows in the human review file.

## Prompt Cell Rules

Prompt/edit cells must be copy-ready where the row is generation-ready.

They may be long, but should not include:
- unresolved bracket placeholders
- full biography text
- audit commentary
- pipeline notes
- unsupported visual invention

If markdown table cells become too hard to read, use block format under the global task row. Keep the `task_id` and `state_asset_id` visible.

## Manual Review / Blocked Items

Include a compact section for items that should not silently proceed.

Columns:
- `task_id`
- `state_asset_id`
- `资产 / 状态`
- `task_type`
- `问题`
- `影响`
- `建议处理`

Use for:
- evidence gaps
- conflicts
- uncertain aliases
- uncertain state splits
- missing identity/reference images
- flashback / timeline uncertainty
- blocked prompt or edit tasks

## Generation Notes

Add only practical notes:
- image ratios used
- B/C asset handling
- reference image requirements
- that final delivery is MD-only
- any known limitations

Do not include long pipeline explanations.

## Language Rules

Use Chinese for:
- table labels
- evidence summaries
- review focus
- manual review notes
- compact biographies

Use English for final image prompts when it improves model output.

Do not leave Chinese bracket placeholders inside English prompts unless the user specifically wants template prompts instead of final prompts.

## Output Validation

Before final delivery:
- final output includes `main-image-production-table.md`
- final output includes `main-image-review-table.md`
- final output does not require `prompt-manifest.json`
- Key Character Identity Anchor Table appears before dependent character edit tasks
- Global Asset State Task Table exists
- Episode Asset Usage Mapping Tables exist
- `main-image-production-table.md` includes the Global Asset State Task Table
- `main-image-review-table.md` does not include a Global Asset State Task Table or full prompt cells
- `main-image-review-table.md` includes only Project Summary, short Key Character Identity Anchor Table, and Episode Asset Usage Mapping
- `main-image-review-table.md` is derived from the machine table and does not change machine-table task counts, state splits, task types, blocked statuses, or episode mapping row counts
- every production-relevant state has a stable `task_id`
- every episode mapping row has `state_asset_id` and `task_id`
- every episode mapping row joins to a global task row
- every used character, scene, and prop state appears in episode mapping, including reused assets
- generation task rows are not duplicated just to show episode reuse
- `reuse_existing` rows do not contain new prompts
- `image_text_edit` rows have a reference image and state delta
- final prompts/edit instructions have no unresolved placeholders
- manual review items are compact and actionable
- no API secrets are included

## Acceptance Checklist

Before leaving this layer:
- final output does not expose process artifacts as deliverables
- machine table is complete enough for AI/downstream parsing
- human review table is readable and complete for art review
- global task table and episode mapping tables are aligned
- prompts/edit instructions are copy-ready when status is ready
- every episode has usage mapping rows
- reused assets are visible without duplicate prompts
- no JSON manifest is required by default
- no secrets are included
