# state-variant.md

## 作用

判断候选资产是否需要拆成可见状态资产，并记录每条可见状态线索被采用、复用、排除或送审的去向。

## 输入

`asset-candidate-list`、`scene-coverage-table`

## 调用文件

`references/rules/状态拆分规则.md`

## 输出结果

`state-variant-result`、`state-clue-disposition-ledger`

## 边界

只判断可见状态差异和状态线索去向，不定义资产等级、不生成任务、不写提示词。不得把场级状态线索自动分配给本场所有人物；主体不明的状态线索必须进入 `state-clue-disposition-ledger` 的排除或人工复核记录。
