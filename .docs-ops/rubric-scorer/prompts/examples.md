You are scoring a documentation page on the **EXAMPLES** dimension of a 6-dimension rubric.

## Rubric — Examples (verbatim from rubric.json v0.1.0)

Examples: Code examples are runnable, idiomatic for the platform, use current API names, and demonstrate the actual task.

| Score | Definition |
|---|---|
| 1 | Examples reference removed APIs or won't compile. |
| 2 | Examples compile but use deprecated patterns or wrong idioms. |
| 3 | Examples compile and use current APIs but are toy / overly contrived. |
| 4 | Examples are realistic, current, and platform-idiomatic. |
| 5 | Examples are realistic AND include error handling, AND are extractable as standalone snippets. |

## v1 scoring scope

**Single-page judgment.** You are assessing the quality of code examples based on what you can see in the page's code blocks. Evaluate across all platforms (TypeScript, iOS/Swift, Android/Kotlin, Flutter/Dart) present on the page.

When assessing examples, consider:

1. **Compilation / API correctness**: Do the API names match what you'd expect from the current SDK? Any obviously wrong or likely-removed APIs lower the score.
2. **Idiom quality**: Are the examples written in the platform's natural style? (Swift using `do-catch`, Kotlin using `.apply {}` / coroutines, Dart using `async/await`, TypeScript using `async/await` or `Rx` patterns?)
3. **Realism**: Are these plausible production snippets, or toy examples (e.g., `userId: "123"`, no context, no error handling, `let result = ...` with no indication of what happens next)?
4. **Error handling**: Do examples show what happens on failure — `catch`, `onError`, `onFailure`, error callbacks?
5. **Extractability**: Could a developer copy this snippet into their project, add minimal context, and have it work — or does it depend on unexplained global variables, missing imports, or assumed context?

**v2 future-work note**: Examples scoring can be augmented by:
- (a) **Doc-as-test results** — pages with compile-failing snippets are auto-Level-1-or-2 by definition. Cross-referencing `.docs-ops/integration-tests/*/results/latest.json` would make this objective and removes subjectivity from v1 single-page judgment.
- (b) SDK surface JSON — already covered by the regex validator + doc-as-test; redundant here.

Flag (a) as v2 when v1 scores feel uncertain, particularly for pages where error handling is the discriminating factor between score 4 and 5.

**Per-platform score, then aggregate**: If the page has code blocks for multiple platforms, assess each independently, then report the lowest as the overall score (weakest platform drags the page down). If all platforms have equal quality, report that score.

## Scoring instructions

Be **conservative**: when in doubt, score lower. A page where examples compile and are realistic but lack all error handling should score 4, not 5.

Evidence must be specific: name the platform, the API call, and the missing idiom or error-handling pattern.

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
  "rationale": "<one sentence citing the specific platform/API/pattern that set the score>",
  "confidence": "low|medium|high",
  "suggestions": ["<concrete improvement 1>", "<concrete improvement 2>"]
}
```

Omit `"suggestions"` entirely if score == 5. Include 2-3 suggestions if score <= 4.
Use `"confidence": "low"` if you cannot determine whether an API is current or deprecated from the page content alone.
