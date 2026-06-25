# Local Inferential SDK Page Review

This layer is for local agent work only. It must not run in CI.

Use it when deterministic checks pass but a page still needs judgment about clarity, platform truthfulness, AI-consumability, or product-reader usefulness.

## Workflow

1. Run deterministic checks first:

```bash
python3 .docs-ops/ci/check-mdx.py <page.mdx>
python3 .docs-ops/ci/check-sdk-style.py <page.mdx>
python3 .docs-ops/ci/check-drift.py --base HEAD --skip-fetch --require-doc-as-test all
```

2. Ask the local agent to review the page with `sdk-page-review.md`.

3. The agent returns structured JSON findings:

```json
{
  "page": "social-plus-sdk/...",
  "summary": "one sentence",
  "findings": [
    {
      "severity": "P1",
      "line": 42,
      "issue_type": "platform_behavior",
      "finding": "The page describes Live Objects as universal.",
      "why_it_matters": "Flutter and Android expose different shapes, so the wording can mislead integrators.",
      "suggested_fix": "Qualify the sentence by platform.",
      "deterministic_rule_candidate": true
    }
  ]
}
```

4. Fix the page and rerun deterministic checks.

5. If the same inferential finding repeats across pages, promote it into `.docs-ops/ci/check-sdk-style.py`.

## What Belongs Here

- Concept separation issues: one section mixes two operations.
- Platform behavior nuance: same feature exists, but return/observe shapes differ.
- Human copy-paste quality: examples compile only because doc-as-test scaffolding helps them.
- AI ambiguity: wording that an AI assistant could overgeneralize.
- Product-reader clarity: page says what exists but not why it matters.

## What Does Not Belong Here

- MDX validity.
- Code fences inside `CardGroup`.
- Missing `CodeGroup` around SDK snippets.
- Known Live Object overgeneralization.
- Known generic TypeScript/React snippet problems.

Those belong in deterministic checks.
