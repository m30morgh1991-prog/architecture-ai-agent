# Architecture AI Agent — Runtime MVP

This repository contains the first deployable, vendor-neutral runtime slice for the Architecture AI Agent.

## Scope
- JSON contract-driven runtime
- locked-element protection
- furniture-only change path
- deterministic validation
- post-edit diff
- no prompt-to-editor shortcut
- real JPG/PNG/WEBP/PDF artifact ingestion with conservative visual evidence

Real visual detection/editing adapters remain replaceable and are not claimed as implemented by this slice.

## Run
python -m runtime.app

## Test
python -m unittest discover -s tests -v

## Real visual artifact path
runtime.real_visual_runtime.RealVisualRuntime accepts a real JPG/PNG/WEBP/PDF path and produces traceable source/detection evidence. Approval/editing is blocked when locked-element identification is uncertain.
