# 模块：剧本解析与资产识别

## 作用

从原始剧本中建立可追溯事实，抽取候选资产，记录污染标签清洗，拆分可见状态，完成制作连续性评级，注册资产，并生成候选去向、任务草稿和分集映射草稿。

## 层级顺序

`script-intake.md -> scene-coverage.md -> asset-extraction.md -> state-variant.md -> asset-rating.md -> asset-registry.md -> candidate-disposition.md -> task-manifest-generation.md -> episode-usage-map.md`

## 边界

本模块只形成生产前结构化结果，不生成最终提示词，不输出最终 MD。各层只产出自己的粒度：注册层不生成任务，任务层不改去向，映射层不改任务。
