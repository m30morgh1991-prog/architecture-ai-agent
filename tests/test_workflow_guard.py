import unittest
from runtime.idempotency import IdempotencyConflictError
from runtime.workflow_guard import WorkflowGuard


class WorkflowGuardTests(unittest.TestCase):
    def test_successful_lifecycle_is_audited_and_idempotent(self):
        guard = WorkflowGuard()
        started = guard.begin("E18", "K18")
        finished = guard.finish("E18", "K18")
        duplicate = guard.begin("E18", "K18")
        self.assertEqual(started.state, "RUNNING")
        self.assertEqual(finished.state, "SUCCEEDED")
        self.assertEqual(duplicate, finished)
        self.assertEqual([e.stage for e in guard.trace("E18")], ["WORKFLOW", "WORKFLOW"])

    def test_repeated_finish_replays_first_terminal_decision(self):
        guard = WorkflowGuard()
        guard.begin("E18R", "K18R")
        finished = guard.finish("E18R", "K18R")
        replay = guard.finish("E18R", "K18R", "LOCKED_ELEMENT_CONFLICT")
        self.assertEqual(replay, finished)
        self.assertEqual(len(guard.trace("E18R")), 2)

    def test_finish_without_begin_is_rejected(self):
        guard = WorkflowGuard()
        with self.assertRaisesRegex(ValueError, "WORKFLOW_NOT_STARTED"):
            guard.finish("E18N", "K18N")

    def test_idempotency_key_cannot_be_reused_for_another_execution(self):
        guard = WorkflowGuard()
        guard.begin("E18D", "shared-key")

        with self.assertRaisesRegex(
            IdempotencyConflictError,
            "IDEMPOTENCY_KEY_REUSED_WITH_DIFFERENT_REQUEST",
        ):
            guard.begin("E19D", "shared-key")

    def test_blocking_failure_becomes_blocked(self):
        guard = WorkflowGuard()
        guard.begin("E18B", "K18B")
        result = guard.finish("E18B", "K18B", "LOCKED_ELEMENT_CONFLICT")
        self.assertEqual(result.status, "REJECT")
        self.assertEqual(result.state, "BLOCKED")
        self.assertEqual(guard.trace("E18B")[-1].status, "BLOCKED")
        self.assertEqual(guard.begin("E18B", "K18B"), result)

    def test_nonblocking_failure_needs_revision(self):
        guard = WorkflowGuard()
        guard.begin("E18C", "K18C")
        result = guard.finish("E18C", "K18C", "TARGET_NOT_FOUND")
        self.assertEqual(result.status, "NEEDS_REVISION")
        self.assertEqual(result.state, "FAILED")
        self.assertEqual(guard.trace("E18C")[-1].status, "NEEDS_REVIEW")
        self.assertEqual(guard.begin("E18C", "K18C"), result)


if __name__ == "__main__":
    unittest.main()
