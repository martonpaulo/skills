# Project Working Agreements

## Project identity and policy

- Project name: `{{PROJECT_NAME}}`
- Public name: `{{PUBLIC_NAME}}`
- Benefit-first description: {{BENEFIT_FIRST_DESCRIPTION}}
- Repository: `{{REPOSITORY_OWNER}}/{{REPOSITORY_SLUG}}` ({{VISIBILITY}})
- Public identifiers: {{PUBLIC_IDENTIFIERS}}
- Landing page: {{LANDING_PAGE_POLICY}}
- License: `{{LICENSE}}`
- Copyright: {{COPYRIGHT_YEAR}} {{COPYRIGHT_HOLDER}}
- Development language: English.
- Product copy: {{COPY_LANGUAGE_AND_LOCALIZATION_STRATEGY}}
- Branch policy: {{BRANCH_POLICY}}
- Commit policy: {{COMMIT_POLICY}}
- Push policy: {{PUSH_POLICY}}
- Product versioning: {{PRODUCT_VERSIONING_POLICY}}
- Merge policy: merge commits only, every commit of the branch preserved. Never squash.
- Commit subject: a commit made for an issue ends with `(#<issue number>)`.
- Delete branches after merge: {{DELETE_BRANCH_ON_MERGE}}
- Release, signing, and secret-storage policy: {{RELEASE_POLICY_OR_NOT_APPLICABLE}}

Treat these values as stable project decisions. Change an established identifier, license, visibility, branch policy, versioning model, localization strategy, landing-page contract, or release policy only through an explicit task that describes the migration and downstream effects.

## Instruction hierarchy and sources of truth

- Follow the direct task, the most specific applicable scoped instructions, this root file, and then general working agreements, in that order.
- Read applicable instructions before changing files.
- Code is evidence of current behavior. `AGENTS.md` is normative for process. An approved specification is normative for desired behavior. Expose divergence among them; do not silently resolve every conflict in favor of one source.
- Keep one canonical source for each rule. Secondary documents should summarize or link to it instead of restating it.
- Do not turn analysis, research, or a read-only audit into implementation without authorization.
- Be direct and evidence-based. State assumptions, uncertainty, risks, tradeoffs, and blockers.
- Ask only when a material decision cannot be discovered safely. Prefer explicit, reversible assumptions when enough context exists.
- Give concise progress updates during long-running work.

## Skills

Skills this repository owns. Keep one line each: what it owns, when it applies, what it defers to.
Remove an entry when its skill is gone; add one when a new skill is written.

- `{{PROJECT_SKILL_NAME}}` — {{WHAT_IT_OWNS_AND_WHEN}}. Defers to: {{WHAT_IT_DEFERS_TO}}.

Precedence: when a project skill and a general one both cover a task, the project skill owns the
project-specific procedure and the general skill keeps the process around it. A task no project
skill claims follows normal skill triggering. Two skills claiming the same job is a defect to
resolve, not a preference to exercise per task.

Delete this section when the repository owns no skills.

## Before editing

1. Check applicable instructions, Git status, and the current branch.
2. Search for the behavior, callers, tests, contracts, and nearby patterns before adding anything.
3. Read only the files and chunks required to understand the affected behavior.
4. Distinguish verified facts, reasonable inferences, and unknowns.
5. Define the source of truth and ownership before changing data or state.
6. Make a short plan only for complex, risky, ambiguous, or multi-file work.

## Scope, reuse, and implementation

- Keep changes scoped to the requested result. Do not mix unrelated cleanup, redesign, dependency updates, broad refactors, or future work.
- Preserve behavior outside the task and preserve unrelated or uncommitted user changes.
- Search for existing components, services, types, helpers, tokens, configuration, tests, and platform capabilities before creating new ones.
- Follow the patterns this project already repeats. When a change would break a recorded pattern or establish a new one, stop and ask first, naming the existing pattern, the proposed one, and why the existing one does not fit. Deviating is allowed; deviating silently is not.
- Prefer the smallest correct, readable, reversible, and low-operational-cost solution.
- Maintain one owner and one source of truth for each business rule, state, mapping, default, and copy value.
- Keep business rules out of presentation, transport, CLI, and external-adapter layers when a domain owner exists.
- Derive values instead of storing synchronized copies. Model invalid states explicitly.
- Do not add dependencies, services, layers, caches, observers, timers, polling, background jobs, or infrastructure without a current requirement and a clear owner.
- For large changes, use reviewable, executable increments and patches small enough to diagnose failures. Do not fragment one coherent concern mechanically.
- Implement relevant errors, states, accessibility, and tests with the behavior rather than as unrelated follow-up work.

## Data, security, and destructive operations

- Distinguish canonical data, reconstructible cache, transient state, local preferences, durable intent, and operating-system artifacts.
- Persist or synchronize only data that must survive or cross devices. Never turn a cache or mirror into an independent source of truth.
- Use stable application-owned identifiers. Validate data at input and persistence boundaries.
- Make every relational schema change through an explicit, deterministic, tested, versioned migration. Never edit a production schema manually.
- Use transactions or atomic writes when partial failure could leave inconsistent state. Preserve unrelated fields during external updates.
- Request only necessary permissions, fields, and scopes. Keep credentials, tokens, private keys, signing material, personal data, and sensitive payloads out of the repository and logs.
- Use structured subprocess arguments and validate destinations, redirects, and untrusted inputs.
- Resolve an exact target before deletion, overwrite, interruption, or another hard-to-recover action. A clear request authorizes its exact resolved operation; ask again when the target is ambiguous, loss is difficult to recover, or effects exceed the named scope.
- Prefer recoverable deletion where practical. Never force-push or perform broad cleanup without explicit authorization.

## Product interface and accessibility

- Prefer native platform components and established product patterns. Custom UI must provide clear product or domain value.
- Define layout, hierarchy, controls, loading, content, empty, error, retry, disabled, cancellation, and destructive states when applicable.
- Include keyboard navigation, focus, screen-reader labels, scalable text, contrast, safe areas, reduced motion, and non-color status cues in the same change.
- Keep visible copy centralized, localized, and consistent with the product language strategy.
- Keep expensive work out of render paths, hot loops, and latency-sensitive request paths. Prefer event-driven, on-demand, bounded, incremental, lazy, paginated, and cancelable work.
- Measure before claiming a performance problem and optimize measured user-visible bottlenecks.

## Code, comments, and documentation

- Write code, comments, commits, filenames, tests, configuration, and developer documentation in English. Product copy follows the recorded localization strategy.
- Follow the existing formatter, linter, naming, file layout, and architectural conventions.
- Prefer clear types, explicit ownership, and simple control flow over cleverness.
- Put comments next to non-obvious constraints. Explain intent, provenance, or a subtle external rule, not mechanics.
- Link official documentation in a code comment when an external rule or workaround must remain visible to prevent a future regression.
- Durable documentation describes responsibilities, contracts, invariants, commands, and decisions. Audits cite exact evidence. Manuals use exact filenames only when users must act on them and the names are stable contracts.
- Update the smallest canonical documentation section when a durable contract changes. Do not create empty documentation for possible future use.
- Keep the README easy to scan. Cover benefit, behavior, requirements, setup, usage, validation, security, privacy, limitations, landing page, and download where applicable.
- Use badges, real screenshots, statistics, and emoji only when they improve comprehension and can remain current.
- Preserve third-party licenses, copyright, attribution, and notices. Maintain `NOTICE.md` or the established attribution file when required.
- Maintain `CHANGELOG.md` when the project has public releases.

## Configuration and repository hygiene

- Ignore secrets, local environments, logs, caches, build output, and generated artifacts appropriate to the actual stack.
- When local environment variables exist, maintain `.env.example` with every supported name and a safe placeholder in the same syntax as the real value.
- Configure dependency updates, CI, release workflows, a release channel, signing, and secure secret storage when distribution or project risk requires them. Do not add placeholder automation.
- Keep secrets in the platform or provider's secure store, never in versioned files.

## Tests and validation

- Add or update focused tests for changed behavior, regressions, persistence, migrations, validation, security, and critical accessibility.
- Test observable contracts at stable seams; avoid tests that only mirror implementation details or framework behavior.
- Run the smallest relevant check during iteration. Inspect the first useful failure and make a relevant change before rerunning it.
- Once stable, run one broader validation proportional to risk. Use a bounded real integration only when mocks and local tests cannot prove the relevant contract.
- Never claim a check passed unless it ran successfully. Report exact skips, blockers, residual risk, and manual gaps.

## Artifacts and processes

- Temporary is the default; retention is an explicit repository exception.
- Remove only temporary files created by the current task when they are no longer needed. Preserve deliverables, next-phase inputs, failure evidence, and anything protected by repository policy.
- Never delete pre-existing user artifacts, fixtures, baselines, or logs merely because they look temporary.
- Use the repository's established artifact location and never version secrets, caches, local logs, coverage, or build output without an explicit requirement.
- Stop servers, watchers, browsers, simulators, containers, workers, and other processes started by the task. Do not stop the user's pre-existing processes.

## Git and releases

- Follow the recorded branch, commit, push, and version policies.
- Check status and branch before editing and before the final report. Work only on task files and leave unrelated changes untouched.
- Use Conventional Commits in English. Make one commit per concern: a small task usually has one; a large task may have several independent concerns. Do not split mechanically or combine unrelated changes.
- End a commit subject with its issue number when the commit belongs to one: `feat: add the export button (#54)`. Use the issue number, never the pull request's, and leave the suffix off when there is no issue.
- Merge a branch with all of its commits: `gh pr merge <number> --merge --delete-branch`. Never squash. Squashing discards the one-commit-per-concern history and every issue reference but one.
- Inspect the diff before committing. Never commit secrets, caches, generated logs, temporary artifacts, or unrelated formatting churn.
- Never force-push. If commit or push fails, report the exact failure without claiming success.
- For a release, update the version and changelog, tag the published version, build from clean validated state, sign and verify applicable artifacts, validate install and update paths, then publish and verify download surfaces.
- Do not publish a release or change a version unless the task and recorded policy authorize it.

## Completion report

Lead with the outcome and include:

- what changed and why;
- files touched;
- validation commands and actual results;
- warnings, failures, skips, manual gaps, and remaining risks;
- temporary artifacts kept or removed;
- commit, branch, and push status when applicable;
- final worktree status and unrelated dirty files left untouched.
