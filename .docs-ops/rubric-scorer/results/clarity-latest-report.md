# Rubric Scorer — Clarity Dimension

_Generated: 2026-05-19T07:12:15Z · model: ? · rubric: v0.1.0_

## Headline

**Average score:** 3.20 / 5 across 10 pages

**Score distribution:**

```
  5 |  (0)
  4 | ███ (3)
  3 | ██████ (6)
  2 | █ (1)
  1 |  (0)
```

## Per-page scores (lowest first)

| Page | Cohort | Score | Confidence | Rationale |
|---|---|---|---|---|
| `chat/messaging-features/message-flagging.mdx` | eastern | 🟠 2 | high | Opens with an Info block reading 'Empower your community to self-moderate by providing robust flagging tools that integr… |
| `core-concepts/content-handling/files-images-and-videos/file.mdx` | western | 🟡 3 | high | Opening sentence uses 'robust' and 'seamless' (marketing adjectives); reader must scan two paragraphs of feature asserti… |
| `core-concepts/content-handling/files-images-and-videos/image-handling.mdx` | western | 🟡 3 | high | Same structural pattern as file.mdx: 'comprehensive image handling capabilities' opener followed by a 'Key Features' Car… |
| `getting-started/authentication.mdx` | shared | 🟡 3 | high | At 950 lines includes both conceptual prose and full SDK setup code for 4 platforms; no one-sentence summary after the t… |
| `chat/messaging-features/message-creation/send-a-message.mdx` | eastern | 🟡 3 | high | Opening sentence describes mechanism not purpose; CardGroup feature overview repeats title metadata before any code is s… |
| `chat/messaging-features/messages/query-and-filter-messages.mdx` | eastern | 🟡 3 | high | Page opens with an Info component (not a sentence) so the first prose is a 'Feature Overview' section header; reader sca… |
| `social/content-management/posts/retrieval/query-posts.mdx` | western | 🟡 3 | high | Opens with 'provides powerful post querying functionality' — 'powerful' and 'flexible' are marketing adjectives; CardGro… |
| `chat/conversation-management/channels/query-channels.mdx` | eastern | 🟢 4 | high | Opens with a clear functional statement about getChannels; headings are scan-friendly; 'comprehensive' in the opening se… |
| `core-concepts/user-management/user-operations/get-user-information.mdx` | shared | 🟢 4 | high | Opens with a direct functional statement answering what the page gives; Live Objects Info block is brief and useful; hea… |
| `core-concepts/user-management/user-operations/update-user-information.mdx` | western | 🟢 4 | high | First sentence directly answers what the page does; at 120 lines the page is tight; two Info prerequisite notes appear b… |

## Immediate action items (score ≤ 3)

### `chat/messaging-features/message-flagging.mdx` — score 2

**Rationale:** Opens with an Info block reading 'Empower your community to self-moderate by providing robust flagging tools that integrate seamlessly' — marketing register; at 587 lines the 'Feature Overview' CardGroup, conceptual moderation workflow, and API reference are interspersed without clear separation.

**Suggestions:**
- Replace the opening Info block: 'Flag a message to report it for moderation; unflag to retract a report.'
- Move the 'Feature Overview' CardGroup to a collapsible section or remove it — it duplicates the section headings below.
- Separate conceptual content (what flagging is) from reference content (how to call the API) into distinct sections.

### `core-concepts/content-handling/files-images-and-videos/file.mdx` — score 3

**Rationale:** Opening sentence uses 'robust' and 'seamless' (marketing adjectives); reader must scan two paragraphs of feature assertions before reaching the first code block.

**Suggestions:**
- Cut both opening paragraphs to one sentence: 'Upload, download, and manage files up to 1 GB using the FileRepository.'
- Remove the 'Key Features' CardGroup — it duplicates section headings and the Note at the top.
- The 'Enterprise-grade security' and 'Optimized global delivery' icon cards read as marketing copy — replace with technical facts.

### `core-concepts/content-handling/files-images-and-videos/image-handling.mdx` — score 3

**Rationale:** Same structural pattern as file.mdx: 'comprehensive image handling capabilities' opener followed by a 'Key Features' CardGroup with marketing-register copy before any code.

**Suggestions:**
- Replace opening paragraph: 'Upload images (max 100 MB; JPEG/PNG/GIF/WebP), access auto-generated thumbnails, and retrieve file URLs.'
- Remove or collapse the 'Key Features' CardGroup.
- The 'Accessibility Support' card mentions alt text — move that detail to the upload API section.

### `getting-started/authentication.mdx` — score 3

**Rationale:** At 950 lines includes both conceptual prose and full SDK setup code for 4 platforms; no one-sentence summary after the title; 'How Auth Tokens Work' section restates the CardGroup above it.

**Suggestions:**
- Add a one-sentence lede: 'Initialize the SDK with your API key, then log in with a user ID and optional auth token.'
- The 'How Auth Tokens Work' sequence diagram restates the CardGroup — cut one or the other.
- Consider splitting into Authentication Concepts and Authentication Implementation to reduce 950-line length.

### `chat/messaging-features/message-creation/send-a-message.mdx` — score 3

**Rationale:** Opening sentence describes mechanism not purpose; CardGroup feature overview repeats title metadata before any code is shown.

**Suggestions:**
- Replace opening sentence with: 'This page shows how to send text, image, file, and custom messages in a channel.'
- Remove or collapse the CardGroup feature overview at the top — it duplicates the title and description metadata.
- The 'Supported Message Types' section links out to sub-pages but re-explains each type in prose — cut the inline explanations.

### `chat/messaging-features/messages/query-and-filter-messages.mdx` — score 3

**Rationale:** Page opens with an Info component (not a sentence) so the first prose is a 'Feature Overview' section header; reader scans two paragraphs before understanding what queryable fields exist.

**Suggestions:**
- Move the opening Info block to after the first code example.
- Replace the 'Feature Overview' CardGroup with a single sentence: 'Query messages by tags, type, thread, or deletion status; results update in real time.'
- The 'Advanced Usage' section restates filtering logic already in the parameter table — cut or consolidate.

### `social/content-management/posts/retrieval/query-posts.mdx` — score 3

**Rationale:** Opens with 'provides powerful post querying functionality' — 'powerful' and 'flexible' are marketing adjectives; CardGroup before the parameter table repeats the table intro in less precise terms.

**Suggestions:**
- Replace opening paragraph: 'Query posts from a community feed or user feed, filtered by post type, tags, or deletion status.'
- Remove the 'Live Collection / Flexible Filtering' CardGroup — the parameter table is the authoritative content.
- The includeDeleted parameter description is 3 sentences with moderation-role nuances — break into a sub-note.

## Top suggestions across all pages

- Replace the opening Info block: 'Flag a message to report it for moderation; unflag to retract a report.'
- Move the 'Feature Overview' CardGroup to a collapsible section or remove it — it duplicates the section headings below.
- Separate conceptual content (what flagging is) from reference content (how to call the API) into distinct sections.
- Cut both opening paragraphs to one sentence: 'Upload, download, and manage files up to 1 GB using the FileRepository.'
- Remove the 'Key Features' CardGroup — it duplicates section headings and the Note at the top.
- The 'Enterprise-grade security' and 'Optimized global delivery' icon cards read as marketing copy — replace with technical facts.
- Replace opening paragraph: 'Upload images (max 100 MB; JPEG/PNG/GIF/WebP), access auto-generated thumbnails, and retrieve file URLs.'
- Remove or collapse the 'Key Features' CardGroup.
- The 'Accessibility Support' card mentions alt text — move that detail to the upload API section.
- Add a one-sentence lede: 'Initialize the SDK with your API key, then log in with a user ID and optional auth token.'

## Detailed suggestions by page

**`chat/messaging-features/message-flagging.mdx`** (score 2, high confidence)
- Replace the opening Info block: 'Flag a message to report it for moderation; unflag to retract a report.'
- Move the 'Feature Overview' CardGroup to a collapsible section or remove it — it duplicates the section headings below.
- Separate conceptual content (what flagging is) from reference content (how to call the API) into distinct sections.

**`core-concepts/content-handling/files-images-and-videos/file.mdx`** (score 3, high confidence)
- Cut both opening paragraphs to one sentence: 'Upload, download, and manage files up to 1 GB using the FileRepository.'
- Remove the 'Key Features' CardGroup — it duplicates section headings and the Note at the top.
- The 'Enterprise-grade security' and 'Optimized global delivery' icon cards read as marketing copy — replace with technical facts.

**`core-concepts/content-handling/files-images-and-videos/image-handling.mdx`** (score 3, high confidence)
- Replace opening paragraph: 'Upload images (max 100 MB; JPEG/PNG/GIF/WebP), access auto-generated thumbnails, and retrieve file URLs.'
- Remove or collapse the 'Key Features' CardGroup.
- The 'Accessibility Support' card mentions alt text — move that detail to the upload API section.

**`getting-started/authentication.mdx`** (score 3, high confidence)
- Add a one-sentence lede: 'Initialize the SDK with your API key, then log in with a user ID and optional auth token.'
- The 'How Auth Tokens Work' sequence diagram restates the CardGroup — cut one or the other.
- Consider splitting into Authentication Concepts and Authentication Implementation to reduce 950-line length.

**`chat/messaging-features/message-creation/send-a-message.mdx`** (score 3, high confidence)
- Replace opening sentence with: 'This page shows how to send text, image, file, and custom messages in a channel.'
- Remove or collapse the CardGroup feature overview at the top — it duplicates the title and description metadata.
- The 'Supported Message Types' section links out to sub-pages but re-explains each type in prose — cut the inline explanations.

**`chat/messaging-features/messages/query-and-filter-messages.mdx`** (score 3, high confidence)
- Move the opening Info block to after the first code example.
- Replace the 'Feature Overview' CardGroup with a single sentence: 'Query messages by tags, type, thread, or deletion status; results update in real time.'
- The 'Advanced Usage' section restates filtering logic already in the parameter table — cut or consolidate.

**`social/content-management/posts/retrieval/query-posts.mdx`** (score 3, high confidence)
- Replace opening paragraph: 'Query posts from a community feed or user feed, filtered by post type, tags, or deletion status.'
- Remove the 'Live Collection / Flexible Filtering' CardGroup — the parameter table is the authoritative content.
- The includeDeleted parameter description is 3 sentences with moderation-role nuances — break into a sub-note.

**`chat/conversation-management/channels/query-channels.mdx`** (score 4, high confidence)
- Replace 'provides comprehensive search capabilities' with: 'lets you filter channels by display name, tags, membership status, and channel type.'
- The CardGroup under 'Query Capabilities' duplicates the parameter table below — remove it.

**`core-concepts/user-management/user-operations/get-user-information.mdx`** (score 4, high confidence)
- Merge opening sentence and Info block: 'Use UserRepository to retrieve profiles and user cards; results are Live Objects that update automatically.'
- The 'Observe Users' section repeats the Live Objects concept from the opening Info — trim section intro to one sentence.

**`core-concepts/user-management/user-operations/update-user-information.mdx`** (score 4, high confidence)
- Move the image-upload prerequisite Info block to just before the avatar-update code block.
- The description frontmatter already covers the opening sentence — trim prose to add something new.

---
_Generated by `.docs-ops/rubric-scorer/render-report.py`_
