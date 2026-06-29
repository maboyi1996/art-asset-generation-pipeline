# output-contracts.md

## 作用

将带提示词的生产任务表、人物候选去向台账和分集映射草稿整理成最终两张 Markdown。

## 输入

`prompted-production-task-table`、`character-disposition-ledger`、`episode-usage-map-draft`、`production-audit-result`

## 调用文件

- `references/rules/任务类型字段审核规则.md`
- `references/rules/分集映射规则.md`
- `references/templates/机器长表模板.md`
- `references/templates/人审短表模板.md`

## 输出结果

`main-image-production-table.md`、`main-image-review-table.md`

## 边界

机器长表必须包含独立的 `人物候选去向审计表`，但中台生产源表只能是 `全局生产任务表`。人审短表从机器长表派生，可以保留人物候选异常摘要，但不得承载完整 ledger，不得减少、改名、合并、补建或重算机器长表任务。
