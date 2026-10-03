import unittest

from runtime.idempotency import IdempotencyGuard


class IdempotencyTests(unittest.TestCase):
    def test_duplicate_returns_original(self):
        guard = IdempotencyGuard()
        original = {"status": "PASS"}
        self.assertIs(guard.store("k", original), original)
        self.assertIs(guard.store("k", {"status": "OTHER"}), original)

    def test_completed_key_is_replayable(self):
        guard = IdempotencyGuard()
        result = {"status": "PASS", "failure_code": None}
        guard.store("execution-1", result)
        self.assertTrue(guard.has_completed("execution-1"))
        self.assertEqual(guard.check("execution-1"), result)

    def test_unknown_key_is_not_completed(self):
        guard = IdempotencyGuard()
        self.assertIsNone(guard.check("missing"))
        self.assertFalse(guard.has_completed("missing"))

    def test_clear_removes_replay_evidence(self):
        guard = IdempotencyGuard()
        guard.store("execution-1", {"status": "PASS"})
        guard.clear("execution-1")
        self.assertIsNone(guard.check("execution-1"))
        self.assertFalse(guard.has_completed("execution-1"))


if __name__ == "__main__":
    unittest.main()
