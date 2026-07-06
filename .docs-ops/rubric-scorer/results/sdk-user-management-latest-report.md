# Rubric Scorer - SDK User Management

_Generated: 2026-06-25T09:43:30Z. Rubric: v0.1.0. Scoring mode: local agent inferential review._

This report refreshes the rubric score for `social-plus-sdk/core-concepts/user-management`. It is intentionally scoped to the SDK user-management section and does not overwrite the historical 10-page pilot reports.

## Headline

**Average score:** 4.00 / 5 across 11 pages.

**Distribution:**

```text
  5 | 0
  4 | 11
  3 | 0
  2 | 0
  1 | 0
```

**Deterministic metrics for the same slice:**

- MDX validation: passed for 11 user-management pages.
- SDK style gate: passed for 11 user-management pages.
- Changed SDK style gate: passed for 10 changed SDK pages.
- Quality proxy scan: 0 parity flags, 0 clarity flags, 0 completeness flags.
- Metrics JSON: `.docs-ops/quality-scan/sdk-user-management-latest.json`

## Caveats

- This is not a CI gate.
- Full doc-as-test was not run for this refresh.
- Accuracy scores are informed by local SDK source spot checks and fast deterministic gates.
- The older `overall-latest-report.md` remains a historical global pilot from 2026-05-19.

## Per-page Scores

| Page | Overall | Acc | Cla | Par | Cmp | Exm | AIc | Confidence |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `core-concepts/user-management/roles-permissions.mdx` | 4.00 | 4 | 4 | 4 | 4 | 4 | 4 | high |
| `core-concepts/user-management/overview.mdx` | 4.00 | 4 | 4 | 4 | 4 | 4 | 4 | high |
| `core-concepts/user-management/user-operations/update-user-information.mdx` | 4.00 | 4 | 4 | 4 | 4 | 4 | 4 | high |
| `core-concepts/user-management/user-operations/delete-user.mdx` | 4.00 | 4 | 4 | 4 | 4 | 4 | 4 | high |
| `core-concepts/user-management/user-operations/flag-unflag-user.mdx` | 4.00 | 4 | 4 | 4 | 4 | 4 | 4 | high |
| `core-concepts/user-management/user-identity.mdx` | 4.00 | 4 | 4 | 4 | 4 | 4 | 4 | high |
| `core-concepts/user-management/user-operations/overview.mdx` | 4.00 | 4 | 4 | 4 | 4 | 4 | 4 | high |
| `core-concepts/user-management/user-operations/create-user.mdx` | 4.00 | 4 | 4 | 4 | 4 | 4 | 4 | high |
| `core-concepts/user-management/user-operations/get-user-information.mdx` | 4.00 | 4 | 4 | 4 | 4 | 4 | 4 | high |
| `core-concepts/user-management/user-operations/search-and-query-users.mdx` | 4.00 | 4 | 4 | 4 | 4 | 4 | 4 | high |
| `core-concepts/user-management/user-operations/user-token-management.mdx` | 4.00 | 4 | 4 | 4 | 4 | 4 | 4 | high |

## Remaining Upgrades Toward 5

1. Add version or availability tags where the SDK surface differs by platform.
2. Add canonical anchors for every public API mentioned.
3. Run full doc-as-test for TypeScript, iOS, Android, and Flutter snippets.
4. Add edge cases such as cache freshness, permission-source timing, and moderation workflow side effects.

## Reading The Scores

- A score of 4 means the page is passing for the current local rubric.
- A score of 5 is reserved for pages with stronger version/availability tags, canonical anchors, edge cases, and fully extractable standalone snippets.
- A score below 4 does not mean the page is wrong; it means the page is either older style, less compact, or not fully verified by the stronger evidence layer yet.

Raw JSON: `.docs-ops/rubric-scorer/results/sdk-user-management-latest.json`
