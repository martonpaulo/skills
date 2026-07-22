"""Implemented documentation providers."""

from .docc import DoccProvider
from .github_docs import GitHubDocsProvider
from .llms_txt import LlmsTxtProvider
from .local_cli import LocalCLIProvider
from .openapi import OpenAPIProvider

PROVIDERS = {
    "docc": DoccProvider,
    "github_docs": GitHubDocsProvider,
    "llms_txt": LlmsTxtProvider,
    "local_cli": LocalCLIProvider,
    "openapi": OpenAPIProvider,
}

__all__ = [
    "DoccProvider",
    "GitHubDocsProvider",
    "LlmsTxtProvider",
    "LocalCLIProvider",
    "OpenAPIProvider",
    "PROVIDERS",
]
