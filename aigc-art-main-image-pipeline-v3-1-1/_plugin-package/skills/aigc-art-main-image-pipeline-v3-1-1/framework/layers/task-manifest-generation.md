# task-manifest-generation.md

## 作用

把已注册、已评级、已确认状态或去向的资产转换成可被中台消费的全局生产任务草稿。

## 输入

`audit/global-asset-registry.md`、`audit/state-variant-result.md`、`audit/character-disposition-ledger.md`、`audit/generic-template-coverage-ledger.md`

## 调用文件

- `references/rules/全局资产任务生成规则.md`
- `references/rules/任务类型字段审核规则.md`

## 输出结果

`audit/global-task-draft.md`

## 边界

本层只生成任务草稿和可见排除任务行，不重新抽取、不重新拆状态、不重新评级、不改人物候选去向、不生成分集映射、不建立脸模锚点、不写提示词正文。`audit/character-disposition-ledger.md` 的生产类去向和 `audit/generic-template-coverage-ledger.md` 的模板任务去向必须能在本层生成的 `audit/global-task-draft.md` 中找到对应 `task_id`。
