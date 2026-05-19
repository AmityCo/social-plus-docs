# Rubric Scorer — Parity Dimension

_Generated: 2026-05-19T07:12:02Z · model: ? · rubric: v0.1.0_

## Headline

**Average score:** 3.20 / 5 across 10 pages

**Score distribution:**

```
  5 |  (0)
  4 | ████ (4)
  3 | ████ (4)
  2 | ██ (2)
  1 |  (0)
```

## Per-page scores (lowest first)

| Page | Cohort | Score | Confidence | Rationale |
|---|---|---|---|---|
| `core-concepts/content-handling/files-images-and-videos/file.mdx` | western | 🟠 2 | high | iOS, Android, and TypeScript each have 3 code blocks; Flutter has 1 — a 3x depth disparity with Flutter missing upload-p… |
| `chat/messaging-features/message-creation/send-a-message.mdx` | eastern | 🟠 2 | high | iOS and Android each have 5 code blocks; TypeScript has 1 block; Flutter/Dart has 0 blocks — a >5x depth disparity with … |
| `chat/messaging-features/message-flagging.mdx` | eastern | 🟡 3 | medium | All 4 platforms have 3 code blocks each (balanced coverage), but the iOS section uses async/await patterns while the And… |
| `core-concepts/content-handling/files-images-and-videos/image-handling.mdx` | western | 🟡 3 | high | iOS, Android, and TypeScript each have 2 code blocks; Flutter has 1 — Flutter is missing the image-retrieval/URL section… |
| `getting-started/authentication.mdx` | shared | 🟡 3 | high | All 4 platforms are present with 5-9 blocks each; TypeScript has 9 blocks vs Flutter's 5 — the TypeScript section includ… |
| `chat/messaging-features/messages/query-and-filter-messages.mdx` | eastern | 🟡 3 | high | iOS, Android, and TypeScript each have 3 code blocks; Flutter has 2 — one section (Advanced Filtering) lacks a Flutter e… |
| `chat/conversation-management/channels/query-channels.mdx` | eastern | 🟢 4 | high | All 4 platforms (iOS, Android, TypeScript, Flutter) each have 1 code block in a CodeGroup; parameter table covers all pl… |
| `social/content-management/posts/retrieval/query-posts.mdx` | western | 🟢 4 | high | All 4 platforms have 1 code block each in equivalent CodeGroup structure; the parameter table applies cross-platform; mi… |
| `core-concepts/user-management/user-operations/get-user-information.mdx` | shared | 🟢 4 | high | All 4 platforms have 2 code blocks each (get single user + search/query users) with equivalent structure; each uses its … |
| `core-concepts/user-management/user-operations/update-user-information.mdx` | western | 🟢 4 | high | All 4 platforms have 1 code block in a CodeGroup with equivalent depth; each uses its platform's native pattern (iOS Bui… |

## Immediate action items (score ≤ 3)

### `core-concepts/content-handling/files-images-and-videos/file.mdx` — score 2

**Rationale:** iOS, Android, and TypeScript each have 3 code blocks; Flutter has 1 — a 3x depth disparity with Flutter missing upload-progress and download sections entirely.

**Suggestions:**
- Add Flutter code blocks for upload-with-progress and download sections to match the other 3 platforms.
- If Flutter file handling has a known limitation (e.g., no progress callbacks), document it explicitly with a platform note rather than silently omitting the section.

### `chat/messaging-features/message-creation/send-a-message.mdx` — score 2

**Rationale:** iOS and Android each have 5 code blocks; TypeScript has 1 block; Flutter/Dart has 0 blocks — a >5x depth disparity with two platforms entirely missing or minimally covered.

**Suggestions:**
- Add TypeScript and Flutter code blocks for each major code section (initialize, send text, send image, send file, handle sync state).
- Audit whether Flutter is intentionally excluded (if the feature is mobile-only, document this explicitly with a platform-availability note at the top).

### `chat/messaging-features/message-flagging.mdx` — score 3

**Rationale:** All 4 platforms have 3 code blocks each (balanced coverage), but the iOS section uses async/await patterns while the Android section uses callback-style — terminology for the flag reason enum differs between platforms ('AmityContentFlagReason' vs 'AmityFlagReason').

**Suggestions:**
- Standardize enum naming documentation — call out platform-specific enum names in a terminology note rather than using different names silently.
- Confirm the Flutter section uses idiomatic Dart (Future<void> pattern) rather than a direct translation of the Kotlin callback style.

### `core-concepts/content-handling/files-images-and-videos/image-handling.mdx` — score 3

**Rationale:** iOS, Android, and TypeScript each have 2 code blocks; Flutter has 1 — Flutter is missing the image-retrieval/URL section present in the other 3 platforms.

**Suggestions:**
- Add the Flutter code block for image retrieval/URL access to match iOS, Android, and TypeScript.
- Check that the Flutter upload block uses idiomatic Dart (async/await with File object) rather than a transliteration of the iOS UIImage pattern.

### `getting-started/authentication.mdx` — score 3

**Rationale:** All 4 platforms are present with 5-9 blocks each; TypeScript has 9 blocks vs Flutter's 5 — the TypeScript section includes additional token-refresh and error-handling subsections not mirrored in the Flutter section.

**Suggestions:**
- Add equivalent token-refresh and session-expiry handling examples to the Flutter and iOS sections to match the depth of the TypeScript section.
- The iOS section uses a SessionHandler class pattern not present in other platforms — add a cross-platform note explaining that this is an iOS-specific architectural requirement.

### `chat/messaging-features/messages/query-and-filter-messages.mdx` — score 3

**Rationale:** iOS, Android, and TypeScript each have 3 code blocks; Flutter has 2 — one section (Advanced Filtering) lacks a Flutter example, creating a minor structural inconsistency.

**Suggestions:**
- Add the missing Flutter code block in the Advanced Filtering section to match iOS/Android/TypeScript coverage.
- Verify the Flutter example in the remaining sections uses Dart idioms (Stream/Future patterns) rather than a transliteration of the iOS completion-handler style.

## Top suggestions across all pages

- Add Flutter code blocks for upload-with-progress and download sections to match the other 3 platforms.
- If Flutter file handling has a known limitation (e.g., no progress callbacks), document it explicitly with a platform note rather than silently omitting the section.
- Add TypeScript and Flutter code blocks for each major code section (initialize, send text, send image, send file, handle sync state).
- Audit whether Flutter is intentionally excluded (if the feature is mobile-only, document this explicitly with a platform-availability note at the top).
- Standardize enum naming documentation — call out platform-specific enum names in a terminology note rather than using different names silently.
- Confirm the Flutter section uses idiomatic Dart (Future<void> pattern) rather than a direct translation of the Kotlin callback style.
- Add the Flutter code block for image retrieval/URL access to match iOS, Android, and TypeScript.
- Check that the Flutter upload block uses idiomatic Dart (async/await with File object) rather than a transliteration of the iOS UIImage pattern.
- Add equivalent token-refresh and session-expiry handling examples to the Flutter and iOS sections to match the depth of the TypeScript section.
- The iOS section uses a SessionHandler class pattern not present in other platforms — add a cross-platform note explaining that this is an iOS-specific architectural requirement.

## Detailed suggestions by page

**`core-concepts/content-handling/files-images-and-videos/file.mdx`** (score 2, high confidence)
- Add Flutter code blocks for upload-with-progress and download sections to match the other 3 platforms.
- If Flutter file handling has a known limitation (e.g., no progress callbacks), document it explicitly with a platform note rather than silently omitting the section.

**`chat/messaging-features/message-creation/send-a-message.mdx`** (score 2, high confidence)
- Add TypeScript and Flutter code blocks for each major code section (initialize, send text, send image, send file, handle sync state).
- Audit whether Flutter is intentionally excluded (if the feature is mobile-only, document this explicitly with a platform-availability note at the top).

**`chat/messaging-features/message-flagging.mdx`** (score 3, medium confidence)
- Standardize enum naming documentation — call out platform-specific enum names in a terminology note rather than using different names silently.
- Confirm the Flutter section uses idiomatic Dart (Future<void> pattern) rather than a direct translation of the Kotlin callback style.

**`core-concepts/content-handling/files-images-and-videos/image-handling.mdx`** (score 3, high confidence)
- Add the Flutter code block for image retrieval/URL access to match iOS, Android, and TypeScript.
- Check that the Flutter upload block uses idiomatic Dart (async/await with File object) rather than a transliteration of the iOS UIImage pattern.

**`getting-started/authentication.mdx`** (score 3, high confidence)
- Add equivalent token-refresh and session-expiry handling examples to the Flutter and iOS sections to match the depth of the TypeScript section.
- The iOS section uses a SessionHandler class pattern not present in other platforms — add a cross-platform note explaining that this is an iOS-specific architectural requirement.

**`chat/messaging-features/messages/query-and-filter-messages.mdx`** (score 3, high confidence)
- Add the missing Flutter code block in the Advanced Filtering section to match iOS/Android/TypeScript coverage.
- Verify the Flutter example in the remaining sections uses Dart idioms (Stream/Future patterns) rather than a transliteration of the iOS completion-handler style.

**`chat/conversation-management/channels/query-channels.mdx`** (score 4, high confidence)
- Expand the Flutter code example to match the depth of the iOS/Android blocks — it currently omits the filter options shown in the other platforms.

**`social/content-management/posts/retrieval/query-posts.mdx`** (score 4, high confidence)
- Add equivalent error-handling patterns to the iOS, Android, and Flutter examples, or remove it from TypeScript — asymmetric patterns signal incomplete coverage.

**`core-concepts/user-management/user-operations/get-user-information.mdx`** (score 4, high confidence)
- The TypeScript section uses a different variable naming convention ('liveObject' vs 'liveUser' in other platforms) — standardize for easier cross-platform reading.

**`core-concepts/user-management/user-operations/update-user-information.mdx`** (score 4, high confidence)
- The iOS section uses AmityUserUpdateOptions while the Android section uses a Builder pattern — add a brief note explaining this is an intentional SDK-level difference, not a doc inconsistency.

---
_Generated by `.docs-ops/rubric-scorer/render-report.py`_
