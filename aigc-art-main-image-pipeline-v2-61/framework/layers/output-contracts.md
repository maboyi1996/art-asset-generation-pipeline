# output-contracts.md

## 作用

将三类评级前证据账本、全局注册、别名、状态、候选去向、模板覆盖、污染清洗、带提示词任务、分集映射和审计结果整理成最终两张 Markdown。

## 输入

`script-intake-result`、`character-evidence-ledger`、`scene-evidence-ledger`、`prop-evidence-ledger`、`global-asset-registry`、`alias-resolution-map`、`state-variant-result`、`state-clue-disposition-ledger`、`character-disposition-ledger`、`generic-template-coverage-ledger`、`polluted-label-cleanup-ledger`、`prompted-production-task-table`、`episode-usage-map-draft`、`production-audit-result`、`character-anchor-result`

## 调用文件

- `references/rules/任务类型字段审核规则.md`
- `references/rules/分集映射规则.md`
- `references/templates/机器长表模板.md`
- `references/templates/人审短表模板.md`

## 输出结果

`main-image-production-table.md`、`main-image-review-table.md`

## 边界

机器长表是唯一完整 source-of-truth，必须包含三类评级前证据账本、注册、别名、状态索引、状态线索去向、人物候选去向、泛称/群体模板覆盖、污染清洗、全局生产任务、分集映射和生产审计摘要。人审短表从机器长表派生，只保留人审需要的摘要，不得承载完整 ledger，不得减少、改名、合并、补建或重算机器长表任务。
