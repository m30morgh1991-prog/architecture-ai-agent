import unittest

from runtime.post_edit_diff_validation import (
    build_post_edit_diff,
    build_post_edit_diff_from_runtime,
)


class PostEditDiffIntegrationTests(unittest.TestCase):
    def _det(self, element_id="F01", geometry=(0, 0), state="EDITABLE"):
        return {
            "native_dwg_candidates": [{
                "candidate_id": element_id,
                "element_type": "FURNITURE",
                "status": state,
                "geometry": geometry,
                "evidence_ids": ("E1",),
            }]
        }

    def test_clean_approved_change_passes(self):
        diff = build_post_edit_diff_from_runtime(
            before_detection=self._det(),
            after_detection=self._det(geometry=(10, 0)),
            source_sha256="a" * 64,
            model_id="M1",
            before_status="PASS",
            after_status="PASS",
            approved_target_ids=("F01",),
        )
        self.assertTrue(diff.valid)
        self.assertEqual(diff.status, "PASS")
        self.assertEqual(diff.changed_ids, ("F01",))

    def test_locked_change_blocks(self):
        diff = build_post_edit_diff_from_runtime(
            before_detection=self._det(),
            after_detection=self._det(geometry=(10, 0), state="LOCKED"),
            source_sha256="b" * 64,
            model_id="M2",
            before_status="PASS",
            after_status="PASS",
            approved_target_ids=("F01",),
        )
        self.assertFalse(diff.valid)
        self.assertEqual(diff.status, "BLOCKED")

    def test_unauthorized_change_blocks(self):
        diff = build_post_edit_diff_from_runtime(
            before_detection=self._det(),
            after_detection=self._det(geometry=(10, 0)),
            source_sha256="c" * 64,
            model_id="M3",
            before_status="PASS",
            after_status="PASS",
            approved_target_ids=(),
        )
        self.assertFalse(diff.valid)
        self.assertEqual(diff.status, "BLOCKED")
        self.assertEqual(diff.unauthorized_changes, ("F01",))

    def test_missing_before_after_input_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "BEFORE_AFTER_DETECTION_MISSING"):
            build_post_edit_diff(before_after=None)

    def test_missing_after_never_passes(self):
        diff = build_post_edit_diff_from_runtime(
            before_detection=self._det(),
            after_detection=None,
            source_sha256="d" * 64,
            model_id="M4",
            before_status="PASS",
            after_status=None,
            approved_target_ids=("F01",),
        )
        self.assertFalse(diff.valid)
        self.assertEqual(diff.status, "UNKNOWN")

    def test_identity_mismatch_is_blocked(self):
        from runtime.runtime_before_after import compare_runtime_detections
        from runtime.before_after_detection import DetectionSnapshot, compare_before_after

        before = DetectionSnapshot(
            source_sha256="e" * 64,
            model_id="M5",
            elements=(
                {"element_id": "F01", "element_type": "FURNITURE",
                 "state": "EDITABLE", "geometry": (0, 0), "evidence_ids": ("E1",)},
            ),
            status="PASS",
        )
        after = DetectionSnapshot(
            source_sha256="f" * 64,
            model_id="M5",
            elements=before.elements,
            status="PASS",
        )
        comparison = compare_before_after(
            before=before, after=after, approved_target_ids=("F01",)
        )
        self.assertEqual(comparison.status, "BLOCKED")

    def test_added_and_removed_never_pass(self):
        diff = build_post_edit_diff_from_runtime(
            before_detection=self._det(),
            after_detection={"native_dwg_candidates": []},
            source_sha256="g" * 64,
            model_id="M6",
            before_status="PASS",
            after_status="PASS",
            approved_target_ids=("F01",),
        )
        self.assertFalse(diff.valid)
        self.assertEqual(diff.status, "BLOCKED")
        self.assertEqual(diff.removed_ids, ("F01",))


if __name__ == "__main__":
    unittest.main()
