# 模块五：中台交付与机器完整性规则

## pre-delivery-audit

- 汇总四个结构 gate、run manifest 和 production source 的机器状态。
- 不在运行时与人工 benchmark 比较，不宣称语义结果绝对精准。

## json-delivery

- prompt-manifest.json 是默认正式交付。
- 只能从 main-image-production-source.jsonl 生成。
- skill/schema/policy/template 版本来自冻结 run manifest；artifact 路径必须相对。
- 所有 appearance 状态固定 ready；manual review 状态不得进入 V4 JSON。

## human-view-delivery

- 默认关闭。仅在 include_human_views=true 或用户明确要求时生成 MD/DOCX。
- 派生视图不得成为机器输入，也不参与默认放行。

## final-quality

- 只检查机器结构和交付可用性。
- 输出 precision_claim=not_evaluated_at_runtime。
- 精准性由发布前 benchmark 和最终图片反馈评估，后续版本改规则，不回写当前 run。
