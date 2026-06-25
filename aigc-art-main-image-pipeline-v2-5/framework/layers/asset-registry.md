# asset-registry.md

## 作用

合并资产别名，生成稳定资产 ID、状态 ID、任务草稿和分集映射草稿。

## 输入

`asset-candidate-list`、`state-variant-result`、`asset-rating-result`、`scene-coverage-table`

## 调用文件

- `references/rules/任务类型字段审核规则.md`
- `references/rules/分集映射规则.md`

## 输出结果

`global-asset-registry`、`global-task-draft`、`episode-usage-map-draft`

## 边界

不重新抽取资产、不重新拆状态、不重新评级。分集映射只引用全局任务草稿中的 `task_id`。
