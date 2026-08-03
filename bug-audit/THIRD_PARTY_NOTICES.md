# Third-party notices

## codexstar69/bug-hunter

- **Upstream repository:** https://github.com/codexstar69/bug-hunter
- **Reviewed revision:** `8dedbbb10e93a3465e4549778587a4c40d0e673f`
- **Upstream version:** `3.1.0`
- **Last checked against upstream:** 2026-08-03
- **Original author:** codexstar69
- **License:** MIT, full text in `LICENSE`, preserved unchanged.

### What was adapted

The personalized skill keeps the useful adversarial shape: reconnaissance, behavioral hypothesis generation, a skeptic pass that searches for counterevidence, a final evidence threshold, concrete runtime triggers, coverage accounting, safe documentation verification, and separate treatment of security reachability and exploitability.

### What changed

- The default and only mode is audit-only. It never fixes code, generates fix plans, creates branches, commits, stashes, worktrees, or project artifacts.
- A single agent can execute the complete workflow. Subagents are optional only when explicitly requested and available.
- Functional, logic, runtime, concurrency, integrity, contract, and security lenses share one evidence contract.
- Failed verification downgrades a candidate instead of accepting it by default.
- Temporary reproduction work is isolated outside the repository and removed before completion.

### What was removed

The upstream Node.js orchestration package, schemas, prompts, role skills, mode files, `.bug-hunter/` state, dependency scanner, threat-model generator, report renderer, Figma-unrelated assets, CI/release files, auto-fix/fixer pipeline, worktree and lock management, background loops, vendor-specific dispatch, and planted test fixture are not vendored.

The upstream test suite was executed at the reviewed revision: 112 of 113 tests passed. The failing test expected README wording that was absent (`README documents the integrated enterprise security pack flows`). No upstream scripts are shipped or documented as available in this adaptation.
