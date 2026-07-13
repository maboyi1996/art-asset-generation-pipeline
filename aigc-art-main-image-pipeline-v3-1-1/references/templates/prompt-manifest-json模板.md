# prompt-manifest.json 模板

## 文件名

`deliverables/prompt-manifest.json`

## 输出要求

输出必须是纯 JSON 文件，不能包 Markdown 代码块，不能有注释，不能使用 JSON5。

## 顶层结构

```json
{
  "schemaVersion": "seedance-element-extract-manifest.v1",
  "manifestVersion": "1.0",
  "generationScope": "main_image_only",
  "source": {
    "skillId": "aigc-art-main-image-pipeline-v3-1-1",
    "skillVersion": "3.1.1",
    "generatedAt": "ISO-8601 datetime with timezone",
    "promptMode": "core_prompt_requires_style_prefix",
    "stylePrefixOwner": "middle_platform",
    "stylePrefixRequired": true,
    "artifactManifest": "artifact-manifest.json"
  },
  "project": {
    "title": "项目名"
  },
  "summary": {
    "totalItems": 0,
    "manualReviewItems": 0
  },
  "assets": []
}
```

`contentId` 仅在用户或上游输入明确提供时加入，且必须是字符串。

## assets[] 结构

```json
{
  "assetId": "base_asset_id",
  "templateName": "资产名称",
  "templateType": "ROLE",
  "description": "元素说明",
  "appearance": {
    "description": "整体外观说明",
    "appearances": [
      {
        "stateId": "task_or_state_id",
        "name": "默认状态",
        "episodes": [1],
        "imageRatio": "9:16",
        "imagePrompt": "等待中台拼接风格前缀的中文 core prompt 或中文状态编辑 core instruction",
        "negativePrompt": "中文负向约束",
        "priority": "S",
        "status": "ready",
        "generation": {
          "method": "text_to_image"
        },
        "reviewFocus": "审核关注点"
      }
    ]
  },
  "metadata": {
    "source": "agent",
    "taskIds": ["task_id"],
    "firstAppearance": "E01-S001",
    "evidenceSummary": "证据摘要"
  }
}
```

## templateType 映射

| `asset_type` | `templateType` |
|---|---|
| `character` | `ROLE` |
| `scene` | `SCENE` |
| `prop` | `PROP` |

## imageRatio 默认值

| `templateType` | `imageRatio` |
|---|---|
| `ROLE` | `9:16` |
| `SCENE` | `16:9` |
| `PROP` | `1:1` |

## 状态数组要求

- 一个 base asset 只生成一个 `assets[]` 元素。
- 同一 base asset 的基础图和 S/A 状态图都放入同一个 `appearance.appearances[]`。
- B/C 只允许基础图进入 `appearances[]`，不得生成多状态项。
- `excluded` 任务不得进入 `appearances[]`。
- `manual_review_required` 可进入，但必须保留状态和审核关注点。
- `image_text_edit` 必须在 `generation.referenceTaskId` 中保留 `anchor_task_id`。
- V3.1.1 中 `imagePrompt` 不得包含题材世界段、画法段、`{{include:...}}`、风格前缀或旧英文写实模板残留。
