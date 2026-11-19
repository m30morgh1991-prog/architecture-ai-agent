import unittest

from runtime.app import Handler, fingerprint_request_payload
from runtime.idempotency import IdempotencyConflictError, IdempotencyGuard


class IdempotencyTests(unittest.TestCase):
    def test_duplicate_returns_original(self):
        guard = IdempotencyGuard()
        original = {"status": "PASS"}
        self.assertIs(guard.store("k", "fingerprint-1", original), original)
        self.assertIs(guard.store("k", "fingerprint-1", {"status": "OTHER"}), original)

    def test_completed_key_is_replayable(self):
        guard = IdempotencyGuard()
        result = {"status": "PASS", "failure_code": None}
        guard.store("execution-1", "fingerprint-1", result)
        self.assertTrue(guard.has_completed("execution-1"))
        self.assertEqual(guard.check("execution-1", "fingerprint-1"), result)

    def test_different_fingerprint_is_a_conflict_and_does_not_replace_result(self):
        guard = IdempotencyGuard()
        original = {"status": "PASS"}
        guard.store("execution-1", "fingerprint-1", original)
        with self.assertRaisesRegex(IdempotencyConflictError, "IDEMPOTENCY_KEY_REUSED_WITH_DIFFERENT_REQUEST"):
            guard.check("execution-1", "fingerprint-2")
        with self.assertRaisesRegex(IdempotencyConflictError, "IDEMPOTENCY_KEY_REUSED_WITH_DIFFERENT_REQUEST"):
            guard.store("execution-1", "fingerprint-2", {"status": "OTHER"})
        self.assertIs(guard.check("execution-1", "fingerprint-1"), original)

    def test_running_workflow_decision_is_not_reported_completed(self):
        from runtime.workflow_guard import WorkflowDecision

        guard = IdempotencyGuard()
        guard.store("workflow-1", "execution-1", WorkflowDecision("PASS", "RUNNING"))
        self.assertFalse(guard.has_completed("workflow-1"))
        guard.replace("workflow-1", "execution-1", WorkflowDecision("PASS", "SUCCEEDED"))
        self.assertTrue(guard.has_completed("workflow-1"))

    def test_unknown_key_is_not_completed(self):
        guard = IdempotencyGuard()
        self.assertIsNone(guard.check("missing", "fingerprint-1"))
        self.assertFalse(guard.has_completed("missing"))

    def test_clear_removes_replay_evidence(self):
        guard = IdempotencyGuard()
        guard.store("execution-1", "fingerprint-1", {"status": "PASS"})
        guard.clear("execution-1")
        self.assertIsNone(guard.check("execution-1", "fingerprint-1"))
        self.assertFalse(guard.has_completed("execution-1"))

    def test_request_fingerprint_changes_when_payload_changes(self):
        first = {
            "execution_id": "same-execution",
            "request": {"instruction": "Move sofa"},
        }
        second = {
            "execution_id": "same-execution",
            "request": {"instruction": "Move sofa elsewhere"},
        }
        self.assertNotEqual(fingerprint_request_payload(first), fingerprint_request_payload(second))

    def test_http_endpoint_stays_blocked_before_request_body_or_idempotency(self):
        class TrackingReader:
            read_called = False
            def read(self, length):
                self.read_called = True
                return b"{}"

        handler = Handler.__new__(Handler)
        handler.path = "/v1/execute"
        handler.rfile = TrackingReader()
        handler._json = lambda status, body: (status, body)
        handler.send_error = lambda status, *args, **kwargs: (status, {"error": "HTTP_ERROR"})
        status, body = handler.do_POST()
        self.assertEqual(status, 503)
        self.assertEqual(body["error"], "CANONICAL_EXECUTION_NOT_CONFIGURED")
        self.assertEqual(body["status"], "BLOCKED")
        self.assertFalse(handler.rfile.read_called)


if __name__ == "__main__":
    unittest.main()
