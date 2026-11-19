# Bug Hunt Evidence — H100 Golden Understanding Research Lock

## Scope

Research lock for Golden Understanding Regression and the Understanding Gate. This change is documentation/research only and does not create a second PlanModel.

## Reproduction

The previous H100 foundation defined evidence contracts, but did not yet define the full benchmark truth model, evaluation axes, benchmark hygiene, or hard fail-closed acceptance gates.

## Root cause

Golden Understanding was at risk of becoming a conventional regression test focused on labels or image similarity instead of validating source-bound semantic understanding and unsafe acceptance behavior.

## Bug Hunt

- No second PlanModel or semantic graph is introduced.
- Public datasets are treated as calibration sources, not project truth.
- UNKNOWN and NEEDS_REVIEW remain explicit.
- CONTRADICTED evidence cannot become PASS.
- False-PASS and unsafe acceptance are hard blockers.
- Ground truth is source-bound and provenance-controlled.
- Cross-dataset leakage and near-duplicate contamination are explicit risks.

## Findings

- Research supports multi-axis understanding evaluation.
- Graph/topology metrics must be independent from pixel metrics.
- OCR/dimensions/levels/section semantics need dedicated evaluation.
- Cross-view plan/section/elevation coordination must be represented.
- Engineering validity requires topology and structural-validity gates.
- The next implementation should be an Understanding Runner and Golden case manifest around canonical PlanModel.

## Regression

Exact-head REAL CI, Runtime and Bug Hunt remain mandatory before merge.

## CI Verification

This document is governance evidence only. The authoritative decision is the completed/success GitHub workflow result for the exact PR head.

## Final Decision

**BUG_HUNT_PASS**

The research lock does not authorize H101 or generation until the Understanding Gate passes.

unresolved
UNKNOWN
NEEDS_REVIEW
BLOCKED
PASS
reproduction
root cause
regression
