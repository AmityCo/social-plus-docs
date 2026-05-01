# SDK Harness — Agent Runbook

_Generated 2026-05-01 10:35 — 1 findings requiring AI_

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


---

## MANIFEST_FILL (8 sections need assignment)

For each section below, edit the manifest file and add the GendocsKeys
that belong in that section to the `snippets:` array.

### social-plus-sdk/core-concepts/foundation/logging → key-features

**Manifest:** `social-plus-sdk/core-concepts/foundation/logging.manifest.yml`
**Section:** `### Key Features`
**Available keys:**
- `channel-presence-observe`
- `channel-presence-sync`
- `channel-presence-unsync-all`
- `channel-presence-unsync`
- `channel_level_notificaiton_toggle`
- `client-get-configuration`
- `client-get-current-user-type`
- `client-get-current-user`
- `client-get-mention-configurations`
- `client-get-notification-settings`
- `client-presence-disable`
- `client-presence-enable`
- `client-presence-is-enabled`
- `client-presence-start-heartbeat`
- `client-presence-stop-heartbeat`
- `client-register-push-notification`
- `client-register-push`
- `client-unregister-push-notification`
- `client-unregister-push`
- `client-update-notification-settings`
- `client-update-user`
- `comment-reaction-add`
- `comment-reaction-query`
- `comment-reaction-remove`
- `compose-live-collection-sample`
- `compose-live-object-sample`
- `core-model-mentionee`
- `create_reaction_repository`
- `create_user_token`
- `delete_file`
- `delete_poll`
- `download_image`
- `enable_presence_settings`
- `error_handling`
- `file-delete`
- `file-get`
- `file-update-alt-text`
- `file-upload-audio`
- `file-upload-clip`
- `file-upload-file`
- `file-upload-image`
- `file-upload-video`
- `flag_user`
- `get-network-ads`
- `get_file_with_id`
- `get_video_thumbnail`
- `image-get`
- `is_user_flagged-by-me`
- `live-reaction-create`
- `mark-ad-clicked`
- `mark-ad-seen`
- `message-reaction-add`
- `message-reaction-query`
- `message-reaction-remove`
- `notification-community-settings-get`
- `notification-community-settings-set`
- `notification-fcm-observer`
- `notification-get-settings`
- `notification-register`
- `notification-registration`
- `notification-unregister`
- `notification-unregistration`
- `notification-update-settings`
- `notification-user-settings-get`
- `notification-user-settings-set`
- `online-users-count`
- `online-users-snapshot`
- `poll-get`
- `poll-unvote`
- `post-create-poll-post`
- `post-reaction-add`
- `post-reaction-query`
- `post-reaction-remove`
- `presence-heartbeat-start`
- `presence-heartbeat-stop`
- `presence-settings-disable`
- `presence-settings-enable`
- `presence-settings-query`
- `r-t-e-comment-subscription`
- `r-t-e-community-subscription`
- `r-t-e-follow-subscription`
- `r-t-e-post-subscription`
- `r-t-e-story-subscription`
- `r-t-e-unsubscription`
- `r-t-e-user-subscription`
- `reaction-add-reaction`
- `reaction-comment-add`
- `reaction-comment-query`
- `reaction-comment-remove`
- `reaction-get-reactions`
- `reaction-post-add`
- `reaction-post-query`
- `reaction-post-remove`
- `reaction-query`
- `reaction-remove-reaction`
- `request_push_notifcation_permission`
- `setup_sdk_notification`
- `story-reaction-add`
- `story-reaction-query`
- `story-reaction-remove`
- `subscription_topic_example`
- `unflag_user`
- `unsync_all_channel_presence`
- `unsync_all_user_presence`
- `update_file_alt_text`
- `upload_image`
- `user-check-flag-by-me`
- `user-flag`
- `user-get-viewed-users`
- `user-is-flagged-by-me`
- `user-presence-get-online-users-count`
- `user-presence-get-online-users-snapshot`
- `user-presence-get-syncing-user-presence`
- `user-presence-get-user-presence`
- `user-presence-observe`
- `user-presence-query`
- `user-presence-sync-user-presence`
- `user-presence-sync`
- `user-presence-unsync-all-user-presence`
- `user-presence-unsync-all`
- `user-presence-unsync-user-presence`
- `user-presence-unsync`
- `user-unflag`
- `validate-text`
- `validate-url`
- `video-get`

### social-plus-sdk/core-concepts/user-management/user-identity → initializing-user-repository

**Manifest:** `social-plus-sdk/core-concepts/user-management/user-identity.manifest.yml`
**Section:** `### Initializing User Repository`
**Available keys:**
- `channel-presence-observe`
- `channel-presence-sync`
- `channel-presence-unsync-all`
- `channel-presence-unsync`
- `channel_level_notificaiton_toggle`
- `client-get-configuration`
- `client-get-current-user-type`
- `client-get-current-user`
- `client-get-mention-configurations`
- `client-get-notification-settings`
- `client-presence-disable`
- `client-presence-enable`
- `client-presence-is-enabled`
- `client-presence-start-heartbeat`
- `client-presence-stop-heartbeat`
- `client-register-push-notification`
- `client-register-push`
- `client-unregister-push-notification`
- `client-unregister-push`
- `client-update-notification-settings`
- `client-update-user`
- `comment-reaction-add`
- `comment-reaction-query`
- `comment-reaction-remove`
- `compose-live-collection-sample`
- `compose-live-object-sample`
- `core-model-mentionee`
- `create_reaction_repository`
- `create_user_token`
- `delete_file`
- `delete_poll`
- `download_image`
- `enable_presence_settings`
- `error_handling`
- `file-delete`
- `file-get`
- `file-update-alt-text`
- `file-upload-audio`
- `file-upload-clip`
- `file-upload-file`
- `file-upload-image`
- `file-upload-video`
- `flag_user`
- `get-network-ads`
- `get_file_with_id`
- `get_video_thumbnail`
- `image-get`
- `is_user_flagged-by-me`
- `live-reaction-create`
- `mark-ad-clicked`
- `mark-ad-seen`
- `message-reaction-add`
- `message-reaction-query`
- `message-reaction-remove`
- `notification-community-settings-get`
- `notification-community-settings-set`
- `notification-fcm-observer`
- `notification-get-settings`
- `notification-register`
- `notification-registration`
- `notification-unregister`
- `notification-unregistration`
- `notification-update-settings`
- `notification-user-settings-get`
- `notification-user-settings-set`
- `online-users-count`
- `online-users-snapshot`
- `poll-get`
- `poll-unvote`
- `post-create-poll-post`
- `post-reaction-add`
- `post-reaction-query`
- `post-reaction-remove`
- `presence-heartbeat-start`
- `presence-heartbeat-stop`
- `presence-settings-disable`
- `presence-settings-enable`
- `presence-settings-query`
- `r-t-e-comment-subscription`
- `r-t-e-community-subscription`
- `r-t-e-follow-subscription`
- `r-t-e-post-subscription`
- `r-t-e-story-subscription`
- `r-t-e-unsubscription`
- `r-t-e-user-subscription`
- `reaction-add-reaction`
- `reaction-comment-add`
- `reaction-comment-query`
- `reaction-comment-remove`
- `reaction-get-reactions`
- `reaction-post-add`
- `reaction-post-query`
- `reaction-post-remove`
- `reaction-query`
- `reaction-remove-reaction`
- `request_push_notifcation_permission`
- `setup_sdk_notification`
- `story-reaction-add`
- `story-reaction-query`
- `story-reaction-remove`
- `subscription_topic_example`
- `unflag_user`
- `unsync_all_channel_presence`
- `unsync_all_user_presence`
- `update_file_alt_text`
- `upload_image`
- `user-check-flag-by-me`
- `user-flag`
- `user-get-viewed-users`
- `user-is-flagged-by-me`
- `user-presence-get-online-users-count`
- `user-presence-get-online-users-snapshot`
- `user-presence-get-syncing-user-presence`
- `user-presence-get-user-presence`
- `user-presence-observe`
- `user-presence-query`
- `user-presence-sync-user-presence`
- `user-presence-sync`
- `user-presence-unsync-all-user-presence`
- `user-presence-unsync-all`
- `user-presence-unsync-user-presence`
- `user-presence-unsync`
- `user-unflag`
- `validate-text`
- `validate-url`
- `video-get`

### social-plus-sdk/core-concepts/user-management/user-operations/search-and-query-users → query-implementation

**Manifest:** `social-plus-sdk/core-concepts/user-management/user-operations/search-and-query-users.manifest.yml`
**Section:** `### Query Implementation`
**Available keys:**
- `channel-presence-observe`
- `channel-presence-sync`
- `channel-presence-unsync-all`
- `channel-presence-unsync`
- `channel_level_notificaiton_toggle`
- `client-get-configuration`
- `client-get-current-user-type`
- `client-get-current-user`
- `client-get-mention-configurations`
- `client-get-notification-settings`
- `client-presence-disable`
- `client-presence-enable`
- `client-presence-is-enabled`
- `client-presence-start-heartbeat`
- `client-presence-stop-heartbeat`
- `client-register-push-notification`
- `client-register-push`
- `client-unregister-push-notification`
- `client-unregister-push`
- `client-update-notification-settings`
- `client-update-user`
- `comment-reaction-add`
- `comment-reaction-query`
- `comment-reaction-remove`
- `compose-live-collection-sample`
- `compose-live-object-sample`
- `core-model-mentionee`
- `create_reaction_repository`
- `create_user_token`
- `delete_file`
- `delete_poll`
- `download_image`
- `enable_presence_settings`
- `error_handling`
- `file-delete`
- `file-get`
- `file-update-alt-text`
- `file-upload-audio`
- `file-upload-clip`
- `file-upload-file`
- `file-upload-image`
- `file-upload-video`
- `flag_user`
- `get-network-ads`
- `get_file_with_id`
- `get_video_thumbnail`
- `image-get`
- `is_user_flagged-by-me`
- `live-reaction-create`
- `mark-ad-clicked`
- `mark-ad-seen`
- `message-reaction-add`
- `message-reaction-query`
- `message-reaction-remove`
- `notification-community-settings-get`
- `notification-community-settings-set`
- `notification-fcm-observer`
- `notification-get-settings`
- `notification-register`
- `notification-registration`
- `notification-unregister`
- `notification-unregistration`
- `notification-update-settings`
- `notification-user-settings-get`
- `notification-user-settings-set`
- `online-users-count`
- `online-users-snapshot`
- `poll-get`
- `poll-unvote`
- `post-create-poll-post`
- `post-reaction-add`
- `post-reaction-query`
- `post-reaction-remove`
- `presence-heartbeat-start`
- `presence-heartbeat-stop`
- `presence-settings-disable`
- `presence-settings-enable`
- `presence-settings-query`
- `r-t-e-comment-subscription`
- `r-t-e-community-subscription`
- `r-t-e-follow-subscription`
- `r-t-e-post-subscription`
- `r-t-e-story-subscription`
- `r-t-e-unsubscription`
- `r-t-e-user-subscription`
- `reaction-add-reaction`
- `reaction-comment-add`
- `reaction-comment-query`
- `reaction-comment-remove`
- `reaction-get-reactions`
- `reaction-post-add`
- `reaction-post-query`
- `reaction-post-remove`
- `reaction-query`
- `reaction-remove-reaction`
- `request_push_notifcation_permission`
- `setup_sdk_notification`
- `story-reaction-add`
- `story-reaction-query`
- `story-reaction-remove`
- `subscription_topic_example`
- `unflag_user`
- `unsync_all_channel_presence`
- `unsync_all_user_presence`
- `update_file_alt_text`
- `upload_image`
- `user-check-flag-by-me`
- `user-flag`
- `user-get-viewed-users`
- `user-is-flagged-by-me`
- `user-presence-get-online-users-count`
- `user-presence-get-online-users-snapshot`
- `user-presence-get-syncing-user-presence`
- `user-presence-get-user-presence`
- `user-presence-observe`
- `user-presence-query`
- `user-presence-sync-user-presence`
- `user-presence-sync`
- `user-presence-unsync-all-user-presence`
- `user-presence-unsync-all`
- `user-presence-unsync-user-presence`
- `user-presence-unsync`
- `user-unflag`
- `validate-text`
- `validate-url`
- `video-get`

### social-plus-sdk/core-concepts/user-management/user-operations/search-and-query-users → search-implementation

**Manifest:** `social-plus-sdk/core-concepts/user-management/user-operations/search-and-query-users.manifest.yml`
**Section:** `### Search Implementation`
**Available keys:**
- `channel-presence-observe`
- `channel-presence-sync`
- `channel-presence-unsync-all`
- `channel-presence-unsync`
- `channel_level_notificaiton_toggle`
- `client-get-configuration`
- `client-get-current-user-type`
- `client-get-current-user`
- `client-get-mention-configurations`
- `client-get-notification-settings`
- `client-presence-disable`
- `client-presence-enable`
- `client-presence-is-enabled`
- `client-presence-start-heartbeat`
- `client-presence-stop-heartbeat`
- `client-register-push-notification`
- `client-register-push`
- `client-unregister-push-notification`
- `client-unregister-push`
- `client-update-notification-settings`
- `client-update-user`
- `comment-reaction-add`
- `comment-reaction-query`
- `comment-reaction-remove`
- `compose-live-collection-sample`
- `compose-live-object-sample`
- `core-model-mentionee`
- `create_reaction_repository`
- `create_user_token`
- `delete_file`
- `delete_poll`
- `download_image`
- `enable_presence_settings`
- `error_handling`
- `file-delete`
- `file-get`
- `file-update-alt-text`
- `file-upload-audio`
- `file-upload-clip`
- `file-upload-file`
- `file-upload-image`
- `file-upload-video`
- `flag_user`
- `get-network-ads`
- `get_file_with_id`
- `get_video_thumbnail`
- `image-get`
- `is_user_flagged-by-me`
- `live-reaction-create`
- `mark-ad-clicked`
- `mark-ad-seen`
- `message-reaction-add`
- `message-reaction-query`
- `message-reaction-remove`
- `notification-community-settings-get`
- `notification-community-settings-set`
- `notification-fcm-observer`
- `notification-get-settings`
- `notification-register`
- `notification-registration`
- `notification-unregister`
- `notification-unregistration`
- `notification-update-settings`
- `notification-user-settings-get`
- `notification-user-settings-set`
- `online-users-count`
- `online-users-snapshot`
- `poll-get`
- `poll-unvote`
- `post-create-poll-post`
- `post-reaction-add`
- `post-reaction-query`
- `post-reaction-remove`
- `presence-heartbeat-start`
- `presence-heartbeat-stop`
- `presence-settings-disable`
- `presence-settings-enable`
- `presence-settings-query`
- `r-t-e-comment-subscription`
- `r-t-e-community-subscription`
- `r-t-e-follow-subscription`
- `r-t-e-post-subscription`
- `r-t-e-story-subscription`
- `r-t-e-unsubscription`
- `r-t-e-user-subscription`
- `reaction-add-reaction`
- `reaction-comment-add`
- `reaction-comment-query`
- `reaction-comment-remove`
- `reaction-get-reactions`
- `reaction-post-add`
- `reaction-post-query`
- `reaction-post-remove`
- `reaction-query`
- `reaction-remove-reaction`
- `request_push_notifcation_permission`
- `setup_sdk_notification`
- `story-reaction-add`
- `story-reaction-query`
- `story-reaction-remove`
- `subscription_topic_example`
- `unflag_user`
- `unsync_all_channel_presence`
- `unsync_all_user_presence`
- `update_file_alt_text`
- `upload_image`
- `user-check-flag-by-me`
- `user-flag`
- `user-get-viewed-users`
- `user-is-flagged-by-me`
- `user-presence-get-online-users-count`
- `user-presence-get-online-users-snapshot`
- `user-presence-get-syncing-user-presence`
- `user-presence-get-user-presence`
- `user-presence-observe`
- `user-presence-query`
- `user-presence-sync-user-presence`
- `user-presence-sync`
- `user-presence-unsync-all-user-presence`
- `user-presence-unsync-all`
- `user-presence-unsync-user-presence`
- `user-presence-unsync`
- `user-unflag`
- `validate-text`
- `validate-url`
- `video-get`

### social-plus-sdk/getting-started/visitor-mode → permission-enforcement

**Manifest:** `social-plus-sdk/getting-started/visitor-mode.manifest.yml`
**Section:** `### Permission Enforcement`
**Available keys:**
- `client-fetch-link-preview`
- `client-get-login-method`
- `client-get-product-catalogue-setting`
- `client-login-as-bot`
- `client-login-as-visitor`
- `client-login-with-access-token`
- `client-login`
- `client-logout`
- `client-observe-session-state`
- `client-read-session-state`
- `client-renew-access-token`
- `client-renew-with-access-token`
- `client-resume-session`
- `client-secure-logout`
- `client-set-access-token-handler`
- `my-view`
- `my_session_handler`
- `observe_session_state`
- `product-get`
- `renewal_with_auth_token`

### social-plus-sdk/getting-started/visitor-mode → step-2-get-visitor-device-id

**Manifest:** `social-plus-sdk/getting-started/visitor-mode.manifest.yml`
**Section:** `### Step 2: Get Visitor Device ID`
**Available keys:**
- `client-fetch-link-preview`
- `client-get-login-method`
- `client-get-product-catalogue-setting`
- `client-login-as-bot`
- `client-login-as-visitor`
- `client-login-with-access-token`
- `client-login`
- `client-logout`
- `client-observe-session-state`
- `client-read-session-state`
- `client-renew-access-token`
- `client-renew-with-access-token`
- `client-resume-session`
- `client-secure-logout`
- `client-set-access-token-handler`
- `my-view`
- `my_session_handler`
- `observe_session_state`
- `product-get`
- `renewal_with_auth_token`

### social-plus-sdk/video-new/analytics/overview → amityroom-extension

**Manifest:** `social-plus-sdk/video-new/analytics/overview.manifest.yml`
**Section:** `### AmityRoom Extension`
**Available keys:**
- `child-stream-access`
- `child-stream-create`
- `compose-video-camera-sample`
- `compose-video-player-sample`
- `get_recorded_livestreams`
- `live-stream-chat`
- `live-stream-create`
- `live-stream-dispose`
- `live-stream-moderation`
- `live-stream-play`
- `live-stream-post-create`
- `live-stream-reaction`
- `play_a_livestream`
- `post-cd-get-community-live-room-posts`
- `post-cd-get-live-room-posts`
- `post-community-live-room-query`
- `post-create-live-stream`
- `post-create-livestream-post`
- `post-create-room-post`
- `post-get-community-live-room-posts`
- `post-get-live-room-posts`
- `post-live-room-query`
- `recorded-stream-play`
- `room-cancel-invitation`
- `room-create-invitation`
- `room-create`
- `room-delete`
- `room-get-broadcaster-data`
- `room-get-co-host-event`
- `room-get-recorded-url`
- `room-get-rooms`
- `room-get`
- `room-leave`
- `room-presence-get-room-online-users`
- `room-presence-get-room-user-count`
- `room-presence-start-heartbeat`
- `room-presence-stop-heartbeat`
- `room-remove-participant`
- `room-stop`
- `room-update-cohost-permissions`
- `room-update`
- `stream-broadcaster-setup`
- `stream-broadcaster-start-publish`
- `stream-broadcaster-stop-publish`
- `stream-broadcaster-switch-camera`
- `stream-create`
- `stream-delete`
- `stream-dispose`
- `stream-end`
- `stream-get`
- `stream-live-query`
- `stream-player-play`
- `stream-player-stop`
- `stream-query`
- `stream-update`
- `stream_moderation`

### social-plus-sdk/video-new/analytics/overview → amityroomanalytics

**Manifest:** `social-plus-sdk/video-new/analytics/overview.manifest.yml`
**Section:** `### AmityRoomAnalytics`
**Available keys:**
- `child-stream-access`
- `child-stream-create`
- `compose-video-camera-sample`
- `compose-video-player-sample`
- `get_recorded_livestreams`
- `live-stream-chat`
- `live-stream-create`
- `live-stream-dispose`
- `live-stream-moderation`
- `live-stream-play`
- `live-stream-post-create`
- `live-stream-reaction`
- `play_a_livestream`
- `post-cd-get-community-live-room-posts`
- `post-cd-get-live-room-posts`
- `post-community-live-room-query`
- `post-create-live-stream`
- `post-create-livestream-post`
- `post-create-room-post`
- `post-get-community-live-room-posts`
- `post-get-live-room-posts`
- `post-live-room-query`
- `recorded-stream-play`
- `room-cancel-invitation`
- `room-create-invitation`
- `room-create`
- `room-delete`
- `room-get-broadcaster-data`
- `room-get-co-host-event`
- `room-get-recorded-url`
- `room-get-rooms`
- `room-get`
- `room-leave`
- `room-presence-get-room-online-users`
- `room-presence-get-room-user-count`
- `room-presence-start-heartbeat`
- `room-presence-stop-heartbeat`
- `room-remove-participant`
- `room-stop`
- `room-update-cohost-permissions`
- `room-update`
- `stream-broadcaster-setup`
- `stream-broadcaster-start-publish`
- `stream-broadcaster-stop-publish`
- `stream-broadcaster-switch-camera`
- `stream-create`
- `stream-delete`
- `stream-dispose`
- `stream-end`
- `stream-get`
- `stream-live-query`
- `stream-player-play`
- `stream-player-stop`
- `stream-query`
- `stream-update`
- `stream_moderation`

## DOC_PAGE_STALE_IMPORT (1)

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

## PUBLIC_FUNC_UNANNOTATED (1253 functions need sp_docs_page: annotation)

These public functions in `*Repository` / `*Client` classes have no `sp_docs_page:` annotation.
Add a `begin_sample_code` block with the appropriate `sp_docs_page:` value, or skip if internal.

### ANDROID (759 functions)

**`AmityPostRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/api/social/post/AmityPostRepository.kt`) — 31 functions:
- `getPost`
- `getPostByIds`
- `getPosts`
- `searchPostsByHashtag`
- `createTextPost`
- `createImagePost`
- `createFilePost`
- `createVideoPost`
- `createClipPost`
- `createPollPost`
- `createLiveStreamPost`
- `createRoomPost`
- `createCustomPost`
- `createAudioPost`
- `createMixedAttachmentPost`
- `editPost`
- `editCustomPost`
- `softDeletePost`
- `hardDeletePost`
- `approvePost`
- `declinePost`
- `flagPost`
- `unflagPost`
- `getPinnedPosts`
- `getGlobalPinnedPosts`
- `getLiveRoomPosts`
- `getCommunityLiveRoomPosts`
- `semanticSearchPosts`
- `createPost`
- `pinProduct`
- `unpinProduct`

**`ReadReceiptRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/chat/data/marker/readreceipt/ReadReceiptRepository.kt`) — 12 functions:
- `getLegacyReadReceipt`
- `saveLegacyReadReceipts`
- `updateLegacyLatestSegment`
- `updateLegacyLatestSyncSegment`
- `deleteLegacyReadReceipt`
- `getUnsyncLegacyReadReceipt`
- `getReadReceipt`
- `saveReadReceipts`
- `updateLatestSegment`
- `updateLatestSyncSegment`
- `deleteReadReceipt`
- `getUnsyncReadReceipt`

**`PinRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/core/data/pin/PinRepository.kt`) — 2 functions:
- `getPinnedPostPagingData`
- `getGlobalPinnedPostPagingData`

**`ReactionRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/core/data/reaction/ReactionRepository.kt`) — 9 functions:
- `getReactionPagingData`
- `getMyReactions`
- `getLatestReaction`
- `addReaction`
- `removeReaction`
- `createMyReaction`
- `observeLiveReactions`
- `addLiveReactions`
- `addRoomReactions`

**`ChannelMembershipRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/chat/data/channel/membership/ChannelMembershipRepository.kt`) — 18 functions:
- `observeChannelMember`
- `observeChannelMembers`
- `addChannelMembers`
- `removeChannelMembers`
- `getChannelMembershipPagingData`
- `searchChannelMembershipPagingData`
- `assignChannelRole`
- `unassignChannelRole`
- `banChannelUsers`
- `unbanChannelUsers`
- `muteChannelUsers`
- `unmuteChannelUsers`
- `muteChannel`
- `unmuteChannel`
- `handleMembershipBanned`
- `handleMembershipMuted`
- `getLatestChannel`
- `getChannelMembers`

**`ChannelMarkerRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/chat/data/marker/channel/ChannelMarkerRepository.kt`) — 10 functions:
- `fetchChannelMarker`
- `getChannelMarker`
- `saveChannelMarkers`
- `markChannelAsRead`
- `getChannelUnreadInfo`
- `saveChannelUnreadInfo`
- `getTotalChannelsUnreadInfo`
- `getChannelUnread`
- `saveChannelUnread`
- `getTotalChannelsUnread`

**`CoreClient`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/core/CoreClient.kt`) — 25 functions:
- `setup`
- `disconnect`
- `login`
- `loginAsVisitor`
- `loginWithAccessToken`
- `setAccessTokenHandler`
- `getLoginMethod`
- `publishLogoutEvent`
- `observeSessionState`
- `observeUserUnread`
- `presence`
- `newUserPresenceRepository`
- `newRoomPresenceRepository`
- `getAnalyticsEngine`
- `createTextMessage`
- `createAttachmentMessage`
- `isConsistentMode`
- `isUnreadCountEnable`
- `enableUnreadCount`
- `markRead`
- `resolve`
- `setUploadedFileAccessType`
- `getUploadedFileAccessType`
- `getAccessToken`
- `observeNetworkActivities`

**`PollRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/social/data/poll/PollRepository.kt`) — 6 functions:
- `createPoll`
- `observePoll`
- `closePoll`
- `deletePoll`
- `vote`
- `unvote`

**`AmityRoomRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/api/video/room/AmityRoomRepository.kt`) — 13 functions:
- `getRooms`
- `getRoom`
- `fetchRoom`
- `createRoom`
- `updateRoom`
- `deleteRoom`
- `stopRoom`
- `getBroadcasterData`
- `getRecordedUrls`
- `leaveRoom`
- `removeRoomParticipant`
- `getCoHostEvent`
- `updateCohostPermission`

**`AmityPollRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/api/social/poll/AmityPollRepository.kt`) — 6 functions:
- `createPoll`
- `getPoll`
- `closePoll`
- `deletePoll`
- `votePoll`
- `unvotePoll`

**`AnalyticsRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/core/data/analytics/AnalyticsRepository.kt`) — 5 functions:
- `saveAnalyticEvent`
- `sendAnalyticsEvents`
- `deleteAllAnalyticsEvents`
- `getViewedUsers`
- `createAnalyticEvent`

**`UserNotificationRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/core/data/notification/user/UserNotificationRepository.kt`) — 2 functions:
- `saveNotificationSettings`
- `getNotificationSettings`

**`NotificationTrayItemRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/core/data/notificationtray/NotificationTrayItemRepository.kt`) — 2 functions:
- `getNotificationTrayItemPagingData`
- `markSeen`

**`SessionRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/core/data/session/SessionRepository.kt`) — 12 functions:
- `getActiveUserId`
- `getVisitorDeviceId`
- `getActiveUserType`
- `login`
- `loginVisitor`
- `loginWithAccessToken`
- `getLoginMethod`
- `logout`
- `revokeAccessToken`
- `clearData`
- `getCurrentAccount`
- `renewToken`

**`PostRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/social/data/post/PostRepository.kt`) — 25 functions:
- `fetchAndSave`
- `queryFromCache`
- `mapper`
- `observeFromCache`
- `getPostByIds`
- `semanticSearchPosts`
- `getUserPostPagingData`
- `getCommunityPostPagingData`
- `searchPosts`
- `getGlobalFeedPagingData`
- `getCustomPostRankingPagingData`
- `getLiveRoomPosts`
- `getUserFeed`
- `getPost`
- `getPosts`
- `createPostV4`
- `deletePost`
- `approvePost`
- `declinePost`
- `editPost`
- `togglePinPost`
- `flagPost`
- `unFlagPost`
- `getLatestPost`
- `isFlaggedByMe`

**`StoryRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/social/data/story/StoryRepository.kt`) — 20 functions:
- `fetchAndSave`
- `queryFromCache`
- `mapper`
- `observeFromCache`
- `generateUniqueId`
- `createLocalImageStory`
- `createImageStory`
- `updateStorySyncState`
- `createLocalVideoStory`
- `createVideoStory`
- `getActiveStories`
- `deleteStory`
- `getStoryNow`
- `getSyncingStoriesCount`
- `getFailedStoriesCount`
- `getHighestStoryExpiresAt`
- `getHighestSyncedStoryExpiresAt`
- `triggerStoryReload`
- `findCache`
- `getStoriesByTargets`

**`AmityUserPresenceRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/api/core/presence/AmityUserPresenceRepository.kt`) — 7 functions:
- `getUserPresence`
- `syncUserPresence`
- `unsyncUserPresence`
- `unsyncAllUserPresence`
- `getSyncingUserPresence`
- `getOnlineUsersSnapshot`
- `getOnlineUsersCount`

**`AmityEventRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/api/social/event/AmityEventRepository.kt`) — 5 functions:
- `getEvent`
- `getEvents`
- `createEvent`
- `updateEvent`
- `deleteEvent`

**`MessageMarkerRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/chat/data/marker/message/MessageMarkerRepository.kt`) — 10 functions:
- `fetchMessageMarker`
- `getReadCount`
- `getDeliveredCount`
- `saveLocalMessageMarkers`
- `markMessageDelivered`
- `markMessageRead`
- `fetchMessageReadUsers`
- `getMessageReadUsers`
- `fetchMessageDeliveredUsers`
- `getMessageDeliveredUsers`

**`ContentCheckRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/core/data/content/ContentCheckRepository.kt`) — 1 functions:
- `fetchContentCheck`

**`ChannelNotificationRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/core/data/notification/channel/ChannelNotificationRepository.kt`) — 2 functions:
- `saveNotificationSettings`
- `getNotificationSettings`

**`PresenceRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/core/data/presence/PresenceRepository.kt`) — 13 functions:
- `getPresenceUserSetting`
- `getPresenceNetworkSetting`
- `getPresenceRoomSetting`
- `updatePresenceUserSetting`
- `sendPresenceHeartbeat`
- `getUserPresences`
- `getUserPresence`
- `getUserPresenceNow`
- `getOnlineUsers`
- `getOnlineUsersCount`
- `sendRoomPresenceHeartbeat`
- `getRoomUserPresences`
- `getRoomOnlineUsersCount`

**`ShareableLinkRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/core/data/shareablelink/ShareableLinkRepository.kt`) — 1 functions:
- `getShareableLink`

**`TombstoneRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/core/data/tombstone/TombstoneRepository.kt`) — 2 functions:
- `getTombstone`
- `saveTombstone`

**`AmitySocialClient`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/api/social/AmitySocialClient.kt`) — 8 functions:
- `newFeedRepository`
- `newCommunityRepository`
- `newCommentRepository`
- `newPostRepository`
- `newPollRepository`
- `newStoryRepository`
- `newEventRepository`
- `getSettings`

**`MessageRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/chat/data/message/MessageRepository.kt`) — 19 functions:
- `fetchAndSave`
- `queryFromCache`
- `mapper`
- `observeFromCache`
- `createMessage`
- `syncMessage`
- `observeLatestMessage`
- `updateMessage`
- `deleteMessage`
- `flagMessage`
- `unflagMessage`
- `observeMessages`
- `loadFirstPageMessages`
- `loadMessages`
- `getMessagePagingData`
- `getLatestMessage`
- `isFlaggedByMe`
- `deleteFailedMessages`
- `findCacheAroundMessageId`

**`NotificationTraySeenRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/core/data/notificationtray/notificationtrayseen/NotificationTraySeenRepository.kt`) — 5 functions:
- `fetchAndSave`
- `queryFromCache`
- `mapper`
- `observeFromCache`
- `markTraySeen`

**`CommentRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/social/data/comment/CommentRepository.kt`) — 19 functions:
- `getComment`
- `getCommentByIds`
- `getLatestComments`
- `getLatestReplies`
- `observeComment`
- `createComment`
- `editComment`
- `deleteComment`
- `getCommentPagingData`
- `getLatestComment`
- `observeCommentAfter`
- `loadComments`
- `loadFirstPageComments`
- `markDeletedAfterCommentId`
- `markDeletedBeforeCommentId`
- `getCommentCollection`
- `flagComment`
- `unflagComment`
- `isFlaggedByMe`

**`AmityStoryRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/api/social/story/AmityStoryRepository.kt`) — 11 functions:
- `createImageStory`
- `createVideoStory`
- `getStoryTarget`
- `getStoryTargets`
- `getGlobalStoryTargets`
- `getActiveStories`
- `getStoriesByTargets`
- `getStory`
- `softDeleteStory`
- `hardDeleteStory`
- `analytics`

**`ProductCatalogueSettingRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/core/data/settings/network/product/ProductCatalogueSettingRepository.kt`) — 1 functions:
- `getProductCatalogueSetting`

**`TopicRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/core/data/topic/TopicRepository.kt`) — 2 functions:
- `subscribe`
- `unsubscribe`

**`PostRepositoryHelper`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/social/data/post/PostRepositoryHelper.kt`) — 1 functions:
- `convertPostTypesToString`

**`AmityHttpClient`** (`amity-sdk/src/main/java/com/ekoapp/ekosdk/internal/api/AmityHttpClient.kt`) — 5 functions:
- `onSessionStateChange`
- `establish`
- `destroy`
- `handleTokenExpire`
- `notification`

**`AmityStreamPlayerClient`** (`amity-video-player/src/main/java/com/amity/socialcloud/sdk/video/AmityStreamPlayerClient.kt`) — 1 functions:
- `setup`

**`FlagRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/core/data/flag/FlagRepository.kt`) — 6 functions:
- `isPostFlaggedByMe`
- `isCommentFlaggedByMe`
- `isUserFlaggedByMe`
- `isUserFlaggedByMeNow`
- `isMessageFlaggedByMe`
- `isMessageFlaggedByMeNow`

**`CommunityNotificationRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/core/data/notification/community/CommunityNotificationRepository.kt`) — 2 functions:
- `saveNotificationSettings`
- `getNotificationSettings`

**`AmityStreamRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/api/video/stream/AmityStreamRepository.kt`) — 6 functions:
- `getStreams`
- `fetchStream`
- `getStream`
- `createStream`
- `editStream`
- `disposeStream`

**`ChannelRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/chat/data/channel/ChannelRepository.kt`) — 16 functions:
- `fetchAndSave`
- `queryFromCache`
- `mapper`
- `observeFromCache`
- `getChannelPagingData`
- `createChannel`
- `createConversationChannel`
- `joinChannel`
- `leaveChannel`
- `updateChannel`
- `getLatestChannel`
- `getAllJoinedChannels`
- `getMessagePreviewId`
- `isChannelCacheExists`
- `bulkMarkRead`
- `setIsMutedChannel`

**`AmityLiveReactionRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/api/core/reaction/AmityLiveReactionRepository.kt`) — 3 functions:
- `getReactions`
- `createReaction`
- `createRoomReaction`

**`AmityChatClient`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/api/chat/AmityChatClient.kt`) — 5 functions:
- `newChannelRepository`
- `newSubChannelRepository`
- `newMessageRepository`
- `newChannelPresenceRepository`
- `getSettings`

**`AmityRoomPresenceRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/api/core/presence/AmityRoomPresenceRepository.kt`) — 6 functions:
- `startHeartbeat`
- `stopHeartbeat`
- `observeOnlineUsersCount`
- `getOnlineUsersCount`
- `getOnlineUsersSnapshot`
- `roomId`

**`AmityObjectRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/common/AmityObjectRepository.kt`) — 2 functions:
- `observe`
- `obtain`

**`AmityAdRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/api/core/ads/AmityAdRepository.kt`) — 2 functions:
- `getNetworkAds`
- `analytics`

**`AdRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/core/data/ad/AdRepository.kt`) — 2 functions:
- `getNetworkAds`
- `getAdvertiser`

**`TokenRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/core/data/auth/TokenRepository.kt`) — 1 functions:
- `createToken`

**`InvitationRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/core/data/invitation/InvitationRepository.kt`) — 11 functions:
- `getInvitationPagingData`
- `getMyCommunityInvitation`
- `createCommunityInvitations`
- `createCohostInvitation`
- `getMyCohostInvitation`
- `observeMyInvitation`
- `getInvitationById`
- `observeInvitations`
- `acceptInvitation`
- `rejectInvitation`
- `cancelInvitation`

**`DeviceNotificationRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/core/data/notification/device/DeviceNotificationRepository.kt`) — 2 functions:
- `register`
- `unregisterAll`

**`PollRepositoryHelper`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/social/data/poll/PollRepositoryHelper.kt`) — 1 functions:
- `convertAnswersToJsonArray`

**`StreamRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/video/data/stream/StreamRepository.kt`) — 11 functions:
- `getStreamCollectionPagingData`
- `observeStream`
- `getStreamByIds`
- `fetchStream`
- `createStream`
- `editStream`
- `createStreamBroadcaster`
- `disposeVideoStreaming`
- `getLatestSteam`
- `getStreamModeration`
- `setStreamIsBanned`

**`StreamPlayerClient`** (`amity-video-player/src/main/java/com/amity/socialcloud/sdk/video/StreamPlayerClient.kt`) — 2 functions:
- `setup`
- `getFunction`

**`FileRepository`** (`amity-rxupload/src/main/java/co/amity/rxupload/internal/repository/FileRepository.kt`) — 18 functions:
- `upload`
- `getRawFile`
- `createLocalFile`
- `getImage`
- `getImageNow`
- `getFile`
- `getAudio`
- `getVideo`
- `getClip`
- `uploadImage`
- `uploadFile`
- `uploadAudio`
- `uploadVideo`
- `uploadClip`
- `cancelUpload`
- `getUploadInfo`
- `deleteFile`
- `updateFile`

**`AmityProductRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/api/core/product/AmityProductRepository.kt`) — 2 functions:
- `searchProduct`
- `getProduct`

**`ChannelReaderRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/chat/data/channel/reader/ChannelReaderRepository.kt`) — 2 functions:
- `hasUnreadMention`
- `updateLastMentionedSegment`

**`UserRelationshipRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/core/data/relationship/UserRelationshipRepository.kt`) — 1 functions:
- `hasInLocal`

**`StreamBroadcasterClient`** (`amity-video-publisher/src/main/java/com/amity/socialcloud/sdk/video/StreamBroadcasterClient.kt`) — 2 functions:
- `setup`
- `getFunction`

**`AmityInvitationRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/api/core/invitation/AmityInvitationRepository.kt`) — 2 functions:
- `getMyCommunityInvitations`
- `getInvitations`

**`AmityFeedRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/api/social/post/AmityFeedRepository.kt`) — 5 functions:
- `getGlobalFeed`
- `getCustomRankingGlobalFeed`
- `getCommunityFeed`
- `getUserFeed`
- `getMyFeed`

**`SubChannelMarkerRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/chat/data/marker/subchannel/SubChannelMarkerRepository.kt`) — 13 functions:
- `fetchSubChannelMarker`
- `getSubChannelMarker`
- `updateReadToSegment`
- `getUserSubChannelMarker`
- `startSubChannelReading`
- `readSubChannels`
- `stopSubChannelReading`
- `fetchSubChannelUnreadInfo`
- `getSubChannelUnreadInfo`
- `saveSubChannelUnreadInfo`
- `deleteUnreadInfoBySubChannelId`
- `deleteUnreadInfoByChannelId`
- `deleteUnreadInfoCacheByChannelId`

**`MarkerSyncRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/chat/data/marker/sync/MarkerSyncRepository.kt`) — 1 functions:
- `syncMarkers`

**`WatchSessionRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/video/data/watch/WatchSessionRepository.kt`) — 8 functions:
- `getWatchSessionCollection`
- `getById`
- `resetSyncState`
- `createWatchSession`
- `updateWatchSession`
- `markAsSyncing`
- `markAsSynced`
- `markAsFailed`

**`StreamBroadcasterRepository`** (`amity-video-publisher/src/main/java/com/amity/socialcloud/sdk/video/StreamBroadcasterRepository.kt`) — 3 functions:
- `createVideoStreaming`
- `getVideoStreaming`
- `disposeVideoStreaming`

**`AmitySubChannelRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/api/chat/subchannel/AmitySubChannelRepository.kt`) — 8 functions:
- `getSubChannel`
- `getSubChannels`
- `createSubChannel`
- `editSubChannel`
- `softDeleteSubChannel`
- `hardDeleteSubChannel`
- `startMessageReceiptSync`
- `stopMessageReceiptSync`

**`AmityCommunityRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/api/social/community/AmityCommunityRepository.kt`) — 16 functions:
- `createCommunity`
- `getCommunities`
- `getJoinRequestList`
- `searchCommunities`
- `semanticSearchCommunities`
- `getRecommendedCommunities`
- `getTrendingCommunities`
- `membership`
- `getCommunity`
- `getCategory`
- `getCategories`
- `deleteCommunity`
- `editCommunity`
- `joinCommunity`
- `leaveCommunity`
- `moderation`

**`AmityVideoClient`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/api/video/AmityVideoClient.kt`) — 2 functions:
- `newStreamRepository`
- `newRoomRepository`

**`UserMarkerRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/chat/data/marker/user/UserMarkerRepository.kt`) — 1 functions:
- `getUserMarker`

**`SubChannelRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/chat/data/subchannel/SubChannelRepository.kt`) — 9 functions:
- `fetchAndSave`
- `queryFromCache`
- `mapper`
- `observeFromCache`
- `createSubChannel`
- `updateSubChannel`
- `deleteSubChannel`
- `getSubChannelPagingData`
- `getLatestSubChannel`

**`FollowRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/core/data/follow/FollowRepository.kt`) — 18 functions:
- `fetchAndSave`
- `queryFromCache`
- `mapper`
- `observeFromCache`
- `getUserFollowInfo`
- `requestFollow`
- `acceptFollow`
- `declineFollow`
- `removeFollower`
- `unfollow`
- `getFollowingsPagingData`
- `getFollowersPagingData`
- `getLatestFollowing`
- `getLatestFollower`
- `blockUser`
- `unblockUser`
- `getBlockedUsersPagingData`
- `getAllBlockedUsers`

**`PermissionRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/core/data/permission/PermissionRepository.kt`) — 3 functions:
- `getGlobalPermission`
- `getChannelPermission`
- `getCommunityPermission`

**`CommunityMembershipRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/social/data/community/membership/CommunityMembershipRepository.kt`) — 10 functions:
- `addUsers`
- `removeUsers`
- `addRoles`
- `removeRoles`
- `banUsers`
- `unbanUsers`
- `getMembership`
- `searchCommunityMembershipPagingData`
- `getCommunityMembershipPagingData`
- `getLatestCommunityMember`

**`AmityChannelRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/api/chat/channel/AmityChannelRepository.kt`) — 12 functions:
- `createChannel`
- `getChannels`
- `getChannel`
- `joinChannel`
- `leaveChannel`
- `editChannel`
- `membership`
- `moderation`
- `muteChannel`
- `unmuteChannel`
- `getTotalChannelsUnreadInfo`
- `getTotalChannelUnread`

**`NetworkSettingsRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/core/data/settings/network/NetworkSettingsRepository.kt`) — 6 functions:
- `getChatSettings`
- `getSocialSettings`
- `getUserSettings`
- `validateUrls`
- `validateTexts`
- `getLinkPreviewMetadata`

**`AmityEventResponseRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/social/data/event/AmityEventResponseRepository.kt`) — 6 functions:
- `fetchAndSave`
- `queryFromCache`
- `mapper`
- `observeFromCache`
- `getEventResponsePagingData`
- `getLatestEventResponse`

**`AmityMessageRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/api/chat/message/AmityMessageRepository.kt`) — 14 functions:
- `getMessages`
- `getMessage`
- `createTextMessage`
- `createImageMessage`
- `createFileMessage`
- `createVideoMessage`
- `createAudioMessage`
- `createCustomMessage`
- `editTextMessage`
- `editCustomMessage`
- `softDeleteMessage`
- `flagMessage`
- `unflagMessage`
- `deleteFailedMessages`

**`UserRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/core/data/user/UserRepository.kt`) — 15 functions:
- `fetchAndSave`
- `queryFromCache`
- `mapper`
- `observeFromCache`
- `getUserPagingData`
- `getUser`
- `getUserNow`
- `getUserByIds`
- `getUserByIdsNow`
- `updateUser`
- `hasInLocal`
- `flagUser`
- `unflagUser`
- `isFlaggedByMe`
- `getUserDtoByIds`

**`AmityMqttClient`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/infra/mqtt/AmityMqttClient.kt`) — 7 functions:
- `onSessionStateChange`
- `establish`
- `destroy`
- `handleTokenExpire`
- `disconnect`
- `subscribe`
- `unsubscribe`

**`CommunityRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/social/data/community/CommunityRepository.kt`) — 27 functions:
- `fetchAndSave`
- `queryFromCache`
- `mapper`
- `observeFromCache`
- `getCommunityPagingData`
- `searchCommunityPagingData`
- `getRecommendedCommunities`
- `getTrendingCommunities`
- `createCommunity`
- `updateCommunity`
- `getCommunityById`
- `joinCommunity`
- `getJoinRequestPagingData`
- `getJoinRequestList`
- `getMyJoinRequest`
- `joinRequest`
- `approveJoinRequest`
- `rejectJoinRequest`
- `cancelJoinRequest`
- `getJoinRequestByTargetId`
- `leaveCommunity`
- `deleteCommunity`
- `getLatestCommunity`
- `searchCommunities`
- `getPostCount`
- `fetchCommunityByIds`
- `getCommunityByIds`

**`EventRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/social/data/event/EventRepository.kt`) — 10 functions:
- `fetchAndSave`
- `queryFromCache`
- `mapper`
- `observeFromCache`
- `getEvent`
- `getEventPagingData`
- `createEvent`
- `updateEvent`
- `deleteEvent`
- `getLatestEvent`

**`StoryTargetRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/social/data/storytarget/StoryTargetRepository.kt`) — 12 functions:
- `fetchAndSave`
- `queryFromCache`
- `mapper`
- `observeFromCache`
- `getStoryTarget`
- `getStoryTargets`
- `updateStoryTargetLocalLastStoryExpiresAt`
- `updateStoryTargetLastStoryExpiresAt`
- `updateStoryTargetLocalLastStorySeenExpiresAt`
- `updateStoryTargetHasUnseen`
- `getGlobalFeed`
- `getLatestStoryTargets`

**`StreamSessionRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/video/data/session/StreamSessionRepository.kt`) — 8 functions:
- `getStreamSessionCollection`
- `getById`
- `resetSyncState`
- `createStreamSession`
- `updateStreamSession`
- `markAsSyncing`
- `markAsSynced`
- `markAsFailed`

**`UserRepositoryHelper`** (`amity-sdk/src/main/java/com/ekoapp/ekosdk/internal/repository/user/helper/UserRepositoryHelper.kt`) — 2 functions:
- `attachDataAndMapToExternal`
- `attachUserFollowInfoDataAndMapToExternal`

**`AmityChannelPresenceRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/api/chat/presence/AmityChannelPresenceRepository.kt`) — 4 functions:
- `syncChannelPresence`
- `unsyncChannelPresence`
- `unsyncAllChannelPresence`
- `getSyncingChannelPresence`

**`AmityFileRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/api/core/file/AmityFileRepository.kt`) — 10 functions:
- `uploadFile`
- `uploadImage`
- `uploadAudio`
- `uploadVideo`
- `uploadClip`
- `cancelUpload`
- `getUploadInfo`
- `deleteFile`
- `getFile`
- `updateAltText`

**`AmityUserRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/api/core/user/AmityUserRepository.kt`) — 10 functions:
- `getUsers`
- `searchUsers`
- `getUser`
- `getUserByIds`
- `flagUser`
- `unflagUser`
- `getBlockedUsers`
- `getAllBlockedUsers`
- `relationship`
- `getReachedUsers`

**`AmityCommentRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/api/social/comment/AmityCommentRepository.kt`) — 10 functions:
- `getComment`
- `getCommentByIds`
- `getComments`
- `createComment`
- `editComment`
- `softDeleteComment`
- `hardDeleteComment`
- `getLatestComment`
- `flagComment`
- `unflagComment`

**`MessagePreviewRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/chat/data/message/preview/MessagePreviewRepository.kt`) — 9 functions:
- `getMessagePreview`
- `getMessagePreviewByChannelId`
- `getMessagePreviewBySubChannelId`
- `saveMessagePreviews`
- `saveMessagePreview`
- `deleteMessagePreview`
- `updateSubChannelInfo`
- `clearDeletedMessagePreviews`
- `clearAllMessagePreviews`

**`CategoryRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/social/data/category/CategoryRepository.kt`) — 7 functions:
- `fetchAndSave`
- `queryFromCache`
- `mapper`
- `observeFromCache`
- `getCategories`
- `getAllCategoriesPagingData`
- `getLatestCategory`

**`AmityCoreClient`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/api/core/AmityCoreClient.kt`) — 48 functions:
- `getCurrentSessionState`
- `setup`
- `registerPushNotification`
- `unregisterPushNotification`
- `disconnect`
- `login`
- `loginAsVisitor`
- `loginWithAccessToken`
- `setAccessTokenHandler`
- `getLoginMethod`
- `logout`
- `secureLogout`
- `getUserId`
- `editUser`
- `hasPermission`
- `getCurrentUser`
- `newUserRepository`
- `newAdRepository`
- `newFileRepository`
- `newReactionRepository`
- `newLiveReactionRepository`
- `newInvitationRepository`
- `newProductRepository`
- `getAmityCoreSdkVersion`
- `getGlobalBanEvents`
- `notifications`
- `notificationTray`
- `getShareableLinkConfiguration`
- `getConfiguration`
- `subscription`
- `getContentCheck`
- `observeSessionState`
- `observeUserUnread`
- `presence`
- `newUserPresenceRepository`
- `newRoomPresenceRepository`
- `enableUnreadCount`
- `validateUrls`
- `validateTexts`
- `setUploadedFileAccessType`
- `getUploadedFileAccessType`
- `getAccessToken`
- `observeNetworkActivities`
- `getCoreUserSettings`
- `getVisitorDeviceId`
- `getCurrentUserType`
- `getLinkPreviewMetadata`
- `getProductCatalogueSetting`

**`AmityReactionRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/api/core/reaction/AmityReactionRepository.kt`) — 3 functions:
- `getReactions`
- `addReaction`
- `removeReaction`

**`ProductRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/core/data/product/ProductRepository.kt`) — 6 functions:
- `getProductSearchPagingData`
- `fetchAndSave`
- `queryFromCache`
- `mapper`
- `observeFromCache`
- `getProducts`

**`RoomRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/core/data/room/RoomRepository.kt`) — 19 functions:
- `getRoomCollectionPagingData`
- `observeRoom`
- `getRoomsByIds`
- `fetchRoom`
- `createRoom`
- `updateRoom`
- `deleteRoom`
- `leaveRoom`
- `stopRoom`
- `removeParticipant`
- `getRecordedUrls`
- `getBroadcasterData`
- `getLatestRoom`
- `getRoomModerationByRoom`
- `updateCohostPermissions`
- `fetchAndSave`
- `queryFromCache`
- `mapper`
- `observeFromCache`

**`AmityStreamBroadcasterClient`** (`amity-video-publisher/src/main/java/com/amity/socialcloud/sdk/video/AmityStreamBroadcasterClient.kt`) — 1 functions:
- `setup`

### IOS (207 functions)

**`AmityPostRepository`** (`EkoChat/Features/Feed/Public/Repository/Post/AmityPostRepository.swift`) — 31 functions:
- `createTextPost`
- `createCustomPost`
- `createImagePost`
- `createFilePost`
- `createVideoPost`
- `createPollPost`
- `createRoomPost`
- `createLiveStreamPost`
- `createAudioPost`
- `createMixedMediaPost`
- `createClipPost`
- `editPost`
- `softDeletePost`
- `hardDeletePost`
- `approvePost`
- `declinePost`
- `getPost`
- `getPosts`
- `getLiveRoomPosts`
- `getCommunityLiveRoomPosts`
- `getReactions`
- `flagPost`
- `unflagPost`
- `isFlaggedByMe`
- `getPinnedPosts`
- `getGlobalPinnedPosts`
- `semanticSearchPosts`
- `searchPostsByHashtag`
- `pinProduct`
- `unpinProduct`
- `updateProductTags`

**`AmityFileRepository`** (`EkoChat/Features/File/Public/AmityFileRepository.swift`) — 15 functions:
- `uploadImage`
- `updateAltText`
- `uploadFile`
- `uploadVideo`
- `uploadAudio`
- `downloadImageAsData`
- `downloadImage`
- `downloadFileAsData`
- `downloadFile`
- `deleteFile`
- `getFile`
- `getUploadProgress`
- `cancelFileDownload`
- `cancelImageDownload`
- `uploadClip`

**`AmityStreamRepository`** (`EkoChat/Features/LiveStream/Public/Repositories/AmityStreamRepository.swift`) — 5 functions:
- `createStream`
- `disposeStream`
- `getStream`
- `getStreams`
- `editStream`

**`AmitySubChannelRepository`** (`EkoChat/Features/SubChannel/AmitySubChannelRepository.swift`) — 11 functions:
- `createSubChannel`
- `editSubChannel`
- `softDeleteSubChannel`
- `hardDeleteSubChannel`
- `getSubChannel`
- `getSubChannels`
- `startMessageReceiptSync`
- `stopMessageReceiptSync`
- `channelId`
- `isDeleted`
- `excludeDefaultSubChannel`

**`AmityRoomRepository`** (`EkoChat/Features/CoHostStream/Public/AmityRoomRepository.swift`) — 11 functions:
- `createRoom`
- `getRoom`
- `updateRoom`
- `getRooms`
- `deleteRoom`
- `stopRoom`
- `leaveRoom`
- `removeParticipant`
- `generateRoomToken`
- `getCoHostEvent`
- `updateCohostPermissions`

**`AmityFeedRepository`** (`EkoChat/Features/Feed/Public/Repository/Feed/AmityFeedRepository.swift`) — 5 functions:
- `getMyFeed`
- `getUserFeed`
- `getGlobalFeed`
- `getCustomRankingGlobalFeed`
- `getCommunityFeed`

**`AmityInvitationRepository`** (`EkoChat/Features/Invitation/Public/Repository/AmityInvitationRepository.swift`) — 2 functions:
- `getMyCommunityInvitations`
- `getInvitations`

**`AmityProductRepository`** (`EkoChat/Features/Product/Public/AmityProductRepository.swift`) — 2 functions:
- `getProduct`
- `searchProducts`

**`AmityUserRepository`** (`EkoChat/Features/User/Public/AmityUserRepository.swift`) — 9 functions:
- `getUser`
- `searchUsers`
- `getUsers`
- `getBlockedUsers`
- `getAllBlockedUsers`
- `flagUser`
- `unflagUser`
- `isUserFlaggedByMe`
- `getReachedUsers`

**`AmityClient`** (`EkoChat/Core/Client/AmityClient.swift`) — 31 functions:
- `notificationTray`
- `currentUserId`
- `loginMethod`
- `accessToken`
- `presence`
- `getUserUnread`
- `user`
- `currentUserType`
- `notificationManager`
- `mentionConfigurations`
- `setup`
- `enableUnreadCount`
- `login`
- `getVisitorDeviceId`
- `loginAsVisitor`
- `loginWithAccessToken`
- `setAccessTokenHandler`
- `disconnect`
- `logout`
- `secureLogout`
- `registerPushNotification`
- `unregisterPushNotification`
- `editUser`
- `validateUrls`
- `validateTexts`
- `setUploadedFileAccessType`
- `sendCustomCommandRequest`
- `getShareableLinkConfiguration`
- `sendCustomCommand`
- `observeNetworkActivities`
- `getLinkPreviewMetadata`

**`AmityUserPresenceRepository`** (`EkoChat/Core/Presence/Public/AmityUserPresenceRepository.swift`) — 8 functions:
- `defaultViewId`
- `getOnlineUsersCount`
- `getOnlineUsersSnapshot`
- `getUserPresence`
- `syncUserPresence`
- `unsyncUserPresence`
- `unsyncAllUserPresence`
- `getSyncingUserPresence`

**`AmityAdRepository`** (`EkoChat/Features/Ads/Public/AmityAdRepository.swift`) — 1 functions:
- `getNetworkAds`

**`AmityRoomPresenceRepository`** (`EkoChat/Features/CoHostStream/Presence/AmityRoomPresenceRepository.swift`) — 4 functions:
- `startHeartbeat`
- `stopHeartbeat`
- `getRoomOnlineUsers`
- `getRoomUserCount`

**`AmityReactionRepository`** (`EkoChat/Features/Reaction/Public/AmityReactionRepository.swift`) — 4 functions:
- `createReaction`
- `getReactions`
- `addReaction`
- `removeReaction`

**`AmityStoryRepository`** (`EkoChat/Features/Story/Public/AmityStoryRepository.swift`) — 10 functions:
- `createVideoStory`
- `createImageStory`
- `getActiveStoriesByTarget`
- `getStoriesByTargets`
- `getStoryTarget`
- `softDeleteStory`
- `hardDeleteStory`
- `getStory`
- `getStoryTargets`
- `getGlobalStoryTargets`

**`AmityChannelRepository`** (`EkoChat/Features/Channel/Public/AmityChannelRepository.swift`) — 10 functions:
- `getTotalChannelsUnread`
- `notificationManagerForChannel`
- `getChannel`
- `getChannels`
- `joinChannel`
- `createChannel`
- `editChannel`
- `leaveChannel`
- `muteChannel`
- `unmuteChannel`

**`AmityPollRepository`** (`EkoChat/Features/Feed/Public/Repository/Poll/AmityPollRepository.swift`) — 5 functions:
- `createPoll`
- `closePoll`
- `votePoll`
- `unvotePoll`
- `deletePoll`

**`AmityMessageRepository`** (`EkoChat/Features/Message/Public/AmityMessageRepository.swift`) — 17 functions:
- `softDeleteMessage`
- `deleteFailedMessages`
- `createCustomMessage`
- `createTextMessage`
- `createImageMessage`
- `createAudioMessage`
- `createFileMessage`
- `createVideoMessage`
- `getMessage`
- `getMessages`
- `getReactions`
- `editTextMessage`
- `editCustomMessage`
- `setTags`
- `flagMessage`
- `unflagMessage`
- `isMessageFlaggedByMe`

**`AmityChannelPresenceRepository`** (`EkoChat/Core/Presence/Public/AmityChannelPresenceRepository.swift`) — 5 functions:
- `defaultViewId`
- `syncChannelPresence`
- `unsyncChannelPresence`
- `unsyncAllChannelPresence`
- `getSyncingChannelPresence`

**`AmityCommentRepository`** (`EkoChat/Features/Comment/Public/AmityCommentRepository.swift`) — 11 functions:
- `softDeleteComment`
- `hardDeleteComment`
- `createComment`
- `editComment`
- `getLatestComment`
- `getComments`
- `getComment`
- `getReactions`
- `flagComment`
- `unflagComment`
- `isCommentFlaggedByMe`

**`AmityCommunityRepository`** (`EkoChat/Features/Community/Public/Repository/AmityCommunityRepository.swift`) — 5 functions:
- `createCommunity`
- `editCommunity`
- `deleteCommunity`
- `joinCommunity`
- `leaveCommunity`

**`AmityEventRepository`** (`EkoChat/Features/Event/Public/AmityEventRepository.swift`) — 5 functions:
- `createEvent`
- `updateEvent`
- `deleteEvent`
- `getEvent`
- `getEvents`

### FLUTTER (243 functions)

**`stream_repository`** (`lib/src/public/repo/stream/stream_repository.dart`) — 3 functions:
- `getStreams`
- `getStream`
- `serviceLocator`

**`amity_user_flag_repository`** (`lib/src/public/repo/sub_set/amity_user_flag_repository.dart`) — 3 functions:
- `flag`
- `serviceLocator`
- `unflag`

**`comment_repository`** (`lib/src/public/repo/comment_repository.dart`) — 6 functions:
- `createComment`
- `updateComment`
- `getComments`
- `getReaction`
- `getComment`
- `serviceLocator`

**`feed_repository`** (`lib/src/public/repo/feed_repository.dart`) — 4 functions:
- `getGlobalFeed`
- `getCustomRankingGlobalFeed`
- `getUserFeed`
- `getCommunityFeed`

**`amity_story_repository`** (`lib/src/public/repo/amity_story_repository.dart`) — 9 functions:
- `createImageStory`
- `createVideoStory`
- `getActiveStories`
- `getStoriesByTargets`
- `hardDeleteStory`
- `serviceLocator`
- `softDeleteStory`
- `getStoryTargets`
- `analytics`

**`amity_object_repository`** (`lib/src/domain/repo/amity_object_repository.dart`) — 8 functions:
- `isChildObjectType`
- `fetchAndSave`
- `queryFromCache`
- `mapper`
- `observeFromCache`
- `observe`
- `getEntity`
- `obtain`

**`amity_chat_client`** (`lib/src/public/client/amity_chat_client.dart`) — 4 functions:
- `newMessageRepository`
- `serviceLocator`
- `newChannelRepository`
- `newSubChannelRepository`

**`amity_social_client`** (`lib/src/public/client/amity_social_client.dart`) — 7 functions:
- `newPostRepository`
- `newCommentRepository`
- `newFeedRepository`
- `newCommunityRepository`
- `newPollRepository`
- `newStoryRepository`
- `newReactionRepository`

**`amity_file_repository`** (`lib/src/public/repo/amity_file_repository.dart`) — 6 functions:
- `uploadFile`
- `serviceLocator`
- `uploadImage`
- `uploadAudio`
- `uploadVideo`
- `cancelUpload`

**`amity_post_repository`** (`lib/src/public/repo/amity_post_repository.dart`) — 11 functions:
- `getPost`
- `serviceLocator`
- `getPosts`
- `getPostStream`
- `createPost`
- `deletePost`
- `reviewPost`
- `getReaction`
- `isFlaggedByMe`
- `getPinnedPosts`
- `getGlobalPinnedPosts`

**`channel_moderation_repository`** (`lib/src/public/repo/channel/channel_moderation_repository.dart`) — 8 functions:
- `channelId`
- `addRole`
- `serviceLocator`
- `removeRole`
- `muteMembers`
- `unmuteMembers`
- `banMembers`
- `unbanMembers`

**`sub_channel_repository`** (`lib/src/public/repo/sub_channel_repository.dart`) — 6 functions:
- `createSubChannel`
- `getSubChannels`
- `getSubChannel`
- `softDeleteSubChannel`
- `hardDeleteSubChannel`
- `updateeditSubChannelSubChannel`

**`amity_ad_repository`** (`lib/src/public/repo/ads/amity_ad_repository.dart`) — 3 functions:
- `getNetworkAds`
- `serviceLocator`
- `analytics`

**`amity_community_repository`** (`lib/src/public/repo/amity_community_repository.dart`) — 16 functions:
- `createCommunity`
- `updateCommunity`
- `getCommunities`
- `getCategories`
- `getCategory`
- `serviceLocator`
- `getCommunity`
- `deleteCommunity`
- `joinCommunity`
- `leaveCommunity`
- `getTrendingCommunities`
- `getRecommendedCommunities`
- `membership`
- `moderation`
- `getCurentUserRoles`
- `getCurrentUserRoles`

**`abs_db_client`** (`lib/src/data/data_source/local/db_client/abs_db_client.dart`) — 2 functions:
- `init`
- `reset`

**`amity_core_client_mock_setup`** (`test/helper/amity_core_client_mock_setup.dart`) — 2 functions:
- `setup`
- `loadMockSession`

**`collection_repository`** (`lib/src/domain/repo/collection_repository.dart`) — 2 functions:
- `listenEntities`
- `getEntities`

**`message_repository`** (`lib/src/public/repo/message/message_repository.dart`) — 16 functions:
- `getMessages`
- `newGetMessages`
- `newCreateMessage`
- `getMessage`
- `serviceLocator`
- `createMessage`
- `updateMessage`
- `editTextMessage`
- `deleteMessage`
- `getReaction`
- `flag`
- `flagMessage`
- `unflag`
- `createCustomMessage`
- `editCustomMessage`
- `searchMessage`

**`poll_repository`** (`lib/src/public/repo/poll_repository.dart`) — 5 functions:
- `createPoll`
- `deletePoll`
- `serviceLocator`
- `vote`
- `closePoll`

**`amity_my_user_relationship_repository`** (`lib/src/public/repo/sub_set/follow/amity_my_user_relationship_repository.dart`) — 9 functions:
- `accept`
- `serviceLocator`
- `decline`
- `removeFollower`
- `unfollow`
- `getFollowings`
- `getFollowers`
- `getFollowInfo`
- `getBlockedUsers`

**`user_repository`** (`lib/src/public/repo/user_repository.dart`) — 9 functions:
- `getUsers`
- `searchUserByDisplayName`
- `getUser`
- `serviceLocator`
- `updateUser`
- `report`
- `relationship`
- `getBlockedUsers`
- `getViewedUsers`

**`http_api_client`** (`lib/src/data/data_source/remote/client/http/http_api_client.dart`) — 4 functions:
- `call`
- `parseResponseData`
- `jsonDecode`
- `initDio`

**`amity_core_client`** (`lib/src/public/amity_core_client.dart`) — 22 functions:
- `setup`
- `login`
- `logout`
- `validateUrls`
- `validateTexts`
- `disconnect`
- `isUserLoggedIn`
- `getUserId`
- `getCurrentUser`
- `getConfiguration`
- `updateUser`
- `registerDeviceNotification`
- `unregisterDeviceNotification`
- `notifications`
- `hasPermission`
- `newUserRepository`
- `newAdRepository`
- `newFileRepository`
- `getAnalyticsEngine`
- `observeSessionState`
- `observeUnreadCount`
- `copyWith`

**`amity_video_client`** (`lib/src/public/client/amity_video_client.dart`) — 1 functions:
- `newStreamRepository`

**`amity_user_relationship_repository`** (`lib/src/public/repo/sub_set/follow/amity_user_relationship_repository.dart`) — 6 functions:
- `follow`
- `serviceLocator`
- `unfollow`
- `getFollowings`
- `getFollowers`
- `getFollowInfo`

**`amity_user_relationships_repository`** (`lib/src/public/repo/sub_set/follow/amity_user_relationships_repository.dart`) — 16 functions:
- `me`
- `user`
- `follow`
- `serviceLocator`
- `unfollow`
- `acceptMyFollower`
- `declineMyFollower`
- `removeMyFollower`
- `getMyFollowings`
- `getFollowings`
- `getMyFollowers`
- `getFollowers`
- `getMyFollowInfo`
- `getFollowInfo`
- `blockUser`
- `unblockUser`

**`core_client`** (`lib/src/core/core_client.dart`) — 26 functions:
- `setup`
- `setupSessionComponents`
- `resolve`
- `resolveAll`
- `login`
- `logout`
- `serviceLocator`
- `disconnect`
- `isUserLoggedIn`
- `getUserId`
- `getCurrentUser`
- `getConfiguration`
- `updateUser`
- `registerDeviceNotification`
- `unregisterDeviceNotification`
- `notifications`
- `hasPermission`
- `newUserRepository`
- `newFileRepository`
- `getAnalyticsEngine`
- `observeSessionState`
- `onAppEvent`
- `observeUnreadCount`
- `isLegacyLogin`
- `getServerTime`
- `markRead`

**`hive_client_impl`** (`lib/src/data/data_source/local/db_client_impl/hive_client_impl.dart`) — 2 functions:
- `init`
- `reset`

**`amity_reaction_repository`** (`lib/src/public/repo/amity_reaction_repository.dart`) — 3 functions:
- `getReactions`
- `addReaction`
- `removeReaction`

**`amity_channel_repository`** (`lib/src/public/repo/channel/amity_channel_repository.dart`) — 21 functions:
- `createChannel`
- `updateChannel`
- `getChannel`
- `serviceLocator`
- `getChannels`
- `joinChannel`
- `leaveChannel`
- `muteChannel`
- `unMuteChannel`
- `addMembers`
- `removeMembers`
- `membership`
- `moderation`
- `startReading`
- `stopReading`
- `archiveChannel`
- `unarchiveChannel`
- `getArchivedChannels`
- `getArchivedChannelIds`
- `searchChannels`
- `getChannelTotalUnreads`

**`notification_repository`** (`lib/src/public/repo/notification_repository.dart`) — 3 functions:
- `registerDeviceNotification`
- `serviceLocator`
- `unregisterDeviceNotification`

### TYPESCRIPT (44 functions)

**`setClientToken`** (`packages/sdk/src/client/utils/setClientToken.ts`) — 3 functions:
- `setSessionState`
- `ingestInCache`
- `prepareUserPayload`

**`disconnectClient`** (`packages/ui-tests/src/views/TestCase/cases/disconnectClient.ts`) — 1 functions:
- `append`

**`createClient`** (`packages/sdk/src/client/api/createClient.ts`) — 2 functions:
- `log`
- `setActiveClient`

**`terminateClient`** (`packages/sdk/src/client/api/terminateClient.ts`) — 2 functions:
- `setSessionState`
- `logout`

**`createClient.branches.integration.test`** (`packages/sdk/src/client/api/tests/integration/createClient.branches.integration.test.ts`) — 7 functions:
- `beforeAll`
- `afterAll`
- `beforeEach`
- `afterEach`
- `disableCache`
- `test`
- `expect`

**`createClient.integration.test`** (`packages/sdk/src/client/api/tests/integration/createClient.integration.test.ts`) — 7 functions:
- `beforeAll`
- `afterAll`
- `beforeEach`
- `afterEach`
- `disableCache`
- `test`
- `expect`

**`setVisitorClientToken`** (`packages/sdk/src/client/utils/setVisitorClientToken.ts`) — 3 functions:
- `setSessionState`
- `ingestInCache`
- `prepareUserPayload`

**`connectClient`** (`packages/ui-tests/src/views/TestCase/cases/connectClient.ts`) — 1 functions:
- `append`

**`client`** (`packages/sdk/src/@types/domains/client.ts`) — 4 functions:
- `sessionWillRenewAccessToken`
- `onTokenRenew`
- `sessionWillRenewAccessToken`
- `sdkDisconnectClient`

**`onClientDisconnected`** (`packages/code-snippets/src/client/events/onClientDisconnected.ts`) — 1 functions:
- `useEffect`

**`activeClient.test`** (`packages/sdk/src/client/api/tests/activeClient.test.ts`) — 4 functions:
- `afterAll`
- `test`
- `getActiveClient`
- `expect`

**`createClient.test`** (`packages/sdk/src/client/api/tests/createClient.test.ts`) — 2 functions:
- `test`
- `expect`

**`terminateClient.test`** (`packages/sdk/src/client/api/tests/terminateClient.test.ts`) — 4 functions:
- `beforeAll`
- `test`
- `terminateClient`
- `expect`

**`setBotClientToken`** (`packages/sdk/src/client/utils/setBotClientToken.ts`) — 3 functions:
- `setSessionState`
- `ingestInCache`
- `prepareUserPayload`

---

## After completion

```bash
cd social-plus-docs/harness
./harness-bin audit --config harness-config.yml
# If open findings remain: ./harness-bin prompt --config harness-config.yml
```
