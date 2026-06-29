# state-variant.md

## 作用

判断候选资产是否需要拆成可见状态资产，并确保人物状态有明确主体证据。

## 输入

`asset-candidate-list`、`scene-coverage-table`

## 调用文件

`references/rules/状态拆分规则.md`

## 输出结果

`state-variant-result`

## 边界

只判断可见状态差异，不定义资产等级、不生成任务、不写提示词。不得把场级状态线索自动分配给本场所有人物。
