You are scoring a documentation page on the **COMPLETENESS** dimension of a 6-dimension rubric.

## Rubric — Completeness (verbatim from rubric.json v0.1.0)

Completeness: All public APIs the page claims to document are actually documented — with parameters, return types, and error cases.

| Score | Definition |
|---|---|
| 1 | Major public APIs missing from a page that claims to document them. |
| 2 | Most APIs covered; several missing parameters, return types, or error cases. |
| 3 | All APIs covered; some parameters lack descriptions or types. |
| 4 | All APIs, parameters, return types, and primary error cases documented. |
| 5 | Adds edge cases, rate limits, and side effects beyond the API signature. |

## v1 scoring scope

**Single-page judgment.** You are judging the page on its own content — you do not have the SDK surface JSON to compare against. Assess completeness based on:

1. **API coverage**: For every API function / method / operation the page title and headings claim to document, are all relevant parameters described?
2. **Parameter documentation**: Are parameter names, types, whether they're required/optional, and their purpose described?
3. **Return type documentation**: Is what the API returns described (e.g., "returns a LiveObject of type AmityUser")?
4. **Error cases**: Are failure conditions called out — what happens if the user ID doesn't exist, if the network is unavailable, if permissions are missing?
5. **Edge cases and limits**: Does the page mention things like rate limits, maximum values, async behavior, side effects, or platform-specific constraints?

**v1 limitation note**: True Completeness validation requires comparing the page against the SDK surface (`.docs-ops/sdk-surface/*.json`) — "here is what the SDK exposes; does this page cover it all?" This v2 surface-augmented approach is planned but skipped here to match the established pilot pattern. v1 single-page scores reflect internal completeness (what the page claims vs what it delivers) rather than external completeness (what the SDK has vs what the page covers).

## Scoring instructions

Be **conservative**: when in doubt, score lower. A page that covers all main parameters but omits error cases should score 3, not 4.

Evidence must be specific: cite the API name, the missing parameter, or the absent error case.

Suggestions must be actionable within 30 minutes.

## Page to score

```
{page_content}
```

## Response format

Respond with **valid JSON only** — no prose before or after:

```json
{
  "score": <int 1-5>,
  "rationale": "<one sentence citing specific evidence — name the API, parameter, or error case>",
  "confidence": "low|medium|high",
  "suggestions": ["<concrete improvement 1>", "<concrete improvement 2>"]
}
```

Omit `"suggestions"` entirely if score == 5. Include 2-3 suggestions if score <= 4.
Use `"confidence": "low"` when you cannot determine what the SDK exposes from the page alone (this is common in v1; v2 surface-augmented scoring will resolve this).
