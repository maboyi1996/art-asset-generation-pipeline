# asset-registry.md

## 作用

合并资产别名，生成稳定资产 ID、状态 ID、可被中台消费的全局任务草稿、人物候选去向台账、污染标签清洗记录和分集映射草稿。

## 输入

`asset-candidate-list`、`state-variant-result`、`asset-rating-result`、`scene-coverage-table`

## 调用文件

- `references/rules/全局资产任务生成规则.md`
- `references/rules/任务类型字段审核规则.md`
- `references/rules/分集映射规则.md`
- `references/rules/人物候选去向闭环规则.md`
- `references/rules/污染标签清洗记录规则.md`

## 输出结果

`global-asset-registry`、`global-task-draft`、`character-disposition-ledger`、`polluted-label-cleanup-ledger`、`episode-usage-map-draft`

## 边界

不重新抽取资产、不重新拆状态、不重新评级。本层可以生成任务草稿字段、可见排除记录和污染标签清洗记录，但不建立脸模锚点、不生成提示词正文。B/C 人物不需要项目级锚点，但可生产人物必须先进入 `global-task-draft` 形成 `text_to_image` 任务；泛称、群体或背景人物优先模板化、分组或可见排除，不得仅因重复出现制造独立单人脸模任务；人物候选去向台账只登记已进入 `asset-candidate-list` 的真实人物候选最终去向，不得替代全局生产任务。被准入门挡下的污染标签只能进入 `polluted-label-cleanup-ledger`，不得作为伪人物候选写入 `character-disposition-ledger`。分集映射只引用全局任务草稿中的 `task_id`。
