---
name: aigc-art-main-image-pipeline-v3-0
description: "当 Codex 需要读取中文剧本、小说草稿、分集短剧脚本或项目剧本文档，并为人物、场景、道具生成忠于剧本证据的 AIGC 主图资产任务时使用本技能。V3.0 输出机器长表、Seedance JSON 和人审 DOCX；提示词为中文 core prompt，等待中台拼接风格前缀；可见 C 级角色独立生成 text_to_image 任务，不再合并成模板。"
---

# AIGC 主图资产生成流程 V3.0

把中文剧本转换为人物、场景、道具主图生产任务，并从完成后的机器长表派生中台导入 JSON 和人审 DOCX。

## 默认交付

- `main-image-production-table.md`：完整机器长表，唯一 source-of-truth。
- `prompt-manifest.json`：Seedance 中台导入 JSON；`imagePrompt` 存放等待中台拼接风格前缀的中文 core prompt。
- `main-image-review-table.docx`：从机器长表派生的人审 DOCX。

## 执行顺序

1. 先读 `framework/workflow.md`。
2. 按 workflow 的模块和层级顺序执行。
3. 每一层只读取该层列出的规则、模板、守卫、契约和脚本。

第三模块固定顺序：

```text
output-contracts -> json-manifest-generation -> review-docx-generation -> final-quality
```

## 三大模块

| 模块 | 层级范围 | 作用 |
|---|---|---|
| 剧本解析与资产识别 | `script-intake` 到 `episode-usage-map` | 建立场次事实、三类证据账本、候选资产、污染清洗、S/A/B/C 评级、注册表、S/A 状态、人物去向、任务草稿和分集映射。 |
| 资产生产与提示词生成 | `character-anchor` 到 `prompt-generation` | 建立角色锚点，审计生产风险，生成中文 core prompt 或中文状态编辑指令。 |
| 输出交付与质检 | `output-contracts` 到 `final-quality` | 输出机器长表，投影 JSON，派生人审 DOCX，并做最终契约验收。 |

## 全局硬边界

- 证据、候选、评级、注册、状态、任务、映射、提示词、JSON、DOCX 各层职责不得互相替代。
- 评级必须发生在状态拆分之前；`asset-rating.md` 是唯一 S/A/B/C 评级层。
- 状态拆分只覆盖 S/A 资产；B/C 不进入状态索引、状态线索去向或状态任务。
- 可见 C 级角色不得合并成模板；保留为生产资产时必须有独立 `text_to_image` 任务。
- `prompt-generation.md` 只输出中文 core prompt，不生成题材世界段、画法段或风格前缀。
- 风格前缀的选择、存储和拼接属于中台或外部提交流程；本技能不自动选风格、不读取风格文件、不把风格前缀拼进 JSON。
- `output-contracts.md` 只输出机器长表；JSON 和 DOCX 都只能从完成后的机器长表派生。
- `final-quality.md` 只检查最终契约，不抽取、不评级、不补任务、不补 JSON 或 DOCX 字段。

## 资源导航

- 全流程、模块和层级输入输出：`framework/workflow.md`
- 层级职责：`framework/layers/*.md`
- 业务判断规则：`references/rules/*.md`
- 提示词、机器长表、DOCX、JSON 模板：`references/templates/*.md`
- 质量守卫：`references/guards/*.md`
- JSON 外部契约：`references/json-contracts/*`
- 确定性脚本：`scripts/*.py`

详细硬规则不要复制到入口页；执行时按 workflow 进入对应层级，再读取该层指定的规则、模板、守卫和脚本。
