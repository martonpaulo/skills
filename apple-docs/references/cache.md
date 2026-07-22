# Cache behavior

The runner has no persistent disk cache.

Several providers memoize indexes or fetched metadata in memory for the lifetime of one `scripts/run.py` process. This includes the Swift Evolution index, HIG topic index, and the local Xcode documentation index. Some other network helpers fetch on every call. Starting a new runner process clears all in-memory state.

Local Xcode document content remains on disk inside Xcode; the skill stores only its in-process index. Network responses are not persisted across runs. A failed index fetch is generally left uncached so a later call in the same process can retry.
