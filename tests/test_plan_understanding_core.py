import unittest

from runtime.plan_understanding_core import PlanUnderstandingCore


class _Detector:
    def detect(self, source_path, source_sha256):
        return {
            "status": "UNKNOWN",
            "source_sha256": source_sha256,
            "candidates": [
                {
                    "candidate_id": "W01",
                    "element_type": "WALLS",
                    "bbox": [0, 0, 10, 10],
                    "confidence": 0.82,
                    "evidence_ids": ["ev-w01"],
                    "status": "UNKNOWN",
                    "rationale": "Wall candidate only.",
                }
            ],
            "unresolved_fixed_element_types": [
                "COLUMNS", "OUTER_BOUNDARY", "DOORS", "WINDOWS", "OVERALL_PLAN_FORM"
            ],
        }


class PlanUnderstandingCoreTests(unittest.TestCase):
    def test_core_composes_detection_planmodel_and_constraintmap_fail_closed(self):
        source = "a" * 64
        result = PlanUnderstandingCore(detector=_Detector()).understand(
            source_path="drawing.dwg",
            source_sha256=source,
            model_id="pm-h98",
        )
        self.assertEqual(result.status, "UNKNOWN")
        self.assertEqual(result.plan_model.source_sha256, source)
        self.assertIn("W01", result.constraint_map.unknown_element_ids)
        self.assertIn("COLUMNS", result.constraint_map.unknown_element_ids)
        result.validate()

    def test_empty_detection_returns_unknown_without_crashing(self):
        class _EmptyDetector:
            def detect(self, source_path, source_sha256):
                return {
                    "status": "UNKNOWN",
                    "source_sha256": source_sha256,
                    "candidates": [],
                    "unresolved_fixed_element_types": [
                        "COLUMNS", "OUTER_BOUNDARY", "WALLS",
                        "DOORS", "WINDOWS", "OVERALL_PLAN_FORM",
                    ],
                }

        source = "c" * 64
        result = PlanUnderstandingCore(detector=_EmptyDetector()).understand(
            source_path="empty-evidence.dwg",
            source_sha256=source,
            model_id="pm-empty",
        )

        self.assertEqual(result.status, "UNKNOWN")
        self.assertEqual(result.plan_model.elements, ())
        self.assertEqual(len(result.plan_model.element_evidence.evidences), 6)
        self.assertTrue(result.constraint_map.evidence_ids)
        self.assertEqual(
            set(result.constraint_map.unknown_element_ids),
            {"COLUMNS", "OUTER_BOUNDARY", "WALLS", "DOORS", "WINDOWS", "OVERALL_PLAN_FORM"},
        )
        result.validate()

    def test_unknown_evidence_never_becomes_locked(self):
        source = "b" * 64
        result = PlanUnderstandingCore(detector=_Detector()).understand(
            source_path="drawing.dwg",
            source_sha256=source,
            model_id="pm-h98-2",
        )
        self.assertEqual(result.constraint_map.protected_element_ids, ())
        self.assertNotEqual(result.status, "PASS")


if __name__ == "__main__":
    unittest.main()
