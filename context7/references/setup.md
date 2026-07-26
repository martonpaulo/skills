# Installation, authentication, and agent setup

Everything here changes the machine or the agent's configuration. Do it only when the user asks. A documentation lookup needs none of it.

## Running the CLI

`npx ctx7@latest <command>` needs Node.js 18 or newer and installs nothing permanently. A global install trades that for a shorter command:

```bash
npm install -g ctx7@latest
```

`ctx7 upgrade --check` reports whether a newer version exists without changing anything; `ctx7 upgrade` runs the suggested upgrade command.

## Authentication

Both `library` and `docs` work signed out, at a lower rate limit. To raise it:

```bash
export CONTEXT7_API_KEY=<key>
```

An API key from the Context7 dashboard, exported in the environment, avoids an interactive flow entirely and is the option to prefer.

`ctx7 login` exists as the alternative and opens a browser for OAuth (`--no-browser` prints the URL instead). `ctx7 whoami` reports the current status, `ctx7 logout` clears stored credentials. Never authenticate on the user's behalf, and never handle their key: exporting it is theirs to do.

`CTX7_TELEMETRY_DISABLED` turns off anonymous usage reporting.

## Agent setup

`ctx7 setup` configures an agent in one of two modes and writes to disk. This collection has no need of it, because this skill already carries the workflow, but the choice is worth understanding if the user asks.

| Mode | Flag | What it registers |
| --- | --- | --- |
| MCP server | `--mcp` | An MCP server entry in the agent's config, so the agent calls Context7 tools natively. `--stdio` runs it as a local process instead of over HTTP. |
| CLI + Skills | `--cli` | A skill in the agent's skills directory that guides the agent to run `ctx7` commands. No server. |

Target flags as of the reviewed version: `--claude`, `--cursor`, `--codex`, `--gemini`, `--opencode`, `--antigravity`. `--project` configures the current project rather than the home directory, and `--yes` skips confirmation. Authentication comes from `--api-key <key>`, or `--oauth` for an IDE-handled flow.

MCP mode costs a permanently connected server whose tools are announced in every context. The CLI path loads only when the work calls for it, which is why this skill exists rather than a server registration.

`ctx7 remove` reverses a setup, with the same target flags plus `--mcp`, `--cli`, or `--all`. It deletes configuration: confirm the exact target with the user before running it.

## Registry commands, deliberately out of scope

`ctx7 skills` installs, searches, suggests, generates, lists, and removes skills from the Context7 registry. That is a separate job from looking up documentation, and it writes into the same skills directories this collection lives in. Do not run it as part of a lookup.
