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

    def test_rejected_version_is_recorded_but_never_activated(self):
        active = self.adapter.attach_plan(self.workspace, self.plan, "V001", status="WORKING")
        rejected = self.adapter.attach_plan(
            self.workspace, self.plan, "V002", status="REJECTED",
            source_version_id=active.version_id,
        )
        self.assertEqual(rejected.status, "REJECTED")
        self.assertIn(rejected, self.workspace.versions)
        self.assertEqual(self.workspace.active_version_id, "V001")

    def test_rejected_version_does_not_activate_empty_workspace(self):
        self.adapter.attach_plan(self.workspace, self.plan, "V-REJECTED", status="REJECTED")
        self.assertIsNone(self.workspace.active_version_id)

    def test_unknown_version_status_is_rejected_without_mutation(self):
        with self.assertRaisesRegex(ValueError, "PROJECT_VERSION_STATUS_INVALID"):
            self.adapter.attach_plan(self.workspace, self.plan, "V-INVALID", status="INVALID")
        self.assertEqual(self.workspace.versions, [])
        self.assertIsNone(self.workspace.active_version_id)

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
