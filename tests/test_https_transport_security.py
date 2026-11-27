import os
import unittest
from email.message import Message
from unittest.mock import patch

from runtime import app as runtime_app
from runtime.app import Handler, load_runtime_security_config


TOKEN = "t" * 48


class HttpsTransportSecurityTests(unittest.TestCase):
    def test_startup_requires_certificate_and_private_key(self):
        with self.assertRaisesRegex(RuntimeError, "TLS_CONFIGURATION_REQUIRED"):
            load_runtime_security_config({})

    def test_startup_rejects_missing_or_weak_bearer_token(self):
        env = {
            "ARCH_AGENT_TLS_CERT_FILE": "/secure/runtime.crt",
            "ARCH_AGENT_TLS_KEY_FILE": "/secure/runtime.key",
        }
        with self.assertRaisesRegex(RuntimeError, "AUTHENTICATION_CONFIGURATION_INVALID"):
            load_runtime_security_config(env)

        env["ARCH_AGENT_API_TOKEN"] = "short"
        with self.assertRaisesRegex(RuntimeError, "AUTHENTICATION_CONFIGURATION_INVALID"):
            load_runtime_security_config(env)

    def test_security_configuration_accepts_explicit_tls_and_strong_token(self):
        env = {
            "ARCH_AGENT_TLS_CERT_FILE": "/secure/runtime.crt",
            "ARCH_AGENT_TLS_KEY_FILE": "/secure/runtime.key",
            "ARCH_AGENT_API_TOKEN": TOKEN,
        }
        self.assertEqual(
            load_runtime_security_config(env),
            ("/secure/runtime.crt", "/secure/runtime.key", TOKEN),
        )

    def _handler(self, authorization_values=()):
        handler = Handler.__new__(Handler)
        handler.path = "/v1/executions/E1"
        handler.headers = Message()
        for value in authorization_values:
            handler.headers.add_header("Authorization", value)
        handler._json = lambda status, body: (status, body)
        handler.send_error = lambda status, *args, **kwargs: (status, {"error": "HTTP_ERROR"})
        return handler

    def test_execution_read_requires_bearer_authentication(self):
        handler = self._handler()
        with patch.object(Handler, "api_token", TOKEN):
            status, body = handler.do_GET()
        self.assertEqual(status, 401)
        self.assertEqual(body["error"], "AUTHENTICATION_REQUIRED")

    def test_duplicate_authorization_headers_are_rejected(self):
        handler = self._handler((f"Bearer {TOKEN}", f"Bearer {TOKEN}"))
        with patch.object(Handler, "api_token", TOKEN):
            status, body = handler.do_GET()
        self.assertEqual(status, 401)
        self.assertEqual(body["error"], "AUTHENTICATION_REQUIRED")

    def test_valid_bearer_token_allows_read_only_execution_lookup(self):
        handler = self._handler((f"Bearer {TOKEN}",))
        with patch.object(Handler, "api_token", TOKEN):
            with patch.object(runtime_app.execution_records, "public", return_value={"state": "SUCCEEDED"}):
                status, body = handler.do_GET()
        self.assertEqual(status, 200)
        self.assertEqual(body, {"state": "SUCCEEDED"})

    def test_missing_tls_configuration_prevents_server_start(self):
        with patch.dict(os.environ, {}, clear=True):
            with patch.object(runtime_app, "BoundedThreadingHTTPServer") as server_class:
                with self.assertRaisesRegex(RuntimeError, "TLS_CONFIGURATION_REQUIRED"):
                    runtime_app.main()
        server_class.assert_not_called()


if __name__ == "__main__":
    unittest.main()
