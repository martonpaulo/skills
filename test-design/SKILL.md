---
name: test-design
description: Decide what to test, where the test seam belongs, and whether an existing or proposed test is worth keeping. Use when writing tests for new behavior, when a suite breaks on refactors that changed no behavior, when tests pass but defects still ship, or when a test's value is disputed. Do not use for running an existing suite, fixing an unrelated build failure, diagnosing a product bug, or choosing a test framework.
license: MIT
metadata:
  scope: project
  role: foundation
  mutation: write
  upstream: https://github.com/mattpocock/skills
  upstream-author: Matt Pocock
  upstream-path: skills/engineering/tdd
  upstream-revision: 2ab958093e83e0ec752e6c1c5932da465bf23e0c
  upstream-checked: 2026-08-03
  version: mattpocock-personal.1
---

# Test Design

Decide which behavior deserves a test, at which seam, and whether the resulting test earns its
maintenance cost. A suite that breaks on every refactor and still misses defects is worse than a
smaller suite that holds.

Use the project's own framework, runner, and conventions. This skill decides what a test asserts
and where it attaches, never which library to adopt.

## Seams

A seam is the public boundary where behavior is observable without reaching inside. Tests attach
to seams.

Name the seams under test before writing anything and check them against the caller's view: if no
caller depends on it, it is not a seam. `module-design` owns the boundary itself; this skill
decides where the test attaches to it. When the right seam is genuinely contested and the answer
changes what ships, resolve it through `grilling` rather than testing both.

Coverage is not the goal. Agreeing the seams is how effort lands on critical paths and complex
logic instead of on every reachable branch.

## A weak test is worse than no test

A test that cannot fail for a real reason still costs a run on every commit, still breaks on
refactors, and still reports green when the behavior is broken. It buys confidence it has not
earned. When the only test available for a piece of behavior would be one of the anti-patterns
below, write no test and say which behavior is therefore unprotected. Do not fill the gap with a
weak one.

This applies to writing new tests and to judging existing ones. A weak test found during review is
reported, not preserved for its coverage number.

## What a good test asserts

A good test reads as a specification of a capability, survives refactors that preserve behavior,
and fails for exactly one reason. Prefer real interfaces over substitutes for anything the project
controls.

Take vocabulary from the project's domain language so test names match the terms the code and
documentation already use. Route to `domain-model` when the terms themselves are contradictory.

See [tests.md](tests.md) for worked good and bad examples, and [mocking.md](mocking.md) for the
substitution boundary. Both use TypeScript for illustration; the criteria are language-neutral.

## Anti-patterns

- **Implementation-coupled.** Substitutes internal collaborators, asserts on private state, or
  verifies through a side channel such as querying the database instead of reading back through
  the interface. The tell: the test breaks under refactoring while behavior is unchanged.
- **Tautological.** The expected value is recomputed the way the code computes it, so the test
  passes by construction and can never disagree with the implementation. Expected values must come
  from an independent source: a known-good literal, a worked example, or the specification.
- **Duplicated constant.** The test imports or restates a constant, string, label, enum case, or
  configuration value from the source and asserts the source equals it. Comparing a string to the
  same string proves only that the assignment compiled. If the value matters, assert the behavior
  that depends on it; if nothing depends on it, it does not need a test.
- **Wrapper-only.** The subject forwards to something else and adds no behavior of its own, so the
  test pins the delegation rather than a capability. Test the behavior at the layer that owns it.
  A wrapper worth testing is one that transforms, validates, or decides something.
- **Duplicate coverage.** The behavior is already pinned by an existing test at the same seam.
  A second test that fails whenever the first does adds maintenance and no signal. Search the
  suite before adding, and extend the existing test instead when the case is a variation.
- **Horizontal slicing.** Writing every test first, then every implementation. Bulk tests verify
  imagined behavior and commit to a test structure before the implementation is understood. Work
  in vertical slices: one seam, one test, one implementation, then reassess.
- **Assertion-free.** The test executes code and asserts nothing meaningful, or asserts only that
  no exception was thrown. It reports coverage without reporting correctness.

## Writing order

Write the failing test first by default, because a test never observed failing has not been shown
to test anything. Watch it fail for the expected reason, then write only enough code to pass it.

Deviate when the cost is real, and say so: exploratory spikes, generated code, and behavior whose
shape is unknown until something runs. A test written afterwards is still valid once it has been
observed failing against the unfixed code. Do not force the order onto prototypes; `prototype`
owns disposable experiments and they are not required to carry tests.

Refactoring is not part of the write-then-pass loop. It is a separate pass, and `review-changes`
owns reviewing the result.

## Regression tests

A regression test for a fixed defect attaches to the same seam as the behavior it protects, and
must be observed failing against the unfixed code. `debug` owns diagnosis and the fix, and
delegates the test's placement here when the seam is unclear.

## Safety and completion

Do not weaken, skip, or delete an existing test to make a suite pass. A test that is wrong is
rewritten with its reason stated, never silenced. Do not add substitutes for components the
project controls merely to make a test easier to write; that is a boundary problem for
`module-design`.

The work is complete when every new test names its seam, was observed failing before passing,
asserts behavior rather than structure, takes its expected values from an independent source, and
pins behavior no existing test already pins. Report the seams covered, the behavior deliberately
left untested, and any test not written because only a weak one was available.
