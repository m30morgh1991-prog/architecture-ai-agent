import unittest
from runtime.decision_trace import DecisionTrace

class DecisionTraceTests(unittest.TestCase):
    def test_trace_is_audit_ready(self):
        t=DecisionTrace("d1","e1","CONTROLLED_EDIT","APPROVED",["rule-1"],["validated"])
        event=t.as_audit_event()
        self.assertEqual(event["execution_id"],"e1")
        self.assertEqual(event["outcome"],"APPROVED")

    def test_missing_traceability_fails(self):
        with self.assertRaises(ValueError):
            DecisionTrace("","","APPROVED").validate()

if __name__=="__main__":
    unittest.main()
