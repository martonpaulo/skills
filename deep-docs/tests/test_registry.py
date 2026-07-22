import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from registry import DocumentationRegistry


class RegistryTests(unittest.TestCase):
    def test_apple_product_routes_to_apple_docs(self):
        with tempfile.TemporaryDirectory() as directory:
            registry = DocumentationRegistry(directory)
            result = registry.search_docs("View lifecycle", "SwiftUI")
        self.assertEqual("apple-docs", result["route_to"])

    def test_no_source_and_no_network_are_graceful(self):
        with tempfile.TemporaryDirectory() as directory:
            registry = DocumentationRegistry(directory)
            result = registry.search_docs("transactions", "Spring")
        self.assertEqual([], result["matches"])
        self.assertIn("No configured", result["uncertainty"])

    def test_unknown_provider_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            registry = DocumentationRegistry(directory)
            with self.assertRaises(ValueError):
                registry.add_source({"name": "x", "provider": "placeholder", "source": "https://example.com", "product": "X"})


if __name__ == "__main__":
    unittest.main()
