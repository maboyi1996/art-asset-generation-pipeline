# 模块二：三类资产识别与证据规则

## mention-scan

- 对每个 scene 分别高召回扫描人物、场景、道具。
- 人物覆盖实名、称谓、身份称呼、泛称、画像、尸体、梦境和回忆中可见主体。
- 场景覆盖具体可画空间，不把抽象地域、方向词和纯叙事地点当资产。
- 道具覆盖具体可见物件，不把动作、概念、能力、声音和台词修饰当道具。
- 模型只提交提及事实；Python 生成 mention_id 并去除完全重复记录。

## mention-confirmation

- 确认提及是否真实存在、资产类型和可见性；不得以“生产价值低”为由删除真实可见主体。
- 动作、情绪、语气、纯声音、不可见抽象概念自动排除，并保留排除原因。
- 不设置人工待确认状态；必须自动 accepted 或 excluded。

## entity-resolution

- 同一主体合并需要明确称谓、上下文、身份或连续性证据。
- 证据不足时默认不跨主体合并；泛称默认只在本场或本集范围归一。
- 模型提交 canonical name、scope key 和关系依据；Python 生成 entity/alias ID。
- 同名异人必须通过 scope key 分离。

## evidence-ledger

- 每个 accepted mention 至少生成一条可追溯 evidence。
- evidence 必须引用 source block、scene、mention、entity 和原文片段。
- 视觉事实、设计线索和状态线索只能来自原文，不补造外貌、空间或材质。

## recognition-closure

- 检查 accepted mention、entity、evidence 的主外键和集合闭环。
- 不能证明剧本中不存在未扫描主体；精准性通过离线 benchmark 评估。
