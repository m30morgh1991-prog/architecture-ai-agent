import unittest
from runtime.idempotency import IdempotencyGuard
class IdempotencyTests(unittest.TestCase):
 def test_duplicate_returns_original(self):
  g=IdempotencyGuard(); r=g.store("k",{"status":"PASS"}); self.assertIs(g.store("k",{"status":"OTHER"}),r)
if __name__=="__main__": unittest.main()
