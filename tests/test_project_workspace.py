import unittest

from runtime.contracts import Element, PlanModel, ChangeRequest
from runtime.project_workspace import ProjectWorkspaceAdapter


class ProjectWorkspaceAdapterTests(unittest.TestCase):
    def setUp(self):
        self.adapter = ProjectWorkspaceAdapter()
        self.workspace = self.adapter.create_project("PRJ-001", "Residential Test")
        self.plan = PlanModel("PLAN-001", [
            Element("C01", "COLUMN", "LOCKED", {"x": 1, "y": 1}),
            Element("F01", "FURNITURE", "EDITABLE", {"x": 2, "y": 2}),
        ])

    def test_attach_plan_creates_working_version(self):
        version = self.adapter.attach_plan(self.workspace, self.plan, "V001")
        self.assertEqual(version.status, "WORKING")
        self.assertEqual(self.workspace.active_version_id, "V001")

    def test_change_request_is_project_context(self):
        request = ChangeRequest("FURNITURE", ["F01"], "Move sofa")
        self.adapter.record_change_request(self.workspace, request)
        self.assertEqual(
            self.workspace.context["change_requests"][0]["target_ids"], ["F01"]
        )

    def test_only_validated_version_can_be_promoted(self):
        self.adapter.attach_plan(self.workspace, self.plan, "V001", status="WORKING")
        with self.assertRaises(ValueError):
            self.adapter.promote_validated_version(self.workspace, "V001")

    def test_validated_version_can_be_promoted(self):
        self.adapter.attach_plan(self.workspace, self.plan, "V001", status="VALIDATED")
        self.adapter.promote_validated_version(self.workspace, "V001")
        self.assertEqual(self.workspace.active_version_id, "V001")


if __name__ == "__main__":
    unittest.main()
