import sys
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from network import HTTPResponse, SafeHTTPClient


class NetworkSecurityTests(unittest.TestCase):
    def test_rejects_non_https_private_and_unowned_hosts(self):
        public = lambda host: ["93.184.216.34"]
        client = SafeHTTPClient({"docs.example.com"}, resolver=public)
        for url in ("http://docs.example.com/a", "file:///etc/passwd", "https://other.example.com/a"):
            with self.subTest(url=url), self.assertRaises(ValueError):
                client.validate_url(url)
        private = SafeHTTPClient({"docs.example.com"}, resolver=lambda host: ["127.0.0.1"])
        with self.assertRaises(ValueError):
            private.validate_url("https://docs.example.com/a")

    def test_redirect_is_revalidated(self):
        calls = []

        def transport(url, headers, timeout, max_bytes):
            calls.append(url)
            return HTTPResponse(302, {"location": "https://127.0.0.1/private"}, b"")

        client = SafeHTTPClient(
            {"docs.example.com", "127.0.0.1"},
            resolver=lambda host: ["93.184.216.34"] if host == "docs.example.com" else ["127.0.0.1"],
            transport=transport,
        )
        with self.assertRaises(ValueError):
            client.get("https://docs.example.com/start", ("text/plain",))
        self.assertEqual(1, len(calls))

    def test_response_type_and_size_are_checked(self):
        resolver = lambda host: ["93.184.216.34"]
        wrong_type = SafeHTTPClient(
            {"docs.example.com"}, resolver=resolver,
            transport=lambda *args: HTTPResponse(200, {"content-type": "text/html"}, b"ok"),
        )
        with self.assertRaises(ValueError):
            wrong_type.get("https://docs.example.com/docs", ("application/json",))
        oversized = SafeHTTPClient(
            {"docs.example.com"}, resolver=resolver, max_bytes=2,
            transport=lambda *args: HTTPResponse(200, {"content-type": "text/plain"}, b"long"),
        )
        with self.assertRaises(ValueError):
            oversized.get("https://docs.example.com/docs", ("text/plain",))


if __name__ == "__main__":
    unittest.main()
