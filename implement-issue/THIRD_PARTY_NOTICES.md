# Third-Party Notices

This skill adapts high-level workflows and SDD concepts from the following open-source projects:

## openclaw (gh-issues)
- **Repository**: https://github.com/openclaw/openclaw
- **Imported revision**: `db4ad84d7f0b22664f65a2e98a73a8cdd599f7b7`
- **Imported on**: 2026-07-30
- **Last checked against upstream**: 2026-08-03
- **Author**: openclaw
- **License**: None published in the repository.

### Changes
- Adapted useful mechanics: resolve repository and base branch, detect branches and PRs, avoid duplicate work, create commits, push, open PR, link issues, and report publication failures.
- Removed batch issue processing, watch mode, cron mode, background workers, claim files, fixed branch names, and automatic review processing.

## spec-kit (implement)
- **Repository**: https://github.com/github/spec-kit
- **Imported revision**: `5e2f9bcd9ba92702b0bff34ecdaa71283e1d1e42`
- **Imported on**: 2026-07-30
- **Last checked against upstream**: 2026-08-03
- **Author**: GitHub
- **License**: MIT

### Changes
- Adapted SDD Implement principles: verify prerequisites, read specification and plan, respect task dependencies, validate against specification, and do not claim completion early.
- Removed `.specify/` requirements, separate `.md` file structures, extension hooks, ignore-file generation, fixed phase names, and specific command requirements.

## tabelo (implement-issue)
- **Repository**: https://github.com/martonpaulo/tabelo
- **Imported revision**: `196bab5a1fe63616a429ac7ad3147554b9b19995`
- **Imported on**: 2026-07-30
- **Last checked against upstream**: 2026-08-03
- **Author**: Marton Paulo
- **License**: MIT

### Changes
- Generalized principles: issue scope contract, distinguishing rules, inspecting before editing, checking dependencies from code, and routing to specialized skills.
- Removed all Tabelo-specific product rules, testing commands, hardcoded design-system paths, direct-to-main policy assumptions, and Tabelo-local skill dependencies.
