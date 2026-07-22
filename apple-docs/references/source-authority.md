# Source authority

Use the order defined in `SKILL.md` and exposed by `get_source_authority()`.

- Official Apple documentation, specifications, and release notes are primary for public API behavior.
- Official Apple and Swift repositories are primary source evidence, but internal implementation details are not public contracts.
- Accepted Swift Evolution proposals are authoritative for accepted language design; pitches and reviews are not accepted behavior.
- Official WWDC pages and transcripts are primary guidance, scoped to the session's SDK and release.
- Apple Developer Forums and Swift Forums are secondary unless they link to a primary contract.
- Community-written WWDC notes and summaries are discovery aids and must be labeled community.

When sources conflict, report the conflict and prefer the source that matches the detected SDK, Xcode, platform, and deployment target. Do not silently generalize behavior across versions.
