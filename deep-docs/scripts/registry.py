"""Provider registry and normalized documentation APIs."""

from __future__ import annotations

import re

from context import ProjectContextDetector
from models import SourceConfig
from providers import PROVIDERS


_APPLE_TERMS = {
    "apple", "appkit", "foundation", "ios", "ipados", "macos", "swift", "swiftui", "uikit",
    "visionos", "watchos", "xcode", "xros",
}


def _is_apple_product(product: str | None) -> bool:
    if not product:
        return False
    lowered = product.lower()
    return any(re.search(rf"\b{re.escape(term)}\b", lowered) for term in _APPLE_TERMS)


class DocumentationRegistry:
    def __init__(self, project_root: str = "."):
        self.context = ProjectContextDetector(project_root)
        self.providers = []

    def add_provider(self, provider) -> None:
        self.providers.append(provider)

    def add_source(self, value: dict) -> None:
        config = SourceConfig.from_dict(value)
        if _is_apple_product(config.product):
            raise ValueError("Apple development documentation must be configured through apple-docs")
        provider_type = PROVIDERS.get(config.provider)
        if provider_type is None:
            raise ValueError(f"unsupported provider: {config.provider}")
        if not provider_type.detect(config.source):
            raise ValueError(f"source does not match provider {config.provider}")
        self.add_provider(provider_type(config))

    def detect_project_context(self, path: str = ".") -> dict:
        return self.context.detect(path)

    def resolve_product(self, name: str | None = None, path: str = ".") -> dict:
        if _is_apple_product(name):
            return {"route_to": "apple-docs", "reason": "Apple development documentation is owned by apple-docs"}
        return self.context.resolve_product(name, path)

    def list_available_sources(self, product: str | None = None) -> list[dict]:
        matches = []
        for provider in self.providers:
            if product and provider.product.lower() != product.lower():
                continue
            matches.append(
                {
                    "name": provider.name,
                    "product": provider.product,
                    "provider": type(provider).__name__,
                    "source": provider.source,
                    "version": provider.version,
                    "capabilities": vars(provider.capabilities),
                }
            )
        return matches

    def _matching(self, product: str | None):
        if _is_apple_product(product):
            return []
        return [provider for provider in self.providers if not product or provider.product.lower() == product.lower()]

    def search_docs(self, query: str, product: str | None = None, version: str | None = None, limit: int = 10) -> dict:
        if _is_apple_product(product):
            return {"route_to": "apple-docs", "reason": "Apple documentation is intentionally not duplicated"}
        providers = self._matching(product)
        if not providers:
            return {"matches": [], "uncertainty": "No configured documentation source matches the product"}
        per_provider = max(1, min(int(limit), 50))
        matches, errors = [], []
        for provider in providers:
            try:
                matches.extend(provider.search(query, version=version, limit=per_provider).get("matches", []))
            except Exception as exc:
                errors.append({"provider": provider.name, "error": f"{type(exc).__name__}: {exc}"})
            if len(matches) >= limit:
                break
        output = {"matches": matches[:limit], "count": min(len(matches), limit)}
        if errors:
            output["errors"] = errors
        if not matches:
            output["uncertainty"] = "No authoritative match was returned; network or source coverage may be unavailable"
        return output

    def fetch_doc(self, reference: str, sections: list[str] | None = None, max_chars: int = 10_000) -> dict:
        errors = []
        for provider in self.providers:
            try:
                return provider.fetch(reference, sections=sections, max_chars=max_chars)
            except Exception as exc:
                errors.append({"provider": provider.name, "error": f"{type(exc).__name__}: {exc}"})
        return {"error": "reference_not_supported", "details": errors}

    def search_release_notes(self, query: str, product: str | None = None, from_version: str | None = None, to_version: str | None = None) -> dict:
        if _is_apple_product(product):
            return {"route_to": "apple-docs"}
        matches, errors = [], []
        for provider in self._matching(product):
            if not provider.capabilities.release_notes:
                continue
            try:
                result = provider.get_release_notes(to_version or from_version)
                for match in result.get("matches", []):
                    if query.lower() in str(match).lower():
                        matches.append(match)
            except Exception as exc:
                errors.append({"provider": provider.name, "error": f"{type(exc).__name__}: {exc}"})
        output = {"matches": matches, "from_version": from_version, "to_version": to_version}
        if errors:
            output["errors"] = errors
        if not matches:
            output["uncertainty"] = "No configured provider returned matching release notes"
        return output

    def search_official_source(self, query: str, product: str | None = None, version: str | None = None) -> dict:
        matches, errors = [], []
        for provider in self._matching(product):
            if not provider.capabilities.official_source:
                continue
            try:
                matches.extend(provider.search(query, version=version, limit=20).get("matches", []))
            except Exception as exc:
                errors.append({"provider": provider.name, "error": f"{type(exc).__name__}: {exc}"})
        output = {"matches": matches, "count": len(matches)}
        if errors:
            output["errors"] = errors
        return output


_registry = DocumentationRegistry()


def configure(project_root: str = ".", sources: list[dict] | None = None) -> None:
    global _registry
    _registry = DocumentationRegistry(project_root)
    for source in sources or []:
        _registry.add_source(source)


def detect_project_context(path: str = ".") -> dict:
    return _registry.detect_project_context(path)


def resolve_product(name: str | None = None, path: str = ".") -> dict:
    return _registry.resolve_product(name, path)


def list_available_sources(product: str | None = None) -> list[dict]:
    return _registry.list_available_sources(product)


def search_docs(query: str, product: str | None = None, version: str | None = None, limit: int = 10) -> dict:
    return _registry.search_docs(query, product, version, limit)


def fetch_doc(reference: str, sections: list[str] | None = None, max_chars: int = 10_000) -> dict:
    return _registry.fetch_doc(reference, sections, max_chars)


def search_release_notes(query: str, product: str | None = None, from_version: str | None = None, to_version: str | None = None) -> dict:
    return _registry.search_release_notes(query, product, from_version, to_version)


def search_official_source(query: str, product: str | None = None, version: str | None = None) -> dict:
    return _registry.search_official_source(query, product, version)


PUBLIC_APIS = (
    "detect_project_context", "resolve_product", "list_available_sources", "search_docs",
    "fetch_doc", "search_release_notes", "search_official_source",
)
