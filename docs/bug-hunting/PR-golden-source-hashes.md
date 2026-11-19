# Bug Hunt — Golden source SHA-256 evidence

## Scope
H100 — independently compute SHA-256 for every preserved Golden DWG directly from the checked-out repository.

## Bug Hunt
Verify both preserved Golden DWG files exist and produce non-empty, 64-character SHA-256 digests from their actual bytes.

## Findings
The manifest currently leaves `source_sha256` unset. This test provides CI-native evidence without confusing a Git blob SHA with a file SHA-256.

## Regression
The test covers every case in `golden_manifest.json`, so adding another Golden case automatically adds hash coverage.

## Reproduction
Run:
`python -m unittest tests.test_golden_source_hashes -v`

CI output includes:
`GOLDEN_SOURCE_SHA256 case=<id> path=<path> sha256=<sha256>`

## Root cause
The repository previously had no machine-checked path that independently emitted the real SHA-256 of the preserved DWG bytes.

## CI Verification
Fresh exact-head REAL CI, Runtime Tests, and Bug Hunt are required.

## Final Decision
BLOCKED until exact-head gates are green and both hashes are captured and verified.

## Required fail-closed states
UNKNOWN
NEEDS_REVIEW
BLOCKED
PASS

unresolved
regression
