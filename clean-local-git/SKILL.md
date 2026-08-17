---
name: clean-local-git
description: Consolidate one repository's local Git state by auditing every local branch, linked worktree, stash, tracked change, untracked path, ignored path, and live remote counterpart before cleanup. Stop with a short plain-language decision table when anything exists only locally; otherwise remove only proven-redundant local branches and clean linked worktrees, fast-forward the confirmed default branch, and finish there. Use only when the user explicitly asks to clean local branches or worktrees, remove local-only Git state, or return a repository to its remote-backed default branch. Do not use for finishing one active feature branch, resolving conflicts, deleting remote branches, ordinary pull requests, or general disk cleanup.
disable-model-invocation: true
metadata:
  scope: project
  role: workflow
  mutation: write
---

# Clean Local Git

Reduce one repository to local branches that still have a live remote counterpart, one primary
worktree on the confirmed target branch, and no unreviewed local work. Preserve first; clean only
after the evidence is complete.

## Safety boundaries

- Treat the user's explicit invocation as permission for the safe cleanup path only. It does not
  authorize discarding work, force deletion, remote-branch deletion, or rewriting history.
- Inventory every worktree before changing any branch or worktree. If anything needs a decision,
  make no cleanup changes at all; return one complete decision report and stop.
- Preserve ignored files. Inspect only their paths, counts, sizes when useful, and matching ignore
  rules; never read their contents. An ignored path inside a linked worktree blocks its removal
  until the user chooses a preservation destination.
- Treat tracked edits, staged edits, untracked paths, stashes, detached commits, and commits not
  reachable from a live remote branch as local work. Never assume they are disposable because a
  branch looks old, a pull request was merged, or a worktree is clean.
- Never use `git clean`, `git reset --hard`, `git checkout -- .`, `git restore .`,
  `git worktree remove --force`, `git branch -D`, force-push, or remote-branch deletion in the safe
  path. A later explicit decision may authorize selected file removal or force-deleting a named,
  proven patch-equivalent branch, but not a broad destructive command.
- Never remove the primary worktree. Do not unlock a locked worktree or remove a worktree with an
  initialized submodule without a separate explicit decision.
- Do not pull, switch, or delete while a merge, rebase, cherry-pick, revert, bisect, or sequencer
  operation is active. Report the operation and stop.
- Do not assume `origin` or `main`. Use the user-specified target when present; otherwise resolve
  the remote's symbolic `HEAD`. State the chosen remote and target before cleanup.
- Stop if the relevant remote cannot be queried or fetched. Stale remote-tracking refs are not
  proof that local work is safely published or incorporated.

## 1. Establish the repository and target

Read the applicable repository instructions. Confirm this is a non-bare repository, identify the
common Git directory and primary worktree, and record the current path and branch before changing
directories.

Resolve the target branch and its remote without guessing:

1. Honor an explicit user-supplied target and remote.
2. Otherwise select the sole configured remote, or a remote identified as authoritative by the
   repository's instructions or the target branch's existing upstream.
3. Query that remote's symbolic `HEAD` and verify the reported branch exists remotely.
4. If several remotes could be authoritative, stop and ask which one owns the target.

If the user explicitly requested `main` and it does not exist on the chosen remote, stop rather
than silently substituting another branch.

## 2. Capture the complete local snapshot

Use machine-readable, pathname-safe output where Git provides it. At minimum collect:

```bash
git worktree list --porcelain -z
git for-each-ref refs/heads --format='%(refname)%00%(objectname)%00%(upstream)%00%(upstream:track)%00%(worktreepath)%00'
git stash list --format='%gd%x00%H%x00%gs'
git status --porcelain=v2 --branch -z --untracked-files=all
git ls-files --others --ignored --exclude-standard --directory -z
```

Run the status and ignored-path checks separately in every worktree with `git -C <path>`. Also
record detached, locked, prunable, missing, and bare annotations from the worktree inventory.
Inspect submodule state when `.gitmodules` exists.

For tracked and staged changes, inspect `git diff` and `git diff --cached` plus enough surrounding
code to explain the behavior. Inspect safe untracked text files when needed. Do not open likely
secret material such as `.env`, credentials, keys, tokens, or ignored content; name the path and
describe it only as sensitive local material.

## 3. Refresh and map live remote state

Snapshot local state before fetching, then query every relevant remote's live heads. Inspect each
remote's fetch refspec before pruning. Use `git fetch --prune <remote>` only when its destinations
stay inside `refs/remotes/<remote>/`; otherwise fetch without pruning and report the custom
refspec. Never use `--prune-tags`.

After fetching, map each local branch to:

- a live same-name or configured remote branch, if one exists;
- commits reachable from any live remote branch;
- commits reachable from the target branch by ancestry;
- commits that are not ancestors but have equivalent patches in the target branch.

Use several signals rather than one shortcut:

```bash
git rev-list --left-right --count <target-remote-ref>...<local-branch>
git log --cherry-pick --left-right --no-merges --oneline <target-remote-ref>...<local-branch>
git cherry -v <target-remote-ref> <local-branch>
git diff --stat <target-remote-ref>...<local-branch>
```

Read each unique commit's message and diff before summarizing its purpose. `git cherry` can detect
many cherry-picked, rebased, or squashed patches, but it excludes merge commits; treat merge-only
or otherwise ambiguous history as requiring a decision.

Classify a branch as safely redundant only when its name has no live remote counterpart and all of
its work is already reachable from a live remote branch. Prefer the stronger ancestry proof that
allows `git branch -d`. Patch equivalence without ancestry is evidence of incorporation, but it
still requires an explicit named confirmation before force-deleting the branch.

## 4. Apply the all-or-nothing decision gate

Stop before any cleanup when at least one of these exists anywhere:

- staged or unstaged tracked changes;
- untracked paths;
- ignored paths in a linked worktree that would be removed;
- any stash;
- a local commit not reachable from a live remote branch;
- ambiguous or patch-equivalent-only history that would require force deletion;
- a detached HEAD whose commit is not safely preserved remotely;
- a locked, missing, externally managed, or submodule-bearing worktree that needs intervention;
- local divergence on the target branch.

Account for every affected path and commit, then explain related files as one logical change. Do
not make the report longer by repeating the same explanation for every file.

Return one sentence with the counts, followed by one compact table in the user's language:

| Location | Local work | What it does | Decision |
| --- | --- | --- | --- |
| Branch, worktree, stash, or grouped paths | Plain state and count | One short behavioral explanation | `Include`, `keep`, or `discard` choices that actually apply |

Keep every path visible in its logical row. Collapse the contents of an ignored or generated
directory to the directory path and item count because its contents are intentionally not read.
Avoid raw diffs, command transcripts, unexplained Git terms, severity columns, and repeated
summaries. Translate the headings and choices into the user's language.

End with one direct question asking for the decisions. Do not decide usefulness on the user's
behalf. After the user acts or authorizes selected actions, start the inventory again from step 1;
never continue from a stale snapshot.

## 5. Execute the safe cleanup path

Proceed automatically only when the decision gate is empty.

1. Move to the primary worktree so no command runs from a path that may be removed.
2. Remove each clean linked worktree normally. Preserve its branch when that branch has a live
   remote counterpart. Stop on any refusal; never retry with `--force`.
3. Run `git worktree prune --dry-run --verbose`, inspect the result, then prune only stale
   administrative records whose paths are already absent and are not locked.
4. Delete local-only branches only with `git branch -d`, after rechecking their exact tip SHA and
   ancestry. Keep all local branches that still have a live remote counterpart.
5. If the target branch does not exist locally, create it from the verified remote-tracking ref.
   Otherwise switch the primary worktree to it without discarding files.
6. Update the target with `git pull --ff-only <remote> <target>`. If it cannot fast-forward, stop;
   do not merge, rebase, or reset as a fallback.

Do not create local copies of every remote branch. "Keep what also exists remotely" means preserve
existing remote-backed local branches, not multiply local branches.

## 6. Verify and report

Re-run the worktree, branch, stash, status, ignored-path, and remote-reachability checks. Verify:

- the primary worktree is on the target branch;
- the target and its remote have zero ahead/behind divergence;
- every remaining local branch has a live remote counterpart;
- no linked worktree expected to be removed remains registered;
- every ignored path in a retained worktree still exists;
- no stash, file, branch, worktree, remote branch, or tag outside the approved scope changed.

Keep the completion report short. Start with one sentence, then use this table in the user's
language:

| Item | Why it was safe | Action |
| --- | --- | --- |
| Branch or worktree | Remote or ancestry proof in plain language | Removed, preserved, or synchronized |

Finish with one line naming the current branch, remote synchronization result, and preserved local
content. Omit the table when no cleanup action was needed. Never include command logs unless a
failure needs the exact error.
