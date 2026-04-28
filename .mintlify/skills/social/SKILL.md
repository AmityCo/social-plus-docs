---
name: social
description: Use when building social features — user profiles, communities, posts, comments, reactions, feeds, stories, follow/unfollow, or content moderation.
license: MIT
metadata:
  author: social.plus
  version: "1.0"
  display-name: social.plus Social
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
