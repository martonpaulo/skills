"""Safe best-effort project and version detection without dependency changes."""

from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path


_RANGE_MARKERS = re.compile(r"[<>=~^*|,\s]|(latest|workspace|file|path|git)\b", re.IGNORECASE)


def version_kind(value: str | None) -> str:
    if not value:
        return "unresolved"
    cleaned = value.strip().strip('"\'')
    if not cleaned or _RANGE_MARKERS.search(cleaned):
        return "range"
    return "exact"


def _read(path: Path, max_bytes: int = 2_000_000) -> str:
    if path.is_symlink() or not path.is_file() or path.stat().st_size > max_bytes:
        return ""
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def _record(ecosystem: str, name: str, declared: str | None = None, locked: str | None = None, source: str | None = None) -> dict:
    result = {
        "ecosystem": ecosystem,
        "name": name,
        "declared_version": declared,
        "declared_version_kind": version_kind(declared),
        "locked_version": locked,
        "detected_runtime_version": None,
        "source": source,
    }
    result["resolved_version"] = locked or (declared if version_kind(declared) == "exact" else None)
    result["resolution"] = "locked" if locked else ("declared_exact" if result["resolved_version"] else "unresolved")
    return result


def _package_json(root: Path) -> list[dict]:
    manifest = root / "package.json"
    try:
        data = json.loads(_read(manifest))
    except json.JSONDecodeError:
        return []
    declared = {}
    for section in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
        declared.update(data.get(section, {}))
    locked = {}
    lock = root / "package-lock.json"
    if lock.is_file():
        try:
            lock_data = json.loads(_read(lock))
            for path, item in lock_data.get("packages", {}).items():
                if path.startswith("node_modules/") and path.count("node_modules/") == 1 and item.get("version"):
                    locked[path.removeprefix("node_modules/")] = str(item["version"])
            for name, item in lock_data.get("dependencies", {}).items():
                if isinstance(item, dict) and item.get("version"):
                    locked.setdefault(name, str(item["version"]))
        except json.JSONDecodeError:
            pass
    for filename in ("pnpm-lock.yaml", "yarn.lock"):
        text = _read(root / filename)
        if filename == "pnpm-lock.yaml":
            for name, version in re.findall(r"(?m)^\s{2,}/?(@?[^/@\s]+(?:/[^/@\s]+)?)[@:]([^\s:]+):\s*$", text):
                locked.setdefault(name, version.strip("'\""))
        else:
            current = []
            for line in text.splitlines():
                if line and not line.startswith(" ") and line.endswith(":"):
                    current = [part.rsplit("@", 1)[0].strip('"') for part in line[:-1].split(", ")]
                match = re.match(r'\s+version\s+"([^"]+)"', line)
                if match:
                    for name in current:
                        locked.setdefault(name, match.group(1))
    return [_record("npm", name, str(value), locked.get(name), "package.json") for name, value in sorted(declared.items())]


def _maven(root: Path) -> list[dict]:
    path = root / "pom.xml"
    if not path.is_file():
        return []
    try:
        tree = ET.fromstring(_read(path))
    except ET.ParseError:
        return []
    records = []
    for dependency in tree.findall(".//{*}dependency"):
        group = dependency.findtext("{*}groupId")
        artifact = dependency.findtext("{*}artifactId")
        version = dependency.findtext("{*}version")
        if group and artifact:
            records.append(_record("maven", f"{group}:{artifact}", version, source="pom.xml"))
    return records


def _gradle(root: Path) -> list[dict]:
    records = []
    for filename in ("build.gradle", "build.gradle.kts"):
        text = _read(root / filename)
        for group, artifact, version in re.findall(r"['\"]([^:'\"]+):([^:'\"]+):([^'\"]+)['\"]", text):
            records.append(_record("gradle", f"{group}:{artifact}", version, source=filename))
    versions = _read(root / "gradle/libs.versions.toml")
    for name, version in re.findall(r'(?m)^([A-Za-z0-9_.-]+)\s*=\s*"([^"]+)"\s*$', versions):
        records.append(_record("gradle-catalog", name, version, source="gradle/libs.versions.toml"))
    return records


def _python(root: Path) -> list[dict]:
    records = []
    requirements = _read(root / "requirements.txt")
    for line in requirements.splitlines():
        match = re.match(r"^([A-Za-z0-9_.-]+)\s*(==|~=|>=|<=|>|<)?\s*([^;#\s]+)?", line.strip())
        if match and match.group(1) and not line.startswith(("-", "#")):
            value = (match.group(2) or "") + (match.group(3) or "")
            records.append(_record("pypi", match.group(1), value or None, value.removeprefix("==") if value.startswith("==") else None, "requirements.txt"))
    pyproject = _read(root / "pyproject.toml")
    for name, version in re.findall(r'(?m)^([A-Za-z0-9_.-]+)\s*=\s*"([^"]+)"\s*$', pyproject):
        if name.lower() not in {"name", "version", "description", "python"}:
            records.append(_record("pypi", name, version, source="pyproject.toml"))
    poetry_lock = _read(root / "poetry.lock")
    names = re.findall(r'(?m)^name\s*=\s*"([^"]+)"\s*\nversion\s*=\s*"([^"]+)"', poetry_lock)
    locks = {name: version for name, version in names}
    for record in records:
        if record["name"] in locks:
            record.update(_record(record["ecosystem"], record["name"], record["declared_version"], locks[record["name"]], record["source"]))
    return records


def _swift(root: Path) -> list[dict]:
    declared = {}
    package_swift = _read(root / "Package.swift")
    for url, from_version, exact_version in re.findall(r'\.package\s*\(\s*url:\s*"([^"]+)"\s*,\s*(?:from:\s*"([^"]+)"|exact:\s*"([^"]+)")', package_swift):
        declared[url.rstrip("/").rsplit("/", 1)[-1].removesuffix(".git")] = from_version or exact_version
    locked = {}
    for path in (root / "Package.resolved", root / ".swiftpm/Package.resolved"):
        if not path.is_file():
            continue
        try:
            data = json.loads(_read(path))
        except json.JSONDecodeError:
            continue
        for pin in data.get("pins") or data.get("object", {}).get("pins") or []:
            name = pin.get("identity") or pin.get("package")
            state = pin.get("state", {})
            version = state.get("version") or state.get("revision")
            if name and version:
                locked[name] = version
    return [_record("swift-package", name, declared.get(name), version, "Package.resolved") for name, version in sorted(locked.items())] + [
        _record("swift-package", name, version, source="Package.swift") for name, version in sorted(declared.items()) if name not in locked
    ]


def _pods(root: Path) -> list[dict]:
    text = _read(root / "Podfile.lock")
    records = []
    in_pods = False
    for line in text.splitlines():
        if line == "PODS:":
            in_pods = True
            continue
        if in_pods and line and not line.startswith(" "):
            break
        match = re.match(r"\s{2}-\s+([^\s(/:]+)(?:/[^\s(:]+)?\s+\(([^)]+)\)", line)
        if in_pods and match:
            records.append(_record("cocoapods", match.group(1), locked=match.group(2), source="Podfile.lock"))
    return records


def _cargo(root: Path) -> list[dict]:
    manifest = _read(root / "Cargo.toml")
    declared = {name: version for name, version in re.findall(r'(?m)^([A-Za-z0-9_-]+)\s*=\s*"([^"]+)"\s*$', manifest)}
    lock = _read(root / "Cargo.lock")
    locked = {name: version for name, version in re.findall(r'(?m)^name\s*=\s*"([^"]+)"\s*\nversion\s*=\s*"([^"]+)"', lock)}
    return [_record("crates.io", name, version, locked.get(name), "Cargo.toml") for name, version in sorted(declared.items())]


def _go(root: Path) -> list[dict]:
    text = _read(root / "go.mod")
    records = []
    for name, version in re.findall(r"(?m)^\s*([^\s]+)\s+(v[^\s]+)(?:\s+//.*)?$", text):
        if "/" in name:
            records.append(_record("go", name, version, version, "go.mod"))
    return records


def _dotnet(root: Path) -> list[dict]:
    records = []
    for path in root.glob("*.csproj"):
        try:
            tree = ET.fromstring(_read(path))
        except ET.ParseError:
            continue
        for package in tree.findall(".//PackageReference"):
            name = package.get("Include") or package.get("Update")
            version = package.get("Version") or package.findtext("Version")
            if name:
                records.append(_record("nuget", name, version, source=path.name))
    return records


def _containers(root: Path) -> list[dict]:
    records = []
    for path in (root / "Dockerfile", root / "docker-compose.yml", root / "compose.yml"):
        text = _read(path)
        for image in re.findall(r"(?mi)^\s*(?:FROM|image:)\s+([^\s#]+)", text):
            name, separator, tag = image.rpartition(":")
            if not separator or "/" in tag:
                name, tag = image, None
            records.append(_record("container", name, tag, tag if tag and tag != "latest" else None, path.name))
    return records


class ProjectContextDetector:
    def __init__(self, root: str | Path = "."):
        self.root = Path(root).expanduser().resolve()

    def _target(self, path: str) -> Path:
        candidate = (self.root / path).resolve() if not Path(path).is_absolute() else Path(path).resolve()
        try:
            candidate.relative_to(self.root)
        except ValueError as exc:
            raise ValueError("path must remain inside the configured project root") from exc
        if not candidate.is_dir():
            raise ValueError("project path is not a directory")
        return candidate

    def detect(self, path: str = ".") -> dict:
        root = self._target(path)
        parser_results = [
            *_package_json(root), *_maven(root), *_gradle(root), *_python(root),
            *_swift(root), *_pods(root), *_cargo(root), *_go(root), *_dotnet(root), *_containers(root),
        ]
        merged = {}
        for item in parser_results:
            key = (item["ecosystem"], item["name"].lower())
            previous = merged.get(key)
            if previous is None or (item.get("locked_version") and not previous.get("locked_version")):
                merged[key] = item

        manifests = [
            name for name in (
                "package.json", "package-lock.json", "pnpm-lock.yaml", "yarn.lock", "pom.xml",
                "build.gradle", "build.gradle.kts", "gradle/libs.versions.toml", "Package.swift",
                "Package.resolved", "Podfile.lock", "pyproject.toml", "requirements.txt", "poetry.lock",
                "Cargo.toml", "Cargo.lock", "go.mod", "global.json", "Dockerfile",
                "docker-compose.yml", "compose.yml",
            ) if (root / name).is_file()
        ]
        manifests.extend(path.name for path in root.glob("*.csproj"))
        package_swift = _read(root / "Package.swift").lower()
        apple_project = bool(list(root.glob("*.xcodeproj")) or list(root.glob("*.xcworkspace")) or (root / "Podfile.lock").is_file())
        apple_project |= any(token in package_swift for token in (".ios(", ".macos(", ".tvos(", ".watchos(", ".visionos("))

        runtime = {}
        global_json = root / "global.json"
        if global_json.is_file():
            try:
                runtime["dotnet"] = json.loads(_read(global_json)).get("sdk", {}).get("version")
            except json.JSONDecodeError:
                runtime["dotnet"] = None
        return {
            "project_root": str(root),
            "manifests": sorted(set(manifests)),
            "dependencies": sorted(merged.values(), key=lambda item: (item["ecosystem"], item["name"].lower())),
            "runtime_versions": runtime,
            "routing": "apple-docs" if apple_project else "deep-docs",
            "uncertainty": [] if manifests else ["No supported project manifest was found"],
        }

    def resolve_product(self, name: str | None = None, path: str = ".") -> dict:
        context = self.detect(path)
        if context["routing"] == "apple-docs":
            return {"route_to": "apple-docs", "reason": "Apple project context detected"}
        if not name:
            return {"product": None, "resolved_version": None, "status": "unknown_product"}
        matches = [item for item in context["dependencies"] if item["name"].lower() == name.lower()]
        if not matches:
            return {"product": name, "resolved_version": None, "status": "unknown_version"}
        item = matches[0]
        return {
            "product": item["name"],
            "ecosystem": item["ecosystem"],
            "declared_version": item["declared_version"],
            "declared_version_kind": item["declared_version_kind"],
            "locked_version": item["locked_version"],
            "detected_runtime_version": item["detected_runtime_version"],
            "resolved_version": item["resolved_version"],
            "status": item["resolution"],
        }
