import json
import unittest
from dataclasses import replace

from runtime.conflict_validation_contract import Conflict, ValidationResult
from runtime.drawing_standards_validation import validate_drawing_standards
from runtime.review_report_contract import (
    Finding,
    ReviewReport,
    build_report,
    findings_from_drawing_standards,
    findings_from_rule_evaluation,
    findings_from_validation_result,
)
from runtime.rule_engine import RuleDecision, RuleEvaluation

SHA = "a" * 64


def finding(fid="F1", status="NEEDS_REVIEW", severity="WARNING", **kw):
    base = dict(finding_id=fid, category="RULE", check_id="R-1", status=status,
                severity=severity, message="msg", evidence_ids=("ev1",))
    base.update(kw)
    return Finding(**base)


def report(*findings):
    return build_report("rep1", "model1", SHA, findings)


class FindingValidationTests(unittest.TestCase):
    def test_finding_without_evidence_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "FINDING_EVIDENCE_MISSING"):
            finding(evidence_ids=()).validate()

    def test_pass_must_be_info(self):
        with self.assertRaisesRegex(ValueError, "PASS_FINDING_SEVERITY_INVALID"):
            finding(status="PASS", severity="WARNING").validate()

    def test_blocked_must_be_blocking(self):
        with self.assertRaisesRegex(ValueError, "BLOCKED_FINDING_SEVERITY_INVALID"):
            finding(status="BLOCKED", severity="WARNING").validate()

    def test_disposition_requires_reviewer_and_reason(self):
        with self.assertRaisesRegex(ValueError, "DISPOSITION_REVIEWER_MISSING"):
            finding(disposition="OVERRIDDEN", disposition_reason="ok").validate()
        with self.assertRaisesRegex(ValueError, "DISPOSITION_REASON_MISSING"):
            finding(disposition="OVERRIDDEN", reviewer_id="r1").validate()

    def test_blocking_cannot_be_overridden(self):
        f = finding(status="BLOCKED", severity="BLOCKING", disposition="OVERRIDDEN",
                    reviewer_id="r1", disposition_reason="trust me")
        with self.assertRaisesRegex(ValueError, "OVERRIDE_NOT_ALLOWED_FOR_BLOCKING"):
            f.validate()

    def test_pass_finding_takes_no_disposition(self):
        f = finding(status="PASS", severity="INFO", disposition="ACKNOWLEDGED",
                    reviewer_id="r1", disposition_reason="ok")
        with self.assertRaisesRegex(ValueError, "PASS_FINDING_NEEDS_NO_DISPOSITION"):
            f.validate()


class ReviewReportTests(unittest.TestCase):
    def test_empty_report_is_unknown_not_pass(self):
        self.assertEqual(report().overall_status, "UNKNOWN")
        self.assertFalse(report().human_review_complete)

    def test_status_precedence(self):
        r = report(finding("a", "PASS", "INFO"), finding("b", "UNKNOWN"),
                   finding("c", "NEEDS_REVIEW"), finding("d", "SOURCE_REQUIRED"))
        self.assertEqual(r.overall_status, "SOURCE_REQUIRED")
        r = report(r.findings[0], finding("e", "BLOCKED", "BLOCKING"))
        self.assertEqual(r.overall_status, "BLOCKED")

    def test_all_pass_is_pass(self):
        self.assertEqual(report(finding("a", "PASS", "INFO")).overall_status, "PASS")

    def test_duplicate_finding_ids_rejected(self):
        with self.assertRaisesRegex(ValueError, "FINDING_ID_DUPLICATE"):
            report(finding("x"), finding("x"))

    def test_bad_source_hash_rejected(self):
        with self.assertRaisesRegex(ValueError, "REVIEW_REPORT_SOURCE_INVALID"):
            build_report("r", "m", "short", [finding()])

    def test_override_never_changes_status_to_pass(self):
        r = report(finding("u", "UNKNOWN"))
        r2 = r.with_disposition("u", "OVERRIDDEN", reviewer_id="eng1", reason="site verified")
        self.assertEqual(r2.overall_status, "UNKNOWN")
        self.assertTrue(r2.human_review_complete)
        self.assertEqual(r.findings[0].disposition, "PENDING")  # original untouched

    def test_acknowledged_is_not_resolved(self):
        r = report(finding("n", "NEEDS_REVIEW")).with_disposition(
            "n", "ACKNOWLEDGED", reviewer_id="eng1", reason="seen")
        self.assertFalse(r.human_review_complete)

    def test_blocked_finding_cannot_be_overridden_via_report(self):
        r = report(finding("b", "BLOCKED", "BLOCKING"))
        with self.assertRaisesRegex(ValueError, "OVERRIDE_NOT_ALLOWED_FOR_BLOCKING"):
            r.with_disposition("b", "OVERRIDDEN", reviewer_id="eng1", reason="x")

    def test_unknown_finding_id_rejected(self):
        with self.assertRaisesRegex(ValueError, "FINDING_NOT_FOUND"):
            report(finding()).with_disposition("nope", "OVERRIDDEN", reviewer_id="a", reason="b")

    def test_to_dict_is_deterministic_json(self):
        r = report(finding("a", "PASS", "INFO"), finding("b"))
        self.assertEqual(json.dumps(r.to_dict(), sort_keys=True),
                         json.dumps(r.to_dict(), sort_keys=True))
        self.assertEqual(r.to_dict()["summary"]["PASS"], 1)


class AdapterTests(unittest.TestCase):
    def test_rule_evaluation_adapter(self):
        decisions = (
            RuleDecision("R-OK", "PASS", "SRC1", "1", "BINDING", "fine", ("e1",)),
            RuleDecision("R-NO", "BLOCKED", "SRC1", "1", "BINDING", "violates", ("e2",)),
        )
        ev = RuleEvaluation("m1", SHA, "BLOCKED", decisions, ("RULE_INPUT_MODEL_MISMATCH",))
        found = findings_from_rule_evaluation(ev)
        self.assertEqual(len(found), 3)
        self.assertEqual({f.status for f in found}, {"PASS", "BLOCKED"})
        self.assertEqual(report(*found).overall_status, "BLOCKED")

    def test_drawing_standards_adapter_marks_missing_as_source_required(self):
        v = validate_drawing_standards(source_sha256=SHA, evidence_ids=["e1"],
                                       metadata={"scale_units_consistent": True,
                                                 "title_block_fields_valid": False})
        found = findings_from_drawing_standards(v)
        by_id = {f.check_id: f.status for f in found}
        self.assertEqual(by_id["DRAW-SCALE-001"], "PASS")
        self.assertEqual(by_id["DRAW-TITLE-001"], "BLOCKED")
        self.assertEqual(by_id["DRAW-DIM-001"], "SOURCE_REQUIRED")

    def test_validation_result_adapter_keeps_state_visible(self):
        res = ValidationResult("v1", "UNKNOWN", [Conflict("c1", "OVERLAP", "INFO", ["W1"])])
        found = findings_from_validation_result(res)
        self.assertEqual(report(*found).overall_status, "UNKNOWN")
        self.assertEqual([f for f in found if f.check_id == "OVERLAP"][0].element_ids, ("W1",))

    def test_blocking_conflict_blocks(self):
        res = ValidationResult("v2", "PASS", [Conflict("c2", "COLUMN_MOVED", "BLOCKING", ["C1"])])
        self.assertEqual(report(*findings_from_validation_result(res)).overall_status, "BLOCKED")


if __name__ == "__main__":
    unittest.main()
