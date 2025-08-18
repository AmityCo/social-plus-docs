# Unreferenced .mdx Files (not listed in docs.json navigation)

Totals:
- Total .mdx files: 377
- Referenced in docs.json: 204
- Unreferenced: 173

## Legend / Suggested Action
- LEGACY: Old path superseded by a newer structure (good delete candidate once confirmed no inbound links)
- DUPLICATE: Content appears duplicated elsewhere (compare before removal)
- KEEP?: Might be intentionally hidden (sample, WIP, or internal include) – review before deleting

## Top-level Counts
- social-plus-sdk: 144
- uikit: 8
- analytics-and-moderation: 6
- essentials: 6
- api-reference: 5
- misc root (README, development, quickstart, snippets): 4

---
## Root / Misc
README.mdx (KEEP? landing alt?)
development.mdx (KEEP? internal contributor guide?)
quickstart.mdx (LEGACY?)
snippets/snippet-intro.mdx (KEEP? referenced via MDX imports?)

## Essentials (likely internal helpers – KEEP?)
essentials/code.mdx
essentials/images.mdx
essentials/markdown.mdx
essentials/navigation.mdx
essentials/reusable-snippets.mdx
essentials/settings.mdx

## API Reference (decide if to expose or remove)
api-reference/endpoint/create.mdx
api-reference/endpoint/delete.mdx
api-reference/endpoint/get.mdx
api-reference/endpoint/webhook.mdx
api-reference/introduction.mdx

## Analytics & Moderation (changelogs / unused subpages)
analytics-and-moderation/console/analytics/overview.mdx
analytics-and-moderation/console/changelogs.mdx
analytics-and-moderation/console/chat-management/README.mdx
analytics-and-moderation/console/settings/settings.mdx
analytics-and-moderation/console/social-management/README.mdx
analytics-and-moderation/social+-portal/dashboard/video-analytics.mdx

## UIKit (platform guides & legacy getting-started pages)
uikit/components/chat/overview.mdx (DUPLICATE of uikit/components/chat.mdx?)
uikit/getting-started/first-steps.mdx (LEGACY)
uikit/getting-started/quick-start.mdx (LEGACY – recently edited but not in nav)
uikit/platform-guides/android-specific.mdx (Not in nav after cleanup)
uikit/platform-guides/flutter-specific.mdx
uikit/platform-guides/ios-specific.mdx
uikit/platform-guides/react-native-specific.mdx
uikit/platform-guides/web-specific.mdx

## social-plus-sdk (grouped)

### Chat – Conversation Management / Messaging / Moderation (some legacy paths)
social-plus-sdk/chat/conversation-management/channels/overview.mdx
social-plus-sdk/chat/conversation-management/members/overview.mdx
social-plus-sdk/chat/messaging-features/message-creation/overview.mdx
social-plus-sdk/chat/messaging-features/messages/flag-unflag-a-message.mdx
social-plus-sdk/chat/moderation-safety/content-moderation/channel-moderation.mdx
social-plus-sdk/chat/moderation-safety/content-moderation/channel-rate-limiting.mdx
social-plus-sdk/chat/moderation-safety/content-moderation/overview.mdx
social-plus-sdk/chat/moderation-safety/member-management/ban-unban-a-list-of-channel-members.mdx
social-plus-sdk/chat/moderation-safety/member-management/mute-unmute-a-list-of-channel-members.mdx
social-plus-sdk/chat/moderation-safety/member-management/roles-and-permission.mdx
social-plus-sdk/chat/moderation-safety/overview.mdx

### Core Concepts – Realtime (legacy presence & overview variants)
social-plus-sdk/core-concepts/realtime-communication/overview.mdx
social-plus-sdk/core-concepts/realtime-communication/presence-state/channel-presence.mdx
social-plus-sdk/core-concepts/realtime-communication/presence-state/heartbeat-sync.mdx
social-plus-sdk/core-concepts/realtime-communication/presence-state/overview.mdx
social-plus-sdk/core-concepts/realtime-communication/presence-state/user-presence.mdx
social-plus-sdk/core-concepts/realtime-communication/push-notifications/overview.mdx
social-plus-sdk/core-concepts/realtime-communication/push-notifications/setup/web-setup.mdx

### SDK Misc
social-plus-sdk/ionic.mdx (KEEP? separate platform doc?)
social-plus-sdk/technical-faq.mdx (DECIDE: integrate or remove)

### Social – Comments (legacy path duplicates of content-management structure)
social-plus-sdk/social/comments/README.mdx
social-plus-sdk/social/comments/create-comment.mdx
social-plus-sdk/social/comments/delete-comment.mdx
social-plus-sdk/social/comments/edit-comment.mdx
social-plus-sdk/social/comments/flag-unflag-comment.mdx
social-plus-sdk/social/comments/get-comment.mdx
social-plus-sdk/social/comments/get-comment-reaction-data.mdx
social-plus-sdk/social/comments/get-latest-comment.mdx
social-plus-sdk/social/comments/mention-in-comment.mdx
social-plus-sdk/social/comments/query-comment.mdx
social-plus-sdk/social/comments/view-comment.mdx

### Social – Communities (legacy flat vs new communities-spaces hierarchy)
social-plus-sdk/social/communities/README.mdx
social-plus-sdk/social/communities/community-categories.mdx
social-plus-sdk/social/communities/community-moderation.mdx
social-plus-sdk/social/communities/create-community.mdx
social-plus-sdk/social/communities/delete-community.mdx
social-plus-sdk/social/communities/get-community.mdx
social-plus-sdk/social/communities/join-leave-community.mdx
social-plus-sdk/social/communities/query-communities.mdx
social-plus-sdk/social/communities/query-community-members.mdx
social-plus-sdk/social/communities/trending-and-recommended-communities.mdx
social-plus-sdk/social/communities/update-community.mdx

### Social – Communities Spaces (legacy nested variants still unreferenced)
social-plus-sdk/social/communities-spaces/governance/community-moderation.mdx
social-plus-sdk/social/communities-spaces/governance/overview.mdx
social-plus-sdk/social/communities-spaces/membership/community-invitation.mdx
social-plus-sdk/social/communities-spaces/membership/join-leave-community.mdx
social-plus-sdk/social/communities-spaces/membership/query-community-members.mdx

### Social – Content Management (legacy moderation & reactions pages)
social-plus-sdk/social/content-management/comments/creation/create-comment.mdx
social-plus-sdk/social/content-management/moderation/overview.mdx
social-plus-sdk/social/content-management/moderation/review-process.mdx
social-plus-sdk/social/content-management/posts/engagement/reactions.mdx

### Social – Discovery / Feed / Search
social-plus-sdk/social/discovery-engagement/overview.mdx
social-plus-sdk/social/feed/README.mdx
social-plus-sdk/social/feed/custom-post-ranking.mdx
social-plus-sdk/social/feed/query-global-feed.mdx

### Social – Follow / Relationship (legacy path)
social-plus-sdk/social/follow-unfollow/README.mdx
social-plus-sdk/social/follow-unfollow/accept-decline-follow-request.mdx
social-plus-sdk/social/follow-unfollow/follow-unfollow-user.mdx
social-plus-sdk/social/follow-unfollow/get-connection-status-and-connection-counter.mdx
social-plus-sdk/social/follow-unfollow/get-follower-following-list.mdx

### Social – Intelligent Search (multiple legacy variants)
social-plus-sdk/social/intelligent-search/README.mdx
social-plus-sdk/social/intelligent-search/intelligent-search-community.mdx
social-plus-sdk/social/intelligent-search/intelligent-search-community-new.mdx
social-plus-sdk/social/intelligent-search/intelligent-search-community-updated.mdx
social-plus-sdk/social/intelligent-search/intelligent-search-post.mdx

### Social – Notification Tray (legacy vs new discovery-engagement/notifications)
social-plus-sdk/social/notification-tray/README.mdx
social-plus-sdk/social/notification-tray/get-notification-tray-seen.mdx
social-plus-sdk/social/notification-tray/mark-notification-tray-item-seen.mdx
social-plus-sdk/social/notification-tray/mark-notification-tray-seen.mdx
social-plus-sdk/social/notification-tray/query-notification-tray-item.mdx

### Social – Posts (legacy pre content-management restructure)
social-plus-sdk/social/posts/README.mdx
social-plus-sdk/social/posts/create-post/README.mdx
social-plus-sdk/social/posts/create-post/custom-post.mdx
social-plus-sdk/social/posts/create-post/file-post.mdx
social-plus-sdk/social/posts/create-post/image-post.mdx
social-plus-sdk/social/posts/create-post/live-stream-post.mdx
social-plus-sdk/social/posts/create-post/poll-post.mdx
social-plus-sdk/social/posts/create-post/text-post.mdx
social-plus-sdk/social/posts/create-post/video-post.mdx
social-plus-sdk/social/posts/delete-post.mdx
social-plus-sdk/social/posts/edit-post.mdx
social-plus-sdk/social/posts/flag-unflag-post.mdx
social-plus-sdk/social/posts/get-post.mdx
social-plus-sdk/social/posts/mention-in-post.mdx
social-plus-sdk/social/posts/pinned-post.mdx
social-plus-sdk/social/posts/post-impression.mdx
social-plus-sdk/social/posts/post-review.mdx
social-plus-sdk/social/posts/query-post.mdx
social-plus-sdk/social/posts/viewing-post-content.mdx

### Social – Reactions (legacy path)
social-plus-sdk/social/reactions/README.mdx
social-plus-sdk/social/reactions/add-remove-reaction.mdx
social-plus-sdk/social/reactions/query-reactions.mdx

### Video (legacy SDK video docs & new video-new set all unreferenced)
# Old video/* platform folders
social-plus-sdk/video/README.mdx
social-plus-sdk/video/android/README.mdx
social-plus-sdk/video/android/broadcast.mdx
social-plus-sdk/video/android/push-notification.mdx
social-plus-sdk/video/android/view-play.mdx
social-plus-sdk/video/flutter/README.mdx
social-plus-sdk/video/flutter/push-notification.mdx
social-plus-sdk/video/flutter/view-play.mdx
social-plus-sdk/video/ios/README.mdx
social-plus-sdk/video/ios/broadcast.mdx
social-plus-sdk/video/ios/push-notification.mdx
social-plus-sdk/video/ios/view-play.mdx
social-plus-sdk/video/react-native/README.mdx
social-plus-sdk/video/react-native/broadcast-live-stream.mdx
social-plus-sdk/video/react-native/view-and-play-live-stream.mdx
social-plus-sdk/video/typescript-react-native/README.mdx
social-plus-sdk/video/typescript-react-native/live-stream.mdx
social-plus-sdk/video/typescript-react-native/runquery-pattern.mdx
social-plus-sdk/video/web/README.mdx
social-plus-sdk/video/web/live-stream.mdx
social-plus-sdk/video/web/push-notification.mdx
social-plus-sdk/video/web/view-and-play-live-stream.mdx

# New video-new/* (entire set currently hidden)
social-plus-sdk/video-new/overview.mdx
social-plus-sdk/video-new/broadcasting/advanced-features.mdx
social-plus-sdk/video-new/broadcasting/camera-controls.mdx
social-plus-sdk/video-new/broadcasting/overview.mdx
social-plus-sdk/video-new/broadcasting/setup.mdx
social-plus-sdk/video-new/core-concepts/lifecycle-management.mdx
social-plus-sdk/video-new/core-concepts/overview.mdx
social-plus-sdk/video-new/core-concepts/permissions.mdx
social-plus-sdk/video-new/core-concepts/streaming-basics.mdx
social-plus-sdk/video-new/core-concepts/video-quality.mdx
social-plus-sdk/video-new/getting-started/authentication.mdx
social-plus-sdk/video-new/getting-started/first-stream.mdx
social-plus-sdk/video-new/getting-started/installation.mdx
social-plus-sdk/video-new/getting-started/overview.mdx
social-plus-sdk/video-new/notifications/push-notifications.mdx
social-plus-sdk/video-new/notifications/stream-events.mdx
social-plus-sdk/video-new/platform-specific/android-specific.mdx
social-plus-sdk/video-new/platform-specific/flutter-specific.mdx
social-plus-sdk/video-new/platform-specific/ios-specific.mdx
social-plus-sdk/video-new/platform-specific/platform-comparison.mdx
social-plus-sdk/video-new/platform-specific/react-native-specific.mdx
social-plus-sdk/video-new/platform-specific/web-specific.mdx
social-plus-sdk/video-new/playback/live-viewing.mdx
social-plus-sdk/video-new/playback/overview.mdx
social-plus-sdk/video-new/playback/recorded-playback.mdx
social-plus-sdk/video-new/troubleshooting/events.mdx
social-plus-sdk/video-new/troubleshooting/notifications.mdx
social-plus-sdk/video-new/troubleshooting/overview.mdx
social-plus-sdk/video-new/troubleshooting/platform-issues.mdx

---
## Recommended Next Steps
1. Decide which cohorts are legacy vs to be reintroduced; update docs.json or delete accordingly.
2. For legacy duplicates (posts/comments/reactions), add redirects if external links might exist.
3. If keeping a subset (e.g., video-new) plan new navigation grouping before exposing.
4. Create a cleanup branch and remove in batches; run `mint broken-links` after each batch.

Generated automatically – review before deletion.
