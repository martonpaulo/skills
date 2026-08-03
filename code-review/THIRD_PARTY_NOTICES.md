# Third-Party Notices

This skill adapts workflows and concepts from the following open-source projects:

## hermes-agent (github-code-review)

- **Repository**: https://github.com/NousResearch/hermes-agent
- **Upstream path**: `skills/github/github-code-review`
- **Imported revision**: `cc4cab2f592e60a197e796506de9168f74baf3ea`
- **Imported on**: 2026-07-30
- **Last checked against upstream**: 2026-08-03
- **Author**: Hermes Agent
- **License**: MIT

### Changes
- Retained mechanics to resolve the PR, inspect metadata, inspect full diff, checkout PR locally, read complete changed files, run tests/linters, publish inline comments, submit formal GitHub review, and approve or request changes.
- Removed standalone summary comments, praise, "Looks Good", optional suggestions, nits, generic style advice, comments that merely summarize code, using COMMENT as a normal final verdict, automatically fixing findings, and asking questions before investigating the repository.

## pr-reviewer-skill

- **Repository**: https://github.com/SpillwaveSolutions/pr-reviewer-skill
- **Imported revision**: `4aa1d9b3f6c1acc3b5876c8d8faa24b93af4c8c2`
- **Imported on**: 2026-07-30
- **Last checked against upstream**: 2026-08-03
- **Author**: Claude Code / SpillwaveSolutions
- **License**: None published in the repository.

### Changes
- Adapted context collection concepts for PR metadata, complete diff, commits, comments, reviews, threads, and related issues.
- Removed `/send` workflow, two-stage manual publication ceremony, generated review workspace, praise, nits, broad suggestions, and generic human review templates.
