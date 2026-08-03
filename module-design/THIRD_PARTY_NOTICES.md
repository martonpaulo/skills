# Third-party notices

## mattpocock/skills (engineering/codebase-design)

- **Upstream repository:** https://github.com/mattpocock/skills
- **Upstream path:** `skills/engineering/codebase-design`
- **Imported revision:** `ed37663cc5fbef691ddfecd080dff42f7e7e350d`
- **Imported on:** 2026-07-22
- **Last checked against upstream:** 2026-08-03
- **Original author:** Matt Pocock
- **License:** MIT

No upstream file is vendored. `DEEPENING.md` and `DESIGN-IT-TWICE.md` keep upstream's purpose and
were rewritten to about a quarter of their length.

### What was adapted

The central criterion, which is upstream's: prefer a deep module, meaning substantial behavior
behind a small, stable interface. The seam as the place where behavior can be altered without
editing in that place, and as the surface both callers and tests cross. Considering at least two
designs when the boundary is consequential. Accepting dependencies rather than creating them.
Avoiding a seam that nothing actually varies across, and avoiding abstraction that only forwards
calls.

### What changed

**The vocabulary mandate was removed.** Upstream's glossary opens with "use these terms exactly,
don't substitute component, service, API, or boundary", and its rejected-framings section argues
against "boundary" specifically. This version states the opposite: names such as service,
component, API, manager, and helper are normal repository vocabulary and are criticized only when
they conceal unclear responsibility. A design skill that spends its findings on renaming is not
improving the design, and this collection's skills run against codebases whose conventions the
owner did not choose.

**The criteria are not laws.** An explicit statement was added that a small function, a local
helper, a framework component, or a direct dependency may be the best design. Upstream presents
its principles as the correct answer.

**Framework fit was added.** A section requires applying the same criteria through native
conventions, naming Spring services and beans, React and Next.js components and hooks, and Swift
types and protocols, and forbids forcing one ecosystem's layering or terminology onto another.
Upstream has no equivalent and its examples are TypeScript throughout.

**No required subagents.** Upstream's design-it-twice pattern spins up parallel sub-agents to
design the interface several ways. Here designing it twice is the discipline and the parallelism
is not required.

**Compressed from 114 lines to 44.** The formal glossary, the ASCII deep-versus-shallow diagrams,
the relationships list, and the rejected-framings section were dropped. They defined a vocabulary
this version deliberately does not enforce.
