# asset-registry.md

## 作用

合并候选资产别名，生成稳定 base asset ID，并输出可追踪的别名归并关系。

## 输入

`asset-candidate-list`、`asset-rating-result`

## 调用文件

`references/rules/资产注册规则.md`

## 输出结果

`global-asset-registry`、`alias-resolution-map`

## 边界

本层只做 base asset 注册和别名归并：不重新抽取资产、不重新拆状态、不生成状态 ID、不重新评级、不生成人物候选去向、不生成污染标签清洗记录、不生成 `global-task-draft`、不生成分集映射、不建立脸模锚点、不生成提示词。可转移称谓和别名合并必须保留证据；证据不足时默认不合并，并把不确定性留给下游审计读取。
