"""Controlled discovery and reading of additional local Xcode documentation."""

from __future__ import annotations

import os
import plistlib
from pathlib import Path
from typing import Iterable


_DOC_RELATIVE = Path(
    "Contents/PlugIns/IDEIntelligenceChat.framework/Versions/A/Resources/AdditionalDocumentation"
)


def _safe_name(value: str, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    if value in {".", ".."} or "/" in value or "\\" in value or "\x00" in value:
        raise ValueError(f"{field} must not contain a path")
    return value.strip()


class LocalXcodeDocumentation:
    """Index expected Xcode documentation folders without exposing arbitrary paths."""

    def __init__(self, application_roots: Iterable[str | Path] = ("/Applications",)):
        self.application_roots = tuple(Path(root).expanduser().resolve() for root in application_roots)
        self._sources: dict[str, dict] | None = None
        self._documents: dict[tuple[str, str], Path] | None = None

    def _xcode_version(self, app: Path) -> str:
        plist = app / "Contents/Info.plist"
        try:
            with plist.open("rb") as handle:
                data = plistlib.load(handle)
            return str(data.get("CFBundleShortVersionString") or data.get("CFBundleVersion") or "unknown")
        except (OSError, plistlib.InvalidFileException):
            return "unknown"

    def _build_index(self) -> None:
        sources: dict[str, dict] = {}
        documents: dict[tuple[str, str], Path] = {}
        for root in self.application_roots:
            if not root.is_dir():
                continue
            for app in sorted(root.glob("Xcode*.app")):
                try:
                    app.resolve().relative_to(root)
                except ValueError:
                    continue
                docs = (app / _DOC_RELATIVE).resolve()
                try:
                    docs.relative_to(app.resolve())
                except ValueError:
                    continue
                if not docs.is_dir():
                    continue
                version = self._xcode_version(app)
                source_id = app.name
                count = 0
                for doc in sorted(docs.glob("*.md")):
                    resolved = doc.resolve()
                    try:
                        resolved.relative_to(docs)
                    except ValueError:
                        continue
                    name = doc.stem
                    documents[(source_id, name)] = resolved
                    count += 1
                sources[source_id] = {
                    "source": source_id,
                    "xcode_version": version,
                    "document_count": count,
                    "source_type": "local_xcode_additional_documentation",
                    "authority": "local_sdk_documentation",
                    "public_api_contract": False,
                }
        self._sources = sources
        self._documents = documents

    def _ensure_index(self) -> None:
        if self._sources is None or self._documents is None:
            self._build_index()

    def list_sources(self) -> list[dict]:
        self._ensure_index()
        return [dict(value) for _, value in sorted(self._sources.items())]

    def _matching_sources(self, xcode_version: str | None) -> list[str]:
        self._ensure_index()
        if xcode_version is None:
            return sorted(self._sources)
        value = _safe_name(xcode_version, "xcode_version")
        return [
            source
            for source, metadata in sorted(self._sources.items())
            if source == value or metadata["xcode_version"] == value
        ]

    def search(self, query: str, xcode_version: str | None = None, limit: int = 20) -> dict:
        if not isinstance(query, str) or not query.strip():
            raise ValueError("query must be a non-empty string")
        limit = max(1, min(int(limit), 100))
        query_lower = query.lower()
        source_ids = set(self._matching_sources(xcode_version))
        matches = []
        self._ensure_index()
        for (source_id, name), path in sorted(self._documents.items()):
            if source_id not in source_ids:
                continue
            try:
                content = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            index = content.lower().find(query_lower)
            if query_lower in name.lower() or index >= 0:
                start = max(0, index - 180) if index >= 0 else 0
                snippet = content[start : start + 500].strip()
                matches.append(
                    {
                        "name": name,
                        "source": source_id,
                        "xcode_version": self._sources[source_id]["xcode_version"],
                        "snippet": snippet,
                        "source_type": "local_xcode_additional_documentation",
                        "authority": "local_sdk_documentation",
                        "public_api_contract": False,
                    }
                )
                if len(matches) >= limit:
                    break
        return {"query": query, "matches": matches, "count": len(matches)}

    def fetch(self, name: str, xcode_version: str | None = None, max_chars: int = 10_000) -> dict:
        name = _safe_name(name, "name")
        max_chars = max(1, min(int(max_chars), 50_000))
        source_ids = self._matching_sources(xcode_version)
        self._ensure_index()
        candidates = [(source, self._documents.get((source, name))) for source in source_ids]
        candidates = [(source, path) for source, path in candidates if path is not None]
        if not candidates:
            return {"error": "document_not_found", "name": name}
        if len(candidates) > 1 and xcode_version is None:
            return {
                "error": "ambiguous_document",
                "name": name,
                "sources": [source for source, _ in candidates],
            }
        source, path = candidates[0]
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            return {"error": "document_unreadable", "message": type(exc).__name__}
        truncated = len(content) > max_chars
        return {
            "name": name,
            "source": source,
            "xcode_version": self._sources[source]["xcode_version"],
            "source_type": "local_xcode_additional_documentation",
            "authority": "local_sdk_documentation",
            "public_api_contract": False,
            "content": content[:max_chars],
            "truncated": truncated,
        }


_local_docs = LocalXcodeDocumentation()


def configure_xcode_application_roots(roots: Iterable[str | Path]) -> None:
    global _local_docs
    _local_docs = LocalXcodeDocumentation(roots)


def list_xcode_documentation_sources() -> list[dict]:
    return _local_docs.list_sources()


def search_local_xcode_docs(query: str, xcode_version: str | None = None, limit: int = 20) -> dict:
    return _local_docs.search(query, xcode_version, limit)


def fetch_local_xcode_doc(name: str, xcode_version: str | None = None, max_chars: int = 10_000) -> dict:
    return _local_docs.fetch(name, xcode_version, max_chars)
