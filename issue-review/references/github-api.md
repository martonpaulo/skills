# GitHub API commands

Every command below was verified against `gh` and the GitHub API. Reach the API through the
available native GitHub integration or `gh api`; they are transports for the same endpoints.

## Resolve the pull request

Parse the command before calling GitHub:

| Invocation | Meaning | Lookup |
| --- | --- | --- |
| `/issue-review 123` | Issue `#123` | Find the unique open PR that closes it |
| `/issue-review pr 456` | Pull request `#456` | Read PR `#456` directly |

A bare number is always an issue number. Never query a same-numbered PR as a fallback when issue
resolution returns zero results.

For `/issue-review <issue-number>`, find the open pull request that closes the issue:

```bash
gh pr list --state open --json number,title,closingIssuesReferences \
  --jq '.[] | select(.closingIssuesReferences[]?.number == <issue-number>)'
```

Exactly one result is the expected case; use its `number` as `<number>` in every command below.

- **Zero results** means no open PR closes the supplied issue. Stop and report the missing linkage
  rather than guessing at a draft, body mention, closed PR, or same-numbered PR.
- **More than one result** means multiple open PRs claim the supplied issue. Stop and report
  the conflict; do not pick one without the user's direction.

For `/issue-review pr <pull-request-number>`, read that exact PR and require it to be open:

```bash
gh pr view <pull-request-number> --json number,state
```

Stop when it does not exist or its state is not `OPEN`. Do not reinterpret the PR number as an
issue number.

## Read the pull request

```bash
gh pr view <number> --json number,title,body,isDraft,baseRefName,headRefName,headRefOid,mergeable,mergeStateStatus,reviewDecision,latestReviews,commits,files,labels,closingIssuesReferences,comments
```

`headRefOid` is the head SHA. Record it before reviewing and compare it again before submitting.
`closingIssuesReferences` gives every issue this PR closes, which is the controlling contract.
The set must be non-empty and match the leading `Closes #N` lines in the body. For issue-form
invocation, it must contain the supplied issue. GitHub interprets those keywords only when
`baseRefName` is the repository's default branch.
`mergeStateStatus` and `reviewDecision` decide whether merging is even possible.

```bash
gh pr diff <number>                 # the diff under review
gh pr diff <number> --name-only     # changed paths, for scoping
gh pr checks <number>               # check runs, to tell introduced failures from pre-existing
```

## Read existing review threads

The REST API does not report whether a thread is resolved. GraphQL does:

```bash
gh api graphql -f query='
query($owner:String!,$repo:String!,$pr:Int!){
  repository(owner:$owner,name:$repo){
    pullRequest(number:$pr){
      reviewThreads(first:100){
        nodes{ id isResolved isOutdated path line
          comments(first:10){ nodes{ databaseId author{login} body } } } } } } }
' -F owner=<owner> -F repo=<repo> -F pr=<number>
```

Unresolved, non-outdated threads are the ones that can block approval. Reply inside an existing
thread instead of opening a parallel one:

```bash
gh api --method POST repos/<owner>/<repo>/pulls/comments/<comment_id>/replies -f body='...'
```

## Publish the review

One request carries the inline comments and the verdict together, pinned to the reviewed SHA.
Nested arrays cannot be expressed with `-f`, so pass JSON on stdin:

```bash
gh api --method POST repos/<owner>/<repo>/pulls/<number>/reviews --input - <<'JSON'
{
  "commit_id": "<the reviewed head SHA>",
  "event": "REQUEST_CHANGES",
  "body": "What was verified, and why this verdict follows.",
  "comments": [
    {
      "path": "src/auth/session.ts",
      "line": 84,
      "side": "RIGHT",
      "body": "`expiresAt` is compared before it is parsed, so an expired session passes. Parse it first, or compare against the epoch value."
    },
    {
      "path": "src/auth/session.ts",
      "start_line": 120,
      "start_side": "RIGHT",
      "line": 126,
      "side": "RIGHT",
      "body": "This branch cannot be reached: the guard on line 118 already returned. Delete it or fix the guard."
    }
  ]
}
JSON
```

- `event`: `APPROVE` or `REQUEST_CHANGES`. Never `COMMENT` as the final verdict.
- `line` is the line number in the file at the reviewed SHA. `side` is `RIGHT` for the new
  version and `LEFT` for the deleted one.
- A range uses `start_line` plus `start_side` with `line` plus `side`.
- The anchor must fall inside the diff. GitHub rejects a comment on an untouched line.

`gh pr review --approve` and `gh pr review --request-changes` are acceptable only when the review
carries no inline comments, because they cannot anchor any.

## When the review event is refused

`APPROVE` on a PR authored by the same account returns HTTP 422. The findings are still published,
as a PR comment whose first line is the verdict:

```bash
gh pr comment <number> --body-file - <<'MD'
Approved ✅

What was verified, and why this verdict follows.

`src/auth/session.ts:84` — ...

🤖 AI-generated by ❋ Claude Sonnet 5 (High)
MD
```

The first line is `Approved ✅`, `Requested Changes 🔄` or `Commented 💬`. A plain comment cannot
anchor to the diff, so each finding names its file and line in the text. Report the formal event as
refused; never report it as submitted.

## Verify, then report

```bash
gh pr view <number> --json reviewDecision,latestReviews,headRefOid
```

A verdict is published only when the API reports it. If the head SHA moved between reviewing and
submitting, the review is pinned to the wrong state: inspect the new commits and redo the verdict.

After merging, verify the PR and every issue recorded before merge:

```bash
gh pr view <number> --json state,mergedAt,baseRefName,closingIssuesReferences
gh issue view <issue-number> --json number,state,stateReason,url
```

GitHub normally auto-closes linked issues after merge to the default branch. If a recorded issue
is still open, close it only after `mergedAt` is non-null, then read it back:

```bash
gh issue close <issue-number> --reason completed
gh issue view <issue-number> --json number,state,stateReason,url
```

The merge workflow is complete only when every recorded issue reports `CLOSED`. If a close fails,
report that the PR merged but name the exact issue whose closure remains incomplete.

## What makes a comment worth publishing

Anchor every claim about a line to that line. A review body that says "line 84 is wrong" while
the API could have attached that text to line 84 is a defect in the review, not a style choice.

Each inline comment states the failure, the evidence, the rule or requirement it violates, and the
minimum correction. A comment that only restates what the code does, praises it, marks a
preference, or asks something the repository answers is not published at all. Silence on a hunk
means it was read and found sound.

Consolidate repeated symptoms of one cause into a single comment on the clearest occurrence and
name the other sites in its body, rather than pasting the same note across ten lines.
