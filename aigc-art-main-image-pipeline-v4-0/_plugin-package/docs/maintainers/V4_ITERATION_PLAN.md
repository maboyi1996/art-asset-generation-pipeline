# V4.0.0 自动化生产实施记录

状态：源码候选已实现并通过离线自动测试；完整剧本 benchmark 与中台图片验收待完成，未安装、未发布。

## 实施顺序

1. 冻结 V3 基线并重写维护门禁。
2. 建立唯一 pipeline contract、26 节点和 grouped schemas。
3. 实现公共 ID、storage、contract、policy、validator 和 model factor gate。
4. 实现 ingest、recognition、planning、visual、delivery 五模块。
5. 默认输出 prompt-manifest.json，可选派生 MD/DOCX。
6. 运行合同、结构、负向和端到端 fixture。
7. 使用万劫断链样本、春棠欲醉人工对照和完整原始剧本完成发布 benchmark。

## 发布硬门槛

- 主角、重要配角、核心场景和关键道具不得明显漏项或错合。
- 关键资产必须追溯到原文 evidence。
- 机器事实主外键、task/usage/anchor/prompt/source/JSON 集合必须一致。
- JSON 可导入中台。
- 次要资产、等级、状态和 Prompt 允许少量合理差异，后续版本优化。

## 当前发布状态

allow_implicit_invocation=false。完整剧本 benchmark 和中台导入验收前不得更新 cachebuster、安装插件或宣称稳定生产。
