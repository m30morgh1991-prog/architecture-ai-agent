import unittest

from runtime.independent_runner_policy import evaluate_runner_readiness


def ready_snapshot():
    return {
        "main_sha": "a" * 40,
        "active_stage": "H100",
        "gates": {
            "pr_ci": "success",
            "runtime_tests": "success",
            "bug_hunt": "success",
            "required_regression": "success",
        },
        "provider_configured": True,
        "agent_pr_open": False,
    }


class IndependentRunnerPolicyTests(unittest.TestCase):
    def test_ready_state_allows_isolated_work_only(self):
        result = evaluate_runner_readiness(ready_snapshot())
        self.assertEqual(result["decision"], "READY_FOR_TASK")
        self.assertTrue(result["can_edit_in_isolated_branch"])
        self.assertTrue(result["can_open_pull_request"])
        self.assertFalse(result["can_merge"])
        self.assertFalse(result["can_advance_stage"])
        self.assertTrue(result["requires_human_merge_approval"])

    def test_pending_gate_is_not_green(self):
        snapshot = ready_snapshot()
        snapshot["gates"]["runtime_tests"] = "in_progress"
        result = evaluate_runner_readiness(snapshot)
        self.assertEqual(result["decision"], "BLOCKED")
        self.assertIn("GATE_NOT_GREEN:runtime_tests", result["blockers"])
        self.assertFalse(result["can_edit_in_isolated_branch"])

    def test_missing_gate_is_not_green(self):
        snapshot = ready_snapshot()
        del snapshot["gates"]["bug_hunt"]
        result = evaluate_runner_readiness(snapshot)
        self.assertIn("GATE_NOT_GREEN:bug_hunt", result["blockers"])

    def test_missing_provider_blocks_ai_execution(self):
        snapshot = ready_snapshot()
        snapshot["provider_configured"] = False
        result = evaluate_runner_readiness(snapshot)
        self.assertIn("AI_PROVIDER_NOT_CONFIGURED", result["blockers"])
        self.assertFalse(result["can_open_pull_request"])

    def test_unknown_provider_state_blocks(self):
        snapshot = ready_snapshot()
        snapshot.pop("provider_configured")
        result = evaluate_runner_readiness(snapshot)
        self.assertIn("AI_PROVIDER_NOT_CONFIGURED", result["blockers"])

    def test_existing_agent_pr_blocks_duplicate_task(self):
        snapshot = ready_snapshot()
        snapshot["agent_pr_open"] = True
        result = evaluate_runner_readiness(snapshot)
        self.assertIn("EXISTING_AGENT_PR_REQUIRES_RECONCILIATION", result["blockers"])

    def test_unknown_agent_pr_state_blocks(self):
        snapshot = ready_snapshot()
        snapshot["agent_pr_open"] = "unknown"
        result = evaluate_runner_readiness(snapshot)
        self.assertIn("AGENT_PR_STATE_UNKNOWN", result["blockers"])

    def test_invalid_main_sha_blocks(self):
        snapshot = ready_snapshot()
        snapshot["main_sha"] = "main"
        result = evaluate_runner_readiness(snapshot)
        self.assertIn("MAIN_SHA_MISSING_OR_INVALID", result["blockers"])

    def test_missing_stage_blocks(self):
        snapshot = ready_snapshot()
        snapshot["active_stage"] = "H1010"
        result = evaluate_runner_readiness(snapshot)
        self.assertIn("ACTIVE_STAGE_MISSING_OR_INVALID", result["blockers"])

    def test_missing_gate_snapshot_blocks(self):
        snapshot = ready_snapshot()
        snapshot.pop("gates")
        result = evaluate_runner_readiness(snapshot)
        self.assertIn("GATE_SNAPSHOT_MISSING", result["blockers"])

    def test_all_failure_states_are_fail_closed(self):
        for state in ("failure", "cancelled", "skipped", "queued", "unknown", None):
            with self.subTest(state=state):
                snapshot = ready_snapshot()
                snapshot["gates"]["pr_ci"] = state
                result = evaluate_runner_readiness(snapshot)
                self.assertEqual(result["decision"], "BLOCKED")
                self.assertFalse(result["can_merge"])
                self.assertFalse(result["can_advance_stage"])


if __name__ == "__main__":
    unittest.main()
