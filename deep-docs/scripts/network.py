"""Controlled HTTPS client with SSRF and response-boundary enforcement."""

from __future__ import annotations

import ipaddress
import socket
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Callable


@dataclass
class HTTPResponse:
    status: int
    headers: dict[str, str]
    body: bytes


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def _default_resolver(hostname: str) -> list[str]:
    return sorted({item[4][0] for item in socket.getaddrinfo(hostname, 443, type=socket.SOCK_STREAM)})


def _default_transport(url: str, headers: dict[str, str], timeout: float, max_bytes: int) -> HTTPResponse:
    request = urllib.request.Request(url, headers=headers)
    opener = urllib.request.build_opener(_NoRedirect())
    try:
        response = opener.open(request, timeout=timeout)
    except urllib.error.HTTPError as exc:
        if 300 <= exc.code < 400:
            return HTTPResponse(exc.code, {key.lower(): value for key, value in exc.headers.items()}, b"")
        raise
    with response:
        body = response.read(max_bytes + 1)
        if len(body) > max_bytes:
            raise ValueError(f"response exceeds {max_bytes} bytes")
        return HTTPResponse(
            response.status,
            {key.lower(): value for key, value in response.headers.items()},
            body,
        )


class SafeHTTPClient:
    def __init__(
        self,
        allowed_hosts: set[str],
        *,
        max_bytes: int = 2_000_000,
        timeout: float = 10.0,
        max_redirects: int = 3,
        resolver: Callable[[str], list[str]] = _default_resolver,
        transport: Callable[[str, dict[str, str], float, int], HTTPResponse] = _default_transport,
    ):
        self.allowed_hosts = {host.lower().rstrip(".") for host in allowed_hosts}
        self.max_bytes = max_bytes
        self.timeout = timeout
        self.max_redirects = max_redirects
        self.resolver = resolver
        self.transport = transport

    def validate_url(self, url: str) -> str:
        parsed = urllib.parse.urlsplit(url)
        if parsed.scheme != "https" or not parsed.hostname:
            raise ValueError("documentation URLs must use HTTPS")
        if parsed.username or parsed.password:
            raise ValueError("credentials in URLs are not allowed")
        hostname = parsed.hostname.lower().rstrip(".")
        if hostname not in self.allowed_hosts:
            raise ValueError(f"host is not owned by this provider: {hostname}")
        addresses = self.resolver(hostname)
        if not addresses:
            raise ValueError("hostname did not resolve")
        for address in addresses:
            ip = ipaddress.ip_address(address)
            if not ip.is_global:
                raise ValueError(f"unsafe destination address: {address}")
        return urllib.parse.urlunsplit(parsed)

    def get(self, url: str, accepted_types: tuple[str, ...]) -> HTTPResponse:
        current = self.validate_url(url)
        for redirect_count in range(self.max_redirects + 1):
            response = self.transport(
                current,
                {"User-Agent": "deep-docs/0.1", "Accept": ", ".join(accepted_types)},
                self.timeout,
                self.max_bytes,
            )
            if 300 <= response.status < 400:
                if redirect_count >= self.max_redirects:
                    raise ValueError("too many redirects")
                location = response.headers.get("location")
                if not location:
                    raise ValueError("redirect has no location")
                current = self.validate_url(urllib.parse.urljoin(current, location))
                continue
            if not 200 <= response.status < 300:
                raise ValueError(f"documentation request failed with HTTP {response.status}")
            content_type = response.headers.get("content-type", "").split(";", 1)[0].strip().lower()
            if not content_type:
                raise ValueError("documentation response has no content type")
            if not any(content_type == accepted or content_type.startswith(accepted + "/") for accepted in accepted_types):
                raise ValueError(f"unsupported content type: {content_type}")
            if len(response.body) > self.max_bytes:
                raise ValueError(f"response exceeds {self.max_bytes} bytes")
            return response
        raise ValueError("redirect handling failed")
