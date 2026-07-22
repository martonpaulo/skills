"""Normalized provider contract used by the documentation registry."""

from __future__ import annotations

from typing import Protocol

from models import ProviderCapabilities


class DocumentationProvider(Protocol):
    name: str
    product: str
    capabilities: ProviderCapabilities

    @classmethod
    def detect(cls, source: str) -> bool: ...

    def search(self, query: str, *, version: str | None, limit: int) -> dict: ...

    def fetch(self, reference: str, *, sections: list[str] | None, max_chars: int) -> dict: ...

    def get_release_notes(self, version: str | None) -> dict: ...
