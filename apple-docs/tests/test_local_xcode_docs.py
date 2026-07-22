import plistlib
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from apis.local_xcode_docs import LocalXcodeDocumentation, _DOC_RELATIVE


def create_xcode(root: Path, name: str, version: str, document: str, content: str) -> None:
    app = root / name
    docs = app / _DOC_RELATIVE
    docs.mkdir(parents=True)
    with (app / "Contents/Info.plist").open("wb") as handle:
        plistlib.dump({"CFBundleShortVersionString": version}, handle)
    (docs / f"{document}.md").write_text(content, encoding="utf-8")


class LocalXcodeDocumentationTests(unittest.TestCase):
    def test_discovers_multiple_versions_and_returns_version_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_xcode(root, "Xcode.app", "16.2", "Concurrency", "Structured concurrency guidance")
            create_xcode(root, "Xcode-16.3.app", "16.3", "Concurrency", "Updated concurrency guidance")
            docs = LocalXcodeDocumentation([root])
            sources = docs.list_sources()
            self.assertEqual(["16.3", "16.2"], [item["xcode_version"] for item in sources])
            result = docs.search("structured", "16.2")
            self.assertEqual("16.2", result["matches"][0]["xcode_version"])
            self.assertFalse(result["matches"][0]["public_api_contract"])

    def test_rejects_traversal_and_caps_output(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_xcode(root, "Xcode.app", "16.2", "Large", "x" * 500)
            docs = LocalXcodeDocumentation([root])
            with self.assertRaises(ValueError):
                docs.fetch("../Large")
            result = docs.fetch("Large", "16.2", max_chars=80)
            self.assertEqual(80, len(result["content"]))
            self.assertTrue(result["truncated"])

    def test_missing_xcode_is_graceful(self):
        with tempfile.TemporaryDirectory() as directory:
            docs = LocalXcodeDocumentation([Path(directory) / "missing"])
            self.assertEqual([], docs.list_sources())
            self.assertEqual([], docs.search("anything")["matches"])


if __name__ == "__main__":
    unittest.main()
