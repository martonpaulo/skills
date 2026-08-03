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

An exception, not a workflow. `blocked` says the issue cannot proceed for a reason **outside the
backlog**: an upstream release, a vendor, a pending access request, a decision belonging to
somebody who is not the owner. `needs-decision` says it is waiting on a human choice that evidence
cannot settle.

**Waiting on another issue is never `blocked`.** That is a GitHub issue dependency, which
`project-groom` reads directly to build the blocking order. A label cannot say *which* issue blocks
this one, so using it here replaces a precise fact with a vague one and leaves two copies to drift
apart. Record the dependency and leave `status:` off.

Either value requires the reason to be written in the issue, in the body or a comment. `blocked`
with no stated cause is unactionable: nobody can tell whether it cleared, and nobody knows what to
watch for.

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

## Reading an issue's state

There is no `phase:` label and there should not be one. The SDD phases are sections in the issue
body, so a label claiming an issue has a `Plan` is a cached copy of something written a few
centimetres away, and it goes stale the first time somebody edits the body without touching the
label. The skills would gain nothing either: `issue-implement` reads the body to confirm the
phases are implementation-safe, and would have to keep reading it even with a label present,
because it cannot trust one.

Every state worth filtering on is already readable from a field that has exactly one owner:

| Question | What answers it | Owner |
| --- | --- | --- |
| Did Specify and Clarify happen? | The issue exists as a canonical issue, unless `status: needs-decision` says a product choice is still open | `issue-capture` |
| Is there a Plan and are there Tasks? | The `effort:` label. Its absence means nobody has planned it yet | `issue-plan` |
| Is somebody working on it? | Assignee and linked pull request | GitHub |
| Can it proceed at all? | `status:`, and the issue dependencies for a backlog-internal block | `status:` and GitHub |

So the backlog filter for work that is not ready yet is the absence of `effort:`, which costs no
new label and cannot fall out of step with the issue, because the skill that writes the plan is the
skill that sets the estimate.

An issue that entered the backlog without passing through `issue-capture`, from an audit or filed by
hand, is the one case none of this covers. What it is missing is a product decision rather than a
phase, and `status: needs-decision` already says exactly that.

If a real board is wanted, it belongs in a GitHub Project with a Status field. That is a view over
the issues and copies nothing into them. It stays optional; no skill here requires it.

## Colours

Colour is an accelerant, never information. The prefix already carries the meaning, and an issue
list has to stay readable to somebody who cannot separate these hues. Nothing may be encoded in
colour alone.

Within that limit, one rule makes a wall of labels scannable: **the family says which dimension, the
lightness says where in it.**

| Dimension | Family | What varies | Why |
| --- | --- | --- | --- |
| `priority:` | Warm, deep red through amber | Darkness, dark is urgent | Ordered, and the one dimension that should pull the eye |
| `effort:` | Cool blue | Darkness, dark is large | Ordered, so `XL` carries visible weight and invites the split |
| `type:` | Purple through magenta | Hue only, lightness constant | Unordered. A ramp would imply a rank that does not exist |
| `evidence:` | Green | Darkness, dark is stronger evidence | Ordered |
| `status:` | Neutral charcoal | Nothing, both are dark | An exception. It must stand out without competing with `priority:` for red |
| `area:` | One light grey for every value | Nothing | Open set. An unbounded set cannot hold a scale, and areas should sit quietest |

A starting palette. Adjust the values; keep the rule.

| Label | Colour | | Label | Colour |
| --- | --- | --- | --- | --- |
| `priority: P0` | `8C1B12` | | `type: bug` | `7B3FA0` |
| `priority: P1` | `C0341D` | | `type: feature` | `8A3FA8` |
| `priority: P2` | `E08A2E` | | `type: improvement` | `9A3FAB` |
| `priority: P3` | `F3D08A` | | `type: refactor` | `A93FA6` |
| `effort: XS` | `D3E7F2` | | `type: maintenance` | `B53F9B` |
| `effort: S` | `A5CCE3` | | `type: research` | `BE3F8D` |
| `effort: M` | `6BA4C9` | | `type: documentation` | `C4407D` |
| `effort: L` | `3A75A3` | | `evidence: confirmed` | `1E6B3A` |
| `effort: XL` | `1D4A6B` | | `evidence: likely` | `4E9E68` |
| `status: blocked` | `24292F` | | `evidence: judgment` | `A8D2B4` |
| `status: needs-decision` | `57606A` | | every `area:` | `D0D7DE` |

GitHub picks the text colour itself from the background, so a ramp will flip from dark text to light
text partway down. That is expected and is why each ramp crosses the middle only once.

Recolouring is the one label operation that touches no issue:

```bash
gh label edit "priority: P0" --color 8C1B12
```

It is safe to run over an established repository and needs no per-issue verification, unlike a
rename and unlike a deletion. Apply it through `project-groom` when a migration is already
underway, rather than as a separate pass over the label list.

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
gh label edit "bug" --name "type: bug"
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
