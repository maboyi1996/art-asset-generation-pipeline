# character-candidate-disposition.md

## 作用

为已进入 `audit/asset-candidate-list.md` 的人物候选和泛称/群体人物候选生成最终去向台账，说明每个候选被生产、模板化、别名合并、分组、排除、标记为非视觉候选或送审。

## 输入

`audit/asset-candidate-list.md`、`audit/asset-rating-result.md`、`audit/global-asset-registry.md`、`audit/alias-resolution-map.md`

## 调用文件

`references/rules/人物候选去向闭环规则.md`

## 输出结果

`audit/character-disposition-ledger.md`、`audit/generic-template-coverage-ledger.md`

## 边界

本层只回答 admitted character candidates 的最终去向，不生成生产任务、不注册资产、不重新评级、不记录污染标签清洗过程、不拆状态。`audit/character-disposition-ledger.md` 只覆盖已进入 `audit/asset-candidate-list.md` 的真实人物候选；被准入门挡下的污染标签只能在 `audit/polluted-label-cleanup-ledger.md` 中出现，并由 `production-audit.md` 检查是否污染下游。
