# Third-party notices

This skill adapts security and documentation-provider architecture from two MIT-licensed projects by Patrick Ahrentløv.

## Ahrentlov/apple-docs-skill

- Repository: https://github.com/Ahrentlov/apple-docs-skill
- Reviewed commit: `c45f520e5c9ab8e4aabbeaa532b061ada06883ce`
- Reviewed on: 2026-07-22
- Last checked against upstream: 2026-08-03
- Original author: Patrick Ahrentløv
- License: MIT, copyright (c) 2025 Patrick Ahrentløv
- Adapted elements: AST validation, restricted built-ins, subprocess isolation, JSON IPC, required filtered result, resource limits, and documentation-specific host APIs.

## Ahrentlov/appledeepdoc-mcp

- Repository: https://github.com/Ahrentlov/appledeepdoc-mcp
- Reviewed commit: `5087bd04fb0cf6cb5dda422dcda798506a678df4`
- Reviewed on: 2026-07-22
- Last checked against upstream: 2026-08-03
- Original author: Patrick Ahrentløv
- License: MIT, copyright (c) 2025 Patrick
- Adapted elements: provider separation, local documentation discovery concepts, API bridge normalization, controlled result filtering, and explicit documentation-source metadata.

`deep-docs` is a standalone Agent Skill. It does not copy or depend on FastMCP, does not launch an MCP server, and does not require either upstream repository at runtime.
