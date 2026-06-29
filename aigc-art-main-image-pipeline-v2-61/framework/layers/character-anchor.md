# character-anchor.md

## 作用

建立 S/A 人物项目级脸模锚点，处理 B 级人物单集脸模一致要求，并为状态图建立锚点依赖。

## 输入

`global-task-draft`、`asset-rating-result`、`state-variant-result`

## 调用文件

- `references/rules/角色锚定规则.md`
- `references/rules/任务类型字段审核规则.md`

## 输出结果

`character-anchor-result`

## 边界

只处理人物锚定，不重新评级、不补建任务、不生成最终提示词。发现基础人物任务缺失时，输出锚定问题并指回 `task-manifest-generation.md`。
