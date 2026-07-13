# prompt-generation.md

## 作用

读取已确认的任务草稿、锚点结果和审计结果，为已有生产任务生成提示词或编辑指令。

## 输入

`global-task-draft`、`character-anchor-result`、`production-audit-result`

## 调用文件

- `references/templates/人物主图提示词模板.md`
- `references/templates/场景主图提示词模板.md`
- `references/templates/道具主图提示词模板.md`
- `references/templates/角色状态编辑模板.md`
- `references/guards/写实风格守卫.md`
- `references/guards/提示词语言守卫.md`
- `references/guards/角色状态编辑守卫.md`

## 输出结果

`prompted-production-task-table`

## 边界

只读取已存在的 `base_asset_id`、`state_asset_id`、`priority_level`、`task_type`、`review_status`、状态和锚点字段，并据此套用模板和守卫。输出 `prompted-production-task-table` 时必须原样保留 `task_id`、`base_asset_id`、`state_asset_id` 和 `anchor_task_id`，供机器长表和 JSON 生成层稳定回指。

不得为缺失的 B/C 人物或其他资产补建任务；发现应有 prompt 但缺少任务时，问题必须回溯到 `task-manifest-generation.md` 的 `global-task-draft` 生成。
