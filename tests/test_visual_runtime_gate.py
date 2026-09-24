import unittest
from runtime.visual_runtime_gate import VisualRuntimeReadiness

class VisualRuntimeGateTests(unittest.TestCase):
    def test_missing_source_is_not_ready(self):
        r=VisualRuntimeReadiness("JPG",[],["SOURCE_DOCUMENT_MISSING"])
        self.assertFalse(r.ready)

    def test_real_evidence_without_blockers_is_ready(self):
        r=VisualRuntimeReadiness("PDF",["source","detection","post-edit"])
        self.assertTrue(r.ready)

    def test_unknown_blocker_is_rejected(self):
        with self.assertRaises(ValueError):
            VisualRuntimeReadiness("PNG",["source"],["FAKE_BLOCKER"]).validate()

if __name__=="__main__":
    unittest.main()
