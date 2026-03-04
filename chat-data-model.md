# Chat Module — Data Model Reference

> **Audience**: Engineers performing data import and analytics integration.
> This document describes the core chat/messaging entities, their fields, relationships, and conventions you need to understand when importing or querying chat module data.
>
> For social entities (User, Community, Post, Comment, etc.), see [social-data-model.md](./social-data-model.md).

---

## Table of Contents

- [Chat Module — Data Model Reference](#chat-module--data-model-reference)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
    - [Conventions used across all entities](#conventions-used-across-all-entities)
  - [Entity-Relationship Diagram](#entity-relationship-diagram)
  - [Entity Reference](#entity-reference)
    - [Channel](#channel)
    - [ChannelUser](#channeluser)
    - [Message](#message)
    - [MessageFeed](#messagefeed)
  - [Message Threading Model](#message-threading-model)
  - [Channel ↔ Community Relationship](#channel--community-relationship)
  - [Key Enums Reference](#key-enums-reference)
  - [Data Import Tips](#data-import-tips)
    - [1. ID Resolution](#1-id-resolution)
    - [2. Channel ↔ Community Linking](#2-channel--community-linking)
    - [3. Message Ordering by Segment](#3-message-ordering-by-segment)
    - [4. ChannelUser Composite Key](#4-channeluser-composite-key)
    - [5. Computed Fields — Do Not Import](#5-computed-fields--do-not-import)
    - [6. Filtering Deleted Records](#6-filtering-deleted-records)
    - [7. Reactions on Messages](#7-reactions-on-messages)
    - [8. Message Threading](#8-message-threading)

---

## Overview

The chat module provides real-time messaging through **channels** (group chats, direct conversations, broadcasts). Users join channels as **channel users**, exchange **messages** within **message feeds** (threads), and can attach media, reactions, and mentions.

Channels are the top-level container. Each channel has one or more **message feeds** (threads), and each feed contains **messages** ordered by a monotonically increasing `segment`. Messages support threading via a self-referential `parentId`.

### Conventions used across all entities

| Convention            | Description                                                                                                                                                                                     |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Triple-ID pattern** | Most entities expose three IDs: a primary `{entity}Id`, a `{entity}PublicId` (stable external identifier), and a `{entity}InternalId` (database-level reference). For joins, prefer public IDs. |
| **Soft delete**       | Nearly every entity has an `isDeleted` boolean. Deleted records remain in the database with `isDeleted: true`. Filter these out unless you specifically need deletion history.                  |
| **Timestamps**        | `createdAt` and `updatedAt` (ISO 8601 date-time) are present on all entities. Some also have `editedAt`.                                                                                        |
| **Metadata**          | A freeform `metadata` object is available on most entities for custom fields.                                                                                                                   |
| **Flagging**          | `flagCount` (number of reports) and `hashFlag` (bloom-filter structure) track moderation state on messages. Channels bubble up flags via `hasFlaggedMessage`.                                   |

---

## Entity-Relationship Diagram

```mermaid
erDiagram
    User {
        string userId PK
        string userPublicId
        string userInternalId
        string displayName
    }

    Community {
        string communityId PK
        string channelId FK
    }

    File {
        string fileId PK
        string type
        string fileUrl
    }

    Channel {
        string channelId PK
        string type
        string displayName
        string avatarFileId FK
        boolean isPublic
        string notificationMode
        datetime lastActivity
        integer memberCount
        integer messageCount
        object attachedTo
        boolean isDeleted
    }

    ChannelUser {
        string userId FK
        string channelId FK
        string membership
        array roles
        array permissions
        number readToSegment
        boolean isBanned
        boolean isMuted
    }

    MessageFeed {
        string messageFeedId PK
        string channelId FK
        string channelType
        string creatorId FK
        string lastMessageId FK
        integer childCount
        boolean isDeleted
    }

    Message {
        string messageId PK
        string channelId FK
        string messageFeedId FK
        string parentId FK
        string creatorId FK
        string dataType
        object data
        number segment
        integer childCount
        object reactions
        boolean isDeleted
    }

    Reaction {
        string reactionId PK
        string reactionName
        string userId FK
        string referenceId FK
        string referenceType
    }

    Room {
        string roomId PK
        string type
        string status
        boolean liveChatEnabled
    }

    %% === Relationships ===

    Channel ||--o{ ChannelUser : "has members"
    User ||--o{ ChannelUser : "joins channels"

    Channel ||--o{ MessageFeed : "contains feeds"
    MessageFeed ||--o{ Message : "contains messages"

    User ||--o{ Message : "creates"
    Message ||--o{ Message : "parent has replies"
    Message }o--o| File : "attaches media"
    Message ||--o{ Reaction : "receives (referenceType=message)"
    User ||--o{ Reaction : "creates"

    Channel }o--o| File : "avatar"
    Community ||--o| Channel : "backed by (1:1)"
    Room }o--o| Channel : "live chat (attachedTo.roomId)"
```

---

## Entity Reference

### Channel

A chat room, conversation, or group. Channels are the top-level container for messaging. Every community has a 1:1 backing channel. Channels can be standard (open), private, direct conversations, broadcast, community-backed, or live (attached to a room).

| Field                          | Type      | Description                                                                        |
| ------------------------------ | --------- | ---------------------------------------------------------------------------------- |
| `channelId`                    | string    | **Primary key.** Public channel identifier.                                        |
| `channelInternalId`            | string    | Internal database identifier.                                                      |
| `channelPublicId`              | string    | Public identifier (same as `channelId`).                                           |
| `type`                         | enum      | `standard` \| `private` \| `conversation` \| `broadcast` \| `community` \| `live`. |
| `displayName`                  | string    | Channel display name.                                                              |
| `isDistinct`                   | boolean   | If true, reuses existing channel for the same user set (conversations).            |
| `tags`                         | string[]  | Tags for filtering/categorization.                                                 |
| `metadata`                     | object    | Arbitrary custom fields.                                                           |
| `avatarFileId`                 | string    | FK → File. Channel avatar image.                                                   |
| `lastActivity`                 | date-time | Timestamp of last activity (message, event, etc.).                                 |
| `memberCount`                  | integer   | _(Computed)_ Number of members.                                                    |
| `messageCount`                 | integer   | _(Computed)_ Number of messages.                                                   |
| `moderatorMemberCount`         | integer   | Count of moderator members.                                                        |
| `isPublic`                     | boolean   | Whether channel is publicly listed.                                                |
| `notificationMode`             | enum      | `default` \| `silent` \| `subscribe`.                                              |
| `isMuted`                      | boolean   | _(Computed)_ Whether the channel is currently muted (based on `muteTimeout`).      |
| `muteTimeout`                  | date-time | When the channel-level mute expires.                                               |
| `isRateLimited`                | boolean   | _(Computed)_ Whether rate limiting is active (based on `rateLimitTimeout`).        |
| `rateLimit`                    | number    | Maximum messages per rate limit window.                                            |
| `rateLimitWindow`              | number    | Rate limit window in milliseconds.                                                 |
| `rateLimitTimeout`             | date-time | When the current rate limit expires.                                               |
| `messageAutoDeleteEnabled`     | boolean   | Whether auto-delete by flag threshold is enabled.                                  |
| `autoDeleteMessageByFlagLimit` | number    | Flag count threshold for auto-deletion.                                            |
| `messagePreviewId`             | string    | _(Computed)_ ID of the latest message preview.                                     |
| `attachedTo`                   | object    | Linked resources: `{postId, videoStreamId, roomId}`.                               |
| `isDeleted`                    | boolean   | Soft-delete flag.                                                                  |
| `createdAt`                    | date-time | Creation timestamp.                                                                |
| `updatedAt`                    | date-time | Last update timestamp.                                                             |

**Relationships:**

- `1:1` → Community (community-type channels back a community; see [Channel ↔ Community Relationship](#channel--community-relationship))
- `1:N` → ChannelUser (members)
- `1:N` → MessageFeed (message threads within the channel)
- `0:1` → Room (live-type channels are attached to a room via `attachedTo.roomId`)
- `0:1` → File (avatar via `avatarFileId`)

---

### ChannelUser

The **join entity** between User and Channel. Represents a user's membership, roles, and read state within a channel.

| Field                  | Type      | Description                                       |
| ---------------------- | --------- | ------------------------------------------------- |
| `userId`               | string    | FK → User. User's public ID.                      |
| `userInternalId`       | string    | User's internal ID.                               |
| `userPublicId`         | string    | User's public ID.                                 |
| `channelId`            | string    | FK → Channel. Channel's public ID.                |
| `channelInternalId`    | string    | Channel's internal ID.                            |
| `channelPublicId`      | string    | Channel's public ID.                              |
| `membership`           | enum      | `none` \| `member` \| `banned`.                   |
| `roles`                | string[]  | Role public IDs assigned within this channel.     |
| `permissions`          | string[]  | Resolved permissions from roles.                  |
| `isBanned`             | boolean   | _(Computed)_ `true` when `membership = "banned"`. |
| `isMuted`              | boolean   | _(Computed)_ `true` when `muteTimeout > now`.     |
| `muteTimeout`          | date-time | When the user-level mute expires in this channel. |
| `readToSegment`        | number    | Last-read message segment (read cursor).          |
| `lastMentionedSegment` | number    | Segment of last @mention for this user.           |
| `lastActivity`         | date-time | User's last activity in the channel.              |
| `createdAt`            | date-time | Record creation timestamp.                        |
| `updatedAt`            | date-time | Last update timestamp.                            |

**Relationships:**

- `N:1` → User
- `N:1` → Channel
- Composite key: (`userId`, `channelId`)

---

### Message

A message within a channel. Messages belong to a [MessageFeed](#messagefeed) and support threading (replies). Each message is stored as its own document.

| Field             | Type      | Description                                                                            |
| ----------------- | --------- | -------------------------------------------------------------------------------------- |
| `messageId`       | string    | **Primary key.** Internal message ID.                                                  |
| `publicId`        | string    | Public-facing message ID.                                                              |
| `channelId`       | string    | FK → Channel. Channel this message belongs to.                                         |
| `channelPublicId` | string    | Channel's public ID.                                                                   |
| `messageFeedId`   | string    | FK → MessageFeed. The feed/thread containing this message.                             |
| `parentId`        | string    | FK → Message (self). Parent message ID for replies. `null` for top-level messages.     |
| `creatorId`       | string    | FK → User. Creator's internal ID.                                                      |
| `creatorPublicId` | string    | Creator's public ID.                                                                   |
| `dataType`        | enum      | `text` \| `image` \| `video` \| `file` \| `audio` \| `custom` \| `json` \| `imagemap`. |
| `data`            | object    | Message payload. For media types, includes `fileId` and optionally `thumbnailFileId`.  |
| `segment`         | number    | Ordering position within the feed.                                                     |
| `tags`            | string[]  | Tags associated with this message.                                                     |
| `metadata`        | object    | Arbitrary custom fields.                                                               |
| `mentionedUsers`  | array     | Mentioned users: `[{type: "user"\|"channel", userIds: [...]}]`.                        |
| `childCount`      | integer   | Number of direct replies.                                                              |
| `reactions`       | object    | Map of `reactionName → count`.                                                         |
| `reactionCount`   | integer   | Total reaction count.                                                                  |
| `myReactions`     | string[]  | Current user's reaction names.                                                         |
| `flagCount`       | integer   | Number of moderation reports.                                                          |
| `hashFlag`        | object    | _(Computed)_ Bloom-filter flag structure.                                              |
| `editedAt`        | date-time | Last content edit timestamp.                                                           |
| `isDeleted`       | boolean   | Soft-delete flag.                                                                      |
| `createdAt`       | date-time | Creation timestamp.                                                                    |
| `updatedAt`       | date-time | Last update timestamp.                                                                 |

> **Threading model:** See [Message Threading Model](#message-threading-model) below for details on how replies work.

**Relationships:**

- `N:1` → User (creator via `creatorId`)
- `N:1` → Channel (via `channelId`)
- `N:1` → MessageFeed (via `messageFeedId`)
- `1:N` → Message (replies via `parentId`, self-referential)
- `1:N` → Reaction (via `reaction.referenceId` where `referenceType = "message"`)
- `0:1` → File (attachment via `data.fileId`)

---

### MessageFeed

A message thread/feed within a channel. Each channel has one or more message feeds. The feed tracks the latest message and provides a message preview for UI display.

| Field                  | Type      | Description                                                                                      |
| ---------------------- | --------- | ------------------------------------------------------------------------------------------------ |
| `messageFeedId`        | string    | **Primary key.**                                                                                 |
| `channelId`            | string    | FK → Channel. The channel this feed belongs to.                                                  |
| `channelPublicId`      | string    | Channel's public ID.                                                                             |
| `channelType`          | enum      | Channel type: `standard` \| `private` \| `conversation` \| `broadcast` \| `community` \| `live`. |
| `name`                 | string    | Feed display name.                                                                               |
| `creatorId`            | string    | FK → User. Feed creator's internal ID.                                                           |
| `creatorPublicId`      | string    | Creator's public ID.                                                                             |
| `lastMessageId`        | string    | FK → Message. Most recent message.                                                               |
| `lastMessageTimestamp` | date-time | Timestamp of the most recent message.                                                            |
| `messagePreviewId`     | string    | _(Computed)_ ID of the preview message.                                                          |
| `childCount`           | integer   | Number of messages in this feed.                                                                 |
| `isDeleted`            | boolean   | Soft-delete flag.                                                                                |
| `editedAt`             | date-time | Last metadata edit timestamp.                                                                    |
| `createdAt`            | date-time | Creation timestamp.                                                                              |
| `updatedAt`            | date-time | Last update timestamp.                                                                           |

**Relationships:**

- `N:1` → Channel (via `channelId`)
- `N:1` → User (creator via `creatorId`)
- `1:N` → Message (messages reference feed via `messageFeedId`)

---

## Message Threading Model

Messages support single-level threading within a message feed:

```
MessageFeed (messageFeedId)
├── Message A  (parentId = null, segment = 1)
│   ├── Reply A1  (parentId = A, segment = 2)
│   └── Reply A2  (parentId = A, segment = 3)
├── Message B  (parentId = null, segment = 4)
└── Message C  (parentId = null, segment = 5)
    └── Reply C1  (parentId = C, segment = 6)
```

**Key rules:**

- **Top-level messages** have `parentId = null`. They belong directly to the feed.
- **Replies** have `parentId` set to the parent message's ID.
- `childCount` on each message tracks its direct reply count.
- Messages are ordered by `segment` within their feed (monotonically increasing).
- All messages (top-level and replies) live in the same feed and share the same segment counter.

**How to reconstruct threads:**

1. Query messages by `messageFeedId`.
2. Top-level messages: `parentId = null`.
3. Group replies by `parentId`.
4. Order all messages by `segment`.

---

## Channel ↔ Community Relationship

Every community in the social module has a 1:1 backing channel with `type = "community"`. This relationship connects the social and chat modules:

```
Community (communityId)  ────→  Channel (channelId, type = "community")
         └── community.channelId = channel.channelId
```

- The Community entity stores a `channelId` foreign key pointing to its backing channel.
- Community-type channels inherit the community's membership — a user who is a community member is also a channel member.
- When importing data that spans both modules, ensure the Community's `channelId` FK is correctly linked.

---

## Key Enums Reference

| Enum                         | Values                                                                  | Used By                     |
| ---------------------------- | ----------------------------------------------------------------------- | --------------------------- |
| **Channel.type**             | `standard`, `private`, `conversation`, `broadcast`, `community`, `live` | Channel `.type`             |
| **Channel.notificationMode** | `default`, `silent`, `subscribe`                                        | Channel `.notificationMode` |
| **ChannelUser.membership**   | `none`, `member`, `banned`                                              | ChannelUser `.membership`   |
| **Message.dataType**         | `text`, `image`, `video`, `file`, `audio`, `custom`, `json`, `imagemap` | Message `.dataType`         |
| **Reaction.referenceType**   | `post`, `comment`, `story`, `message`                                   | Reaction `.referenceType`   |

---

## Data Import Tips

### 1. ID Resolution

Most entities expose three IDs (`channelId`, `channelPublicId`, `channelInternalId`). For joining data across entities, **use the public ID** — these are the values used in foreign key references. Internal IDs are database-level identifiers and may not appear in all API responses.

### 2. Channel ↔ Community Linking

Every community has a 1:1 backing channel (with `type = "community"`). When importing both communities and channels, ensure corresponding records are linked. The community stores a `channelId` foreign key.

### 3. Message Ordering by Segment

Messages within a feed are ordered by `segment` (a monotonically increasing integer). **Preserve segment ordering** during import to maintain correct message sequence. Each feed maintains its own independent segment counter.

### 4. ChannelUser Composite Key

The ChannelUser entity uses a composite key of (`userId`, `channelId`). When importing, deduplicate on **both** fields to avoid creating duplicate membership records.

### 5. Computed Fields — Do Not Import

Several fields are derived at read time and should **not** be imported as stored values:

- `Channel.isMuted` — derived from `muteTimeout > now`.
- `Channel.isRateLimited` — derived from `rateLimitTimeout > now`.
- `Channel.memberCount` / `messageCount` — aggregated from related records.
- `ChannelUser.isBanned` — derived from `membership = "banned"`.
- `ChannelUser.isMuted` — derived from `muteTimeout > now`.
- `Message.myReactions` — derived per-request for the current user.
- `MessageFeed.messagePreviewId` — derived from latest message.

### 6. Filtering Deleted Records

Soft-deleted records have `isDeleted: true`. **Exclude these by default** for analytics unless you need deletion history.

### 7. Reactions on Messages

Message reactions follow the same model as social reactions (see [social-data-model.md](./social-data-model.md)). Each reaction is stored as a separate document with `referenceType = "message"` and `referenceId` pointing to the message. The `reactions` object on Message provides pre-aggregated `{name: count}` maps.

### 8. Message Threading

To get only top-level messages (not replies), filter by `parentId = null`. To reconstruct threads, group replies by `parentId` and order by `segment`. See [Message Threading Model](#message-threading-model) for the full pattern.
