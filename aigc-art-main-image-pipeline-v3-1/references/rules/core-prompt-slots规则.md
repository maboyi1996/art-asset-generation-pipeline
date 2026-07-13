# core-prompt-slots 规则

## 规则目的

约束 `prompt-generation.md` 只能把上游生产任务和证据转写为结构化槽位，不得直接手写整段最终 prompt。

## 输入依据

- `audit/global-task-draft.md`
- `audit/global-asset-registry.md`
- `audit/state-variant-result.md`
- `audit/character-anchor-result.md`
- `audit/production-audit-result.md`
- 三类 evidence ledger、分集映射和必要 source evidence

## 输出结果

`production-source/core-prompt-slots.md`

## 通用字段

每个槽位行必须包含：

| 字段 | 要求 |
|---|---|
| `task_id` | 必须来自 `audit/global-task-draft.md`，不得新造 |
| `asset_type` | 只允许 `character`、`scene`、`prop` |
| `task_type` | 只允许 `text_to_image`、`image_text_edit` |
| `base_asset_id` | 必须来自全局资产注册表 |
| `state_asset_id` | 仅状态任务填写，B/C 任务必须为空 |
| `slot_name` | 必须属于本规则列出的槽位 |
| `slot_value` | 只写正向可见事实或指定编辑事实 |
| `slot_status` | 只允许 `ready`、`missing_evidence`、`manual_review_required` |
| `source_evidence_ids` | 回指上游证据，多个值用英文逗号分隔 |
| `source_locator` | 回指剧本或上游产物定位 |
| `slot_issue` | 缺证据或人工复核原因 |

## 人物 text_to_image 必填槽位

| 槽位 | 内容边界 |
|---|---|
| `identity` | 年龄段、性别、身份、阶层、职业或一句话定位 |
| `face_features` | 脸型、骨相、五官比例、肤色、面部识别点 |
| `hair_and_decoration` | 发型、妆造、面部小物件、疤痕或标记 |
| `body_posture` | 肩颈、体型、年龄感、基础姿态 |
| `costume_visible_decoration` | 服装轮廓、材质、新旧状态、局部装饰 |
| `palette_memory_point` | 主色、辅助色、一眼不能丢的视觉记忆点 |
| `gaze` | 视线方向、眼神状态、心理暗示 |
| `expression` | 表情强度、嘴角、情绪克制程度 |
| `body_language` | 头部角度、肩颈状态、姿态张力 |
| `emotion_core` | 当前主设定图要体现的核心气质，不写剧情动作 |

## 场景 text_to_image 必填槽位

| 槽位 | 内容边界 |
|---|---|
| `scene_name` | 场景名称 |
| `space_identity` | 具体空间类型、所属地点或建筑层级、空间功能 |
| `scene_positioning` | 城市、区域、建筑级别、室内外、阶层属性 |
| `time_state` | 时间、天气或事件前后状态 |
| `story_function` | 场景承担的剧情功能 |
| `one_sentence_positioning` | 精准场景定位、核心空间锚点和功能 |
| `camera_space_relation` | 观察点、入口、过渡和主空间关系 |
| `visual_center` | 画面最重要的空间锚点 |
| `foreground` | 前景空间元素 |
| `midground` | 中景主空间和视觉中心 |
| `background` | 深处结构或延展空间 |
| `hidden_space_hint` | 不完整出现但需要暗示存在的区域 |
| `required_elements` | 必须出现的核心元素，多个元素用分号分隔 |
| `optional_details` | 可选辅助元素，多个元素用分号分隔 |
| `key_light` | 主光源 |
| `fill_light` | 辅助光 |
| `light_dark_relation` | 明暗关系 |
| `color_tendency` | 色彩倾向 |
| `air_state` | 空气状态 |
| `mood_core` | 氛围与情绪 |

## 道具 text_to_image 必填槽位

| 槽位 | 内容边界 |
|---|---|
| `prop_name` | 道具名称 |
| `object_identity` | 具体实体类型、核心结构、归属对象或势力 |
| `ownership_usage` | 归属、阶层属性、技术等级、实际用途 |
| `story_function` | 线索、武器、交易物、信物、身份凭证等剧情功能 |
| `one_sentence_positioning` | 精准道具定位、归属对象、用途和识别特征 |
| `required_elements` | 必须出现的核心部件，多个元素用分号分隔 |
| `optional_details` | 可选辅助结构，多个元素用分号分隔 |
| `overall_condition` | 新旧、破损、污渍、烧灼、氧化等整体状态 |

## image_text_edit 必填槽位

| 槽位 | 内容边界 |
|---|---|
| `identity_reference_image` | 已确认锚点图或锚点任务引用 |
| `identity_preservation` | 必须保持的人脸、年龄、体型和气质识别点 |
| `state_delta_prompt` | 只允许改变的可见状态差异 |
| `composition_preservation` | 需要保持的构图和背景规则 |

## 禁止内容

- 不得在正向槽位写“不要、不能、避免、不得、无 XX 设定、不加入 XX”等负向或排除式句子。
- 不得把动作戏、关系戏、剧情截图、镜头运动、对白、语气、声音写成外观槽位。
- 不得把缺失证据写成“无某物设定”；没有证据时使用 `slot_status: missing_evidence`。
- 不得在槽位中写题材世界段、画法段、风格库前缀、`{{include:...}}` 或旧英文写实摄影模板。
- 不得为 JSON/DOCX 需要而补造任务、ID、状态或锚点。

## 异常处理

必填槽位证据不足时，填写该槽位行并设置 `slot_status: missing_evidence`，`slot_value` 留空，`slot_issue` 写明缺口。渲染脚本必须失败并指回本层或上游证据层修复。
