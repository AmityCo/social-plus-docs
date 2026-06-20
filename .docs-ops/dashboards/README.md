# Docs-Quality Dashboard

This directory contains the tooling for the cohort-aware docs-quality dashboard.

## Concepts

**Cohort**: A named group of pages that share a customer profile.  
Three cohorts are defined in `cohort-tags.json`:

| Cohort | Description |
|---|---|
| `eastern` | Chat-heavy pages most used by Asian markets |
| `western` | Social / media pages most used by Western markets |
| `shared` | Auth, user management, push-notifications — universal |

Pages not in any cohort are bucketed as `other`.

## Files

| File | Purpose |
|---|---|
| `cohort-tags.json` | Page → cohort mapping. `enumerate:` entries walk a subdirectory for `*.mdx` files. |
| `snapshot.py` | Reads all drift + doc-as-test reports and writes a dated JSON snapshot. |
| `render-report.py` | Reads the latest (and previous) snapshot and renders `latest-report.md`. |
| `strict-proof-latest.json` | Latest strict SDK proof run from `check-drift.py --require-doc-as-test all`. |
| `snapshots/` | Archive of daily/weekly snapshots. Committed to git for trend analysis. |
| `latest-report.md` | Auto-generated report. Do not edit manually. |

## Workflow

```sh
# From the repo root:
python3 .docs-ops/dashboards/snapshot.py       # writes snapshots/<date>.json
python3 .docs-ops/ci/check-drift.py --base HEAD --skip-fetch --require-doc-as-test all --json-out .docs-ops/dashboards/strict-proof-latest.json
python3 .docs-ops/dashboards/render-report.py  # writes latest-report.md
```

Run weekly (e.g., as a cron job or CI step) to build trend history.

## Report sections

1. **Headline** — total drift issues, total type-check failures, cohort health scores (% blocks passing), Δ vs last week
2. **Per-platform (regex drift)** — issues broken down by platform and cohort
3. **Per-platform (doc-as-test)** — pass / skip / fail / warn totals + cohort block counts
4. **Trend** — table + ASCII sparkline for the last 8 snapshots
5. **Alerts** — concise list of regressions or open issues

When `strict-proof-latest.json` exists, the report also includes **Strict SDK Proof**: runner availability, compile/type-check counts, regex drift delta, and MDX structure status from the latest strict proof run.

## Snapshot schema

```jsonc
{
  "snapshot_date": "YYYY-MM-DD",
  "snapshot_run_at": "ISO8601Z",
  "regex_drift": {
    "<platform>": { "total": 0, "by_cohort": { "eastern": 0, "western": 0, "shared": 0, "other": 0 } }
  },
  "doc_as_test": {
    "<platform>": {
      "passed": 0, "skipped": 0, "failed": 0, "warnings": 0,
      "by_cohort": {
        "<cohort>": { "passed": 0, "failed": 0, "skipped": 0 }
      }
    }
  },
  "summary": {
    "total_drift_issues": 0,
    "total_doc_as_test_failures": 0,
    "healthy": true,
    "eastern_health_score": 1.0,
    "western_health_score": 1.0
  }
}
```

## Health score

`health_score = 1.0 - (failures / (passed + failed))` across all platforms for the cohort.  
Returns `null` if the cohort has no measured blocks on any platform.
