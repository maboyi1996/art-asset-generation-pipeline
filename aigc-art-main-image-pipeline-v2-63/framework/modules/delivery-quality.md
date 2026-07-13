# 模块：输出交付与质检

## 作用

生成完整机器长表和派生人审短表，从机器长表投影生成中台导入 JSON，并检查最终交付是否符合 V2.63 输出契约。

## 层级顺序

`output-contracts.md -> json-manifest-generation.md -> final-quality.md`

## 边界

本模块只交付、投影和验收，不重新做资产判断，不让 JSON 或人审短表反向改变机器长表。JSON 生成层只读取机器长表并输出 `prompt-manifest.json`；最终质检只检查文件、章节、字段、JSON 结构和断链审计结果，不重新执行上游业务规则。
