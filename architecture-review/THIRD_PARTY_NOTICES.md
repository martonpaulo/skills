# Third-party notices

## mattpocock/skills (engineering/improve-codebase-architecture)

- **Upstream repository:** https://github.com/mattpocock/skills
- **Upstream path:** `skills/engineering/improve-codebase-architecture`
- **Imported revision:** `ed37663cc5fbef691ddfecd080dff42f7e7e350d`
- **Imported on:** 2026-07-22
- **Last checked against upstream:** 2026-08-03
- **Original author:** Matt Pocock
- **License:** MIT

No upstream file is vendored. Upstream's `HTML-REPORT.md` is not carried at all.

### What was adapted

Scoping the scan before running it, weighting recent change history so the review lands on code
that actually moves, delegating the boundary vocabulary to the codebase-design skill (here
`module-design`), consulting the domain glossary and existing decisions, ranking a top
recommendation with a reason, and stopping before implementation until the user picks a candidate.

### What changed

**No HTML report.** Upstream's main artifact is a self-contained HTML file built with Tailwind and
Mermaid from CDNs, written to the OS temporary directory and opened in the user's browser, with a
before/after visualisation per candidate. That is dropped entirely; findings are reported as
Markdown in the conversation, or to a file only when the user asks or repository guidance says
where. `HTML-REPORT.md` was not imported.

**No required subagent.** Upstream walks the codebase through the `Explore` subagent and reaches
for a design-it-twice parallel subagent pattern. This collection does not require subagents.

**The vocabulary lock was removed.** Upstream requires using its terms exactly and forbids drifting
into "component", "service", "API", or "boundary". This collection's `module-design` takes the
opposite position: those names are normal and are criticized only when they conceal unclear
responsibility. Enforcing a private vocabulary on someone else's codebase produces findings about
naming rather than about architecture.

**Audit-only.** Upstream writes to `CONTEXT.md` and offers ADRs inline during the interview loop
after a candidate is chosen. Here the skill is `mutation: docs`, does not refactor, and routes to
`domain-model` only when inconsistent terminology materially affects the architecture. Selecting a
finding for implementation is a separate request.

**Findings carry a cost model.** Upstream rates candidates `Strong`, `Worth exploring`, or
`Speculative`. This version requires evidence in files and symbols, the observed consequence, and
a ranking across impact, confidence, effort, implementation risk, and expected payoff, and prefers
a few high-value findings over an exhaustive catalogue.
