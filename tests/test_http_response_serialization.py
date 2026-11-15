import io
import json
import unittest

from runtime.app import Handler
from runtime.contracts import ApprovedChangePlan, ChangeRequest


class HttpResponseSerializationTests(unittest.TestCase):
    def test_json_response_serializes_nested_change_request_dataclass(self):
        handler = Handler.__new__(Handler)
        handler.wfile = io.BytesIO()
        handler.send_response = lambda status: None
        handler.send_header = lambda name, value: None
        handler.end_headers = lambda: None

        approved = ApprovedChangePlan(
            ChangeRequest("FURNITURE", ["F01"], "Move sofa"),
            ["F01"],
            "APPROVED",
        )
        body = {"result": {"approved_change_plan": approved.__dict__}}

        try:
            handler._json(200, body)
        except TypeError as error:
            self.fail(
                "HTTP JSON response must serialize nested dataclass values; "
                f"got {error}"
            )

        decoded = json.loads(handler.wfile.getvalue().decode("utf-8"))
        self.assertEqual(
            decoded["result"]["approved_change_plan"]["request"]["instruction"],
            "Move sofa",
        )
        self.assertEqual(
            decoded["result"]["approved_change_plan"]["approved_target_ids"],
            ["F01"],
        )


if __name__ == "__main__":
    unittest.main()
