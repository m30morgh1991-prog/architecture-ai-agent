from pathlib import Path
import tempfile
import unittest

from runtime.bug_hunting_gate import REQUIRED_SECTIONS, REQUIRED_TOKENS, validate_evidence, run

GOOD = """# Bug Hunt
## Scope
Changed runtime contract.
## Bug Hunt
Checked positive, negative, integration, and fail-closed paths.
## Findings
No unresolved findings. Reproduction and root cause were checked; no product bug found.
## Reproduction
Run the exact test command and reproduce the affected behavior.
## Root Cause
The previous contract omitted a required evidence field.
## Regression
Permanent regression coverage is present. UNKNOWN, NEEDS_REVIEW, and BLOCKED cannot become PASS.
## Required fail-closed states
UNKNOWN
NEEDS_REVIEW
BLOCKED
PASS
unresolved
## CI Verification
Exact-head PR CI and Runtime Tests are required and must be green.
## Affected Contracts
PlanModel, ConstraintMap, Golden manifest, CAD adapter boundary.
## Risk Classification
HIGH: false PASS, source identity mismatch, unauthorized write.
## Negative Tests
Wrong source hash, missing evidence, stale revision, and unsupported capability are blocked.
## Unresolved Findings
None. Any unresolved finding remains BLOCKED.
## Final Decision
PASS only after exact-head CI verification; unresolved findings block merge and false pass is prohibited.
"""

class BugHuntingGateTests(unittest.TestCase):
    def test_good_evidence_passes(self):
        self.assertEqual(validate_evidence(GOOD), [])

    def test_missing_section_blocks(self):
        text = GOOD.replace("## Regression", "")
        errors = validate_evidence(text)
        self.assertTrue(any(e.startswith("MISSING_SECTION:## Regression") for e in errors))

    def test_missing_fail_closed_token_blocks(self):
        text = GOOD.replace("BLOCKED", "NO_FAIL_CLOSED_TOKEN")
        errors = validate_evidence(text)
        self.assertTrue(any(e == "MISSING_TOKEN:BLOCKED" for e in errors))

    def test_missing_exact_head_evidence_blocks(self):
        text = GOOD.replace("Exact-head", "Stale-head").replace("exact-head", "stale-head")
        errors = validate_evidence(text)
        self.assertIn("MISSING_TOKEN:exact-head", errors)

    def test_missing_affected_contract_blocks(self):
        text = GOOD.replace("## Affected Contracts", "## Missing Contracts")
        errors = validate_evidence(text)
        self.assertIn("MISSING_SECTION:## Affected Contracts", errors)

    def test_missing_negative_test_token_blocks(self):
        text = GOOD.replace("Negative Tests", "Positive Tests")
        errors = validate_evidence(text)
        self.assertIn("MISSING_SECTION:## Negative Tests", errors)

    def test_missing_pr_evidence_blocks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(run("123", root), 1)

    def test_required_contract_is_stronger(self):
        self.assertEqual(len(REQUIRED_SECTIONS), 13)
        self.assertEqual(len(REQUIRED_TOKENS), 13)

if __name__ == "__main__":
    unittest.main()
