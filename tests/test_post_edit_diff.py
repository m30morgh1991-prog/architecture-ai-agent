import unittest
from runtime.post_edit_diff import Delta, PostEditDiff

class PostEditDiffTests(unittest.TestCase):
    def test_unauthorized_delta_is_detected(self):
        d=PostEditDiff("d1","v1","v2",[Delta("C01","x","1","2",False)])
        self.assertFalse(d.clean)
        self.assertEqual(len(d.unauthorized_deltas),1)

    def test_authorized_delta_is_clean(self):
        d=PostEditDiff("d2","v1","v2",[Delta("F01","x","1","2",True)])
        self.assertTrue(d.clean)

    def test_traceability_required(self):
        with self.assertRaises(ValueError):
            PostEditDiff("","","v2").validate()

if __name__=="__main__":
    unittest.main()
