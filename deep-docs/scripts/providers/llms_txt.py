"""Provider for official llms.txt and llms-full.txt documentation indexes."""

from __future__ import annotations

import re
import urllib.parse

from models import DocumentationResult, ProviderCapabilities, SourceConfig
from network import SafeHTTPClient


_LINK = re.compile(r"^\s*[-*]?\s*\[([^]]+)\]\((https://[^)]+)\)(?:\s*[-:]\s*(.*))?$", re.MULTILINE)


class LlmsTxtProvider:
    capabilities = ProviderCapabilities()

    def __init__(self, config: SourceConfig, client: SafeHTTPClient | None = None):
        if not self.detect(config.source):
            raise ValueError("llms.txt provider requires an HTTPS llms.txt or llms-full.txt URL")
        self.name = config.name
        self.product = config.product
        self.source = config.source
        self.version = config.version
        host = urllib.parse.urlsplit(config.source).hostname
        self.client = client or SafeHTTPClient({host})

    @classmethod
    def detect(cls, source: str) -> bool:
        path = urllib.parse.urlsplit(source).path.lower()
        return source.startswith("https://") and path.endswith(("/llms.txt", "/llms-full.txt"))

    def _text(self, url: str) -> str:
        response = self.client.get(url, ("text/plain", "text/markdown", "application/octet-stream"))
        return response.body.decode("utf-8", errors="replace")

    def search(self, query: str, *, version: str | None, limit: int) -> dict:
        limit = max(1, min(int(limit), 100))
        text = self._text(self.source)
        terms = query.lower().split()
        matches = []
        for title, url, summary in _LINK.findall(text):
            haystack = f"{title} {summary} {url}".lower()
            if all(term in haystack for term in terms):
                matches.append(
                    DocumentationResult(
                        product=self.product,
                        requested_version=version,
                        resolved_version=self.version,
                        title=title.strip(),
                        source_type="official_documentation_index",
                        authority="primary",
                        url=url,
                        content=summary.strip(),
                    ).to_dict()
                )
            if len(matches) >= limit:
                break
        if not matches and self.source.lower().endswith("llms-full.txt"):
            for section in re.split(r"(?m)^#{1,3}\s+", text)[1:]:
                title, _, body = section.partition("\n")
                if all(term in section.lower() for term in terms):
                    matches.append(
                        DocumentationResult(
                            product=self.product,
                            requested_version=version,
                            resolved_version=self.version,
                            title=title.strip(),
                            source_type="official_documentation",
                            authority="primary",
                            url=self.source,
                            content=body.strip()[:2_000],
                        ).to_dict()
                    )
                if len(matches) >= limit:
                    break
        return {"provider": self.name, "matches": matches, "count": len(matches)}

    def fetch(self, reference: str, *, sections: list[str] | None, max_chars: int) -> dict:
        parsed_source = urllib.parse.urlsplit(self.source)
        parsed_reference = urllib.parse.urlsplit(reference)
        if parsed_reference.hostname != parsed_source.hostname:
            raise ValueError("reference must use the configured documentation host")
        text = self._text(reference)
        if sections:
            wanted = {section.lower() for section in sections}
            chunks = []
            for chunk in re.split(r"(?m)(?=^#{1,6}\s+)", text):
                heading = chunk.splitlines()[0].lstrip("# ").lower() if chunk.splitlines() else ""
                if any(section in heading for section in wanted):
                    chunks.append(chunk)
            text = "\n".join(chunks)
        max_chars = max(1, min(int(max_chars), 50_000))
        return DocumentationResult(
            product=self.product,
            resolved_version=self.version,
            title=reference.rsplit("/", 1)[-1] or self.product,
            source_type="official_documentation",
            authority="primary",
            url=reference,
            content=text[:max_chars],
        ).to_dict()
