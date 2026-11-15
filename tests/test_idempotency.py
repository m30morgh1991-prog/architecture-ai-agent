import http.client
import json
import threading
import unittest
from copy import deepcopy
from http.server import HTTPServer
from unittest.mock import patch

from runtime import app as runtime_app
from runtime.audit import AuditTrail
from runtime.execution_record import ExecutionRecordStore
from runtime.idempotency import IdempotencyConflictError, IdempotencyGuard


class IdempotencyTests(unittest.TestCase):
    def test_duplicate_returns_original(self):
        guard = IdempotencyGuard()
        original = {"status": "PASS"}
        self.assertIs(guard.store("k", "fingerprint-1", original), original)
        self.assertIs(
            guard.store("k", "fingerprint-1", {"status": "OTHER"}), original
        )

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

        with self.assertRaisesRegex(
            IdempotencyConflictError,
            "IDEMPOTENCY_KEY_REUSED_WITH_DIFFERENT_REQUEST",
        ):
            guard.check("execution-1", "fingerprint-2")

        with self.assertRaisesRegex(
            IdempotencyConflictError,
            "IDEMPOTENCY_KEY_REUSED_WITH_DIFFERENT_REQUEST",
        ):
            guard.store("execution-1", "fingerprint-2", {"status": "OTHER"})

        self.assertIs(guard.check("execution-1", "fingerprint-1"), original)

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


    def test_same_execution_id_with_different_payload_returns_conflict(self):
        payload = {
            "execution_id": "same-execution",
            "project_id": "project-1",
            "input_version_id": "version-1",
            "plan_id": "plan-1",
            "elements": [],
            "request": {
                "change_type": "FURNITURE",
                "target_ids": ["MISSING"],
                "instruction": "Move missing sofa",
            },
        }

        with (
            patch.object(runtime_app, "execution_records", ExecutionRecordStore()),
            patch.object(runtime_app, "audit_trail", AuditTrail()),
            patch.object(runtime_app, "idempotency_guard", IdempotencyGuard()),
        ):
            server = HTTPServer(("127.0.0.1", 0), runtime_app.Handler)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                def post(body):
                    connection = http.client.HTTPConnection(
                        "127.0.0.1", server.server_port, timeout=3
                    )
                    connection.request(
                        "POST",
                        "/v1/execute",
                        body=json.dumps(body),
                        headers={"Content-Type": "application/json"},
                    )
                    response = connection.getresponse()
                    result = json.loads(response.read().decode("utf-8"))
                    connection.close()
                    return response.status, result

                first_status, first = post(payload)
                self.assertEqual(first_status, 200)
                self.assertFalse(first["idempotent_replay"])
                self.assertEqual(first["result"]["status"], "REJECT")

                replay_status, replay = post(payload)
                self.assertEqual(replay_status, 200)
                self.assertTrue(replay["idempotent_replay"])

                changed_payload = deepcopy(payload)
                changed_payload["request"]["instruction"] = "Move sofa elsewhere"
                conflict_status, conflict = post(changed_payload)
                self.assertEqual(conflict_status, 409)
                self.assertEqual(
                    conflict["error"],
                    "IDEMPOTENCY_KEY_REUSED_WITH_DIFFERENT_REQUEST",
                )
            finally:
                server.shutdown()
                thread.join(timeout=3)
                server.server_close()


if __name__ == "__main__":
    unittest.main()
