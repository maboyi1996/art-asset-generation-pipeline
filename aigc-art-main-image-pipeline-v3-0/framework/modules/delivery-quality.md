# 模块：输出交付与质检

## 作用

生成完整机器长表，从机器长表投影生成中台导入 JSON，从机器长表派生人审 DOCX，并检查最终交付是否符合 V3.0 输出契约。

## 层级顺序

`output-contracts.md -> json-manifest-generation.md -> review-docx-generation.md -> final-quality.md`

## 边界

本模块只交付、投影、派生和验收，不重新做资产判断，不让 JSON 或人审 DOCX 反向改变机器长表。

- `output-contracts.md` 只输出 `main-image-production-table.md`。
- `json-manifest-generation.md` 只读取机器长表并输出 `prompt-manifest.json`。
- `review-docx-generation.md` 只读取机器长表并输出 `main-image-review-table.docx`。
- `final-quality.md` 只检查文件、章节、字段、JSON 结构、DOCX 结构和断链审计结果，不重新执行上游业务规则。
