import unittest

from runtime.scale_unit_evidence import ScaleEvidence, evaluate_scale_evidence


class ScaleUnitEvidenceTests(unittest.TestCase):
    def test_two_independent_signals_pass_with_known_unit(self):
        result = evaluate_scale_evidence(
            source_id="dwg1", unit="MM", explicit_unit=True, header_unit=True,
            dimension_evidence=False, source_metadata=False, evidence_ids=("h", "u")
        )
        self.assertEqual(result.status, "PASS")
        self.assertTrue(result.scale_known)
        self.assertEqual(result.unit, "MM")

    def test_conflicting_units_block(self):
        result = evaluate_scale_evidence(
            source_id="dwg1", unit="MM", explicit_unit="MM", header_unit="CM",
            dimension_evidence=True, source_metadata=True, evidence_ids=("h", "u")
        )
        self.assertEqual(result.status, "BLOCKED")
        self.assertEqual(result.unit, "UNKNOWN")

    def test_single_signal_needs_review(self):
        result = evaluate_scale_evidence(
            source_id="dwg1", unit="MM", explicit_unit=True, header_unit=False,
            dimension_evidence=False, source_metadata=False, evidence_ids=("u",)
        )
        self.assertEqual(result.status, "NEEDS_REVIEW")

    def test_no_signal_unknown(self):
        result = evaluate_scale_evidence(
            source_id="dwg1", unit="UNKNOWN", explicit_unit=False, header_unit=False,
            dimension_evidence=False, source_metadata=False, evidence_ids=("src",)
        )
        self.assertEqual(result.status, "UNKNOWN")

    def test_multiple_signals_without_resolvable_unit_cannot_pass(self):
        result = evaluate_scale_evidence(
            source_id="dwg1", unit="UNKNOWN", explicit_unit=True, header_unit=True,
            dimension_evidence=False, source_metadata=False,
            evidence_ids=("explicit", "header")
        )
        self.assertEqual(result.status, "NEEDS_REVIEW")
        self.assertEqual(result.unit, "UNKNOWN")
        self.assertFalse(result.scale_known)

    def test_unknown_string_is_not_counted_as_unit_evidence(self):
        result = evaluate_scale_evidence(
            source_id="dwg1", unit="UNKNOWN", explicit_unit="UNKNOWN",
            header_unit="UNKNOWN", dimension_evidence=False, source_metadata=False,
            evidence_ids=("src",)
        )
        self.assertEqual(result.status, "UNKNOWN")

    def test_pass_with_unknown_unit_is_rejected_by_contract(self):
        evidence = ScaleEvidence("dwg1", "UNKNOWN", True, 0.99, ("e1", "e2"), "PASS")
        with self.assertRaisesRegex(
            ValueError, "SCALE_PASS_REQUIRES_VERIFIED_SCALE_AND_UNIT"
        ):
            evidence.validate()

    def test_units_are_normalized_before_pass(self):
        result = evaluate_scale_evidence(
            source_id="dwg1", unit="mm", explicit_unit="mm", header_unit="MM",
            dimension_evidence=False, source_metadata=False, evidence_ids=("text", "header")
        )
        self.assertEqual(result.status, "PASS")
        self.assertEqual(result.unit, "MM")

    def test_unsupported_unit_label_cannot_become_pass(self):
        result = evaluate_scale_evidence(
            source_id="dwg1", unit="MM", explicit_unit="MILLIMETERS",
            header_unit=True, dimension_evidence=False, source_metadata=False,
            evidence_ids=("text", "header")
        )
        self.assertEqual(result.status, "NEEDS_REVIEW")
        self.assertFalse(result.scale_known)


if __name__ == "__main__":
    unittest.main()
