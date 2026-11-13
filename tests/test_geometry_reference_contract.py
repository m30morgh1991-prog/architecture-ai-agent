import unittest

from runtime.geometry_reference_contract import build_geometry_reference


class GeometryReferenceContractTests(unittest.TestCase):
    def base(self, **overrides):
        data = {
            "reference_id": "geom-ref-01",
            "source_sha256": "a" * 64,
        }
        data.update(overrides)
        if "evidence_records" not in data:
            domains = {
                "coordinate_evidence_ids": "COORDINATE_FRAME",
                "unit_evidence_ids": "UNIT",
                "scale_evidence_ids": "SCALE",
                "transform_evidence_ids": "TRANSFORM",
                "dimension_evidence_ids": "DIMENSION",
            }
            records = []
            for field, domain in domains.items():
                for evidence_id in data.get(field, ()):
                    records.append({
                        "evidence_id": evidence_id,
                        "source_sha256": data["source_sha256"],
                        "domain": domain,
                        "status": "SUPPORTED",
                        "source_ref": "test-fixture",
                        "value": "test-value",
                    })
            data["evidence_records"] = records
        return build_geometry_reference(**data)

    def test_default_reference_is_unknown_and_cannot_report_metric_area(self):
        ref = self.base()
        self.assertEqual(ref.area_unit, "UNKNOWN")
        self.assertIsNone(ref.square_metre_factor)
        self.assertFalse(ref.can_report_area_m2)

    def test_verified_unit_requires_source_evidence(self):
        with self.assertRaisesRegex(ValueError, "GEOMETRY_REFERENCE_UNIT_SUPPORT_UNPROVEN"):
            self.base(linear_unit="MM", unit_status="SUPPORTED")

    def test_verified_mm_unit_exposes_area_conversion_only_with_evidence(self):
        ref = self.base(
            linear_unit="MM", unit_status="SUPPORTED",
            unit_evidence_ids=["unit-dim-01"],
        )
        self.assertEqual(ref.area_unit, "MM^2")
        self.assertAlmostEqual(ref.square_metre_factor, 1e-6)
        self.assertTrue(ref.can_report_area_m2)

    def test_supported_unit_rejects_uncertain_evidence_record(self):
        with self.assertRaisesRegex(ValueError, "GEOMETRY_REFERENCE_UNIT_EVIDENCE_NOT_SUPPORTED"):
            self.base(
                linear_unit="MM", unit_status="SUPPORTED",
                unit_evidence_ids=["unit-uncertain"],
                evidence_records=[{
                    "evidence_id": "unit-uncertain", "source_sha256": "a" * 64,
                    "domain": "UNIT", "status": "UNCERTAIN",
                    "source_ref": "ambiguous-header", "value": "MM",
                }],
            )

    def test_insunits_or_unit_label_without_supported_status_does_not_convert(self):
        ref = self.base(linear_unit="IN", unit_status="UNKNOWN")
        self.assertIsNone(ref.square_metre_factor)
        self.assertFalse(ref.can_report_area_m2)

    def test_supported_coordinate_frame_requires_evidence(self):
        with self.assertRaisesRegex(ValueError, "GEOMETRY_REFERENCE_FRAME_SUPPORT_UNPROVEN"):
            self.base(coordinate_frame="WCS", coordinate_frame_status="SUPPORTED")

    def test_paper_scale_is_separate_from_model_units(self):
        ref = self.base(
            linear_unit="UNKNOWN",
            scale_basis="PAPER_SPACE",
            scale_status="SUPPORTED",
            paper_scale_ratio=[1, 100],
            scale_evidence_ids=["title-block-scale-01"],
        )
        self.assertEqual(ref.paper_scale_ratio, (1, 100))
        self.assertFalse(ref.can_report_area_m2)

    def test_supported_paper_scale_requires_ratio(self):
        with self.assertRaisesRegex(ValueError, "GEOMETRY_REFERENCE_PAPER_SCALE_MISSING"):
            self.base(
                scale_basis="PAPER_SPACE", scale_status="SUPPORTED",
                scale_evidence_ids=["scale-note-01"],
            )

    def test_raster_calibration_requires_affine_transform(self):
        with self.assertRaisesRegex(ValueError, "GEOMETRY_REFERENCE_RASTER_CALIBRATION_MISSING"):
            self.base(
                scale_basis="RASTER_CALIBRATION", scale_status="SUPPORTED",
                scale_evidence_ids=["dimension-check-01"],
            )

    def test_raster_calibration_requires_invertible_transform_and_evidence(self):
        with self.assertRaisesRegex(ValueError, "GEOMETRY_REFERENCE_PIXEL_TRANSFORM_SINGULAR"):
            self.base(
                scale_basis="RASTER_CALIBRATION", scale_status="SUPPORTED",
                scale_evidence_ids=["dimension-check-01"],
                pixel_to_world_transform=[1, 0, 0, 0, 0, 0, 0, 0, 1],
                transform_evidence_ids=["calibration-01"],
            )

    def test_pixel_transform_rejects_non_finite_and_boolean_values(self):
        for invalid in (float("nan"), float("inf"), True):
            matrix = [1, 0, 0, 0, 1, 0, 0, 0, 1]
            matrix[0] = invalid
            with self.subTest(invalid=invalid):
                with self.assertRaisesRegex(ValueError, "GEOMETRY_REFERENCE_PIXEL_TRANSFORM_INVALID"):
                    self.base(
                        pixel_to_world_transform=matrix,
                        transform_evidence_ids=["calibration-01"],
                    )

    def test_supported_dimension_reconciliation_requires_dimension_evidence(self):
        with self.assertRaisesRegex(ValueError, "GEOMETRY_REFERENCE_DIMENSION_SUPPORT_UNPROVEN"):
            self.base(dimension_reconciliation_status="SUPPORTED")

    def test_duplicate_evidence_ids_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "GEOMETRY_REFERENCE_UNIT_EVIDENCE_INVALID"):
            self.base(
                linear_unit="CM", unit_status="SUPPORTED",
                unit_evidence_ids=["dim-1", "dim-1"],
            )

    def test_evidence_must_match_source_hash(self):
        with self.assertRaisesRegex(ValueError, "GEOMETRY_REFERENCE_EVIDENCE_SOURCE_MISMATCH"):
            self.base(
                linear_unit="MM", unit_status="SUPPORTED",
                unit_evidence_ids=["unit-01"],
                evidence_records=[{
                    "evidence_id": "unit-01", "source_sha256": "b" * 64,
                    "domain": "UNIT", "status": "SUPPORTED",
                    "source_ref": "drawing-header", "value": "MM",
                }],
            )

    def test_bad_source_hash_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "GEOMETRY_REFERENCE_SOURCE_HASH_INVALID"):
            self.base(source_sha256="not-a-hash")


if __name__ == "__main__":
    unittest.main()
