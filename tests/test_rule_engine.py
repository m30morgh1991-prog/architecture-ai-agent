import unittest

from runtime.change_request_contract import ChangeRequest
from runtime.impact_analysis import analyze_impact
from runtime.plan_model_contract import ConstraintMap, PlanElement, PlanModel
from runtime.rule_context import ProjectRuleContext
from runtime.rule_engine import ArchitectureRule, evaluate_rules

SOURCE = "a" * 64


def plan_and_impact():
    plan = PlanModel(
        model_id="pm-76",
        source_sha256=SOURCE,
        drawing_count=1,
        elements=(
            PlanElement("F01", "FURNITURE", "EDITABLE",
                        {"kind": "bbox", "bbox": [0, 0, 1, 1]},
                        ("ev-f01",), 0.95),
        ),
    )
    cmap = ConstraintMap(
        map_id="cm-76", model_id="pm-76",
        protected_element_ids=(),
        editable_element_ids=("F01",),
        conditional_element_ids=(),
        unknown_element_ids=(),
        evidence_ids=("ev-f01",),
    )
    request = ChangeRequest(
        request_id="cr-76", source_sha256=SOURCE, model_id="pm-76",
        change_type="FURNITURE_LAYOUT_CHANGE",
        instruction="Move the sofa.",
        target_ids=("F01",), evidence_ids=("ev-f01",),
    )
    impact = analyze_impact(plan, cmap, request)
    return plan, cmap, impact


class RuleEngineTests(unittest.TestCase):
    def rule(self, **kwargs):
        data = dict(
            rule_id="R-DOOR-001",
            source_id="nbr-55",
            version="2026",
            authority_level="BINDING",
            applicability="residential",
            requirement="Effective clear opening must satisfy the applicable threshold.",
            evidence_ids=("rule-ev-1",),
        )
        data.update(kwargs)
        return ArchitectureRule(**data)

    def context(self, **kwargs):
        data = dict(
            jurisdiction="Iran",
            project_type="residential",
            authority_scope=["national"],
            source_ids=["ctx-1"],
            version="2026",
        )
        data.update(kwargs)
        return ProjectRuleContext(**data)

    def test_applicable_evidenced_rule_is_review_not_implicit_pass(self):
        plan, cmap, impact = plan_and_impact()
        result = evaluate_rules(plan, cmap, impact, self.context(), [self.rule()])
        self.assertEqual(result.status, "NEEDS_REVIEW")
        self.assertIn("RULE_CHECK_REQUIRED:R-DOOR-001", result.blockers)
        self.assertEqual(result.decisions[0].authority_level, "BINDING")

    def test_missing_rule_set_fails_closed(self):
        plan, cmap, impact = plan_and_impact()
        result = evaluate_rules(plan, cmap, impact, self.context(), [])
        self.assertEqual(result.status, "UNKNOWN")
        self.assertIn("RULE_SET_MISSING", result.blockers)

    def test_blocked_impact_blocks_rules(self):
        plan, cmap, impact = plan_and_impact()
        blocked_impact = impact.__class__(
            SOURCE, "pm-76", "cr-76", "BLOCKED", blockers=("PROTECTED_TARGET",)
        )
        result = evaluate_rules(plan, cmap, blocked_impact, self.context(), [self.rule()])
        self.assertEqual(result.status, "BLOCKED")
        self.assertIn("IMPACT_NOT_APPROVABLE", result.blockers)

    def test_context_source_is_required(self):
        plan, cmap, impact = plan_and_impact()
        with self.assertRaises(ValueError):
            evaluate_rules(plan, cmap, impact, self.context(source_ids=[]), [self.rule()])

    def test_authority_order_is_deterministic(self):
        plan, cmap, impact = plan_and_impact()
        rules = [
            self.rule(rule_id="R-TECH", authority_level="TECHNICAL"),
            self.rule(rule_id="R-BIND", authority_level="BINDING"),
            self.rule(rule_id="R-OFFICIAL", authority_level="OFFICIAL_STANDARD"),
        ]
        result = evaluate_rules(plan, cmap, impact, self.context(), rules)
        self.assertEqual(
            [d.rule_id for d in result.decisions],
            ["R-BIND", "R-OFFICIAL", "R-TECH"],
        )


if __name__ == "__main__":
    unittest.main()
