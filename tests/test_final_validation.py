import unittest
from runtime.final_validation import validate_post_edit

class FinalValidationTests(unittest.TestCase):
    def test_clean_diff_passes(self):
        r=validate_post_edit({"locked_delta_ids":[],"unauthorized_delta_ids":[]})
        self.assertEqual(r.status,"PASS")
    def test_locked_delta_rejects(self):
        r=validate_post_edit({"locked_delta_ids":["C01"],"unauthorized_delta_ids":[]})
        self.assertEqual(r.status,"REJECT")
        self.assertIn("POST_EDIT_REJECTED",r.failure_codes)
    def test_unauthorized_delta_rejects(self):
        r=validate_post_edit({"locked_delta_ids":[],"unauthorized_delta_ids":["W01"]})
        self.assertEqual(r.status,"REJECT")
        self.assertIn("POST_EDIT_UNAUTHORIZED_DELTA",r.failure_codes)

if __name__=="__main__": unittest.main()
