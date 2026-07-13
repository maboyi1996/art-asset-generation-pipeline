# json-manifest-generation.md

## 作用

读取完成后的 `main-image-production-table.md`，将机器长表中的已确认生产任务确定性投影为 Seedance 中台导入文件 `prompt-manifest.json`。

## 输入

`main-image-production-table.md`，以及用户明确提供的 `contentId`、项目名或其他导入元信息。

## 调用文件

- `references/rules/中台JSON输出规则.md`
- `references/templates/prompt-manifest-json模板.md`
- `references/json-contracts/seedance-element-extract-manifest-v1-contract.md`
- `references/json-contracts/seedance-element-extract-manifest.v1.schema.json`
- `scripts/generate_prompt_manifest.py`

## 输出结果

`prompt-manifest.json`

## 边界

本层只做机器长表到 JSON 的确定性投影，不重新抽取资产、不重新评级、不重新拆状态、不补建任务、不改写提示词、不修改 `main-image-production-table.md` 或 `main-image-review-table.md`。

如果机器长表缺少 `base_asset_id`、`state_asset_id`、提示词、锚点引用、合法枚举或必要分集/状态引用，本层必须失败并指回拥有层，不得临时拼接 ID、臆造字段或静默降级。

`prompt-manifest.json` 是中台导入主交付，但不是机器长表的替代品；JSON 不得承载完整 evidence ledger、污染清洗记录、人物候选去向台账或人审短表内容。
