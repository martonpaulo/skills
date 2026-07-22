# Runner contract

Invoke `scripts/run.py` with one small Python program. The program must assign its final JSON-serializable value to `result`.

```bash
python3 scripts/run.py "result = search_proposals('concurrency')" --pretty
```

For project-aware queries, bind the read-only repository root on the host:

```bash
python3 scripts/run.py "result = detect_apple_project_context()" --project-path /path/to/repository --pretty
```

Use list comprehensions and dictionary construction to filter responses before they leave the sandbox. Do not return full pages when a title, declaration, availability record, or short section answers the question.

The JSON envelope contains `success`, `result`, execution time, API call count, and error fields when relevant. Validation errors, timeouts, non-serializable values, and oversized output fail the query.
