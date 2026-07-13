# V4 维护者迭代门禁

## 产品边界

- V4 是全自动剧本到中台 JSON 的生产 Skill。
- 单次运行无人介入、无中间复核、无动态规则调整。
- 精准性属于版本质量；运行时只检查机器结构和交付可用性。
- 默认正式交付为 prompt-manifest.json；MD/DOCX 仅按需派生。

## 架构硬约束

- 五大业务模块、26 个逻辑节点、15 P / 6 M→P / 5 M+P / 0 模型独立执行。
- JSON/JSONL 是唯一机器事实源。
- Python 拥有稳定 ID、固定政策、最终计算、任务、映射、渲染、对账和放行。
- 人物、场景、道具必须使用平行的数据血缘和 closure。
- pipeline-contract.json 是 DAG、artifact、producer/consumer 和节点 mode 的唯一事实源。
- 不允许 pipeline.yaml、手写 workflow 双事实源或 MD 机器事实源。

## 运行时错误边界

只阻止：不可读输入、schema 错误、重复 ID、主外键断裂、必需产物缺失、ready task 未交付和损坏 JSON。

不阻止：少量次要资产差异、评级边界差异、状态数量差异、结构合法的语义偏差和 Prompt 后续优化空间。

## 版本迭代

- 发布版本在整次 run 中冻结 rule/schema/policy/template hash。
- 生产反馈进入后续 PATCH/MINOR，不回写已经完成的 run。
- 关键资产精准性只在开发/发布 benchmark 中验收。
- V3.2 固定为 non-production reference，不安装、不发布。
