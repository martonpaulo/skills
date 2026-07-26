---
name: deep-docs
description: Perform authoritative, version-aware documentation research for software, frameworks, SDKs, libraries, APIs, CLIs, databases, developer tools, and platforms used in the current task or project. Detect the exact product and installed version from project files or safe local commands, then search official versioned documentation, release notes, API specifications, official source repositories, local CLI manuals, and explicitly configured read-only documentation sources. Use when implementation correctness depends on precise behavior, version compatibility, availability, deprecation, configuration, migration, or documented constraints. Prefer primary sources and return source-linked evidence. Defer Apple development documentation to apple-docs. Do not use for general web research, product recommendations, build-versus-buy decisions, debugging without a documentation question, or broad architecture decisions.
license: MIT
allowed-tools: "Bash(python3:*)"
metadata:
  version: 0.1.0
---

# Deep Docs

Answer precise non-Apple software documentation questions with explicit product and version context. Use `apple-docs` for Apple development; do not duplicate Apple providers here.

Use `context7` when an indexed snippet of a library's current API is enough. This skill owns conclusions that must be traced to an official versioned source, and is the escalation when a library is not indexed or when compatibility, availability, deprecation, or migration has to be proven.

## Workflow

1. Run `detect_project_context()` before external lookup in an existing project. Resolve declared, locked, locally detected, and unresolved versions separately.
2. Define the exact behavior, configuration, migration, compatibility, availability, or deprecation question. Use the requested version when explicit; otherwise prefer a trustworthy lock or installed version.
3. Select the smallest applicable configured provider. Read [provider-contract.md](references/provider-contract.md) for the five implemented provider types.
4. Use sources in this order: official versioned documentation; official specifications or API schemas; official release and migration notes; official repository documentation; local installed CLI documentation; accepted standards or language proposals; official vendor forums; community sources.
5. Search narrowly, fetch only the relevant document or sections, and preserve the source URL or local CLI identifier. Do not infer versions, URLs, availability, deprecation, or examples that the source did not provide.
6. Return: detected product, detected or requested version, documentation version used, documented behavior, availability or deprecation when grounded, compatibility conclusion, source, and uncertainty.

If network access or an authoritative source is unavailable, state that current external facts remain unverified. Community material may locate a risk but must not silently replace an authoritative source.

## Runner

This skill requires local shell execution and Python 3.10 or newer. `allowed-tools` is optional compatibility metadata; other agents should use their normal shell tool.

```bash
python3 scripts/run.py "result = detect_project_context()" --project-path /path/to/project --pretty
```

External providers are explicit, read-only host configuration. For example:

```bash
python3 scripts/run.py \
  "result = search_docs('transaction propagation', 'Spring Framework', '6.2.3', 5)" \
  --project-path /path/to/project \
  --source '{"name":"spring-docs","provider":"llms_txt","source":"https://docs.example.invalid/llms.txt","product":"Spring Framework","version":"6.2.3"}'
```

Replace the example domain with the product's verified official source. Submitted sandbox code has no imports, file access, subprocess access, or direct network access. It can call only:

- `detect_project_context(path=".")`
- `resolve_product(name=None, path=".")`
- `list_available_sources(product=None)`
- `search_docs(query, product=None, version=None, limit=10)`
- `fetch_doc(reference, sections=None, max_chars=10000)`
- `search_release_notes(query, product=None, from_version=None, to_version=None)`
- `search_official_source(query, product=None, version=None)`

Every query must assign a small JSON-serializable value to `result`.

## Boundaries

- Do not use this skill for general research, comparisons, product recommendations, build-versus-buy decisions, broad architecture, or debugging without a documentation dependency.
- Never update dependencies, run package scripts, build, deploy, migrate, or modify a project during detection.
- The local CLI provider allows only known executables and fixed help/version arguments. It never accepts command strings.
- Host network providers enforce HTTPS, provider-owned hosts, redirect revalidation, DNS address checks, content types, timeouts, and response limits. See [security.md](references/security.md).
- Existing read-only documentation MCP tools may be used only through an explicit profile described in [mcp.md](references/mcp.md). This skill does not bundle or launch an MCP server.

The lookup is complete when its concise conclusion is source-linked, version-scoped, and explicit about unresolved context.
