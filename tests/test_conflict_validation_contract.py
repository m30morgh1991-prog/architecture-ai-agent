import unittest

from runtime.conflict_validation_contract import Conflict, ValidationResult


class ConflictValidationContractTests(unittest.TestCase):
    def test_blocking_conflict_cannot_be_reported_as_pass(self):
        c = Conflict("c1", "LOCKED_ELEMENT_CONFLICT", "BLOCKING", ["C01"])
        v = ValidationResult("v1", "PASS", [c], ["e1"])
        with self.assertRaisesRegex(ValueError, "VALIDATION_PASS_HAS_BLOCKING_CONFLICT"):
            v.validate()

    def test_pass_requires_evidence_ids(self):
        v = ValidationResult("v-no-evidence", "PASS", [], [])
        with self.assertRaisesRegex(ValueError, "VALIDATION_PASS_EVIDENCE_MISSING"):
            v.validate()

    def test_clean_pass_is_executable(self):
        v = ValidationResult("v2", "PASS", [], ["e2"])
        self.assertTrue(v.executable)

    def test_unknown_is_not_executable(self):
        v = ValidationResult("v3", "UNKNOWN", [], [])
        self.assertFalse(v.executable)

    def test_invalid_conflict_severity_is_rejected(self):
        with self.assertRaises(ValueError):
            ValidationResult("v4", "PASS", [Conflict("c", "X", "INVALID")]).validate()


if __name__ == "__main__":
    unittest.main()
