---
name: project-release
description: Cut one release of a project according to the versioning policy the repository already recorded, covering the version bump, changelog entry, tag, and publication. Use only when the user explicitly asks to release, cut a version, bump the version, or publish a build. Do not use for ordinary commits and pushes, for merging a pull request, for deciding a versioning policy that does not exist yet, or for configuring release automation.
argument-hint: "[explicit version, e.g. 1.4.0]"
disable-model-invocation: true
metadata:
  scope: project
  role: workflow
  mutation: write
---

# Release

Cut exactly one release, following the policy the repository already recorded. This skill executes
a contract; it does not invent one.

`project-setup` owns establishing the versioning policy and writes it to `## Project identity and
policy`. If no policy exists, stop and say so. Do not choose a version scheme, a canonical source,
or a release trigger on the user's behalf, and do not release a project that policy says is
unversioned.

## 1. Read the contract

Read the applicable `AGENTS.md` and locate the recorded decisions:

- whether the product has user-visible versions at all;
- the version scheme and the canonical source of the current version;
- whether increments are automatic or occur only on an explicit release request;
- the changelog, commit, tag, artifact, and published-release boundary;
- the distribution channel, signing identity, and secret store when one exists.

Read the current version from its canonical source, never from a guess or from the latest tag when
the canonical source is a manifest. When several files carry the version, list every one of them
now; they all have to move together.

Stop with an exact gap when the policy is missing, contradictory, or silent on something this
release needs. Recommend `project-setup` and do not continue.

## 2. Establish the release is safe to cut

Verify and report before proposing anything:

- the working tree is clean, or the only changes are the ones this release will make;
- the current branch is the branch the policy releases from;
- local and remote are in sync, and nothing needs rebasing;
- the project's own checks pass. Run them. A release is not the place to discover a red suite;
- the previous release's tag exists and the commit range since it is non-empty.

If the checks fail, stop and report the failures. Do not release over a red suite because the
failure looks unrelated.

## 3. Determine the version

Take an explicit version from the argument when given, and validate it against the recorded scheme
and against the current version. Reject a version that moves backwards or skips in a way the
scheme does not allow.

Without an argument, derive the increment from the commits since the previous release, using the
repository's own convention. Under Conventional Commits with semantic versioning, that is a
breaking change for major, `feat:` for minor, and `fix:` for patch. State the commits that drove
the decision and confirm the derived version before writing anything.

A version that changes a public interface, a stored data format, or a documented contract is a
breaking change regardless of the commit prefix used. Say so when the derivation and the actual
content disagree.

## 4. Show the plan

Before mutating anything, show:

- the current and proposed versions, and what drove the increment;
- every file whose version string will change;
- the changelog entry in full;
- the tag name and message;
- the commit and push actions, quoting the policy that authorizes them;
- whether a published release, artifact, or distribution step is included;
- anything the policy requires that cannot be done here, such as a secret only the user holds.

Get explicit confirmation. A request to release authorizes the local writes previewed here; it
does not by itself authorize publishing, pushing a tag, or distributing a build.

## 5. Execute

In order, stopping at the first failure:

1. Update the version in every file that carries it.
2. Write the changelog entry. Group by change type, describe user-visible effects rather than
   commit subjects, credit contributors when the project does, and link the compare range. Follow
   the existing file's format exactly; match its heading style, date format, and ordering.
3. Re-run the project's checks against the bumped state.
4. Commit as one release commit, following the repository's commit convention.
5. Tag, using the project's existing tag format. Never move or delete an existing tag.
6. Push the commit and the tag only when the policy authorizes it and the user confirmed.
7. Create the published release only when the policy includes one, with notes derived from the
   changelog entry.
8. Run the distribution step only when the policy defines one and every required credential is
   already available. Never enter, request, or store a signing secret.

## Safety

Never force-push, rewrite published history, move an existing tag, or delete a release. Never
release from a dirty tree, a red suite, or a branch the policy does not release from. Never invent
a version, a changelog entry for a change that did not happen, or a contributor's name.

If publication fails partway, report exactly which steps completed and which did not, and leave
the repository in a state the user can finish by hand. Do not retry a publication step that may
have partially succeeded without checking its actual remote state first.

When GitHub or the registry is unavailable, complete the local release, state precisely which
remote actions were not performed, and never claim a tag, release, or package was published.

## Completion

The release is complete when the version matches in every file that carries it, the changelog
describes the actual change, the tag points at the release commit, the policy's publication
boundary was honored, and the report states the version, the commit, the tag, what was published,
and anything left for the user to finish.
