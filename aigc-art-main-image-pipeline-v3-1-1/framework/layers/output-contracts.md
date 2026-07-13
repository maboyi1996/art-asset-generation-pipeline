# output-contracts.md

## 作用

将全局注册、状态索引、角色锚点、带中文 core prompt 的任务、分集映射和生产审计摘要整理成 `production-source/main-image-production-table.md`。

V3.1.1 的机器表是瘦生产源表，不再承载完整中间审计包。评级前证据账本、候选去向、污染清洗、状态线索去向等中间产物必须保留在 `audit/` 独立文件中，并在 `artifact-manifest.json` 登记。

## 输入

`audit/global-asset-registry.md`、`audit/alias-resolution-map.md`、`audit/state-variant-result.md`、`audit/episode-usage-map-draft.md`、`audit/production-audit-result.md`、`audit/character-anchor-result.md`、`production-source/prompted-production-task-table.md`

## 调用文件

- `references/rules/任务类型字段审核规则.md`
- `references/rules/分集映射规则.md`
- `references/templates/机器长表模板.md`

## 输出结果

`production-source/main-image-production-table.md`

## 边界

本层只汇总 JSON/DOCX 所需的生产字段和最小审计摘要。不得把完整三类 evidence ledger、污染标签清洗记录、人物候选去向审计表、泛称/群体模板覆盖表或状态线索去向表复制进生产源表。

全局生产任务表必须保留 `task_id`、`base_asset_id`、`state_asset_id`、`asset_type`、`priority_level`、`task_type`、`anchor_task_id`、`review_status`、`prompt`、`edit_instruction`、`negative_prompt` 等稳定字段，供 JSON/DOCX 生成层稳定投影。

本层不得输出 `prompt-manifest.json`，不得输出 `main-image-review-table.docx`，不得为迎合 JSON 或 DOCX 改写任务、状态、评级、提示词或分集映射。

`prompt` 字段只能来自 `production-source/prompted-production-task-table.md` 中由脚本渲染的中文 core prompt。`edit_instruction` 字段只能来自脚本渲染的中文状态编辑 core instruction。`negative_prompt` 字段只能来自渲染脚本固定输出或已登记的生产源字段。

core prompt 不得包含题材世界段、画法段、风格库前缀、`{{include:...}}` 或旧英文写实模板残留。

JSON 只由 `json-manifest-generation.md` 在读取 manifest 登记的生产源表后生成。DOCX 只由 `review-docx-generation.md` 在读取同一生产源表后生成。
