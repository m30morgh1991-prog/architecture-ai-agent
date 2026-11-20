import json
import shutil
import ssl
import subprocess
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from http.server import HTTPServer
from pathlib import Path
from unittest.mock import patch

from runtime import app as runtime_app
from runtime.app import Handler, build_tls_context


TOKEN = "integration-test-token-" + ("z" * 40)


class LiveHttpsVerificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        openssl = shutil.which("openssl")
        if not openssl:
            raise unittest.SkipTest("openssl is required for the live TLS integration test")

        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.cert_file = str(Path(cls.temp_dir.name) / "runtime.crt")
        cls.key_file = str(Path(cls.temp_dir.name) / "runtime.key")
        subprocess.run(
            [
                openssl, "req", "-x509", "-newkey", "rsa:2048", "-nodes",
                "-keyout", cls.key_file,
                "-out", cls.cert_file,
                "-days", "1",
                "-subj", "/CN=127.0.0.1",
                "-addext", "subjectAltName=IP:127.0.0.1",
            ],
            check=True,
            capture_output=True,
            text=True,
        )

        cls.previous_token = Handler.api_token
        Handler.api_token = TOKEN
        context = build_tls_context(cls.cert_file, cls.key_file)
        cls.server = HTTPServer(("127.0.0.1", 0), Handler)
        cls.server.socket = context.wrap_socket(cls.server.socket, server_side=True)
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, "server"):
            cls.server.shutdown()
            cls.server.server_close()
            cls.thread.join(timeout=5)
        if hasattr(cls, "previous_token"):
            Handler.api_token = cls.previous_token
        if hasattr(cls, "temp_dir"):
            cls.temp_dir.cleanup()

    def test_trusted_client_verifies_certificate_and_hostname(self):
        context = ssl.create_default_context(cafile=self.cert_file)
        request = urllib.request.Request(
            f"https://127.0.0.1:{self.port}/v1/executions/not-found",
            headers={"Authorization": f"Bearer {TOKEN}"},
        )
        with self.assertRaises(urllib.error.HTTPError) as caught:
            urllib.request.urlopen(request, context=context, timeout=5)
        # 404 proves the TLS handshake, certificate-chain/IP-SAN verification,
        # and bearer authentication all succeeded before the read-only lookup.
        self.assertEqual(caught.exception.code, 404)
        self.assertEqual(
            json.loads(caught.exception.read().decode())["error"],
            "EXECUTION_RECORD_NOT_FOUND",
        )

    def test_untrusted_certificate_is_rejected_by_client(self):
        context = ssl.create_default_context()
        request = urllib.request.Request(
            f"https://127.0.0.1:{self.port}/v1/executions/not-found",
            headers={"Authorization": f"Bearer {TOKEN}"},
        )
        with self.assertRaises(urllib.error.URLError) as caught:
            urllib.request.urlopen(request, context=context, timeout=5)
        self.assertIsInstance(caught.exception.reason, ssl.SSLCertVerificationError)

    def test_tls_connection_without_bearer_token_is_unauthorized(self):
        context = ssl.create_default_context(cafile=self.cert_file)
        request = urllib.request.Request(
            f"https://127.0.0.1:{self.port}/v1/executions/not-found"
        )
        with self.assertRaises(urllib.error.HTTPError) as caught:
            urllib.request.urlopen(request, context=context, timeout=5)
        self.assertEqual(caught.exception.code, 401)
        self.assertEqual(
            json.loads(caught.exception.read().decode())["error"],
            "AUTHENTICATION_REQUIRED",
        )


if __name__ == "__main__":
    unittest.main()
