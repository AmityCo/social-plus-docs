---
name: video
description: Use when building live video features — room creation, broadcasting, co-hosting, viewer chat, recorded playback, or video analytics.
license: MIT
metadata:
  author: social.plus
  version: "1.0"
  display-name: social.plus Video
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
