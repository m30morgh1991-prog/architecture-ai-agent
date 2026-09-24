import unittest
from runtime.accessibility_validation import AccessibilityResult

class AccessibilityValidationTests(unittest.TestCase):
    def test_unknown_does_not_pass(self):
        r=AccessibilityResult("a1","UNKNOWN",True,"e1")
        self.assertFalse(r.passes_gate)

    def test_accessible_passes(self):
        r=AccessibilityResult("a2","ACCESSIBLE",True,"e2")
        self.assertTrue(r.passes_gate)

    def test_missing_evidence_fails_closed(self):
        with self.assertRaises(ValueError):
            AccessibilityResult("a3","ACCESSIBLE",True,"").validate()

if __name__=="__main__":
    unittest.main()
