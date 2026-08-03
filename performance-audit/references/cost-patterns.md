# Cost Patterns

Patterns that make a candidate into a finding. Each one needs a traced path and an input size or a
frequency before it counts. Translate every pattern into the project's own runtime and idiom.

A pattern found on code that never runs, runs once, or runs over a bounded input is not a finding.
Say so and move on.

## Repeated work

- Work performed once per element that could be performed once for the whole collection: formatting,
  parsing, locale or timezone construction, regular-expression compilation, configuration lookup,
  permission checks, capability checks.
- Derivation recomputed on every read where the inputs did not change, especially sorting,
  filtering, grouping, and aggregation feeding something that renders or serializes.
- The same value fetched, computed, or validated by several layers of one request because no layer
  trusts the one before it.
- Startup work duplicated across services that each initialize the same thing.

## Access patterns

- N+1: one query, request, or file read per element of a collection that could be one batched call.
- A broad fetch or full scan where the consumer needs one bounded slice, especially when the slice
  is knowable before the call.
- Nested iteration over two collections that both grow with real input, when a lookup structure
  would remove the inner loop.
- Pagination implemented by fetching everything and slicing in memory.
- Missing index, or a query whose filter cannot use the index that exists.

## Blocking and scheduling

- Synchronous input or output on the thread the user waits on: disk, network, database, inter-process
  calls, or permission prompts inside a UI event, a render pass, or a request handler that could
  have returned first.
- Work that must be off the critical path but was never moved: notification scheduling, cache
  warming, index rebuilds, telemetry, cleanup.
- Serial execution of independent operations that could overlap, and the opposite: unbounded
  parallelism that overwhelms a pool, a rate limit, or the disk.
- Polling where an event, subscription, or notification already exists.
- Timers and observers that stay registered after their subject is gone, so the work continues with
  nobody to receive it.
- Retry without backoff, or retry over an error that will never succeed.

## Rendering and reactive layers

Where the project has a UI or any invalidate-and-recompute layer:

- Expensive work inside the function that recomputes on every change, rather than derived once
  outside it.
- State stored higher in the tree than the thing it changes, so an unrelated update invalidates a
  wide subtree.
- Lifecycle or change hooks that redo the same work on every appearance, not only on real change.
- Layout, measurement, or geometry passes triggered per element.
- Effects that write state which retriggers the same effect.
- A custom component that reimplements a platform primitive at a higher rendering cost, without a
  behavior that justifies it.

## Memory and storage growth

These are the findings a snapshot profile never catches. Look for what only grows.

- A cache with no eviction policy, no size bound, and no retention window.
- Logs, artifacts, temporary files, or generated state written to a location nothing cleans.
- Collections that accumulate for the process lifetime because removal was never implemented.
- Large payloads retained after the consumer finished with them, including references held by
  closures, observers, or listeners that outlive their subject.
- Derived or fully reconstructible state written to durable storage on every change.
- Duplicate persisted rows produced by unstable identity matching.
- Reading a whole file, response, or result set into memory where streaming is available and the
  input is unbounded.
- Maintenance or compaction that runs far more often, or over far more data, than the change rate
  requires.

## External cost

- Per-call cost, rate limits, or quota consumed by a call that is repeated, uncached, or made
  eagerly for data that may never be used.
- A payload requesting far more than the caller reads.
- A dependency pulled into a startup or hot path only for a small part of its surface.

## False-positive guards

- Do not report an optimization the runtime, compiler, database planner, or framework already
  performs. Verify before claiming a missing one.
- Do not report micro-cost on a path that runs once, or over an input the project bounds.
- Do not report a cache as missing without saying what invalidates it. An unmanaged cache is a
  correctness problem wearing a performance costume.
- Do not treat asynchronous code as fast or synchronous code as slow. Trace what each waits on.
- Do not report allocation counts, string concatenation, or collection choice unless a measurement
  or an input size makes the difference matter.
- Do not report a pattern found only in tests, fixtures, tooling, or generated code as a product
  finding.
- Do not accept a previous audit report, a comment, or a variable name as evidence that something is
  already optimized.
