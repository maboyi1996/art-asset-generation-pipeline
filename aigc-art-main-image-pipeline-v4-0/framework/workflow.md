# V4 自动化生产 Workflow

> 本文件由 framework/pipeline-contract.json 自动生成，请勿手工维护节点合同。

- 运行中无人介入、无 review queue、无动态规则修改。
- 默认正式交付为 deliverables/prompt-manifest.json。
- runtime gate 只检查机器结构，不评价语义精准性。

## 全局建档

| # | Node | Mode | Inputs | Outputs |
|---:|---|---|---|---|
| 1 | run-bootstrap | P | - | run-manifest |

## 模块一：剧本接入

| # | Node | Mode | Inputs | Outputs |
|---:|---|---|---|---|
| 2 | document-read | P | run-manifest | source-blocks |
| 3 | scene-segmentation | M→P | source-blocks | scene-boundary-factors, scenes |
| 4 | source-coverage-gate | P | source-blocks, scenes | source-coverage |

## 模块二：资产识别

| # | Node | Mode | Inputs | Outputs |
|---:|---|---|---|---|
| 5 | mention-scan | M+P | source-blocks, scenes, source-coverage | mention-scan-facts, raw-asset-mentions |
| 6 | mention-confirmation | M+P | raw-asset-mentions, source-blocks | mention-confirmation-facts, mention-dispositions |
| 7 | entity-resolution | M→P | mention-dispositions | entity-relation-factors, asset-entities, asset-aliases |
| 8 | evidence-ledger | M+P | asset-entities, mention-dispositions, scenes, source-blocks | evidence-facts, character-evidence, scene-evidence, prop-evidence |
| 9 | recognition-closure-gate | P | raw-asset-mentions, mention-dispositions, asset-entities, asset-aliases, character-evidence, scene-evidence, prop-evidence | recognition-closure |

## 模块三：资产规划

| # | Node | Mode | Inputs | Outputs |
|---:|---|---|---|---|
| 10 | candidate-admission | M→P | asset-entities, character-evidence, scene-evidence, prop-evidence, recognition-closure | admission-factors, asset-candidates, admission-dispositions, polluted-labels |
| 11 | asset-rating | M→P | asset-candidates, character-evidence, scene-evidence, prop-evidence | rating-factors, asset-ratings |
| 12 | base-asset-registration | P | asset-entities, asset-aliases, asset-candidates, asset-ratings | base-asset-registry |
| 13 | state-variant | M→P | base-asset-registry, asset-ratings, character-evidence, scene-evidence, prop-evidence | state-factors, asset-states, state-dispositions |
| 14 | asset-disposition | M→P | asset-candidates, asset-ratings, base-asset-registry, asset-states, character-evidence, scene-evidence, prop-evidence | disposition-factors, asset-dispositions |
| 15 | task-generation | P | asset-dispositions, base-asset-registry, asset-states, asset-ratings | production-tasks |
| 16 | episode-usage-map | P | production-tasks, character-evidence, scene-evidence, prop-evidence, scenes | episode-usage-map |
| 17 | planning-closure-gate | P | asset-candidates, admission-dispositions, polluted-labels, asset-ratings, base-asset-registry, asset-states, state-dispositions, asset-dispositions, production-tasks, episode-usage-map | planning-closure |

## 模块四：视觉生产

| # | Node | Mode | Inputs | Outputs |
|---:|---|---|---|---|
| 18 | asset-anchor | M+P | production-tasks, base-asset-registry, asset-states, character-evidence, scene-evidence, prop-evidence, planning-closure | anchor-facts, asset-anchors |
| 19 | prompt-slots | M+P | production-tasks, asset-anchors, asset-states, character-evidence, scene-evidence, prop-evidence | prompt-slot-facts, prompt-slots |
| 20 | prompt-render | P | prompt-slots | rendered-prompts |
| 21 | production-source | P | production-tasks, asset-ratings, base-asset-registry, asset-states, asset-dispositions, asset-anchors, rendered-prompts, episode-usage-map | main-image-production-source |
| 22 | prompt-closure-gate | P | production-tasks, asset-anchors, prompt-slots, rendered-prompts, main-image-production-source | prompt-closure |

## 模块五：交付

| # | Node | Mode | Inputs | Outputs |
|---:|---|---|---|---|
| 23 | pre-delivery-audit | P | run-manifest, source-coverage, recognition-closure, planning-closure, prompt-closure, main-image-production-source | production-audit |
| 24 | json-delivery | P | main-image-production-source, production-audit | prompt-manifest |
| 25 | human-view-delivery | P | main-image-production-source, production-audit | view-manifest |
| 26 | final-quality-gate | P | run-manifest, main-image-production-source, prompt-manifest, production-audit, prompt-closure, view-manifest | final-quality |
