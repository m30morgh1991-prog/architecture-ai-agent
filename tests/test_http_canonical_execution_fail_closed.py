import io
import json
import unittest

from runtime.app import Handler


class _ResponseSink:
    def __init__(self):
        self.status = None
        self.headers = {}
        self.wfile = io.BytesIO()

    def send_response(self, status):
        self.status = status

    def send_header(self, name, value):
        self.headers[name] = value

    def end_headers(self):
        pass

    def _json(self, status, body):
        return Handler._json(self, status, body)


class HttpCanonicalExecutionFailClosedTests(unittest.TestCase):
    def test_execute_endpoint_blocks_before_reading_untrusted_payload(self):
        sink = _ResponseSink()
        sink.path = "/v1/execute"
        sink.headers_in = {}
        sink.headers = {}
        # A forged payload claims that a structural column is editable.
        sink.rfile = io.BytesIO(json.dumps({
            "execution_id": "forged-1",
            "project_id": "p1",
            "input_version_id": "v1",
            "plan_id": "client-plan",
            "elements": [{
                "element_id": "column-1",
                "element_type": "COLUMN",
                "state": "EDITABLE",
                "geometry": {"x": 0, "y": 0},
            }],
            "request": {
                "change_type": "FURNITURE",
                "target_ids": ["column-1"],
                "instruction": "move",
            },
        }).encode())

        # The handler must reject before parsing or trusting the body.
        Handler.do_POST(sink)

        self.assertEqual(sink.status, 503)
        payload = json.loads(sink.wfile.getvalue().decode())
        self.assertEqual(payload["status"], "BLOCKED")
        self.assertEqual(payload["error"], "CANONICAL_EXECUTION_NOT_CONFIGURED")

    def test_execution_server_uses_https_and_is_bound_to_loopback(self):
        import inspect
        from runtime import app

        source = inspect.getsource(app.main)
        self.assertIn('("127.0.0.1", 8443)', source)
        self.assertIn("ssl.PROTOCOL_TLS_SERVER", source)
        self.assertIn("wrap_socket", source)
        self.assertNotIn('("0.0.0.0", 8443)', source)
        self.assertNotIn('("127.0.0.1", 8000)', source)


if __name__ == "__main__":
    unittest.main()
