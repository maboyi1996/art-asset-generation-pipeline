# asset-candidate-admission.md

## 作用

从三类评级前证据账本中判断哪些人物、场景、道具事实可以进入候选资产池，并在候选准入门口处理污染标签。候选准入不得按生产价值提前筛掉可见事实；人物候选必须使用规范主体名，动作、情绪、语气、声音、瞬时表情或组合短语不得进入人物候选池。

## 输入

`audit/character-evidence-ledger.md`、`audit/scene-evidence-ledger.md`、`audit/prop-evidence-ledger.md`、`audit/scene-coverage-table.md`

## 调用文件

- `references/rules/资产候选准入规则.md`
- `references/rules/污染标签清洗规则.md`

## 输出结果

`audit/asset-candidate-list.md`、`audit/polluted-label-cleanup-ledger.md`

## 边界

本层只判断候选资产准入，并记录候选准入时发生的污染标签拦截、归一、拆分、证据保留或阻断复核事件。可见人物、场景、道具事实必须从对应 evidence ledger 被候选、污染清洗、可见排除或阻断复核承接，不能因为“看起来不重要”或“后续可能不生产”提前丢弃。普通 `raw_label -> normalized_subject` 归一如果没有触发候选污染风险，不重复写入 `polluted-label-cleanup-ledger`。不得做 S/A/B/C 评级、状态拆分、资产注册、人物去向、任务生成或分集映射。
