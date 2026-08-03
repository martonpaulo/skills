# Bug Lenses

Use these lenses after reconnaissance. They are hypothesis generators, not finding checklists: report only defects with a reachable trigger, wrong result, and evidence that survives counteranalysis.

## Functional and logic

- Inverted conditions, wrong comparisons, off-by-one boundaries, precedence and coercion errors, unreachable or accidentally reachable branches.
- State-machine transitions that skip prerequisites, permit illegal transitions, repeat irreversible work, or leave partial state after failure.
- Caller/callee assumption mismatches, inconsistent defaults, wrong units, time zones, rounding, encoding, localization, pagination, and ordering.
- Missing valid-input cases and incorrect handling of zero, empty, null, duplicate, maximum, minimum, negative, expired, or reordered values.

## Runtime and resilience

- Null dereferences, crashes, unhandled async failures, swallowed errors, false success, retry storms, non-idempotent retries, leaks, and cleanup that does not run on every exit.
- Partial failure across multi-step operations, missing rollback/compensation, transaction boundaries that exclude related writes, and caches that diverge from their source of truth.
- Framework lifecycle or threading assumptions that differ from actual documented behavior.
- Resource, timeout, cancellation, and backpressure paths with a concrete normal-use or attacker-controlled trigger.

## Concurrency and data integrity

- Read-modify-write races, TOCTOU checks, duplicate delivery, lost updates, stale reads, lock-order cycles, and shared mutable state without the coordination the runtime requires.
- Idempotency keys with incorrect scope or lifetime, retry handlers that duplicate side effects, and background work that acknowledges before durable completion.
- Serialization, migration, schema, or API changes that silently truncate, reinterpret, or drop persisted data.

## Contracts and boundaries

- External input reaching a sink with weaker validation than its callers assume.
- Authentication checked without authorization, tenant/owner identifiers trusted from the client, or privileged internal functions reachable through a weaker path.
- Errors caught at one boundary but interpreted as success at another.
- Request, response, event, callback, persistence, or SDK contracts that disagree across modules or versions.
- Configuration and deployment assumptions count only when verified from repository evidence; do not assume a missing proxy, secret store, or platform control.

## Security

- Injection into SQL, commands, templates, paths, URLs, headers, logs with downstream interpretation, or deserializers.
- Authorization bypass, insecure direct-object access, confused-deputy flows, tenant isolation failure, session/token lifecycle defects, and sensitive response overexposure.
- Path traversal, unsafe archive extraction, server-side request forgery with attacker control over destination, unsafe redirects, insecure deserialization, and cross-site request or script execution where framework protections do not apply.
- Cryptographic misuse only when the primitive protects a relevant asset and the threat is reachable; a deprecated name alone is not a demonstrated bug.
- Dependency advisories only after verifying the resolved version, authoritative advisory, vulnerable behavior, and reachability from this code.

## False-positive guards

- Trace middleware, validation, framework defaults, transactions, locks, callers, and deployment configuration before claiming a missing protection.
- Do not report style, naming, duplication, TODOs, missing tests, theoretical hardening, or unavailable optional defenses as bugs.
- Do not infer races merely because code is asynchronous, injection merely because input is concatenated outside a sink, or memory corruption in memory-safe code without unsafe/native boundaries.
- Do not treat trusted administrator configuration, environment variables, or local CLI arguments as hostile unless the product threat model says otherwise.
- Do not report a vulnerability that requires an impossible state, dead path, or control the attacker does not possess.
- Treat dependency scanner output and static analyzer warnings as candidates until code reachability and version applicability are verified.

## Verification ladder

Use the strongest safe level available:

1. Direct local reproduction with a benign input and observed wrong result.
2. Existing focused test that exercises the exact behavior.
3. Deterministic trace through all relevant code and documented framework behavior.
4. Strong trace with one unverified environmental assumption: `High confidence`, not confirmed.
5. Pattern match or suspicion only: dismiss or leave as a lead, not a reported bug.
