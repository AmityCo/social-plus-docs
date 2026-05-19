You are scoring a documentation page on the **CLARITY** dimension of a 6-dimension rubric.

## Rubric — Clarity (verbatim from rubric.json v0.1.0)

Clarity: Plain language. Defines its terms. No marketing fluff. Right-sized for an engineer scanning, not reading.

| Score | Definition |
|---|---|
| 1 | Marketing copy where reference is needed; unexplained jargon. |
| 2 | Mixed registers; some sections explain, some only assert. |
| 3 | Clear but verbose; could be cut 20% without loss. |
| 4 | Tight, terms defined on first use, scan-friendly headings. |
| 5 | Tight AND opens with a one-sentence answer to "what does this page give me". |

## Scoring instructions

Be **conservative**: when in doubt, choose the lower score. It is better to flag a borderline page than to over-grade it.

Evidence must be specific: cite the section name, paragraph number, or a brief quote — not "it's a bit wordy".

Suggestions (if score < 5) must be actionable: a specific change a doc author could make in under 30 minutes.

## Page to score

```
{page_content}
```

## Response format

Respond with **valid JSON only** — no prose before or after:

```json
{
  "score": <int 1-5>,
  "rationale": "<one sentence citing specific evidence from the page>",
  "confidence": "low|medium|high",
  "suggestions": ["<concrete improvement 1>", "<concrete improvement 2>"]
}
```

Omit `"suggestions"` entirely if score == 5. Include 2-3 suggestions if score <= 4.
