# Doc-as-Test Framework (TypeScript)

Type-checks every TypeScript code block in a curated set of high-traffic doc pages against the real `@amityco/ts-sdk` source using `tsc --noEmit --strict`.

## What it catches

- Wrong method signatures (missing/extra arguments)
- Wrong argument types
- Wrong async/await patterns
- Non-existent properties
- Import path errors

The regex validator (`ts-accuracy-validator.py`) catches stale API *names*. This catches wrong *shapes*.

## How to run

```bash
cd social-plus-docs

# Step 1 — extract code blocks into results/extracted/
python3 .docs-ops/integration-tests/extract-blocks.py

# Step 2 — type-check each block, emit results/latest.json
python3 .docs-ops/integration-tests/run-tests.py

# Read the report
cat .docs-ops/integration-tests/results/latest.json | python3 -m json.tool | head -60
```

## Reading the report

- `stats.pass_rate` — overall health signal. Target: >90% before wiring as a CI gate.
- `failures[].errors` — first 5 tsc error lines per block.
- `failures[].source_page` + `source_line_range` — jump directly to the offending doc block.
- `by_page` — per-page pass/fail summary; pages with 0 passed usually indicate a preamble gap.

## Preamble gaps vs real doc errors

- `Cannot find name 'X'` → preamble gap (add `declare const X` to `preamble.d.ts`)
- `Property 'X' does not exist on type 'Y'` → real API drift in the doc
- `Expected N arguments, but got M` → wrong call signature in the doc

## Files

| File | Purpose |
|---|---|
| `preamble.d.ts` | Shared `declare const` context variables |
| `pages.json` | Curated page list (edit to add/remove pages) |
| `tsconfig.json` | Compiler config — strict, noEmit, paths to SDK source |
| `extract-blocks.py` | Walks pages.json, writes one `.ts` per code block |
| `run-tests.py` | Runs tsc per block, emits `results/latest.json` |
| `results/latest.json` | Latest run report |
| `results/extracted/` | Generated `.ts` files (gitignored) |
