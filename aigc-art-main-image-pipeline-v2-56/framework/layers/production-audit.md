# production-audit.md

## 作用

在提示词生成前检查前序结构化结果是否完整、一致、可进入生产，尤其检查应生产资产是否已经进入 `global-task-draft`，以及是否存在未解析场次、污染人物名、主体不明状态或泛称人物任务爆炸。

## 输入

`global-asset-registry`、`global-task-draft`、`character-disposition-ledger`、`polluted-label-cleanup-ledger`、`episode-usage-map-draft`、`character-anchor-result`、`scene-coverage-table`

## 调用文件

`references/rules/生产审计规则.md`

## 输出结果

`production-audit-result`

## 边界

只做一致性审计和问题标记，不重新抽取资产、不重新拆状态、不重新评级、不补写资产任务、不重写提示词。发现 B/C 可生产人物只有去向、没有任务，或污染标签进入人物候选去向台账时，必须返回 blocking 问题并指回 `asset-registry.md`。
