# 中台 JSON 质量守卫

## 目的

检查 `deliverables/prompt-manifest.json` 是否符合 Seedance 元素库导入契约。

本守卫只检查 JSON 文件、字段、结构、枚举、引用和审计状态，不重新抽取资产、不重新拆状态、不重新评级、不补任务、不重写提示词。

## 必查项

- 是否输出真实文件 `deliverables/prompt-manifest.json`。
- `artifact-manifest.json` 是否把该文件登记为 `role: deliverable`。
- JSON 是否由 manifest 登记的 `production-source/main-image-production-table.md` 投影生成。
- 文件内容是否为纯 JSON 对象，不是数组、Markdown、JSON5 或带注释文本。
- `schemaVersion` 是否固定为 `seedance-element-extract-manifest.v1`。
- `assets` 是否存在且为非空数组。
- 是否使用 `assets` 作为唯一主结构；不得把旧版 `items/main_image_tasks/asset_state_tasks/roleList/sceneList/propList` 作为主交付结构。
- 每个 `assets[]` 是否有 `templateName`、`templateType`、`appearance.appearances`。
- `templateType` 是否只使用 `ROLE`、`SCENE`、`PROP`。
- 每个 `appearance.appearances[]` 是否有 `name` 和 `imagePrompt`。
- 每个 `imagePrompt` 是否为中文 core prompt 或中文状态编辑 core instruction。
- 每个 `imagePrompt` 是否不包含 `{{include:...}}`、`【A. 题材世界】`、`【B. 画法】`、风格前缀或旧英文写实模板残留。
- `contentId` 如存在是否为字符串，不得输出大整数 JSON number。
- `priority` 如存在是否只使用 `S/A/B/C`。
- `generation.method` 如存在是否只使用 `text_to_image`、`image_to_image`、`image_text_edit`。
- `text_to_image` 状态是否有 `imagePrompt` 和中文 `negativePrompt`。
- `image_text_edit` 状态是否有 `imagePrompt`、中文 `negativePrompt` 和 `generation.referenceTaskId`。
- `episodes` 如存在是否为正整数数组，不得输出字符串集号。
- `assets[].assetId` 是否能回溯到 `global-asset-registry.base_asset_id`。
- `appearances[].stateId` 是否能回溯到 `state-variant-result.state_asset_id` 或生产任务 `task_id`。
- 同一 base asset 是否只出现一个 JSON asset；多状态必须合并到同一个 `appearance.appearances[]`。
- B/C 是否只输出基础 appearance；不得存在 B/C 多状态、B/C `image_text_edit` 状态链路或 B/C 状态人工复核。
- `review_status: excluded` 的任务是否没有进入 `deliverables/prompt-manifest.json`。
- `manual_review_required` 的 appearance 是否保留 `status: manual_review_required`，并有 `reviewFocus` 或 `metadata.reviewReason`。
- `summary.totalItems` 是否等于 `assets.length`。
- `summary.manualReviewItems` 是否等于 `manual_review_required` appearance 数量。
- `production-audit-result` 是否仍有 `severity: blocking`；如有，不得将 JSON 标记为可导入。

## 非阻断项

- `description`、`appearance.description`、`metadata` 字段缺少时不自动阻断，除非会导致导入关键字段缺失。
- 未提供 `contentId` 不阻断；不得为通过检查而臆造。
- 不因 B/C 状态线索没有进入 JSON 多状态而阻断。

## 失败处理

发现 JSON 缺文件、非 JSON、schema 必填字段缺失、枚举非法、导入主结构错误、任务引用断链、B/C 进入多状态、core prompt 不合格或 `production-audit-result` 仍有 blocking 时，返回对应拥有层修复，不在最终质检层重写结果。
