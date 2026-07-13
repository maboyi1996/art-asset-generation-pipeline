# json-manifest-generation.md

## 作用

读取 `artifact-manifest.json` 登记的 `production-source/main-image-production-table.md`，将已确认生产任务确定性投影为 Seedance 中台导入文件 `deliverables/prompt-manifest.json`。

V3.1.1 中 `prompt-manifest.json` 的 `assets[].appearance.appearances[].imagePrompt` 存放中文 core prompt，即等待中台拼接风格前缀的基础提示词。

## 输入

`artifact-manifest.json`、manifest 中 `id: main-image-production-table` 且 `role: production_source` 的生产源表，以及用户明确提供的 `contentId`、项目名或其他导入元信息。

## 调用文件

- `references/rules/中台JSON输出规则.md`
- `references/templates/prompt-manifest-json模板.md`
- `references/json-contracts/artifact-manifest-v1-contract.md`
- `references/json-contracts/artifact-manifest.v1.schema.json`
- `references/json-contracts/seedance-element-extract-manifest-v1-contract.md`
- `references/json-contracts/seedance-element-extract-manifest.v1.schema.json`
- `scripts/generate_prompt_manifest.py`

## 输出结果

`deliverables/prompt-manifest.json`

## 边界

本层只做生产源表到 JSON 的确定性投影，不重新抽取资产、不重新评级、不重新拆状态、不补建任务、不改写提示词、不拼接风格前缀、不读取画风 MD、不修改 `production-source/main-image-production-table.md` 或 `deliverables/main-image-review-table.docx`。

本层不得读取 `audit/` 文件来补 `base_asset_id`、`state_asset_id`、提示词、锚点引用、分集映射或审核状态。manifest 如果把 `audit/` 路径登记为 JSON 生产输入，脚本必须失败。

如果生产源表缺少 `base_asset_id`、`state_asset_id`、提示词、锚点引用、合法枚举或必要分集/状态引用，本层必须失败并指回拥有层，不得临时拼接 ID、臆造字段或静默降级。

`prompt-manifest.json` 是中台导入主交付，但不是生产源表的替代品；JSON 不得承载完整 evidence ledger、污染清洗记录、人物候选去向台账或人审 DOCX 内容。

如果生产源表中的 `prompt` 或 `edit_instruction` 含有 `{{include:...}}`、`【A. 题材世界】`、`【B. 画法】`、旧英文写实模板残留或非中文核心提示词，本层必须失败并指回 `prompt-generation.md` 和 `render_core_prompts.py`。
