"""Strict read-only provider for installed CLI help and version output."""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import urllib.parse

from models import DocumentationResult, ProviderCapabilities, SourceConfig


SAFE_EXECUTABLES = {
    "ansible", "cargo", "cmake", "deno", "docker", "dotnet", "gh", "git", "go",
    "gradle", "helm", "java", "javac", "kotlin", "kubectl", "mvn", "node", "npm",
    "php", "pod", "python3", "ruby", "rustc", "terraform",
}
SAFE_ARGUMENTS = {("--version",), ("-version",), ("--help",), ("help",)}
SAFE_PATH = "/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:/opt/homebrew/bin"


class LocalCLIProvider:
    capabilities = ProviderCapabilities()

    def __init__(self, config: SourceConfig, executable_paths: dict[str, str] | None = None):
        if not self.detect(config.source):
            raise ValueError("local CLI source must be cli://<allowlisted-executable>")
        self.executable = urllib.parse.urlsplit(config.source).hostname
        self.name = config.name
        self.product = config.product
        self.source = config.source
        self.version = config.version
        self.executable_paths = executable_paths or {}

    @classmethod
    def detect(cls, source: str) -> bool:
        parsed = urllib.parse.urlsplit(source)
        return parsed.scheme == "cli" and parsed.hostname in SAFE_EXECUTABLES and parsed.path in ("", "/")

    def _path(self) -> str:
        configured = self.executable_paths.get(self.executable)
        if configured:
            return configured
        path = shutil.which(self.executable, path=SAFE_PATH)
        if not path:
            raise ValueError(f"allowlisted executable is not installed: {self.executable}")
        return path

    def _run(self, args: tuple[str, ...]) -> str:
        if args not in SAFE_ARGUMENTS:
            raise ValueError("CLI arguments are not in the read-only policy")
        env = {"PATH": SAFE_PATH, "LANG": "C", "LC_ALL": "C", "NO_COLOR": "1"}
        with tempfile.TemporaryDirectory(prefix="deep-docs-cli-") as directory:
            completed = subprocess.run(
                [self._path(), *args], capture_output=True, text=True, timeout=5,
                check=False, shell=False, env=env, cwd=directory,
            )
        output = (completed.stdout or completed.stderr)[:50_000]
        if not output.strip() and completed.returncode != 0:
            raise ValueError(f"CLI exited with status {completed.returncode}")
        return output

    def search(self, query: str, *, version: str | None, limit: int) -> dict:
        lowered = query.lower().strip()
        args = ("--version",) if lowered in {"version", "installed version"} else ("--help",)
        result = self._result(args, version)
        return {"provider": self.name, "matches": [result], "count": 1}

    def _result(self, args: tuple[str, ...], requested_version: str | None = None) -> dict:
        output = self._run(args)
        kind = "version" if "version" in args[0] else "help"
        return DocumentationResult(
            product=self.product,
            requested_version=requested_version,
            resolved_version=output.strip().splitlines()[0][:200] if kind == "version" else self.version,
            title=f"{self.executable} {kind}",
            source_type="local_cli_documentation",
            authority="local",
            url=f"cli://{self.executable}/{kind}",
            content=output,
        ).to_dict()

    def fetch(self, reference: str, *, sections: list[str] | None, max_chars: int) -> dict:
        parsed = urllib.parse.urlsplit(reference)
        if parsed.scheme != "cli" or parsed.hostname != self.executable or parsed.path not in {"/help", "/version"}:
            raise ValueError("CLI reference must request this executable's help or version")
        args = ("--help",) if parsed.path == "/help" else ("--version",)
        result = self._result(args)
        result["content"] = result.get("content", "")[: max(1, min(int(max_chars), 50_000))]
        return result
