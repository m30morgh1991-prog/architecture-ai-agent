import unittest
from runtime.runtime_release_gate import evaluate_runtime_release

def runtime(status="READY_FOR_APPROVAL", contracts="VALID", semantics="ACCESSIBLE"):
    return {"status":status,"blockers":[],"contracts":{"status":contracts,"constraint_map_id":"cm-1"},"semantic_corroboration":{"status":semantics},"constraint_map":{"map_id":"cm-1","evidence_ids":["ev-1"]},"evidence":{"evidence_id":"ev-1","complete":True,"source_sha256":"src-1"},"source":{"sha256":"src-1"}}

class H52RuntimeTopLevelStateTests(unittest.TestCase):
    def green(self, result):
        return evaluate_runtime_release(result, workflow_ok=True, final_validation_ok=True, regression_ok=True)
    def test_only_ready_for_approval_can_pass(self):
        self.assertEqual(self.green(runtime()).status, "PASS")
        self.assertEqual(self.green(runtime(status="BLOCKED",semantics="ACCESSIBLE")).status, "BLOCKED")
    def test_blocked_runtime_with_all_component_checks_green_still_blocks(self):
        result=self.green(runtime(status="BLOCKED"))
        self.assertIn("RELEASE_CONTRACTS_FAILED", result.failure_codes)
        self.assertIn("RELEASE_SEMANTIC_CORROBORATION_FAILED", result.failure_codes)
    def test_non_ready_state_blocks_even_when_contracts_and_semantics_are_green(self):
        for state in ("BLOCKED","UNKNOWN","NEEDS_REVIEW","ABSTAIN"):
            self.assertEqual(self.green(runtime(status=state)).status, "BLOCKED")
    def test_ready_state_still_requires_valid_components(self):
        self.assertEqual(self.green(runtime(contracts="BLOCKED")).status, "BLOCKED")
        self.assertEqual(self.green(runtime(semantics="BLOCKED")).status, "BLOCKED")
if __name__=="__main__":
    unittest.main()
