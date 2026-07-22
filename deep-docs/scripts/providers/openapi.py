"""Provider for JSON OpenAPI and Swagger specifications."""

from __future__ import annotations

import json
import urllib.parse

from models import DocumentationResult, ProviderCapabilities, SourceConfig
from network import SafeHTTPClient


class OpenAPIProvider:
    capabilities = ProviderCapabilities()

    def __init__(self, config: SourceConfig, client: SafeHTTPClient | None = None):
        if not self.detect(config.source):
            raise ValueError("OpenAPI provider requires an HTTPS JSON specification URL")
        self.name = config.name
        self.product = config.product
        self.source = config.source
        self.version = config.version
        host = urllib.parse.urlsplit(config.source).hostname
        self.client = client or SafeHTTPClient({host})
        self._document = None

    @classmethod
    def detect(cls, source: str) -> bool:
        parsed = urllib.parse.urlsplit(source)
        return parsed.scheme == "https" and parsed.path.lower().endswith(".json")

    def _load(self) -> dict:
        if self._document is None:
            response = self.client.get(self.source, ("application/json", "application/vnd.oai.openapi+json"))
            document = json.loads(response.body.decode("utf-8"))
            if "openapi" not in document and "swagger" not in document:
                raise ValueError("JSON document is not an OpenAPI or Swagger specification")
            self._document = document
        return self._document

    def _resolved_version(self) -> str | None:
        info_version = self._load().get("info", {}).get("version")
        return str(info_version) if info_version is not None else self.version

    def search(self, query: str, *, version: str | None, limit: int) -> dict:
        terms = query.lower().split()
        matches = []
        for path, operations in self._load().get("paths", {}).items():
            for method, operation in operations.items():
                if method.lower() not in {"get", "put", "post", "delete", "options", "head", "patch", "trace"} or not isinstance(operation, dict):
                    continue
                title = operation.get("summary") or operation.get("operationId") or f"{method.upper()} {path}"
                description = operation.get("description", "")
                if all(term in f"{title} {description} {path}".lower() for term in terms):
                    matches.append(
                        DocumentationResult(
                            product=self.product,
                            requested_version=version,
                            resolved_version=self._resolved_version(),
                            title=title,
                            source_type="official_api_specification",
                            authority="primary",
                            url=f"{self.source}#{method.lower()}:{path}",
                            content=f"{method.upper()} {path}\n{description}".strip(),
                        ).to_dict()
                    )
                if len(matches) >= max(1, min(int(limit), 100)):
                    return {"provider": self.name, "matches": matches, "count": len(matches)}
        return {"provider": self.name, "matches": matches, "count": len(matches)}

    def fetch(self, reference: str, *, sections: list[str] | None, max_chars: int) -> dict:
        base, separator, fragment = reference.partition("#")
        if base != self.source or not separator or ":" not in fragment:
            raise ValueError("OpenAPI reference must come from this provider's search results")
        method, path = fragment.split(":", 1)
        operation = self._load().get("paths", {}).get(path, {}).get(method)
        if not isinstance(operation, dict):
            raise ValueError("OpenAPI operation was not found")
        content = json.dumps(operation, indent=2, ensure_ascii=False)
        title = operation.get("summary") or operation.get("operationId") or f"{method.upper()} {path}"
        return DocumentationResult(
            product=self.product,
            resolved_version=self._resolved_version(),
            title=title,
            source_type="official_api_specification",
            authority="primary",
            url=reference,
            content=content[: max(1, min(int(max_chars), 50_000))],
            deprecated=operation.get("deprecated") if isinstance(operation.get("deprecated"), bool) else None,
        ).to_dict()
