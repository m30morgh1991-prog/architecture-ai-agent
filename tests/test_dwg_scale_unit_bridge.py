import unittest

from runtime.dwg_scale_unit_bridge import observe_dwg_scale_unit


class DwgScaleUnitBridgeTests(unittest.TestCase):
    def test_known_insunits_is_review_only_without_dimension_scale_evidence(self):
        result = observe_dwg_scale_unit({"dwg_units": 4}, "a" * 64)
        self.assertEqual(result["unit"], "MM")
        self.assertEqual(result["status"], "NEEDS_REVIEW")
        self.assertFalse(result["scale_known"])
        self.assertEqual(result["source_id"], "a" * 64)
        self.assertTrue(result["evidence_ids"])

    def test_unknown_or_unitless_insunits_remains_unknown(self):
        for raw in (0, 3, 999, None, "4", True):
            with self.subTest(raw=raw):
                result = observe_dwg_scale_unit({"dwg_units": raw}, "b" * 64)
                self.assertEqual(result["unit"], "UNKNOWN")
                self.assertEqual(result["status"], "UNKNOWN")
                self.assertFalse(result["scale_known"])

    def test_missing_unit_metadata_remains_unknown(self):
        result = observe_dwg_scale_unit({}, "c" * 64)
        self.assertEqual(result["status"], "UNKNOWN")
        self.assertEqual(result["unit"], "UNKNOWN")


if __name__ == "__main__":
    unittest.main()
