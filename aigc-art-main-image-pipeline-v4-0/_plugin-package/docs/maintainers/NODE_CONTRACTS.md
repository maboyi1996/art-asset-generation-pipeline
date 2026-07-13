# V4 Node Contracts

> 自动生成文件。唯一事实源为 pipeline-contract.json。

## 1. run-bootstrap

- Module: global
- Mode: P
- Depends on: -
- Inputs: -
- Model factors: -
- Python outputs: run-manifest
- Executor: scripts/run_pipeline.py:init
- Validator: scripts/validate_pipeline_contract.py
- Rules: -

## 2. document-read

- Module: ingest
- Mode: P
- Depends on: run-bootstrap
- Inputs: run-manifest
- Model factors: -
- Python outputs: source-blocks
- Executor: scripts/ingest.py:document-read
- Validator: scripts/ingest.py:source-blocks
- Rules: -

## 3. scene-segmentation

- Module: ingest
- Mode: M→P
- Depends on: document-read
- Inputs: source-blocks
- Model factors: scene-boundary-factors
- Python outputs: scenes
- Executor: scripts/ingest.py:scene-segmentation
- Validator: scripts/ingest.py:scenes
- Rules: rules/01-ingest.md#scene-segmentation

## 4. source-coverage-gate

- Module: ingest
- Mode: P
- Depends on: scene-segmentation
- Inputs: source-blocks, scenes
- Model factors: -
- Python outputs: source-coverage
- Executor: scripts/ingest.py:source-coverage
- Validator: scripts/ingest.py:source-coverage
- Rules: -

## 5. mention-scan

- Module: recognition
- Mode: M+P
- Depends on: source-coverage-gate
- Inputs: source-blocks, scenes, source-coverage
- Model factors: mention-scan-facts
- Python outputs: raw-asset-mentions
- Executor: scripts/recognition.py:mention-scan
- Validator: scripts/recognition.py:raw-mentions
- Rules: rules/02-recognition.md#mention-scan

## 6. mention-confirmation

- Module: recognition
- Mode: M+P
- Depends on: mention-scan
- Inputs: raw-asset-mentions, source-blocks
- Model factors: mention-confirmation-facts
- Python outputs: mention-dispositions
- Executor: scripts/recognition.py:mention-confirmation
- Validator: scripts/recognition.py:mention-dispositions
- Rules: rules/02-recognition.md#mention-confirmation

## 7. entity-resolution

- Module: recognition
- Mode: M→P
- Depends on: mention-confirmation
- Inputs: mention-dispositions
- Model factors: entity-relation-factors
- Python outputs: asset-entities, asset-aliases
- Executor: scripts/recognition.py:entity-resolution
- Validator: scripts/recognition.py:entities
- Rules: rules/02-recognition.md#entity-resolution

## 8. evidence-ledger

- Module: recognition
- Mode: M+P
- Depends on: entity-resolution
- Inputs: asset-entities, mention-dispositions, scenes, source-blocks
- Model factors: evidence-facts
- Python outputs: character-evidence, scene-evidence, prop-evidence
- Executor: scripts/recognition.py:evidence-ledger
- Validator: scripts/recognition.py:evidence
- Rules: rules/02-recognition.md#evidence-ledger

## 9. recognition-closure-gate

- Module: recognition
- Mode: P
- Depends on: evidence-ledger
- Inputs: raw-asset-mentions, mention-dispositions, asset-entities, asset-aliases, character-evidence, scene-evidence, prop-evidence
- Model factors: -
- Python outputs: recognition-closure
- Executor: scripts/recognition.py:recognition-closure
- Validator: scripts/recognition.py:recognition-closure
- Rules: -

## 10. candidate-admission

- Module: planning
- Mode: M→P
- Depends on: recognition-closure-gate
- Inputs: asset-entities, character-evidence, scene-evidence, prop-evidence, recognition-closure
- Model factors: admission-factors
- Python outputs: asset-candidates, admission-dispositions, polluted-labels
- Executor: scripts/planning.py:candidate-admission
- Validator: scripts/planning.py:candidates
- Rules: rules/03-planning.md#candidate-admission

## 11. asset-rating

- Module: planning
- Mode: M→P
- Depends on: candidate-admission
- Inputs: asset-candidates, character-evidence, scene-evidence, prop-evidence
- Model factors: rating-factors
- Python outputs: asset-ratings
- Executor: scripts/planning.py:asset-rating
- Validator: scripts/planning.py:ratings
- Rules: rules/03-planning.md#asset-rating

## 12. base-asset-registration

- Module: planning
- Mode: P
- Depends on: asset-rating
- Inputs: asset-entities, asset-aliases, asset-candidates, asset-ratings
- Model factors: -
- Python outputs: base-asset-registry
- Executor: scripts/planning.py:base-registration
- Validator: scripts/planning.py:registry
- Rules: -

## 13. state-variant

- Module: planning
- Mode: M→P
- Depends on: base-asset-registration
- Inputs: base-asset-registry, asset-ratings, character-evidence, scene-evidence, prop-evidence
- Model factors: state-factors
- Python outputs: asset-states, state-dispositions
- Executor: scripts/planning.py:state-variant
- Validator: scripts/planning.py:states
- Rules: rules/03-planning.md#state-variant

## 14. asset-disposition

- Module: planning
- Mode: M→P
- Depends on: state-variant
- Inputs: asset-candidates, asset-ratings, base-asset-registry, asset-states, character-evidence, scene-evidence, prop-evidence
- Model factors: disposition-factors
- Python outputs: asset-dispositions
- Executor: scripts/planning.py:asset-disposition
- Validator: scripts/planning.py:dispositions
- Rules: rules/03-planning.md#asset-disposition

## 15. task-generation

- Module: planning
- Mode: P
- Depends on: asset-disposition
- Inputs: asset-dispositions, base-asset-registry, asset-states, asset-ratings
- Model factors: -
- Python outputs: production-tasks
- Executor: scripts/planning.py:task-generation
- Validator: scripts/planning.py:tasks
- Rules: -

## 16. episode-usage-map

- Module: planning
- Mode: P
- Depends on: task-generation
- Inputs: production-tasks, character-evidence, scene-evidence, prop-evidence, scenes
- Model factors: -
- Python outputs: episode-usage-map
- Executor: scripts/planning.py:episode-usage-map
- Validator: scripts/planning.py:usage
- Rules: -

## 17. planning-closure-gate

- Module: planning
- Mode: P
- Depends on: episode-usage-map
- Inputs: asset-candidates, admission-dispositions, polluted-labels, asset-ratings, base-asset-registry, asset-states, state-dispositions, asset-dispositions, production-tasks, episode-usage-map
- Model factors: -
- Python outputs: planning-closure
- Executor: scripts/planning.py:planning-closure
- Validator: scripts/planning.py:planning-closure
- Rules: -

## 18. asset-anchor

- Module: visual
- Mode: M+P
- Depends on: planning-closure-gate
- Inputs: production-tasks, base-asset-registry, asset-states, character-evidence, scene-evidence, prop-evidence, planning-closure
- Model factors: anchor-facts
- Python outputs: asset-anchors
- Executor: scripts/visual.py:asset-anchor
- Validator: scripts/visual.py:anchors
- Rules: rules/04-visual-writing.md#asset-anchor

## 19. prompt-slots

- Module: visual
- Mode: M+P
- Depends on: asset-anchor
- Inputs: production-tasks, asset-anchors, asset-states, character-evidence, scene-evidence, prop-evidence
- Model factors: prompt-slot-facts
- Python outputs: prompt-slots
- Executor: scripts/visual.py:prompt-slots
- Validator: scripts/visual.py:prompt-slots
- Rules: rules/04-visual-writing.md#prompt-slots

## 20. prompt-render

- Module: visual
- Mode: P
- Depends on: prompt-slots
- Inputs: prompt-slots
- Model factors: -
- Python outputs: rendered-prompts
- Executor: scripts/visual.py:prompt-render
- Validator: scripts/visual.py:rendered-prompts
- Rules: -

## 21. production-source

- Module: visual
- Mode: P
- Depends on: prompt-render
- Inputs: production-tasks, asset-ratings, base-asset-registry, asset-states, asset-dispositions, asset-anchors, rendered-prompts, episode-usage-map
- Model factors: -
- Python outputs: main-image-production-source
- Executor: scripts/visual.py:production-source
- Validator: scripts/visual.py:production-source
- Rules: -

## 22. prompt-closure-gate

- Module: visual
- Mode: P
- Depends on: production-source
- Inputs: production-tasks, asset-anchors, prompt-slots, rendered-prompts, main-image-production-source
- Model factors: -
- Python outputs: prompt-closure
- Executor: scripts/visual.py:prompt-closure
- Validator: scripts/visual.py:prompt-closure
- Rules: -

## 23. pre-delivery-audit

- Module: delivery
- Mode: P
- Depends on: prompt-closure-gate
- Inputs: run-manifest, source-coverage, recognition-closure, planning-closure, prompt-closure, main-image-production-source
- Model factors: -
- Python outputs: production-audit
- Executor: scripts/delivery.py:pre-delivery-audit
- Validator: scripts/delivery.py:production-audit
- Rules: -

## 24. json-delivery

- Module: delivery
- Mode: P
- Depends on: pre-delivery-audit
- Inputs: main-image-production-source, production-audit
- Model factors: -
- Python outputs: prompt-manifest
- Executor: scripts/delivery.py:json-delivery
- Validator: scripts/delivery.py:prompt-manifest
- Rules: -

## 25. human-view-delivery

- Module: delivery
- Mode: P
- Depends on: pre-delivery-audit
- Inputs: main-image-production-source, production-audit
- Model factors: -
- Python outputs: view-manifest
- Executor: scripts/delivery.py:human-view-delivery
- Validator: scripts/delivery.py:view-manifest
- Rules: -

## 26. final-quality-gate

- Module: delivery
- Mode: P
- Depends on: json-delivery, human-view-delivery
- Inputs: run-manifest, main-image-production-source, prompt-manifest, production-audit, prompt-closure, view-manifest
- Model factors: -
- Python outputs: final-quality
- Executor: scripts/delivery.py:final-quality
- Validator: scripts/delivery.py:final-quality
- Rules: -
