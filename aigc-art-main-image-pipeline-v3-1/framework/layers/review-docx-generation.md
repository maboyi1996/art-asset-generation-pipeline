# review-docx-generation.md

## 作用

读取 `artifact-manifest.json` 登记的 `production-source/main-image-production-table.md`，将已确认生产任务和分集映射确定性派生为人审文件 `deliverables/main-image-review-table.docx`。

## 输入

`artifact-manifest.json`、manifest 中 `id: main-image-production-table` 且 `role: production_source` 的生产源表。

## 调用文件

- `references/templates/人审DOCX表格模板.md`
- `references/json-contracts/artifact-manifest-v1-contract.md`
- `scripts/generate_review_docx.py`

## 输出结果

`deliverables/main-image-review-table.docx`

## 边界

本层只做生产源表到 DOCX 人审表的确定性派生，不重新抽取资产、不重新评级、不重新拆状态、不补建任务、不改写提示词、不修改 `production-source/main-image-production-table.md` 或 `deliverables/prompt-manifest.json`。

本层不得读取 `audit/` 文件来补任务、补集数、补资产名、补状态或补审核状态。manifest 如果把 `audit/` 路径登记为 DOCX 生产输入，脚本必须失败。

DOCX 不得成为生产源表。DOCX 不得反向减少、合并、改名、补建或重算生产源表任务。

DOCX 不输出 `prompt`、`edit_instruction`、`negative_prompt`、完整 core prompt 或风格前缀。图片列只留空白占位，不读取、不复制、不生成图片。

如果生产源表缺少全局生产任务表、分集使用映射表、必要字段、合法 `task_id` 引用或可解析 `episode_id`，本层必须失败并指回拥有层，不得临时补任务、补集数或手工拼表。
