# production-audit.md

## 作用

在提示词生成前检查前序结构化结果是否完整、一致、可进入生产，尤其检查三类评级前证据账本、事实覆盖、候选准入、评级、注册、S/A 状态主体、B/C 未进入状态层、人物候选去向、污染清洗、任务草稿、分集映射和锚点依赖是否断链。

## 输入

`scene-coverage-table`、`character-evidence-ledger`、`scene-evidence-ledger`、`prop-evidence-ledger`、`asset-candidate-list`、`state-variant-result`、`state-clue-disposition-ledger`、`asset-rating-result`、`global-asset-registry`、`alias-resolution-map`、`character-disposition-ledger`、`generic-template-coverage-ledger`、`polluted-label-cleanup-ledger`、`global-task-draft`、`episode-usage-map-draft`、`character-anchor-result`

## 调用文件

`references/rules/生产审计规则.md`

## 输出结果

`production-audit-result`

## 边界

只做一致性审计和问题标记，不重新抽取资产、不重新拆状态、不重新评级、不补写资产任务、不重写提示词。发现断链时必须指回具体拥有层：证据账本漏项回 `asset-evidence-ledger.md`，污染清洗回 `asset-candidate-admission.md`，S/A 状态主体或 B/C 进入状态层回 `state-variant.md`，候选去向回 `character-candidate-disposition.md`，任务缺失回 `task-manifest-generation.md`，映射缺引用回 `episode-usage-map.md`。
