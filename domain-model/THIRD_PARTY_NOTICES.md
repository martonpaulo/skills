# Third-party notices

## mattpocock/skills (engineering/domain-modeling)

- **Upstream repository:** https://github.com/mattpocock/skills
- **Upstream path:** `skills/engineering/domain-modeling`
- **Imported revision:** `ed37663cc5fbef691ddfecd080dff42f7e7e350d`
- **Imported on:** 2026-07-22
- **Last checked against upstream:** 2026-08-03
- **Original author:** Matt Pocock
- **License:** MIT

No upstream file is vendored. `CONTEXT-FORMAT.md` and `ADR-FORMAT.md` keep upstream's purpose and
were rewritten to about a third of their length.

### What was adapted

The distinction between changing the model and merely reading it, which is upstream's and is why
this skill has a narrow trigger. Challenging a term against the existing glossary, proposing a
canonical meaning for an overloaded one, stress-testing relationships with concrete scenarios,
cross-referencing stated behavior against the code, creating files lazily, and keeping
`CONTEXT.md` free of implementation details, specifications, and scratch notes.

The three-part ADR test is upstream's and is kept unchanged: hard to reverse, surprising without
context, and the result of a real tradeoff. All three must hold.

### What changed

**Contradictions are surfaced, not resolved.** Upstream challenges the user immediately and asks
which reading is right. Here the requested behavior, the documentation, and the code are compared
and the contradiction is made visible rather than silently settled in favour of one source.

**Multi-context structure is preserved, not prescribed.** Upstream documents a `CONTEXT-MAP.md`
layout with per-context glossaries and per-context ADR directories. This version assumes one
context unless the repository already shows clear, meaningful context boundaries, and preserves an
existing multi-context structure when it finds one. Imposing that layout on a repository that does
not need it is the failure mode.

**Paths are configurable.** Repository guidance decides where the glossary lives, with `CONTEXT.md`
as the fallback. `setup-agent-docs` owns recording that choice.

**Scope is bounded by ambiguity.** Entities, value concepts, states, transitions, rules, ownership,
and relationships are distinguished only as far as the current ambiguity requires, and no glossary
is created for a codebase without meaningful domain language. Upstream models actively and
continuously.
