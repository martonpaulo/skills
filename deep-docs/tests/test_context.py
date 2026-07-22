import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from context import ProjectContextDetector, version_kind


class ContextTests(unittest.TestCase):
    def test_exact_and_ranged_versions_are_distinct(self):
        self.assertEqual("exact", version_kind("6.2.3"))
        self.assertEqual("range", version_kind("^6.2.0"))
        self.assertEqual("range", version_kind(">=1.0,<2"))
        self.assertEqual("unresolved", version_kind(None))

    def test_package_lock_takes_precedence_over_declared_range(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "package.json").write_text(json.dumps({"dependencies": {"react": "^19.0.0"}}), encoding="utf-8")
            (root / "package-lock.json").write_text(
                json.dumps({"packages": {"node_modules/react": {"version": "19.1.1"}}}), encoding="utf-8"
            )
            detector = ProjectContextDetector(root)
            resolved = detector.resolve_product("react")
        self.assertEqual("^19.0.0", resolved["declared_version"])
        self.assertEqual("range", resolved["declared_version_kind"])
        self.assertEqual("19.1.1", resolved["locked_version"])
        self.assertEqual("19.1.1", resolved["resolved_version"])
        self.assertEqual("locked", resolved["status"])

    def test_apple_project_routes_to_apple_docs(self):
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / "Demo.xcodeproj").mkdir()
            result = ProjectContextDetector(directory).resolve_product("SwiftUI")
        self.assertEqual("apple-docs", result["route_to"])

    def test_unknown_context_is_graceful(self):
        with tempfile.TemporaryDirectory() as directory:
            detector = ProjectContextDetector(directory)
            context = detector.detect()
            product = detector.resolve_product("missing")
        self.assertIn("No supported project manifest", context["uncertainty"][0])
        self.assertEqual("unknown_version", product["status"])


if __name__ == "__main__":
    unittest.main()
