---
name: review-changes
description: Review the working diff against a fixed point on two independent axes, standards and intent, before the change becomes a pull request. Use only when the user explicitly invokes $review-changes for uncommitted work, staged work, a local branch, or a range such as "review since main". Not for reviewing a pull request, which belongs to code-review, and not for adversarial bug hunting, implementing the findings, or reviewing an untouched codebase.
argument-hint: "[fixed point, e.g. main | HEAD~3 | <sha>]"
disable-model-invocation: true
license: MIT
metadata:
  scope: project
  role: audit
  mutation: none
  upstream: https://github.com/mattpocock/skills
  upstream-author: Matt Pocock
  upstream-path: skills/engineering/code-review
  upstream-revision: 2ab958093e83e0ec752e6c1c5932da465bf23e0c
  upstream-checked: 2026-08-03
  version: mattpocock-personal.1
---

# Review Changes

Review a local diff before it becomes a pull request, on two axes that are reported separately:

- **Standards:** does the change follow the conventions this repository documents?
- **Intent:** does the change do what it was supposed to do, no less and no more?

A change can pass one axis and fail the other. Code that follows every convention can implement
the wrong thing, and code that satisfies the request can break the repository's rules. Reporting
them separately stops one from masking the other.

This skill reports findings and never edits. `code-review` owns the formal Validate phase for a
pull request; do not use this skill in its place. `bug-hunter` owns adversarial defect hunting
with runtime traces; this review reports a defect it happens to see but does not run that hunt.

## 1. Pin the fixed point

Take the argument as the fixed point: a SHA, branch, tag, `main`, `HEAD~5`. Without an argument,
infer it from the repository's own default branch and state the inference before continuing.

Resolve it and capture the scope once:

```bash
git rev-parse <fixed-point>
git diff <fixed-point>...HEAD
git log <fixed-point>..HEAD --oneline
git status --porcelain
```

Use the three-dot form so the comparison runs against the merge base. Include uncommitted and
staged work when it exists, and say which of the three states each finding came from.

Stop here if the ref does not resolve or the combined diff is empty. Do not proceed with an empty
scope and report findings about unchanged code.

## 2. Establish intent

Find what the change was supposed to do, in this order:

1. an issue referenced by the commit messages or the branch name, fetched from the GitHub API
   through the available native GitHub integration or `gh api`. GitHub is the only tracker this
   collection targets; do not degrade towards another one;
2. a path the user supplied;
3. a specification, plan, or issue body already present in the repository;
4. the user's own description of the change.

When no statement of intent exists, say so and report the Standards axis alone. Never reconstruct
the intent from the diff itself and then judge the diff against it; that check always passes.

## 3. Establish the standards

Read the applicable `AGENTS.md`, nested instruction files, and any documented conventions such as
`CONTRIBUTING.md` or a coding-standards document. Read enough surrounding code to know what the
repository's established patterns actually are.

On top of what the repository documents, apply the smell baseline in
[smell-baseline.md](references/smell-baseline.md). Two rules bind it:

- **The repository overrides.** A documented convention always wins. Where the repository endorses
  something the baseline would flag, suppress it.
- **The baseline is always a judgment call.** Report each as a labelled heuristic, never as a
  violation.

Skip anything the project's tooling already enforces. A formatter or linter finding is not a
review finding.

## 4. Run both axes

Run the two axes without letting one inform the other. Evaluate Standards against the documented
conventions and the baseline; evaluate Intent against the statement found in step 2.

If independent agents are available and the user wants them, the axes may run as two read-only
agents in parallel to keep their contexts separate. This is an optimization. A single pass must
produce the same report, and the skill retains the evidence contract either way.

For each axis:

- **Standards:** where the diff breaks a documented convention, cite the file and the rule. Where
  it trips a baseline smell, name the smell and quote the hunk. Keep hard violations and judgment
  calls visibly separate.
- **Intent:** what the statement asked for that is missing or partial; behavior in the diff that
  was never asked for; and requirements that look implemented but are implemented wrongly. Quote
  the line of the statement behind each finding.

Route out rather than expanding scope: a missing or weak test is a `test-design` question, an
unstable boundary is a `module-design` question, and a suspected runtime defect that needs a
reachability trace is a `bug-hunter` question. Name the route; do not perform it here.

## 5. Report

Report the two axes under separate headings and do not merge or rerank them across axes. The
separation is the point.

Include:

1. **Scope:** the fixed point, the commit list, the file count, and which of committed, staged,
   and uncommitted work was included.
2. **Standards:** findings with file, line, the cited rule or named smell, the quoted hunk, and
   whether it is a hard violation or a judgment call.
3. **Intent:** findings with the quoted statement line, the gap, and its consequence.
4. **Routed out:** anything that belongs to another skill, named with the skill.
5. **Summary:** the count per axis and the worst finding within each axis. Do not pick a single
   worst across axes.

Every finding names a location. Report no finding that rests on code you did not read.

## Safety and completion

Do not edit code, tests, configuration, or documentation; do not stage, commit, push, create a
branch, or open a pull request; do not fix a finding. If the user asks for fixes during the
review, finish the report and treat the fixes as a separate request that names the selected
findings.

The review is complete when the scope is exact, both axes ran or the missing axis is explained,
every finding cites evidence, tooling-enforced noise is absent, and nothing was mutated.
