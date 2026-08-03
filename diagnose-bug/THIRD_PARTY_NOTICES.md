# Third-party notices

## mattpocock/skills (engineering/diagnosing-bugs)

- **Upstream repository:** https://github.com/mattpocock/skills
- **Upstream path:** `skills/engineering/diagnosing-bugs`
- **Imported revision:** `ed37663cc5fbef691ddfecd080dff42f7e7e350d`
- **Imported on:** 2026-07-22
- **Last checked against upstream:** 2026-08-03
- **Original author:** Matt Pocock
- **License:** MIT

No upstream file is vendored. Upstream's `scripts/hitl-loop.template.sh` is not carried.

### What was adapted

The core discipline, which is upstream's real contribution: get concrete evidence before forming a
theory, reduce the scenario while preserving the failure, write falsifiable hypotheses instead of
vibes, test one variable at a time, remove temporary instrumentation afterwards, put the
regression test at a seam that reaches the actual bug pattern, and verify against the original
symptom rather than a nearby one.

The rule that an impossible reproduction must be stated rather than worked around is also
upstream's, and is kept as the evidence-gaps section.

### What changed

**Renamed to `diagnose-bug`.** Claude Code bundles a skill called `debug` that enables debug
logging, which is a different job. The action-oriented form also matches upstream's own
`diagnosing-bugs` more closely than the bare word did.

**Compressed from 134 lines to 33.** Upstream is six numbered phases with checkbox gates. The
retained version is a single workflow. The phase scaffolding did not change what the agent does;
it changed how much context the skill costs on every run.

**Hard gates removed.** Upstream forbids proceeding past phase 1 without a named, already-executed,
red-capable command, and forbids proceeding past phase 2 without both reproducing and minimising.
Those become strong defaults here. A bug whose evidence is a production log the user cannot rerun
still deserves diagnosis, and the honest report of missing evidence is the substitute for the
gate.

**The hypothesis count is not fixed.** Upstream requires 3 to 5 ranked hypotheses before testing
any. Here hypotheses are explicit, falsifiable, and ranked by evidence, without a quota.

**Ceremony dropped.** The `[DEBUG-xxxx]` log-tagging convention, the human-in-the-loop bash
template, and the post-mortem question about what would have prevented the bug are not carried.
The cleanup requirement they served is stated directly instead.

**Routing corrected.** Upstream hands architectural findings to its own
`improve-codebase-architecture` skill. Here documented-behavior questions route to `apple-docs` or
`deep-docs`, and this skill keeps ownership of reproduction, diagnosis, and the fix.
