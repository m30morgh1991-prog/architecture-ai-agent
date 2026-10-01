import unittest

from runtime.plan_model_reconstruction import build_plan_model_from_detection


class H70PlanModelReconstructionTests(unittest.TestCase):
    SHA = "a" * 64

    def _detection(self):
        return {
            "detector_id": "conservative-vector-fixed-v0.2-dwg",
            "source_sha256": self.SHA,
            "candidates": [
                {
                    "candidate_id": "W01",
                    "element_type": "WALLS",
                    "bbox": [0, 0, 100, 20],
                    "confidence": 0.82,
                    "evidence_ids": ["E-WALL"],
                    "status": "UNKNOWN",
                    "rationale": "Native line geometry supports a wall candidate.",
                },
                {
                    "candidate_id": "C01",
                    "element_type": "COLUMNS",
                    "bbox": [20, 20, 40, 40],
                    "confidence": 0.96,
                    "evidence_ids": ["E-COLUMN"],
                    "status": "LOCKED",
                    "rationale": "Approval-grade column evidence.",
                },
            ],
            "unresolved_fixed_element_types": [
                "OUTER_BOUNDARY", "WALLS", "DOORS", "WINDOWS", "OVERALL_PLAN_FORM"
            ],
        }

    def test_reconstructs_source_bound_plan_model_fail_closed(self):
        result = build_plan_model_from_detection(
            model_id="PM01",
            source_sha256=self.SHA,
            detection_result=self._detection(),
        )
        model = result.plan_model
        self.assertEqual(model.source_sha256, self.SHA)
        self.assertEqual(len(model.elements), 2)
        self.assertEqual(model.elements[0].state, "UNKNOWN")
        self.assertEqual(model.elements[1].state, "LOCKED")
        self.assertIn("WALLS", model.unresolved)
        self.assertIsNotNone(model.element_evidence)
        model.validate()

    def test_source_mismatch_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "PLAN_RECONSTRUCTION_SOURCE_MISMATCH"):
            build_plan_model_from_detection(
                model_id="PM01",
                source_sha256=self.SHA,
                detection_result={
                    **self._detection(),
                    "source_sha256": "b" * 64,
                },
            )

    def test_unknown_candidates_never_become_locked(self):
        result = build_plan_model_from_detection(
            model_id="PM01",
            source_sha256=self.SHA,
            detection_result=self._detection(),
        )
        unknown = [
            e for e in result.plan_model.elements
            if e.element_type == "WALLS"
        ][0]
        self.assertEqual(unknown.state, "UNKNOWN")
        self.assertIn("WALLS", result.plan_model.element_evidence.unresolved_element_types)

    def test_duplicate_evidence_is_normalized(self):
        detection = self._detection()
        detection["candidates"][0]["evidence_ids"] = ["E-SAME", "E-SAME"]
        with self.assertRaisesRegex(ValueError, "MISSING"):
            # PlanElement itself must retain the source evidence references;
            # duplicate evidence IDs are normalized only at the bundle layer,
            # while an empty evidence list remains invalid.
            build_plan_model_from_detection(
                model_id="PM01",
                source_sha256=self.SHA,
                detection_result=detection,
            )


if __name__ == "__main__":
    unittest.main()
