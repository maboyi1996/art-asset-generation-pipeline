# prompt-generation.md

## 作用

读取已确认的任务草稿、锚点结果、生产审计结果和必要证据，为已有生产任务填写 core prompt 槽位表。

V3.1 的本层不得直接输出整段最终 prompt。模型只能把剧本证据、注册结果、状态结果、锚点结果和审计结论转写为结构化槽位。中文 core prompt 和中文状态编辑 core instruction 由 `scripts/render_core_prompts.py` 确定性渲染。

## 输入

`audit/global-task-draft.md`、`audit/character-anchor-result.md`、`audit/production-audit-result.md`，以及填写槽位所需的 `audit/` 上游证据、注册、状态和映射产物。

## 调用文件

- `references/rules/core-prompt-slots规则.md`
- `references/templates/core-prompt-slots模板.md`
- `references/templates/core-prompt-render-templates.json`
- `references/templates/人物主图提示词模板.md`
- `references/templates/场景主图提示词模板.md`
- `references/templates/道具主图提示词模板.md`
- `references/templates/角色状态编辑模板.md`
- `references/guards/core prompt结构守卫.md`
- `references/guards/提示词语言守卫.md`
- `references/guards/角色状态编辑守卫.md`

## 输出结果

`production-source/core-prompt-slots.md`

随后由 `scripts/render_core_prompts.py` 输出：

`production-source/prompted-production-task-table.md`

## 边界

本层只读取已存在的 `task_id`、`base_asset_id`、`state_asset_id`、`priority_level`、`task_type`、`review_status`、状态、锚点和证据字段，并按 `core-prompt-slots规则.md` 填入槽位。

不得为缺失的 B/C 人物或其他资产补建任务；发现应有 prompt 但缺少任务时，问题必须回溯到 `task-manifest-generation.md` 的 `audit/global-task-draft.md`。

不得读取、选择或拼接任何画风文件。不得生成 `【A. 题材世界】`、`【B. 画法】`、`{{include:...}}` 或风格前缀。不得残留旧版英文写实摄影模板。

不得在槽位里写负向约束、排除式句子或“无 XX 设定”等串层内容，除非该槽位在规则中明确是生产防错槽位。防遮脸、防多人物、防场景、防动作、防手、防文字等内容由渲染模板的固定负向段和 `negative_prompt` 处理。

如果某个必填槽位缺少证据，本层必须填写 `slot_status: missing_evidence` 并在 `slot_issue` 中指明缺口；不得用推测内容硬填。渲染脚本遇到必填槽位缺失或 `missing_evidence` 必须失败。
