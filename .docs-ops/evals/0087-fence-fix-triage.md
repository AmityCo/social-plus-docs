# Triage: FENCE_RE Fix Drift (Task 0087)

Generated after applying `TICKET-0086-V1` fix to `ts-accuracy-validator.py`.
The `FENCE_RE` change (`^[ \t]*` prefix) now scans indented fenced code blocks inside MDX components (`<Tab>`, `<Tabs>`, `<CodeGroup>`, `<Accordion>`, etc.).

**Gate status**: RED (expected — see task 0087 notes)  
**Follow-up cleanup tasks needed before merge**: yes

---

## §1 · Totals

| Metric | Value |
|---|---|
| New `(file, ref)` drift pairs surfaced | **92** |
| Files affected | **46** |
| Unique API refs drifted | **73** |
| Unique *import* refs | 43 |
| Unique *namespace.member* refs | 30 |
| Gate verdict | RED |

---

## §2 · Section breakdown

| Section | Pairs | Files |
|---|---|---|
| `social-plus-sdk/social/` | ~81 | ~38 |
| `use-cases/` | ~16 | ~8 |
| `social-plus-sdk/chat/` | ~10 | ~4 |
| `api-reference/` / other | 0 | 0 |

Drift is concentrated in the **social module docs** and **use-cases guides**. Chat docs have minor exposure (4 files, 10 pairs).

---

## §3 · Top 20 files (sorted by drift count)

| Count | File |
|---|---|
| 7 | `social-plus-sdk/social/communities/community-moderation.mdx` |
| 4 | `social-plus-sdk/social/feed/query-global-feed.mdx` |
| 4 | `social-plus-sdk/social/notification-tray/query-notification-tray-item.mdx` |
| 4 | `social-plus-sdk/social/posts/get-post.mdx` |
| 4 | `social-plus-sdk/social/posts/pinned-post.mdx` |
| 4 | `social-plus-sdk/social/posts/query-post.mdx` |
| 4 | `social-plus-sdk/social/reactions/add-remove-reaction.mdx` |
| 3 | `social-plus-sdk/social/communities/community-categories.mdx` |
| 3 | `social-plus-sdk/social/communities/query-communities.mdx` |
| 3 | `social-plus-sdk/social/feed/get-user-feed.mdx` |
| 3 | `social-plus-sdk/social/follow-unfollow/get-follower-following-list.mdx` |
| 3 | `social-plus-sdk/social/reactions/query-reactions.mdx` |
| 3 | `use-cases/social/notifications-and-engagement.mdx` |
| 2 | `social-plus-sdk/chat/messaging-features/messages/flag-unflag-a-message.mdx` |
| 2 | `social-plus-sdk/social/communities/create-community.mdx` |
| 2 | `social-plus-sdk/social/communities/get-community.mdx` |
| 2 | `social-plus-sdk/social/communities/update-community.mdx` |
| 2 | `social-plus-sdk/social/follow-unfollow/follow-unfollow-user.mdx` |
| 2 | `social-plus-sdk/social/follow-unfollow/get-connection-status-and-connection-counter.mdx` |
| 2 | `social-plus-sdk/social/posts/flag-unflag-post.mdx` |

---

## §4 · Top symbols by frequency

| Count | Ref | Present in current surface? | Classification |
|---|---|---|---|
| 5 | `import AmityUserRepository` | ❌ (`UserRepository` ns exists) | REAL_DRIFT — old `Amity`-prefix; rename to `UserRepository` |
| 4 | `import AmityPost` | ❌ (no surface entry) | REAL_DRIFT — type likely removed/renamed |
| 4 | `import AmityNotificationTrayRepository` | ❌ (`notificationTray` ns exists) | REAL_DRIFT — renamed; use `notificationTray` |
| 3 | `import CommunityPostSetting` | ❌ | REAL_DRIFT — type removed or renamed |
| 3 | `import LiveCollection` | ❌ | REAL_DRIFT — generic collection type, not in surface |
| 2 | `PostRepository.updatePost` | ❌ (`editPost` member exists) | REAL_DRIFT — renamed `updatePost` → `editPost` |
| 2 | `import AmityClient` | ❌ (`Client` ns exists) | REAL_DRIFT — old `Amity`-prefix; rename to `Client` |
| 2 | `import Reaction` | ❌ | REAL_DRIFT — type import not in surface |
| 2 | `import ReactionReferenceType` | ❌ | REAL_DRIFT — type import not in surface |
| 1 | `MessageRepository.createTextMessage` | ❌ (`createMessage` exists) | REAL_DRIFT — renamed `createTextMessage` → `createMessage` |
| 1 | `Client.hasPermission` | ❌ | REAL_DRIFT — method removed from Client namespace |
| 1 | `CommunityRepository.addMembers` | ❌ | REAL_DRIFT — member management methods removed from CommunityRepository |
| 1 | `CommunityRepository.addRoles` | ❌ | REAL_DRIFT — (same cohort as above) |
| 1 | `CommunityRepository.banMembers` | ❌ | REAL_DRIFT — (same cohort) |
| 1 | `CommunityRepository.removeMembers` | ❌ | REAL_DRIFT — (same cohort) |
| 1 | `CommunityRepository.removeRoles` | ❌ | REAL_DRIFT — (same cohort) |
| 1 | `CommunityRepository.unbanMembers` | ❌ | REAL_DRIFT — (same cohort) |
| 1 | `CommunityRepository.getCommunityLive` | ❌ (`getCommunity` exists) | REAL_DRIFT — renamed (dropped `Live` suffix) |
| 1 | `CommunityRepository.isMember` | ❌ | REAL_DRIFT — method removed |
| 1 | `notificationTray.markAllNotificationTrayItemsAsSeen` | ❌ (`markTraySeen`/`markItemsSeen` exist) | REAL_DRIFT — renamed to shorter form |
| 1 | `PostRepository.isFlaggedByMe` | ❌ (`isPostFlaggedByMe` exists) | REAL_DRIFT — renamed (added `Post` infix) |
| 1 | `PostRepository.getPostsByIds` | ❌ (`getPostByIds` exists) | REAL_DRIFT — renamed (plural `Ids` → `Id`) |
| 1 | `PostRepository.postForId` | ❌ (`getPost` exists) | REAL_DRIFT — renamed to `getPost` |
| 1 | `PostRepository.getPinnedPostsLive` | ❌ (`getPinnedPosts` exists) | REAL_DRIFT — renamed (dropped `Live` suffix) |
| 1 | `PostRepository.queryPosts` | ❌ (`getPosts` exists) | REAL_DRIFT — renamed `query` → `get` pattern |
| 1 | `PostRepository.deletePost` | ❌ (`hardDeletePost`/`softDeletePost` exist) | REAL_DRIFT — fixed once in 0085/0086; another occurrence in `use-cases/social/rich-content-creation.mdx` |
| 1 | `RoomRepository.getRecordedUrls` | ❌ (`getRecordedUrl` exists, singular) | REAL_DRIFT — plural → singular rename |
| 1 | `InvitationRepository.getMyRoomInvitations` | ❌ (`getMyCommunityInvitations` exists) | REAL_DRIFT — renamed |
| 1 | `UserRepository.getNotificationSettings` | ❌ | REAL_DRIFT — method not in UserRepository (17 members) |
| 1 | `UserRepository.updateNotificationSettings` | ❌ | REAL_DRIFT — (same, not in surface) |
| 1 | `UserRepository.getViewedUsers` | ❌ | REAL_DRIFT — not in surface |
| 1 | `UserRepository.Relationship.acceptFollower` | ❌ | REAL_DRIFT — `Relationship` sub-namespace not in surface |
| 1 | `ChannelRepository.getMember` | ❌ (no `getMember` in 28 members) | REAL_DRIFT — renamed to `getChannel` or removed |
| 1 | `ChannelRepository.archiveChannel` | ❌ | REAL_DRIFT — removed from surface |
| 1 | `ChannelRepository.getMembers` | ❌ | REAL_DRIFT — removed; use events/query pattern |
| 1 | `ChannelRepository.unmuteMembers` | ❌ | REAL_DRIFT — removed; `unmuteChannel` exists |
| 1 | `ChannelRepository.subscribeChannel` | ❌ | REAL_DRIFT — removed from surface |
| 1 | `ChannelRepository.banMembers` | ❌ | REAL_DRIFT — removed |
| 1 | `import FeedType` | ❌ | REAL_DRIFT — type not exported from current surface |

**None of the newly surfaced refs classified as `NEEDS_SKIP_MARKER` or `VALIDATOR_FALSE_POSITIVE`** — every hit is a stale API name that the validator correctly identifies as missing from the published surface.

---

## §5 · Distribution analysis and cleanup task recommendation

**Distribution pattern**: **concentrated by symbol cohort, diffuse by file**

- Most files have 1–4 drifts, from a shared pool of ~73 unique stale symbols
- No single file has more than 7 drifts
- The top 5 symbols alone account for 20 of 92 pairs (22%)
- Several symbols cluster by rename cohort:
  - **Amity-prefix cohort** (`AmityUserRepository`, `AmityPost`, `AmityNotificationTrayRepository`, `AmityClient`): 15 pairs across ~12 files
  - **CommunityRepository member removal cohort** (`addMembers`, `removeMembers`, `banMembers`, `addRoles`, `removeRoles`, `unbanMembers`): 6 pairs in 1 file
  - **PostRepository renames** (`updatePost`, `isFlaggedByMe`, `getPostsByIds`, `postForId`, `getPinnedPostsLive`, `queryPosts`, `deletePost`): ~10 pairs

**Recommended cleanup structure**: **split by API-rename cohort** (not by file), so each task has a focused search-replace pattern:

| Proposed task | Scope | Pairs | Pattern |
|---|---|---|---|
| 0088a | `Amity`-prefix import renames across all files | ~15 | `AmityUserRepository` → remove import or `UserRepository`; `AmityClient` → `Client`; etc. |
| 0088b | CommunityRepository member cohort (moderation.mdx heavy) | ~8 | `addMembers/removeMembers/banMembers` → confirm new API or mark skip |
| 0088c | PostRepository renames (posts/ files) | ~10 | `updatePost→editPost`, `isFlaggedByMe→isPostFlaggedByMe`, etc. |
| 0088d | Type import renames (Reaction, CommunityPostSetting, LiveCollection, etc.) | ~30 | Requires SDK surface confirmation per type — may need `//doc-as-test:skip` if types are intentionally unexported |
| 0088e | Notification + Follow + Channel cohorts | ~15 | `notificationTray.markAllNotificationTrayItemsAsSeen→markTraySeen`; `UserRepository.Relationship→?`; Channel removals |

Total estimated cleanup: 5 batched tasks, each touching 5–15 files with a focused pattern. Each task should be executable in under 2 hours.

**Gate will stay RED until all 5 cohort tasks land.** The branch can merge once all cleanup tasks are done and gate returns GREEN.
