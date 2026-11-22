import tempfile
import unittest
from pathlib import Path

from security_review.invariant_lint import lint_py, lint_workflow


class InvariantLintTests(unittest.TestCase):
    def lint_source(self, source, filename="runtime/sample.py"):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp, "sample.py")
            path.write_text(source, encoding="utf-8")
            return lint_py(path, filename)

    def test_nan_clamp_pattern_is_flagged(self):
        findings = self.lint_source("def normalize(x):\n    return max(0.0, min(1.0, float(x)))\n")
        self.assertTrue(any(f["rule"] == "INV-002" for f in findings))

    def test_unknown_error_classifier_pattern_is_flagged(self):
        findings = self.lint_source("def classify(code):\n    if code in BLOCKING: return BLOCKING\n    return NON_BLOCKING\n", "runtime/error_policy.py")
        self.assertTrue(any(f["rule"] == "INV-003" for f in findings))

    def test_unconditional_completion_return_is_flagged(self):
        findings = self.lint_source("def has_completed(result):\n    return True\n", "runtime/idempotency.py")
        self.assertTrue(any(f["rule"] == "INV-004" for f in findings))

    def test_all_interfaces_bind_is_flagged(self):
        findings = self.lint_source('HOST = "0.0.0.0"')
        self.assertTrue(any(f["rule"] == "INV-005" for f in findings))

    def test_action_tag_pin_and_permissions_checks(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp, "workflow.yml")
            path.write_text("name: test\njobs:\n  test:\n    steps:\n      - uses: actions/checkout@v4\n", encoding="utf-8")
            findings = lint_workflow(path, ".github/workflows/test.yml")
        self.assertTrue(any(f["rule"] == "INV-101" for f in findings))
        self.assertTrue(any(f["rule"] == "INV-102" for f in findings))


if __name__ == "__main__":
    unittest.main()
