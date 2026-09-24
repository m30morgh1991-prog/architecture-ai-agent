import unittest
from runtime.runtime_release_gate import evaluate_runtime_release

class H56EvidenceSourceBindingTests(unittest.TestCase):
    def base(self):
        return {
            "status":"READY_FOR_APPROVAL","blockers":[],
            "contracts":{"status":"VALID","constraint_map_id":"cm-1"},
            "constraint_map":{"map_id":"cm-1"},
            "evidence":{"evidence_id":"ev-1","complete":True,"source_sha256":"src-1"},
            "source":{"sha256":"src-1"},
            "semantic_corroboration":{"status":"ACCESSIBLE"},
        }
    def test_matching_source_identity_passes(self):
        r=evaluate_runtime_release(self.base(),workflow_ok=True,final_validation_ok=True,regression_ok=True)
        self.assertEqual(r.status,"PASS")
    def test_mismatched_source_identity_blocks(self):
        x=self.base(); x["evidence"]["source_sha256"]="src-2"
        r=evaluate_runtime_release(x,workflow_ok=True,final_validation_ok=True,regression_ok=True)
        self.assertEqual(r.status,"BLOCKED")
    def test_missing_source_identity_blocks(self):
        x=self.base(); del x["evidence"]["source_sha256"]
        r=evaluate_runtime_release(x,workflow_ok=True,final_validation_ok=True,regression_ok=True)
        self.assertEqual(r.status,"BLOCKED")
if __name__=="__main__": unittest.main()
