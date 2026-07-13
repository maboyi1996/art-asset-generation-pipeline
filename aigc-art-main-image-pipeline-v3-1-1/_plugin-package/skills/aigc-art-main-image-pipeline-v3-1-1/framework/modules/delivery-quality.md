# 模块：输出交付与质检

## 作用

生成瘦生产源表，从 manifest 登记的生产源投影生成中台导入 JSON，从同一生产源派生人审 DOCX，并检查最终交付是否符合 V3.1.1 输出契约。

## 层级顺序

`output-contracts.md -> json-manifest-generation.md -> review-docx-generation.md -> final-quality.md`

## 边界

本模块只交付、投影、派生和验收，不重新做资产判断，不让 JSON 或人审 DOCX 反向改变生产源表。

- `output-contracts.md` 只输出 `production-source/main-image-production-table.md`。
- `json-manifest-generation.md` 只通过 `artifact-manifest.json` 读取生产源表并输出 `deliverables/prompt-manifest.json`。
- `review-docx-generation.md` 只通过 `artifact-manifest.json` 读取生产源表并输出 `deliverables/main-image-review-table.docx`。
- `final-quality.md` 只检查 manifest、文件、章节、字段、JSON 结构、DOCX 结构和断链审计结果，不重新执行上游业务规则。
