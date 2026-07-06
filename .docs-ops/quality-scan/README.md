# Docs quality proxy scan

`proxy-scan.py` — fast, **LLM-free** structural proxies for the three editorial
quality dimensions a 10-page rubric pilot found weakest. Scans the SDK docs in
seconds, zero model cost, and reports defect counts per dimension and per
section.

## What it measures

| Proxy | Flags a page when… | Confidence |
|---|---|---|
| **Parity** | a `<CodeGroup>` shows code for some platforms but is missing a platform without explicitly marking it unavailable, or has a large per-platform depth disparity | high = CodeGroup intent |
| **Clarity** | the opener uses marketing-register words, or the page opens with a component before any functional sentence | — |
| **Completeness** | a page shows a **multi-parameter / options-object** call but ships no parameter table, including any table inside `## Parameters` | precision-filtered |

Each proxy is gated so its count is a *defect* count, not a raw match (e.g. a
single-arg call doesn't demand a param table; a page that legitimately opens
with `<Update>` like a changelog is not a clarity defect).

Changelog pages keep their raw scan fields in JSON, but they are excluded from
the clarity and completeness defect counts because they are not SDK operation
pages.

Parity keeps explicitly unavailable platforms separate from missing platforms,
so pages that say Flutter has no current public API do not count as Flutter
coverage defects.

## Usage

```bash
# Scope to live docs.json pages (recommended — matches what's actually shipped):
python3 .docs-ops/quality-scan/proxy-scan.py --root social-plus-sdk \
  --docs-json docs.json \
  --json-out .docs-ops/quality-scan/scan-latest.json \
  --md-out .docs-ops/quality-scan/scan-latest-report.md

# Whole filesystem (includes non-nav / archived-candidate pages):
python3 .docs-ops/quality-scan/proxy-scan.py --root social-plus-sdk
```

Always pass `--docs-json` for a picture of the *live* docs; without it the scan
includes pages that aren't in navigation.

## Current snapshot

See `scan-latest-report.md`. As of the last run (live pages): clarity is
effectively clear (remaining flags are correct component-first pages like
changelogs); the open levers are **Flutter parity** and **parameter tables**.
