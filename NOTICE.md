# Notice

## Scope of the MIT license

The [MIT license](LICENSE) in this repository covers the **original work in this collection**:
the personalized skill content, the documentation, the reference files, and the configuration
written for it.

It does not, and cannot, relicense third-party work that this repository vendors or adapts.

## Third-party work

| Upstream | Author | Upstream license | Applies to |
| --- | --- | --- | --- |
| [mattpocock/skills](https://github.com/mattpocock/skills) | Matt Pocock | MIT | `architecture-review`, `debug`, `domain-model`, `grill`, `grill-and-document`, `grilling`, `handoff`, `module-design`, `prototype`, `research`, `resolve-conflicts`, `setup-agent-docs`, `skill-authoring` |
| [Ahrentlov/apple-docs-skill](https://github.com/Ahrentlov/apple-docs-skill) | Patrick Ahrentløv | MIT | `apple-docs` (vendored), `deep-docs` (adapted architecture) |
| [Ahrentlov/appledeepdoc-mcp](https://github.com/Ahrentlov/appledeepdoc-mcp) | Patrick Ahrentløv | MIT | `deep-docs` (architecture reference only) |
| [gccszs/disk-cleaner](https://github.com/gccszs/disk-cleaner) | Disk Cleaner Contributors | MIT | `disk-cleaner` (vendored) |
| [upstash/context7](https://github.com/upstash/context7) | Upstash, Inc. | MIT | `context7` (skill prose rewritten; the CLI itself is not vendored) |
| [felinto-dev/felinto-skills](https://github.com/felinto-dev/felinto-skills) | felinto-dev | **none published** | `dont-reinvent-the-wheel`, `grey-market` |
| [jakubkrehel/skills](https://github.com/jakubkrehel/skills) | Jakub Krehel | MIT | `product-audit` (adapted interface-review orchestration and criteria) |
| [content-designer/ux-writing-skill](https://github.com/content-designer/ux-writing-skill) | Christopher Greer | MIT | `product-audit` (adapted UX-writing review criteria) |
| [Thecsiz/ux-critique](https://github.com/Thecsiz/ux-critique) | thecsiz | MIT and CC BY 4.0 by upstream path | `product-audit` (adapted deep-critique method; no KB or scripts vendored) |
| [codexstar69/bug-hunter](https://github.com/codexstar69/bug-hunter) | codexstar69 | MIT | `bug-hunter` (audit workflow adapted; no scripts vendored) |
| [obra/superpowers](https://github.com/obra/superpowers) | obra | **none published** | `plan-issue` (adapted planning discipline) |
| [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) | Hermes Agent | MIT | `code-review` (adapted review mechanics) |
| [SpillwaveSolutions/pr-reviewer-skill](https://github.com/SpillwaveSolutions/pr-reviewer-skill) | SpillwaveSolutions | **none published** | `code-review` (adapted context collection) |
| [martonpaulo/tabelo](https://github.com/martonpaulo/tabelo) | Marton Paulo | MIT | `implement-issue` (design input only) |
| [openclaw/openclaw](https://github.com/openclaw/openclaw) | openclaw | **none published** | `implement-issue` (design input only) |
| [github/spec-kit](https://github.com/github/spec-kit) | GitHub | MIT | `implement-issue` (design input only) |
| [github/gh-aw](https://github.com/github/gh-aw) | GitHub | MIT | `backlog-curator` (behavioral reference only) |

Where upstream code is vendored, that skill's directory keeps the upstream `LICENSE` file
unchanged, alongside a `THIRD_PARTY_NOTICES.md` recording the imported revision and exactly what
was changed.

## Unlicensed upstream

`dont-reinvent-the-wheel`, `grey-market`, `plan-issue`, `code-review`, and `implement-issue` derive partly from repositories that publish no license.
The MIT grant in `LICENSE` **does not extend to the upstream material in those
directories**. That permission is not mine to give. They are kept here for personal use, with
attribution to the original author. Contact the original authors before reusing them.
