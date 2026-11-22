import unittest
from runtime.error_policy import classify


class ErrorPolicyTests(unittest.TestCase):
    def test_blocking(self):
        self.assertEqual(classify("LOCKED_ELEMENT_CONFLICT"), "BLOCKING")

    def test_nonblocking(self):
        self.assertEqual(classify("TARGET_NOT_FOUND"), "NON_BLOCKING")

    def test_unknown_error_codes_are_blocking(self):
        self.assertEqual(classify("UNRECOGNIZED_CODE"), "BLOCKING")

    def test_locked_conflict_suffix_is_blocking(self):
        self.assertEqual(classify("LOCKED_ELEMENT_CONFLICT:wall-12"), "BLOCKING")

    def test_unknown_empty_and_malformed_codes_are_blocking(self):
        for code in ("", None, "TARGET_NOT_FOUND:unexpected", "UNKNOWN"):
            with self.subTest(code=code):
                self.assertEqual(classify(code), "BLOCKING")


if __name__ == "__main__":
    unittest.main()
