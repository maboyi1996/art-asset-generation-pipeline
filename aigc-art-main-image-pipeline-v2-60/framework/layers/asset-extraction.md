# asset-extraction.md

## 作用

从场次事实中抽取候选人物、场景、道具，并在候选准入门口清洗污染标签。人物候选必须使用规范主体名，动作、情绪、语气、声音、瞬时表情或组合短语不得进入人物候选池。

## 输入

`scene-coverage-table`

## 调用文件

- `references/rules/资产抽取边界规则.md`
- `references/rules/污染标签清洗记录规则.md`

## 输出结果

`asset-candidate-list`、`polluted-label-cleanup-ledger`

## 边界

本层只判断候选资产准入并记录被准入门拦下的污染标签清洗过程。不得做 S/A/B/C 评级、状态拆分、资产注册、人物去向、任务生成或分集映射。
