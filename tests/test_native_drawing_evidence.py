import unittest
from runtime.native_drawing_evidence import cross_view_consistency

class NativeDrawingEvidenceTests(unittest.TestCase):
    def test_cross_view_stays_unknown_without_correspondence(self):
        self.assertIsNone(cross_view_consistency([])["cross_view_consistent"])

    def test_cross_view_accepts_verified_correspondence(self):
        result=cross_view_consistency([
            {"identity":"PLAN","fingerprint":"a","evidence_id":"p","correspondence_verified":True},
            {"identity":"SECTION","fingerprint":"b","evidence_id":"s","correspondence_verified":True},
        ])
        self.assertTrue(result["cross_view_consistent"])

    def test_cross_view_blocks_explicit_contradiction(self):
        result=cross_view_consistency([
            {"identity":"PLAN","fingerprint":"a","evidence_id":"p","correspondence_verified":False},
            {"identity":"SECTION","fingerprint":"b","evidence_id":"s","correspondence_verified":False},
        ])
        self.assertFalse(result["cross_view_consistent"])
        self.assertIn("VIEW_CORRESPONDENCE_CONTRADICTION",result["unresolved"])

if __name__=="__main__": unittest.main()
