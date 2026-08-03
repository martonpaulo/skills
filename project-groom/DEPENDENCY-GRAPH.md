# Dependency Graph

The closing output of every curation pass: one Mermaid block, a short legend, then the table of
issues that have no blocking relationship. The block encodes blocking order and nothing else.

## Block structure

```
%%{init: {"flowchart": {"curve": "linear", "nodeSpacing": 40, "rankSpacing": 60}}}%%
flowchart TD
```

- `flowchart TD`, never `LR`.
- No `%%` comments anywhere in the block. The `%%{init}%%` line above is a configuration
  directive, not a comment, and stays.
- Strip accents and diacritics from every label. They break the import in some renderers.
- Node id is `N<zero-padded number>`.

## Node label

An identity block, a blank line, then the labels. Lines break on `<br/>` and the blank line is
`<br/><br/>`; `\n` does nothing inside a Mermaid label.

```
N091["#091<br/>Workspace passa a aceitar de um a quatro panes<br/><br/>type: feature<br/>priority: P1<br/>effort: L"]
```

- The number, zero-padded to three digits (`#003`, `#021`, `#245`). Past three digits, every
  digit is kept as it is (`#2952`).
- A short description written by the agent in the language of the conversation, saying what the
  issue *does* rather than repeating its title.
- Then, after the blank line, one line each for `type:`, `priority:`, `effort:`, `evidence:` and
  `status:`, in that order, carrying the issue's real label values.

Drop a line entirely when the issue does not carry that label, rather than printing an empty or
invented value. An issue with no `effort:` yet is an issue nobody has planned, and the graph
should show that gap instead of papering over it. The taxonomy behind these values is the one
[`issue-capture` documents](../issue-capture/LABELS.md).

**`area:` never appears.** Every issue carries several, they are the longest lines in the node,
and they are the one dimension nobody reads off a blocking graph. Filter by area in the issue
list, where the filter exists.

`evidence:` and `status:` are absent on most issues, so the common node stays three lines. They
earn their place when they are there: an issue nobody has confirmed and an issue waiting on a
human are both bad places to start, and the graph is where somebody decides where to start.

```
N073(["#073<br/>Import perde a ultima coluna quando o arquivo termina sem newline<br/><br/>type: bug<br/>priority: P1<br/>evidence: likely<br/>status: needs-decision"])
```

Neither one gets a colour or a marker of its own, and `evidence:` gets no shape either. Colour is
the dependent count and shape is readiness; a third visual channel makes the graph unreadable,
which is the reason most things here are text lines. `status:` reaches the shape only because it
is one of the two things that make an issue unstartable, not as a channel of its own.

## No links

No `click` lines and no anchor tags. The issue number is in the node and the reader has the
backlog open anyway.

## Edges

- Solid `-->` only for real blocking order: the source must land before the target.
- Dashed `-.->` with an inline label only for cycles that must be broken before anyone starts:
  `N073 -.->|"cycle, #070 lists Move pane but #073 says it comes after #070"| N070`.
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

Color encodes **how many issues depend on it**, never how many it waits for. It has to read as
an ordered scale at a glance, so it walks one continuous path, green to teal to blue to indigo
to purple, getting darker at every step, with the border thickening along with it. Two channels
in the same direction, which survives a grayscale print and a dark theme:

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
This block colours by dependent count, which is not a label dimension at all. Colouring nodes by
`type:` or `priority:` would spend the graph's only ordered channel on something already written
inside every node, and lose the one fact the graph exists to show.

Collapse the unused steps and always land the darkest class on the highest count actually
present, so the top of the scale is the root of the backlog rather than a fixed number. The
legend states the exact count behind each step it used.

## Grouping

**Only issues with at least one edge go in the block.** An issue with no blocking relationship in
either direction is not part of a dependency graph; it is a row in the table below it.

This is what keeps the graph readable as the backlog grows. `flowchart TD` puts every node that
waits for nobody on the same top rank, so a few dozen unconnected issues line up beside the real
roots and push the connected pairs metres apart, and the edges then run the whole width of the
canvas to reach each other. The connected structure is small and roughly constant; the
unconnected set grows with the backlog. Leaving them in means the thing worth reading is always
the thing hardest to see.

Fencing them in a subgraph does not fix it. Forty loose boxes inside a box are still forty loose
boxes, and the rule against subgraphs exists because every earlier attempt at grouping made the
graph worse.

So, still no subgraphs at all: not by area, not by epic, not by milestone, and not for the
unconnected issues either. Every node in the block sits loose on the canvas, and every node in
the block has an edge.

The unconnected issues are never dropped, only moved. They go into a table immediately after the
legend, ordered by `priority:` and then by `effort:`, one row each:

| Issue | Does | type | priority | effort | Ready |
| --- | --- | --- | --- | --- | --- |
| `#030` | Stops pane zoom from stealing the browser zoom keys | bug | P1 | M | yes |
| `#044` | Lifts notices out of the layout into an overlay | improvement | P1 | | not planned |

`Ready` follows the same rule as the shape: `yes` for an issue with an `effort:` and no `status:`,
otherwise the reason, `not planned` or the `status:` value. Sorted this way the table answers
"what can I start right now" better than a scatter of boxes ever did, which is the question those
nodes were on the canvas to answer.

Say the count in one line above the table. A backlog where that table is much longer than the
graph is telling you something true about the backlog, not about the graph.

## Legend

Two or three lines of prose after the block, in this order:

1. what the shapes mean: rectangle ready, stadium not ready,
2. the color scale with the exact dependent count of each step,
3. where to start: the root that unblocks the most, and any cycle that has to be broken first.
   Say so in that same line when that root carries `status:` or a non-`confirmed` `evidence:`,
   because then the real first move is unblocking it or verifying it.

Nothing longer. The findings are already in the report above it. The table of unconnected issues
comes after this, with its one line of count.

## When the graph gets too big

Simplify the single graph instead of splitting it: remove everything that is not a blocking
dependency and shorten the labels. Never emit a high-level graph plus per-component graphs.

If it is still too big after that, the graph is not the problem. A backlog whose blocking
structure genuinely does not fit on a canvas has too many declared dependencies, and saying that
in the report is more useful than another rendering attempt.
