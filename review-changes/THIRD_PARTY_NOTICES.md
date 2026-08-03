# Third-party notices

## mattpocock/skills (engineering/code-review)

- **Upstream repository:** https://github.com/mattpocock/skills
- **Upstream path:** `skills/engineering/code-review`
- **Imported revision:** `2ab958093e83e0ec752e6c1c5932da465bf23e0c`
- **Imported on:** 2026-08-03
- **Original author:** Matt Pocock
- **License:** MIT, full text in [LICENSE](LICENSE), preserved unchanged.

### What was adapted

The two-axis structure and the reason for it, pinning a fixed point with the three-dot diff,
resolving the ref before doing anything expensive, the ordered search for the originating
statement, the rule that a documented repository convention overrides the baseline, skipping
anything tooling enforces, and the prohibition on reranking findings across axes.

The smell baseline in `references/smell-baseline.md` is upstream's list, drawn from Martin
Fowler's *Refactoring* chapter 3. It was reformatted into a table and given a routing boundary,
but the selection and the what-it-is/how-to-fix pairing are upstream's.

### What changed

**Renamed to `review-changes`.** The name `code-review` is already taken in this collection by the
pull-request Validate phase. The two skills now state each other as non-triggers instead of
competing: `code-review` owns a pull request, `review-changes` owns the local diff before one
exists.

**Subagents are optional.** Upstream requires spawning two `general-purpose` sub-agents in
parallel and pastes the baseline into their prompts, because they have no other access to it.
Here a single pass must produce the same report, and parallel read-only agents are an explicit
optimization. This collection does not require subagents.

**No required tracker configuration.** Upstream stops and tells the user to run
`/setup-matt-pocock-skills` when `docs/agents/issue-tracker.md` is missing. The intent search here
degrades through four ordered sources and reports the Standards axis alone when none is found.

**The absent-intent case is a stated rule.** Reconstructing intent from the diff and then judging
the diff against it is now explicitly prohibited, because that check always passes. Upstream
skipped the axis without saying why the shortcut is invalid.

**Uncommitted and staged work is in scope.** Upstream compares `HEAD` to the fixed point only.
Here `git status --porcelain` is part of the scope capture and every finding names which of the
three states it came from, since the point of this skill is reviewing work before it is committed.

**Audit boundary added.** Upstream states no mutation policy. This version is `mutation: none`,
user-invoked, and prohibited from editing, staging, committing, pushing, branching, opening a pull
request, or fixing a finding. Findings that need deeper work are routed by name to `test-design`,
`module-design`, or `bug-hunter` rather than expanding the review.

**Word limits dropped.** Upstream caps each sub-agent report at 400 words. The cap was an artifact
of the subagent transport, not a review property.
