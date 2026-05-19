# Rubric Scorer — Examples Dimension

_Generated: 2026-05-19T07:46:43Z · model: ? · rubric: v0.1.0_

## Headline

**Average score:** 4.30 / 5 across 10 pages

**Score distribution:**

```
  5 | ███ (3)
  4 | ███████ (7)
  3 |  (0)
  2 |  (0)
  1 |  (0)
```

## Per-page scores (lowest first)

| Page | Cohort | Score | Confidence | Rationale |
|---|---|---|---|---|
| `chat/conversation-management/channels/query-channels.mdx` | eastern | 🟢 4 | high | Query examples are realistic and use current APIs across all four platforms with idiomatic LiveCollection observe patter… |
| `core-concepts/content-handling/files-images-and-videos/file.mdx` | western | 🟢 4 | high | Upload and download examples are realistic and use current APIs with platform-idiomatic async patterns and error callbac… |
| `core-concepts/content-handling/files-images-and-videos/image-handling.mdx` | western | 🟢 4 | high | Image upload and retrieval examples are realistic and idiomatic with error handling present for most platforms, but impo… |
| `chat/messaging-features/messages/query-and-filter-messages.mdx` | eastern | 🟢 4 | high | Examples are realistic and idiomatic across platforms using LiveCollection observers with current API names, but only so… |
| `social/content-management/posts/retrieval/query-posts.mdx` | western | 🟢 4 | high | Examples are realistic and cover all four platforms with idiomatic observer patterns; TypeScript uses the error-in-rende… |
| `core-concepts/user-management/user-operations/get-user-information.mdx` | shared | 🟢 4 | high | All three operations (getUser, searchByDisplayName, getUsersByIds) are shown with realistic usage and platform-idiomatic… |
| `core-concepts/user-management/user-operations/update-user-information.mdx` | western | 🟢 4 | high | Examples are realistic (meaningful displayName, description, metadata values) and idiomatic per platform with error hand… |
| `getting-started/authentication.mdx` | shared | ✅ 5 | high | Authentication examples across all four platforms include sessionHandler callbacks, error handling (Swift do-catch, Kotl… |
| `chat/messaging-features/message-creation/send-a-message.mdx` | eastern | ✅ 5 | high | All four platforms show realistic, current API calls with platform-idiomatic error handling (Swift do-catch, Kotlin try/… |
| `chat/messaging-features/message-flagging.mdx` | eastern | ✅ 5 | high | All four platforms include explicit error handling (Swift do-catch, Kotlin try/catch, Dart try/catch, TS async try/catch… |

## Top suggestions across all pages

- Add .onFailure / catch / onError handlers to the Android (Kotlin), Flutter (Dart), and TypeScript examples to reach score 5.
- Add import statements to the Android and Flutter snippets — the Swift and TS examples have them but Kotlin/Dart don't.
- Add import statements to all four platform code blocks (e.g., `import { FileRepository } from '@amityco/ts-sdk'` for TS).
- Add a brief error-handling example showing what to display to the user when upload fails (network timeout, oversized file).
- Add import statements to all code blocks for standalone extractability.
- Extend the Flutter snippet to show using the returned image URL with an `Image.network()` widget — a realistic production step.
- Apply consistent error handling across all variant examples (filter-by-tags, filter-by-type, etc.) as shown in the base query example.
- Add import statements to Android/Kotlin snippets — currently absent, making them harder to copy standalone.
- Move error handling inline into the Swift and Kotlin observe closures — show `if let error = error { ... }` rather than deferring it to a separate accordion.
- Add import statements to Android/Kotlin and Flutter snippets.

## Detailed suggestions by page

**`chat/conversation-management/channels/query-channels.mdx`** (score 4, high confidence)
- Add .onFailure / catch / onError handlers to the Android (Kotlin), Flutter (Dart), and TypeScript examples to reach score 5.
- Add import statements to the Android and Flutter snippets — the Swift and TS examples have them but Kotlin/Dart don't.

**`core-concepts/content-handling/files-images-and-videos/file.mdx`** (score 4, high confidence)
- Add import statements to all four platform code blocks (e.g., `import { FileRepository } from '@amityco/ts-sdk'` for TS).
- Add a brief error-handling example showing what to display to the user when upload fails (network timeout, oversized file).

**`core-concepts/content-handling/files-images-and-videos/image-handling.mdx`** (score 4, high confidence)
- Add import statements to all code blocks for standalone extractability.
- Extend the Flutter snippet to show using the returned image URL with an `Image.network()` widget — a realistic production step.

**`chat/messaging-features/messages/query-and-filter-messages.mdx`** (score 4, high confidence)
- Apply consistent error handling across all variant examples (filter-by-tags, filter-by-type, etc.) as shown in the base query example.
- Add import statements to Android/Kotlin snippets — currently absent, making them harder to copy standalone.

**`social/content-management/posts/retrieval/query-posts.mdx`** (score 4, high confidence)
- Move error handling inline into the Swift and Kotlin observe closures — show `if let error = error { ... }` rather than deferring it to a separate accordion.
- Add import statements to Android/Kotlin and Flutter snippets.

**`core-concepts/user-management/user-operations/get-user-information.mdx`** (score 4, high confidence)
- Add import statements to all platform snippets.
- Add error handling to the Flutter getUsersByIds example — the Swift and Kotlin versions show it but Dart is missing it.

**`core-concepts/user-management/user-operations/update-user-information.mdx`** (score 4, high confidence)
- Add import statements (e.g., `import { UserRepository } from '@amityco/ts-sdk'`) to each platform snippet.
- Show a concrete completion handler or callback that confirms the update succeeded, as a production app would typically show a success toast or navigate away.

---
_Generated by `.docs-ops/rubric-scorer/render-report.py`_
