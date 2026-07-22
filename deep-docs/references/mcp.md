# Read-only documentation MCP profiles

The skill may use a documentation MCP source already exposed by the current agent. It does not install, bundle, launch, or probe an MCP server and has no FastMCP dependency.

A profile must explicitly name:

- the server or source;
- the search tool;
- the fetch tool;
- an optional version-resolution tool;
- whether every operation is read-only;
- how source URLs or stable identifiers are returned.

Conceptual profile:

```yaml
servers:
  context7:
    search_tool: resolve-library-id
    fetch_tool: get-library-docs
    read_only: true
    source_identity: returned-url-or-library-id
```

Use a profile only when the server is already configured, all invoked operations are read-only, source identity survives normalization, and version context is represented or explicitly marked unresolved. Do not infer arbitrary tool schemas and do not expose a generic MCP executor to sandbox code.
