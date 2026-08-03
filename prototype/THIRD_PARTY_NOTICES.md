# Third-party notices

## mattpocock/skills (engineering/prototype)

- **Upstream repository:** https://github.com/mattpocock/skills
- **Upstream path:** `skills/engineering/prototype`
- **Imported revision:** `ed37663cc5fbef691ddfecd080dff42f7e7e350d`
- **Imported on:** 2026-07-22
- **Last checked against upstream:** 2026-08-03
- **Original author:** Matt Pocock
- **License:** MIT

No upstream file is vendored. `LOGIC.md` and `UI.md` keep upstream's split and were rewritten down
to the parts that are not framework-specific.

### What was adapted

A prototype is throwaway code that answers a question, and the question decides the shape. The
logic-versus-UI branch and its two reference files, one command to run it, no persistence by
default, skipping polish, surfacing the full relevant state after every action, and stating the
assumption when the branch is ambiguous.

### What changed

**The experiment is isolated, not embedded.** Upstream places prototype code next to the module or
page it prototypes for, inside the project, named so a reader can tell it is a prototype. Here it
goes to `.scratch/prototypes/<slug>/` inside a repository or a uniquely named temporary workspace
outside one, and production files are never modified to make the prototype easier. Naming
convention is a weaker guarantee than location.

**No branch or issue ceremony.** Upstream's capture step commits the prototype to a throwaway
branch off main and leaves a context pointer on the implementation issue. This collection requires
no issue tracker and no branches, so the prototype is not committed, published, or pushed unless
the user explicitly asks. Every disposable file created is reported instead.

**The question is stated first and can falsify.** The workflow now opens by naming the single
question, the observable result that would answer it, and what would falsify the current
assumption, and allows adjusting the experiment only when an observation shows it cannot answer
that question.

**An adoption boundary was added.** Prototype code is never silently integrated into production;
adoption is separate implementation work with normal review and testing. Real data, credentials,
and destructive integrations stay out unless the question requires a safe isolated substitute.
Upstream stated neither.

**Reference files reduced.** Upstream's `UI.md` is 112 lines of a specific web stack's routing and
variant-switching recipe, and `LOGIC.md` is 79 lines of terminal-app scaffolding. Both were cut to
the criteria that survive outside that stack, since this collection is also used on Swift and
Python projects.
