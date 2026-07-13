# asset-evidence-ledger.md

## 作用

从 `audit/scene-coverage-table.md` 中整理全剧人物、场景、道具相关证据，生成三张评级前无损证据账本。它解决“评级前到底有哪些资产事实存在，以及这些事实如何回溯到场次和原文”的问题，避免事实在候选准入、生产价值判断或锚点逻辑之前被筛掉。

## 输入

`audit/scene-coverage-table.md`、原剧本 `source_evidence` / `source_locator`

## 调用文件

`references/rules/资产证据账本规则.md`

## 输出结果

`audit/character-evidence-ledger.md`、`audit/scene-evidence-ledger.md`、`audit/prop-evidence-ledger.md`

## 边界

本层只记录和归整资产证据，生成稳定 `evidence_id`，保留 `raw_label/raw_text`、归一主体、可见性、同一性线索、状态线索归属、不确定性和来源定位。不做候选准入、不写 `audit/polluted-label-cleanup-ledger.md`、不做 S/A/B/C 评级、不注册资产、不拆状态、不生成任务、不决定候选最终去向。它不得重新切场；如发现 `audit/script-intake-result.md` 或 `audit/scene-coverage-table.md` 有漏场、污染主体或可见性错误，必须标记阻断复核并指回对应层级。
