# final-quality.md

## 作用

检查 `prompt-manifest.json` 和最终两张 Markdown 是否符合 V2.63 输出契约。

## 输入

`prompt-manifest.json`、`main-image-production-table.md`、`main-image-review-table.md`、`production-audit-result`

## 调用文件

- `references/guards/输出质量守卫.md`
- `references/guards/中台JSON质量守卫.md`
- `scripts/validate_prompt_manifest.py`

## 输出结果

`final-quality-report`

## 边界

只做最终交付验收：检查 JSON 文件是否存在且符合导入契约、Markdown 章节是否完整、字段是否符合模板、机器长表、人审短表和 JSON 是否分工正确、`production-audit-result` 是否仍有 blocking。不得重新做资产抽取、状态拆分、评级、人物去向补写、污染标签补写、任务补建、分集映射生成、提示词生成或 JSON 字段补造。
