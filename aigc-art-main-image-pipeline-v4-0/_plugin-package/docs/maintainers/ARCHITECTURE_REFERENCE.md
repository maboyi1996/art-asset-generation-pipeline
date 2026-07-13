# V4 自动化生产架构参考

## 单一合同

framework/pipeline-contract.json 定义 26 节点、输入输出、model factors、Python outputs、schema、executor、validator、producer 和 consumer。workflow.md 与 NODE_CONTRACTS.md 自动生成。

## 五模块公共入口

- ingest.py：文档、场次和原文覆盖。
- recognition.py：三类 mention、entity、evidence 和结构 closure。
- planning.py：候选、评级、注册、状态、去向、task 和 usage。
- visual.py：三类 anchor、slots、Prompt 渲染和 production source。
- delivery.py：机器审计、中台 JSON、可选视图和 final quality。

模块内部允许合理拆分；文件数量不是验收 KPI。公共能力位于 scripts/core。

## 模型与 Python 边界

模型阶段分别提交语义 factor，不因为节省调用而强行合并扫描、确认、归一、准入、评级、状态和去向。Python 拒绝模型提交最终 ID、等级、去向、task、prompt 和 ready 状态。

## 自动默认政策

- 不确定主体默认分开。
- 明确可见主体召回优先保留。
- 单集人物缺少 15 秒正证据时默认 B。
- 可见 C 级人物独立出图。
- B/C 不拆状态。
- 动作、情绪、声音、抽象概念和污染短语自动排除。

## 交付边界

machine/*.json|jsonl 是机器事实。deliverables/prompt-manifest.json 是默认交付。views 和 DOCX 默认关闭，且永不成为机器输入。final-quality 只声明机器完整性，并固定 precision_claim=not_evaluated_at_runtime。
