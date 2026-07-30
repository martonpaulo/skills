# Third-Party Notices

This skill adapts workflows and concepts from the following open-source projects:

## hermes-agent (github-code-review)

- **Repository**: https://github.com/NousResearch/hermes-agent
- **Revision**: main (July 2026)
- **Author**: Hermes Agent
- **License**: MIT

### Changes
- Retained mechanics to resolve the PR, inspect metadata, inspect full diff, checkout PR locally, read complete changed files, run tests/linters, publish inline comments, submit formal GitHub review, and approve or request changes.
- Removed standalone summary comments, praise, "Looks Good", optional suggestions, nits, generic style advice, comments that merely summarize code, using COMMENT as a normal final verdict, automatically fixing findings, and asking questions before investigating the repository.

## pr-reviewer-skill

- **Repository**: https://github.com/SpillwaveSolutions/pr-reviewer-skill
- **Revision**: main (July 2026)
- **Author**: Claude Code / SpillwaveSolutions
- **License**: None published in the repository.

### Changes
- Adapted context collection concepts for PR metadata, complete diff, commits, comments, reviews, threads, and related issues.
- Removed `/send` workflow, two-stage manual publication ceremony, generated review workspace, praise, nits, broad suggestions, and generic human review templates.
