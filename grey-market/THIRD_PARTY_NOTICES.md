# Third-party notices

## grey-market

- **Upstream repository:** https://github.com/felinto-dev/felinto-skills
- **Upstream path:** `.agents/skills/grey-market`
- **Imported revision:** `8fde9cd3424e7fd612879e4d44c0680c834b68e9`
- **Imported on:** 2026-07-25
- **Original author:** felinto-dev
- **License:** the upstream repository publishes no license file. This copy is kept for
  personal use with attribution to the original author. Do not redistribute it as an original
  work, and re-check the upstream terms before reusing it elsewhere.

`references/markets.md` and the `scripts/` helpers are upstream work, kept essentially intact.
The regional market intelligence in them is the substance of this skill.

### What was adapted

**Optional tooling instead of required tooling.** Upstream mandated SearXNG and Lightpanda over
Docker and required 2 to 4 parallel subagents for broad sweeps. Here, both stacks are stated as
ordered preferences with real fallbacks, and the parallel sweep is an optimization that a
single-threaded run must be able to match. Skills in this collection do not require Docker,
background execution, or subagents to work.

**Explicit transaction boundary.** The skill now states up front and again at the end that it
never enters payment details, creates accounts, or completes a purchase. Upstream implied this;
it is now a rule.

**Editorial pass.** Rewritten for the house style of this collection: narrower frontmatter
description with explicit non-triggers, `python3` rather than `python`, and a maintenance note
about the exchange rates going stale.

### Script change

`scripts/dork-generator.sh` derived its year-variant dork from a hardcoded `2024`. It now uses
the current year, so the generated dorks keep surfacing fresh threads.
