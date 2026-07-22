---
name: resolve-conflicts
description: Resolve an in-progress Git merge, rebase, or cherry-pick conflict by reconstructing the intent of both sides, preserving compatible behavior, and validating the resulting code and history.
---

# Resolve Conflicts

Use this skill only when a Git operation is already conflicted or the user explicitly asks to resolve a known conflict.

## Workflow

1. Inspect `git status`, the operation metadata, current branch, conflicted paths, and worktree changes. Identify whether this is a merge, rebase, cherry-pick, revert, or another operation.
2. Reconstruct both intentions from the conflicting changes, nearby code, relevant commits, call sites, tests, and documentation.
3. Resolve one coherent unit at a time. Preserve both valid intentions when compatible; never choose `ours` or `theirs` blindly.
4. When intentions conflict, explain the behavioral tradeoff. If code and history cannot determine the correct product or architectural behavior, stop for that decision.
5. Inspect the resolved diff and run the smallest relevant tests first, then broader checks appropriate to the affected behavior.
6. Remove conflict markers and confirm the index contains only intended resolutions.

## Operation safety

Aborting is appropriate when continuing risks data loss, produces invalid history, or lacks a required decision. Explain what an abort would preserve before performing it.

Do not continue the operation, create a commit, push, force-push, or rewrite remote history unless the user's requested scope includes that action. If the user requested complete merge or rebase resolution, continue after tests pass and repeat the workflow for any later conflict. Force-pushing always requires explicit authorization.

## Completion

Report the operation, conflicts resolved, intent preserved, tests and results, final diff or status, and whether the operation remains paused or was explicitly completed.
