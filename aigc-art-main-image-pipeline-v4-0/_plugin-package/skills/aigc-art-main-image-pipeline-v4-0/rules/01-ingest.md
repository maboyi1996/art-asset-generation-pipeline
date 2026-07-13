# 模块一：剧本接入与场次规则

## document-read

- 读取 DOCX、PDF、TXT、MD；按原顺序生成不可变 source blocks。
- 每个 block 必须保存定位、文本和 SHA-256；不得概括、改写或跳过空白之外的正文。
- 文档读取失败属于机器完整性错误；不得猜测缺失正文。

## scene-segmentation

- 模型只提交 block 分组、原始集标题、场标题、地点、时间和置信事实，不创建 episode_id 或 scene_id。
- Python 按 source block 顺序生成稳定 episode/scene ID。
- 模糊边界仍必须自动定案；优先服从显式“第X集”、场次标题、地点/时间切换和连续动作关系。
- 同名标题不共享 ID；重复标题由 Python 加稳定顺序区分。

## source-coverage

- 每个非空 source block 必须恰好属于一个 scene。
- 漏块、重复归属和未知 block ID 属于结构错误。
- 本 gate 只证明正文被完整路由，不宣称资产识别绝对无漏项。
