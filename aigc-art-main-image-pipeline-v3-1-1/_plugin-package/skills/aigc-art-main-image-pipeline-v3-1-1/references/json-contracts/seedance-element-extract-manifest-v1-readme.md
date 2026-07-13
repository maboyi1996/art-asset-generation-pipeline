# 元素提取 Agent JSON 格式包 v1

用途：给业务人员、外部供应商或 AI skill 输出可导入元素库、并可用于主图生成的元素清单。

交付文件名必须是：

```text
prompt-manifest.json
```

格式版本必须是：

```text
seedance-element-extract-manifest.v1
```

## 必填要求

1. JSON 根节点必须是对象，不能是数组。
2. 不要包 Markdown 代码块，不要写注释，不要用 JSON5。
3. 新输出统一使用 `assets` 数组。
4. `contentId` 这类 ID 必须用字符串，不要用数字。
5. `templateType` 只能是 `ROLE`、`SCENE`、`PROP`。
6. 每个元素必须有 `templateName`、`templateType`、`appearance.appearances`。
7. 每个状态必须有 `name` 和 `imagePrompt`。
8. 一个角色/场景/道具有多个视觉状态时，不要拆成多个元素，放在同一个元素的 `appearances` 数组里。

## 字段说明

| 字段 | 是否必填 | 说明 |
| --- | --- | --- |
| `schemaVersion` | 必填 | 固定为 `seedance-element-extract-manifest.v1` |
| `manifestVersion` | 建议 | 文件自身版本，例如 `1.0` |
| `generationScope` | 建议 | 主图任务使用 `main_image_only` |
| `contentId` | 建议 | 项目 ID，字符串 |
| `source.skillId` | 建议 | 生成该文件的 skill 名称 |
| `project.title` | 建议 | 项目名称 |
| `summary.totalItems` | 建议 | 元素总数 |
| `summary.manualReviewItems` | 建议 | 需人工复核数量 |
| `assets[].assetId` | 建议 | 生成方稳定 ID |
| `assets[].templateName` | 必填 | 元素名称 |
| `assets[].templateType` | 必填 | `ROLE`、`SCENE`、`PROP` |
| `assets[].description` | 建议 | 元素描述 |
| `assets[].appearance.appearances[].name` | 必填 | 状态名称 |
| `assets[].appearance.appearances[].episodes` | 建议 | 出现集数 |
| `assets[].appearance.appearances[].imageRatio` | 建议 | 角色常用 `9:16`，场景常用 `16:9`，道具按模型要求 |
| `assets[].appearance.appearances[].imagePrompt` | 必填 | 可直接用于主图生成的正向提示词 |
| `assets[].appearance.appearances[].negativePrompt` | 建议 | 负向提示词 |
| `assets[].appearance.appearances[].priority` | 建议 | `S`、`A`、`B`、`C` |
| `assets[].appearance.appearances[].generation.method` | 建议 | `text_to_image`、`image_to_image`、`image_text_edit` |
| `assets[].appearance.appearances[].generation.referenceTaskId` | 编辑图必填 | `image_text_edit` 使用的锚点/参考任务 ID |

## 最小可导入示例

```json
{
  "schemaVersion": "seedance-element-extract-manifest.v1",
  "manifestVersion": "1.0",
  "generationScope": "main_image_only",
  "contentId": "326706045055401984",
  "assets": [
    {
      "assetId": "role_tang_ning",
      "templateName": "棠宁",
      "templateType": "ROLE",
      "description": "聪慧隐忍的女主，外柔内刚。",
      "appearance": {
        "appearances": [
          {
            "stateId": "role_tang_ning_plain",
            "name": "素衣常服",
            "episodes": [1, 2],
            "imageRatio": "9:16",
            "imagePrompt": "Chinese historical drama heroine, plain light robe, calm but resilient expression, clean face identity, cinematic portrait, no text, no watermark.",
            "negativePrompt": "modern clothes, wrong age, duplicate face, text, watermark",
            "priority": "S",
            "status": "ready",
            "generation": {
              "method": "text_to_image"
            }
          }
        ]
      }
    }
  ]
}
```

## 包内文件

- `README.md`：给业务人员看的说明。
- `contract.md`：给开发和自动化系统看的字段规则与兼容说明。
- `prompt-manifest.example.json`：标准样例，可复制后改内容。
- `seedance-element-extract-manifest.v1.schema.json`：给开发或自动化系统使用的 JSON Schema。
- `element-extract-json-v1.zip`：对外发送的下载包。
