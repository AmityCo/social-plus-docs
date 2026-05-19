# Rubric Scorer — Ai-consumability Dimension

_Generated: 2026-05-19T08:20:52Z · model: ? · rubric: v0.1.0_

## Headline

**Average score:** 3.50 / 5 across 10 pages

**Score distribution:**

```
  5 |  (0)
  4 | █████ (5)
  3 | █████ (5)
  2 |  (0)
  1 |  (0)
```

## Per-page scores (lowest first)

| Page | Cohort | Score | Confidence | Rationale |
|---|---|---|---|---|
| `core-concepts/content-handling/files-images-and-videos/file.mdx` | western | 🟡 3 | high | Frontmatter present and in llms.txt, but description opens with 'Comprehensive guide to file handling…' (genre, not task… |
| `core-concepts/content-handling/files-images-and-videos/image-handling.mdx` | western | 🟡 3 | high | Frontmatter present and in llms.txt, but 7 code blocks are interleaved within prose paragraphs reducing snippet extracta… |
| `getting-started/authentication.mdx` | shared | 🟡 3 | high | 18 code blocks are interleaved within flowing prose (most common pattern: prose sentence → code block → more prose), mak… |
| `core-concepts/user-management/user-operations/get-user-information.mdx` | shared | 🟡 3 | high | Frontmatter description front-loads the task ('Retrieve user profiles and information using the UserRepository with real… |
| `core-concepts/user-management/user-operations/update-user-information.mdx` | western | 🟡 3 | high | Frontmatter description front-loads the task ('Update user profiles, avatars, and metadata using the social.plus SDK') a… |
| `social/content-management/posts/retrieval/query-posts.mdx` | western | 🟢 4 | medium | Frontmatter front-loads the task ('Search and filter posts with advanced querying capabilities for communities and user … |
| `chat/conversation-management/channels/query-channels.mdx` | eastern | 🟢 4 | high | Frontmatter description front-loads the task ('Search and retrieve channels based on various criteria'), 0 interleaved c… |
| `chat/messaging-features/message-creation/send-a-message.mdx` | eastern | 🟢 4 | high | Frontmatter present with task-clear title ('Send a Message'), all code blocks are preceded by headings or blank lines (0… |
| `chat/messaging-features/messages/query-and-filter-messages.mdx` | eastern | 🟢 4 | high | Frontmatter description front-loads the task ('Retrieve and filter messages from channels with advanced querying capabil… |
| `chat/messaging-features/message-flagging.mdx` | eastern | 🟢 4 | high | Frontmatter front-loads intent ('Enable user-driven content moderation with comprehensive flagging capabilities'), 0 int… |

## Immediate action items (score ≤ 3)

### `core-concepts/content-handling/files-images-and-videos/file.mdx` — score 3

**Rationale:** Frontmatter present and in llms.txt, but description opens with 'Comprehensive guide to file handling…' (genre, not task) and 11 code blocks are immediately preceded by mid-sentence prose, making snippet boundaries ambiguous for an AI parser extracting code examples.

**Suggestions:**
- Rewrite description to front-load the primary task: 'Upload, download, and retrieve file metadata using FileRepository across iOS, Android, Flutter, and TypeScript.'
- Precede each code block with a dedicated heading or blank line rather than prose continuation — move inline-annotated calls to a parameter table.
- Add API-named headings (e.g. '## FileRepository.uploadFile()', '## FileRepository.getFile()').

### `core-concepts/content-handling/files-images-and-videos/image-handling.mdx` — score 3

**Rationale:** Frontmatter present and in llms.txt, but 7 code blocks are interleaved within prose paragraphs reducing snippet extractability, and the description ('Advanced image handling with social.plus SDK including upload, processing, optimization…') lists features rather than front-loading the primary operation.

**Suggestions:**
- Move inline-annotated code to standalone blocks preceded by headings — resolve the 7 interleaved instances.
- Rewrite description: 'Upload images and retrieve processed URLs (thumbnail, full-size) using ImageRepository across all four platforms.'
- Add API-named headings ('## ImageRepository.uploadImage()', '## Image URL variants').

### `getting-started/authentication.mdx` — score 3

**Rationale:** 18 code blocks are interleaved within flowing prose (most common pattern: prose sentence → code block → more prose), making snippet extraction ambiguous; the description 'Authentication is required to access social.plus features. This comprehensive guide…' describes the page genre rather than the primary operation (login with userId + authToken).

**Suggestions:**
- Restructure the page to give each code block its own heading ('### Basic Login', '### Login with Auth Token', '### Session Handler') — resolving the 18 interleaved instances.
- Rewrite description: 'Log in to social.plus using Client.login(userId, authToken) and manage session lifecycle with sessionHandler across all four platforms.'
- Add canonical API headings ('## Client.login()', '## Session Handler Lifecycle') for anchor linking.

### `core-concepts/user-management/user-operations/get-user-information.mdx` — score 3

**Rationale:** Frontmatter description front-loads the task ('Retrieve user profiles and information using the UserRepository with real-time updates') and page is in llms.txt, but 8 code blocks immediately follow prose sentences without intervening headings, reducing AI-parser extractability across the three operations (getUser, searchByDisplayName, getUsersByIds).

**Suggestions:**
- Add a dedicated heading before each code block for each operation ('### getUser()', '### searchUserByDisplayName()', '### getUsersByIds()').
- Add API-named headings at the section level ('## UserRepository.getUser()', '## UserRepository.searchUserByDisplayName()') for canonical anchor linking.
- The llms.txt description could include method names: 'Retrieve user profiles using UserRepository.getUser(), search by display name, or fetch multiple users by ID.'

### `core-concepts/user-management/user-operations/update-user-information.mdx` — score 3

**Rationale:** Frontmatter description front-loads the task ('Update user profiles, avatars, and metadata using the social.plus SDK') and page is in llms.txt, but 4 code blocks follow inline prose introducing them mid-sentence, reducing extractability for AI agents parsing the page.

**Suggestions:**
- Precede each code block with a dedicated heading ('### Update Display Name', '### Update Avatar') rather than a prose sentence ending in a colon.
- Add an API-named heading: '## UserRepository.updateUser()' to enable canonical anchor linking.
- Tighten llms.txt description to include the SDK method: 'Update displayName, description, avatar, and metadata for the authenticated user using UserRepository.updateUser().'

## Top suggestions across all pages

- Rewrite description to front-load the primary task: 'Upload, download, and retrieve file metadata using FileRepository across iOS, Android, Flutter, and TypeScript.'
- Precede each code block with a dedicated heading or blank line rather than prose continuation — move inline-annotated calls to a parameter table.
- Add API-named headings (e.g. '## FileRepository.uploadFile()', '## FileRepository.getFile()').
- Move inline-annotated code to standalone blocks preceded by headings — resolve the 7 interleaved instances.
- Rewrite description: 'Upload images and retrieve processed URLs (thumbnail, full-size) using ImageRepository across all four platforms.'
- Add API-named headings ('## ImageRepository.uploadImage()', '## Image URL variants').
- Restructure the page to give each code block its own heading ('### Basic Login', '### Login with Auth Token', '### Session Handler') — resolving the 18 interleaved instances.
- Rewrite description: 'Log in to social.plus using Client.login(userId, authToken) and manage session lifecycle with sessionHandler across all four platforms.'
- Add canonical API headings ('## Client.login()', '## Session Handler Lifecycle') for anchor linking.
- Add a dedicated heading before each code block for each operation ('### getUser()', '### searchUserByDisplayName()', '### getUsersByIds()').

## Detailed suggestions by page

**`core-concepts/content-handling/files-images-and-videos/file.mdx`** (score 3, high confidence)
- Rewrite description to front-load the primary task: 'Upload, download, and retrieve file metadata using FileRepository across iOS, Android, Flutter, and TypeScript.'
- Precede each code block with a dedicated heading or blank line rather than prose continuation — move inline-annotated calls to a parameter table.
- Add API-named headings (e.g. '## FileRepository.uploadFile()', '## FileRepository.getFile()').

**`core-concepts/content-handling/files-images-and-videos/image-handling.mdx`** (score 3, high confidence)
- Move inline-annotated code to standalone blocks preceded by headings — resolve the 7 interleaved instances.
- Rewrite description: 'Upload images and retrieve processed URLs (thumbnail, full-size) using ImageRepository across all four platforms.'
- Add API-named headings ('## ImageRepository.uploadImage()', '## Image URL variants').

**`getting-started/authentication.mdx`** (score 3, high confidence)
- Restructure the page to give each code block its own heading ('### Basic Login', '### Login with Auth Token', '### Session Handler') — resolving the 18 interleaved instances.
- Rewrite description: 'Log in to social.plus using Client.login(userId, authToken) and manage session lifecycle with sessionHandler across all four platforms.'
- Add canonical API headings ('## Client.login()', '## Session Handler Lifecycle') for anchor linking.

**`core-concepts/user-management/user-operations/get-user-information.mdx`** (score 3, high confidence)
- Add a dedicated heading before each code block for each operation ('### getUser()', '### searchUserByDisplayName()', '### getUsersByIds()').
- Add API-named headings at the section level ('## UserRepository.getUser()', '## UserRepository.searchUserByDisplayName()') for canonical anchor linking.
- The llms.txt description could include method names: 'Retrieve user profiles using UserRepository.getUser(), search by display name, or fetch multiple users by ID.'

**`core-concepts/user-management/user-operations/update-user-information.mdx`** (score 3, high confidence)
- Precede each code block with a dedicated heading ('### Update Display Name', '### Update Avatar') rather than a prose sentence ending in a colon.
- Add an API-named heading: '## UserRepository.updateUser()' to enable canonical anchor linking.
- Tighten llms.txt description to include the SDK method: 'Update displayName, description, avatar, and metadata for the authenticated user using UserRepository.updateUser().'

**`social/content-management/posts/retrieval/query-posts.mdx`** (score 4, medium confidence)
- Add '## PostRepository.getPosts()' as a canonical API heading.
- The 4 mild interleaved blocks could be converted to standalone examples under their own subheadings ('### Filter by Post Type', '### Filter by Tags') for cleaner extraction.

**`chat/conversation-management/channels/query-channels.mdx`** (score 4, high confidence)
- Add canonical API headings such as '## ChannelRepository.getChannels()' to enable direct anchor linking.
- The llms.txt description could be slightly tighter — current: 'Search and retrieve channels based on various criteria including display name, tags, membership stat…' — truncated; ensure the full description fits within 150 chars.

**`chat/messaging-features/message-creation/send-a-message.mdx`** (score 4, high confidence)
- Add API-named headings (e.g. '## createTextMessage()', '## createImageMessage()') so agents can anchor-link directly to each method.
- Rewrite description to front-load the primary task: e.g. 'Send text, image, file, and custom messages to a channel using MessageRepository across all four platforms.'

**`chat/messaging-features/messages/query-and-filter-messages.mdx`** (score 4, high confidence)
- Add API-named headings ('## MessageRepository.getMessages()', '## Query by Tags', '## Filter by Message Type') to support canonical anchor linking.
- The filtering variant sections ('Filter by Tags', 'Filter by Type') could each carry a brief one-line API signature in the heading description.

**`chat/messaging-features/message-flagging.mdx`** (score 4, high confidence)
- Add API-named headings for flagMessage(), unflagMessage(), and isFlaggedByMe() to enable canonical anchor links.
- The description could be sharper: 'Flag, unflag, and check flag status on messages using MessageRepository.flagMessage() across all four platforms.'

---
_Generated by `.docs-ops/rubric-scorer/render-report.py`_
