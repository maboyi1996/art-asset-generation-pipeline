# core-prompt-slots 模板

## 文件名

`production-source/core-prompt-slots.md`

## 用途

供 `prompt-generation.md` 输出结构化 prompt 槽位。模型只填写本表，不直接手写整段最终 prompt。

本模板只规定表格结构和字段。`slot_value` 的具体写法、合格细节密度和人物/场景/道具样例，以 `references/rules/core-prompt-slots规则.md` 为准。

## 必须包含章节

```markdown
# core-prompt-slots

## 槽位表

| task_id | asset_type | task_type | base_asset_id | state_asset_id | slot_name | slot_value | slot_status | source_evidence_ids | source_locator | slot_issue |
|---|---|---|---|---|---|---|---|---|---|---|
```

## 字段要求

| 字段 | 要求 |
|---|---|
| `task_id` | 来自 `audit/global-task-draft.md` |
| `asset_type` | `character`、`scene`、`prop` |
| `task_type` | `text_to_image`、`image_text_edit` |
| `base_asset_id` | 来自 `audit/global-asset-registry.md` |
| `state_asset_id` | 状态任务填写；基础任务为空 |
| `slot_name` | 只能使用 `core-prompt-slots规则.md` 定义的槽位 |
| `slot_value` | 中文正向、具体、可画的视觉细节；缺证据时留空 |
| `slot_status` | `ready`、`missing_evidence`、`manual_review_required` |
| `source_evidence_ids` | 证据 ID，多个值用英文逗号分隔 |
| `source_locator` | 剧本或上游产物定位 |
| `slot_issue` | 缺证据或人工复核说明 |

## 输出约束

- 每个 `task_id` 必须具备其 `asset_type` 和 `task_type` 对应的全部必填槽位。
- 一个 `task_id + slot_name` 只能出现一次。
- `slot_status` 为 `missing_evidence` 的必填槽位会导致渲染脚本失败。
- `slot_value` 不得写负向约束、题材世界段、画法段、风格前缀或 `{{include:...}}`。
- `slot_value` 不得只写抽象判断或身份逻辑；必须按 `core-prompt-slots规则.md` 的样例密度写成可画细节。
