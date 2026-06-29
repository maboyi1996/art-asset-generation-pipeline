# scene-evidence-ledger.md

## 作用

从 `scene-coverage-table` 中整理全剧场景和空间证据，生成评级前无损场景证据账本。它解决“哪些空间事实、地点表述、同一空间线索和泛化空间证据存在”的问题。

## 输入

`scene-coverage-table`、原剧本 `source_evidence` / `source_locator`

## 调用文件

`references/rules/场景证据账本规则.md`

## 输出结果

`scene-evidence-ledger`

## 边界

本层只记录和归整场景证据，不做 S/A/B/C 评级、不合并为最终场景资产、不拆状态、不生成任务、不决定生产去向。它不得重新切场；同一空间证据不足时只记录不确定性，不在本层升级或合并。
