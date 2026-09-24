import unittest

from runtime.controlled_editing_contract import (
    EditPermission,
    ImpactDependency,
    UncertaintyAssessment,
    build_controlled_editing_decision,
)
from runtime.request_contract import ExecutionRequest


class ControlledEditingContractTests(unittest.TestCase):
    def test_locked_element_without_authorization_blocks(self):
        decision = build_controlled_editing_decision(
            [EditPermission("C01", "LOCKED")]
        )
        self.assertFalse(decision.executable)
        self.assertIn("LOCKED_ELEMENT_CONFLICT:C01", decision.blocking_reasons())

    def test_editable_element_is_executable(self):
        decision = build_controlled_editing_decision(
            [EditPermission("F01", "EDITABLE")]
        )
        self.assertTrue(decision.executable)

    def test_conditional_element_requires_conditions(self):
        decision = build_controlled_editing_decision(
            [EditPermission("D01", "CONDITIONAL", conditions=["clear_width_verified"])]
        )
        self.assertTrue(decision.executable)

        unresolved = build_controlled_editing_decision(
            [EditPermission("D02", "CONDITIONAL")]
        )
        self.assertFalse(unresolved.executable)

    def test_uncertainty_is_fail_closed(self):
        decision = build_controlled_editing_decision(
            [EditPermission("F01", "EDITABLE")],
            [UncertaintyAssessment("C01", "LOCKED_ELEMENT_UNCERTAIN", "not detected")]
        )
        # The canonical uncertainty state is UNKNOWN/SOURCE_REQUIRED/etc.; an
        # invalid state must be rejected rather than silently treated as safe.
        self.assertRaises(ValueError, decision.validate)

    def test_unknown_blocks_execution(self):
        decision = build_controlled_editing_decision(
            [EditPermission("F01", "EDITABLE")],
            [UncertaintyAssessment("C01", "UNKNOWN", "scale missing")]
        )
        self.assertFalse(decision.executable)
        self.assertIn("UNCERTAINTY_BLOCKING:UNKNOWN", decision.blocking_reasons())

    def test_impact_dependencies_are_exposed(self):
        impact = ImpactDependency("W01", ["D01", "R01"], ["door", "circulation"])
        decision = build_controlled_editing_decision(
            [EditPermission("W01", "EDITABLE")],
            impacts=[impact],
        )
        self.assertTrue(decision.executable)
        self.assertEqual(decision.impacts[0].affected_ids, ["D01", "R01"])

    def test_execution_request_preserves_legacy_contract_and_adds_context(self):
        request = ExecutionRequest.from_dict({
            "execution_id": "e1",
            "project_id": "p1",
            "input_version_id": "v1",
            "plan_id": "plan1",
            "request": {"change_type": "FURNITURE"},
            "edit_permissions": [{"element_id": "F01", "state": "EDITABLE"}],
            "uncertainty": [{"element_id": "C01", "state": "UNKNOWN"}],
            "impact_dependencies": [{"source_id": "F01", "affected_ids": ["R01"]}],
        })
        self.assertEqual(request.trace()["execution_id"], "e1")
        self.assertEqual(request.controlled_editing_context()["edit_permissions"][0]["element_id"], "F01")
        self.assertEqual(request.controlled_editing_context()["impact_dependencies"][0]["source_id"], "F01")

    def test_legacy_execution_request_still_works(self):
        request = ExecutionRequest.from_dict({
            "execution_id": "e2",
            "project_id": "p1",
            "input_version_id": "v1",
            "plan_id": "plan1",
            "request": {},
        })
        self.assertEqual(request.edit_permissions, [])
        self.assertEqual(request.uncertainty, [])
        self.assertEqual(request.impact_dependencies, [])


if __name__ == "__main__":
    unittest.main()
