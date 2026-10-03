# Bug Hunt — H90 v2

## Scope
Verify PostEditDiff derives only from before/after detection and preserves Source-of-Truth identity and fail-closed behavior.

## Bug Hunt
Reproduction covers clean approved edits, locked changes, unauthorized changes, missing before/after evidence, source identity mismatch, and added/removed elements.
Root Cause checks focus on contract drift between BeforeAfterDetection and PostEditDiff.

## Findings
No edit authority is introduced. UNKNOWN, NEEDS_REVIEW, and BLOCKED states cannot become PASS. Identity mismatch is BLOCKED. Added/removed/locked/unauthorized deltas are merge-blocking validation findings.

## Regression
Permanent tests cover the above cases and malformed/missing inputs. Any future regression must be added before merge.

## CI Verification
This PR must pass Bug Hunt Gate, Runtime Tests, and PR CI on the exact PR head SHA. Local or prior green is not sufficient.

## Final Decision
MERGE only when all required gates are SUCCESS on the exact head SHA and the PR is mergeable. Otherwise BLOCKED.
