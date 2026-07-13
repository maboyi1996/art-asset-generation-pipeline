# artifact-manifest.v1 contract

## 用途

`artifact-manifest.json` 是 V3.1.1 项目输出文件夹的产物总索引。它声明每个文件的角色、路径、生产者、消费者和读取策略，让脚本能确定性找到输入输出。

## 文件位置

`project-output/artifact-manifest.json`

## 根字段

| 字段 | 类型 | 要求 |
|---|---|---|
| `schema_version` | string | 固定为 `aigc-artifact-manifest.v1` |
| `skill_id` | string | 固定为 `aigc-art-main-image-pipeline-v3-1-1` |
| `skill_version` | string | 固定为 `3.1.1` |
| `project_id` | string | 项目唯一 ID |
| `created_at` | string | ISO 时间字符串 |
| `artifacts` | array | 产物登记列表 |

## artifacts 字段

| 字段 | 类型 | 要求 |
|---|---|---|
| `id` | string | 产物稳定 ID，不得重复 |
| `role` | string | `audit`、`production_source`、`deliverable`、`validation_report` |
| `path` | string | 相对 manifest 所在目录的路径 |
| `artifact_type` | string | `markdown`、`markdown_table`、`json`、`docx`、`directory`、`report` |
| `producer` | string | 产出层级或脚本 |
| `consumers` | array | 读取该产物的层级或脚本 |
| `required` | boolean | 正式交付是否必须存在 |
| `read_policy` | string | `audit_only`、`production_source_only`、`deliverable_only`、`validation_only` |

## 固定产物 ID

| id | role | path |
|---|---|---|
| `core-prompt-slots` | `production_source` | `production-source/core-prompt-slots.md` |
| `prompted-production-task-table` | `production_source` | `production-source/prompted-production-task-table.md` |
| `main-image-production-table` | `production_source` | `production-source/main-image-production-table.md` |
| `prompt-manifest` | `deliverable` | `deliverables/prompt-manifest.json` |
| `main-image-review-table` | `deliverable` | `deliverables/main-image-review-table.docx` |
| `final-quality-report` | `validation_report` | `deliverables/final-quality-report.md` |

## 硬性失败规则

脚本必须在以下情况失败：

- manifest 文件不存在。
- 根字段缺失或版本不匹配。
- `artifacts[].id` 重复。
- `path` 是绝对路径。
- `path` 跳出 manifest 所在目录。
- `role`、`artifact_type` 或 `read_policy` 非法。
- 必需产物未登记。
- JSON/DOCX 脚本读取的生产源不是 `role: production_source`。
- 生产源路径位于 `audit/`。
- deliverable 输出路径不在 `deliverables/`。

## 边界

manifest 只声明产物路由，不承载业务判断。它不得替代 evidence ledger、评级、注册、状态拆分、prompt 槽位或 JSON 内容。
