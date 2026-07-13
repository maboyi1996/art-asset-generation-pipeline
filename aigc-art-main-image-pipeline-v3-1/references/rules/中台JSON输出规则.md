# 中台 JSON 输出规则

## 规则目的

本文件只用于 `json-manifest-generation.md` 通过 `artifact-manifest.json` 读取完成后的 `production-source/main-image-production-table.md`，并投影为 Seedance 元素库导入文件 `deliverables/prompt-manifest.json`。

本规则解决的唯一问题是：

> 如何把 V3.1 production source 中已确认的角色、场景、道具主图任务转换为中台可导入的 JSON 结构？

本文件不重新抽取资产、不重新评级、不重新拆状态、不补建任务、不重写提示词、不拼接风格前缀、不修复审计问题、不修改 Markdown 或 DOCX。

## 输入依据

必须先读取：

- `artifact-manifest.json`

再从 manifest 中读取：

- `production-source/main-image-production-table.md`

生产源表中至少要能读取以下章节：

- 项目概览
- 全局资产注册表
- 状态索引表
- 全局生产任务表
- 分集使用映射表
- 生产审计摘要

可读取用户提供的 `contentId`、项目名或其他导入元信息。没有明确提供时，不得臆造业务 ID；可省略可选字段。

## 输出结果

输出文件固定路径为：

- `deliverables/prompt-manifest.json`

JSON 必须符合 `references/json-contracts/seedance-element-extract-manifest.v1.schema.json`，并遵守 `references/json-contracts/seedance-element-extract-manifest-v1-contract.md`。

根节点必须是对象，不得是数组。不得输出 Markdown 代码块、注释、JSON5 语法或尾随逗号。

## 根字段

| JSON 字段 | 规则 |
|---|---|
| `schemaVersion` | 固定为 `seedance-element-extract-manifest.v1`。 |
| `manifestVersion` | 固定为 `1.0`，除非用户要求更高 manifest 版本。 |
| `generationScope` | 固定为 `main_image_only`。 |
| `contentId` | 仅在用户或上游输入明确提供时输出；必须是字符串。 |
| `source.skillId` | 固定为 `aigc-art-main-image-pipeline-v3-1`。 |
| `source.skillVersion` | 固定为 `3.1`。 |
| `source.generatedAt` | 使用生成时的 ISO 8601 时间字符串，包含时区。 |
| `project.title` | 来自项目概览或用户提供项目名；不确定时可省略。 |
| `summary.totalItems` | `assets.length`。 |
| `summary.manualReviewItems` | `assets[].appearance.appearances[]` 中 `status: manual_review_required` 的状态数量。 |
| `assets` | 必填，使用统一元素结构；不得使用旧版 `items/main_image_tasks/asset_state_tasks/roleList/sceneList/propList` 作为主结构。 |

## 资产映射

`assets[]` 每一项对应一个已注册 base asset，而不是一个任务行。

| 生产源表来源 | JSON 字段 | 规则 |
|---|---|---|
| `全局资产注册表.base_asset_id` 或 `全局生产任务表.base_asset_id` | `assetId` | 优先使用稳定 base asset ID。无法唯一匹配时必须阻断，不得临时拼接。 |
| `全局资产注册表.asset_name` 或 `全局生产任务表.asset_name` | `templateName` | 使用注册后的规范资产名。 |
| `asset_type: character` | `templateType` | `ROLE`。 |
| `asset_type: scene` | `templateType` | `SCENE`。 |
| `asset_type: prop` | `templateType` | `PROP`。 |
| 注册说明、提示词摘要或证据摘要 | `description` | 用于人看懂元素，不承担导入关键字段。 |
| 注册说明、提示词摘要或默认外观描述 | `appearance.description` | 描述该元素整体外观。 |
| 任务和证据回溯 | `metadata` | 可放 `source: agent`、`taskIds`、`firstAppearance`、`evidenceSummary`、`reviewReason` 等审计信息。 |

同一个 base asset 的基础图和 S/A 状态图必须合并为同一个 `assets[]` 元素，并将不同视觉状态放入 `appearance.appearances[]`。不得因为多状态把同一个角色、场景或道具拆成多个 JSON 元素。

## 状态映射

`appearance.appearances[]` 每一项对应一条可生成的主图任务。

只输出 `review_status: ready` 或 `manual_review_required` 且具备可用正向内容的任务。`review_status: excluded` 的任务不得进入 `prompt-manifest.json`。

| 生产源表来源 | JSON 字段 | 规则 |
|---|---|---|
| `全局生产任务表.state_asset_id` 或 `全局生产任务表.task_id` | `stateId` | 状态任务优先使用 `state_asset_id`；基础任务使用稳定 `task_id`。 |
| `state_name` | `name` | 无拆分基础任务写 `默认状态` 或生产表中的默认状态名；状态任务写状态名。 |
| `episode_id` 和 `分集使用映射表` | `episodes` | 输出正整数数组；无法可靠解析为集数时省略，不写字符串集号。 |
| `asset_type` | `imageRatio` | 角色默认 `9:16`，场景默认 `16:9`，道具默认 `1:1`。 |
| `prompt` 或 `edit_instruction` | `imagePrompt` | `text_to_image` 使用中文 core prompt；`image_text_edit` 使用中文状态编辑 core instruction。不得拼接风格前缀。 |
| `negative_prompt` | `negativePrompt` | 直接映射中文负向约束。 |
| `priority_level` | `priority` | 只能是 `S/A/B/C`。 |
| `review_status` | `status` | 直接使用 `ready` 或 `manual_review_required`。 |
| `task_type` | `generation.method` | `text_to_image` 或 `image_text_edit`。 |
| `review_focus` | `reviewFocus` | 直接映射。 |

`image_text_edit` 状态任务必须在 `generation` 内保留锚点引用：

- `referenceTaskId`: 来自 `anchor_task_id`。
- `referenceAssetId`: 能由锚点任务回溯到 base asset 时填写。
- `referenceStateId`: 能由锚点任务回溯到基础或锚点状态时填写。
- `referenceAppearanceName`: 能确认锚点状态名时填写。

不得为缺失锚点的 `image_text_edit` 任务生成可导入 JSON；应由 `production-audit.md` 或 `final-quality.md` 阻断。

## B/C 状态边界

沿用 V2.63 状态规则：B/C 资产不得进入状态层。

- B/C 基础资产可作为 JSON 元素输出。
- B/C 基础图可作为 `appearance.appearances[]` 中的默认状态输出。
- B/C 不得拥有状态任务、`image_text_edit` 状态链路或状态人工复核记录。
- B/C 的服装、伤病、脏污、血迹、空间或物体条件变化不得作为 JSON 多状态输出。

## 人工复核状态

`manual_review_required` 任务可以进入 `prompt-manifest.json`，但必须：

- 保留 `status: manual_review_required`。
- 填写 `reviewFocus` 或在 `metadata.reviewReason` 中说明原因。
- 仍然具备可用 `imagePrompt` 和 `negativePrompt`。

仍有 `severity: blocking` 的 `production-audit-result` 时，不得交付可导入的最终 `prompt-manifest.json`。

## 脚本化要求

`json-manifest-generation.md` 应调用 `scripts/generate_prompt_manifest.py --artifact-manifest artifact-manifest.json` 执行确定性投影。脚本失败时，不得改由模型手工补造 JSON；必须返回对应生产源表或上游拥有层修复。

V3.1 中脚本必须拒绝：

- `{{include:...}}`
- `【A. 题材世界】`
- `【B. 画法】`
- 旧英文写实模板残留
- 非中文 core prompt
- 缺失 `negative_prompt`
- 缺失 `artifact-manifest.json`
- manifest 未登记 `main-image-production-table`
- manifest 将 `audit/` 路径登记为 JSON 生产源

## 边界

- 不新增 JSON 合同之外的必填字段。
- 不输出旧版兼容结构作为主结构。
- 不把 evidence ledger、污染清洗、人物候选去向或人审 DOCX 内容塞进 JSON。
- 不把 `excluded` 任务放入 `assets[].appearance.appearances[]`。
- 不把 Markdown 表格字段名原样当成 JSON 字段。
- 不改变 `production-source/main-image-production-table.md` 或 `deliverables/main-image-review-table.docx` 的内容来迎合 JSON。

只使用以上列举过的字段和职责。
