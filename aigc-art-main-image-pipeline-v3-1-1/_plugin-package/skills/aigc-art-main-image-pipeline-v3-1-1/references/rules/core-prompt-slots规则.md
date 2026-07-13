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
| `slot_value` | 只写正向、具体、可画的视觉细节或指定编辑事实 |
| `slot_status` | 只允许 `ready`、`missing_evidence`、`manual_review_required` |
| `source_evidence_ids` | 回指上游证据，多个值用英文逗号分隔 |
| `source_locator` | 回指剧本或上游产物定位 |
| `slot_issue` | 缺证据或人工复核原因 |

## 槽位值可画视觉细节准入规则

`slot_value` 的目标不是解释资产为什么成立，而是给图像生成提供可以画出来的可见信息。槽位表中的维度是填写方向，不是允许输出抽象词的占位符。

合格槽位值必须满足：

- 人物槽位写脸型、骨相、五官、发型、妆造、服装轮廓、材质、颜色、姿态、眼神、表情强度等可见细节。
- 场景槽位写空间类型、观察点、入口、前景、中景、背景、核心元素、材质状态、光源、色彩倾向、空气状态等可见细节。
- 道具槽位写实体类型、核心结构、部件、材质、颜色、新旧状态、磨损、污渍、使用痕迹等可见细节。
- 如果剧本证据不足但该任务仍应生产，只能填由身份、时代、资产类型和上游审计可支撑的保守视觉默认；无法支撑时使用 `missing_evidence` 或 `manual_review_required`。

以下内容不能作为 `slot_value` 独立使用：身份由称谓确定、与身份气质一致、符合阶层属性、自然、端正、稳定、清楚、有辨识度、核心气质明确、古典盘发或长发造型、服装与身份相符。它们最多只能作为理解方向，必须转写成可见细节。

本节样例来自 V5 模板库，迁移到规则层作为“合格细节密度和可画程度”标准。执行时必须根据当前剧本证据改写，不得把样例当作固定文案复用。A/B 题材世界和画法段不进入本规则。

### 人物槽位样例

| 槽位 | 合格写法片段 |
|---|---|
| `identity` | Dane，21-24 岁，年轻男性，来自 Watson 的年轻街头佣兵，低级 edgerunner，街头赌徒。精瘦、紧绷、街头化，带年轻人的冲动、轻微自负和尚未被彻底磨平的锋利感。 |
| `face_features` | 瘦削棱角脸，脸型偏窄但不病态，颧骨紧，下颌利落，眉骨清楚，鼻梁直，脸部结构面明确。深色眼睛，眼睑略压，直鼻，嘴唇偏干，唇形清楚。偏白橄榄肤调，有轻微不均匀色彩变化和少量细小街头磨损痕迹。 |
| `hair_and_decoration` | 短而凌乱的深色头发，顶部略蓬松，发束有明显方向感。上唇和下巴有轻微胡茬。鼻梁上有一条小型肤色胶布或修补贴，左眉上方有小型金属眉钉，左脸颊靠近眼下位置有小字样标记，耳朵带简单耳环。 |
| `body_posture` | 精瘦、轻但紧绷的年轻街头佣兵体型。肩窄但有张力，颈部修长，锁骨与胸锁乳突肌可见，像长期处在戒备状态中。 |
| `costume_visible_decoration` | 荧光绿与碳黑拼接机车夹克，夹克有磨损、掉漆、旧化和廉价未来工业感。内搭黑色做旧 T 恤，胸前有明显红色图形。颈部两侧和锁骨上方有低价外露式接口，领口边缘可见少量黑色线缆和简化机械接点。 |
| `palette_memory_point` | 荧光绿为主识别色，碳黑为主体基底，辅以少量冷青色边缘反光。绿色鲜明但不刺眼，是角色一眼不能丢的视觉记忆点。 |
| `gaze` | 带伤的傲气眼神，轻微挑衅，不安而戒备。视线平静但带压迫感，眼神里有伤、讽刺感、不服输和没愈合的痛。 |
| `expression` | 克制的痞气半笑。嘴上还在逞强，愤怒、痛感和戒备被压在表面之下，表情强度低而锋利。 |
| `body_language` | 头部略微偏转，肩颈放松中带轻微绷劲，姿态克制，整体接近角色资产图状态。 |
| `emotion_core` | 年轻、冷、傲、带伤、克制、街头感明确；失去、愤怒和底层生存压力转译为傲气、敌意和逞强。 |

### 场景槽位样例

| 槽位 | 合格写法片段 |
|---|---|
| `scene_name` | 暴雨中的 Night City 霓虹天际线 |
| `space_identity` | 暴雨夜晚的赛博朋克巨型城市高空建立镜头，由多层钢铁高速路网、商业全息广告牌和密集发光塔楼组成。 |
| `scene_positioning` | Night City 巨型都市夜景，高空室外视角，企业商业区与高架交通系统交叠，公共城市空间，企业压迫型赛博朋克城市尺度场景。 |
| `time_state` | 夜晚，暴雨中。 |
| `story_function` | 建立城市规模、企业冷漠、街道黑暗和悲剧余韵。 |
| `one_sentence_positioning` | 暴雨中由企业霓虹、高架交通和巨型广告压迫出来的 Night City 高空建立镜头。 |
| `camera_space_relation` | 高空航拍视角看向城市深处，视线从前景低位高速线条穿过雨幕，进入中景钢铁路网，再延伸到背景垂直城市峡谷和巨型广告牌。 |
| `visual_center` | 巨型商业全息广告牌，以及雨夜城市峡谷中的冷硬企业光。 |
| `foreground` | 湿冷高速路面、钢铁护栏、红色车辆尾灯拖痕消失在雨中。 |
| `midground` | 多层钢铁高速路网、雨雾中的城市交通结构、霓虹光反射。 |
| `background` | 垂直城市峡谷、密集发光塔楼、巨型商业全息广告牌。 |
| `hidden_space_hint` | 街道底层黑暗、远处车辆流动、被企业光吞没的低层城市空间。 |
| `required_elements` | 多层钢铁高速路网 + 湿冷金属护栏 + 暴雨反光；湿沥青路面 + 雨水覆盖 + 真实暗部反射；红色车辆尾灯拖痕 + 雨中模糊 + 向城市深处消失；密集玻璃塔楼群 + 夜间发光窗口 + 雨雾遮罩。 |
| `optional_details` | 垂直城市峡谷 + 玻璃与钢铁立面 + 冷色霓虹污染；雨幕 + 真实空气散射；街道黑暗缝隙 + 自然暗部；远处小型车辆灯流 + 雨雾遮挡。 |
| `key_light` | 霓虹城市光、巨型商业全息广告牌光。 |
| `fill_light` | 红色车辆尾灯、塔楼窗口光、湿路面反光、远处城市光晕。 |
| `light_dark_relation` | 自然暗部保留，街道黑暗与企业硬光形成压迫对比。 |
| `color_tendency` | 冷色霓虹、玻璃蓝灰、雨夜黑色、少量红色尾灯。 |
| `air_state` | heavy rain、rain curtain、rain haze、真实空气散射。 |
| `mood_core` | 城市尺度冷漠，企业光覆盖街道黑暗，人在城市系统中被压低和吞没；空间寒冷、潮湿、宏大、无情。 |

### 道具槽位样例

| 槽位 | 合格写法片段 |
|---|---|
| `prop_name` | Wes 的刮花不锈钢香烟盒 |
| `object_identity` | 一个薄型、扁平、长方形的金属铰链香烟盒，属于街头 solo 佣兵长期随身携带的旧式个人收纳物。实体结构为可反复开合、专门用来存放香烟的金属香烟盒。 |
| `ownership_usage` | 属于 Wes，一名长期在夜之城底层生存的 wandering street solo。阶层属性为街头佣兵个人随身物件，技术等级低，结构以机械铰链和金属壳体为主，强调耐用、便携和长期使用痕迹。 |
| `story_function` | 情绪锚点、角色生活痕迹、身份线索、私人物件。技术等级低，个人旧物属性明确，反映长期流浪、街头生存和旧帮派接触痕迹。 |
| `one_sentence_positioning` | Wes 这个街头 solo 长期贴身携带、严重刮花但仍在使用的不锈钢香烟盒。 |
| `required_elements` | 香烟盒主体外壳 + 拉丝不锈钢材质 + 冷灰银色 + 长期使用后的密集划痕、细碎磨痕和轻微反光衰减；盒盖与盒身接缝 + 金属结构缝 + 暗灰细缝色 + 浅而清楚的 lid seam；铰链结构 + 不锈钢金属 + 深灰银色 + 长期开合后的磨损。 |
| `optional_details` | 盒身局部压痕 + 不锈钢面板 + 暗灰凹陷阴影 + 轻微 dents；表面拉丝方向变化 + 金属工艺纹理 + 冷灰亮面与暗面交替；边缘厚度暗示 + 金属切边结构 + 银灰色。 |
| `overall_condition` | heavily used but functional。整体为严重使用过、明显刮花、带旧胶痕、轻微磕碰和边角磨圆的状态，结构完整，仍可正常开合和继续使用。 |

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
