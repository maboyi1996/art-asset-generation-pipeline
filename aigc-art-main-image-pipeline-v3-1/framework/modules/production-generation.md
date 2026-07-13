# 模块：资产生产与提示词生成

## 作用

基于全局任务草稿、base asset 注册和状态索引建立角色锚点，做生产前一致性审计，并为可生产任务生成 core prompt 槽位，再由脚本渲染主图提示词或状态编辑指令。

## 层级顺序

`character-anchor.md -> production-audit.md -> prompt-generation.md -> render_core_prompts.py`

## 边界

本模块读取前序资产、状态、评级、去向、任务草稿和映射结果，不重新抽取资产、不重新拆状态、不重新评级、不补建任务。`prompt-generation.md` 只产出槽位表，不手写整段 prompt；`render_core_prompts.py` 只渲染和校验，不补写证据。
