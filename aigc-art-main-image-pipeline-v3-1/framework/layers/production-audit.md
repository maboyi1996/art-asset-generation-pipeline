# production-audit.md

## 作用

在提示词生成前检查前序结构化结果是否完整、一致、可进入生产，尤其检查三类评级前证据账本、事实覆盖、候选准入、评级、注册、S/A 状态主体、B/C 未进入状态层、人物候选去向、污染清洗、任务草稿、分集映射和锚点依赖是否断链。

## 输入

`audit/scene-coverage-table.md`、`audit/character-evidence-ledger.md`、`audit/scene-evidence-ledger.md`、`audit/prop-evidence-ledger.md`、`audit/asset-candidate-list.md`、`audit/state-variant-result.md`、`audit/state-clue-disposition-ledger.md`、`audit/asset-rating-result.md`、`audit/global-asset-registry.md`、`audit/alias-resolution-map.md`、`audit/character-disposition-ledger.md`、`audit/generic-template-coverage-ledger.md`、`audit/polluted-label-cleanup-ledger.md`、`audit/global-task-draft.md`、`audit/episode-usage-map-draft.md`、`audit/character-anchor-result.md`

## 调用文件

`references/rules/生产审计规则.md`

## 输出结果

`audit/production-audit-result.md`

## 边界

只做一致性审计和问题标记，不重新抽取资产、不重新拆状态、不重新评级、不补写资产任务、不重写提示词。发现断链时必须指回具体拥有层：证据账本漏项回 `asset-evidence-ledger.md`，污染清洗回 `asset-candidate-admission.md`，S/A 状态主体或 B/C 进入状态层回 `state-variant.md`，候选去向回 `character-candidate-disposition.md`，任务缺失回 `task-manifest-generation.md`，映射缺引用回 `episode-usage-map.md`。
