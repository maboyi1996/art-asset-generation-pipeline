# asset-rating.md

## 作用

给每个 base asset 评定制作连续性等级 `S/A/B/C`。评级主输入是对应的评级前证据账本；人物跨集评级只统计同一具体人物的可见脸模生产出场。

## 输入

`character-evidence-ledger`、`scene-evidence-ledger`、`prop-evidence-ledger`、`asset-candidate-list`、`state-variant-result`、`scene-coverage-table`、原剧本 `source_evidence/source_locator`

## 调用文件

- `references/rules/人物评级规则.md`
- `references/rules/场景评级规则.md`
- `references/rules/道具评级规则.md`

## 输出结果

`asset-rating-result`

## 边界

本层是唯一正式评级层。后续层读取 `asset-rating-result`，不得重新评级。评级层主要读取三类 evidence ledger，并可回看 ledger 中的 `source_locator` 对应原文核验同一资产证据；不得重新扫 PDF、不得重新切场、不得重新发明候选。发现 evidence ledger 或 `asset-candidate-list` 漏掉可见事实时，不得静默补候选，必须输出阻断并指回对应证据层或 `asset-extraction.md`。本层不注册资产、不生成任务。
