import unittest
from runtime.visual_evidence import VisualEvidence, REQUIRED_STAGES

class VisualEvidenceTests(unittest.TestCase):
    def test_complete_ordered_evidence_is_complete(self):
        e=VisualEvidence("ev1","JPG",REQUIRED_STAGES.copy())
        self.assertTrue(e.complete)

    def test_incomplete_evidence_is_not_complete(self):
        e=VisualEvidence("ev2","PDF",["SOURCE","DETECTION"])
        self.assertFalse(e.complete)

    def test_wrong_stage_order_is_rejected(self):
        with self.assertRaises(ValueError):
            VisualEvidence("ev3","PNG",["DETECTION","SOURCE"]).validate()

if __name__=="__main__":
    unittest.main()
