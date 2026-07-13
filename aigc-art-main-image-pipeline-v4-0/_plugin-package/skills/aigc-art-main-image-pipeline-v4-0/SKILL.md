---
name: aigc-art-main-image-pipeline-v4-0
description: 当 Codex 需要读取中文剧本、小说草稿、分集短剧或项目剧本文档，并全自动生成忠于原文证据的人物、场景、道具主图生产 JSON 时使用本技能。V4.0.0 采用五模块 26 节点、JSON/JSONL 唯一机器事实源和 Python 确定性 ID/政策/任务/投影；运行中不请求人工复核，默认交付 Seedance prompt-manifest.json，DOCX/MD 仅按需派生。
---

# AIGC 主图资产自动生产 V4.0.0

把中文剧本自动转换为可导入中台的主图生产 JSON。人物、场景、道具必须平行完成识别、归一、证据、规划、提示词和交付链路。

## 运行原则

- 使用固定的 skill、pipeline、schema、policy 和 template 版本完成整次运行。
- 不在运行中修改规则，不询问用户如何处理中间项，不生成 review queue。
- 模型负责语义事实和视觉文学内容；Python 负责稳定 ID、固定映射、最终等级、状态、去向、任务、渲染、对账和 JSON。
- 精准性差异属于版本质量，不在单次运行中动态纠正；只有机器结构损坏才使本次运行失败。
- 默认只交付 `deliverables/prompt-manifest.json`。只有用户明确要求时才启用人审 MD/DOCX。

## 启动

1. 读取 `framework/pipeline-contract.json`。
2. 初始化 run：

```powershell
python scripts/run_pipeline.py init --source <script.docx|pdf|txt|md> --output-dir <project-output> --project-id <id> --project-title <title>
```

3. 严格按 contract 顺序执行 26 个节点。P 节点调用脚本；M→P/M+P 节点由当前 Codex 自动读取声明输入和对应规则，写入 factor JSONL，再立即调用 Python finalizer。
4. 模型 factor 只能包含 schema 允许字段，禁止创建最终 ID、等级、去向、task、prompt 或 ready 状态。
5. 每个节点完成后更新 run manifest。发生结构错误时停止本次任务并报告具体 artifact/record；不得把损坏结果伪装成成功。

## 模块命令

```text
scripts/ingest.py       document-read | scene-segmentation | source-coverage
scripts/recognition.py  mention-scan | mention-confirmation | entity-resolution | evidence-ledger | recognition-closure
scripts/planning.py     candidate-admission | asset-rating | base-registration | state-variant | asset-disposition | task-generation | episode-usage-map | planning-closure
scripts/visual.py       asset-anchor | prompt-slots | prompt-render | production-source | prompt-closure
scripts/delivery.py     pre-delivery-audit | json-delivery | human-view-delivery | final-quality
```

统一调用方式：

```powershell
python scripts/<module>.py --run-manifest <project-output/run-manifest.json> --action <action>
```

模型节点执行前，读取：

- contract 中该节点的 inputs、model_produces 和 forbidden_model_fields；
- 当前模块规则对应章节；
- factor artifact 指向的 schema；
- 当前输入 JSON/JSONL。

随后将完整 factor JSONL 写到 run manifest 声明路径，不得写 MD 表格。

## 精准性默认政策

- 主体关系证据不足时默认分开，不跨主体强合并。
- 明确可见主体默认保留；污染、动作、情绪、声音和抽象概念自动排除。
- 单集人物不能证明全部位于最长 15 秒单片段时默认 B。
- 可见 C 级人物保留独立 text_to_image 任务。
- B/C 不拆状态；image_text_edit 只用于同一人物 S/A 状态。
- Prompt 只使用可追溯证据，不补造外貌、空间和道具细节。
- PROP 固定横版 16:9；SCENE 16:9；ROLE 9:16。

## 长剧本分批执行

- 分集分场按显式集边界分批；mention/evidence 按集或有限 scene 批次处理；规划和 Prompt 按资产批次处理。
- 每批 factor 写入 staging/model-parts/<node>/*.jsonl，不把整部长剧本长期保留在对话上下文。
- 全部批次完成后运行：

```powershell
python scripts/model_gateway.py merge --run-manifest <run-manifest.json> --node <node-id> --parts-dir <parts-dir>
```

- merge 会拒绝同一业务键的冲突记录并校验 factor schema；合并完成后再运行节点 finalizer。
- 分批只改变上下文装载方式，不合并节点职责，不改变固定规则。

## 输出

```text
project-output/
├─ run-manifest.json
├─ machine/                       # 唯一机器事实源
│  └─ main-image-production-source.jsonl
├─ validation/                    # 机器结构检查
├─ deliverables/
│  └─ prompt-manifest.json        # 默认正式交付
└─ views/                         # 默认仅有 view-manifest；按需派生 MD/DOCX
```

最终质量报告必须写明 `precision_claim: not_evaluated_at_runtime`。它只证明机器结构和交付文件可用，不宣称剧本资产绝对无漏项。

## 资源导航

- 唯一 DAG 与 artifact 合同：`framework/pipeline-contract.json`
- 人类可读流程：`framework/workflow.md`
- 五模块语义规则：`rules/*.md`
- 字段与枚举：`contracts/*.schema.json`
- 固定政策：`policies/*.json`
- Prompt 与可选视图模板：`templates/*.json`
- 语义自检：`guards/*.md`
- 确定性实现：`scripts/*.py`
