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

## Install
python -m pip install -r requirements.txt

Dependencies include PyMuPDF (`fitz`), OpenCV, NumPy and `ezdwg`. Without them, 16 test modules may fail to import; a run without required dependencies is not a valid Green.

## Run
python -m runtime.app

## Test
python -m unittest discover -s tests -v

CI runs this suite on GitHub Actions. Only a completed/success run on the exact head SHA counts as Green; queued, in-progress, cancelled or missing runs do not.

## Real visual artifact path
runtime.real_visual_runtime.RealVisualRuntime accepts a real JPG/PNG/WEBP/PDF path and produces traceable source/detection evidence. Approval/editing is blocked when locked-element identification is uncertain.

## Review reporting
- `runtime/review_report_contract.py` — unified findings report; a human override never turns a finding into PASS and BLOCKED findings cannot be overridden.
- `runtime/input_completeness_check.py` — flags missing scale, units, dimensions and title-block evidence before any understanding or editing.
- `runtime/plan_revision_diff.py` — compares two PlanModel versions and rejects any change to a LOCKED or protected element.

## Project state and governance
- `PROJECT_STATE.md` and `MASTER_HANDOFF.md` are the durable state documents; read them before changing anything.
- Every PR needs `docs/bug-hunting/PR-<number>.md` with the mandatory Bug Hunt sections and tokens (see `runtime/bug_hunting_gate.py`).
- Golden DWG fixtures in `test-assets/golden-projects/` are immutable.
