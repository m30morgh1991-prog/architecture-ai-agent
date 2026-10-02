import unittest

from runtime.post_edit_diff_validation import build_post_edit_diff


class PostEditDiffIntegrationTests(unittest.TestCase):
    def _det(self, element_id="F01", geometry=(0, 0)):
        return {
            "native_dwg_candidates": [{
                "candidate_id": element_id,
                "element_type": "FURNITURE",
                "status": "EDITABLE",
                "geometry": geometry,
                "evidence_ids": ("E1",),
            }]
        }

    def test_clean_approved_change_passes(self):
        before = self._det(geometry=(0, 0))
        after = self._det(geometry=(10, 0))
        diff = build_post_edit_diff(
            before_after=__import__("runtime.runtime_before_after", fromlist=["compare_runtime_detections"]).compare_runtime_detections(
                before_detection=before,
                after_detection=after,
                source_sha256="a" * 64,
                model_id="M1",
                before_status="PASS",
                after_status="PASS",
                approved_target_ids=("F01",),
            )
        )
        self.assertTrue(diff.valid)
        self.assertEqual(diff.status, "PASS")
        self.assertEqual(diff.changed_ids, ("F01",))

    def test_locked_change_blocks(self):
        before = self._det()
        after = self._det()
        after["native_dwg_candidates"][0]["status"] = "LOCKED"
        after["native_dwg_candidates"][0]["geometry"] = (10, 0)
        from runtime.runtime_before_after import compare_runtime_detections
        comparison = compare_runtime_detections(
            before_detection=before,
            after_detection=after,
            source_sha256="b" * 64,
            model_id="M2",
            before_status="PASS",
            after_status="PASS",
            approved_target_ids=("F01",),
        )
        diff = build_post_edit_diff(before_after=comparison)
        self.assertFalse(diff.valid)
        self.assertEqual(diff.status, "BLOCKED")

    def test_missing_after_never_passes(self):
        from runtime.runtime_before_after import compare_runtime_detections
        comparison = compare_runtime_detections(
            before_detection=self._det(),
            after_detection=None,
            source_sha256="c" * 64,
            model_id="M3",
            before_status="PASS",
            after_status=None,
            approved_target_ids=("F01",),
        )
        diff = build_post_edit_diff(before_after=comparison)
        self.assertFalse(diff.valid)
        self.assertEqual(diff.status, "UNKNOWN")


if __name__ == "__main__":
    unittest.main()
