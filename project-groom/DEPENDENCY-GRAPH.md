# Dependency Graph

The closing output of every curation pass: one Mermaid block and a short legend. The block contains
every open issue considered, including issues with no blocking relationship. Edges encode blocking
order; rectangular group boxes encode sets that can be closed by the same pull request.

## Block structure

```
%%{init: {"flowchart": {"curve": "linear", "nodeSpacing": 40, "rankSpacing": 60}}}%%
flowchart TD
```

- `flowchart TD`, never `LR`.
- No `%%` comments anywhere in the block. The `%%{init}%%` line above is a configuration
  directive, not a comment, and stays.
- Strip accents and diacritics from every label. They break the import in some renderers.
- Node id is `N<number>`, using the issue number exactly as GitHub displays it.

## Node label

An identity block, a blank line, then the labels. Lines break on `<br/>` and the blank line is
`<br/><br/>`; `\n` does nothing inside a Mermaid label.

```
N91["#91<br/>Workspace passa a aceitar de um a quatro panes<br/><br/>type: feature<br/>priority: P1<br/>effort: L"]
```

- The number with no leading zeros (`#3`, `#21`, `#245`, `#2952`).
- A short description written by the agent in the language of the conversation, saying what the
  issue *does* rather than repeating its title.
- Then, after the blank line, one line each for `type:`, `priority:`, `effort:` and `status:`, in
  that order, carrying the issue's real label values.

Drop a line entirely when the issue does not carry that label, rather than printing an empty or
invented value. An issue with no `effort:` yet is an issue nobody has planned, and the graph
should show that gap instead of papering over it. The taxonomy behind these values is the one
[`issue-capture` documents](../issue-capture/LABELS.md).

**`area:` and `evidence:` never appear.** Area labels are long and already filterable in the issue
list. Evidence remains part of backlog analysis and written findings, but do not render its label
or value in the Mermaid block or legend.

`status:` is absent on most issues, so the common node stays three lines. It earns its place when
present because an issue waiting on a human is a bad place to start.

```
N73(["#73<br/>Import perde a ultima coluna quando o arquivo termina sem newline<br/><br/>type: bug<br/>priority: P1<br/>status: needs-decision"])
```

`status:` gets no colour or marker of its own. Colour is the dependent count and shape is
readiness. `status:` reaches the shape only because it is one of the two things that make an issue
unstartable, not as a channel of its own.

## No links

No `click` lines and no anchor tags. The issue number is in the node and the reader has the
backlog open anyway.

## Edges

- Solid `-->` only for real blocking order: the source must land before the target.
- Dashed `-.->` with an inline label only for cycles that must be broken before anyone starts:
  `N73 -.->|"cycle, #70 lists Move pane but #73 says it comes after #70"| N70`.
- Nothing else becomes an edge. Coordination, overlap, supersession, duplicates, conflicts and
  umbrella issues belong in the written report; as edges they make the graph unreadable.
- Never add an edge to make the graph connected.

## Shape

Shape encodes **readiness**: can somebody pick this up right now.

- `[ ]` rectangle: ready to implement. It carries an `effort:` label, so `issue-plan` has run and
  the Tasks exist, and it carries no `status:` label, so nothing is holding it.
- `([ ])` stadium: not ready. Either it has no `effort:` label, meaning nobody has planned it, or
  it carries a `status:`, meaning something is holding it. The soft edge reads as draft, which is
  what it is.
- No emoji or symbol markers inside labels. They disappear on render.

The binary is deliberate. Which of the two reasons applies is already legible inside the node: a
missing `effort:` line, or a `status:` line that is present. The shape only has to answer whether
somebody can start, and a third shape would spend a visual channel on something the text already
says.

Shape used to mean "waits for nobody", which was a poor use of the channel: the arrows say that
already, and better, because they say *what* it waits for. Readiness is not visible anywhere else
in the graph, so it earns the shape.

An issue can be perfectly ready and still blocked by an arrow. That combination is a rectangle
with an incoming edge, and it reads correctly: prepared, waiting its turn.

## Color

Color encodes **how many unique issues depend on it directly or indirectly**, never how many it
waits for. This transitive dependent count answers which issue has the greatest total downstream
unlock reach, not only which issue has the most immediate children.

For each issue, follow the real dependency relation from that issue to every issue it blocks,
then continue through everything those issues block. Count the unique reachable issues and exclude
the starting issue itself:

```
transitiveDependents(issue) = union of every reachable downstream issue
dependentCount(issue) = size(transitiveDependents(issue) - {issue})
```

For `#3 --> #2 --> #1`, the counts are `#3 = 2`, `#2 = 1`, `#1 = 0`. In a diamond where
`#4` reaches `#1` through both `#2` and `#3`, the count for `#4` is `3`, not `4`: count `#1`
once because path count is not issue count.
Compute from GitHub's complete `blockedBy` and `blocking` relation before choosing solid or dashed
edge styles. In a cycle, use the unique reachable set and still exclude the starting issue, so a
node is never counted as its own dependent.

The ordered scale has to read at a glance, so it walks one continuous path, green to teal to blue
to indigo to purple, getting darker at every step, with the border thickening along with it. Two
channels move in the same direction, which survives a grayscale print and a dark theme:

```
classDef d0 fill:#cdeac0,stroke:#7cb342,stroke-width:1px,color:#1b5e20
classDef d1 fill:#8ed3b8,stroke:#2e9e75,stroke-width:2px,color:#0b3d2e
classDef d2 fill:#4fb3c9,stroke:#0f7f96,stroke-width:2px,color:#053540
classDef d3 fill:#2b6cb0,stroke:#174e7c,stroke-width:3px,color:#ffffff
classDef d4 fill:#3b4b9e,stroke:#1f2a6b,stroke-width:3px,color:#ffffff
classDef d5 fill:#5b2a86,stroke:#37134f,stroke-width:4px,color:#ffffff
```

Two constraints hold whatever the palette:

- **Lightness only ever decreases.** A step that is lighter than the one before it destroys the
  ordering, however pleasant the hue.
- **The bottom step still has to be a color.** Near-white and light grey wash out against a
  white page and read as "unstyled" rather than as "zero".

Avoid the red and amber family here. It reads as severity, not as quantity, and the backlog
already has priority for that. Amber fills are the most common way this spec gets ignored, and
they are wrong twice over: they claim urgency the count does not carry, and they collide with the
`priority:` palette.

**The label colour palette does not apply here.** The colours in
[LABELS.md](../issue-capture/LABELS.md) dress GitHub label chips, where family means dimension.
This block colours by transitive dependent count, which is not a label dimension at all. Colouring
nodes by `type:` or `priority:` would spend the graph's only ordered channel on something already
written inside every node, and lose the one fact the graph exists to show.

Collapse the unused steps and always land the darkest class on the highest transitive count
actually present, so the top of the scale is the root with the greatest total downstream reach
rather than a fixed number. The legend states the exact transitive count behind each step it used.

## Coverage and pull request groups

Every open issue considered by the pass appears exactly once as a node in the Mermaid block.
Never omit an issue because it has no incoming or outgoing dependency edge. An independent issue
stays as a loose node unless it belongs to a real same-PR group.

Put two or more issues inside a rectangular Mermaid `subgraph` when they can be implemented,
validated, and closed by one coherent pull request:

```mermaid
subgraph PR1["Same PR: preserve workspace layout"]
  direction LR
  N3["#3<br/>Persist pane sizes<br/><br/>type: feature<br/>priority: P1<br/>effort: S"]
  N53["#53<br/>Restore pane sizes<br/><br/>type: bug<br/>priority: P1<br/>effort: S"]
end
style PR1 fill:#f6f8fa,stroke:#6e7781,stroke-width:1px,stroke-dasharray:4 3
```

The box means **same pull request candidate**, never dependency. Draw every real dependency as an
edge even when both nodes share a box, and never add an edge merely to keep grouped nodes beside
each other. Name the box for the shared outcome in the language of the conversation, not `Group
1`, and use `direction LR` so its issues sit side by side when the renderer permits it.

Group only when one implementation boundary, owner, and validation story can satisfy every
issue's acceptance criteria without making the pull request harder to review. Shared area,
priority, milestone, or timing is not enough. A group is a delivery recommendation, not a promise:
the implementation skill may split it when the code proves the boundary false.

An issue belongs to at most one same-PR group. Leave it loose when membership is ambiguous. Do not
create subgraphs for area, epic, milestone, dependency component, or all independent issues;
those boxes would imply a same-PR relationship that does not exist. Do not nest group boxes.

## Legend

Three or four lines of prose after the block, in this order:

1. what the shapes mean: rectangle ready, stadium not ready,
2. the color scale with the exact direct-plus-indirect dependent count of each step,
3. what each rectangular group box means: its issues can close through one coherent pull request,
4. where to start: the root that unblocks the most, and any cycle that has to be broken first. Say
   so in that same line when that root carries `status:`, because then the real first move is
   unblocking it.

Nothing longer. The findings are already in the report above it.

## When the graph gets too big

Simplify the single graph instead of splitting it: shorten labels and remove nonessential prose
around it. Never remove independent issues, invent dependencies, or group unrelated issues to
reduce the node count. Never emit a high-level graph plus per-component graphs.

If it is still too big after that, the graph is not the problem. A backlog whose blocking
structure genuinely does not fit on a canvas has too many declared dependencies, and saying that
in the report is more useful than another rendering attempt.
