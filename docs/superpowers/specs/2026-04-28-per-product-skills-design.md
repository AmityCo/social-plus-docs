# Design: Per-Product Skill Files for social.plus

## Problem

Mintlify auto-generates a single `skill.md` that covers all of social.plus. This is useful as an overview but too broad for AI agents working on a specific feature area. A developer building a chat feature needs chat-specific guidance, not a 1,000-line file about every SDK.

## Approach

Create four focused skill files under `.mintlify/skills/`, one per product area, plus a root `skill.md` that serves as an overview and links to all four. When Mintlify detects multiple skill files, it exposes a discovery endpoint (`/.well-known/agent-skills/index.json`) and each skill is accessible individually.

## File Layout

```
social-plus-docs/
  skill.md                            ← root overview (overrides Mintlify auto-gen)
  .mintlify/
    skills/
      chat/SKILL.md                   ← Channels, messages, real-time, unread
      social/SKILL.md                 ← Users, communities, posts, feeds, stories
      video/SKILL.md                  ← Rooms, broadcasting, co-hosting, playback
      uikit/SKILL.md                  ← Pre-built components, theming, customization
```

## Content Structure (per skill)

Each `SKILL.md` follows this template:

1. **Frontmatter** — `name`, `description`, `license`, `metadata.version`
2. **Product Summary** — 2–3 sentences on what this product does
3. **When to Use** — specific trigger conditions for picking this skill
4. **Quick Reference** — initialization code for all platforms + most-used API calls
5. **Core Concepts** — 3–5 foundational ideas (e.g., "channels are containers for messages")
6. **Common Workflows** — step-by-step pseudocode for top 3–4 tasks
7. **Decision Guidance** — tables for common "which API?" questions
8. **Common Gotchas** — known pain points, edge cases, memory leaks
9. **Verification Checklist** — before-you-ship items
10. **Key Documentation Links** — direct links to the most relevant pages

## Per-Product Scope

### Chat (`chat/SKILL.md`)
- Channel types: community channel, live channel, conversation (DM/group)
- Messaging: text, image, file, custom message types, mentions
- Real-time: Live Collections for message lists, typing indicators
- Unread counts and read receipt management
- Channel membership: join, leave, invite, ban, mute
- Moderation: flag messages, mute users, ban users
- Push notification integration for chat events

### Social (`social/SKILL.md`)
- User management: create, update, follow, unfollow, block, search
- Communities: create, join, manage roles, permissions, discovery
- Posts: text, image, video, poll; targeting community or user profile
- Comments: threaded replies, reactions on comments
- Reactions: named reactions, query by type
- Feeds: global, community, user feeds; pagination and live updates
- Stories: ephemeral 24h content, reactions, impressions
- Moderation: flag posts/comments, AI content filtering, manual review

### Video (`video/SKILL.md`)
- Rooms: create, list, terminate; room settings and permissions
- Broadcasting: start stream, stop stream, stream keys (single-use)
- Co-hosting: send invitation, accept, end co-host session
- Viewers: join room channel, receive live updates
- Recording: auto-recorded rooms, access playback after broadcast ends
- Notifications: push events for broadcast start/end, co-host invites
- Analytics: viewer counts, watch duration, engagement metrics

### UIKit (`uikit/SKILL.md`)
- Setup: installation per platform, authentication integration
- Chat components: MessageListComponent, MessageComposerComponent, ChannelListComponent
- Social components: PostListComponent, CreatePostComponent, UserProfileComponent
- Customization: ThemeConfig, component-level style overrides, dynamic UI
- Platform guides: iOS (Swift/SwiftUI), Android (Compose), React Native, Flutter
- Advanced: injecting custom components, overriding default behaviors

## Root `skill.md`

The root file:
- Contains frontmatter with a broad description ("building social, chat, video, or community features")
- Summarizes all four products in one table
- Points agents to the per-product skills for deeper guidance
- Replaces the Mintlify auto-generated file (which is already good but monolithic)

## Constraints

- Each file must start with valid YAML frontmatter (Mintlify requirement)
- Content must be accurate — validated against the actual documentation
- No version-specific content unless clearly marked
- Code examples use pseudocode patterns (not tied to one SDK version)

## Success Criteria

- `learn.social.plus/.well-known/agent-skills/index.json` lists all 4 skills
- Each skill is accessible at its own endpoint
- AI tools select the right skill based on developer context (building chat → chat skill)
- Content is more focused and actionable than the auto-generated monolith
