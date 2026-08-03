# GitHub API commands

Every command below was verified against `gh` and the GitHub API. Reach the API through the
available native GitHub integration or `gh api`; they are transports for the same endpoints.

## Read the pull request

```bash
gh pr view <number> --json number,title,body,isDraft,baseRefName,headRefName,headRefOid,mergeable,mergeStateStatus,reviewDecision,latestReviews,commits,files,labels,closingIssuesReferences,comments
```

`headRefOid` is the head SHA. Record it before reviewing and compare it again before submitting.
`closingIssuesReferences` gives the issues this PR closes, which is the controlling contract.
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

## Verify, then report

```bash
gh pr view <number> --json reviewDecision,latestReviews,headRefOid
```

A verdict is published only when the API reports it. If the head SHA moved between reviewing and
submitting, the review is pinned to the wrong state: inspect the new commits and redo the verdict.

## What makes a comment worth publishing

Anchor every claim about a line to that line. A review body that says "line 84 is wrong" while
the API could have attached that text to line 84 is a defect in the review, not a style choice.

Each inline comment states the failure, the evidence, the rule or requirement it violates, and the
minimum correction. A comment that only restates what the code does, praises it, marks a
preference, or asks something the repository answers is not published at all. Silence on a hunk
means it was read and found sound.

Consolidate repeated symptoms of one cause into a single comment on the clearest occurrence and
name the other sites in its body, rather than pasting the same note across ten lines.
