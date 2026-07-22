"""Grounded normalized documentation result models."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


_AUTHORITIES = {"primary", "secondary", "community", "local"}


@dataclass
class DocumentationResult:
    product: str
    title: str
    source_type: str
    authority: str
    url: str
    content: str = ""
    requested_version: str | None = None
    resolved_version: str | None = None
    code_examples: list[str] = field(default_factory=list)
    deprecated: bool | None = None
    availability: dict[str, Any] = field(default_factory=dict)
    fetched_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def validate(self) -> None:
        for field_name in ("product", "title", "source_type", "authority", "url"):
            if not isinstance(getattr(self, field_name), str) or not getattr(self, field_name).strip():
                raise ValueError(f"{field_name} must be a non-empty string")
        if self.authority not in _AUTHORITIES:
            raise ValueError(f"unsupported authority: {self.authority}")
        if not self.url.startswith("https://") and not self.url.startswith("cli://"):
            raise ValueError("result URL must be HTTPS or a local CLI identifier")
        if self.deprecated is not None and not isinstance(self.deprecated, bool):
            raise ValueError("deprecated must be true, false, or omitted")

    def to_dict(self) -> dict:
        self.validate()
        data = asdict(self)
        return {
            key: value
            for key, value in data.items()
            if value not in (None, "", [], {})
        }


@dataclass(frozen=True)
class ProviderCapabilities:
    search: bool = True
    fetch: bool = True
    release_notes: bool = False
    official_source: bool = False


@dataclass(frozen=True)
class SourceConfig:
    name: str
    provider: str
    source: str
    product: str
    version: str | None = None
    authority: str = "primary"

    @classmethod
    def from_dict(cls, value: dict) -> "SourceConfig":
        required = ("name", "provider", "source", "product")
        missing = [key for key in required if not isinstance(value.get(key), str) or not value[key].strip()]
        if missing:
            raise ValueError(f"source configuration is missing: {', '.join(missing)}")
        return cls(
            name=value["name"].strip(),
            provider=value["provider"].strip(),
            source=value["source"].strip(),
            product=value["product"].strip(),
            version=value.get("version"),
            authority=value.get("authority", "primary"),
        )
