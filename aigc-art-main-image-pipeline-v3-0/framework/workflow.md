# V3.0 Workflow

## 核心原则

每个层级必须产出明确结果；后续层不得重新切场、不得重做其他层判断。V3.0 沿用 V2.63 的三类证据账本、评级、S/A 状态规则和 JSON 主交付，并新增中文 core prompt、DOCX 人审交付和 C 级可见角色独立任务口径。

`prompt-generation.md` 只生成等待中台拼接风格前缀的中文 core prompt，不生成题材世界段，不生成画法段，不读取风格文件。

`output-contracts.md` 只整理机器长表。`json-manifest-generation.md` 在其后读取完成的 `main-image-production-table.md`，确定性投影生成 `prompt-manifest.json`。`review-docx-generation.md` 再读取完成的 `main-image-production-table.md`，确定性派生 `main-image-review-table.docx`。JSON 和 DOCX 都不得反向修改机器长表。

第三模块固定顺序：

```text
output-contracts -> json-manifest-generation -> review-docx-generation -> final-quality
```

## 流程图

```mermaid
flowchart TD
  RAW["原始剧本/PDF"] --> SI["script-intake.md<br/>输出: script-intake-result"]
  SI --> SC["scene-coverage.md<br/>输出: scene-coverage-table"]
  SC --> AEL["asset-evidence-ledger.md<br/>输出: character-evidence-ledger<br/>scene-evidence-ledger<br/>prop-evidence-ledger"]
  AEL --> ACA["asset-candidate-admission.md<br/>输出: asset-candidate-list<br/>polluted-label-cleanup-ledger"]
  ACA --> ARATE["asset-rating.md<br/>输出: asset-rating-result"]
  AEL --> ARATE
  SC --> ARATE
  ARATE --> REG["asset-registry.md<br/>输出: global-asset-registry<br/>alias-resolution-map"]
  ACA --> REG
  REG --> SV["state-variant.md<br/>输出: state-variant-result<br/>state-clue-disposition-ledger"]
  ARATE --> SV
  AEL --> SV
  SV --> CCD["character-candidate-disposition.md<br/>输出: character-disposition-ledger<br/>generic-template-coverage-ledger"]
  REG --> CCD
  ARATE --> CCD
  ACA --> CCD
  CCD --> TM["task-manifest-generation.md<br/>输出: global-task-draft"]
  SV --> TM
  REG --> TM
  TM --> EM["episode-usage-map.md<br/>输出: episode-usage-map-draft"]
  SC --> EM
  SV --> EM
  EM --> CA["character-anchor.md<br/>输出: character-anchor-result"]
  TM --> CA
  REG --> CA
  CA --> AUD["production-audit.md<br/>输出: production-audit-result"]
  AUD --> PG["prompt-generation.md<br/>输出: prompted-production-task-table"]
  PG --> OC["output-contracts.md<br/>输出: main-image-production-table.md"]
  OC --> JSON["json-manifest-generation.md<br/>输出: prompt-manifest.json"]
  JSON --> RDOCX["review-docx-generation.md<br/>输出: main-image-review-table.docx"]
  RDOCX --> QC["final-quality.md<br/>输出: final-quality-report"]
```

## 三大模块

| 模块 | 顺序 | 作用 |
|---|---|---|
| 剧本解析与资产识别 | `script-intake -> scene-coverage -> asset-evidence-ledger -> asset-candidate-admission -> asset-rating -> asset-registry -> state-variant -> character-candidate-disposition -> task-manifest-generation -> episode-usage-map` | 建立场次事实、三类评级前证据账本、候选资产、污染标签清洗记录、评级、base asset 注册表、S/A 状态索引、S/A 状态线索去向、人物候选去向、任务草稿和分集映射草稿。 |
| 资产生产与提示词生成 | `character-anchor -> production-audit -> prompt-generation` | 建立角色锚点、审计生产风险、生成中文 core prompt 或中文状态编辑 core instruction。 |
| 输出交付与质检 | `output-contracts -> json-manifest-generation -> review-docx-generation -> final-quality` | 汇总完整机器长表，从机器长表投影生成中台导入 JSON，从机器长表派生人审 DOCX，并做最终契约验收。 |

## 输入/输出契约

| 模块 | 层级 | 输入 | 调用文件 | 输出结果 |
|---|---|---|---|---|
| 剧本解析与资产识别 | `script-intake.md` | 原始剧本/PDF | `剧本解析输出规则.md` | `script-intake-result` |
| 剧本解析与资产识别 | `scene-coverage.md` | `script-intake-result` | `场次覆盖记录规则.md` | `scene-coverage-table` |
| 剧本解析与资产识别 | `asset-evidence-ledger.md` | `scene-coverage-table`、原剧本 `source_evidence/source_locator` | `资产证据账本规则.md` | `character-evidence-ledger`、`scene-evidence-ledger`、`prop-evidence-ledger` |
| 剧本解析与资产识别 | `asset-candidate-admission.md` | `character-evidence-ledger`、`scene-evidence-ledger`、`prop-evidence-ledger`、`scene-coverage-table` | `资产候选准入规则.md`、`污染标签清洗规则.md` | `asset-candidate-list`、`polluted-label-cleanup-ledger` |
| 剧本解析与资产识别 | `asset-rating.md` | `character-evidence-ledger`、`scene-evidence-ledger`、`prop-evidence-ledger`、`asset-candidate-list`、`scene-coverage-table`、原剧本 `source_evidence/source_locator` | `人物评级规则.md`、`场景评级规则.md`、`道具评级规则.md` | `asset-rating-result` |
| 剧本解析与资产识别 | `asset-registry.md` | `asset-candidate-list`、`asset-rating-result` | `资产注册规则.md` | `global-asset-registry`、`alias-resolution-map` |
| 剧本解析与资产识别 | `state-variant.md` | `global-asset-registry`、`asset-rating-result`、`asset-candidate-list`、`character-evidence-ledger`、`scene-evidence-ledger`、`prop-evidence-ledger`、`scene-coverage-table` | `状态拆分规则.md` | `state-variant-result`、`state-clue-disposition-ledger`，均只覆盖 S/A 状态范围 |
| 剧本解析与资产识别 | `character-candidate-disposition.md` | `asset-candidate-list`、`asset-rating-result`、`global-asset-registry`、`alias-resolution-map` | `人物候选去向闭环规则.md` | `character-disposition-ledger`、`generic-template-coverage-ledger` |
| 剧本解析与资产识别 | `task-manifest-generation.md` | `global-asset-registry`、`state-variant-result`、`character-disposition-ledger`、`generic-template-coverage-ledger` | `全局资产任务生成规则.md`、`任务类型字段审核规则.md` | `global-task-draft` |
| 剧本解析与资产识别 | `episode-usage-map.md` | `scene-coverage-table`、`global-asset-registry`、`state-variant-result`、`global-task-draft`、`character-disposition-ledger`、`generic-template-coverage-ledger` | `分集映射规则.md` | `episode-usage-map-draft` |
| 资产生产与提示词生成 | `character-anchor.md` | `global-task-draft`、`global-asset-registry`、`state-variant-result` | `角色锚定规则.md`、`任务类型字段审核规则.md` | `character-anchor-result` |
| 资产生产与提示词生成 | `production-audit.md` | `scene-coverage-table`、`character-evidence-ledger`、`scene-evidence-ledger`、`prop-evidence-ledger`、`asset-candidate-list`、`polluted-label-cleanup-ledger`、`asset-rating-result`、`global-asset-registry`、`alias-resolution-map`、`state-variant-result`、`state-clue-disposition-ledger`、`character-disposition-ledger`、`generic-template-coverage-ledger`、`global-task-draft`、`episode-usage-map-draft`、`character-anchor-result` | `生产审计规则.md` | `production-audit-result` |
| 资产生产与提示词生成 | `prompt-generation.md` | `global-task-draft`、`character-anchor-result`、`production-audit-result` | `人物主图提示词模板.md`、`场景主图提示词模板.md`、`道具主图提示词模板.md`、`角色状态编辑模板.md`、`core prompt结构守卫.md`、`提示词语言守卫.md`、`角色状态编辑守卫.md` | `prompted-production-task-table` |
| 输出交付与质检 | `output-contracts.md` | `script-intake-result`、`character-evidence-ledger`、`scene-evidence-ledger`、`prop-evidence-ledger`、`global-asset-registry`、`alias-resolution-map`、`state-variant-result`、`state-clue-disposition-ledger`、`character-disposition-ledger`、`generic-template-coverage-ledger`、`polluted-label-cleanup-ledger`、`prompted-production-task-table`、`episode-usage-map-draft`、`production-audit-result`、`character-anchor-result` | `任务类型字段审核规则.md`、`分集映射规则.md`、`机器长表模板.md` | `main-image-production-table.md` |
| 输出交付与质检 | `json-manifest-generation.md` | `main-image-production-table.md`、用户明确提供的 `contentId` 或项目元信息 | `中台JSON输出规则.md`、`prompt-manifest-json模板.md`、`seedance-element-extract-manifest-v1-contract.md`、`seedance-element-extract-manifest.v1.schema.json`、`generate_prompt_manifest.py` | `prompt-manifest.json` |
| 输出交付与质检 | `review-docx-generation.md` | `main-image-production-table.md` | `人审DOCX表格模板.md`、`generate_review_docx.py` | `main-image-review-table.docx` |
| 输出交付与质检 | `final-quality.md` | `prompt-manifest.json`、`main-image-production-table.md`、`main-image-review-table.docx`、`production-audit-result` | `输出质量守卫.md`、`中台JSON质量守卫.md`、`validate_prompt_manifest.py`、`validate_review_docx.py` | `final-quality-report` |

## 输出接续检查

- `script-intake-result` 被 `scene-coverage.md` 和 `output-contracts.md` 接住。
- `scene-coverage-table` 被 `asset-evidence-ledger.md`、`asset-candidate-admission.md`、`asset-rating.md`、`state-variant.md`、`episode-usage-map.md`、`production-audit.md` 接住。
- `character-evidence-ledger`、`scene-evidence-ledger`、`prop-evidence-ledger` 被候选准入、评级、状态、生产审计和机器长表接住。
- `asset-candidate-list` 和 `polluted-label-cleanup-ledger` 被下游去向、评级、注册、生产审计和机器长表接住。
- `asset-rating-result` 被注册、状态、人物去向和生产审计接住。
- `global-asset-registry` 和 `alias-resolution-map` 被状态、人物去向、任务生成、分集映射、锚点、生产审计和机器长表接住。
- `state-variant-result` 被任务生成、分集映射、锚点、生产审计和机器长表接住。
- `state-clue-disposition-ledger` 被生产审计和机器长表接住。
- `character-disposition-ledger` 和 `generic-template-coverage-ledger` 被任务生成、分集映射、生产审计和机器长表接住。
- `global-task-draft` 被分集映射、锚点、生产审计和提示词生成接住。
- `episode-usage-map-draft` 被生产审计和机器长表接住。
- `character-anchor-result` 被生产审计、提示词生成和机器长表接住。
- `production-audit-result` 被提示词生成、机器长表和最终质检接住。
- `prompted-production-task-table` 被 `output-contracts.md` 接住，并进入机器长表生产任务章节。
- `main-image-production-table.md` 被 `json-manifest-generation.md`、`review-docx-generation.md` 和 `final-quality.md` 接住。
- `prompt-manifest.json` 被 `review-docx-generation.md` 的顺序前置完成，但不作为 DOCX 输入；同时被 `final-quality.md` 接住。
- `main-image-review-table.docx` 被 `final-quality.md` 接住。
- `final-quality-report` 是终点输出。
