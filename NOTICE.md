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
| [felinto-dev/felinto-skills](https://github.com/felinto-dev/felinto-skills) | felinto-dev | **none published** | `dont-reinvent-the-wheel`, `grey-market` |

Where upstream code is vendored, that skill's directory keeps the upstream `LICENSE` file
unchanged, alongside a `THIRD_PARTY_NOTICES.md` recording the imported revision and exactly what
was changed.

## Unlicensed upstream

`dont-reinvent-the-wheel` and `grey-market` derive from a repository that publishes no license.
The MIT grant in `LICENSE` **does not extend to the upstream material in those two
directories**. That permission is not mine to give. They are kept here for personal use, with
attribution to the original author. Contact felinto-dev before reusing them.
