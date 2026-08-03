# Third-party notices

## felinto-dev/felinto-skills (dont-reinvent-the-wheel)

- **Upstream repository:** https://github.com/felinto-dev/felinto-skills
- **Upstream path:** `.agents/skills/dont-reinvent-the-wheel`
- **Imported revision:** `8fde9cd3424e7fd612879e4d44c0680c834b68e9`
- **Imported on:** 2026-07-22
- **Last checked against upstream:** 2026-08-03
- **Original author:** felinto-dev
- **License:** the upstream repository publishes no license file. This copy is kept for personal
  use with attribution to the original author. Do not redistribute it as an original work, and
  check with the author before reusing it elsewhere.

No upstream file is vendored verbatim. The reference files under `references/` were written for
this collection.

### What was adapted

The premise and the decision procedure: evaluate one specific capability rather than a codebase,
walk an ordered option ladder from what the project already has down to writing it yourself, keep
custom implementation as a real baseline rather than a last resort, and lead the answer with a
single decision label.

### What changed

**Renamed to `build-or-reuse`.** Upstream's name is a slogan: memorable, but it states a
preference rather than what the skill produces, and this version deliberately keeps building
custom as a real option rather than a last resort. The new name says which decision comes out.

**The repository is inspected before anything external.** Manifests, lockfiles, installed
dependencies, framework and platform configuration, and existing abstractions are read first, with
a standing rule never to recommend adding what the project already has.

**A dependency admission test.** Any candidate that adds a dependency, external service, or
self-hosted project must pass it before it can be recommended, and a failed must-have requirement
disqualifies a candidate regardless of its aggregate score. See `references/scorecard.md`.

**Evidence rules.** Never fabricate a package, API, price, license, compatibility claim, security
status, or maintenance signal. Verify consequential claims through primary sources, check dates,
and state plainly when web access is unavailable and current external facts remain unverified.

**Routing to the collection's other skills.** `research` for external evidence, `prototype` when
practical fit is the strongest uncertainty, `grilling` when unresolved requirements would change
the candidate set, `apple-docs` and `deep-docs` for whether a platform already provides the
capability, and `architecture-review` for a broad codebase-wide reuse audit. This skill keeps the
decision itself.

**Scope boundaries.** Explicit non-triggers were added for general research, architecture reviews,
codebase-wide audits, implementation, debugging, and requirements interviews, plus a rule not to
interrupt ordinary implementation for small utilities, domain-specific business logic, or choices
the user already settled.

**Safety.** The decision changes no production code, removes no behavior, purchases nothing, and
starts no migration. Replacement stays unapproved until must-have behavior, migration, rollback,
licensing, security, and exit paths are verified.
