---
name: aigc-art-main-image-pipeline-v3-1-1
description: "当 Codex 需要读取中文剧本、小说草稿、分集短剧脚本或项目剧本文档，并为人物、场景、道具生成忠于剧本证据的 AIGC 主图资产任务时使用本技能。V3.1.1 输出 manifest 路由的项目文件夹、分层 audit 产物、production-source 生产源、Seedance JSON 和人审 DOCX；prompt 先填 core-prompt slots，再由脚本确定性渲染；可见 C 级角色独立生成 text_to_image 任务。"
---

# AIGC 主图资产生成流程 V3.1.1

把中文剧本转换为人物、场景、道具主图生产任务，并通过 manifest 路由的项目输出文件夹交付中台 JSON 和人审 DOCX。

## 默认交付

```text
project-output/
├─ artifact-manifest.json
├─ audit/
├─ production-source/
└─ deliverables/
```

- `artifact-manifest.json`：项目产物总索引，声明每个产物的 role、path、producer、consumers、read_policy。
- `audit/`：分层中间证据和审计产物，按层级独立成文件。
- `production-source/`：唯一机器生产源，包含 `core-prompt-slots.md`、`prompted-production-task-table.md`、`main-image-production-table.md`。
- `deliverables/`：最终交付，包含 `prompt-manifest.json`、`main-image-review-table.docx`、`final-quality-report.md`。

## 执行顺序

1. 先读 `framework/workflow.md`。
2. 按 workflow 的模块和层级顺序执行。
3. 每一层只读取该层列出的规则、模板、守卫、契约和脚本。
4. 进入脚本阶段时，优先读取 `artifact-manifest.json` 定位输入输出，不扫描目录、不从 `audit/` 补生产字段。

第三模块固定顺序：

```text
output-contracts -> json-manifest-generation -> review-docx-generation -> final-quality
```

## 三大模块

| 模块 | 层级范围 | 作用 |
|---|---|---|
| 剧本解析与资产识别 | `script-intake` 到 `episode-usage-map` | 建立场次事实、三类证据账本、候选资产、污染清洗、S/A/B/C 评级、注册表、S/A 状态、人物去向、任务草稿和分集映射，并分别写入 `audit/`。 |
| 资产生产与提示词生成 | `character-anchor` 到 `prompt-generation` | 建立角色锚点，审计生产风险，产出 core prompt 槽位表，并由脚本渲染中文 core prompt 或中文状态编辑指令。 |
| 输出交付与质检 | `output-contracts` 到 `final-quality` | 输出瘦生产源表，从生产源投影 JSON，派生人审 DOCX，并做最终契约验收。 |

## 全局硬边界

- 证据、候选、评级、注册、状态、任务、映射、提示词、JSON、DOCX 各层职责不得互相替代。
- 评级必须发生在状态拆分之前；`asset-rating.md` 是唯一 S/A/B/C 评级层。
- 状态拆分只覆盖 S/A 资产；B/C 不进入状态索引、状态线索去向或状态任务。
- 可见 C 级角色不得合并成模板；保留为生产资产时必须有独立 `text_to_image` 任务。
- `prompt-generation.md` 不得手写整段最终 prompt；只能产出 `core-prompt-slots.md`，再由 `scripts/render_core_prompts.py` 确定性渲染。
- 风格前缀的选择、存储和拼接属于中台或外部提交流程；本技能不自动选风格、不读取风格文件、不把风格前缀拼进 JSON。
- `main-image-production-table.md` 是 `production-source/` 下的瘦生产源表，不承载完整中间审计包。
- JSON 和 DOCX 都只能从 `production-source/main-image-production-table.md` 派生，不得从 `audit/` 读取字段补生产结果。
- 所有脚本遇到缺 manifest、错 role、缺字段、非法枚举、槽位缺失或旧产物冲突时必须失败并报错，不得猜测、补造或改写上游结果。
- `final-quality.md` 只检查最终契约，不抽取、不评级、不补任务、不补 JSON 或 DOCX 字段。

## 资源导航

- 全流程、模块和层级输入输出：`framework/workflow.md`
- 层级职责：`framework/layers/*.md`
- 业务判断规则：`references/rules/*.md`
- 提示词槽位、渲染模板、机器长表、DOCX、JSON 模板：`references/templates/*`
- 质量守卫：`references/guards/*.md`
- JSON 外部契约和 artifact manifest 契约：`references/json-contracts/*`
- 确定性脚本：`scripts/*.py`

详细硬规则不要复制到入口页；执行时按 workflow 进入对应层级，再读取该层指定的规则、模板、守卫、契约和脚本。
