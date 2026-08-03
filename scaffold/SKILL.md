---
name: scaffold
description: Generate the initial source tree for a brand-new project from an established scaffolder, choosing the stack with the owner and leaving the repository ready for project-setup. Use only when a new project has no source code yet and the owner asked to start one. Never for an existing codebase, for adding a framework or dependency to a project that already runs, or for restructuring what is already there.
argument-hint: "[project directory]"
disable-model-invocation: true
metadata:
  scope: project
  role: setup
  mutation: write
---

# Scaffold

Create the initial source tree for a new project by running an established scaffolder, so the
repository starts from a maintained baseline instead of files invented one at a time.

This runs before `project-setup`, which then aligns the generated repository with the owner's
identity, policy, licensing, and documentation. Keeping them separate is deliberate:
`project-setup` owns policy and explicitly refuses to scaffold, so that a setup run against a
real codebase can never inject source files into it.

## Refuse when it is not a new project

Stop and say so when the target directory already contains source code, a lockfile, a manifest
with real dependencies, or commits beyond an initial empty one. A scaffolder overwrites, and this
skill exists only for an empty start.

Adding a framework, a dependency, or a new package to a project that already runs is ordinary
implementation work. Route it to `dont-reinvent-the-wheel` for the decision and then to normal
implementation. Do not scaffold over a live tree.

## Workflow

1. Resolve the exact target directory and confirm it is empty or holds only a fresh Git
   repository, a README, or a license. Show what is there before proceeding.
2. Establish what is being built from `project-setup` when it has run, or from the owner
   directly. The product decides the stack; the stack never decides the product.
3. Choose the scaffolder. See [Choosing a scaffolder](#choosing-a-scaffolder). State which one and
   why, and accept a different answer from the owner without argument.
4. Resolve the stack choices through `grilling`, one decision at a time. Prefer the scaffolder's
   own defaults for anything the owner has no opinion on, and say that the default was taken.
5. Show the exact command before running it, including every flag and the directory it writes to.
   Get confirmation. This step downloads and executes third-party code, so it is never implicit.
6. Run it. Do not answer its interactive prompts from a guess; drive it with explicit flags decided
   in step 4, so the run is reproducible and visible.
7. Verify the result actually works: install dependencies, then run the project's own build, type
   check, and test commands as generated. Report exactly what ran and what it printed. A scaffold
   that has not been executed once is not a working baseline.
8. Report the tree, the commands available, and what `project-setup` still has to decide.
   Do not commit unless the owner asks; the repository has no commit policy yet, because that is
   `project-setup`'s job.

## Choosing a scaffolder

Use the tool the ecosystem already maintains, and prefer the one closest to the framework's own
conventions.

For a **TypeScript full-stack web project**, use
[Better-T-Stack](https://better-t-stack.dev), an interactive scaffolder for end-to-end type-safe
TypeScript projects:

```bash
npm create better-t-stack@latest <name>
```

`pnpm`, `yarn`, and `bun` expose the same command through their own `create`. Drive it with
explicit flags rather than prompts once the choices are settled:

```bash
npm create better-t-stack@latest <name> \
  --frontend tanstack-router \
  --backend hono \
  --database sqlite \
  --orm drizzle
```

Documented options at the time of writing: `--frontend` (tanstack-router, react-router,
tanstack-start, next, nuxt, svelte, solid, astro, native variants, none), `--backend` (hono,
express, fastify, elysia, convex, self, none), `--database` (sqlite, postgres, mysql, mongodb,
none), `--orm` (drizzle, prisma, mongoose, none), `--auth` (better-auth, clerk, none), and
`--addons`. Verify the current set with the tool's own help rather than trusting this list; it
moves. `--yes` accepts every default without prompting.

It is TypeScript-oriented. A plain JavaScript project, a single script, or a library with no web
surface is not its case.

For anything else, use that ecosystem's established scaffolder, such as the framework's own
`create` command or language-native project tooling. When no maintained scaffolder fits, say so
and create the minimum by hand: a manifest, an entry point, and the project's test and build
commands. Nothing speculative.

A scaffolder is an accelerator, never a requirement. Starting by hand is always allowed, and is
the right answer when the generated baseline would carry far more than the project needs.

## Safety

Show the command before running it and never run a scaffolder the owner has not confirmed. Do not
pipe a remote script into a shell. Do not add a dependency, integration, or paid service the owner
did not choose, and do not accept an interactive prompt on their behalf when it selects a hosted
service or an account.

Do not create the GitHub repository, set a license, write agent guidance, or configure CI. Every
one of those belongs to `project-setup`, which runs next.

Generated code is a starting point, not a contract. Do not treat the scaffolder's conventions as
rules this repository must follow forever; `project-setup` and the repository's own guidance
decide that.

## Completion

The scaffold is complete when the target was verified empty beforehand, the exact command was
shown and confirmed, the generated project installs and passes its own checks with the output
reported, nothing beyond the chosen stack was added, and the next step is stated as
`project-setup`.
