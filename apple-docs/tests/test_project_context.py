import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from apis.project_context import AppleProjectContextDetector


class FakeRunner:
    def __call__(self, args, timeout):
        command = tuple(args)
        outputs = {
            ("xcodebuild", "-version"): "Xcode 16.2\nBuild version 16C5032a",
            ("swift", "--version"): "Apple Swift version 6.0.3",
            ("xcodebuild", "-showsdks"): "iOS 18.2 -sdk iphoneos18.2\nmacOS 15.2 -sdk macosx15.2",
        }
        return {"available": True, "returncode": 0, "output": outputs[command]}


class ProjectContextTests(unittest.TestCase):
    def test_detects_targets_packages_entitlements_and_signing(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            project = root / "Demo.xcodeproj"
            project.mkdir()
            (project / "project.pbxproj").write_text(
                "IPHONEOS_DEPLOYMENT_TARGET = 17.0;\n"
                "MACOSX_DEPLOYMENT_TARGET = 14.0;\n"
                "CODE_SIGN_STYLE = Automatic;\nDEVELOPMENT_TEAM = TEAM123;\n",
                encoding="utf-8",
            )
            (root / "Package.resolved").write_text(
                json.dumps({"pins": [{"identity": "swift-log", "state": {"version": "1.6.2"}}]}),
                encoding="utf-8",
            )
            (root / "App.entitlements").write_bytes(
                b'<?xml version="1.0" encoding="UTF-8"?>'
                b'<plist version="1.0"><dict>'
                b'<key>com.apple.security.app-sandbox</key><true/>'
                b'<key>com.apple.developer.networking.wifi-info</key><true/>'
                b'</dict></plist>'
            )

            context = AppleProjectContextDetector(root, FakeRunner()).detect()

            self.assertEqual(["Demo.xcodeproj"], context["projects"])
            self.assertEqual(["17.0"], context["deployment_targets"]["iOS"])
            self.assertEqual(["14.0"], context["deployment_targets"]["macOS"])
            self.assertEqual("1.6.2", context["swift_packages"][0]["version"])
            self.assertTrue(context["app_sandbox"])
            self.assertIn("com.apple.developer.networking.wifi-info", context["capabilities"])
            self.assertEqual(["TEAM123"], context["relevant_build_settings"]["DEVELOPMENT_TEAM"])

    def test_reports_graceful_absence_of_xcode(self):
        def unavailable(args, timeout):
            return {"available": False, "error": "FileNotFoundError"}

        with tempfile.TemporaryDirectory() as directory:
            context = AppleProjectContextDetector(directory, unavailable).detect()
        self.assertIn("Xcode version", context["unknown"])
        self.assertIn("installed SDKs", context["unknown"])

    def test_rejects_path_outside_configured_root(self):
        with tempfile.TemporaryDirectory() as directory:
            detector = AppleProjectContextDetector(directory, FakeRunner())
            with self.assertRaises(ValueError):
                detector.detect("../outside")


if __name__ == "__main__":
    unittest.main()
