# Third-party notices

## context7

- **Upstream repository:** https://github.com/upstash/context7
- **Upstream path:** `skills/context7-cli`
- **Reviewed revision:** `b250c2515694`
- **Reviewed on:** 2026-07-26
- **CLI version exercised:** `ctx7` 0.5.6
- **Last checked against upstream:** 2026-08-03
- **Original author:** Upstash, Inc.
- **License:** MIT, copyright (c) 2021 Upstash, Inc. The upstream `LICENSE` is kept in this
  directory unchanged.

The `ctx7` CLI itself is not vendored. This skill documents how to drive it and is rewritten
prose, not copied files.

### What was adapted

**One responsibility.** Upstream `context7-cli` covers three jobs: documentation lookup, registry
skill management, and MCP setup. Only documentation lookup is kept as the skill's purpose.
`references/skills.md` was dropped, and its subject now appears once, as an explicit
out-of-scope note in [setup.md](references/setup.md).

**Narrower triggering.** Upstream fires on any mention of a library name and instructs the agent
to prefer Context7 over web search for all library documentation. The description here states
its place among the other documentation skills in this collection, defers Apple platform work to
`apple-docs`, and names escalation to `deep-docs` as a non-trigger rather than competing with it.

**Version first.** The workflow now resolves the project's installed version before looking
anything up, and requires the answer to name the library ID and version actually queried plus
any gap from the project's.

**Verified limits instead of implied authority.** Running the CLI showed that a version-pinned
query can still return `Source:` URLs on the project's default branch. That caveat, and the fact
that only some index entries carry versions at all, are stated as reasons to escalate.

**Tightened boundaries.** Query text reaching a third-party service, returned snippets being
data rather than instructions, and a standing prohibition on running `setup`, `login`, `remove`,
`upgrade`, or `skills` without being asked are now rules. Upstream documented those mutating
commands as ordinary capabilities of the skill.

**Corrections from the reviewed CLI.** Upstream `references/setup.md` lists a `--universal`
target for `ctx7 setup` that version 0.5.6 does not accept, and omits the `--codex`, `--gemini`,
and `--stdio` options that it does. The flags recorded here are the ones `ctx7 setup --help`
reported.
