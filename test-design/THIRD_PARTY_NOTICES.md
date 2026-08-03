# Third-party notices

## mattpocock/skills (engineering/tdd)

- **Upstream repository:** https://github.com/mattpocock/skills
- **Upstream path:** `skills/engineering/tdd`
- **Imported revision:** `2ab958093e83e0ec752e6c1c5932da465bf23e0c`
- **Imported on:** 2026-08-03
- **Original author:** Matt Pocock
- **License:** MIT, full text in [LICENSE](LICENSE), preserved unchanged.

`tests.md` and `mocking.md` are upstream work, kept substantially intact. The worked good and bad
examples in them are the substance of this skill.

### What was adapted

The seam definition, the pre-agreed-seams rule, the three anti-patterns (implementation-coupled,
tautological, horizontal slicing), the independent-source rule for expected values, and the
separation of refactoring from the write-then-pass loop.

### What changed

**Renamed to `test-design`.** Upstream is named for the loop. The retained substance is the
decision of what to test and where the seam belongs; the loop itself is three paragraphs. The new
name pairs with `module-design`, which owns the boundary that the seam attaches to.

**The loop is a default, not a law.** Upstream states the order as a rule of the cycle. Here it is
the default with named exceptions (spikes, generated code, behavior whose shape is unknown until
something runs) and an explicit note that a test written afterwards is still valid once observed
failing. The collection does not require ceremony, and `prototype` is exempted outright.

**Seam confirmation is proportional.** Upstream requires confirming every seam with the user
before any test is written. Here the seams are named and checked against the caller's view, and
only a genuinely contested seam that changes what ships is routed to `grilling`.

**Cross-references corrected to this collection.** Upstream points at its own `code-review` skill
for the refactoring stage and reads `CONTEXT.md` directly. Those now point at `review-changes`,
`module-design`, `domain-model`, `debug`, and `prototype`, which are the skills that actually own
the referenced work here.

**A weak test is worse than no test.** This is the owner's rule and it governs the whole skill.
When the only available test would be one of the anti-patterns, none is written and the
unprotected behavior is named instead. Upstream has no equivalent position and no guidance on
declining to write a test.

**Four anti-patterns added** to upstream's three, all from the owner's stated rejections:
assertion-free tests, duplicated constants (asserting a string equals the same string),
wrapper-only tests, and duplicate coverage of a seam an existing test already pins.

**Safety boundaries added.** Never weaken, skip, or delete an existing test to make a suite pass;
never add a substitute for a component the project controls to make a test easier to write.
Upstream had no equivalent.

**Language neutrality stated.** The retained examples are TypeScript. The criteria are marked
language-neutral because this collection is used on Swift, Python, and TypeScript projects.
