# Dependencies and Test Seams

Classify dependencies before introducing a seam:

- **In-process behavior:** keep it direct unless separation improves ownership or independent change.
- **Local infrastructure:** prefer a real lightweight local implementation when it gives reliable tests without widening the public interface.
- **Owned remote system:** place transport behind a narrow boundary when policy should remain local and another implementation is useful for tests or deployment.
- **External system:** isolate vendor behavior behind a project-owned interface when compatibility, failure handling, or substitution justifies it.

A second implementation can justify an abstraction, but raw implementation count is not a rule. Lifecycle, ownership, volatility, and failure modes also matter.

Test observable behavior through the narrowest stable seam that represents real use. Internal tests are appropriate for complex private behavior, but callers should not learn internals merely to make tests easy. When replacing a shallow boundary, remove obsolete tests only after equivalent behavior is covered at the new seam.
