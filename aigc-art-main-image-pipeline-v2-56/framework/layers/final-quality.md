# final-quality.md

## 作用

检查最终两张 Markdown 是否符合 V2.56 输出契约。

## 输入

`main-image-production-table.md`、`main-image-review-table.md`、`production-audit-result`、`polluted-label-cleanup-ledger`

## 调用文件

`references/guards/输出质量守卫.md`

## 输出结果

`final-quality-report`

## 边界

只做最终验收，不重新做资产抽取、状态拆分、评级、人物去向补写、污染标签补写、任务补建或提示词生成。通过机器长表章节、`polluted-label-cleanup-ledger` 和 `production-audit-result` 检查人物候选去向闭环、污染标签清洗闭环、全局生产任务完整性和提示词完整性。
