import sys
import time
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from sandbox import SandboxExecutor
from security import CodeValidator


class SecurityTests(unittest.TestCase):
    def test_requires_result(self):
        outcome = CodeValidator().validate("value = 1")
        self.assertFalse(outcome.is_safe)
        self.assertIn("result", " ".join(outcome.errors))

    def test_rejects_imports_and_sensitive_builtins(self):
        for code in (
            "import os\nresult = 1",
            "result = open('secret')",
            "result = getattr([], '__class__')",
            "result = (1).__class__",
        ):
            with self.subTest(code=code):
                self.assertFalse(CodeValidator().validate(code).is_safe)

    def test_executes_registered_api_and_serializes_result(self):
        executor = SandboxExecutor(api_handlers={"lookup": lambda value, limit=1: {"value": value, "limit": limit}})
        result = executor.execute("result = lookup('ok', limit=2)")
        self.assertTrue(result.success, result.error)
        self.assertEqual({"value": "ok", "limit": 2}, result.result)
        self.assertEqual(1, result.api_calls_made)

    def test_output_limit_is_enforced(self):
        executor = SandboxExecutor(max_output_bytes=1024)
        result = executor.execute("result = 'x' * 5000")
        self.assertFalse(result.success)
        self.assertIn("exceeds", result.error)

    def test_timeout_is_enforced(self):
        executor = SandboxExecutor(timeout=1)
        started = time.monotonic()
        result = executor.execute("while True:\n    pass\nresult = None")
        self.assertFalse(result.success)
        self.assertIn(result.error_type, {"TimeoutError", "ProcessError"})
        self.assertLess(time.monotonic() - started, 4)


if __name__ == "__main__":
    unittest.main()
