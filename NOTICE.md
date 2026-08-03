# Notice

## Scope of the MIT license

The [MIT license](LICENSE) in this repository covers the **original work in this collection**:
the personalized skill content, the documentation, the reference files, and the configuration
written for it.

It does not, and cannot, relicense third-party work that this repository vendors or adapts.

## Third-party work

| Upstream | Author | Upstream license | Applies to |
| --- | --- | --- | --- |
| [mattpocock/skills](https://github.com/mattpocock/skills) | Matt Pocock | MIT | `architecture-audit`, `diagnose-bug`, `domain-model`, `grilling`, `handoff`, `module-design`, `prototype`, `research`, `resolve-conflicts`, `review-changes`, `setup-agent-docs`, `skill-authoring`, `test-design` |
| [Ahrentlov/apple-docs-skill](https://github.com/Ahrentlov/apple-docs-skill) | Patrick Ahrentløv | MIT | `apple-docs` (vendored), `deep-docs` (adapted architecture) |
| [Ahrentlov/appledeepdoc-mcp](https://github.com/Ahrentlov/appledeepdoc-mcp) | Patrick Ahrentløv | MIT | `deep-docs` (architecture reference only) |
| [gccszs/disk-cleaner](https://github.com/gccszs/disk-cleaner) | Disk Cleaner Contributors | MIT | `disk-cleaner` (vendored) |
| [upstash/context7](https://github.com/upstash/context7) | Upstash, Inc. | MIT | `context7` (skill prose rewritten; the CLI itself is not vendored) |
| [felinto-dev/felinto-skills](https://github.com/felinto-dev/felinto-skills) | felinto-dev | **none published** | `build-or-reuse`, `grey-market` |
| [jakubkrehel/skills](https://github.com/jakubkrehel/skills) | Jakub Krehel | MIT | `interface-audit` (adapted interface-review orchestration and criteria) |
| [content-designer/ux-writing-skill](https://github.com/content-designer/ux-writing-skill) | Christopher Greer | MIT | `interface-audit` (adapted UX-writing review criteria) |
| [Thecsiz/ux-critique](https://github.com/Thecsiz/ux-critique) | thecsiz | MIT and CC BY 4.0 by upstream path | `interface-audit` (adapted deep-critique method; no KB or scripts vendored) |
| [codexstar69/bug-hunter](https://github.com/codexstar69/bug-hunter) | codexstar69 | MIT | `bug-audit` (audit workflow adapted; no scripts vendored) |
| [obra/superpowers](https://github.com/obra/superpowers) | obra | **none published** | `issue-plan` (adapted planning discipline) |
| [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) | Hermes Agent | MIT | `issue-review` (adapted review mechanics) |
| [SpillwaveSolutions/pr-reviewer-skill](https://github.com/SpillwaveSolutions/pr-reviewer-skill) | SpillwaveSolutions | **none published** | `issue-review` (adapted context collection) |
| [openclaw/openclaw](https://github.com/openclaw/openclaw) | openclaw | **none published** | `issue-implement` (design input only) |
| [github/spec-kit](https://github.com/github/spec-kit) | GitHub | MIT | `issue-implement` (design input only) |
| [github/gh-aw](https://github.com/github/gh-aw) | GitHub | MIT | `project-groom` (behavioral reference only) |
| [product-on-purpose/pm-skills](https://github.com/product-on-purpose/pm-skills) | product-on-purpose | Apache-2.0 | `project-setup` (product-definition half only) |

Every skill above keeps a `THIRD_PARTY_NOTICES.md` in its own directory recording the upstream
repository, the pinned commit, the import date, the date of the last comparison against upstream,
the author, the license, and exactly what was adapted, changed, and deliberately not carried. The
same pin is mirrored in the skill's frontmatter as `upstream-revision` and `upstream-checked`.
Where upstream code is vendored, that directory also keeps the upstream `LICENSE` file unchanged.

A branch name is never recorded as a revision. See [Upstream provenance](README.md#upstream-provenance).

## Unlicensed upstream

`issue-review`, `build-or-reuse`, `grey-market`, `issue-implement`, and `issue-plan` derive
partly from repositories that publish no license.

The MIT grant in `LICENSE` **does not extend to the upstream material in those directories**. That
permission is not mine to give. They are kept here for personal use, with attribution to the
original author. Contact the original authors before reusing them.

An absent license is not an obstacle to adapting the work, and several of these are by people I
know. It only means the permission to relicense is theirs, so each of those skills states the
situation plainly in its own `THIRD_PARTY_NOTICES.md` rather than being quietly folded into the
MIT grant.
