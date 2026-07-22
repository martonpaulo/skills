import json
import os
import stat
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from models import DocumentationResult, SourceConfig
from network import HTTPResponse
from providers.docc import DoccProvider
from providers.github_docs import GitHubDocsProvider
from providers.llms_txt import LlmsTxtProvider
from providers.local_cli import LocalCLIProvider
from providers.openapi import OpenAPIProvider


class FakeClient:
    def __init__(self, responses):
        self.responses = responses

    def get(self, url, accepted_types):
        value = self.responses[url]
        if not isinstance(value, bytes):
            value = json.dumps(value).encode()
        return HTTPResponse(200, {"content-type": accepted_types[0]}, value)


def config(provider, source, product="Example", version="1.2.3"):
    return SourceConfig("test", provider, source, product, version)


class ProviderTests(unittest.TestCase):
    def test_normalized_result_validation(self):
        result = DocumentationResult("Example", "Title", "official_documentation", "primary", "https://docs.example.com/a")
        self.assertEqual("Example", result.to_dict()["product"])
        with self.assertRaises(ValueError):
            DocumentationResult("Example", "Title", "docs", "primary", "file:///tmp/a").to_dict()

    def test_llms_txt_parsing(self):
        source = "https://docs.example.com/llms.txt"
        provider = LlmsTxtProvider(
            config("llms_txt", source),
            FakeClient({source: b"# Example\n- [Transactions](https://docs.example.com/tx.md): Transaction behavior\n"}),
        )
        result = provider.search("transaction behavior", version="1.2.3", limit=5)
        self.assertEqual("Transactions", result["matches"][0]["title"])

    def test_github_docs_normalization(self):
        source = "https://github.com/example/docs"
        tree = "https://api.github.com/repos/example/docs/git/trees/v1.2.3?recursive=1"
        provider = GitHubDocsProvider(
            config("github_docs", source),
            FakeClient({tree: {"tree": [{"type": "blob", "path": "guides/transactions.md"}]}}),
        )
        result = provider.search("transactions", version="v1.2.3", limit=5)
        self.assertEqual("official_source_documentation", result["matches"][0]["source_type"])
        self.assertIn("transactions.md", result["matches"][0]["url"])

    def test_openapi_parsing_and_deprecation(self):
        source = "https://api.example.com/openapi.json"
        document = {
            "openapi": "3.1.0", "info": {"title": "Example", "version": "2.0"},
            "paths": {"/items": {"get": {"summary": "List items", "description": "Returns items", "deprecated": True}}},
        }
        provider = OpenAPIProvider(config("openapi", source), FakeClient({source: document}))
        match = provider.search("list items", version=None, limit=5)["matches"][0]
        fetched = provider.fetch(match["url"], sections=None, max_chars=500)
        self.assertEqual("2.0", fetched["resolved_version"])
        self.assertTrue(fetched["deprecated"])

    def test_docc_parsing(self):
        source = "https://docs.example.com/data/index.json"
        document = {"metadata": {"title": "Widget", "platforms": [{"name": "Linux"}]}, "abstract": [{"text": "Widget behavior"}]}
        provider = DoccProvider(config("docc", source), FakeClient({source: document}))
        result = provider.search("widget behavior", version="1.2.3", limit=5)
        self.assertEqual("official_docc_documentation", result["matches"][0]["source_type"])

    def test_local_cli_allowlist_and_command_rejection(self):
        self.assertFalse(LocalCLIProvider.detect("cli://arbitrary-tool"))
        self.assertFalse(LocalCLIProvider.detect("cli://git/status"))
        with tempfile.TemporaryDirectory() as directory:
            executable = Path(directory) / "git"
            executable.write_text("#!/bin/sh\nprintf 'git version 9.9.9\\n'\n", encoding="utf-8")
            executable.chmod(executable.stat().st_mode | stat.S_IXUSR)
            provider = LocalCLIProvider(config("local_cli", "cli://git", product="Git"), {"git": str(executable)})
            result = provider.fetch("cli://git/version", sections=None, max_chars=100)
            self.assertIn("git version 9.9.9", result["content"])
            with self.assertRaises(ValueError):
                provider.fetch("cli://git/status", sections=None, max_chars=100)


if __name__ == "__main__":
    unittest.main()
