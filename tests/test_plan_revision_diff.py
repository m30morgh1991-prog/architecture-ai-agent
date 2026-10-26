import unittest

from runtime.plan_model_contract import PlanElement, PlanModel
from runtime.plan_revision_diff import compute_revision_diff, revision_findings, to_post_edit_diff
from runtime.review_report_contract import build_report

SHA_A, SHA_B = "c" * 64, "d" * 64


def el(eid, etype="column", state="LOCKED", geom=None, conf=0.99):
    return PlanElement(eid, etype, state, geom if geom is not None else {"x": 0.0, "y": 0.0},
                       ("ev",), conf)


def model(mid, sha, *elements):
    return PlanModel(mid, sha, 1, tuple(elements))


def diff(base, revised, **kw):
    kw.setdefault("same_coordinate_frame", True)
    return compute_revision_diff(base, revised, **kw)


class RevisionDiffTests(unittest.TestCase):
    def setUp(self):
        self.base = model("A", SHA_A, el("C01"), el("F01", "sofa", "EDITABLE", {"x": 1.0}, 0.95),
                          el("D01", "door", "CONDITIONAL", {"x": 5.0}, 0.9))

    def test_identical_models_have_no_changes(self):
        d = diff(self.base, model("B", SHA_B, *self.base.elements))
        self.assertEqual(d.changes, ())
        self.assertTrue(d.clean)
        self.assertEqual(revision_findings(d)[0].status, "PASS")

    def test_coordinate_frame_must_be_attested(self):
        with self.assertRaisesRegex(ValueError, "COORDINATE_FRAME_NOT_ESTABLISHED"):
            compute_revision_diff(self.base, self.base, same_coordinate_frame=False)

    def test_negative_tolerance_rejected(self):
        with self.assertRaisesRegex(ValueError, "TOLERANCE_INVALID"):
            diff(self.base, self.base, tolerance=-1)

    def test_moved_locked_column_is_blocked(self):
        rev = model("B", SHA_B, el("C01", geom={"x": 0.5, "y": 0.0}), *self.base.elements[1:])
        d = diff(self.base, rev)
        self.assertFalse(d.clean)
        f = revision_findings(d)
        self.assertEqual(build_report("r", "B", SHA_B, f).overall_status, "BLOCKED")
        self.assertEqual(f[0].check_id, "REV-LOCKED-001")

    def test_removed_locked_column_is_blocked(self):
        rev = model("B", SHA_B, *self.base.elements[1:])
        d = diff(self.base, rev)
        self.assertEqual(d.protection_violations[0].change_type, "REMOVED")

    def test_unlocking_a_locked_element_is_blocked(self):
        rev = model("B", SHA_B, el("C01", state="EDITABLE", conf=0.95), *self.base.elements[1:])
        self.assertFalse(diff(self.base, rev).clean)

    def test_editable_change_is_informational_only(self):
        rev = model("B", SHA_B, self.base.elements[0], el("F01", "sofa", "EDITABLE", {"x": 2.0}, 0.95),
                    self.base.elements[2])
        d = diff(self.base, rev)
        self.assertTrue(d.clean)
        self.assertEqual(build_report("r", "B", SHA_B, revision_findings(d)).overall_status, "PASS")

    def test_conditional_change_needs_review(self):
        rev = model("B", SHA_B, *self.base.elements[:2], el("D01", "door", "CONDITIONAL", {"x": 6.0}, 0.9))
        f = revision_findings(diff(self.base, rev))
        self.assertEqual(f[0].status, "NEEDS_REVIEW")

    def test_protected_ids_from_constraint_map_are_enforced(self):
        rev = model("B", SHA_B, self.base.elements[0], el("F01", "sofa", "EDITABLE", {"x": 9.0}, 0.95),
                    self.base.elements[2])
        self.assertFalse(diff(self.base, rev, protected_element_ids=["F01"]).clean)

    def test_new_locked_element_needs_review(self):
        rev = model("B", SHA_B, *self.base.elements, el("C02"))
        f = revision_findings(diff(self.base, rev))
        self.assertEqual(f[0].check_id, "REV-ADDED-LOCKED-001")
        self.assertEqual(f[0].status, "NEEDS_REVIEW")

    def test_renumbered_element_is_removed_plus_added_never_matched(self):
        rev = model("B", SHA_B, el("C99"), *self.base.elements[1:])
        kinds = sorted(c.change_type for c in diff(self.base, rev).changes)
        self.assertEqual(kinds, ["ADDED", "REMOVED"])

    def test_tolerance_absorbs_float_noise_only_when_given(self):
        rev = model("B", SHA_B, el("C01", geom={"x": 1e-9, "y": 0.0}), *self.base.elements[1:])
        self.assertFalse(diff(self.base, rev).clean)
        self.assertTrue(diff(self.base, rev, tolerance=1e-6).clean)

    def test_nan_geometry_never_equal(self):
        nan = float("nan")
        base = model("A", SHA_A, el("F01", "sofa", "EDITABLE", {"x": nan}, 0.95))
        rev = model("B", SHA_B, el("F01", "sofa", "EDITABLE", {"x": nan}, 0.95))
        self.assertEqual(len(diff(base, rev, tolerance=1.0).changes), 1)

    def test_post_edit_diff_never_authorizes_protected_changes(self):
        rev = model("B", SHA_B, el("C01", geom={"x": 3.0, "y": 0.0}),
                    el("F01", "sofa", "EDITABLE", {"x": 2.0}, 0.95), self.base.elements[2])
        d = diff(self.base, rev)
        ped = to_post_edit_diff(d, authorized_element_ids=["C01", "F01"])
        self.assertFalse(ped.clean)
        self.assertEqual([x.element_id for x in ped.unauthorized_deltas], ["C01"])

    def test_invalid_models_are_rejected(self):
        bad = PlanModel("X", "short", 1, ())
        with self.assertRaises(ValueError):
            diff(bad, self.base)


if __name__ == "__main__":
    unittest.main()
