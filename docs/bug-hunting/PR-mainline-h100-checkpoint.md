# Bug Hunt — mainline H100 checkpoint

## Scope
Verify the current main branch checkpoint after PR #75 and direct state-document persistence.

## Bug Hunt
Validate Golden source binding, fail-closed state documentation, AutoCAD-MCP read-only boundary, exact-head CI, and false-PASS risk.

## Findings
No semantic PASS is introduced. This PR only adds executable regression coverage for the current mainline checkpoint.

## Reproduction
Run:
python -m unittest tests/test_mainline_h100_checkpoint.py -v

## Root Cause
The repository's workflow query exposes pull-request-triggered runs, while direct main commits have not produced observable mainline workflow evidence. An executable checkpoint test provides a machine-checkable gate before the next H100 work.

## Regression
Adds tests for persisted Golden SHA format/status, explicit no-post-merge-green claim, and read-only CAD execution boundary.

## Affected Contracts
Golden manifest, PROJECT_STATE, AutoCAD-MCP adapter boundary, fail-closed governance.

## Risk Classification
MEDIUM: false claim of mainline Green; HIGH if semantic PASS or CAD write authority were accidentally introduced.

## Negative Tests
Invalid SHA, non-UNKNOWN Golden status, missing fail-closed state, and missing read-only boundary are blocked by the checkpoint contract.

## Unresolved Findings
Post-merge workflow evidence for direct main commits remains unavailable through the current GitHub workflow-run query. No semantic Golden PASS is claimed.

## Required fail-closed states
UNKNOWN
NEEDS_REVIEW
BLOCKED
PASS

unresolved
false pass
exact-head

## CI Verification
Exact-head PR CI, Runtime Tests, and Bug Hunt must all complete successfully.

## Final Decision
BLOCKED until exact-head CI is green.
