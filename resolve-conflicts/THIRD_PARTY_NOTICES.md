# Third-party notices

## mattpocock/skills (engineering/resolving-merge-conflicts)

- **Upstream repository:** https://github.com/mattpocock/skills
- **Upstream path:** `skills/engineering/resolving-merge-conflicts`
- **Imported revision:** `ed37663cc5fbef691ddfecd080dff42f7e7e350d`
- **Imported on:** 2026-07-22
- **Last checked against upstream:** 2026-08-03
- **Original author:** Matt Pocock
- **License:** MIT

No upstream file is vendored. The 14-line original was rewritten.

### What was adapted

Inspecting the operation's current state before touching anything, reconstructing each side's
original intent from commits and linked artifacts, preserving both intents where compatible,
never inventing new behavior, and running the project's own checks afterwards.

### What changed

Two upstream instructions were reversed, both for safety:

**Aborting is legitimate.** Upstream says "Always resolve; never `--abort`". This version treats an
abort as appropriate when continuing risks data loss, produces invalid history, or lacks a
required decision, and requires explaining what the abort would preserve before performing it. A
rule that forbids the safe exit is a rule that produces bad resolutions under pressure.

**The operation is not finished by default.** Upstream ends with "Stage everything and commit"
and, when rebasing, continuing until every commit is rebased. Here the skill does not commit,
continue, push, or force-push unless the user's requested scope includes that action, and
force-pushing always needs explicit authorization. Resolving a conflict and completing a rebase
are different requests.

### What was added

Identifying which operation is actually in progress (merge, rebase, cherry-pick, revert), stopping
for a decision when code and history cannot determine the correct product behavior, resolving one
coherent unit at a time, running the smallest relevant tests before the broader ones, confirming
the index holds only intended resolutions, and a completion report stating whether the operation
remains paused or was explicitly completed.
