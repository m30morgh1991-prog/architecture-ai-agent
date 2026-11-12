import unittest

from runtime.input_completeness_check import check_input_completeness
from runtime.input_source_contract import classify_source
from runtime.review_report_contract import build_report

SHA = "b" * 64
FULL = {
    "scale": "1:100", "units": "cm", "dimensions_geometry_associated": True,
    "view_section_identity": True, "sheet_layout_valid": True,
    "title_block_fields_valid": True,
}


def run(name="plan.dwg", metadata=None, **kw):
    return check_input_completeness(
        source_sha256=SHA, source_profile=classify_source(name, **kw), metadata=metadata)


def by_check(findings):
    return {f.check_id: f for f in findings}


class InputCompletenessTests(unittest.TestCase):
    def test_complete_vector_input_passes(self):
        f = run(metadata=FULL)
        self.assertTrue(all(x.status == "PASS" for x in f))
        self.assertEqual(build_report("r", "m", SHA, f).overall_status, "PASS")

    def test_missing_metadata_is_source_required_never_pass(self):
        f = by_check(run(metadata={}))
        for cid in ("INPUT-SCALE-001", "INPUT-UNITS-001", "INPUT-DIM-001", "INPUT-TITLE-001"):
            self.assertEqual(f[cid].status, "SOURCE_REQUIRED", cid)
        self.assertEqual(build_report("r", "m", SHA, f.values()).overall_status, "SOURCE_REQUIRED")

    def test_placeholder_scale_and_units_are_not_pass(self):
        f = by_check(run(metadata=dict(FULL, scale="unknown", units="?")))
        self.assertEqual(f["INPUT-SCALE-001"].status, "SOURCE_REQUIRED")
        self.assertEqual(f["INPUT-UNITS-001"].status, "SOURCE_REQUIRED")

    def test_malformed_scale_requires_review(self):
        f = by_check(run(metadata=dict(FULL, scale="one hundred")))
        self.assertEqual(f["INPUT-SCALE-001"].status, "NEEDS_REVIEW")

    def test_zero_scale_ratio_requires_review(self):
        f = by_check(run(metadata=dict(FULL, scale="1:0")))
        self.assertEqual(f["INPUT-SCALE-001"].status, "NEEDS_REVIEW")

    def test_unitless_metadata_requires_review(self):
        f = by_check(run(metadata=dict(FULL, units="unitless")))
        self.assertEqual(f["INPUT-UNITS-001"].status, "NEEDS_REVIEW")

    def test_unknown_unit_token_requires_review(self):
        f = by_check(run(metadata=dict(FULL, units="mystery-units")))
        self.assertEqual(f["INPUT-UNITS-001"].status, "NEEDS_REVIEW")

    def test_none_metadata_behaves_like_empty(self):
        self.assertEqual(by_check(run(metadata=None))["INPUT-SCALE-001"].status, "SOURCE_REQUIRED")

    def test_explicit_false_blocks(self):
        meta = dict(FULL, dimensions_geometry_associated=False)
        f = by_check(run(metadata=meta))["INPUT-DIM-001"]
        self.assertEqual((f.status, f.severity), ("BLOCKED", "BLOCKING"))

    def test_blank_scale_string_is_not_present(self):
        self.assertEqual(by_check(run(metadata=dict(FULL, scale="  ")))["INPUT-SCALE-001"].status,
                         "SOURCE_REQUIRED")

    def test_raster_image_needs_review(self):
        f = by_check(run("photo.png", FULL))["INPUT-TRUST-001"]
        self.assertEqual(f.status, "NEEDS_REVIEW")

    def test_unclassified_pdf_requires_inspection(self):
        f = by_check(run("plan.pdf", FULL))["INPUT-TRUST-001"]
        self.assertEqual(f.status, "SOURCE_REQUIRED")

    def test_vector_pdf_passes_trust(self):
        f = by_check(run("plan.pdf", FULL, pdf_representation="vector"))["INPUT-TRUST-001"]
        self.assertEqual(f.status, "PASS")

    def test_inch_units_need_review(self):
        f = by_check(run(metadata=dict(FULL, units="in")))
        self.assertEqual(f["INPUT-INCH-001"].status, "NEEDS_REVIEW")

    def test_bad_hash_rejected(self):
        with self.assertRaisesRegex(ValueError, "INPUT_COMPLETENESS_SOURCE_INVALID"):
            check_input_completeness(source_sha256="x", source_profile=classify_source("a.dwg"))

    def test_supplied_evidence_ids_are_used(self):
        f = check_input_completeness(source_sha256=SHA, source_profile=classify_source("a.dwg"),
                                     metadata=FULL, evidence_ids=["dwg-$INSUNITS"])
        self.assertTrue(all(x.evidence_ids == ("dwg-$INSUNITS",) for x in f))


if __name__ == "__main__":
    unittest.main()
