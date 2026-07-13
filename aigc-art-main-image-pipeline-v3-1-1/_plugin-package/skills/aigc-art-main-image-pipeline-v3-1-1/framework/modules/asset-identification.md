# 模块：剧本解析与资产识别

## 作用

从原始剧本中建立可追溯事实，生成三类评级前无损证据账本，完成候选准入、污染标签清洗记录、制作连续性评级、base asset 注册、状态拆分、人物候选去向、任务草稿和分集映射草稿。

## 层级顺序

`script-intake.md -> scene-coverage.md -> asset-evidence-ledger.md -> asset-candidate-admission.md -> asset-rating.md -> asset-registry.md -> state-variant.md -> character-candidate-disposition.md -> task-manifest-generation.md -> episode-usage-map.md`

## 边界

本模块只形成生产前结构化结果，不生成最终提示词，不输出最终 MD。证据账本层只保留事实和来源；候选准入层只处理候选进入与污染准入记录；评级层在状态拆分前硬分流；注册层只注册 base asset；状态层只拆可见状态；任务层不改候选去向；映射层不补建任务。
