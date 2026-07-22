import sys
import time
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from sandbox import SandboxExecutor
from security import CodeValidator


class SecurityAndSandboxTests(unittest.TestCase):
    def test_ast_rejects_imports_builtins_dunders_and_missing_result(self):
        cases = (
            "import socket\nresult = 1",
            "result = open('/etc/passwd')",
            "result = eval('1')",
            "result = (1).__class__",
            "value = 1",
        )
        for code in cases:
            with self.subTest(code=code):
                self.assertFalse(CodeValidator().validate(code).is_safe)

    def test_registered_api_executes_and_arbitrary_api_is_rejected(self):
        executor = SandboxExecutor(api_handlers={"search_docs": lambda query, limit=10: {"query": query, "limit": limit}})
        ok = executor.execute("result = search_docs('transactions', limit=3)")
        self.assertTrue(ok.success, ok.error)
        self.assertEqual({"query": "transactions", "limit": 3}, ok.result)
        bad = executor.execute("result = arbitrary_command('whoami')")
        self.assertFalse(bad.success)

    def test_output_cap(self):
        result = SandboxExecutor(max_output_bytes=1024).execute("result = 'x' * 5000")
        self.assertFalse(result.success)
        self.assertIn("exceeds", result.error)

    def test_timeout(self):
        started = time.monotonic()
        result = SandboxExecutor(timeout=1).execute("while True:\n    pass\nresult = None")
        self.assertFalse(result.success)
        self.assertLess(time.monotonic() - started, 4)


if __name__ == "__main__":
    unittest.main()
