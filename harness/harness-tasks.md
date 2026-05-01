# SDK Harness — Agent Runbook

_Generated 2026-05-01 14:17 — 162 findings requiring AI_

## Step 0 — Start Dashboard (optional but recommended)

Run in a separate terminal before starting any other steps:

```bash
./harness-bin serve --config harness-config.yml
```

Then open http://localhost:8765 to watch pipeline progress live.
The dashboard auto-refreshes every 3 seconds.
You may skip this step if running headlessly.

---

## Agent Instructions

You are an autonomous agent. Execute ALL tasks in this file without stopping for confirmation.

**For each MISSING_SNIPPET task:**
1. Look up the function in the SDK source (search by function ID in the SDK path)
2. Generate a minimal working snippet using the `begin_sample_code` format below
3. Write the file to the specified snippet directory
4. Continue to the next task immediately

**After ALL snippets are written:**
```bash
cd social-plus-docs/harness && ./harness-bin audit --config harness-config.yml
```
Then run `./harness-bin prompt` again if there are still open findings.

**Snippet format (MUST match exactly):**
```
/* begin_sample_code
   filename: <filename>
   sp_docs_page: <path from docs.json, e.g. social-plus-sdk/chat/overview>
   description: <one line>
   */
<working code>
/* end_sample_code */
```

**Rules:**
- Use real Amity SDK class names (look them up in the SDK source)
- Keep it minimal — just enough to demonstrate the function
- `sp_docs_page` must be a relative path (not a full URL)
- Do not ask for confirmation between tasks — work through all of them

---

## MISSING_SNIPPET (151)

For each entry below, create a SDK code snippet file at the given path.
The snippet **must** use this exact format:

```
/* begin_sample_code
   filename: <filename>
   sp_docs_page: <docs.json relative path, e.g. social-plus-sdk/chat/overview>
   description: <one line>
   */
<working code>
/* end_sample_code */
```

Rules:
- Use real Amity/social.plus SDK class names from the platform source
- Keep it minimal — just enough to demonstrate the function
- `sp_docs_page` must be a path from `docs.json` (not a full URL)

### Android (Kotlin) — 50 functions

Snippet directory: `../../Amity-Social-Cloud-SDK-Android/amity-sample-code/src/main/java/com/amity/snipet/verifier`

| Function ID | Write to filename |
|-------------|-------------------|
| `channel.get_total_channels_unread_info` | `AmityChannelGetTotalChannelsUnreadInfo.kt` |
| `channel.get_total_channel_unread` | `AmityChannelGetTotalChannelUnread.kt` |
| `message.create_image` | `AmityMessageCreateImage.kt` |
| `message.create_file` | `AmityMessageCreateFile.kt` |
| `message.create_video` | `AmityMessageCreateVideo.kt` |
| `message.create_audio` | `AmityMessageCreateAudio.kt` |
| `message.delete_failed` | `AmityMessageDeleteFailed.kt` |
| `ad.get_network` | `AmityAdGetNetwork.kt` |
| `file.upload_clip` | `AmityFileUploadClip.kt` |
| `file.cancel_upload` | `AmityFileCancelUpload.kt` |
| `file.get_upload_info` | `AmityFileGetUploadInfo.kt` |
| `file.update_alt_text` | `AmityFileUpdateAltText.kt` |
| `invitation.get_my_community` | `AmityInvitationGetMyCommunity.kt` |
| `invitation.get` | `AmityInvitationGet.kt` |
| `room_presence.start_heartbeat` | `AmityRoomPresenceStartHeartbeat.kt` |
| `room_presence.stop_heartbeat` | `AmityRoomPresenceStopHeartbeat.kt` |
| `room_presence.observe_online_users_count` | `AmityRoomPresenceObserveOnlineUsersCount.kt` |
| `room_presence.get_online_users_count` | `AmityRoomPresenceGetOnlineUsersCount.kt` |
| `room_presence.get_online_users_snapshot` | `AmityRoomPresenceGetOnlineUsersSnapshot.kt` |
| `room_presence.room_id` | `AmityRoomPresenceRoomId.kt` |
| `live_reaction.get_reactions` | `AmityLiveReactionGetReactions.kt` |
| `live_reaction.create_reaction` | `AmityLiveReactionCreateReaction.kt` |
| `live_reaction.create_room_reaction` | `AmityLiveReactionCreateRoomReaction.kt` |
| `post.create_mixed_attachment` | `AmityPostCreateMixedAttachment.kt` |
| `post.get_pinned` | `AmityPostGetPinned.kt` |
| `post.get_global_pinned` | `AmityPostGetGlobalPinned.kt` |
| `post.semantic_search` | `AmityPostSemanticSearch.kt` |
| `story.get_story_target` | `AmityStoryGetStoryTarget.kt` |
| `story.get_story_targets` | `AmityStoryGetStoryTargets.kt` |
| `story.get_global_story_targets` | `AmityStoryGetGlobalStoryTargets.kt` |
| `story.get_active` | `AmityStoryGetActive.kt` |
| `story.get_by_targets` | `AmityStoryGetByTargets.kt` |
| `story.soft_delete` | `AmityStorySoftDelete.kt` |
| `story.hard_delete` | `AmityStoryHardDelete.kt` |
| `room.get_co_host_event` | `AmityRoomGetCoHostEvent.kt` |
| `room.update_cohost_permission` | `AmityRoomUpdateCohostPermission.kt` |
| `marker_sync.sync_markers` | `AmityMarkerSyncSyncMarkers.kt` |
| `user_marker.get` | `AmityUserMarkerGet.kt` |
| `analytics.save_analytic_event` | `AmityAnalyticsSaveAnalyticEvent.kt` |
| `analytics.send_analytics_events` | `AmityAnalyticsSendAnalyticsEvents.kt` |
| `analytics.delete_all_analytics_events` | `AmityAnalyticsDeleteAllAnalyticsEvents.kt` |
| `analytics.get_viewed_users` | `AmityAnalyticsGetViewedUsers.kt` |
| `analytics.create_analytic_event` | `AmityAnalyticsCreateAnalyticEvent.kt` |
| `community_notification.save_notification_settings` | `AmityCommunityNotificationSaveNotificationSettings.kt` |
| `community_notification.get_notification_settings` | `AmityCommunityNotificationGetNotificationSettings.kt` |
| `user_relationship.has_in_local` | `AmityUserRelationshipHasInLocal.kt` |
| `tombstone.get` | `AmityTombstoneGet.kt` |
| `tombstone.save` | `AmityTombstoneSave.kt` |
| `stream_player.get_function` | `AmityStreamPlayerGetFunction.kt` |
| `stream_broadcaster.get_function` | `AmityStreamBroadcasterGetFunction.kt` |

### Ios (Swift) — 40 functions

Snippet directory: `../../AmitySDKIOS/SDKSampleCode/SDKSampleCode`

| Function ID | Write to filename |
|-------------|-------------------|
| `client.get_user_unread` | `AmityClientGetUserUnread.swift` |
| `client.enable_unread_count` | `AmityClientEnableUnreadCount.swift` |
| `client.get_visitor_device_id` | `AmityClientGetVisitorDeviceId.swift` |
| `client.secure_logout` | `AmityClientSecureLogout.swift` |
| `client.validate_urls` | `AmityClientValidateUrls.swift` |
| `client.validate_texts` | `AmityClientValidateTexts.swift` |
| `client.set_uploaded_file_access_type` | `AmityClientSetUploadedFileAccessType.swift` |
| `client.send_custom_command_request` | `AmityClientSendCustomCommandRequest.swift` |
| `client.get_shareable_link_configuration` | `AmityClientGetShareableLinkConfiguration.swift` |
| `client.send_custom_command` | `AmityClientSendCustomCommand.swift` |
| `client.observe_network_activities` | `AmityClientObserveNetworkActivities.swift` |
| `client.get_link_preview_metadata` | `AmityClientGetLinkPreviewMetadata.swift` |
| `channel.get_total_channels_unread` | `AmityChannelGetTotalChannelsUnread.swift` |
| `room_presence.start_heartbeat` | `AmityRoomPresenceStartHeartbeat.swift` |
| `room_presence.stop_heartbeat` | `AmityRoomPresenceStopHeartbeat.swift` |
| `room_presence.get_room_online_users` | `AmityRoomPresenceGetRoomOnlineUsers.swift` |
| `room_presence.get_room_user_count` | `AmityRoomPresenceGetRoomUserCount.swift` |
| `room.generate_room_token` | `AmityRoomGenerateRoomToken.swift` |
| `comment.get_reactions` | `AmityCommentGetReactions.swift` |
| `feed.get_my` | `AmityFeedGetMy.swift` |
| `post.get_reactions` | `AmityPostGetReactions.swift` |
| `file.download_image_as_data` | `AmityFileDownloadImageAsData.swift` |
| `file.download_image` | `AmityFileDownloadImage.swift` |
| `file.download_file_as_data` | `AmityFileDownloadFileAsData.swift` |
| `file.get_upload_progress` | `AmityFileGetUploadProgress.swift` |
| `file.cancel_file_download` | `AmityFileCancelFileDownload.swift` |
| `file.cancel_image_download` | `AmityFileCancelImageDownload.swift` |
| `message.delete_failed` | `AmityMessageDeleteFailed.swift` |
| `message.get_reactions` | `AmityMessageGetReactions.swift` |
| `message.set_tags` | `AmityMessageSetTags.swift` |
| `reaction.get` | `AmityReactionGet.swift` |
| `story.get_active_by_target` | `AmityStoryGetActiveByTarget.swift` |
| `story.get_by_targets` | `AmityStoryGetByTargets.swift` |
| `story.get_story_target` | `AmityStoryGetStoryTarget.swift` |
| `story.soft_delete` | `AmityStorySoftDelete.swift` |
| `story.hard_delete` | `AmityStoryHardDelete.swift` |
| `story.get_story_targets` | `AmityStoryGetStoryTargets.swift` |
| `story.get_global_story_targets` | `AmityStoryGetGlobalStoryTargets.swift` |
| `sub_channel.start_message_receipt_sync` | `AmitySubChannelStartMessageReceiptSync.swift` |
| `sub_channel.stop_message_receipt_sync` | `AmitySubChannelStopMessageReceiptSync.swift` |

### Flutter (Dart) — 61 functions

Snippet directory: `../../Amity-Social-Cloud-SDK-Flutter-Internal/code_snippet`

| Function ID | Write to filename |
|-------------|-------------------|
| `core.validate_urls` | `AmityCoreValidateUrls.dart` |
| `core.validate_texts` | `AmityCoreValidateTexts.dart` |
| `core.is_user_logged_in` | `AmityCoreIsUserLoggedIn.dart` |
| `core.get_user_id` | `AmityCoreGetUserId.dart` |
| `core.has_permission` | `AmityCoreHasPermission.dart` |
| `core.get_analytics_engine` | `AmityCoreGetAnalyticsEngine.dart` |
| `core.observe_session_state` | `AmityCoreObserveSessionState.dart` |
| `core.observe_unread_count` | `AmityCoreObserveUnreadCount.dart` |
| `core.copy_with` | `AmityCoreCopyWith.dart` |
| `chat.service_locator` | `AmityChatServiceLocator.dart` |
| `chat.new_channel_repository` | `AmityChatNewChannelRepository.dart` |
| `chat.new_sub_channel_repository` | `AmityChatNewSubChannelRepository.dart` |
| `social.new_post_repository` | `AmitySocialNewPostRepository.dart` |
| `social.new_comment_repository` | `AmitySocialNewCommentRepository.dart` |
| `social.new_feed_repository` | `AmitySocialNewFeedRepository.dart` |
| `social.new_community_repository` | `AmitySocialNewCommunityRepository.dart` |
| `social.new_poll_repository` | `AmitySocialNewPollRepository.dart` |
| `social.new_story_repository` | `AmitySocialNewStoryRepository.dart` |
| `social.new_reaction_repository` | `AmitySocialNewReactionRepository.dart` |
| `video.new_stream_repository` | `AmityVideoNewStreamRepository.dart` |
| `ad.service_locator` | `AmityAdServiceLocator.dart` |
| `community.service_locator` | `AmityCommunityServiceLocator.dart` |
| `community.get_current_user_roles` | `AmityCommunityGetCurrentUserRoles.dart` |
| `file.cancel_upload` | `AmityFileCancelUpload.dart` |
| `post.service_locator` | `AmityPostServiceLocator.dart` |
| `post.get_post_stream` | `AmityPostGetPostStream.dart` |
| `post.review` | `AmityPostReview.dart` |
| `post.get_reaction` | `AmityPostGetReaction.dart` |
| `post.get_pinned` | `AmityPostGetPinned.dart` |
| `post.get_global_pinned` | `AmityPostGetGlobalPinned.dart` |
| `channel.service_locator` | `AmityChannelServiceLocator.dart` |
| `channel.start_reading` | `AmityChannelStartReading.dart` |
| `channel.stop_reading` | `AmityChannelStopReading.dart` |
| `channel.archive` | `AmityChannelArchive.dart` |
| `channel.unarchive` | `AmityChannelUnarchive.dart` |
| `channel.get_archived` | `AmityChannelGetArchived.dart` |
| `channel.get_channel_total_unreads` | `AmityChannelGetChannelTotalUnreads.dart` |
| `channel_moderation.channel_id` | `AmityChannelModerationChannelId.dart` |
| `message.get_reaction` | `AmityMessageGetReaction.dart` |
| `notification.service_locator` | `AmityNotificationServiceLocator.dart` |
| `notification.unregister_device` | `AmityNotificationUnregisterDevice.dart` |
| `stream.service_locator` | `AmityStreamServiceLocator.dart` |
| `sub_channel.get` | `AmitySubChannelGet.dart` |
| `sub_channel.soft_delete` | `AmitySubChannelSoftDelete.dart` |
| `sub_channel.hard_delete` | `AmitySubChannelHardDelete.dart` |
| `sub_channel.updateedit_sub_channel` | `AmitySubChannelUpdateeditSubChannel.dart` |
| `my_user_relationship.get_blocked_users` | `AmityMyUserRelationshipGetBlockedUsers.dart` |
| `user_relationships.service_locator` | `AmityUserRelationshipsServiceLocator.dart` |
| `user_relationships.accept_my_follower` | `AmityUserRelationshipsAcceptMyFollower.dart` |
| `user_relationships.decline_my_follower` | `AmityUserRelationshipsDeclineMyFollower.dart` |
| `user_relationships.remove_my_follower` | `AmityUserRelationshipsRemoveMyFollower.dart` |
| `user_relationships.get_my_followings` | `AmityUserRelationshipsGetMyFollowings.dart` |
| `user_relationships.get_followings` | `AmityUserRelationshipsGetFollowings.dart` |
| `user_relationships.get_my_followers` | `AmityUserRelationshipsGetMyFollowers.dart` |
| `user_relationships.get_followers` | `AmityUserRelationshipsGetFollowers.dart` |
| `user_relationships.get_my_follow_info` | `AmityUserRelationshipsGetMyFollowInfo.dart` |
| `user_relationships.get_follow_info` | `AmityUserRelationshipsGetFollowInfo.dart` |
| `user_relationships.block_user` | `AmityUserRelationshipsBlockUser.dart` |
| `user_relationships.unblock_user` | `AmityUserRelationshipsUnblockUser.dart` |
| `user.get_blocked` | `AmityUserGetBlocked.dart` |
| `user.get_viewed` | `AmityUserGetViewed.dart` |

## DOC_PAGE_STALE_IMPORT (11)

These doc pages reference gendocs snippet files that are not yet imported.
Run the migrate command to automatically add the missing imports:

```bash
cd social-plus-docs/harness
./harness-bin migrate --config harness-config.yml
```

Or preview changes first with `--dry-run`:

```bash
./harness-bin migrate --config harness-config.yml --dry-run
```


---

## PUBLIC_FUNC_UNANNOTATED (11 functions)

**Full list:** `harness/unannotated-functions-report.md`

Use the `annotate` command to generate annotation patches automatically, then review and apply.

### Step 1 — Generate annotation patches

```bash
cd social-plus-docs/harness
./harness-bin annotate --config harness-config.yml
```

This writes `annotation-patches.yml` with one entry per unannotated function,
including a suggested `id:` value (e.g. `post.create`, `comment.get`).

### Step 2 — Review and correct id values

Open `annotation-patches.yml` and verify each `id:` follows the `feature.action` convention.
Check existing ids in the SDK source for consistency (search for `begin_public_function`).

### Step 3 — Apply patches

```bash
./harness-bin annotate --config harness-config.yml --apply
```

This inserts `begin_public_function` + `end_public_function` markers directly into SDK source files.

### Step 4 — Verify

```bash
./harness-bin audit --config harness-config.yml
```

**Expected:** `PUBLIC_FUNC_UNANNOTATED` count drops. The audit reads SDK source directly —
only actual source file changes count as proof. You cannot satisfy this check by editing
`harness-tasks.md`, `annotation-patches.yml`, or `unannotated-functions-report.md`.
---

## After completion

Run the full audit to verify all tasks are resolved:

```bash
cd social-plus-docs/harness
./harness-bin audit --config harness-config.yml
```

**Expected result:** zero `open` findings. The audit is the authoritative proof —
it re-reads source files directly and cannot be satisfied by editing task or report files.

If findings remain, run `./harness-bin prompt` to regenerate this file with the remaining work.
