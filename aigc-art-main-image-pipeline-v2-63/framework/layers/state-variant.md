# state-variant.md

## 作用

在 base asset 已完成评级和注册后，只对 S/A 资产判断是否需要拆成可见状态资产，并记录 S/A 状态识别范围内的状态线索被采用、复用、排除或送审的去向。

## 输入

`global-asset-registry`、`asset-rating-result`、`asset-candidate-list`、`character-evidence-ledger`、`scene-evidence-ledger`、`prop-evidence-ledger`、`scene-coverage-table`

## 调用文件

`references/rules/状态拆分规则.md`

## 输出结果

`state-variant-result`、`state-clue-disposition-ledger`

## 边界

只判断 S/A 可见状态差异和 S/A 状态线索去向，不定义资产等级、不生成任务、不写提示词。状态继承 base asset 的 `priority_level`。B/C 资产不进入状态识别、状态线索去向、人工复核或状态任务路径；不得为 B/C 写入 `state-clue-disposition-ledger`。不得把场级状态线索自动分配给本场所有人物；主体不明但可能影响 S/A 状态判断的线索才进入 `state-clue-disposition-ledger` 的排除、人工复核或阻断记录。
