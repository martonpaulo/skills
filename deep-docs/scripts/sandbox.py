"""Subprocess sandbox exposing only normalized documentation APIs."""

from __future__ import annotations

import base64
import json
import os
import selectors
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from typing import Any, Callable

from security import CodeValidator


@dataclass
class ExecutionResult:
    success: bool
    result: Any = None
    stdout: str = ""
    stderr: str = ""
    error: str | None = None
    error_type: str | None = None
    execution_time_ms: int = 0
    api_calls_made: int = 0

    def to_dict(self) -> dict:
        return {key: value for key, value in vars(self).items() if value not in (None, "")}


class SandboxExecutor:
    """Use AST checks plus process, namespace, time, memory, and output boundaries."""

    TEMPLATE = r'''
import base64
import json
import resource
import sys

try:
    resource.setrlimit(resource.RLIMIT_CPU, ({timeout}, {timeout}))
    memory = {memory_mb} * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (memory, memory))
    resource.setrlimit(resource.RLIMIT_FSIZE, ({output_bytes}, {output_bytes}))
except (AttributeError, ValueError, resource.error):
    pass

ALLOWED_BUILTINS = {{
    "abs": abs, "all": all, "any": any, "bool": bool, "dict": dict,
    "enumerate": enumerate, "Exception": Exception, "filter": filter,
    "float": float, "IndexError": IndexError, "int": int, "isinstance": isinstance,
    "KeyError": KeyError, "len": len, "list": list, "map": map, "max": max,
    "min": min, "next": next, "None": None, "pow": pow, "range": range,
    "repr": repr, "reversed": reversed, "round": round, "RuntimeError": RuntimeError,
    "set": set, "sorted": sorted, "str": str, "sum": sum, "True": True,
    "False": False, "tuple": tuple, "TypeError": TypeError, "ValueError": ValueError,
    "ZeroDivisionError": ZeroDivisionError, "zip": zip,
}}

def _call(name, *args, **kwargs):
    sys.stdout.write(json.dumps({{"__api_call__": {{"name": name, "args": list(args), "kwargs": kwargs}}}}) + "\n")
    sys.stdout.flush()
    response = json.loads(sys.stdin.readline())
    if "error" in response:
        raise RuntimeError(response["error"])
    return response.get("result")

namespace = {{"__builtins__": ALLOWED_BUILTINS}}
for api_name in {api_names}:
    namespace[api_name] = (lambda name: lambda *args, **kwargs: _call(name, *args, **kwargs))(api_name)
printed = []
def _print(*args, **kwargs):
    unsupported = set(kwargs) - {{"sep", "end"}}
    if unsupported:
        raise TypeError("Only sep and end are supported by print")
    printed.append(kwargs.get("sep", " ").join(str(value) for value in args) + kwargs.get("end", "\n"))
namespace["print"] = _print

try:
    code = base64.b64decode({encoded_code!r}).decode("utf-8")
    exec(compile(code, "<documentation-query>", "exec"), namespace, namespace)
    encoded = json.dumps({{"success": True, "result": namespace["result"], "stdout": "".join(printed)}}, ensure_ascii=False)
    if len(encoded.encode("utf-8")) > {output_bytes}:
        raise ValueError("Sandbox output exceeds {output_bytes} bytes")
except Exception as exc:
    encoded = json.dumps({{"success": False, "error": str(exc), "error_type": type(exc).__name__}})
sys.stdout.write("__SANDBOX_COMPLETE__\n" + encoded + "\n")
sys.stdout.flush()
'''

    def __init__(self, *, timeout: int = 10, max_memory_mb: int = 64, max_output_bytes: int = 100_000, api_handlers: dict[str, Callable] | None = None):
        self.timeout = max(1, min(int(timeout), 60))
        self.max_memory_mb = max(32, min(int(max_memory_mb), 512))
        self.max_output_bytes = max(1_024, min(int(max_output_bytes), 1_000_000))
        self.api_handlers = api_handlers or {}
        self.validator = CodeValidator()

    def execute(self, code: str) -> ExecutionResult:
        started = time.monotonic()
        validation = self.validator.validate(code)
        if not validation.is_safe:
            return ExecutionResult(False, error="; ".join(validation.errors), error_type="ValidationError")
        encoded = base64.b64encode(code.encode()).decode()
        script = self.TEMPLATE.format(
            timeout=self.timeout,
            memory_mb=self.max_memory_mb,
            output_bytes=self.max_output_bytes,
            api_names=repr(sorted(self.api_handlers)),
            encoded_code=encoded,
        )
        result = self._run(script)
        result.execution_time_ms = int((time.monotonic() - started) * 1_000)
        return result

    def _call(self, request: dict) -> dict:
        call = request.get("__api_call__", {})
        name = call.get("name")
        args = call.get("args")
        kwargs = call.get("kwargs", {})
        handler = self.api_handlers.get(name)
        if handler is None or not isinstance(args, list) or not isinstance(kwargs, dict):
            return {"error": "Unknown documentation API or invalid arguments"}
        try:
            value = handler(*args, **kwargs)
            json.dumps(value)
            return {"result": value}
        except Exception as exc:
            return {"error": f"{type(exc).__name__}: {exc}"}

    def _run(self, script: str) -> ExecutionResult:
        api_calls = 0
        process = None
        with tempfile.TemporaryDirectory(prefix="deep-docs-sandbox-") as directory:
            path = os.path.join(directory, "runner.py")
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(script)
            with tempfile.TemporaryFile(mode="w+", encoding="utf-8") as stderr_file:
                process = subprocess.Popen(
                    [sys.executable, "-I", path], cwd=directory,
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=stderr_file,
                    text=True, shell=False, start_new_session=True,
                    env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "LANG": "C", "LC_ALL": "C"},
                )
                selector = selectors.DefaultSelector()
                selector.register(process.stdout, selectors.EVENT_READ)
                payload = None
                deadline = time.monotonic() + self.timeout
                try:
                    while time.monotonic() < deadline:
                        ready = selector.select(timeout=min(0.1, max(0.0, deadline - time.monotonic())))
                        if not ready:
                            if process.poll() is not None:
                                break
                            continue
                        line = process.stdout.readline()
                        if not line:
                            break
                        line = line.rstrip("\n")
                        if line == "__SANDBOX_COMPLETE__":
                            payload = process.stdout.readline()
                            break
                        try:
                            request = json.loads(line)
                        except json.JSONDecodeError:
                            continue
                        if "__api_call__" in request:
                            api_calls += 1
                            process.stdin.write(json.dumps(self._call(request)) + "\n")
                            process.stdin.flush()
                    if payload is None and process.poll() is None:
                        process.kill()
                        process.wait(timeout=1)
                        return ExecutionResult(False, error=f"Execution timed out after {self.timeout} seconds", error_type="TimeoutError", api_calls_made=api_calls)
                    process.wait(timeout=1)
                finally:
                    selector.close()
                    if process.stdin:
                        process.stdin.close()
                    if process.stdout:
                        process.stdout.close()
                stderr_file.seek(0)
                stderr = stderr_file.read()[:20_000]
                if payload is None:
                    return ExecutionResult(False, stderr=stderr, error="Sandbox exited without a result", error_type="ProcessError", api_calls_made=api_calls)
                if len(payload.encode()) > self.max_output_bytes:
                    return ExecutionResult(False, stderr=stderr, error="Sandbox output exceeded the host limit", error_type="OutputLimitError", api_calls_made=api_calls)
                try:
                    decoded = json.loads(payload)
                except json.JSONDecodeError:
                    return ExecutionResult(False, stderr=stderr, error="Sandbox returned invalid JSON", error_type="ParseError", api_calls_made=api_calls)
                return ExecutionResult(
                    bool(decoded.get("success")), result=decoded.get("result"),
                    stdout=decoded.get("stdout", "")[:20_000], stderr=stderr,
                    error=decoded.get("error"), error_type=decoded.get("error_type"),
                    api_calls_made=api_calls,
                )
