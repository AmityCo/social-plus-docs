You are scoring a documentation page on the **CROSS-PLATFORM PARITY** dimension of a 6-dimension rubric.

social.plus docs cover 4 SDK platforms: TypeScript, iOS, Android, Flutter. Parity means: when a feature is documented, all platforms get equivalent coverage — same sections, same depth, same terminology.

## Rubric — Cross-platform parity (verbatim from rubric.json v0.1.0)

Cross-platform parity: When a feature exists on multiple platforms (iOS / Android / TypeScript / Flutter), each platform has equivalent coverage: same sections, same depth, same terminology.

| Score | Definition |
|---|---|
| 1 | Feature documented on only one platform despite being implemented in 2+. |
| 2 | All platforms present but page lengths/depth differ by >3x. |
| 3 | All platforms present; minor structural inconsistency. |
| 4 | Same section structure across platforms; equivalent depth. |
| 5 | Parity matrix shows no gaps AND examples follow each platform's idiom (not transliterated). |

## v1 scoring scope

**Single-page judgment only.** You are scoring THIS page in isolation — you do not have sibling pages to compare against.

Judge the page on:
1. **Platform coverage breadth**: Does this page include code examples for multiple platforms? If so, are all 4 platforms present, or are some missing?
2. **Structural equivalence**: When platform-specific sections exist (e.g., tabs, CodeGroup), are the sections equivalent in depth? Or does one platform get 5 sub-steps while another gets 1?
3. **Terminological consistency**: Are concepts named consistently across platforms (e.g., all use "live collection" vs one says "observable"), or does terminology drift between platform sections?
4. **Idiom authenticity**: Do platform sections use their platform's natural idioms (e.g., iOS uses completion handlers / async-await natively; Flutter uses Futures/Streams; TypeScript uses Promises/Observables)? Or do sections look like mechanical transliterations of one platform's style?
5. **Single-platform pages**: If this page covers only one platform (e.g., "iOS quickstart"), assess whether its structure is consistent with what the equivalent page on other platforms would conventionally contain.

**v1 limitation note**: Full parity assessment requires reading sibling pages in parallel. This v1 single-page score reflects within-page balance and structural signals only. v2 multi-file scoring is a planned follow-up.

## Scoring instructions

Be **conservative**: when in doubt, choose the lower score. A page with mixed-depth platform sections should score 2-3, not 4.

Evidence must be specific: cite which platforms are present or absent, which section is deeper, which term is inconsistent.

## Page to score

```
{page_content}
```

## Response format

Respond with **valid JSON only** — no prose before or after:

```json
{
  "score": <int 1-5>,
  "rationale": "<one sentence citing specific evidence — name the platforms, sections, or terms>",
  "confidence": "low|medium|high",
  "suggestions": ["<concrete improvement 1>", "<concrete improvement 2>"]
}
```

Omit `"suggestions"` entirely if score == 5. Include 2-3 suggestions if score <= 4.
Use `"confidence": "low"` if you cannot tell how many platforms the feature exists on from this page alone.
