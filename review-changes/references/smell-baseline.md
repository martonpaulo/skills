# Smell baseline

A fixed set of code smells from Martin Fowler's *Refactoring*, chapter 3, applied on the Standards
axis when the repository documents nothing that covers the case.

Every entry here is a heuristic, never a violation. Report it as a labelled judgment call
("possible Feature Envy") with the hunk quoted, and let the reader decide.

Two rules bind the whole list:

- **The repository overrides.** A documented convention always wins. Where the repository endorses
  something an entry would flag, suppress it silently.
- **Tooling wins too.** Skip anything a formatter, linter, or type checker already enforces.

Match each against the diff, not against the whole codebase. A smell that predates the change is
not a finding about the change; mention it only when the change makes it materially worse.

| Smell | What it is | Usual fix |
| --- | --- | --- |
| Mysterious Name | A function, variable, or type whose name does not reveal what it does or holds | Rename it. If no honest name comes, the design is murky |
| Duplicated Code | The same logic shape appears in more than one hunk or file in the change | Extract the shared shape and call it from both |
| Feature Envy | A method reaches into another object's data more than its own | Move the method onto the data it envies |
| Data Clumps | The same few fields or parameters keep travelling together | Bundle them into one type and pass that |
| Primitive Obsession | A primitive or string stands in for a domain concept that deserves its own type | Give the concept its own small type |
| Repeated Switches | The same switch or if-cascade on the same type recurs across the change | Replace with polymorphism, or one map both sites share |
| Shotgun Surgery | One logical change forces scattered edits across many files in the diff | Gather what changes together into one module |
| Divergent Change | One file or module is edited for several unrelated reasons | Split so each module changes for one reason |
| Speculative Generality | Abstraction, parameters, or hooks added for needs the intent does not have | Delete it. Inline back until a real need shows |
| Message Chains | Long `a.b().c().d()` navigation the caller should not depend on | Hide the walk behind one method on the first object |
| Middle Man | A class or function that mostly just delegates onward | Cut it and call the real target directly |
| Refused Bequest | A subclass or implementer ignores or overrides most of what it inherits | Drop the inheritance and use composition |

## Boundary

These are surface heuristics read from a diff. When a finding needs the caller graph, the
dependency direction, or the test seam to be judged properly, it belongs to `module-design`, not
here. Name the route and move on.
