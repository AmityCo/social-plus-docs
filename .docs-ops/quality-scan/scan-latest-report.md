# Docs Quality — Full-Corpus Proxy Scan

_LLM-free structural proxies for the 3 weak rubric dimensions. Scanned 166 pages under `social-plus-sdk` (137 with code blocks)._

## Headline

- **Parity:** 61 pages flagged (44.5% of code pages); **55 are Flutter coverage gaps**.
- **Clarity:** 7 pages (4.2%) — 0 marketing-register openers, 7 open with a component before any sentence.
- **Completeness:** 56 pages show a parameter-bearing call but ship **no parameter table** (43.1% of 130 param-call pages; raw any-code-no-table = 61).

## By section

| Section | Pages | Code pages | Parity flagged | Clarity flagged | No param table |
|---|---|---|---|---|---|
| `social` | 71 | 59 | 30 | 0 | 16 |
| `core-concepts` | 36 | 32 | 11 | 0 | 19 |
| `chat` | 34 | 29 | 10 | 0 | 9 |
| `video-new` | 10 | 9 | 9 | 0 | 4 |
| `getting-started` | 7 | 7 | 1 | 0 | 7 |
| `changelogs` | 5 | 1 | 0 | 5 | 1 |
| `(root)` | 3 | 0 | 0 | 2 | 0 |

## Flutter coverage gaps (top 25)

- `social-plus-sdk/getting-started/visitor-mode.mdx` — iOS 8, Android 8, TS 21, **Flutter 0**
- `social-plus-sdk/social/events/create-event.mdx` — iOS 5, Android 5, TS 18, **Flutter 0**
- `social-plus-sdk/social/content-management/posts/creation/mixed-media-post.mdx` — iOS 1, Android 1, TS 16, **Flutter 0**
- `social-plus-sdk/social/content-management/posts/creation/room-post.mdx` — iOS 12, Android 12, TS 15, **Flutter 0**
- `social-plus-sdk/social/events/event-rsvp.mdx` — iOS 7, Android 7, TS 14, **Flutter 0**
- `social-plus-sdk/social/events/manage-events.mdx` — iOS 10, Android 10, TS 14, **Flutter 0**
- `social-plus-sdk/video-new/broadcasting/create-room.mdx` — iOS 7, Android 7, TS 14, **Flutter 0**
- `social-plus-sdk/video-new/broadcasting/manage-rooms.mdx` — iOS 11, Android 11, TS 11, **Flutter 0**
- `social-plus-sdk/social/discovery-engagement/notifications/notification-tray-status.mdx` — iOS 2, Android 2, TS 10, **Flutter 0**
- `social-plus-sdk/social/content-management/posts/creation/text-post.mdx` — iOS 2, Android 2, TS 9, **Flutter 0**
- `social-plus-sdk/social/content-management/posts/retrieval/query-posts.mdx` — iOS 2, Android 2, TS 10, **Flutter 1**
- `social-plus-sdk/video-new/broadcasting/rooms-overview.mdx` — iOS 7, Android 7, TS 9, **Flutter 0**
- `social-plus-sdk/video-new/analytics/overview.mdx` — iOS 4, Android 4, TS 8, **Flutter 0**
- `social-plus-sdk/video-new/broadcasting/co-host-management.mdx` — iOS 8, Android 8, TS 8, **Flutter 0**
- `social-plus-sdk/social/communities-spaces/organization/community-invitation.mdx` — iOS 7, Android 7, TS 7, **Flutter 0**
- `social-plus-sdk/video-new/broadcasting/start-broadcasting.mdx` — iOS 6, Android 6, TS 6, **Flutter 0**
- `social-plus-sdk/chat/messaging-features/message-creation/send-a-message.mdx` — iOS 5, Android 5, TS 1, **Flutter 0**
- `social-plus-sdk/core-concepts/realtime-communication/realtime-events/social-realtime-events.mdx` — iOS 6, Android 6, TS 5, **Flutter 1**
- `social-plus-sdk/video-new/broadcasting/live-viewing.mdx` — iOS 5, Android 5, TS 5, **Flutter 0**
- `social-plus-sdk/core-concepts/safety-privacy/pii-detection.mdx` — iOS 3, Android 4, TS 0, **Flutter 0**
- `social-plus-sdk/social/communities-spaces/organization/join-leave-community.mdx` — iOS 6, Android 6, TS 6, **Flutter 2**
- `social-plus-sdk/video-new/broadcasting/recorded-playback.mdx` — iOS 4, Android 4, TS 4, **Flutter 0**
- `social-plus-sdk/chat/engagement-features/unread-status/message-delivery-status.mdx` — iOS 3, Android 3, TS 3, **Flutter 0**
- `social-plus-sdk/chat/messaging-features/message-creation/custom-message.mdx` — iOS 3, Android 1, TS 2, **Flutter 0**
- `social-plus-sdk/core-concepts/foundation/logging.mdx` — iOS 3, Android 3, TS 2, **Flutter 0**

## Marketing-register openers (top 25)

