# 模块三：资产决策与任务规划规则

## candidate-admission

- 模型只提交可见性、主体稳定性、污染、非视觉性和视觉形态事实。
- Python 自动定案；不允许 manual_review_required 或 blocking_review。
- 明确可见主体默认保留；污染短语和非视觉内容自动进入明确排除结果。

## asset-rating

- 模型提交跨集、频次、主线依赖、设计需求和单片段事实；不得提交 S/A/B/C。
- Python 按 rating policy 定案。
- 单集人物不能证明全部位于最长 15 秒单片段时默认 B，不降 C。
- 关键跨集资产优先 S/A；场景和道具使用同一计算框架及类型差异政策。

## base-asset-registration

- Python 从 entity/candidate/rating 生成稳定 base_asset_id。
- 人物、场景、道具必须使用同一 ID 和血缘框架。

## state-variant

- 只有稳定可见差异才拆状态；瞬时动作和情绪不拆状态。
- S/A 可拆状态；B/C 固定 base_only。
- 模型只提交状态事实，Python 生成 state ID 和结果。

## asset-disposition

- 每个注册资产必须自动得到 production_task、alias_to、grouped_into、excluded 或 not_visual_candidate。
- 可见且有独立视觉需求的资产默认 production_task。
- 不存在人工复核去向。

## task-generation

- Python 生成全部 task、anchor 引用和 ready 状态。
- 可见 C 级人物保留独立 text_to_image 任务。
- image_text_edit 仅限人物状态，且必须引用同 base 的 text_to_image 基础任务。

## episode-usage-map

- task 的 episode/scene/evidence 映射从机器事实自动投影，不允许模型手工汇总。

## planning-closure

- 对账 candidate、rating、registry、state、disposition、task 和 usage。
- 本 gate 只检查内部结构，不评价与人工资产表的轻微差异。
