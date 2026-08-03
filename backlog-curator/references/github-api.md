# GitHub API commands

Every command below was verified against `gh` and the GitHub API. Reach the API through the
available native GitHub integration or `gh api`; they are transports for the same endpoints.

## Read the backlog

```bash
gh issue list --state open --limit 200 \
  --json number,title,labels,milestone,state,createdAt,updatedAt,author,assignees
```

Then read each candidate in full. The single most useful call, because it returns the
relationships GitHub already tracks instead of making you infer them from prose:

```bash
gh issue view <number> --json number,title,body,state,stateReason,labels,milestone,comments,\
blockedBy,blocking,parent,subIssues,subIssuesSummary,closedByPullRequestsReferences,url
```

- `blockedBy` and `blocking` are GitHub's own issue dependencies. **These are the source of truth
  for the dependency graph.** Read them before parsing any sentence in a body that claims a
  blocking relationship.
- `parent`, `subIssues`, and `subIssuesSummary` give the sub-issue hierarchy, which is
  containment, not blocking order. Do not draw it as a blocking edge.
- `closedByPullRequestsReferences` is evidence that an issue is already implemented, which is one
  of the few grounds for closing it as obsolete.

Cross-references and prior closures come from the timeline:

```bash
gh api "repos/<owner>/<repo>/issues/<number>/timeline" \
  --jq '[.[] | select(.event=="cross-referenced" or .event=="closed" or .event=="reopened")]'
```

## Apply relationships

Sub-issues, when the relationship is genuinely containment:

```bash
gh api --method POST repos/<owner>/<repo>/issues/<parent>/sub_issues -F sub_issue_id=<child_id>
gh api repos/<owner>/<repo>/issues/<number>/sub_issues
```

`sub_issue_id` is the issue's internal `id`, not its number. Read it with
`gh issue view <number> --json id,number`.

## Apply metadata

```bash
gh issue edit <number> --add-label "priority:P1" --remove-label "priority:P2"
gh issue edit <number> --milestone "<title>"
gh issue edit <number> --body-file - <<'MD'
...full replacement body...
MD
```

`gh issue edit --body-file -` replaces the whole body, so refetch immediately before writing and
merge by hand. There is no partial-body edit.

Closing a duplicate keeps the record and the reason:

```bash
gh issue close <number> --reason "not planned" --comment "Duplicate of #<canonical>. ..."
```

GitHub's close reasons are `completed`, `not planned`, and `duplicate`. Never delete an issue.

## Verify

```bash
gh issue view <number> --json labels,milestone,state,stateReason,blockedBy,blocking
```

A label, link, edit, or closure counts as applied only when the API reports it back. Never claim a
mutation from the fact that a command exited zero.

## Comment discipline

Comments are for provenance, explicit supersession, duplicate resolution, cross-issue
coordination, and unresolved human decisions. Prefer editing the canonical body.

Do not post a comment that summarizes the issue back to its author, announces that a pass ran,
lists what was checked, or says an issue "looks good". A pass that changes nothing posts nothing.
