import unittest
from unittest.mock import patch

from runtime import app as runtime_app
from runtime.app import Handler, validate_execution_payload


VALID_BODY = {
    "execution_id": "request-guard-test",
    "project_id": "project-1",
    "input_version_id": "version-1",
    "plan_id": "plan-1",
    "elements": [],
    "request": {
        "change_type": "FURNITURE",
        "target_ids": ["F01"],
        "instruction": "Move sofa",
    },
}


class TrackingReader:
    def __init__(self):
        self.read_called = False

    def read(self, length):
        self.read_called = True
        return b"{}"


class HttpRequestGuardrailTests(unittest.TestCase):
    def test_valid_payload_passes_schema_validation(self):
        self.assertIsNone(validate_execution_payload(VALID_BODY))

    def test_non_object_payload_is_rejected(self):
        self.assertEqual(validate_execution_payload([]), "REQUEST_SCHEMA_INVALID")

    def test_duplicate_element_ids_are_rejected(self):
        payload = dict(VALID_BODY)
        payload["elements"] = [
            {"element_id": "F01", "element_type": "FURNITURE", "state": "EDITABLE"},
            {"element_id": "F01", "element_type": "FURNITURE", "state": "EDITABLE"},
        ]
        self.assertEqual(validate_execution_payload(payload), "REQUEST_SCHEMA_INVALID")

    def test_unknown_element_state_is_rejected(self):
        payload = dict(VALID_BODY)
        payload["elements"] = [
            {"element_id": "W1", "element_type": "WALL", "state": "UNKNOWN"}
        ]
        payload["request"] = {
            "change_type": "FURNITURE",
            "target_ids": ["W1"],
            "instruction": "Move",
        }
        self.assertEqual(validate_execution_payload(payload), "REQUEST_SCHEMA_INVALID")

    def test_duplicate_target_ids_are_rejected(self):
        payload = dict(VALID_BODY)
        payload["request"] = {
            "change_type": "FURNITURE",
            "target_ids": ["F01", "F01"],
            "instruction": "Move",
        }
        self.assertEqual(validate_execution_payload(payload), "REQUEST_SCHEMA_INVALID")

    def test_missing_required_fields_are_rejected(self):
        self.assertEqual(validate_execution_payload({}), "REQUEST_SCHEMA_INVALID")

    def test_blocked_http_endpoint_returns_before_reading_request_body(self):
        handler = Handler.__new__(Handler)
        handler.path = "/v1/execute"
        handler.rfile = TrackingReader()
        handler._json = lambda status, body: (status, body)
        handler.send_error = lambda status, *args, **kwargs: (status, {"error": "HTTP_ERROR"})
        status, body = handler.do_POST()
        self.assertEqual(status, 503)
        self.assertEqual(body["status"], "BLOCKED")
        self.assertEqual(body["error"], "CANONICAL_EXECUTION_NOT_CONFIGURED")
        self.assertFalse(handler.rfile.read_called)

    def test_runtime_requires_tls_and_binds_https_to_loopback(self):
        env = {
            "ARCH_AGENT_TLS_CERT_FILE": "/secure/runtime.crt",
            "ARCH_AGENT_TLS_KEY_FILE": "/secure/runtime.key",
            "ARCH_AGENT_API_TOKEN": "x" * 48,
        }
        with patch.dict("os.environ", env, clear=True):
            with patch.object(runtime_app, "HTTPServer") as server_class:
                with patch.object(runtime_app.ssl, "SSLContext") as context_class:
                    context = context_class.return_value
                    context.wrap_socket.return_value = object()
                    runtime_app.main()

        server_class.assert_called_once_with(("127.0.0.1", 8443), runtime_app.Handler)
        context_class.assert_called_once_with(runtime_app.ssl.PROTOCOL_TLS_SERVER)
        self.assertEqual(context.minimum_version, runtime_app.ssl.TLSVersion.TLSv1_2)
        context.load_cert_chain.assert_called_once_with(
            certfile="/secure/runtime.crt", keyfile="/secure/runtime.key"
        )
        context.wrap_socket.assert_called_once_with(
            server_class.return_value.socket, server_side=True
        )
        server_class.return_value.serve_forever.assert_called_once_with()
        server_class.return_value.server_close.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
