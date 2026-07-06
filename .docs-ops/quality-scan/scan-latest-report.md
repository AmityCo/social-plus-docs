# Docs Quality - Proxy Scan

_LLM-free structural proxies for the 3 weak rubric dimensions. Scanned 177 pages under `social-plus-sdk` (141 with code blocks)._

## Headline

- **Parity:** 12 pages flagged (8.5% of code pages); **11 are Flutter coverage gaps**.
- **Clarity:** 0 pages (0.0%) - 0 marketing-register openers, 5 open with a component before any sentence.
- **Completeness:** 0 pages show a parameter-bearing call but ship **no parameter table** (0.0% of 134 param-call pages; raw any-code-no-table = 1).

## By section

| Section | Pages | Code pages | Parity flagged | Clarity flagged | No param table |
|---|---|---|---|---|---|
| `social` | 74 | 62 | 7 | 0 | 0 |
| `core-concepts` | 42 | 34 | 2 | 0 | 0 |
| `chat` | 36 | 29 | 1 | 0 | 0 |
| `video-new` | 10 | 8 | 1 | 0 | 0 |
| `getting-started` | 7 | 7 | 1 | 0 | 0 |
| `changelogs` | 5 | 1 | 0 | 0 | 0 |
| `(root)` | 3 | 0 | 0 | 0 | 0 |

## Flutter coverage gaps (top 25)

- `social-plus-sdk/getting-started/visitor-mode.mdx` - iOS 7, Android 8, TS 19, **Flutter 0**
- `social-plus-sdk/social/communities-spaces/organization/community-invitation.mdx` - iOS 7, Android 7, TS 7, **Flutter 0**
- `social-plus-sdk/social/events/manage-events.mdx` - iOS 5, Android 5, TS 5, **Flutter 0**
- `social-plus-sdk/social/events/event-rsvp.mdx` - iOS 4, Android 4, TS 4, **Flutter 0**
- `social-plus-sdk/social/communities-spaces/organization/join-leave-community.mdx` - iOS 5, Android 5, TS 5, **Flutter 2**
- `social-plus-sdk/video-new/broadcasting/create-room.mdx` - iOS 3, Android 3, TS 3, **Flutter 0**
- `social-plus-sdk/core-concepts/realtime-communication/presence-state/heartbeat-sync.mdx` - iOS 2, Android 2, TS 1, **Flutter 0**
- `social-plus-sdk/social/content-management/posts/retrieval/query-posts.mdx` - iOS 1, Android 3, TS 1, **Flutter 1**
- `social-plus-sdk/social/discovery-engagement/notifications/notification-items.mdx` - iOS 2, Android 2, TS 2, **Flutter 0**
- `social-plus-sdk/core-concepts/safety-privacy/pii-detection.mdx` - iOS 1, Android 1, TS 0, **Flutter 0**
- `social-plus-sdk/social/events/create-event.mdx` - iOS 1, Android 1, TS 1, **Flutter 0**

## Parameter table gaps

- None.

## Marketing-register openers (top 25)


## Component-first openers

- `social-plus-sdk/changelogs/android-sdk-changelog.mdx`
- `social-plus-sdk/changelogs/flutter-sdk-changelog.mdx`
- `social-plus-sdk/changelogs/ios-sdk-changelog.mdx`
- `social-plus-sdk/changelogs/ios-sdk-v8-migration-guide.mdx`
- `social-plus-sdk/changelogs/web-sdk-changelog.mdx`
