# Upstream attribution

`apple-docs` is a personalized fork of **Ahrentlov/apple-docs-skill** by Patrick Ahrentløv.

- Repository: https://github.com/Ahrentlov/apple-docs-skill
- Imported commit: `c45f520e5c9ab8e4aabbeaa532b061ada06883ce`
- Upstream version: `1.5.0`
- License: MIT; see [LICENSE](LICENSE).

The personalized version keeps the upstream author metadata and appends the local version suffix `-personal.1`. Local changes add project-context detection, controlled local Xcode documentation discovery, stricter sandbox validation, output limits, source-authority policy, updated cache documentation, and agent-neutral usage guidance.

Architectural ideas for local Xcode documentation discovery were also reviewed from **Ahrentlov/appledeepdoc-mcp** by Patrick Ahrentløv:

- Repository: https://github.com/Ahrentlov/appledeepdoc-mcp
- Reviewed commit: `5087bd04fb0cf6cb5dda422dcda798506a678df4`
- License: MIT

No FastMCP runtime or MCP server code is required by this skill.
