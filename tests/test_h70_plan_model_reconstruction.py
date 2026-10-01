import unittest

from runtime.plan_model_reconstruction import build_plan_model_from_detection


class H70PlanModelReconstructionTests(unittest.TestCase):
    SHA = "a" * 64

    def detection(self):
        return {
            "source_sha256": self.SHA,
            "candidates": [
                {"candidate_id": "W01", "element_type": "WALLS", "bbox": [0, 0, 100, 20], "confidence": 0.82, "evidence_ids": ["E-WALL"], "status": "UNKNOWN", "rationale": "Wall geometry evidence."},
                {"candidate_id": "C01", "element_type": "COLUMNS", "bbox": [20, 20, 40, 40], "confidence": 0.96, "evidence_ids": ["E-COLUMN"], "status": "LOCKED", "rationale": "Column evidence."},
            ],
            "unresolved_fixed_element_types": ["OUTER_BOUNDARY", "WALLS", "DOORS", "WINDOWS", "OVERALL_PLAN_FORM"],
        }

    def test_reconstructs_and_preserves_uncertainty(self):
        result = build_plan_model_from_detection(model_id="PM01", source_sha256=self.SHA, detection_result=self.detection())
        self.assertEqual(len(result.plan_model.elements), 2)
        self.assertEqual(result.plan_model.elements[0].state, "UNKNOWN")
        self.assertEqual(result.plan_model.elements[1].state, "LOCKED")
        self.assertIn("WALLS", result.plan_model.unresolved)
        result.plan_model.validate()

    def test_source_mismatch_rejected(self):
        with self.assertRaisesRegex(ValueError, "PLAN_RECONSTRUCTION_SOURCE_MISMATCH"):
            build_plan_model_from_detection(model_id="PM01", source_sha256=self.SHA, detection_result={**self.detection(), "source_sha256": "b" * 64})

    def test_evidence_is_source_bound_and_queryable(self):
        result = build_plan_model_from_detection(model_id="PM01", source_sha256=self.SHA, detection_result=self.detection())
        bundle = result.plan_model.element_evidence
        self.assertEqual(bundle.source_sha256, self.SHA)
        self.assertEqual(len(bundle.evidence_for("WALLS")), 1)
        self.assertIn("DOORS", bundle.unresolved_element_types)

    def test_duplicate_candidate_evidence_is_normalized(self):
        data = self.detection()
        data["candidates"][0]["evidence_ids"] = ["E-SAME", "E-SAME"]
        result = build_plan_model_from_detection(model_id="PM01", source_sha256=self.SHA, detection_result=data)
        self.assertEqual(len(result.plan_model.element_evidence.evidences), 2)
        self.assertEqual(result.plan_model.elements[0].evidence_ids, ("E-SAME", "E-SAME"))


if __name__ == "__main__":
    unittest.main()
