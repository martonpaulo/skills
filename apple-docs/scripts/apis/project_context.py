"""Read-only Apple project and local toolchain context detection."""

from __future__ import annotations

import json
import os
import plistlib
import re
import subprocess
from pathlib import Path
from typing import Callable, Iterable


_DEPLOYMENT_KEYS = {
    "IPHONEOS_DEPLOYMENT_TARGET": "iOS",
    "MACOSX_DEPLOYMENT_TARGET": "macOS",
    "TVOS_DEPLOYMENT_TARGET": "tvOS",
    "WATCHOS_DEPLOYMENT_TARGET": "watchOS",
    "XROS_DEPLOYMENT_TARGET": "visionOS",
}
_PLATFORM_HINTS = {
    "iphoneos": "iOS",
    "iphonesimulator": "iOS",
    "macosx": "macOS",
    "appletvos": "tvOS",
    "appletvsimulator": "tvOS",
    "watchos": "watchOS",
    "watchsimulator": "watchOS",
    "xros": "visionOS",
    "xrsimulator": "visionOS",
}


def _safe_run(args: list[str], timeout: float = 5.0) -> dict:
    """Run one fixed read-only tool query without inheriting secrets."""
    env = {
        "PATH": os.environ.get("PATH", "/usr/bin:/bin:/usr/sbin:/sbin"),
        "LANG": "C",
        "LC_ALL": "C",
    }
    try:
        completed = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
            shell=False,
            env=env,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError) as exc:
        return {"available": False, "error": type(exc).__name__}
    output = (completed.stdout or completed.stderr).strip()
    return {
        "available": completed.returncode == 0,
        "returncode": completed.returncode,
        "output": output[:20_000],
    }


def _resolve_within(root: Path, requested: str) -> Path:
    if not isinstance(requested, str) or not requested.strip():
        raise ValueError("path must be a non-empty string")
    candidate = (root / requested).resolve() if not Path(requested).is_absolute() else Path(requested).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise ValueError("path must remain inside the configured project root") from exc
    return candidate


def _safe_matches(root: Path, pattern: str, *, directories: bool = False) -> list[Path]:
    matches = []
    for item in root.rglob(pattern):
        try:
            resolved = item.resolve(strict=True)
            resolved.relative_to(root)
        except (OSError, ValueError):
            continue
        if directories and resolved.is_dir():
            matches.append(resolved)
        elif not directories and resolved.is_file():
            matches.append(resolved)
    return matches


def _extract_deployment_targets(files: Iterable[Path]) -> dict[str, list[str]]:
    found: dict[str, set[str]] = {}
    pattern = re.compile(
        r"\b(" + "|".join(re.escape(key) for key in _DEPLOYMENT_KEYS) + r")\s*=\s*([^;\s]+)"
    )
    for path in files:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for key, value in pattern.findall(text):
            found.setdefault(_DEPLOYMENT_KEYS[key], set()).add(value.strip('"'))
    return {platform: sorted(values) for platform, values in sorted(found.items())}


def _parse_package_resolved(path: Path) -> list[dict]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    pins = data.get("pins") or data.get("object", {}).get("pins") or []
    packages = []
    for pin in pins:
        state = pin.get("state", {})
        version = state.get("version") or state.get("revision")
        identity = pin.get("identity") or pin.get("package")
        if identity and version:
            packages.append({"name": identity, "version": version})
    return sorted(packages, key=lambda item: item["name"].lower())


def _parse_podfile_lock(path: Path) -> list[dict]:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    pods = []
    in_pods = False
    for line in text.splitlines():
        if line == "PODS:":
            in_pods = True
            continue
        if in_pods and line and not line.startswith(" "):
            break
        match = re.match(r"\s{2}-\s+([^\s(/:]+)(?:/[^\s(:]+)?\s+\(([^)]+)\)", line)
        if in_pods and match:
            pods.append({"name": match.group(1), "version": match.group(2)})
    unique = {(item["name"], item["version"]): item for item in pods}
    return sorted(unique.values(), key=lambda item: item["name"].lower())


def _entitlement_summary(path: Path) -> dict:
    try:
        with path.open("rb") as handle:
            values = plistlib.load(handle)
    except (OSError, plistlib.InvalidFileException):
        return {"file": path.name, "unresolved": True}
    keys = sorted(str(key) for key in values)
    capabilities = [key for key in keys if key.startswith("com.apple.developer.")]
    return {
        "file": path.name,
        "keys": keys,
        "capabilities": capabilities,
        "app_sandbox": values.get("com.apple.security.app-sandbox"),
    }


class AppleProjectContextDetector:
    """Detect Apple project context within one configured repository root."""

    def __init__(self, root: str | Path = ".", runner: Callable[[list[str], float], dict] = _safe_run):
        self.root = Path(root).expanduser().resolve()
        self.runner = runner

    def detect(self, path: str = ".") -> dict:
        target = _resolve_within(self.root, path)
        if not target.exists() or not target.is_dir():
            return {"error": "project path does not exist or is not a directory"}

        xcode = self.runner(["xcodebuild", "-version"], 5.0)
        swift = self.runner(["swift", "--version"], 5.0)
        sdks = self.runner(["xcodebuild", "-showsdks"], 8.0)

        projects = sorted(str(item.relative_to(target)) for item in _safe_matches(target, "*.xcodeproj", directories=True))
        workspaces = sorted(str(item.relative_to(target)) for item in _safe_matches(target, "*.xcworkspace", directories=True))
        build_files = _safe_matches(target, "project.pbxproj") + _safe_matches(target, "*.xcconfig")
        deployment_targets = _extract_deployment_targets(build_files)

        sdk_names = []
        if sdks.get("available"):
            for match in re.finditer(r"-sdk\s+([A-Za-z0-9.]+)", sdks.get("output", "")):
                sdk_names.append(match.group(1))

        platforms = set(deployment_targets)
        for sdk in sdk_names:
            lowered = sdk.lower()
            for prefix, platform in _PLATFORM_HINTS.items():
                if lowered.startswith(prefix):
                    platforms.add(platform)

        package_files = _safe_matches(target, "Package.resolved")
        pod_files = _safe_matches(target, "Podfile.lock")
        entitlements = [_entitlement_summary(item) for item in sorted(_safe_matches(target, "*.entitlements"))]

        signing = {}
        signing_pattern = re.compile(
            r"\b(CODE_SIGN_STYLE|DEVELOPMENT_TEAM|CODE_SIGN_IDENTITY|PROVISIONING_PROFILE_SPECIFIER)\s*=\s*([^;\n]+)"
        )
        for build_file in build_files:
            try:
                text = build_file.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            for key, value in signing_pattern.findall(text):
                cleaned = value.strip().strip('"')
                signing.setdefault(key, set()).add(cleaned)

        unknown = []
        if not xcode.get("available"):
            unknown.append("Xcode version")
        if not swift.get("available"):
            unknown.append("Swift version")
        if not sdks.get("available"):
            unknown.append("installed SDKs")
        if not deployment_targets:
            unknown.append("deployment targets")

        return {
            "project_root": str(target),
            "xcode_version": xcode.get("output") if xcode.get("available") else None,
            "swift_version": swift.get("output") if swift.get("available") else None,
            "installed_sdks": sorted(set(sdk_names)),
            "workspaces": workspaces,
            "projects": projects,
            "target_platforms": sorted(platforms),
            "deployment_targets": deployment_targets,
            "swift_packages": [
                item
                for file in package_files
                for item in _parse_package_resolved(file)
            ],
            "cocoapods": [item for file in pod_files for item in _parse_podfile_lock(file)],
            "relevant_build_settings": {
                key: sorted(values) for key, values in sorted(signing.items())
            },
            "entitlements": entitlements,
            "capabilities": sorted(
                {capability for item in entitlements for capability in item.get("capabilities", [])}
            ),
            "app_sandbox": any(item.get("app_sandbox") is True for item in entitlements),
            "unknown": unknown,
        }


_detector = AppleProjectContextDetector()


def configure_project_root(path: str | Path) -> None:
    global _detector
    _detector = AppleProjectContextDetector(path)


def detect_apple_project_context(path: str = ".") -> dict:
    return _detector.detect(path)
