import unittest
from runtime.error_policy import classify
class ErrorPolicyTests(unittest.TestCase):
 def test_blocking(self): self.assertEqual(classify("LOCKED_ELEMENT_CONFLICT"),"BLOCKING")
 def test_nonblocking(self): self.assertEqual(classify("TARGET_NOT_FOUND"),"NON_BLOCKING")
if __name__=="__main__": unittest.main()
