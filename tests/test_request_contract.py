import unittest
from runtime.request_contract import ExecutionRequest


class ExecutionRequestTests(unittest.TestCase):
    def test_valid_request_preserves_traceability(self):
        req = ExecutionRequest.from_dict({
            "execution_id": "E19", "project_id": "P19", "input_version_id": "V19",
            "plan_id": "PLAN19", "request": {"change_type": "FURNITURE"}
        })
        self.assertEqual(req.trace()["input_version_id"], "V19")

    def test_missing_field_rejected(self):
        with self.assertRaisesRegex(ValueError, "REQUEST_FIELD_MISSING:plan_id"):
            ExecutionRequest.from_dict({
                "execution_id": "E19", "project_id": "P19", "input_version_id": "V19",
                "request": {}
            })

    def test_invalid_ids_rejected(self):
        with self.assertRaisesRegex(ValueError, "REQUEST_ID_INVALID"):
            ExecutionRequest.from_dict({
                "execution_id": "", "project_id": "P19", "input_version_id": "V19",
                "plan_id": "PLAN19", "request": {}
            })


if __name__ == "__main__":
    unittest.main()
