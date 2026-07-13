# episode-usage-map.md

## 作用

根据场次事实、资产注册、状态拆分和全局任务草稿，生成每集每场使用哪个资产状态和哪个任务的映射草稿。

## 输入

`audit/scene-coverage-table.md`、`audit/global-asset-registry.md`、`audit/state-variant-result.md`、`audit/global-task-draft.md`、`audit/character-disposition-ledger.md`、`audit/generic-template-coverage-ledger.md`

## 调用文件

`references/rules/分集映射规则.md`

## 输出结果

`audit/episode-usage-map-draft.md`

## 边界

本层只生成分集使用映射，不重新注册资产、不修改任务、不补建任务、不改评级、不生成提示词。每条映射必须引用已存在的 `task_id`，或引用明确的可见排除/非视觉去向/泛称模板覆盖记录。
