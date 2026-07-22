"""Provider for non-Apple DocC JSON documentation."""

from __future__ import annotations

import json
import urllib.parse

from models import DocumentationResult, ProviderCapabilities, SourceConfig
from network import SafeHTTPClient


_APPLE_HOSTS = {"developer.apple.com", "swift.org"}


def _inline_text(value) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "".join(_inline_text(item) for item in value)
    if isinstance(value, dict):
        return str(value.get("text") or value.get("code") or "")
    return ""


class DoccProvider:
    capabilities = ProviderCapabilities()

    def __init__(self, config: SourceConfig, client: SafeHTTPClient | None = None):
        if not self.detect(config.source):
            raise ValueError("DocC provider requires a non-Apple HTTPS JSON documentation source")
        self.name = config.name
        self.product = config.product
        self.source = config.source
        self.version = config.version
        host = urllib.parse.urlsplit(config.source).hostname
        self.client = client or SafeHTTPClient({host})

    @classmethod
    def detect(cls, source: str) -> bool:
        parsed = urllib.parse.urlsplit(source)
        return parsed.scheme == "https" and parsed.hostname not in _APPLE_HOSTS and parsed.path.lower().endswith(".json")

    def _load(self, url: str) -> dict:
        response = self.client.get(url, ("application/json",))
        document = json.loads(response.body.decode("utf-8"))
        if not isinstance(document, dict) or not any(key in document for key in ("metadata", "references", "sections", "primaryContentSections")):
            raise ValueError("JSON document does not look like DocC output")
        return document

    def _result(self, document: dict, url: str, max_chars: int = 10_000) -> dict:
        metadata = document.get("metadata", {})
        title = metadata.get("title") or document.get("identifier", {}).get("url") or self.product
        abstract = _inline_text(document.get("abstract", []))
        parts = [abstract]
        for section in document.get("primaryContentSections", []) or document.get("sections", []):
            heading = section.get("title") or section.get("kind") or ""
            content = _inline_text(section.get("content", []))
            if heading or content:
                parts.append(f"{heading}\n{content}".strip())
        platforms = metadata.get("platforms") if isinstance(metadata.get("platforms"), list) else []
        availability = {"platforms": platforms} if platforms else {}
        return DocumentationResult(
            product=self.product,
            resolved_version=self.version,
            title=str(title),
            source_type="official_docc_documentation",
            authority="primary",
            url=url,
            content="\n\n".join(part for part in parts if part)[:max_chars],
            availability=availability,
        ).to_dict()

    def search(self, query: str, *, version: str | None, limit: int) -> dict:
        document = self._load(self.source)
        terms = query.lower().split()
        matches = []
        root = self._result(document, self.source, 2_000)
        if all(term in f"{root['title']} {root.get('content', '')}".lower() for term in terms):
            root["requested_version"] = version
            matches.append(root)
        for identifier, reference in document.get("references", {}).items():
            if not isinstance(reference, dict):
                continue
            title = reference.get("title") or identifier
            abstract = _inline_text(reference.get("abstract", []))
            if not all(term in f"{title} {abstract}".lower() for term in terms):
                continue
            target = reference.get("url")
            if not isinstance(target, str):
                continue
            target_url = urllib.parse.urljoin(self.source, target)
            if urllib.parse.urlsplit(target_url).scheme != "https":
                continue
            matches.append(
                DocumentationResult(
                    product=self.product,
                    requested_version=version,
                    resolved_version=self.version,
                    title=title,
                    source_type="official_docc_documentation",
                    authority="primary",
                    url=target_url,
                    content=abstract,
                ).to_dict()
            )
            if len(matches) >= max(1, min(int(limit), 100)):
                break
        return {"provider": self.name, "matches": matches, "count": len(matches)}

    def fetch(self, reference: str, *, sections: list[str] | None, max_chars: int) -> dict:
        source_host = urllib.parse.urlsplit(self.source).hostname
        if urllib.parse.urlsplit(reference).hostname != source_host:
            raise ValueError("DocC reference must use the configured source host")
        document = self._load(reference)
        result = self._result(document, reference, max(1, min(int(max_chars), 50_000)))
        if sections:
            lowered = [section.lower() for section in sections]
            chunks = result.get("content", "").split("\n\n")
            result["content"] = "\n\n".join(chunk for chunk in chunks if any(term in chunk.lower() for term in lowered))
        return result
