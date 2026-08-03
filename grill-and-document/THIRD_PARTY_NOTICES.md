# Third-party notices

## mattpocock/skills (engineering/grill-with-docs)

- **Upstream repository:** https://github.com/mattpocock/skills
- **Upstream path:** `skills/engineering/grill-with-docs`
- **Imported revision:** `ed37663cc5fbef691ddfecd080dff42f7e7e350d`
- **Imported on:** 2026-07-22
- **Last checked against upstream:** 2026-08-03
- **Original author:** Matt Pocock
- **License:** MIT

No upstream file is vendored. The original is a single instruction: run a grilling session using
the domain-modeling skill, and it is user-invoked.

### What was adapted

The composition itself: an interview that produces documentation as it goes, delegating the
questioning to `grilling` and the terminology work to `domain-model`, and being user-invoked.

### What changed

The upstream one-liner leaves every judgment to the agent. This version states them:

- inspect existing glossary and ADR conventions first, and respect configured paths before falling
  back to the defaults `domain-model` defines;
- write the glossary entry when terminology becomes canonical rather than at the end;
- keep glossary content to domain vocabulary, states, rules, and relationships, and never let
  `CONTEXT.md` become a specification;
- record an ADR only when the decision is hard to reverse, surprising without context, and based
  on a real tradeoff, which most terminology clarifications are not;
- create no planning or work-management artifacts, and do not start implementing after the
  interview;
- end with the agreed understanding, files written, unresolved decisions, and the recommended next
  action.

The upstream sibling that this skill's counterpart came from, `productivity/grill-me`, is not
carried here at all. It was a seven-line wrapper whose entire content was "apply grilling without
writing files", which `grilling` already guarantees on its own.
