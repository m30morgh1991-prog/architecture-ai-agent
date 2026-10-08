# Bug Hunt — H100 Golden integrity + read-only CAD adapter

## Scope
Persist independently observed Golden DWG SHA-256 values, add byte-level mismatch regression, strengthen Bug Hunt evidence requirements, and introduce a dependency-free read-only CAD inspection adapter boundary.

## Bug Hunt
Check source identity, manifest/source mismatch, adapter source binding, read-only behavior, provenance, negative-path coverage, exact-head CI, unresolved findings, and false-PASS risk.

## Findings
The previous Golden manifest contained null source hashes even though CI had independently emitted SHA-256 values from checked-out bytes. The CAD boundary existed as a contract but had no concrete read-only inspection implementation. Bug Hunt evidence also relied on free-form text tokens without structured affected-contract/risk/reproduction requirements.

## Reproduction
Run:
python -m unittest tests/test_golden_source_hashes.py -v
python -m unittest tests/test_cad_readonly_adapter.py -v
python -m unittest tests/test_bug_hunting_gate.py -v

Expected: real SHA-256 values match the checked-out Golden bytes; wrong hashes are rejected; adapter never writes source bytes; incomplete/contradictory evidence is blocked.

## Root Cause
Golden identity evidence was generated in CI but not persisted into the manifest. The CAD integration seam lacked a concrete read-only implementation. Bug Hunt validation did not require machine-checkable structured risk and contract evidence.

## Regression
Added byte-level Golden hash verification, source mismatch negative tests, dependency-free read-only adapter tests, and stronger Bug Hunt evidence-contract validation. No live AutoCAD write path is enabled.

## Required fail-closed states
UNKNOWN
NEEDS_REVIEW
BLOCKED
PASS

unresolved
false pass
exact-head

## CI Verification
Exact-head PR CI, Runtime Tests, and Bug Hunt must complete successfully. Real AutoCAD connectivity and live write PASS are explicitly out of scope.

## Final Decision
BLOCKED until exact-head CI is green. This change does not promote Golden Understanding to semantic PASS and does not enable live CAD execution.
