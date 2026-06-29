# asset-rating.md

## 作用

给每个 base asset 评定制作连续性等级 `S/A/B/C`。人物跨集评级只统计同一具体人物的可见脸模生产出场。

## 输入

`asset-candidate-list`、`state-variant-result`、`scene-coverage-table`

## 调用文件

- `references/rules/人物评级规则.md`
- `references/rules/场景评级规则.md`
- `references/rules/道具评级规则.md`

## 输出结果

`asset-rating-result`

## 边界

本层是唯一正式评级层。后续层读取 `asset-rating-result`，不得重新评级。
