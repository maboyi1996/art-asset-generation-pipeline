# character-evidence-ledger.md

## 作用

从 `scene-coverage-table` 中整理全剧人物相关证据，生成评级前无损人物证据账本。它解决“评级前到底有哪些人物事实存在”的问题，避免人物在候选准入、生产价值判断或锚点逻辑之前被筛掉。

## 输入

`scene-coverage-table`、原剧本 `source_evidence` / `source_locator`

## 调用文件

`references/rules/人物证据账本规则.md`

## 输出结果

`character-evidence-ledger`

## 边界

本层只记录和归整人物证据，不做 S/A/B/C 评级、不注册资产、不拆状态、不生成任务、不决定候选最终去向。它不得重新切场；如发现 `script-intake-result` 或 `scene-coverage-table` 有漏场、污染主体或可见性错误，必须标记阻断复核并指回对应层级。
