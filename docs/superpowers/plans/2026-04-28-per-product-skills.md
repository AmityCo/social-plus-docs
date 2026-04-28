# Per-Product Skill Files Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create four lightweight per-product Mintlify skill files (Chat, Social, Video, UIKit) that orient AI agents quickly, then explicitly hand off to the MCP `search_social_plus` tool and `llms.txt` for deep content.

**Architecture:** Four `SKILL.md` files live under `.mintlify/skills/<product>/`. Each is ~60–80 lines: frontmatter, when-to-use, core concepts, MCP search guidance, and key doc links. No API signatures (those live in docs and go stale). Mintlify auto-exposes them at `/.well-known/agent-skills/index.json`.

**Tech Stack:** Markdown with YAML frontmatter (Mintlify skill spec). No code, no build step.

---

### Task 1: Create `.mintlify/skills/chat/SKILL.md`

**Files:**
- Create: `.mintlify/skills/chat/SKILL.md`

- [ ] **Step 1: Create the directory and write the file**

```bash
mkdir -p /path/to/social-plus-docs/.mintlify/skills/chat
```

File content for `.mintlify/skills/chat/SKILL.md`:

```markdown
---
name: social.plus Chat
description: Use when building chat features — channels, direct messages, group conversations, real-time messaging, unread counts, read receipts, or moderation in chat contexts.
license: MIT
metadata:
  author: social.plus
  version: "1.0"
---

# social.plus Chat Skill

## When to Use

Reach for this skill when implementing:
- Channel creation (community channels, live channels, direct/group conversations)
- Sending, editing, deleting, or reacting to messages
- Real-time message lists and typing indicators
- Unread count management and read receipt marking
- Channel membership (join, leave, ban, mute users)
- Push notifications for chat events

## Core Concepts

**Channel** — the container for messages. Three types:
- `community` — tied to a Community; members follow community membership
- `live` — tied to a broadcast Room; auto-created with the Room
- `conversation` — direct message or group chat; created explicitly with member list

**Message** — content inside a channel. Built-in types: text, image, file, audio, video, custom. Custom type lets you define any schema.

**Live Collection** — real-time subscription on a message list or channel list. Always call `.dispose()` / unsubscribe when the UI component unmounts. Forgetting this is the single most common memory leak.

**Membership** — each channel tracks its own member list. Ban and mute are channel-scoped by default, not global.

**Unread count** — tracked per user per channel. Viewing messages does not auto-mark them as read; you must call the mark-as-read API explicitly.

## MCP Search Guidance

Use the `search_social_plus` MCP tool with these queries for detailed API docs and code examples:

| Goal | Suggested query |
|------|----------------|
| Create a channel | `"create channel"` or `"channel creation conversation"` |
| Send a message | `"send message createMessage"` |
| Real-time message list | `"message collection live object"` |
| Unread counts | `"unread count channel"` |
| Read receipts | `"mark messages as read"` |
| Typing indicators | `"typing indicator"` |
| Ban or mute a user | `"ban user channel"` or `"mute member"` |
| Push notifications | `"push notification chat channel"` |
| Custom message types | `"custom message type"` |

## Key Documentation

- Full page index: https://learn.social.plus/llms.txt
- Chat overview: https://learn.social.plus/social-plus-sdk/chat/overview
- Messaging features: https://learn.social.plus/social-plus-sdk/chat/messaging-features
- Conversation management: https://learn.social.plus/social-plus-sdk/chat/conversation-management
- Moderation in chat: https://learn.social.plus/social-plus-sdk/chat/moderation-safety
```

- [ ] **Step 2: Verify file structure is correct**

```bash
cat social-plus-docs/.mintlify/skills/chat/SKILL.md | head -10
```
Expected: YAML frontmatter starting with `---` and `name: social.plus Chat`

- [ ] **Step 3: Commit**

```bash
git add .mintlify/skills/chat/SKILL.md
git commit -m "feat: add chat skill for Mintlify MCP"
```

---

### Task 2: Create `.mintlify/skills/social/SKILL.md`

**Files:**
- Create: `.mintlify/skills/social/SKILL.md`

- [ ] **Step 1: Write the file**

File content for `.mintlify/skills/social/SKILL.md`:

```markdown
---
name: social.plus Social
description: Use when building social features — user profiles, communities, posts, comments, reactions, feeds, stories, follow/unfollow, or content moderation.
license: MIT
metadata:
  author: social.plus
  version: "1.0"
---

# social.plus Social Skill

## When to Use

Reach for this skill when implementing:
- User profile creation, search, follow/unfollow, block/unblock
- Community creation, membership, roles, and permissions
- Post creation (text, image, video, poll) targeting communities or user profiles
- Comments and nested replies on posts
- Reactions (named, e.g. "like") on posts, comments, and stories
- News feeds (global, community, or user-specific)
- Stories (ephemeral 24h content with view impressions)
- Content moderation: user flagging, AI filtering, manual review queue

## Core Concepts

**User** — the account identity. Follow/unfollow relationships are directional (A follows B ≠ B follows A). Block is mutual visibility removal.

**Community** — a group space with members, roles, and a feed. Default roles: `community-moderator` and `member`. Permissions are role-based and configurable in the Admin Console.

**Post** — a content unit. Targets either a community (`targetType: "community"`) or a user profile (`targetType: "user"`). Types: text, image, video, poll, liveStream. Images and videos must be uploaded first to get a `fileId`.

**Feed** — an ordered, paginated collection of posts. Types: global feed, community feed, user feed. All support Live Collections for real-time updates.

**Story** — ephemeral content that expires after 24 hours. Supports reactions and impression tracking. Not part of the post feed.

**Reaction** — a named emoji-like response (e.g., `"like"`, `"love"`). Can be added to posts, comments, or stories. Reaction names are configurable in the Admin Console.

## MCP Search Guidance

Use the `search_social_plus` MCP tool with these queries:

| Goal | Suggested query |
|------|----------------|
| Create a post | `"create post"` or `"post creation targetType"` |
| Community setup | `"create community"` or `"community management roles"` |
| User follow system | `"follow user"` or `"user relationship"` |
| News feed | `"news feed query"` or `"global feed community feed"` |
| Comments | `"create comment"` or `"comment on post"` |
| Reactions | `"add reaction"` or `"reaction query"` |
| Stories | `"create story"` or `"story impression"` |
| Content moderation | `"flag post"` or `"AI content moderation"` |
| User search | `"search users"` or `"user query"` |

## Key Documentation

- Full page index: https://learn.social.plus/llms.txt
- Social overview: https://learn.social.plus/social-plus-sdk/social
- Posts: https://learn.social.plus/social-plus-sdk/social/posts
- Communities: https://learn.social.plus/social-plus-sdk/social/communities
- Feeds: https://learn.social.plus/social-plus-sdk/social/feed
- Stories: https://learn.social.plus/social-plus-sdk/social/content-management
- User relationships: https://learn.social.plus/social-plus-sdk/social/user-relationship
```

- [ ] **Step 2: Verify file structure**

```bash
cat social-plus-docs/.mintlify/skills/social/SKILL.md | head -10
```
Expected: YAML frontmatter starting with `---` and `name: social.plus Social`

- [ ] **Step 3: Commit**

```bash
git add .mintlify/skills/social/SKILL.md
git commit -m "feat: add social skill for Mintlify MCP"
```

---

### Task 3: Create `.mintlify/skills/video/SKILL.md`

**Files:**
- Create: `.mintlify/skills/video/SKILL.md`

- [ ] **Step 1: Write the file**

File content for `.mintlify/skills/video/SKILL.md`:

```markdown
---
name: social.plus Video
description: Use when building live video features — room creation, broadcasting, co-hosting, viewer chat, recorded playback, or video analytics.
license: MIT
metadata:
  author: social.plus
  version: "1.0"
---

# social.plus Video Skill

## When to Use

Reach for this skill when implementing:
- Creating and managing broadcast rooms
- Starting and stopping a live stream (broadcaster side)
- Inviting co-hosts and managing multi-broadcaster sessions
- Viewer join flow and real-time viewer count
- Live chat during a broadcast (the room's attached channel)
- Accessing recorded playback after a broadcast ends
- Push notifications for broadcast start/end or co-host invitations
- Video analytics (viewer count, watch duration, engagement)

## Core Concepts

**Room** — the session container for a broadcast. Must be created before any streaming starts. A room has settings (title, description, max viewers, recording enabled/disabled).

**Stream Key** — a single-use RTMP credential. Generate a new key for every broadcast session. Reusing a key from a previous session will fail.

**Co-host** — a secondary broadcaster invited into an active room. Invitation flow: broadcaster sends invite → co-host accepts → co-host gets their own stream key → merged into the broadcast. Invitations expire if not accepted in time.

**Live Channel** — a standard chat Channel automatically created alongside each Room. Use it for viewer messages and reactions during the broadcast. Access it via the Room object.

**Recording** — rooms are recorded by default when recording is enabled in room settings. Recordings are not available during the live stream; they become accessible after the room is terminated.

## MCP Search Guidance

Use the `search_social_plus` MCP tool with these queries:

| Goal | Suggested query |
|------|----------------|
| Create a room | `"create room video"` |
| Start broadcasting | `"start broadcast stream key"` |
| Stop a broadcast | `"end broadcast terminate room"` |
| Co-host flow | `"co-host invitation"` or `"invite co host"` |
| Viewer join | `"join room viewer"` |
| Live chat in room | `"live channel room chat"` |
| Recorded playback | `"video recording playback"` |
| Room analytics | `"room analytics viewer count"` |
| Push for broadcasts | `"push notification broadcast"` |

## Key Documentation

- Full page index: https://learn.social.plus/llms.txt
- Video overview: https://learn.social.plus/social-plus-sdk/video-new/overview
- Getting started: https://learn.social.plus/social-plus-sdk/video-new/getting-started
- Broadcasting: https://learn.social.plus/social-plus-sdk/video-new/broadcasting
- Co-hosting: https://learn.social.plus/social-plus-sdk/video-new/broadcasting
- Playback: https://learn.social.plus/social-plus-sdk/video-new/playback
- Analytics: https://learn.social.plus/social-plus-sdk/video-new/analytics
```

- [ ] **Step 2: Verify file structure**

```bash
cat social-plus-docs/.mintlify/skills/video/SKILL.md | head -10
```
Expected: YAML frontmatter starting with `---` and `name: social.plus Video`

- [ ] **Step 3: Commit**

```bash
git add .mintlify/skills/video/SKILL.md
git commit -m "feat: add video skill for Mintlify MCP"
```

---

### Task 4: Create `.mintlify/skills/uikit/SKILL.md`

**Files:**
- Create: `.mintlify/skills/uikit/SKILL.md`

- [ ] **Step 1: Write the file**

File content for `.mintlify/skills/uikit/SKILL.md`:

```markdown
---
name: social.plus UIKit
description: Use when integrating pre-built social.plus UI components — chat lists, message composers, post feeds, user profiles — or customizing their appearance and behavior.
license: MIT
compatibility: iOS (Swift/SwiftUI), Android (Jetpack Compose), React Native, Flutter
metadata:
  author: social.plus
  version: "1.0"
---

# social.plus UIKit Skill

## When to Use

Reach for this skill when:
- Using pre-built UI components instead of building UI from SDK calls
- Customizing the appearance (colors, fonts, icons) of social.plus components
- Overriding default component behavior with your own widgets
- Setting up UIKit for the first time (installation, authentication wiring)
- Working with chat UI: message lists, composers, channel lists, member lists
- Working with social UI: post feeds, post creation, user profiles, community pages
- Implementing Dynamic UI (server-driven component configuration)

## Core Concepts

**UIKit vs SDK** — UIKit wraps the SDK into ready-made UI components. You style and configure them; the SDK handles all the data fetching, real-time updates, and business logic. Use UIKit for faster integration; use the SDK directly when you need full UI control.

**ThemeConfig** — the global theme object. Set colors, typography, icons, and spacing once and all components inherit the values. Platform-specific: `AmityUIKitManagerOptions` (iOS/Android), `AmityUIKitConfig` (React Native), `AmityCoreClientOption` (Flutter).

**Component override** — inject your own widget at specific slots inside a UIKit component (e.g., replace the default message bubble with your own). Each platform uses a different override mechanism — search docs for your platform.

**Dynamic UI** — server-driven configuration for component visibility and behavior. Configure in the Admin Console → UIKit → Dynamic UI. No app update required to toggle features.

**Platform components** — UIKit components are per-platform. A React Native component is not the same as the iOS or Android equivalent, though they cover the same features. Always specify your platform when searching docs.

## MCP Search Guidance

Use the `search_social_plus` MCP tool with these queries:

| Goal | Suggested query |
|------|----------------|
| Install UIKit | `"UIKit installation"` + your platform (e.g., `"UIKit installation React Native"`) |
| Wire authentication | `"UIKit authentication setup"` |
| Chat components | `"UIKit chat components MessageListComponent"` |
| Social/post components | `"UIKit social components PostListComponent"` |
| Theming | `"UIKit theme customization ThemeConfig"` |
| Override a component | `"UIKit component override custom"` |
| Dynamic UI | `"UIKit dynamic UI server-driven"` |
| iOS-specific | `"UIKit iOS Swift SwiftUI"` |
| Android-specific | `"UIKit Android Compose"` |
| React Native-specific | `"UIKit React Native"` |
| Flutter-specific | `"UIKit Flutter"` |

## Key Documentation

- Full page index: https://learn.social.plus/llms.txt
- UIKit overview: https://learn.social.plus/uikit/overview
- Getting started: https://learn.social.plus/uikit/getting-started/overview
- Chat components: https://learn.social.plus/uikit/components/chat
- Social components: https://learn.social.plus/uikit/components/social
- Customization: https://learn.social.plus/uikit/customization/overview
- Platform guides: https://learn.social.plus/uikit/platform-guides
```

- [ ] **Step 2: Verify file structure**

```bash
cat social-plus-docs/.mintlify/skills/uikit/SKILL.md | head -10
```
Expected: YAML frontmatter starting with `---` and `name: social.plus UIKit`

- [ ] **Step 3: Commit**

```bash
git add .mintlify/skills/uikit/SKILL.md
git commit -m "feat: add UIKit skill for Mintlify MCP"
```

---

### Task 5: Update README to document skills

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Add a Skills section to README.md**

Find the section near the bottom of `README.md` (after the GitHub Actions / CI section). Add the following new section before the final paragraph or at the end:

```markdown
## AI Skills (MCP)

social.plus exposes a [Mintlify MCP server](https://mintlify.com/docs/ai/model-context-protocol) at `https://learn.social.plus/mcp`, giving AI coding tools (Claude Code, Cursor, Windsurf, VS Code + Continue) direct access to the documentation.

### Per-Product Skill Files

Four lightweight skill files live under `.mintlify/skills/`. Each one orients an AI agent to a specific product area, then hands off to the MCP search tool and `llms.txt` for deep content:

| Skill | Path | Purpose |
|-------|------|---------|
| Chat | `.mintlify/skills/chat/SKILL.md` | Channels, messages, real-time, unread |
| Social | `.mintlify/skills/social/SKILL.md` | Users, communities, posts, feeds, stories |
| Video | `.mintlify/skills/video/SKILL.md` | Rooms, broadcasting, co-hosting, playback |
| UIKit | `.mintlify/skills/uikit/SKILL.md` | Pre-built components, theming, customization |

Mintlify exposes these via the discovery endpoint at `/.well-known/agent-skills/index.json`.

### Design Principle

The skill files intentionally contain **no API signatures** — those change and live in the docs. Skills describe *what the product does and when to use which API*, then direct the AI to the MCP search tool for current code examples. This keeps skill files durable and low-maintenance.

### Using the MCP Server

Add to your AI tool's config:

```json
{
  "mcpServers": {
    "social-plus": {
      "url": "https://learn.social.plus/mcp"
    }
  }
}
```

Claude Code: `~/.claude/claude_desktop_config.json`
Cursor: Settings → MCP Servers
```

- [ ] **Step 2: Verify README renders correctly**

```bash
grep -n "AI Skills" social-plus-docs/README.md
```
Expected: line number with `## AI Skills (MCP)`

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "docs: add AI Skills (MCP) section to README"
```

---

### Task 6: Verify Mintlify discovery structure

**Files:** No file changes — verification only.

- [ ] **Step 1: Check local file structure is correct**

```bash
find social-plus-docs/.mintlify/skills -name "SKILL.md" | sort
```
Expected output (4 files):
```
social-plus-docs/.mintlify/skills/chat/SKILL.md
social-plus-docs/.mintlify/skills/social/SKILL.md
social-plus-docs/.mintlify/skills/uikit/SKILL.md
social-plus-docs/.mintlify/skills/video/SKILL.md
```

- [ ] **Step 2: Validate all frontmatter is present**

```bash
for f in social-plus-docs/.mintlify/skills/*/SKILL.md; do
  echo "=== $f ==="; head -7 "$f"; echo
done
```
Expected: Each file shows `---`, `name:`, `description:`, `license:`, `metadata:` fields.

- [ ] **Step 3: After merging to main, verify discovery endpoint**

```bash
curl -s https://learn.social.plus/.well-known/agent-skills/index.json | python3 -m json.tool
```
Expected: JSON listing 4 skills (chat, social, video, uikit) with their URLs.

If endpoint returns 404, Mintlify may need a deployment to pick up `.mintlify/skills/`. This is normal — the endpoint only works after the next Mintlify build.

- [ ] **Step 4: After merging to main, verify `/skill.md` redirects to discovery**

```bash
curl -sI https://learn.social.plus/skill.md | grep -i location
```
Expected: `location: /.well-known/skills/index.json` (302 redirect when multiple skills exist).

---

## Self-Review

**Spec coverage check:**
- ✅ 4 per-product skills: chat, social, video, uikit (Tasks 1–4)
- ✅ Each has frontmatter, when-to-use, core concepts, MCP search guidance, key links
- ✅ No API signatures in skill files (durable design principle)
- ✅ Explicitly references `search_social_plus` MCP tool and `llms.txt` in each skill
- ✅ README updated (Task 5)
- ✅ Discovery endpoint verification (Task 6)

**Placeholder scan:** None found. All tasks contain complete file content.

**Type/name consistency:** No code — markdown only. No consistency issues.
