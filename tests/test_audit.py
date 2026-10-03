import unittest
from runtime.audit import AuditTrail

class AuditTests(unittest.TestCase):
    def test_trace_is_ordered_and_scoped(self):
        a=AuditTrail(); a.record("e1","EXECUTE","PASS"); a.record("e2","EXECUTE","PASS"); a.record("e1","FINAL_VALIDATE","PASS")
        self.assertEqual([x.stage for x in a.events("e1")],["EXECUTE","FINAL_VALIDATE"])

    def test_workflow_started_is_a_valid_lifecycle_marker(self):
        a=AuditTrail()
        event = a.record("e1", "WORKFLOW", "STARTED", {"idempotency_key": "k1"})
        self.assertEqual(event.status, "STARTED")
        self.assertFalse(a.is_complete("e1", ("WORKFLOW",)))

    def test_incomplete_or_non_pass_evidence_is_not_complete(self):
        a=AuditTrail()
        a.record("e1","EXECUTE","PASS")
        self.assertFalse(a.is_complete("e1", ("EXECUTE","POST_EDIT_DIFF")))
        a.record("e1","POST_EDIT_DIFF","BLOCKED")
        self.assertFalse(a.is_complete("e1", ("EXECUTE","POST_EDIT_DIFF")))

    def test_complete_requires_all_required_stages_to_pass(self):
        a=AuditTrail()
        a.record("e1","EXECUTE","PASS")
        a.record("e1","POST_EDIT_DIFF","PASS")
        self.assertTrue(a.is_complete("e1", ("EXECUTE","POST_EDIT_DIFF")))

if __name__=="__main__":
    unittest.main()
