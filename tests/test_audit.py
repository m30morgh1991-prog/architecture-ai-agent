import unittest
from runtime.audit import AuditTrail
class AuditTests(unittest.TestCase):
 def test_trace_is_ordered_and_scoped(self):
  a=AuditTrail(); a.record("e1","EXECUTE","PASS"); a.record("e2","EXECUTE","PASS"); a.record("e1","FINAL_VALIDATE","PASS")
  self.assertEqual([x.stage for x in a.events("e1")],["EXECUTE","FINAL_VALIDATE"])
if __name__=="__main__": unittest.main()
