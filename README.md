# Architecture AI Agent — Runtime MVP

This repository contains the first deployable, vendor-neutral runtime slice for the Architecture AI Agent.

## Scope
- JSON contract-driven runtime
- locked-element protection
- furniture-only change path
- deterministic validation
- post-edit diff
- no prompt-to-editor shortcut

Real visual detection/editing adapters remain replaceable and are not claimed as implemented by this slice.

## Run
python -m runtime.app

## Test
python -m unittest discover -s tests -v
