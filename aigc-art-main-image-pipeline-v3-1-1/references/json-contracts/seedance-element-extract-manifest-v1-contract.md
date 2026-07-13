# Seedance Element Extract Manifest JSON v1

This contract defines the JSON file that an agent skill should output when it extracts project elements and prepares main-image generation prompts for the Seedance element library.

The canonical output filename is:

```text
deliverables/prompt-manifest.json
```

The schema id is:

```text
seedance-element-extract-manifest.v1
```

## Recommended Shape

Use the unified `assets` structure for new skills. It maps cleanly to the element library and supports multiple visual states per role, scene, or prop.

```json
{
  "schemaVersion": "seedance-element-extract-manifest.v1",
  "manifestVersion": "1.0",
  "generationScope": "main_image_only",
  "contentId": "326706045055401984",
  "source": {
    "skillId": "aigc-art-main-image-pipeline-v3-1-1",
    "skillVersion": "3.1.1",
    "generatedAt": "2026-06-22T17:35:20+08:00",
    "promptMode": "core_prompt_requires_style_prefix",
    "stylePrefixOwner": "middle_platform",
    "stylePrefixRequired": true,
    "artifactManifest": "artifact-manifest.json"
  },
  "project": {
    "title": "示例项目"
  },
  "summary": {
    "totalItems": 3,
    "manualReviewItems": 0
  },
  "assets": [
    {
      "assetId": "role_tang_ning",
      "templateName": "棠宁",
      "templateType": "ROLE",
      "description": "聪慧隐忍的女主，外柔内刚。",
      "appearance": {
        "description": "青年女性，古装短剧气质，清冷坚韧。",
        "appearances": [
          {
            "stateId": "role_tang_ning_plain",
            "name": "素衣常服",
            "episodes": [1, 2],
            "imageRatio": "9:16",
            "imagePrompt": "人物胸像主设定图，竖版9:16，单人居中，中性灰背景。棠宁，青年女性，素衣常服，清冷坚韧，脸型干净，眼神克制但有韧性。不要其他人物，不要场景，不要动作戏，不要可读文字或水印。",
            "negativePrompt": "不要现代服装，不要年龄错误，不要重复脸，不要其他人物，不要可读文字，不要水印。",
            "priority": "S",
            "status": "ready",
            "generation": {
              "method": "text_to_image"
            },
            "reviewFocus": "年龄、脸型、服装颜色必须稳定"
          }
        ]
      },
      "metadata": {
        "source": "agent",
        "firstAppearance": "E01-S001",
        "evidenceSummary": "第1集首次出场，是主要女性角色。"
      }
    }
  ]
}
```

## Field Rules

| Field | Required | Rule |
| --- | --- | --- |
| `schemaVersion` | Yes | Must be `seedance-element-extract-manifest.v1`. |
| `manifestVersion` | Recommended | Producer-facing version for this file. |
| `generationScope` | Recommended | Use `main_image_only` when the file is for element import plus main-image prompts. |
| `contentId` | Recommended | String ID. Do not output large numeric IDs as JSON numbers. |
| `source.skillId` | Recommended | Skill identifier that generated the file. |
| `project.title` | Recommended | Human-readable project title. |
| `summary.totalItems` | Recommended | Total asset count. |
| `summary.manualReviewItems` | Recommended | Count of assets or states needing manual review. |
| `assets` | Yes | Canonical element list for new skills. |
| `assets[].assetId` | Recommended | Stable producer-side ID. |
| `assets[].templateName` | Yes | Display name in the element library. |
| `assets[].templateType` | Yes | `ROLE`, `SCENE`, or `PROP`. |
| `assets[].description` | Recommended | Human-readable element description. |
| `assets[].appearance.appearances` | Yes | Visual states for this element. At least one state should be supplied. |
| `appearances[].name` | Yes | State name, such as `常服`, `夜景`, or `破损状态`. |
| `appearances[].episodes` | Recommended | Positive episode numbers where the state appears. |
| `appearances[].imageRatio` | Recommended | `9:16` for roles, `16:9` for scenes, `1:1` or model-specific ratio for props. |
| `appearances[].imagePrompt` | Yes | In V3.1.1, Chinese core prompt awaiting middle-platform style-prefix concatenation. |
| `appearances[].negativePrompt` | Recommended | Chinese negative prompt. |
| `appearances[].priority` | Recommended | `S`, `A`, `B`, or `C`. |
| `appearances[].status` | Recommended | Use `ready` when the state can be generated. |
| `appearances[].generation.method` | Recommended | `text_to_image`, `image_to_image`, or `image_text_edit`. |
| `appearances[].generation.referenceTaskId` | Required for `image_text_edit` | Stable source task ID for the reference/anchor image. |
| `metadata` | Optional | Audit information. Do not put import-critical fields only in metadata. |

## Current Import Compatibility

The current frontend import path recognizes this recommended `assets` structure. It also recognizes older prompt-manifest structures containing:

- `items`
- `main_image_tasks`
- `asset_state_tasks`
- `roleList`
- `sceneList`
- `propList`

For new skills, prefer `assets`. The older task-list fields are compatibility paths and should not be the primary contract for new output.

## Skill Output Requirements

Agent skills that generate element extraction artifacts must follow these rules:

- Output a real JSON file named `prompt-manifest.json`.
- Do not wrap JSON in Markdown fences.
- Do not output comments or JSON5 syntax.
- Use `assets` as the canonical top-level element list.
- Use `ROLE`, `SCENE`, and `PROP` for `templateType`.
- Put Chinese core prompts in `appearance.appearances[].imagePrompt`; style-prefix concatenation is handled outside this skill.
- Use string values for large IDs.
- Keep each visual state as a separate `appearances[]` item.
- If a later state depends on a previous image, set `generation.method` to `image_to_image` or `image_text_edit` and include a stable reference field in `generation`.

## Schema And Example

- JSON Schema: `seedance-element-extract-manifest.v1.schema.json`
- Example: `prompt-manifest.example.json`
