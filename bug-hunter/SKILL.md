---
name: bug-hunter
description: Audit an existing codebase for verified functional, logic, runtime, concurrency, data-integrity, contract, and security bugs without fixing them. Use only when the user explicitly invokes $bug-hunter for adversarial bug finding in a repository, path, staged change, or branch diff. Not for ordinary code review, style issues, missing tests, speculative hardening, implementation, auto-fix, or remediation work.
argument-hint: "[path|--staged|--branch <base>]"
disable-model-invocation: true
license: MIT
metadata:
  scope: project
  role: audit
  mutation: temporary
  upstream: https://github.com/codexstar69/bug-hunter
  upstream-author: codexstar69
  upstream-revision: 8dedbbb10e93a3465e4549778587a4c40d0e673f
  upstream-checked: 2026-08-03
  version: 3.1.0-personal.1
---

# Bug Hunter

Find behavioral bugs that survive an adversarial evidence pass. Report them in the conversation; never edit production code, tests, configuration, or repository documentation.

## Resolve the target

- With a path argument, audit that file or directory. With no argument, use the current repository.
- `--staged` audits the full current contents of staged source files, using the staged diff only to select scope.
- `--branch <base>` audits source files changed from the merge base with `<base>`, while reading unchanged callers, callees, tests, and configuration when required to verify behavior.
- Apply repository guidance and exclude generated output, vendored dependencies, minified assets, and irrelevant documentation. Read tests as intent and coverage evidence; do not report test-only defects unless the test code ships in the product or the user explicitly includes test infrastructure.

If the target is too large for credible full coverage, audit complete risk-bounded slices in this order: external/trust boundaries, authorization and sensitive state, persistence and transactions, concurrency and retries, error boundaries, then remaining business logic. State the exact queue and unscanned scope; never claim full coverage from a sample.

## Workflow

1. Inspect repository guidance, worktree status, architecture, tests, recent relevant history, and the resolved target without changing anything.
2. Map entry points, trust boundaries, state transitions, data ownership, error propagation, concurrency, persistence, external integrations, and cross-module contracts. Prioritize boundary code and recent churn over generic file-by-file scanning.
3. Read [`bug-lenses.md`](references/bug-lenses.md). Generate candidates only when a concrete, reachable input or event can produce wrong runtime behavior, a security consequence, data corruption, a crash, or a contract violation.
4. Trace each candidate end to end across callers, guards, middleware, framework behavior, cleanup, transactions, and tests. Record exact locations and the smallest triggering scenario.
5. Verify any claim that depends on library, language, platform, or framework behavior. Use `apple-docs` for Apple platforms and `deep-docs` elsewhere; if authoritative behavior cannot be established, downgrade the candidate rather than guessing.
6. Run the smallest safe reproduction or existing focused test when it can execute locally without installing dependencies, contacting production, mutating repository files, or consuming real credentials or personal data. Prefer no-cache/read-only modes. If command side effects are unclear, do not run it.
7. Challenge every candidate from the strongest opposing case: impossible precondition, validation elsewhere, framework guarantee, transaction/lock, intended contract, dead code, test-only path, or environmental assumption. Re-read the code used as counterevidence.
8. Assign a verdict and severity only after the challenge. Consolidate multiple symptoms of one root cause and produce the report contract below.

Subagents, background agents, issue trackers, branches, and artifact pipelines are never required. If an independent agent is explicitly available and requested, it may perform a read-only challenge pass, but this skill retains the final evidence and coverage contract.

## Evidence threshold

- `Confirmed`: reproduced safely, or established by a deterministic end-to-end trace that includes all relevant guards and contracts.
- `High confidence`: the trace is strong but one runtime, environment, or external-system assumption remains. Keep it outside confirmed findings.
- `Manual review`: evidence conflicts or the required verification would exceed the safety boundary.
- `Dismissed`: counterevidence defeats the trigger or consequence.

Do not promote a finding because it sounds dangerous. A static pattern without reachable flow and consequence is a lead, not a bug. If a verifier or challenge pass fails, do not accept findings by default; mark the affected candidates unverified.

## Severity

- `CRITICAL`: reachable exploitation, broad authorization bypass, irreversible sensitive data loss/corruption, or failure with catastrophic impact.
- `HIGH`: breaks a core task, exposes sensitive data or privileged action, corrupts important state, or causes a frequent crash/outage path.
- `MEDIUM`: produces wrong behavior or failed recovery for a meaningful subset of valid inputs.
- `LOW`: reachable but limited-impact inconsistency or edge case.

Calibrate security severity from reachability, privileges, exploitability, and actual impact. Add CWE or CVSS only when the classification and current scoring inputs are verified; never manufacture a proof of concept or run a harmful payload.

## Report contract

1. **Scope and coverage:** target mode, files and boundaries inspected, relevant checks run, excluded/generated paths, unscanned scope, and coverage confidence.
2. **Confirmed findings:** order by severity. For each include title, category, location, runtime trigger, execution trace, observed or deterministic result, user/security impact, counteranalysis survived, confidence basis, smallest recommendation, and focused regression validation.
3. **High-confidence and manual-review candidates:** keep separate from confirmed bugs and state the exact missing evidence.
4. **Dismissed candidates:** summarize material false positives and the code or documented behavior that defeated them.
5. **Verification:** list exact commands/interactions and results, plus checks skipped for safety or unavailable state.
6. **Result:** state the number of confirmed bugs. When zero survive, say `No confirmed bugs in the inspected scope`; never translate that into proof that the codebase is bug-free.

## Safety and handoff

Temporary work is limited to a uniquely named system temporary directory, must contain no secrets or personal data, and must be removed and reported before completion. Do not create `.bug-hunter/`, modify `.gitignore`, install tools, create branches or commits, stash changes, write reports into the repository, probe production or third-party systems, use destructive or persistence-changing payloads, or bypass access controls.

Recommendations stop at remediation intent and regression coverage. If the user later selects a confirmed finding for implementation, use `debug` in a separate change task; this audit does not transition into fixing on its own.

The audit is complete when every reported bug has a reachable trigger and verified consequence, every material candidate has a verdict, coverage is honest, temporary artifacts are gone, and no repository or external state was mutated.
