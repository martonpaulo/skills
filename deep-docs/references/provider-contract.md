# Provider contract

Every configured provider exposes detection plus normalized search and fetch operations. Release notes and official-source search are capabilities, not mandatory stubs.

```python
detect(source: str) -> bool
search(query: str, *, version: str | None, limit: int) -> dict
fetch(reference: str, *, sections: list[str] | None, max_chars: int) -> dict
```

Providers declare whether they support release notes or official-source search. The registry calls only declared capabilities.

Implemented providers:

- `llms_txt`: official `llms.txt` or `llms-full.txt` indexes and linked text/Markdown documents on the configured host.
- `github_docs`: Markdown or MDX in an explicitly configured official GitHub repository, using the Git tree and raw-content endpoints.
- `openapi`: JSON OpenAPI or Swagger specifications. YAML is not implemented.
- `docc`: non-Apple DocC JSON documentation on an explicitly configured host.
- `local_cli`: allowlisted local executable help and version output.

Do not advertise Docusaurus, MkDocs, Sphinx, GitBook, arbitrary HTML, or other providers until a complete implementation and tests exist.

Normalized results contain only grounded fields such as product, requested and resolved version, title, source type, authority, URL or CLI identifier, selected content, examples, deprecation, availability, and fetch time. Omit unknown fields instead of guessing.
