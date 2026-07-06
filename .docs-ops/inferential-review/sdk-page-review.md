You are reviewing one social.plus SDK documentation page locally. This is an inferential review, not a CI gate.

## Goal

Find judgment problems that deterministic checks and doc-as-test may miss:

- platform behavior is technically valid but misleading;
- one section mixes distinct operations;
- examples compile only because hidden scaffolding helps them;
- TypeScript examples are unnecessarily framework-specific;
- product managers cannot tell what capability the page unlocks;
- an AI agent could extract an overgeneralized or unsafe answer.

## Standards

Use these standards:

- SDK pages have archetypes: overview, concept, operation, setup, migration, reference-lite.
- Operation pages should have parameters, task sections, platform snippets grouped with `CodeGroup`, and related topics.
- Overview/setup/concept pages are allowed to use a different shape.
- TypeScript examples should be SDK-native by default; React examples must be intentional, labeled, and visibly imported.
- Live Object / Live Collection wording must be platform-qualified:
  - iOS and TypeScript expose Live Object / Live Collection wrappers.
  - Android may use `Flowable<T>` or platform-specific reactive APIs.
  - Flutter may return `Future<T>` for single-object fetches and paging/live collection APIs where available.
- Inferential findings are local agent guidance. If a finding is repeated and mechanically detectable, mark it as a deterministic rule candidate.

## Severity

- `P1`: likely to mislead implementation or product understanding.
- `P2`: page is shippable but should be fixed before calling it polished.
- `P3`: cosmetic or consistency issue.

## Response Format

Return valid JSON only:

```json
{
  "page": "<path>",
  "page_archetype": "overview|concept|operation|setup|migration|reference-lite|unknown",
  "summary": "<one sentence>",
  "findings": [
    {
      "severity": "P1|P2|P3",
      "line": 0,
      "issue_type": "accuracy|platform_behavior|structure|snippet_quality|ai_consumability|product_clarity|style",
      "finding": "<specific issue>",
      "why_it_matters": "<impact>",
      "suggested_fix": "<actionable fix>",
      "deterministic_rule_candidate": true
    }
  ]
}
```

Use an empty `findings` array only when the page is genuinely polished by these standards.
