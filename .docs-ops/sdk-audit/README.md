# SDK Accuracy Audit Tracker

This directory tracks the SDK-first page-by-page accuracy audit. It is deliberately simple: one generated CSV row per `social-plus-sdk/**/*.mdx` page, plus human-editable review columns.

## Generate Or Refresh

```bash
python3 .docs-ops/sdk-audit/build-tracker.py
```

The generator preserves existing review fields by `path`, adds newly created SDK pages, and removes pages that no longer exist.

## Status Values

Use these values in `tracker.csv`:

| Status | Meaning |
|---|---|
| `not_started` | Page has not been reviewed yet. |
| `in_review` | Someone is actively checking the page. |
| `verified` | SDK source, snippets, and information have been reviewed and evidence is recorded. |
| `needs_fix` | The page has a confirmed accuracy or coverage issue. |
| `deferred` | Intentionally out of the current audit pass, with a note explaining why. |

## Review Bar

Do not mark a page `verified` just because the strict proof gate passes. The proof gate is evidence for selected snippets and runner availability. A page-level review should also confirm:

- `source_verified`: the page was checked against the relevant SDK source, generated API surface, changelog, or release tag.
- `snippets_verified`: code snippets compile/type-check or have an explicit skip reason.
- `info_verified`: prose, parameters, platform caveats, and behavior claims match current SDK behavior.
- `evidence`: compact pointer to the proof used, such as SDK repo commit, extractor output, doc-as-test run, or source file.

This tracker is the handoff surface for the full SDK page-by-page pass.
