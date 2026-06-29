# production-audit.md

## 作用

在提示词生成前检查前序结构化结果是否完整、一致、可进入生产。

## 输入

`global-asset-registry`、`global-task-draft`、`character-disposition-ledger`、`episode-usage-map-draft`、`character-anchor-result`、`scene-coverage-table`

## 调用文件

`references/rules/生产审计规则.md`

## 输出结果

`production-audit-result`

## 边界

只做一致性审计和问题标记，不重新抽取资产、不重新拆状态、不重新评级、不补写人物任务、不重写提示词。
