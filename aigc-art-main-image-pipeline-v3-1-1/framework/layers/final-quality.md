# final-quality.md

## 作用

检查 `artifact-manifest.json`、`production-source/main-image-production-table.md`、`deliverables/prompt-manifest.json` 和 `deliverables/main-image-review-table.docx` 是否符合 V3.1.1 输出契约。

## 输入

`artifact-manifest.json`、manifest 登记的 production source、manifest 登记的 deliverables、`audit/production-audit-result.md`

## 调用文件

- `references/guards/输出质量守卫.md`
- `references/guards/中台JSON质量守卫.md`
- `references/json-contracts/artifact-manifest.v1.schema.json`
- `scripts/validate_artifact_manifest.py`
- `scripts/validate_core_prompt_slots.py`
- `scripts/validate_production_source.py`
- `scripts/validate_prompt_manifest.py`
- `scripts/validate_review_docx.py`

## 输出结果

`deliverables/final-quality-report.md`

## 边界

只做最终交付验收：检查 manifest 是否完整、audit/production-source/deliverables 分工是否正确、生产源表章节和字段是否完整、JSON 文件是否存在且符合导入契约、DOCX 是否存在且符合人审模板、`audit/production-audit-result.md` 是否仍有 blocking。

不得重新做资产抽取、状态拆分、评级、人物去向补写、污染标签补写、任务补建、分集映射生成、提示词生成、JSON 字段补造或 DOCX 表格补造。

JSON 和 DOCX 都必须从 manifest 登记的 `production-source/main-image-production-table.md` 派生，不得从 `audit/` 或旧长表派生。终检发现问题时只能报告并指回拥有层修复。
