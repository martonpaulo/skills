# Third-Party Notices

This skill adapts high-level workflows and SDD concepts from the following open-source projects:

## openclaw (gh-issues)
- **Repository**: https://github.com/openclaw/openclaw
- **Revision**: main (July 2026)
- **Author**: openclaw
- **License**: None published in the repository.

### Changes
- Adapted useful mechanics: resolve repository and base branch, detect branches and PRs, avoid duplicate work, create commits, push, open PR, link issues, and report publication failures.
- Removed batch issue processing, watch mode, cron mode, background workers, claim files, fixed branch names, and automatic review processing.

## spec-kit (implement)
- **Repository**: https://github.com/github/spec-kit
- **Revision**: main (July 2026)
- **Author**: GitHub
- **License**: MIT

### Changes
- Adapted SDD Implement principles: verify prerequisites, read specification and plan, respect task dependencies, validate against specification, and do not claim completion early.
- Removed `.specify/` requirements, separate `.md` file structures, extension hooks, ignore-file generation, fixed phase names, and specific command requirements.

## tabelo (implement-issue)
- **Repository**: https://github.com/martonpaulo/tabelo
- **Revision**: main (July 2026)
- **Author**: Marton Paulo
- **License**: MIT

### Changes
- Generalized principles: issue scope contract, distinguishing rules, inspecting before editing, checking dependencies from code, and routing to specialized skills.
- Removed all Tabelo-specific product rules, testing commands, hardcoded design-system paths, direct-to-main policy assumptions, and Tabelo-local skill dependencies.
