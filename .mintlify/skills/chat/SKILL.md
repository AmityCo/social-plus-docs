---
name: chat
description: Use when building chat features — channels, direct messages, group conversations, real-time messaging, unread counts, read receipts, or moderation in chat contexts.
license: MIT
metadata:
  author: social.plus
  version: "1.0"
  display-name: social.plus Chat
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
