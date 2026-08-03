# Issue Labels

The label taxonomy every issue skill reads and writes. A repository that already has its own
convention wins; this is the default when it has none, and the reference when its convention is
incomplete.

The point is sortable work. A backlog labelled only `bug` or `enhancement` cannot be ordered,
filtered or planned.

## Closed sets

No label may be created with a `type:`, `priority:`, `effort:`, `evidence:` or `status:` prefix
outside the values below. A value that seems to be missing is a conversation with the owner, not a
new label.

### `type:` — required, exactly one

`bug` · `feature` · `improvement` · `refactor` · `maintenance` · `research` · `documentation`

No additions. `type: hotfix` is urgency, which `priority:` already carries.

### `priority:` — required, exactly one

`P0` · `P1` · `P2` · `P3`

No additions. `P4` is a backlog that has stopped ordering itself.

### `effort:` — at most one

`XS` · `S` · `M` · `L` · `XL`

An issue may carry no `effort:` label while it is still unestimated, and that absence is
meaningful: it says nobody has sized it yet. Once estimated it takes exactly one value, and
never a second one.

`effort: XL` is a signal to check whether the issue should be split before it is planned.

### `evidence:` — at most one

`confirmed` · `likely` · `judgment`

How strongly the issue is established, for issues that came out of an audit. `confirmed` is a
traced defect or a stated requirement. `likely` is a strong trace with an unverified assumption
still in it. `judgment` is a heuristic call that a reasonable person could decline.

Absence means the issue did not come from an audit, so there is nothing to qualify. Never add
`evidence: confirmed` to an ordinary reported bug to fill the field.

This is orthogonal to `priority:`, not a softer version of it. A confirmed `P2` and a likely `P0`
are different bets, and the pair is the whole reason both labels exist. The value changes when
somebody verifies the finding, and updating it is part of doing that work.

### `status:` — at most one

`blocked` · `needs-decision`

An exception, not a workflow. `blocked` says the issue cannot proceed for an external reason.
`needs-decision` says it is waiting on a human choice that evidence cannot settle.

Absence is the normal state. Do not add `status: ready`, `status: in-progress` or anything else
that turns the label into a board column; assignment, linked PRs and issue state already carry
that.

## Open set

### `area:` — one or more

Free values, drawn from the shape of the repository rather than from a fixed list. Typical
values in a front-end project: `grid`, `source-editor`, `formats`, `clipboard`,
`import-export`, `workspace`, `persistence`, `accessibility`, `design-system`, `performance`,
`documentation`, `tooling`.

Add an `area:` only when it is a filter somebody will use more than once. A label invented for a
single issue is noise with a colour.

## Rules

- The working default on any issue is `type` + `priority` + `effort` + `area`. `evidence:` and
  `status:` are added only when they are true.
- Never label with bare `bug`, `feature` or `enhancement`. They carry no order.
- Never encode a dependency as a label. Dependencies are `Depends on #123` links and the
  dependency graph. `status: blocked` states the state, never who does the blocking.
- Never invent a value to avoid leaving a field empty. An absent `effort:` is honest; a guessed
  one is not.
- Never label provenance. Which agent, tool or session produced an issue belongs in its body.
  Nobody filters by it twice, and the label outlives the fact.

## Outside the taxonomy

These prefixes are the required spine, not an exhaustive list of what a repository may carry. A
label this document does not cover is not thereby wrong. Every existing label gets exactly one of
three verdicts:

| Verdict | Action |
| --- | --- |
| **Maps** to a dimension here | rename it in place |
| **Duplicates** a dimension already applied | apply the replacement first, delete only after verifying |
| **Orthogonal** to every dimension here | leave it untouched |

Orthogonal is the default when the label is in use and its meaning is clear. Deciding a label is
noise is the owner's call, never an inference from its absence here.

A label whose meaning cannot be read from its name is not classifiable yet. Read the issues
carrying it before assigning a verdict, because the same word is often a type in one repository
and an area in another.

## Migrating an existing repository

A migration touches every issue at once, so it is authorized per label by the owner before the
first mutation, and it is `project-groom` that runs it, never a single-issue skill.

**Read the real labels first.** Never plan a migration against a remembered or assumed list; the
most common failure is mapping a label that does not exist.

```bash
gh label list --limit 200 --json name,description,color
gh issue list --state all --limit 500 --json labels \
  --jq '[.[].labels[].name] | group_by(.) | map({name: .[0], count: length}) | sort_by(-.count)'
```

`gh label list` defaults to 30 labels, which silently truncates a real repository. The second
command gives usage counts, which `gh label list` does not expose. A label with a count of zero
is a rename nobody needs.

**Rename, do not recreate.** A rename carries to every issue holding the label, open and closed,
in one operation and with no history loss:

```bash
gh label edit "bug" --name "type:bug"
```

Recreating instead means applying the new label to every issue by hand and losing whatever the
old one recorded on closed issues.

**Deletion is the only irreversible step.** Deleting a label removes it from every issue it is on
and cannot be undone. Delete only after the replacement is applied and read back, and never delete
a label the taxonomy simply does not cover:

```bash
gh label delete "<name>" --yes
```

**Verify from the API.** The migration is done when `gh label list` and a sample of
`gh issue view <number> --json labels` report the new names, not when the commands exited zero.
