---
name: project-setup
description: "Settle what a project is and then make its repository match: the product definition and its non-goals, followed by identity, Git and release policy, root AGENTS.md rules, CLAUDE.md alias, the project's own skills and how they route, public documentation, licensing, ignore rules, GitHub metadata, and applicable CI or release foundations. Use when the user explicitly asks to start a new personal project, adopt this baseline in an existing repository, or refresh a repository that already carries it; do not use for ordinary implementation, a single documentation edit, specifying one feature, or artifact-path configuration alone."
disable-model-invocation: true
license: Apache-2.0
metadata:
  scope: project
  role: setup
  mutation: write
  upstream: https://github.com/product-on-purpose/pm-skills
  upstream-author: product-on-purpose
  upstream-path: skills/develop-solution-brief
  upstream-revision: 9efff804c66183cdff0abd826d90479a673b6b31
  upstream-checked: 2026-08-03
  version: pm-skills-personal.1
---

# Project Setup

Establish the repository's durable operating contract before ordinary implementation begins. Keep the setup idempotent: reuse recorded decisions, ask only for missing or explicitly reopened choices, and update existing files instead of duplicating policy.

Own the product definition and repository policy, not product implementation. Do not write application source, features, domain code, UI, or fixtures. Generating a new project's initial tree is `scaffold`'s job; invoke it from step 2 when the project is new and has no source yet, and let it keep its own refusal to run over an existing tree.

The two halves are one interview on purpose. The benefit-first description, the GitHub topics and the landing-page decision are all derived from knowing what the product is, so settling that first is what stops this run from asking the owner to invent their product's positioning while choosing a license.

Read [`assets/AGENTS.template.md`](assets/AGENTS.template.md) in full before writing project guidance. Adapt its rules to the project; never leave template placeholders in the target repository.

## Skill routing

- Use [`grilling`](../grilling/SKILL.md) to resolve the required one-time project decisions, one decision at a time. Give it the inspected project facts and the unresolved decision set; resume setup only after its completion summary.
- Run [`scaffold`](../scaffold/SKILL.md) from step 2, and only for a new project with no source yet. It keeps its own refusal to run over an existing tree.
- Run [`setup-agent-docs`](../setup-agent-docs/SKILL.md) after the root `AGENTS.md` exists.
- Read [`github-conventions`](../github-conventions/SKILL.md) before recording the branch, commit and merge rules. It owns them; this skill records them into the project's guidance and its GitHub settings.
- Point the owner at [`skill-authoring`](../skill-authoring/SKILL.md) when step 6 finds a skill the project needs and does not have. Setup records the gap; it does not write the skill.
- Use [`research`](../research/SKILL.md) only when a setup decision depends on current external evidence, standards, comparisons, or other primary-source investigation beyond the local repository.
- Use [`apple-docs`](../apple-docs/SKILL.md) when Apple platform, Xcode, signing, entitlement, notarization, privacy, or distribution configuration depends on version-specific official behavior.
- Use [`deep-docs`](../deep-docs/SKILL.md) when non-Apple CI, release, framework, SDK, CLI, database, or platform configuration depends on precise version-specific documentation.
- Let normal skill-triggering rules handle every other task. Do not maintain an inventory of available skills here or invoke a skill merely because it is installed.

## Operating modes

One skill covers three situations. Detect which one applies from the repository itself rather than
from how the request was phrased, and say which mode is running before writing anything.

- **Install** — a new project, or a repository with no agent guidance at all. Establish the identity
  and policies, initialize Git when needed, create the approved repository foundations, and
  configure the remote only after owner and visibility are explicit.
- **Adapt** — an existing project with its own conventions, and possibly its own agent guidance and
  skills. Perform a gap analysis, preserve working conventions and product code, reuse decisions
  that are already explicit, and route only missing or intentionally reopened decisions through
  `grilling`. Merge the baseline narrowly; do not reset the repository to the template.
- **Update** — a repository that already carries this baseline and wants what has changed since.
  Re-interview nothing that is already recorded. Compare the repository against the current template
  and the current conventions, and propose only the differences, each one as a separate item the
  owner can decline. A rule the owner deliberately diverged from stays diverged: when the divergence
  carries a recorded reason, leave it and say so; when it carries none, ask before restoring the
  baseline.

Update mode is a gap report first and a write second. Finding no gap is a complete run: say the
repository is current and change nothing.

In `adapt` and `update`, treat changes to an established name, identifier, license, visibility, default branch, versioning model, localization strategy, landing-page location, or distribution channel as migrations. Show affected code, metadata, documentation, automation, and external systems before changing them.

## 1. Resolve the target and inspect it

1. Resolve the exact project root. Do not run against the skills repository or another current directory by accident.
2. Inspect before writing:
   - applicable `AGENTS.md`, `CLAUDE.md`, and nested instruction files;
   - the skills, commands, and agent configuration the repository already carries, wherever the installed agents keep them;
   - Git status, current branch, remotes, and default branch;
   - README, license, attribution, changelog, ignore, environment-example, package, build, test, database, localization, CI, release, and dependency-update files;
   - GitHub repository metadata and settings when a remote exists and access is available.
3. Preserve unrelated and uncommitted user changes. If they overlap setup files, merge narrowly and show the overlap before writing.
4. If the directory is not a Git repository, include Git initialization in the proposed setup. Do not create or publish a remote until its owner and visibility are explicit.
5. Name the mode from what the inspection found: `install` when there is nothing to preserve, `update` when the recorded project policy and this baseline's rules are already there, `adapt` otherwise. When the owner asked for a different mode than the evidence supports, say which evidence disagrees and let them decide before continuing.

## 2. Define the product

Settle what the project is before deciding anything about its repository. Skip only when a current
product definition already exists and the owner is not reopening it; read it and move on.

Run this through `grilling`, one decision at a time, each with a recommendation. In an existing
project the definition is usually already implicit in the README, the code and the issues: make it
explicit and bring the contradictions you find into the interview instead of resolving them alone.

Decide and record:

- **What it is.** One sentence a stranger understands, naming the thing and the job it does.
- **Who it is for.** The specific person and the situation they are in. "Everyone" is not an
  answer; it is the absence of one.
- **The job.** What that person is trying to get done, and how they cope today without this. If the
  current workaround is fine, say so; that is a finding, not a failure.
- **What it does.** The capabilities that make it worth using, as outcomes rather than features.
- **What it will never do.** The explicit non-goals, each with its reason. This is the section that
  earns the document. A non-goal carrying no reason will be reopened in three months.
- **How you know it worked.** The observable signal that the product does its job, stated so a
  later disagreement about success has an answer. Give a baseline and a target when a number is
  genuinely available; invent neither.
- **Constraints.** What is fixed: platform, privacy, budget, offline behavior, regulation, and
  existing systems it must live with.

Keep it to one page. The constraint is what forces the prioritization, and a definition nobody
rereads protects nothing. Include only sections carrying a real decision; an empty heading is worse
than an absent one because it looks answered.

Write it to the path repository guidance configures, or `docs/product.md` when it configures none.

Two routes out, both before the definition hardens: send contested vocabulary to `domain-model` and
keep its canonical meaning, and send a capability that might not need building at all to
`build-or-reuse`. A product defined around something it should have bought is expensive to
undo.

**This is not a specification.** Individual requirements, acceptance criteria and edge cases belong
to `issue-capture`. Choose no technology, framework, architecture or data model here; if a
constraint truly forces one, record the constraint and its reason, not the choice. Write no
marketing copy: this document is read by the owner and by agents, and both need a statement that
can be checked rather than one that persuades.

**Then scaffold, when the project is new.** If the target has no source yet and the product needs
one, invoke `scaffold` now, so the rest of this setup aligns a real tree instead of an empty
directory. Skip it for an existing project, for a repository that is not a software project, and
whenever the owner declines.

## 3. Make the one-time decisions

Route the unresolved decisions through `grilling`. Accept decisions already supplied by the user, provide evidence for values discoverable from the repository, and do not ask the user factual questions that inspection can answer. Present the resulting consolidated decision summary before mutation.

Resolve and record:

1. **Project identity**
   - canonical project and public display names;
   - a short, benefit-first description;
   - repository slug and applicable public identifiers such as package, module, executable, app, or bundle identifiers;
   - repository owner and visibility when a GitHub repository must be created;
   - whether the project has or plans a landing page and, when applicable, its canonical URL, owner, repository location, and hosting boundary.
2. **Git policy**
   - `main`-only work or a branch-based workflow;
   - automatic task commits or commits only when explicitly requested;
   - automatic pushes or pushes only when explicitly requested;
   - GitHub `delete_branch_on_merge` enabled or disabled.

   Two of these are not open questions. Unless the owner states otherwise for this repository, a
   branch merges into the default branch with every commit preserved and never squashed, and a
   commit made for an issue ends its subject with `(#<number>)`. Both come from
   [`github-conventions`](../github-conventions/SKILL.md); record them in the project's guidance
   rather than reopening them, and carry any deliberate deviation with its reason.
3. **Product versioning**
   - whether the product or app has user-visible versions, distinguishing this from merely using Git and from publishing releases;
   - when versioned, the version scheme, canonical source, initial version, and whether increments are automatic or occur only during an explicitly requested release;
   - the exact automatic trigger and its changelog, commit, tag, artifact, and release boundary when version changes are automatic;
   - when unversioned, any platform-required internal build identifier and the evidence that makes it necessary.
4. **Legal and public metadata**
   - license and every value required by its official template, such as copyright holder and year;
   - a GitHub description derived from the approved benefit-first description;
   - 10 to 16 accurate, useful GitHub topics, with no filler or unsupported claims.
5. **Language and copy**
   - keep code, comments, commits, filenames, tests, configuration, and developer documentation in English;
   - choose the product copy's source language, supported locales, fallback locale, and localization strategy.
6. **Distribution**
   - whether the project will be distributed and through which channel;
   - when applicable, the signing identity and mechanism, secret store, and release-automation boundary consistent with the product-versioning policy;
   - record `Not applicable` with the reason when the project has no distribution contract.

Require the completed decision set to distinguish Git history, product version numbers, version increments, and published releases. Also distinguish a branch workflow from merely allowing an occasional exception to `main`-only work.

When automatic commits or pushes are selected, record their exact completion trigger and boundary. The product-versioning decision above owns version triggers and consequences. Reject or resolve inconsistent combinations such as automatic pushes with no authorized path to create a commit.

Treat these decisions as stable after setup. On later runs, read them from `## Project identity and policy` and ask again only when the user explicitly wants to revisit them or the value is missing. Preview migrations and downstream effects before changing an established identifier, license, visibility, branch policy, versioning model, landing-page contract, or release policy.

## 4. Show the setup plan

Before writing, show a compact preview containing:

- the mode, the resolved project root, and existing-state findings;
- the skills the repository already owns and who ends up owning each overlapping task;
- every one-time decision and any remaining unknown;
- files to create, merge, or leave unchanged;
- Git and GitHub mutations, including repository creation when applicable;
- conditional items that do not apply and why;
- the validation and the selected commit, push, and version behavior.

Do not proceed through a material unresolved conflict. A direct setup request authorizes the previewed in-repository writes, but get exact confirmation before replacing a non-symlink `CLAUDE.md`, making a repository public, changing an existing license or public identifier, overwriting remote metadata, or performing another hard-to-recover external mutation.

## 5. Establish the repository contract

Create or merge the root `AGENTS.md` from the template:

1. Preserve compatible project-specific instructions and more-specific scoped guidance.
2. Add `## Project identity and policy` once and record the resolved one-time decisions there.
3. Add the applicable baseline rules once. Consolidate duplicates under one canonical wording rather than maintaining competing copies.
4. Surface conflicts among existing guidance, the baseline, code, and approved specifications. Do not silently choose one source as universally authoritative.
5. Keep project-specific commands and stable contracts exact. Omit speculative inventories and details likely to drift.

### Record the patterns, and how a new one gets established

A project's real conventions are the ones it repeats, and most of them are never written down.
Whichever agent or person arrives next then invents a second way of doing the same thing, in good
faith, and the project now has two.

Settle two things during setup and record them with the other rules:

1. **Where the project's patterns are written.** Read the code and name the patterns it already
   repeats: how a module is laid out, how errors are surfaced, how state is owned, how a visual
   decision is declared, how something is named. Record the ones that are real and load-bearing.
   Record nothing speculative and nothing the code does not already do. If the list is long enough
   to bury the rest of the guidance, give it its own file and point to it from `AGENTS.md`.
2. **The rule that keeps the list true.** Record, in the project's own guidance, that a change
   which would break a recorded pattern or establish a new one stops and asks the owner first,
   naming the existing pattern, the proposed one, and why the existing one does not fit. Deviating
   is allowed; deviating silently is what produces two patterns.

An existing project's patterns are discovered, never imposed. Where the code contradicts itself,
record the contradiction as an open decision rather than picking a winner on the owner's behalf,
and route it through `grilling` if it is consequential.

Always make `CLAUDE.md` and `.gemini/rules/agents.md` relative symbolic links to `AGENTS.md`:

- create `CLAUDE.md -> AGENTS.md` when absent;
- create `.gemini/rules/agents.md -> ../../AGENTS.md` when absent (creating the directory if needed);
- leave the correct symlinks unchanged;
- if they are regular files or point elsewhere, preserve unique instructions, surface any agent-specific rule that would be broadened to every agent, and replace them only after the user resolves that scope and confirms the replacement;
- never maintain two independent copies of the same agent rules.

## 6. Take stock of the project's own skills

A repository often arrives with skills of its own, from another collection or written in-house, and
the owner may want more. Setup neither ignores them nor overwrites them: it decides who owns what
and writes that down, so the next agent does not run a generic workflow past a project skill that
already knew the answer.

The inventory comes from step 1 and the ownership calls are previewed with the plan, so a
consequential one goes through `grilling` alongside the other decisions rather than being settled
here on the owner's behalf. This step is where the result gets written down.

**Inventory first.** Read what the repository actually carries, wherever the installed agents keep
skills and commands, plus anything its guidance references. Read enough of each one, frontmatter and
body, to know what it claims to own and what it mutates. A filename is not a description. Add the
skills the owner says they want but has not written yet; they are part of the picture even as gaps.

**Then decide ownership**, per overlap with a skill in this collection:

- **The project skill wins.** It knows something a general skill cannot: the real build command, the
  deployment path, the house review checklist, a domain rule. Record it as the owner of that task,
  and record that the general workflow routes to it for that part instead of improvising one.
- **The general skill wins.** The project copy is an older or weaker duplicate of something this
  collection already does. Record which one is authoritative. Removing the project copy needs the
  owner's confirmed decision; what setup must not leave behind is two skills silently claiming the
  same job.
- **Split.** They overlap only partly. State the boundary in one sentence for each, naming what each
  one does not do.
- **Promote.** The project skill is genuinely general and would serve other repositories. Note it as
  a candidate for the personal collection and move on; copying it there is not this run's job.

**Then record it** in the project's guidance, as a `## Skills` section holding one line per
project-owned skill: what it owns, when it applies, and what it defers to. Add the precedence rule
once: when a project skill and a general skill both cover a task, the project skill owns the
project-specific procedure and the general skill keeps the process around it, and a task no project
skill claims follows normal skill triggering. List only skills the repository owns; an inventory of
whatever is installed on the machine is stale the day it is written.

Boundaries for this step:

- Do not copy this collection's skills into the target repository. Which skills are installed for
  which agent is the owner's local concern, and vendoring a copy creates a fork that drifts.
- Do not write a new skill here. Record the gap, and leave writing it to `skill-authoring`, which
  the owner invokes.
- Do not edit a project skill's behavior to fit the baseline. Report the conflict instead.
- In `update` mode, reread this section against what is on disk: drop entries whose skill is gone,
  and add the ones that appeared since.

## 7. Establish applicable project foundations

Create or update only what the project actually needs:

1. **README**: make it easy to scan and cover benefit, behavior, requirements, setup, usage, validation, security, privacy, limitations, landing page, and download where applicable. Use badges, real screenshots, statistics, and emoji only when they improve comprehension and can remain current.
2. **License and attribution**: add the selected `LICENSE` from an authoritative template, replacing only its designated fields such as copyright holder and year. Add `NOTICE.md` or the ecosystem's established attribution file when third-party work requires notice; do not invent attribution or remove upstream notices.
3. **Releases**: add `CHANGELOG.md` when the project will have public releases. Configure a release channel, signing, secret storage, dependency updates, CI, and release workflows only when distribution or project risk requires them and the necessary provider and platform facts are known.
4. **Repository hygiene**: update `.gitignore` for secrets, local environments, logs, caches, build output, and generated artifacts that actually exist or are expected by the chosen stack.
5. **Local configuration**: add `.env.example` only when local environment variables exist. Include every supported variable name with a safe placeholder in the same syntax as the real value; include no secrets.
6. **Data changes**: ensure the project rules require versioned migrations for every relational schema change and prohibit manual production-schema edits.

Do not create empty files or directories, placeholder workflows, fake screenshots or statistics, speculative configuration, secrets, or infrastructure for possible future use.

Do not create product source files or install a framework or dependency merely to make the repository look initialized. Align configuration to an existing or separately approved stack only when the setup requires it.

Recording a planned landing page does not authorize building or publishing it. Treat its implementation, hosting, domain purchase, DNS, analytics, and deployment as separate concerns unless the user's setup request explicitly includes them in the approved plan.

Treat license selection as an informed project decision, not legal advice. Verify uncertain compatibility against authoritative license terms and never synthesize, paraphrase, or alter the selected license's legal terms.

## 8. Configure GitHub deliberately

When a GitHub repository exists or the approved plan creates one:

1. Verify the authenticated account, target owner, remote, and visibility.
2. Show the exact description, 10 to 16 topics, applicable landing-page URL, default branch, and `delete_branch_on_merge` value before applying them.
3. Make the merge settings match the recorded merge policy, so the repository cannot offer a method the policy forbids. For the default policy that means merge commits allowed and squash merging disabled:

   ```bash
   gh api -X PATCH "repos/<owner>/<repo>" -F allow_merge_commit=true -F allow_squash_merge=false
   ```

4. Apply only the approved settings through an available GitHub integration or CLI.
5. Read the settings back and verify them. Never claim a remote setting from the proposed command alone.

Do not create issues, labels, projects, milestones, branch-protection rules, releases, or other repository ceremony unless the user requested them or a concrete project requirement makes them part of the approved setup.

## 9. Run `setup-agent-docs`

After `AGENTS.md` exists, invoke [`setup-agent-docs`](../setup-agent-docs/SKILL.md) to select and record only the artifact paths this project needs. Do not duplicate that workflow here and do not create empty artifact directories.

If `setup-agent-docs` is unavailable, report the missing dependency and leave this step incomplete rather than inventing a parallel convention.

`setup-agent-docs` must remain model-invocable because this parent workflow calls it indirectly. Treat an invocation-policy rejection as a dependency configuration defect, not as evidence that the installed skill is missing.

## 10. Validate and finish

1. Verify that `AGENTS.md` contains one project-policy section, the approved values, and no unresolved placeholders.
2. Verify `CLAUDE.md` and `.gemini/rules/agents.md` resolve to `AGENTS.md`.
3. Verify that every skill named in the recorded `## Skills` section exists on disk, and that no two entries claim the same job.
4. Validate the selected license and all Markdown links.
5. Run the smallest relevant project checks, then one broader check proportional to the setup's risk when practical.
6. Validate CI and release syntax when those files changed. Use a bounded real integration check only when local validation cannot prove the relevant contract.
7. Read GitHub metadata and settings back when changed, including the merge methods the repository now allows.
8. Inspect the final diff, remove setup-created temporary files, and preserve unrelated changes.
9. Apply the newly recorded Git policy to the setup itself:
   - commit setup files as one concern only when automatic commits were selected;
   - push only when automatic pushes were selected and the target remote is allowed;
   - do not change a version merely because setup ran.

Finish with the mode that ran, the decisions recorded, files changed, local and remote validation, conditional items skipped with reasons, Git status, commit and push result, and any remaining risk or manual secret/configuration step. In `update` mode, report the differences applied and the ones the owner declined, so the next run does not propose them again as if they were new.

Setup is complete only when a stranger could tell from the product definition whether a proposed feature belongs, every non-goal carries its reason, the repository contract is internally consistent, the alias is correct, each task has exactly one skill owning it, applicable foundations are usable rather than empty, remote settings are verified when requested, and a second run would update rather than duplicate the result.
