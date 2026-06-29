# V2.61 Workflow

## 核心原则

每个层级必须产出明确结果；后续层不得重新切场、不得重做其他层判断。评级层的主输入是对应的评级前无损证据账本，可读取 `source_locator` 对应原文核验证据，但不得重新扫 PDF、重新发明候选或静默补齐漏项。

V2.61 在 `scene-coverage.md` 之后新增三类证据账本层：人物、场景、道具分别形成评级前无损证据台账。候选抽取、评级、注册、去向、任务和映射都必须围绕这些证据账本闭环，生产筛选只能发生在评级之后。

## 流程图

```mermaid
flowchart TD
  RAW["原始剧本/PDF"] --> SI["script-intake.md<br/>输出: script-intake-result"]
  SI --> SC["scene-coverage.md<br/>输出: scene-coverage-table"]
  SC --> CEL["character-evidence-ledger.md<br/>输出: character-evidence-ledger"]
  SC --> SEL["scene-evidence-ledger.md<br/>输出: scene-evidence-ledger"]
  SC --> PEL["prop-evidence-ledger.md<br/>输出: prop-evidence-ledger"]
  CEL --> AE["asset-extraction.md<br/>输出: asset-candidate-list<br/>polluted-label-cleanup-ledger"]
  SEL --> AE
  PEL --> AE
  AE --> SV["state-variant.md<br/>输出: state-variant-result<br/>state-clue-disposition-ledger"]
  SV --> AR["asset-rating.md<br/>输出: asset-rating-result"]
  CEL --> AR
  SEL --> AR
  PEL --> AR
  AR --> REG["asset-registry.md<br/>输出: global-asset-registry<br/>alias-resolution-map"]
  REG --> CD["candidate-disposition.md<br/>输出: character-disposition-ledger<br/>generic-template-coverage-ledger"]
  CD --> TM["task-manifest-generation.md<br/>输出: global-task-draft"]
  TM --> EM["episode-usage-map.md<br/>输出: episode-usage-map-draft"]
  EM --> CA["character-anchor.md<br/>输出: character-anchor-result"]
  CA --> AUD["production-audit.md<br/>输出: production-audit-result"]
  AUD --> PG["prompt-generation.md<br/>输出: prompted-production-task-table"]
  PG --> OC["output-contracts.md<br/>输出: main-image-production-table.md<br/>main-image-review-table.md"]
  OC --> QC["final-quality.md<br/>输出: final-quality-report"]
```

## 三大模块

| 模块 | 顺序 | 作用 |
|---|---|---|
| 剧本解析与资产识别 | `script-intake -> scene-coverage -> character/scene/prop-evidence-ledger -> asset-extraction -> state-variant -> asset-rating -> asset-registry -> candidate-disposition -> task-manifest-generation -> episode-usage-map` | 建立场次事实、三类评级前证据账本、候选资产、污染清洗记录、状态线索去向、评级、资产注册表、候选去向、任务草稿和分集映射草稿。 |
| 资产生产与提示词生成 | `character-anchor -> production-audit -> prompt-generation` | 建立角色锚点、审计生产风险、生成提示词。 |
| 输出交付与质检 | `output-contracts -> final-quality` | 汇总完整机器长表和派生人审短表，并做最终契约验收。 |

## 输入/输出契约

| 模块 | 层级 | 输入 | 调用文件 | 输出结果 |
|---|---|---|---|---|
| 剧本解析与资产识别 | `script-intake.md` | 原始剧本/PDF | `剧本解析输出规则.md` | `script-intake-result` |
| 剧本解析与资产识别 | `scene-coverage.md` | `script-intake-result` | `场次覆盖记录规则.md` | `scene-coverage-table` |
| 剧本解析与资产识别 | `character-evidence-ledger.md` | `scene-coverage-table`、原剧本 `source_evidence/source_locator` | `人物证据账本规则.md` | `character-evidence-ledger` |
| 剧本解析与资产识别 | `scene-evidence-ledger.md` | `scene-coverage-table`、原剧本 `source_evidence/source_locator` | `场景证据账本规则.md` | `scene-evidence-ledger` |
| 剧本解析与资产识别 | `prop-evidence-ledger.md` | `scene-coverage-table`、原剧本 `source_evidence/source_locator` | `道具证据账本规则.md` | `prop-evidence-ledger` |
| 剧本解析与资产识别 | `asset-extraction.md` | `character-evidence-ledger`、`scene-evidence-ledger`、`prop-evidence-ledger`、`scene-coverage-table` | `资产抽取边界规则.md`、`污染标签清洗记录规则.md` | `asset-candidate-list`、`polluted-label-cleanup-ledger` |
| 剧本解析与资产识别 | `state-variant.md` | `asset-candidate-list`、`scene-coverage-table` | `状态拆分规则.md` | `state-variant-result`、`state-clue-disposition-ledger` |
| 剧本解析与资产识别 | `asset-rating.md` | `character-evidence-ledger`、`scene-evidence-ledger`、`prop-evidence-ledger`、`asset-candidate-list`、`state-variant-result`、`scene-coverage-table`、原剧本 `source_evidence/source_locator` | `人物评级规则.md`、`场景评级规则.md`、`道具评级规则.md` | `asset-rating-result` |
| 剧本解析与资产识别 | `asset-registry.md` | `asset-candidate-list`、`state-variant-result`、`asset-rating-result` | `资产注册规则.md` | `global-asset-registry`、`alias-resolution-map` |
| 剧本解析与资产识别 | `candidate-disposition.md` | `asset-candidate-list`、`asset-rating-result`、`global-asset-registry`、`alias-resolution-map`、`polluted-label-cleanup-ledger` | `人物候选去向闭环规则.md` | `character-disposition-ledger`、`generic-template-coverage-ledger` |
| 剧本解析与资产识别 | `task-manifest-generation.md` | `global-asset-registry`、`asset-rating-result`、`state-variant-result`、`character-disposition-ledger`、`generic-template-coverage-ledger`、`polluted-label-cleanup-ledger` | `全局资产任务生成规则.md`、`任务类型字段审核规则.md` | `global-task-draft` |
| 剧本解析与资产识别 | `episode-usage-map.md` | `scene-coverage-table`、`global-asset-registry`、`state-variant-result`、`global-task-draft`、`character-disposition-ledger`、`generic-template-coverage-ledger` | `分集映射规则.md` | `episode-usage-map-draft` |
| 资产生产与提示词生成 | `character-anchor.md` | `global-task-draft`、`asset-rating-result`、`state-variant-result` | `角色锚定规则.md`、`任务类型字段审核规则.md` | `character-anchor-result` |
| 资产生产与提示词生成 | `production-audit.md` | `scene-coverage-table`、`character-evidence-ledger`、`scene-evidence-ledger`、`prop-evidence-ledger`、`asset-candidate-list`、`state-variant-result`、`state-clue-disposition-ledger`、`asset-rating-result`、`global-asset-registry`、`alias-resolution-map`、`character-disposition-ledger`、`generic-template-coverage-ledger`、`polluted-label-cleanup-ledger`、`global-task-draft`、`episode-usage-map-draft`、`character-anchor-result` | `生产审计规则.md` | `production-audit-result` |
| 资产生产与提示词生成 | `prompt-generation.md` | `global-task-draft`、`character-anchor-result`、`production-audit-result` | `人物主图提示词模板.md`、`场景主图提示词模板.md`、`道具主图提示词模板.md`、`角色状态编辑模板.md`、`写实风格守卫.md`、`提示词语言守卫.md`、`角色状态编辑守卫.md` | `prompted-production-task-table` |
| 输出交付与质检 | `output-contracts.md` | `script-intake-result`、`character-evidence-ledger`、`scene-evidence-ledger`、`prop-evidence-ledger`、`global-asset-registry`、`alias-resolution-map`、`state-variant-result`、`state-clue-disposition-ledger`、`character-disposition-ledger`、`generic-template-coverage-ledger`、`polluted-label-cleanup-ledger`、`prompted-production-task-table`、`episode-usage-map-draft`、`production-audit-result`、`character-anchor-result` | `任务类型字段审核规则.md`、`分集映射规则.md`、`机器长表模板.md`、`人审短表模板.md` | `main-image-production-table.md`、`main-image-review-table.md` |
| 输出交付与质检 | `final-quality.md` | `main-image-production-table.md`、`main-image-review-table.md`、`production-audit-result` | `输出质量守卫.md` | `final-quality-report` |

## 输出接续检查

- `script-intake-result` 被 `scene-coverage.md` 和 `output-contracts.md` 接住。
- `scene-coverage-table` 被三类证据账本、`asset-extraction.md`、`state-variant.md`、`asset-rating.md`、`episode-usage-map.md`、`production-audit.md` 接住。
- `character-evidence-ledger` 被 `asset-extraction.md`、`asset-rating.md`、`production-audit.md`、`output-contracts.md` 接住。
- `scene-evidence-ledger` 被 `asset-extraction.md`、`asset-rating.md`、`production-audit.md`、`output-contracts.md` 接住。
- `prop-evidence-ledger` 被 `asset-extraction.md`、`asset-rating.md`、`production-audit.md`、`output-contracts.md` 接住。
- `asset-candidate-list` 被 `state-variant.md`、`asset-rating.md`、`asset-registry.md`、`candidate-disposition.md`、`production-audit.md` 接住。
- `polluted-label-cleanup-ledger` 由 `asset-extraction.md` 生成，并被 `candidate-disposition.md`、`task-manifest-generation.md`、`production-audit.md`、`output-contracts.md` 接住。
- `state-variant-result` 被 `asset-rating.md`、`asset-registry.md`、`task-manifest-generation.md`、`episode-usage-map.md`、`character-anchor.md`、`production-audit.md`、`output-contracts.md` 接住。
- `state-clue-disposition-ledger` 被 `production-audit.md` 和 `output-contracts.md` 接住。
- `asset-rating-result` 被 `asset-registry.md`、`candidate-disposition.md`、`task-manifest-generation.md`、`character-anchor.md`、`production-audit.md` 接住。
- `global-asset-registry` 被 `candidate-disposition.md`、`task-manifest-generation.md`、`episode-usage-map.md`、`production-audit.md`、`output-contracts.md` 接住。
- `alias-resolution-map` 被 `candidate-disposition.md`、`production-audit.md`、`output-contracts.md` 接住。
- `character-disposition-ledger` 被 `task-manifest-generation.md`、`episode-usage-map.md`、`production-audit.md`、`output-contracts.md` 接住。
- `generic-template-coverage-ledger` 被 `task-manifest-generation.md`、`episode-usage-map.md`、`production-audit.md`、`output-contracts.md` 接住。
- `global-task-draft` 由 `task-manifest-generation.md` 生成，并被 `episode-usage-map.md`、`character-anchor.md`、`production-audit.md`、`prompt-generation.md` 接住。
- `episode-usage-map-draft` 由 `episode-usage-map.md` 生成，并被 `production-audit.md`、`output-contracts.md` 接住。
- `character-anchor-result` 被 `production-audit.md`、`prompt-generation.md`、`output-contracts.md` 接住。
- `production-audit-result` 被 `prompt-generation.md`、`output-contracts.md`、`final-quality.md` 接住。
- `prompted-production-task-table` 被 `output-contracts.md` 接住。
- `main-image-production-table.md` 和 `main-image-review-table.md` 被 `final-quality.md` 接住。
- `final-quality-report` 是终点输出。
