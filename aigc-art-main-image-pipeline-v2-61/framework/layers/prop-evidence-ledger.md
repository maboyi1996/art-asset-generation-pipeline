# prop-evidence-ledger.md

## 作用

从 `scene-coverage-table` 中整理全剧道具和物件证据，生成评级前无损道具证据账本。它解决“哪些物件、使用行为、特写、交接链和泛化陈设证据存在”的问题。

## 输入

`scene-coverage-table`、原剧本 `source_evidence` / `source_locator`

## 调用文件

`references/rules/道具证据账本规则.md`

## 输出结果

`prop-evidence-ledger`

## 边界

本层只记录和归整道具证据，不做 S/A/B/C 评级、不注册资产、不拆状态、不生成任务、不决定生产去向。它不得重新切场；同一物件证据不足时只记录不确定性，不在本层升级或合并。
