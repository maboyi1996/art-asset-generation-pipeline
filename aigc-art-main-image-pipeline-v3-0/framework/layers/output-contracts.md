# output-contracts.md

## 作用

将三类评级前证据账本、全局注册、别名、S/A 状态、候选去向、模板覆盖、污染清洗、带中文 core prompt 的任务、分集映射和审计结果整理成最终机器长表。

## 输入

`script-intake-result`、`character-evidence-ledger`、`scene-evidence-ledger`、`prop-evidence-ledger`、`global-asset-registry`、`alias-resolution-map`、`state-variant-result`、`state-clue-disposition-ledger`、`character-disposition-ledger`、`generic-template-coverage-ledger`、`polluted-label-cleanup-ledger`、`prompted-production-task-table`、`episode-usage-map-draft`、`production-audit-result`、`character-anchor-result`

## 调用文件

- `references/rules/任务类型字段审核规则.md`
- `references/rules/分集映射规则.md`
- `references/templates/机器长表模板.md`

## 输出结果

`main-image-production-table.md`

## 边界

机器长表是唯一完整 source-of-truth，必须包含三类评级前证据账本、注册、别名、S/A 状态索引、S/A 状态线索去向、人物候选去向、泛称/群体模板覆盖、污染清洗、全局生产任务、分集映射和生产审计摘要。全局生产任务表必须保留 `base_asset_id` 和 `state_asset_id`，供 JSON 生成层稳定投影。

本层不得输出 `prompt-manifest.json`，不得输出 `main-image-review-table.docx`，不得为迎合 JSON 或 DOCX 改写任务、状态、评级、提示词或分集映射。

`prompt` 字段写中文 core prompt，`edit_instruction` 字段写中文状态编辑 core instruction，`negative_prompt` 字段写中文负向约束。core prompt 不得包含题材世界段、画法段、风格库前缀、`{{include:...}}` 或旧英文写实模板残留。

JSON 只由 `json-manifest-generation.md` 在读取完成后的机器长表后生成。DOCX 只由 `review-docx-generation.md` 在读取完成后的机器长表后生成。
