import unittest
from runtime.e2e_runtime import E2ERuntimeBoundary


class FakeVisual:
    def render(self,*args,**kwargs): return "candidate"


class FakeBoundary:
    def render(self,*args,**kwargs): return "candidate"


class H42H45E2ETests(unittest.TestCase):
    def test_unapproved_plan_fails_closed(self):
        e2e=E2ERuntimeBoundary(FakeBoundary(), lambda p,r: {"status":"PASS"})
        result=e2e.run("e1",{},None,{"status":"REJECT"}, {})
        self.assertEqual(result.execution["status"],"REJECT")
        self.assertIn("APPROVED_CHANGE_PLAN_REQUIRED", result.execution["failure_codes"])

    def test_post_edit_failure_blocks_release(self):
        e2e=E2ERuntimeBoundary(
            FakeBoundary(),
            lambda p,r: {
                "status":"PASS",
                "post_edit_diff":{"locked_delta_ids":["C01"],"unauthorized_delta_ids":[]},
            },
        )
        result=e2e.run("e2",{},None,{"status":"APPROVED"}, {})
        self.assertEqual(result.final_validation.status,"REJECT")
        self.assertEqual(result.release.status,"BLOCKED")
        self.assertEqual(result.execution["status"],"REJECT")


if __name__ == "__main__":
    unittest.main()
