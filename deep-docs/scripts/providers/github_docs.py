"""Provider for documentation in an official GitHub Markdown or MDX repository."""

from __future__ import annotations

import json
import re
import urllib.parse

from models import DocumentationResult, ProviderCapabilities, SourceConfig
from network import SafeHTTPClient


_REPO = re.compile(r"^https://github\.com/([^/]+)/([^/#]+?)(?:\.git)?/?$")


class GitHubDocsProvider:
    capabilities = ProviderCapabilities(release_notes=True, official_source=True)

    def __init__(self, config: SourceConfig, client: SafeHTTPClient | None = None):
        match = _REPO.match(config.source)
        if not match:
            raise ValueError("GitHub docs source must be an HTTPS repository root")
        self.owner, self.repo = match.groups()
        self.name = config.name
        self.product = config.product
        self.source = config.source
        self.version = config.version
        self.client = client or SafeHTTPClient({"api.github.com", "raw.githubusercontent.com"})

    @classmethod
    def detect(cls, source: str) -> bool:
        return bool(_REPO.match(source))

    def _ref(self, version: str | None) -> str:
        return version or self.version or "main"

    def _json(self, url: str):
        response = self.client.get(url, ("application/json", "application/vnd.github+json"))
        return json.loads(response.body.decode("utf-8"))

    def _tree(self, ref: str) -> list[dict]:
        url = f"https://api.github.com/repos/{self.owner}/{self.repo}/git/trees/{urllib.parse.quote(ref, safe='')}?recursive=1"
        data = self._json(url)
        if data.get("truncated"):
            raise ValueError("GitHub tree is truncated; configure a narrower documentation repository")
        return data.get("tree", [])

    def search(self, query: str, *, version: str | None, limit: int) -> dict:
        ref = self._ref(version)
        terms = query.lower().split()
        matches = []
        for item in self._tree(ref):
            path = item.get("path", "")
            if item.get("type") != "blob" or not path.lower().endswith((".md", ".mdx")):
                continue
            if not all(term in path.lower() for term in terms):
                continue
            url = f"https://raw.githubusercontent.com/{self.owner}/{self.repo}/{urllib.parse.quote(ref, safe='')}/{urllib.parse.quote(path)}"
            matches.append(
                DocumentationResult(
                    product=self.product,
                    requested_version=version,
                    resolved_version=ref,
                    title=path.rsplit("/", 1)[-1],
                    source_type="official_source_documentation",
                    authority="primary",
                    url=url,
                    content=path,
                ).to_dict()
            )
            if len(matches) >= max(1, min(int(limit), 100)):
                break
        return {"provider": self.name, "matches": matches, "count": len(matches)}

    def fetch(self, reference: str, *, sections: list[str] | None, max_chars: int) -> dict:
        parsed = urllib.parse.urlsplit(reference)
        prefix = f"/{self.owner}/{self.repo}/"
        if parsed.hostname != "raw.githubusercontent.com" or not parsed.path.startswith(prefix):
            raise ValueError("reference must belong to the configured GitHub repository")
        response = self.client.get(reference, ("text/plain", "text/markdown", "application/octet-stream"))
        text = response.body.decode("utf-8", errors="replace")
        reference_parts = [part for part in parsed.path.split("/") if part]
        resolved_ref = urllib.parse.unquote(reference_parts[2]) if len(reference_parts) > 2 else self.version
        if sections:
            wanted = [section.lower() for section in sections]
            text = "\n".join(
                chunk for chunk in re.split(r"(?m)(?=^#{1,6}\s+)", text)
                if any(term in chunk.splitlines()[0].lower() for term in wanted) if chunk.splitlines()
            )
        return DocumentationResult(
            product=self.product,
            resolved_version=resolved_ref,
            title=parsed.path.rsplit("/", 1)[-1],
            source_type="official_source_documentation",
            authority="primary",
            url=reference,
            content=text[: max(1, min(int(max_chars), 50_000))],
        ).to_dict()

    def get_release_notes(self, version: str | None) -> dict:
        ref = self._ref(version)
        matches = []
        for item in self._tree(ref):
            path = item.get("path", "")
            lowered = path.lower()
            if item.get("type") == "blob" and lowered.endswith((".md", ".mdx")) and any(token in lowered for token in ("changelog", "release-note", "migration")):
                matches.append({"path": path, "reference": f"https://raw.githubusercontent.com/{self.owner}/{self.repo}/{ref}/{path}"})
            if len(matches) >= 20:
                break
        return {"provider": self.name, "resolved_version": ref, "matches": matches}
