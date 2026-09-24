import unittest
from runtime.workflow_guard import WorkflowGuard


class WorkflowGuardTests(unittest.TestCase):
    def test_successful_lifecycle_is_audited_and_idempotent(self):
        guard = WorkflowGuard()
        started = guard.begin("E18", "K18")
        finished = guard.finish("E18", "K18")
        duplicate = guard.begin("E18", "K18")
        self.assertEqual(started.state, "RUNNING")
        self.assertEqual(finished.state, "SUCCEEDED")
        self.assertEqual(duplicate, started)
        self.assertEqual([e.stage for e in guard.trace("E18")], ["WORKFLOW", "WORKFLOW"])

    def test_blocking_failure_becomes_blocked(self):
        guard = WorkflowGuard()
        guard.begin("E18B", "K18B")
        result = guard.finish("E18B", "K18B", "LOCKED_ELEMENT_CONFLICT")
        self.assertEqual(result.status, "REJECT")
        self.assertEqual(result.state, "BLOCKED")

    def test_nonblocking_failure_needs_revision(self):
        guard = WorkflowGuard()
        guard.begin("E18C", "K18C")
        result = guard.finish("E18C", "K18C", "TARGET_NOT_FOUND")
        self.assertEqual(result.status, "NEEDS_REVISION")
        self.assertEqual(result.state, "FAILED")


if __name__ == "__main__":
    unittest.main()
