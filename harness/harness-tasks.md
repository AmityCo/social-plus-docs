# SDK Harness — Agent Runbook

_Generated 2026-05-01 11:20 — 1 findings requiring AI_

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

## PUBLIC_FUNC_UNANNOTATED (325 functions need begin_public_function annotation)

These public functions in `*Repository` / `*Client` classes have no `begin_public_function` annotation.
Wrap each function with `/* begin_public_function\n  id: <feature.action>\n*/` and `/* end_public_function */`, or mark `@Deprecated` if no longer active.

### ANDROID (101 functions)

**`AmityClientFetchLinkPreview`** (`amity-sample-code/src/main/java/com/amity/snipet/verifier/core/gettingstarted/AmityClientFetchLinkPreview.kt`) — 1 functions:
- `fetchLinkPreview`

**`AmityClientLoginWithAccessToken`** (`amity-sample-code/src/main/java/com/amity/snipet/verifier/core/gettingstarted/AmityClientLoginWithAccessToken.kt`) — 2 functions:
- `loginWithAccessToken`
- `sessionWillRenewAccessToken`

**`AmityMessageRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/api/chat/message/AmityMessageRepository.kt`) — 6 functions:
- `createImageMessage`
- `createFileMessage`
- `createVideoMessage`
- `createAudioMessage`
- `flagMessage`
- `deleteFailedMessages`

**`AmityAdRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/api/core/ads/AmityAdRepository.kt`) — 2 functions:
- `getNetworkAds`
- `analytics`

**`AmityClientPresenceIsEnabled`** (`amity-sample-code/src/main/java/com/amity/snipet/verifier/core/presence/AmityClientPresenceIsEnabled.kt`) — 1 functions:
- `isPresenceEnabled`

**`AmityClientPresenceStartHeartbeat`** (`amity-sample-code/src/main/java/com/amity/snipet/verifier/core/presence/AmityClientPresenceStartHeartbeat.kt`) — 1 functions:
- `startHeartbeat`

**`AmityFileRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/api/core/file/AmityFileRepository.kt`) — 9 functions:
- `uploadFile`
- `uploadImage`
- `uploadAudio`
- `uploadVideo`
- `uploadClip`
- `cancelUpload`
- `getUploadInfo`
- `getFile`
- `updateAltText`

**`AmityUserRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/api/core/user/AmityUserRepository.kt`) — 1 functions:
- `relationship`

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

**`AmityStreamRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/api/video/stream/AmityStreamRepository.kt`) — 2 functions:
- `fetchStream`
- `editStream`

**`StreamBroadcasterClient`** (`amity-video-publisher/src/main/java/com/amity/socialcloud/sdk/video/StreamBroadcasterClient.kt`) — 2 functions:
- `setup`
- `getFunction`

**`FileRepository`** (`amity-rxupload/src/main/java/co/amity/rxupload/internal/repository/FileRepository.kt`) — 1 functions:
- `upload`

**`AmityClientGetLoginMethod`** (`amity-sample-code/src/main/java/com/amity/snipet/verifier/core/gettingstarted/AmityClientGetLoginMethod.kt`) — 1 functions:
- `getLoginMethod`

**`AmityClientGetProductCatalogueSetting`** (`amity-sample-code/src/main/java/com/amity/snipet/verifier/core/gettingstarted/AmityClientGetProductCatalogueSetting.kt`) — 1 functions:
- `getProductCatalogueSetting`

**`AmityClientUnregisterPush`** (`amity-sample-code/src/main/java/com/amity/snipet/verifier/core/notification/registration/AmityClientUnregisterPush.kt`) — 1 functions:
- `unregisterPush`

**`AmityClientPresenceDisable`** (`amity-sample-code/src/main/java/com/amity/snipet/verifier/core/presence/AmityClientPresenceDisable.kt`) — 1 functions:
- `disablePresence`

**`AmityClientPresenceStopHeartbeat`** (`amity-sample-code/src/main/java/com/amity/snipet/verifier/core/presence/AmityClientPresenceStopHeartbeat.kt`) — 1 functions:
- `stopHeartbeat`

**`AmityInitStoryRepository`** (`amity-sample-code/src/main/java/com/amity/snipet/verifier/social/story/init/AmityInitStoryRepository.kt`) — 1 functions:
- `initStoryRepository`

**`UserRelationshipRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/core/data/relationship/UserRelationshipRepository.kt`) — 1 functions:
- `hasInLocal`

**`AmityClientReadSessionState`** (`amity-sample-code/src/main/java/com/amity/snipet/verifier/core/gettingstarted/AmityClientReadSessionState.kt`) — 1 functions:
- `readSessionState`

**`AmityClientRenewAccessToken`** (`amity-sample-code/src/main/java/com/amity/snipet/verifier/core/gettingstarted/AmityClientRenewAccessToken.kt`) — 2 functions:
- `setupRenewal`
- `sessionWillRenewAccessToken`

**`AmityClientRegisterPush`** (`amity-sample-code/src/main/java/com/amity/snipet/verifier/core/notification/registration/AmityClientRegisterPush.kt`) — 1 functions:
- `registerPush`

**`AmityClientUpdateUser`** (`amity-sample-code/src/main/java/com/amity/snipet/verifier/core/user/AmityClientUpdateUser.kt`) — 1 functions:
- `updateUser`

**`AmityCommentRepositoryInitialization`** (`amity-sample-code/src/main/java/com/amity/snipet/verifier/social/comment/AmityCommentRepositoryInitialization.kt`) — 1 functions:
- `initializeCommentRepository`

**`AmityPostRepositoryInitialization`** (`amity-sample-code/src/main/java/com/amity/snipet/verifier/social/post/AmityPostRepositoryInitialization.kt`) — 1 functions:
- `initializePostRepository`

**`AmityLiveReactionRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/api/core/reaction/AmityLiveReactionRepository.kt`) — 3 functions:
- `getReactions`
- `createReaction`
- `createRoomReaction`

**`MarkerSyncRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/chat/data/marker/sync/MarkerSyncRepository.kt`) — 1 functions:
- `syncMarkers`

**`AmityClientSecureLogout`** (`amity-sample-code/src/main/java/com/amity/snipet/verifier/core/gettingstarted/AmityClientSecureLogout.kt`) — 1 functions:
- `secureLogout`

**`AmityClientGetCurrentUser`** (`amity-sample-code/src/main/java/com/amity/snipet/verifier/core/user/AmityClientGetCurrentUser.kt`) — 1 functions:
- `getCurrentUser`

**`AmityPostRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/api/social/post/AmityPostRepository.kt`) — 4 functions:
- `createMixedAttachmentPost`
- `getPinnedPosts`
- `getGlobalPinnedPosts`
- `semanticSearchPosts`

**`AmityClientSetAccessTokenHandler`** (`amity-sample-code/src/main/java/com/amity/snipet/verifier/core/gettingstarted/AmityClientSetAccessTokenHandler.kt`) — 2 functions:
- `setAccessTokenHandler`
- `sessionWillRenewAccessToken`

**`AmityClientPresenceEnable`** (`amity-sample-code/src/main/java/com/amity/snipet/verifier/core/presence/AmityClientPresenceEnable.kt`) — 1 functions:
- `enablePresence`

**`AmityCommunityRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/api/social/community/AmityCommunityRepository.kt`) — 2 functions:
- `membership`
- `moderation`

**`CommunityNotificationRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/core/data/notification/community/CommunityNotificationRepository.kt`) — 2 functions:
- `saveNotificationSettings`
- `getNotificationSettings`

**`TombstoneRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/core/data/tombstone/TombstoneRepository.kt`) — 2 functions:
- `getTombstone`
- `saveTombstone`

**`AmityClientObserveSessionState`** (`amity-sample-code/src/main/java/com/amity/snipet/verifier/core/gettingstarted/AmityClientObserveSessionState.kt`) — 1 functions:
- `observeSessionState`

**`AmityRoomPresenceRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/api/core/presence/AmityRoomPresenceRepository.kt`) — 6 functions:
- `startHeartbeat`
- `stopHeartbeat`
- `observeOnlineUsersCount`
- `getOnlineUsersCount`
- `getOnlineUsersSnapshot`
- `roomId`

**`AmityRoomRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/api/video/room/AmityRoomRepository.kt`) — 6 functions:
- `fetchRoom`
- `getRecordedUrls`
- `leaveRoom`
- `removeRoomParticipant`
- `getCoHostEvent`
- `updateCohostPermission`

**`UserMarkerRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/chat/data/marker/user/UserMarkerRepository.kt`) — 1 functions:
- `getUserMarker`

**`AnalyticsRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/core/data/analytics/AnalyticsRepository.kt`) — 5 functions:
- `saveAnalyticEvent`
- `sendAnalyticsEvents`
- `deleteAllAnalyticsEvents`
- `getViewedUsers`
- `createAnalyticEvent`

**`AmityFeedRepositoryInitialization`** (`amity-sample-code/src/main/java/com/amity/snipet/verifier/social/feed/AmityFeedRepositoryInitialization.kt`) — 1 functions:
- `initializeFeedRepository`

**`AmityChannelRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/api/chat/channel/AmityChannelRepository.kt`) — 5 functions:
- `membership`
- `moderation`
- `getChannels`
- `getTotalChannelsUnreadInfo`
- `getTotalChannelUnread`

**`AmityInvitationRepository`** (`amity-sdk/src/main/java/com/amity/socialcloud/sdk/api/core/invitation/AmityInvitationRepository.kt`) — 2 functions:
- `getMyCommunityInvitations`
- `getInvitations`

**`StreamPlayerClient`** (`amity-video-player/src/main/java/com/amity/socialcloud/sdk/video/StreamPlayerClient.kt`) — 2 functions:
- `setup`
- `getFunction`

### IOS (63 functions)

**`AmityCommentRepository`** (`EkoChat/Features/Comment/Public/AmityCommentRepository.swift`) — 1 functions:
- `getReactions`

**`AmityFeedRepository`** (`EkoChat/Features/Feed/Public/Repository/Feed/AmityFeedRepository.swift`) — 1 functions:
- `getMyFeed`

**`AmityFileRepository`** (`EkoChat/Features/File/Public/AmityFileRepository.swift`) — 11 functions:
- `uploadImage`
- `uploadFile`
- `uploadVideo`
- `uploadAudio`
- `downloadImageAsData`
- `downloadImage`
- `downloadFileAsData`
- `downloadFile`
- `getUploadProgress`
- `cancelFileDownload`
- `cancelImageDownload`

**`AmityRoomRepository`** (`EkoChat/Features/CoHostStream/Public/AmityRoomRepository.swift`) — 1 functions:
- `generateRoomToken`

**`AmityPostRepository`** (`EkoChat/Features/Feed/Public/Repository/Post/AmityPostRepository.swift`) — 3 functions:
- `editPost`
- `getPosts`
- `getReactions`

**`AmityMessageRepository`** (`EkoChat/Features/Message/Public/AmityMessageRepository.swift`) — 3 functions:
- `deleteFailedMessages`
- `getReactions`
- `setTags`

**`AmityReactionRepository`** (`EkoChat/Features/Reaction/Public/AmityReactionRepository.swift`) — 2 functions:
- `createReaction`
- `getReactions`

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

**`AmitySubChannelRepository`** (`EkoChat/Features/SubChannel/AmitySubChannelRepository.swift`) — 5 functions:
- `startMessageReceiptSync`
- `stopMessageReceiptSync`
- `channelId`
- `isDeleted`
- `excludeDefaultSubChannel`

**`AmityClient`** (`EkoChat/Core/Client/AmityClient.swift`) — 19 functions:
- `notificationTray`
- `currentUserId`
- `loginMethod`
- `accessToken`
- `presence`
- `getUserUnread`
- `mentionConfigurations`
- `setup`
- `enableUnreadCount`
- `getVisitorDeviceId`
- `secureLogout`
- `validateUrls`
- `validateTexts`
- `setUploadedFileAccessType`
- `sendCustomCommandRequest`
- `getShareableLinkConfiguration`
- `sendCustomCommand`
- `observeNetworkActivities`
- `getLinkPreviewMetadata`

**`AmityChannelPresenceRepository`** (`EkoChat/Core/Presence/Public/AmityChannelPresenceRepository.swift`) — 1 functions:
- `defaultViewId`

**`AmityUserPresenceRepository`** (`EkoChat/Core/Presence/Public/AmityUserPresenceRepository.swift`) — 1 functions:
- `defaultViewId`

**`AmityChannelRepository`** (`EkoChat/Features/Channel/Public/AmityChannelRepository.swift`) — 1 functions:
- `getTotalChannelsUnread`

**`AmityRoomPresenceRepository`** (`EkoChat/Features/CoHostStream/Presence/AmityRoomPresenceRepository.swift`) — 4 functions:
- `startHeartbeat`
- `stopHeartbeat`
- `getRoomOnlineUsers`
- `getRoomUserCount`

### FLUTTER (95 functions)

**`AmityClientGetConfiguration`** (`code_snippet/user/AmityClientGetConfiguration.dart`) — 1 functions:
- `getConfiguration`

**`amity_video_client`** (`lib/src/public/client/amity_video_client.dart`) — 1 functions:
- `newStreamRepository`

**`comment_repository`** (`lib/src/public/repo/comment_repository.dart`) — 1 functions:
- `updateComment`

**`sub_channel_repository`** (`lib/src/public/repo/sub_channel_repository.dart`) — 6 functions:
- `createSubChannel`
- `getSubChannels`
- `getSubChannel`
- `softDeleteSubChannel`
- `hardDeleteSubChannel`
- `updateeditSubChannelSubChannel`

**`amity_my_user_relationship_repository`** (`lib/src/public/repo/sub_set/follow/amity_my_user_relationship_repository.dart`) — 1 functions:
- `getBlockedUsers`

**`amity_user_relationships_repository`** (`lib/src/public/repo/sub_set/follow/amity_user_relationships_repository.dart`) — 14 functions:
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

**`poll_repository`** (`lib/src/public/repo/poll_repository.dart`) — 1 functions:
- `createPoll`

**`AmityClientGetMentionConfigurations`** (`code_snippet/core/AmityClientGetMentionConfigurations.dart`) — 1 functions:
- `getMentionConfigurations`

**`amity_social_client`** (`lib/src/public/client/amity_social_client.dart`) — 7 functions:
- `newPostRepository`
- `newCommentRepository`
- `newFeedRepository`
- `newCommunityRepository`
- `newPollRepository`
- `newStoryRepository`
- `newReactionRepository`

**`AmityClientUnregisterPush`** (`code_snippet/notification/AmityClientUnregisterPush.dart`) — 1 functions:
- `unregisterPush`

**`amity_story_repository_get`** (`code_snippet/story/amity_story_repository_get.dart`) — 1 functions:
- `initStoryRepository`

**`amity_ad_repository`** (`lib/src/public/repo/ads/amity_ad_repository.dart`) — 3 functions:
- `getNetworkAds`
- `serviceLocator`
- `analytics`

**`amity_post_repository`** (`lib/src/public/repo/amity_post_repository.dart`) — 6 functions:
- `getPostStream`
- `serviceLocator`
- `reviewPost`
- `getReaction`
- `getPinnedPosts`
- `getGlobalPinnedPosts`

**`message_repository`** (`lib/src/public/repo/message/message_repository.dart`) — 1 functions:
- `getReaction`

**`notification_repository`** (`lib/src/public/repo/notification_repository.dart`) — 3 functions:
- `registerDeviceNotification`
- `serviceLocator`
- `unregisterDeviceNotification`

**`stream_repository`** (`lib/src/public/repo/stream/stream_repository.dart`) — 3 functions:
- `getStreams`
- `getStream`
- `serviceLocator`

**`AmityClientGetCurrentUser`** (`code_snippet/user/AmityClientGetCurrentUser.dart`) — 1 functions:
- `getCurrentUser`

**`AmityClientRegisterPush`** (`code_snippet/notification/AmityClientRegisterPush.dart`) — 1 functions:
- `registerPush`

**`amity_stream_repository_initialization`** (`code_snippet/stream/amity_stream_repository_initialization.dart`) — 1 functions:
- `initializeStreamRepository`

**`amity_channel_repository`** (`lib/src/public/repo/channel/amity_channel_repository.dart`) — 9 functions:
- `membership`
- `serviceLocator`
- `moderation`
- `startReading`
- `stopReading`
- `archiveChannel`
- `unarchiveChannel`
- `getArchivedChannels`
- `getChannelTotalUnreads`

**`AmityClientUnregisterPushNotification`** (`code_snippet/notification/AmityClientUnregisterPushNotification.dart`) — 1 functions:
- `unregisterPushNotification`

**`AmityClientUpdateUser`** (`code_snippet/user/AmityClientUpdateUser.dart`) — 1 functions:
- `updateCurrentUser`

**`amity_user_repository`** (`code_snippet/user/amity_user_repository.dart`) — 1 functions:
- `initUserRepository`

**`amity_chat_client`** (`lib/src/public/client/amity_chat_client.dart`) — 4 functions:
- `newMessageRepository`
- `serviceLocator`
- `newChannelRepository`
- `newSubChannelRepository`

**`amity_community_repository`** (`lib/src/public/repo/amity_community_repository.dart`) — 4 functions:
- `membership`
- `moderation`
- `serviceLocator`
- `getCurrentUserRoles`

**`amity_file_repository`** (`lib/src/public/repo/amity_file_repository.dart`) — 1 functions:
- `cancelUpload`

**`amity_core_client`** (`lib/src/public/amity_core_client.dart`) — 13 functions:
- `setup`
- `validateUrls`
- `validateTexts`
- `isUserLoggedIn`
- `getUserId`
- `hasPermission`
- `newUserRepository`
- `newAdRepository`
- `newFileRepository`
- `getAnalyticsEngine`
- `observeSessionState`
- `observeUnreadCount`
- `copyWith`

**`AmityClientRegisterPushNotification`** (`code_snippet/notification/AmityClientRegisterPushNotification.dart`) — 1 functions:
- `registerPushNotification`

**`channel_moderation_repository`** (`lib/src/public/repo/channel/channel_moderation_repository.dart`) — 1 functions:
- `channelId`

**`user_repository`** (`lib/src/public/repo/user_repository.dart`) — 5 functions:
- `updateUser`
- `report`
- `relationship`
- `getBlockedUsers`
- `getViewedUsers`

### TYPESCRIPT (66 functions)

**`FileRepository`** (`packages/sdk/src/fileRepository/api/fileUrlWithSize.ts`) — 1 functions:
- `fileUrlWithSize`

**`InvitationRepository`** (`packages/sdk/src/invitationRepository/observers/getMyCommunityInvitations.ts`) — 1 functions:
- `getMyCommunityInvitations`

**`MessageRepository`** (`packages/sdk/src/messageRepository/api/deleteMessage.ts`) — 5 functions:
- `deleteMessage`
- `getDeliveredUsers`
- `getReadUsers`
- `markAsDelivered`
- `queryMessages`

**`ReactionRepository`** (`packages/sdk/src/reactionRepository/api/constants.ts`) — 3 functions:
- `REFERENCE_API_V5`
- `queryReactions`
- `queryReactor`

**`StreamRepository`** (`packages/sdk/src/streamRepository/api/disposeStream.ts`) — 2 functions:
- `disposeStream`
- `getStreams`

**`ChannelRepository`** (`packages/sdk/src/channelRepository/api/deleteChannel.ts`) — 5 functions:
- `deleteChannel`
- `getChannelByIds`
- `markChannelsAsReadBySegment`
- `queryChannels`
- `getMyMembership`

**`CommentRepository`** (`packages/sdk/src/commentRepository/api/getComment.ts`) — 2 functions:
- `getComment`
- `queryComments`

**`FeedRepository`** (`packages/sdk/src/feedRepository/observers/utils.ts`) — 1 functions:
- `getGlobalFeedSubscriptions`

**`LiveReactionRepository`** (`packages/sdk/src/liveReactionRepository/observers/getReactions.ts`) — 1 functions:
- `getReactions`

**`AdRepository`** (`packages/sdk/src/adRepository/api/getNetworkAds.ts`) — 1 functions:
- `getNetworkAds`

**`CommunityRepository`** (`packages/sdk/src/communityRepository/api/getCommunities.ts`) — 7 functions:
- `getCommunities`
- `getCommunity`
- `getTrendingCommunities`
- `queryCommunities`
- `getJoinRequests`
- `prepareSemanticCommunitiesReferenceId`
- `semanticSearchCommunities`

**`PostRepository`** (`packages/sdk/src/postRepository/api/deletePost.ts`) — 8 functions:
- `deletePost`
- `getPost`
- `queryPosts`
- `getGlobalPinnedPosts`
- `getPinnedPosts`
- `preparePostResponse`
- `semanticSearchPosts`
- `generateCommentSubscriptions`

**`RoomRepository`** (`packages/sdk/src/roomRepository/api/analytics/WatchSessionStorage.ts`) — 4 functions:
- `getWatchSessionStorage`
- `syncWatchSessions`
- `getRoom`
- `convertToRoomEventPayload`

**`UserRepository`** (`packages/sdk/src/userRepository/api/getUser.ts`) — 4 functions:
- `getUser`
- `queryBlockedUsers`
- `queryUsers`
- `getReachedUsers`

**`EventRepository`** (`packages/sdk/src/eventRepository/observers/getEvents.ts`) — 3 functions:
- `getEvents`
- `getMyEvents`
- `getRSVPs`

**`StoryRepository`** (`packages/sdk/src/storyRepository/api/createImageStory.ts`) — 10 functions:
- `createImageStory`
- `createVideoStory`
- `hardDeleteStory`
- `softDeleteStory`
- `getActiveStoriesByTarget`
- `getGlobalStoryTargets`
- `getStoriesByTargetIds`
- `getStoryByStoryId`
- `getTargetById`
- `getTargetsByTargetIds`

**`SubChannelRepository`** (`packages/sdk/src/subChannelRepository/api/deleteSubChannel.ts`) — 8 functions:
- `deleteSubChannel`
- `getSubChannel`
- `getSubChannels`
- `markAsReadBySegment`
- `querySubChannels`
- `readingAPI`
- `startReadingAPI`
- `stopReadingAPI`

---

## After completion

```bash
cd social-plus-docs/harness
./harness-bin audit --config harness-config.yml
# If open findings remain: ./harness-bin prompt --config harness-config.yml
```
