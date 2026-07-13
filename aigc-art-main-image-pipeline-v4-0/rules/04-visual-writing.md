# 模块四：视觉锚点与提示词规则

## asset-anchor

- 人物锚点固定身份、年龄段、脸部识别和基础服装记忆点。
- 场景锚点固定空间身份、布局、入口、纵深和核心元素。
- 道具锚点固定物体类型、结构、材质、用途和状态。
- 所有锚点必须引用 evidence；无证据内容不得补造。

## prompt-slots

- 模型只填写 JSON template 声明的 slots，不得直接提交最终 prompt。
- 每个 slot 必须具体、可画、中文、与资产类型一致并可追溯。
- 剧情摘要不能替代视觉内容；不得加入风格前缀。

## prompt-render

- Python 使用 templates/prompt-render.json 确定性渲染。
- ROLE 9:16；SCENE 16:9；PROP 16:9。
- 风格前缀由中台拥有，本 Skill 不选择、不拼接。

## production-source

- 从 task、rating、registry、state、disposition、anchor、prompt 和 usage 严格 JOIN。
- 模型不得手工增删生产任务或汇总 production source。

## prompt-closure

- ready task、slot、rendered prompt、production source 的 task_id 集合必须一致。
