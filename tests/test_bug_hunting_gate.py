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
## Regression
Permanent regression coverage is present. UNKNOWN, NEEDS_REVIEW, and BLOCKED cannot become PASS.
## CI Verification
PR CI and Runtime Tests are required and must be green.
## Final Decision
PASS only after CI verification; unresolved findings block merge.
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

    def test_missing_pr_evidence_blocks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(run("123", root), 1)

    def test_required_contract_is_nonempty(self):
        self.assertEqual(len(REQUIRED_SECTIONS), 6)
        self.assertEqual(len(REQUIRED_TOKENS), 7)

if __name__ == "__main__":
    unittest.main()
