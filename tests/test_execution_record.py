import unittest

from runtime.execution_record import ExecutionRecordStore


class ExecutionRecordStoreTests(unittest.TestCase):
    def setUp(self):
        self.store = ExecutionRecordStore()

    def test_create_and_read_record(self):
        record = self.store.create("EX-001", "PRJ-001", "V001")
        self.assertEqual(record.state, "QUEUED")
        self.assertEqual(self.store.public("EX-001")["input_version_id"], "V001")

    def test_duplicate_execution_id_rejected(self):
        self.store.create("EX-001", "PRJ-001", "V001")
        with self.assertRaisesRegex(ValueError, "DUPLICATE_EXECUTION_ID"):
            self.store.create("EX-001", "PRJ-001", "V002")

    def test_update_preserves_traceability(self):
        self.store.create("EX-001", "PRJ-001", "V001")
        self.store.update("EX-001", "SUCCEEDED", "result://EX-001")
        result = self.store.public("EX-001")
        self.assertEqual(result["state"], "SUCCEEDED")
        self.assertEqual(result["result_reference"], "result://EX-001")
        self.assertEqual(result["project_id"], "PRJ-001")

    def test_missing_record_rejected(self):
        with self.assertRaisesRegex(KeyError, "EXECUTION_RECORD_NOT_FOUND"):
            self.store.get("EX-404")


if __name__ == "__main__":
    unittest.main()
