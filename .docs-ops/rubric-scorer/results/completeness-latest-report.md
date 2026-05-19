# Rubric Scorer — Completeness Dimension

_Generated: 2026-05-19T07:35:28Z · model: ? · rubric: v0.1.0_

## Headline

**Average score:** 3.40 / 5 across 10 pages

**Score distribution:**

```
  5 |  (0)
  4 | ████ (4)
  3 | ██████ (6)
  2 |  (0)
  1 |  (0)
```

## Per-page scores (lowest first)

| Page | Cohort | Score | Confidence | Rationale |
|---|---|---|---|---|
| `core-concepts/content-handling/files-images-and-videos/file.mdx` | western | 🟡 3 | high | Upload, download, and management operations are shown in code examples but without parameter tables — accepted MIME type… |
| `core-concepts/content-handling/files-images-and-videos/image-handling.mdx` | western | 🟡 3 | high | Upload and retrieval code examples are present but the image object's available fields (thumbnailUrl, fileId, size, dime… |
| `getting-started/authentication.mdx` | shared | 🟡 3 | high | The login() call is shown in code but its parameters (userId, displayName, authToken, sessionHandler) are not compiled i… |
| `chat/messaging-features/message-creation/send-a-message.mdx` | eastern | 🟡 3 | high | The page documents multiple message types (text, image, file, custom) with code examples, but has no parameter table for… |
| `chat/messaging-features/message-flagging.mdx` | eastern | 🟡 3 | high | Flag and unflag operations are shown in code across all 4 platforms, but no parameter table documents the AmityContentFl… |
| `core-concepts/user-management/user-operations/update-user-information.mdx` | western | 🟡 3 | high | At 120 lines, all four updatable fields (displayName, description, avatar, metadata) appear in code, but field constrain… |
| `chat/conversation-management/channels/query-channels.mdx` | eastern | 🟢 4 | high | Three well-formatted parameter tables cover all query options with type, required status, and descriptions; return type … |
| `chat/messaging-features/messages/query-and-filter-messages.mdx` | eastern | 🟢 4 | high | Parameter table covers all query options (tags include/exclude, type, isDeleted, subChannelId, threadId) with types and … |
| `social/content-management/posts/retrieval/query-posts.mdx` | western | 🟢 4 | high | Comprehensive parameter table covers all fields (targetId, targetType, types, tags, includeDeleted, sortBy, isDeleted) w… |
| `core-concepts/user-management/user-operations/get-user-information.mdx` | shared | 🟢 4 | high | getUser(), searchUserByDisplayName(), and getUsersByIds() are all shown with code; return types (LiveObject/LiveCollecti… |

## Immediate action items (score ≤ 3)

### `core-concepts/content-handling/files-images-and-videos/file.mdx` — score 3

**Rationale:** Upload, download, and management operations are shown in code examples but without parameter tables — accepted MIME types, maximum file sizes per type, and the structure of the returned file object (URL, fileId, mimeType fields) are not documented.

**Suggestions:**
- Add a table of accepted file types and size limits (the 1 GB Note at the top is good but incomplete — does it apply to all types?).
- Document the AmityFile object structure returned after upload — what fields are available (fileId, url, mimeType, size)?
- Add an error case: what happens if the upload fails mid-stream, and is the partial upload recoverable?

### `core-concepts/content-handling/files-images-and-videos/image-handling.mdx` — score 3

**Rationale:** Upload and retrieval code examples are present but the image object's available fields (thumbnailUrl, fileId, size, dimensions) are not documented; accepted formats are listed in the Note but maximum dimensions are not mentioned.

**Suggestions:**
- Document the AmityImage object structure — which URL fields are available (fullSize, thumbnail, etc.) and when each is populated.
- Add maximum image dimensions (width × height) alongside the 100 MB size limit.
- Document the error case when the image fails MIME-type validation — does the SDK reject at upload or silently fail?

### `getting-started/authentication.mdx` — score 3

**Rationale:** The login() call is shown in code but its parameters (userId, displayName, authToken, sessionHandler) are not compiled into a parameter table — userId constraints (length, allowed characters) and what happens when login is called while already logged in are absent.

**Suggestions:**
- Add a parameter table for the login() function listing userId, displayName (optional), authToken (optional), and sessionHandler with types and constraints.
- Document userId constraints — maximum length, allowed characters, whether it is case-sensitive.
- Add error cases: what happens when login is called with an invalid API key, an expired auth token, or while a session is already active?

### `chat/messaging-features/message-creation/send-a-message.mdx` — score 3

**Rationale:** The page documents multiple message types (text, image, file, custom) with code examples, but has no parameter table for the core createTextMessage/createImageMessage APIs — parameter names appear only in code, without descriptions of what each accepts, type constraints, or whether they are required.

**Suggestions:**
- Add a parameter table for each message-creation function listing name, type, required/optional, and description.
- Document the return value — what does the create call return and what does the sync state lifecycle look like on success vs failure?
- Add an explicit error-case section: what happens if subChannelId is invalid, if the user lacks send permission, or if the network is unavailable during creation?

### `chat/messaging-features/message-flagging.mdx` — score 3

**Rationale:** Flag and unflag operations are shown in code across all 4 platforms, but no parameter table documents the AmityContentFlagReason enum values — the page uses .others('reason') in code without listing all valid reason cases or describing what the optional custom string field accepts.

**Suggestions:**
- Add a table of all AmityContentFlagReason enum values with descriptions (spam, inappropriate, etc.) and note which cases accept a custom string.
- Document the return type of flagMessage() and unflagMessage() — do they return void, throw on failure, or return a success/failure indicator?
- Add an error case: what happens if the caller tries to flag a message they already flagged, or unflag one they didn't flag?

### `core-concepts/user-management/user-operations/update-user-information.mdx` — score 3

**Rationale:** At 120 lines, all four updatable fields (displayName, description, avatar, metadata) appear in code, but field constraints are absent — no documentation of maximum displayName length, allowed metadata structure/size, or what the return value is on success.

**Suggestions:**
- Add field constraints: maximum character limits for displayName and description, and maximum key/value count for metadata.
- Document the return type of the update call — does it return the updated user object, void, or a success Boolean?
- Add an error case: what happens if displayName exceeds the maximum length — does it truncate or throw?

## Top suggestions across all pages

- Add a table of accepted file types and size limits (the 1 GB Note at the top is good but incomplete — does it apply to all types?).
- Document the AmityFile object structure returned after upload — what fields are available (fileId, url, mimeType, size)?
- Add an error case: what happens if the upload fails mid-stream, and is the partial upload recoverable?
- Document the AmityImage object structure — which URL fields are available (fullSize, thumbnail, etc.) and when each is populated.
- Add maximum image dimensions (width × height) alongside the 100 MB size limit.
- Document the error case when the image fails MIME-type validation — does the SDK reject at upload or silently fail?
- Add a parameter table for the login() function listing userId, displayName (optional), authToken (optional), and sessionHandler with types and constraints.
- Document userId constraints — maximum length, allowed characters, whether it is case-sensitive.
- Add error cases: what happens when login is called with an invalid API key, an expired auth token, or while a session is already active?
- Add a parameter table for each message-creation function listing name, type, required/optional, and description.

## Detailed suggestions by page

**`core-concepts/content-handling/files-images-and-videos/file.mdx`** (score 3, high confidence)
- Add a table of accepted file types and size limits (the 1 GB Note at the top is good but incomplete — does it apply to all types?).
- Document the AmityFile object structure returned after upload — what fields are available (fileId, url, mimeType, size)?
- Add an error case: what happens if the upload fails mid-stream, and is the partial upload recoverable?

**`core-concepts/content-handling/files-images-and-videos/image-handling.mdx`** (score 3, high confidence)
- Document the AmityImage object structure — which URL fields are available (fullSize, thumbnail, etc.) and when each is populated.
- Add maximum image dimensions (width × height) alongside the 100 MB size limit.
- Document the error case when the image fails MIME-type validation — does the SDK reject at upload or silently fail?

**`getting-started/authentication.mdx`** (score 3, high confidence)
- Add a parameter table for the login() function listing userId, displayName (optional), authToken (optional), and sessionHandler with types and constraints.
- Document userId constraints — maximum length, allowed characters, whether it is case-sensitive.
- Add error cases: what happens when login is called with an invalid API key, an expired auth token, or while a session is already active?

**`chat/messaging-features/message-creation/send-a-message.mdx`** (score 3, high confidence)
- Add a parameter table for each message-creation function listing name, type, required/optional, and description.
- Document the return value — what does the create call return and what does the sync state lifecycle look like on success vs failure?
- Add an explicit error-case section: what happens if subChannelId is invalid, if the user lacks send permission, or if the network is unavailable during creation?

**`chat/messaging-features/message-flagging.mdx`** (score 3, high confidence)
- Add a table of all AmityContentFlagReason enum values with descriptions (spam, inappropriate, etc.) and note which cases accept a custom string.
- Document the return type of flagMessage() and unflagMessage() — do they return void, throw on failure, or return a success/failure indicator?
- Add an error case: what happens if the caller tries to flag a message they already flagged, or unflag one they didn't flag?

**`core-concepts/user-management/user-operations/update-user-information.mdx`** (score 3, high confidence)
- Add field constraints: maximum character limits for displayName and description, and maximum key/value count for metadata.
- Document the return type of the update call — does it return the updated user object, void, or a success Boolean?
- Add an error case: what happens if displayName exceeds the maximum length — does it truncate or throw?

**`chat/conversation-management/channels/query-channels.mdx`** (score 4, high confidence)
- Add a note on pagination limits — what is the maximum page size and what happens when the collection reloads?
- Document what happens when displayName search returns no matches — does the collection emit an empty array or an error?

**`chat/messaging-features/messages/query-and-filter-messages.mdx`** (score 4, high confidence)
- Document the behavior when includingTags and excludingTags have overlapping values — does the SDK throw, filter to empty, or favor one set?
- Add a note on the maximum number of tags that can be specified per filter.

**`social/content-management/posts/retrieval/query-posts.mdx`** (score 4, high confidence)
- Add a note on maximum array sizes for types and tags parameters.
- Document whether an empty types array behaves the same as omitting the parameter.

**`core-concepts/user-management/user-operations/get-user-information.mdx`** (score 4, high confidence)
- Document the pagination parameters for searchUserByDisplayName — page size, whether cursor-based or offset, and maximum results per query.
- Add a note on getUsersByIds() limits — is there a maximum number of IDs per call?

---
_Generated by `.docs-ops/rubric-scorer/render-report.py`_
