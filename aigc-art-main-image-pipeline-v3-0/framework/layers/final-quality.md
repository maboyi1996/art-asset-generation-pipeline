# final-quality.md

## 作用

检查 `prompt-manifest.json`、`main-image-production-table.md` 和 `main-image-review-table.docx` 是否符合 V3.0 输出契约。

## 输入

`prompt-manifest.json`、`main-image-production-table.md`、`main-image-review-table.docx`、`production-audit-result`

## 调用文件

- `references/guards/输出质量守卫.md`
- `references/guards/中台JSON质量守卫.md`
- `scripts/validate_prompt_manifest.py`
- `scripts/validate_review_docx.py`

## 输出结果

`final-quality-report`

## 边界

只做最终交付验收：检查机器长表章节和字段是否完整、JSON 文件是否存在且符合导入契约、DOCX 是否存在且符合人审模板、三者分工是否正确、`production-audit-result` 是否仍有 blocking。

不得重新做资产抽取、状态拆分、评级、人物去向补写、污染标签补写、任务补建、分集映射生成、提示词生成、JSON 字段补造或 DOCX 表格补造。

JSON 和 DOCX 都必须从完成后的机器长表派生，不得反向修改机器长表。终检发现问题时只能报告并指回拥有层修复。
