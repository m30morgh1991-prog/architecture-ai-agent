import json
import unittest
from email.message import Message
from unittest.mock import patch

from runtime import app as runtime_app
from runtime.app import Handler


VALID_BODY = {
    "execution_id": "request-guard-test",
    "project_id": "project-1",
    "input_version_id": "version-1",
    "plan_id": "plan-1",
    "elements": [],
    "request": {
        "change_type": "FURNITURE",
        "target_ids": ["MISSING"],
        "instruction": "Move missing sofa",
    },
}


class TrackingReader:
    def __init__(self, payload):
        self.payload = payload
        self.read_called = False

    def read(self, length):
        self.read_called = True
        return self.payload


class HttpRequestGuardrailTests(unittest.TestCase):
    def _handler(self, payload, *, content_type="application/json", content_length=None):
        raw = payload if isinstance(payload, bytes) else json.dumps(payload).encode("utf-8")
        headers = Message()
        if content_type is not None:
            headers["Content-Type"] = content_type
        if content_length is not None:
            headers["Content-Length"] = str(content_length)
        elif raw is not None:
            headers["Content-Length"] = str(len(raw))

        handler = Handler.__new__(Handler)
        handler.path = "/v1/execute"
        handler.headers = headers
        handler.rfile = TrackingReader(raw)
        handler._json = lambda status, body: (status, body)
        handler.send_error = lambda status, *args, **kwargs: (status, {"error": "HTTP_ERROR"})
        return handler

    def _invoke(self, handler):
        try:
            return handler.do_POST()
        except Exception as error:
            self.fail(f"request handler must return a structured 4xx response, not raise: {error}")

    def test_missing_content_length_returns_411_without_reading_body(self):
        handler = self._handler(VALID_BODY, content_length=None)
        del handler.headers["Content-Length"]
        status, body = self._invoke(handler)
        self.assertEqual(status, 411)
        self.assertEqual(body["error"], "CONTENT_LENGTH_REQUIRED")
        self.assertFalse(handler.rfile.read_called)

    def test_invalid_content_length_returns_400_without_reading_body(self):
        handler = self._handler(VALID_BODY, content_length="invalid")
        status, body = self._invoke(handler)
        self.assertEqual(status, 400)
        self.assertEqual(body["error"], "CONTENT_LENGTH_INVALID")
        self.assertFalse(handler.rfile.read_called)

    def test_oversized_body_returns_413_before_reading(self):
        maximum = getattr(runtime_app, "MAX_REQUEST_BODY_BYTES", 16 * 1024 * 1024)
        handler = self._handler(
            VALID_BODY,
            content_length=maximum + 1,
        )
        status, body = self._invoke(handler)
        self.assertEqual(status, 413)
        self.assertEqual(body["error"], "REQUEST_BODY_TOO_LARGE")
        self.assertFalse(handler.rfile.read_called)

    def test_non_json_content_type_returns_415(self):
        handler = self._handler(VALID_BODY, content_type="text/plain")
        status, body = self._invoke(handler)
        self.assertEqual(status, 415)
        self.assertEqual(body["error"], "CONTENT_TYPE_UNSUPPORTED")
        self.assertFalse(handler.rfile.read_called)

    def test_malformed_json_returns_400(self):
        handler = self._handler(b"{not-json")
        status, body = self._invoke(handler)
        self.assertEqual(status, 400)
        self.assertEqual(body["error"], "JSON_BODY_INVALID")

    def test_top_level_array_and_missing_fields_are_rejected(self):
        array_handler = self._handler([1, 2, 3])
        status, body = self._invoke(array_handler)
        self.assertEqual(status, 400)
        self.assertEqual(body["error"], "REQUEST_SCHEMA_INVALID")

        missing_handler = self._handler({})
        status, body = self._invoke(missing_handler)
        self.assertEqual(status, 400)
        self.assertEqual(body["error"], "REQUEST_SCHEMA_INVALID")

    def test_unknown_element_state_is_rejected_before_execution(self):
        payload = dict(VALID_BODY)
        payload["elements"] = [{
            "element_id": "W1",
            "element_type": "WALL",
            "state": "UNKNOWN",
            "geometry": {},
        }]
        payload["request"] = {
            "change_type": "FURNITURE",
            "target_ids": ["W1"],
            "instruction": "Move",
        }
        handler = self._handler(payload)
        status, body = self._invoke(handler)
        self.assertEqual(status, 400)
        self.assertEqual(body["error"], "REQUEST_SCHEMA_INVALID")

    def test_runtime_binds_to_loopback_by_default(self):
        with patch.object(runtime_app, "HTTPServer") as server_class:
            runtime_app.main()
        server_class.assert_called_once_with(("127.0.0.1", 8000), runtime_app.Handler)
        server_class.return_value.serve_forever.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
