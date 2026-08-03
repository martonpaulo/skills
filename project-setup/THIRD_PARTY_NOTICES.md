# Third-party notices

## product-on-purpose/pm-skills

- **Upstream repository:** https://github.com/product-on-purpose/pm-skills
- **Upstream path:** `skills/develop-solution-brief`, with `skills/define-problem-statement` also reviewed
- **Imported revision:** `9efff804c66183cdff0abd826d90479a673b6b31`
- **Imported on:** 2026-08-03
- **Last checked against upstream:** 2026-08-03
- **Original author:** product-on-purpose
- **License:** Apache-2.0, full text in [LICENSE](LICENSE), preserved unchanged.

Only the product-definition half of this skill derives from upstream. Everything about repository
identity, Git policy, versioning, licensing, GitHub metadata and project foundations was written
for this collection. No upstream file is vendored.

### What was adapted

From `develop-solution-brief`: the one-page constraint as the thing that forces prioritization,
documenting explicitly what is not being done and why, connecting the work to a measurable
outcome, and the rule that a brief pitches while a specification specifies, so the two must not be
merged.

From `define-problem-statement`: naming a specific user segment rather than "users", stating the
job and how people cope today, and surfacing constraints before the solution space is narrowed.

### What changed

**Folded into setup rather than standing alone.** Upstream splits problem framing and solution
brief across separate skills in a phased methodology. Here the product definition is the first
half of one setup interview, because its outputs are the inputs to the repository's own questions:
the benefit-first description, the GitHub topics and the landing-page decision all derive from
knowing what the product is.

**Non-goals became the load-bearing section.** Upstream records trade-offs as one step among
several. Here every non-goal must carry its reason, because a non-goal without one is reopened
later, and the definition's whole job is to answer whether a proposed feature belongs.

**No methodology ceremony.** Upstream's Triple Diamond and Foundation Sprint phases, readiness
gates, Decider role, skill-family contracts, and the `timebox_minutes`, `roles`, `prerequisites`
and `phase` metadata are all dropped. This collection requires no methodology.

**No invented numbers.** Upstream's templates prompt for baselines and targets in every row. Here a
baseline or target is recorded only when one genuinely exists, because a fabricated metric is worse
than an absent one.

**Solution-free.** Upstream's solution brief names key features and the proposed approach. This
half deliberately commits to no technology, framework, architecture or data model, and states so;
individual requirements belong to `issue-capture`.

**No templates vendored.** Upstream's `references/TEMPLATE.md` and `references/EXAMPLE.md` were
read and not imported. The section list in the skill replaces them.
