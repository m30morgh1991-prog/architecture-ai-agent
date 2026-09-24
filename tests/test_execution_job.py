import unittest

from runtime.execution_job import ExecutionApiBoundary


class ExecutionJobTests(unittest.TestCase):
    def setUp(self):
        self.api = ExecutionApiBoundary()

    def test_submit_start_complete(self):
        self.api.submit("PRJ-001", "EX-001", "JOB-001")
        self.assertEqual(self.api.get("JOB-001")["state"], "QUEUED")
        self.api.start("JOB-001", "VALIDATION")
        result = self.api.complete("JOB-001", {"status": "PASS"})
        self.assertEqual(result["state"], "SUCCEEDED")
        self.assertEqual(result["result"]["status"], "PASS")

    def test_failure_path(self):
        self.api.submit("PRJ-001", "EX-002", "JOB-002")
        self.api.start("JOB-002", "RULES")
        result = self.api.fail("JOB-002", {"code": "RULE_APPLICABILITY_UNKNOWN"})
        self.assertEqual(result["state"], "FAILED")

    def test_blocked_path(self):
        self.api.submit("PRJ-001", "EX-003", "JOB-003")
        self.api.start("JOB-003", "POST_EDIT")
        result = self.api.block("JOB-003", {"code": "LOCKED_ELEMENT_CONFLICT"})
        self.assertEqual(result["state"], "BLOCKED")

    def test_invalid_transition_is_rejected(self):
        self.api.submit("PRJ-001", "EX-004", "JOB-004")
        with self.assertRaises(ValueError):
            self.api.complete("JOB-004", {"status": "PASS"})


if __name__ == "__main__":
    unittest.main()
