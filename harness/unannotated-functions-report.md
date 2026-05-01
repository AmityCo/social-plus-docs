# Unannotated Public Functions Report

**Total:** 349 functions need `begin_public_function` annotation

## Android (116 functions across 47 classes)

### `AmityPostRepository` (13 functions)
> `amity-sdk/src/main/java/com/amity/socialcloud/sdk/api/social/post/AmityPostRepository.kt`

| Function | Status |
|----------|--------|
| `createCustomPost` | ⬜ needs `begin_public_function` |
| `createFilePost` | ⬜ needs `begin_public_function` |
| `createImagePost` | ⬜ needs `begin_public_function` |
| `createLiveStreamPost` | ⬜ needs `begin_public_function` |
| `createMixedAttachmentPost` | ⬜ needs `begin_public_function` |
| `createPollPost` | ⬜ needs `begin_public_function` |
| `createPost` | ⬜ needs `begin_public_function` |
| `createTextPost` | ⬜ needs `begin_public_function` |
| `createVideoPost` | ⬜ needs `begin_public_function` |
| `flagPost` | ⬜ needs `begin_public_function` |
| `getGlobalPinnedPosts` | ⬜ needs `begin_public_function` |
| `getPinnedPosts` | ⬜ needs `begin_public_function` |
| `semanticSearchPosts` | ⬜ needs `begin_public_function` |

### `AmityStoryRepository` (11 functions)
> `amity-sdk/src/main/java/com/amity/socialcloud/sdk/api/social/story/AmityStoryRepository.kt`

| Function | Status |
|----------|--------|
| `analytics` | ⬜ needs `begin_public_function` |
| `createImageStory` | ⬜ needs `begin_public_function` |
| `createVideoStory` | ⬜ needs `begin_public_function` |
| `getActiveStories` | ⬜ needs `begin_public_function` |
| `getGlobalStoryTargets` | ⬜ needs `begin_public_function` |
| `getStoriesByTargets` | ⬜ needs `begin_public_function` |
| `getStory` | ⬜ needs `begin_public_function` |
| `getStoryTarget` | ⬜ needs `begin_public_function` |
| `getStoryTargets` | ⬜ needs `begin_public_function` |
| `hardDeleteStory` | ⬜ needs `begin_public_function` |
| `softDeleteStory` | ⬜ needs `begin_public_function` |

### `AmityFileRepository` (9 functions)
> `amity-sdk/src/main/java/com/amity/socialcloud/sdk/api/core/file/AmityFileRepository.kt`

| Function | Status |
|----------|--------|
| `cancelUpload` | ⬜ needs `begin_public_function` |
| `getFile` | ⬜ needs `begin_public_function` |
| `getUploadInfo` | ⬜ needs `begin_public_function` |
| `updateAltText` | ⬜ needs `begin_public_function` |
| `uploadAudio` | ⬜ needs `begin_public_function` |
| `uploadClip` | ⬜ needs `begin_public_function` |
| `uploadFile` | ⬜ needs `begin_public_function` |
| `uploadImage` | ⬜ needs `begin_public_function` |
| `uploadVideo` | ⬜ needs `begin_public_function` |

### `AmityMessageRepository` (6 functions)
> `amity-sdk/src/main/java/com/amity/socialcloud/sdk/api/chat/message/AmityMessageRepository.kt`

| Function | Status |
|----------|--------|
| `createAudioMessage` | ⬜ needs `begin_public_function` |
| `createFileMessage` | ⬜ needs `begin_public_function` |
| `createImageMessage` | ⬜ needs `begin_public_function` |
| `createVideoMessage` | ⬜ needs `begin_public_function` |
| `deleteFailedMessages` | ⬜ needs `begin_public_function` |
| `flagMessage` | ⬜ needs `begin_public_function` |

### `AmityRoomPresenceRepository` (6 functions)
> `amity-sdk/src/main/java/com/amity/socialcloud/sdk/api/core/presence/AmityRoomPresenceRepository.kt`

| Function | Status |
|----------|--------|
| `getOnlineUsersCount` | ⬜ needs `begin_public_function` |
| `getOnlineUsersSnapshot` | ⬜ needs `begin_public_function` |
| `observeOnlineUsersCount` | ⬜ needs `begin_public_function` |
| `roomId` | ⬜ needs `begin_public_function` |
| `startHeartbeat` | ⬜ needs `begin_public_function` |
| `stopHeartbeat` | ⬜ needs `begin_public_function` |

### `AmityRoomRepository` (6 functions)
> `amity-sdk/src/main/java/com/amity/socialcloud/sdk/api/video/room/AmityRoomRepository.kt`

| Function | Status |
|----------|--------|
| `fetchRoom` | ⬜ needs `begin_public_function` |
| `getCoHostEvent` | ⬜ needs `begin_public_function` |
| `getRecordedUrls` | ⬜ needs `begin_public_function` |
| `leaveRoom` | ⬜ needs `begin_public_function` |
| `removeRoomParticipant` | ⬜ needs `begin_public_function` |
| `updateCohostPermission` | ⬜ needs `begin_public_function` |

### `AmityChannelRepository` (5 functions)
> `amity-sdk/src/main/java/com/amity/socialcloud/sdk/api/chat/channel/AmityChannelRepository.kt`

| Function | Status |
|----------|--------|
| `getChannels` | ⬜ needs `begin_public_function` |
| `getTotalChannelUnread` | ⬜ needs `begin_public_function` |
| `getTotalChannelsUnreadInfo` | ⬜ needs `begin_public_function` |
| `membership` | ⬜ needs `begin_public_function` |
| `moderation` | ⬜ needs `begin_public_function` |

### `AnalyticsRepository` (5 functions)
> `amity-sdk/src/main/java/com/amity/socialcloud/sdk/core/data/analytics/AnalyticsRepository.kt`

| Function | Status |
|----------|--------|
| `createAnalyticEvent` | ⬜ needs `begin_public_function` |
| `deleteAllAnalyticsEvents` | ⬜ needs `begin_public_function` |
| `getViewedUsers` | ⬜ needs `begin_public_function` |
| `saveAnalyticEvent` | ⬜ needs `begin_public_function` |
| `sendAnalyticsEvents` | ⬜ needs `begin_public_function` |

### `AmityLiveReactionRepository` (3 functions)
> `amity-sdk/src/main/java/com/amity/socialcloud/sdk/api/core/reaction/AmityLiveReactionRepository.kt`

| Function | Status |
|----------|--------|
| `createReaction` | ⬜ needs `begin_public_function` |
| `createRoomReaction` | ⬜ needs `begin_public_function` |
| `getReactions` | ⬜ needs `begin_public_function` |

### `AmityReactionRepository` (3 functions)
> `amity-sdk/src/main/java/com/amity/socialcloud/sdk/api/core/reaction/AmityReactionRepository.kt`

| Function | Status |
|----------|--------|
| `addReaction` | ⬜ needs `begin_public_function` |
| `getReactions` | ⬜ needs `begin_public_function` |
| `removeReaction` | ⬜ needs `begin_public_function` |

### `AmityStreamRepository` (3 functions)
> `amity-sdk/src/main/java/com/amity/socialcloud/sdk/api/video/stream/AmityStreamRepository.kt`

| Function | Status |
|----------|--------|
| `createStream` | ⬜ needs `begin_public_function` |
| `editStream` | ⬜ needs `begin_public_function` |
| `fetchStream` | ⬜ needs `begin_public_function` |

### `AmityClientLoginWithAccessToken` (2 functions)
> `amity-sample-code/src/main/java/com/amity/snipet/verifier/core/gettingstarted/AmityClientLoginWithAccessToken.kt`

| Function | Status |
|----------|--------|
| `loginWithAccessToken` | ⬜ needs `begin_public_function` |
| `sessionWillRenewAccessToken` | ⬜ needs `begin_public_function` |

### `AmityClientRenewAccessToken` (2 functions)
> `amity-sample-code/src/main/java/com/amity/snipet/verifier/core/gettingstarted/AmityClientRenewAccessToken.kt`

| Function | Status |
|----------|--------|
| `sessionWillRenewAccessToken` | ⬜ needs `begin_public_function` |
| `setupRenewal` | ⬜ needs `begin_public_function` |

### `AmityClientSetAccessTokenHandler` (2 functions)
> `amity-sample-code/src/main/java/com/amity/snipet/verifier/core/gettingstarted/AmityClientSetAccessTokenHandler.kt`

| Function | Status |
|----------|--------|
| `sessionWillRenewAccessToken` | ⬜ needs `begin_public_function` |
| `setAccessTokenHandler` | ⬜ needs `begin_public_function` |

### `AmityAdRepository` (2 functions)
> `amity-sdk/src/main/java/com/amity/socialcloud/sdk/api/core/ads/AmityAdRepository.kt`

| Function | Status |
|----------|--------|
| `analytics` | ⬜ needs `begin_public_function` |
| `getNetworkAds` | ⬜ needs `begin_public_function` |

### `AmityInvitationRepository` (2 functions)
> `amity-sdk/src/main/java/com/amity/socialcloud/sdk/api/core/invitation/AmityInvitationRepository.kt`

| Function | Status |
|----------|--------|
| `getInvitations` | ⬜ needs `begin_public_function` |
| `getMyCommunityInvitations` | ⬜ needs `begin_public_function` |

### `AmityCommunityRepository` (2 functions)
> `amity-sdk/src/main/java/com/amity/socialcloud/sdk/api/social/community/AmityCommunityRepository.kt`

| Function | Status |
|----------|--------|
| `membership` | ⬜ needs `begin_public_function` |
| `moderation` | ⬜ needs `begin_public_function` |

### `CommunityNotificationRepository` (2 functions)
> `amity-sdk/src/main/java/com/amity/socialcloud/sdk/core/data/notification/community/CommunityNotificationRepository.kt`

| Function | Status |
|----------|--------|
| `getNotificationSettings` | ⬜ needs `begin_public_function` |
| `saveNotificationSettings` | ⬜ needs `begin_public_function` |

### `TombstoneRepository` (2 functions)
> `amity-sdk/src/main/java/com/amity/socialcloud/sdk/core/data/tombstone/TombstoneRepository.kt`

| Function | Status |
|----------|--------|
| `getTombstone` | ⬜ needs `begin_public_function` |
| `saveTombstone` | ⬜ needs `begin_public_function` |

### `StreamPlayerClient` (2 functions)
> `amity-video-player/src/main/java/com/amity/socialcloud/sdk/video/StreamPlayerClient.kt`

| Function | Status |
|----------|--------|
| `getFunction` | ⬜ needs `begin_public_function` |
| `setup` | ⬜ needs `begin_public_function` |

### `StreamBroadcasterClient` (2 functions)
> `amity-video-publisher/src/main/java/com/amity/socialcloud/sdk/video/StreamBroadcasterClient.kt`

| Function | Status |
|----------|--------|
| `getFunction` | ⬜ needs `begin_public_function` |
| `setup` | ⬜ needs `begin_public_function` |

### `FileRepository` (1 functions)
> `amity-rxupload/src/main/java/co/amity/rxupload/internal/repository/FileRepository.kt`

| Function | Status |
|----------|--------|
| `upload` | ⬜ needs `begin_public_function` |

### `AmityClientFetchLinkPreview` (1 functions)
> `amity-sample-code/src/main/java/com/amity/snipet/verifier/core/gettingstarted/AmityClientFetchLinkPreview.kt`

| Function | Status |
|----------|--------|
| `fetchLinkPreview` | ⬜ needs `begin_public_function` |

### `AmityClientGetLoginMethod` (1 functions)
> `amity-sample-code/src/main/java/com/amity/snipet/verifier/core/gettingstarted/AmityClientGetLoginMethod.kt`

| Function | Status |
|----------|--------|
| `getLoginMethod` | ⬜ needs `begin_public_function` |

### `AmityClientGetProductCatalogueSetting` (1 functions)
> `amity-sample-code/src/main/java/com/amity/snipet/verifier/core/gettingstarted/AmityClientGetProductCatalogueSetting.kt`

| Function | Status |
|----------|--------|
| `getProductCatalogueSetting` | ⬜ needs `begin_public_function` |

### `AmityClientObserveSessionState` (1 functions)
> `amity-sample-code/src/main/java/com/amity/snipet/verifier/core/gettingstarted/AmityClientObserveSessionState.kt`

| Function | Status |
|----------|--------|
| `observeSessionState` | ⬜ needs `begin_public_function` |

### `AmityClientReadSessionState` (1 functions)
> `amity-sample-code/src/main/java/com/amity/snipet/verifier/core/gettingstarted/AmityClientReadSessionState.kt`

| Function | Status |
|----------|--------|
| `readSessionState` | ⬜ needs `begin_public_function` |

### `AmityClientSecureLogout` (1 functions)
> `amity-sample-code/src/main/java/com/amity/snipet/verifier/core/gettingstarted/AmityClientSecureLogout.kt`

| Function | Status |
|----------|--------|
| `secureLogout` | ⬜ needs `begin_public_function` |

### `AmityClientRegisterPush` (1 functions)
> `amity-sample-code/src/main/java/com/amity/snipet/verifier/core/notification/registration/AmityClientRegisterPush.kt`

| Function | Status |
|----------|--------|
| `registerPush` | ⬜ needs `begin_public_function` |

### `AmityClientUnregisterPush` (1 functions)
> `amity-sample-code/src/main/java/com/amity/snipet/verifier/core/notification/registration/AmityClientUnregisterPush.kt`

| Function | Status |
|----------|--------|
| `unregisterPush` | ⬜ needs `begin_public_function` |

### `AmityClientPresenceDisable` (1 functions)
> `amity-sample-code/src/main/java/com/amity/snipet/verifier/core/presence/AmityClientPresenceDisable.kt`

| Function | Status |
|----------|--------|
| `disablePresence` | ⬜ needs `begin_public_function` |

### `AmityClientPresenceEnable` (1 functions)
> `amity-sample-code/src/main/java/com/amity/snipet/verifier/core/presence/AmityClientPresenceEnable.kt`

| Function | Status |
|----------|--------|
| `enablePresence` | ⬜ needs `begin_public_function` |

### `AmityClientPresenceIsEnabled` (1 functions)
> `amity-sample-code/src/main/java/com/amity/snipet/verifier/core/presence/AmityClientPresenceIsEnabled.kt`

| Function | Status |
|----------|--------|
| `isPresenceEnabled` | ⬜ needs `begin_public_function` |

### `AmityClientPresenceStartHeartbeat` (1 functions)
> `amity-sample-code/src/main/java/com/amity/snipet/verifier/core/presence/AmityClientPresenceStartHeartbeat.kt`

| Function | Status |
|----------|--------|
| `startHeartbeat` | ⬜ needs `begin_public_function` |

### `AmityClientPresenceStopHeartbeat` (1 functions)
> `amity-sample-code/src/main/java/com/amity/snipet/verifier/core/presence/AmityClientPresenceStopHeartbeat.kt`

| Function | Status |
|----------|--------|
| `stopHeartbeat` | ⬜ needs `begin_public_function` |

### `AmityClientGetCurrentUser` (1 functions)
> `amity-sample-code/src/main/java/com/amity/snipet/verifier/core/user/AmityClientGetCurrentUser.kt`

| Function | Status |
|----------|--------|
| `getCurrentUser` | ⬜ needs `begin_public_function` |

### `AmityClientUpdateUser` (1 functions)
> `amity-sample-code/src/main/java/com/amity/snipet/verifier/core/user/AmityClientUpdateUser.kt`

| Function | Status |
|----------|--------|
| `updateUser` | ⬜ needs `begin_public_function` |

### `AmityCommentRepositoryInitialization` (1 functions)
> `amity-sample-code/src/main/java/com/amity/snipet/verifier/social/comment/AmityCommentRepositoryInitialization.kt`

| Function | Status |
|----------|--------|
| `initializeCommentRepository` | ⬜ needs `begin_public_function` |

### `AmityFeedRepositoryInitialization` (1 functions)
> `amity-sample-code/src/main/java/com/amity/snipet/verifier/social/feed/AmityFeedRepositoryInitialization.kt`

| Function | Status |
|----------|--------|
| `initializeFeedRepository` | ⬜ needs `begin_public_function` |

### `AmityPostRepositoryInitialization` (1 functions)
> `amity-sample-code/src/main/java/com/amity/snipet/verifier/social/post/AmityPostRepositoryInitialization.kt`

| Function | Status |
|----------|--------|
| `initializePostRepository` | ⬜ needs `begin_public_function` |

### `AmityInitStoryRepository` (1 functions)
> `amity-sample-code/src/main/java/com/amity/snipet/verifier/social/story/init/AmityInitStoryRepository.kt`

| Function | Status |
|----------|--------|
| `initStoryRepository` | ⬜ needs `begin_public_function` |

### `AmityUserRepository` (1 functions)
> `amity-sdk/src/main/java/com/amity/socialcloud/sdk/api/core/user/AmityUserRepository.kt`

| Function | Status |
|----------|--------|
| `relationship` | ⬜ needs `begin_public_function` |

### `AmityCommentRepository` (1 functions)
> `amity-sdk/src/main/java/com/amity/socialcloud/sdk/api/social/comment/AmityCommentRepository.kt`

| Function | Status |
|----------|--------|
| `flagComment` | ⬜ needs `begin_public_function` |

### `AmityFeedRepository` (1 functions)
> `amity-sdk/src/main/java/com/amity/socialcloud/sdk/api/social/post/AmityFeedRepository.kt`

| Function | Status |
|----------|--------|
| `getMyFeed` | ⬜ needs `begin_public_function` |

### `MarkerSyncRepository` (1 functions)
> `amity-sdk/src/main/java/com/amity/socialcloud/sdk/chat/data/marker/sync/MarkerSyncRepository.kt`

| Function | Status |
|----------|--------|
| `syncMarkers` | ⬜ needs `begin_public_function` |

### `UserMarkerRepository` (1 functions)
> `amity-sdk/src/main/java/com/amity/socialcloud/sdk/chat/data/marker/user/UserMarkerRepository.kt`

| Function | Status |
|----------|--------|
| `getUserMarker` | ⬜ needs `begin_public_function` |

### `UserRelationshipRepository` (1 functions)
> `amity-sdk/src/main/java/com/amity/socialcloud/sdk/core/data/relationship/UserRelationshipRepository.kt`

| Function | Status |
|----------|--------|
| `hasInLocal` | ⬜ needs `begin_public_function` |

## Flutter (101 functions across 30 classes)

### `amity_user_relationships_repository` (16 functions)
> `lib/src/public/repo/sub_set/follow/amity_user_relationships_repository.dart`

| Function | Status |
|----------|--------|
| `acceptMyFollower` | ⬜ needs `begin_public_function` |
| `blockUser` | ⬜ needs `begin_public_function` |
| `declineMyFollower` | ⬜ needs `begin_public_function` |
| `follow` | ⬜ needs `begin_public_function` |
| `getFollowInfo` | ⬜ needs `begin_public_function` |
| `getFollowers` | ⬜ needs `begin_public_function` |
| `getFollowings` | ⬜ needs `begin_public_function` |
| `getMyFollowInfo` | ⬜ needs `begin_public_function` |
| `getMyFollowers` | ⬜ needs `begin_public_function` |
| `getMyFollowings` | ⬜ needs `begin_public_function` |
| `me` | ⬜ needs `begin_public_function` |
| `removeMyFollower` | ⬜ needs `begin_public_function` |
| `serviceLocator` | ⬜ needs `begin_public_function` |
| `unblockUser` | ⬜ needs `begin_public_function` |
| `unfollow` | ⬜ needs `begin_public_function` |
| `user` | ⬜ needs `begin_public_function` |

### `amity_core_client` (13 functions)
> `lib/src/public/amity_core_client.dart`

| Function | Status |
|----------|--------|
| `copyWith` | ⬜ needs `begin_public_function` |
| `getAnalyticsEngine` | ⬜ needs `begin_public_function` |
| `getUserId` | ⬜ needs `begin_public_function` |
| `hasPermission` | ⬜ needs `begin_public_function` |
| `isUserLoggedIn` | ⬜ needs `begin_public_function` |
| `newAdRepository` | ⬜ needs `begin_public_function` |
| `newFileRepository` | ⬜ needs `begin_public_function` |
| `newUserRepository` | ⬜ needs `begin_public_function` |
| `observeSessionState` | ⬜ needs `begin_public_function` |
| `observeUnreadCount` | ⬜ needs `begin_public_function` |
| `setup` | ⬜ needs `begin_public_function` |
| `validateTexts` | ⬜ needs `begin_public_function` |
| `validateUrls` | ⬜ needs `begin_public_function` |

### `amity_channel_repository` (9 functions)
> `lib/src/public/repo/channel/amity_channel_repository.dart`

| Function | Status |
|----------|--------|
| `archiveChannel` | ⬜ needs `begin_public_function` |
| `getArchivedChannels` | ⬜ needs `begin_public_function` |
| `getChannelTotalUnreads` | ⬜ needs `begin_public_function` |
| `membership` | ⬜ needs `begin_public_function` |
| `moderation` | ⬜ needs `begin_public_function` |
| `serviceLocator` | ⬜ needs `begin_public_function` |
| `startReading` | ⬜ needs `begin_public_function` |
| `stopReading` | ⬜ needs `begin_public_function` |
| `unarchiveChannel` | ⬜ needs `begin_public_function` |

### `amity_social_client` (7 functions)
> `lib/src/public/client/amity_social_client.dart`

| Function | Status |
|----------|--------|
| `newCommentRepository` | ⬜ needs `begin_public_function` |
| `newCommunityRepository` | ⬜ needs `begin_public_function` |
| `newFeedRepository` | ⬜ needs `begin_public_function` |
| `newPollRepository` | ⬜ needs `begin_public_function` |
| `newPostRepository` | ⬜ needs `begin_public_function` |
| `newReactionRepository` | ⬜ needs `begin_public_function` |
| `newStoryRepository` | ⬜ needs `begin_public_function` |

### `amity_post_repository` (6 functions)
> `lib/src/public/repo/amity_post_repository.dart`

| Function | Status |
|----------|--------|
| `getGlobalPinnedPosts` | ⬜ needs `begin_public_function` |
| `getPinnedPosts` | ⬜ needs `begin_public_function` |
| `getPostStream` | ⬜ needs `begin_public_function` |
| `getReaction` | ⬜ needs `begin_public_function` |
| `reviewPost` | ⬜ needs `begin_public_function` |
| `serviceLocator` | ⬜ needs `begin_public_function` |

### `sub_channel_repository` (6 functions)
> `lib/src/public/repo/sub_channel_repository.dart`

| Function | Status |
|----------|--------|
| `createSubChannel` | ⬜ needs `begin_public_function` |
| `getSubChannel` | ⬜ needs `begin_public_function` |
| `getSubChannels` | ⬜ needs `begin_public_function` |
| `hardDeleteSubChannel` | ⬜ needs `begin_public_function` |
| `softDeleteSubChannel` | ⬜ needs `begin_public_function` |
| `updateeditSubChannelSubChannel` | ⬜ needs `begin_public_function` |

### `amity_community_repository` (5 functions)
> `lib/src/public/repo/amity_community_repository.dart`

| Function | Status |
|----------|--------|
| `getCurentUserRoles` | ⬜ needs `begin_public_function` |
| `getCurrentUserRoles` | ⬜ needs `begin_public_function` |
| `membership` | ⬜ needs `begin_public_function` |
| `moderation` | ⬜ needs `begin_public_function` |
| `serviceLocator` | ⬜ needs `begin_public_function` |

### `user_repository` (5 functions)
> `lib/src/public/repo/user_repository.dart`

| Function | Status |
|----------|--------|
| `getBlockedUsers` | ⬜ needs `begin_public_function` |
| `getViewedUsers` | ⬜ needs `begin_public_function` |
| `relationship` | ⬜ needs `begin_public_function` |
| `report` | ⬜ needs `begin_public_function` |
| `updateUser` | ⬜ needs `begin_public_function` |

### `amity_chat_client` (4 functions)
> `lib/src/public/client/amity_chat_client.dart`

| Function | Status |
|----------|--------|
| `newChannelRepository` | ⬜ needs `begin_public_function` |
| `newMessageRepository` | ⬜ needs `begin_public_function` |
| `newSubChannelRepository` | ⬜ needs `begin_public_function` |
| `serviceLocator` | ⬜ needs `begin_public_function` |

### `message_repository` (4 functions)
> `lib/src/public/repo/message/message_repository.dart`

| Function | Status |
|----------|--------|
| `flag` | ⬜ needs `begin_public_function` |
| `getReaction` | ⬜ needs `begin_public_function` |
| `newCreateMessage` | ⬜ needs `begin_public_function` |
| `newGetMessages` | ⬜ needs `begin_public_function` |

### `amity_ad_repository` (3 functions)
> `lib/src/public/repo/ads/amity_ad_repository.dart`

| Function | Status |
|----------|--------|
| `analytics` | ⬜ needs `begin_public_function` |
| `getNetworkAds` | ⬜ needs `begin_public_function` |
| `serviceLocator` | ⬜ needs `begin_public_function` |

### `notification_repository` (3 functions)
> `lib/src/public/repo/notification_repository.dart`

| Function | Status |
|----------|--------|
| `registerDeviceNotification` | ⬜ needs `begin_public_function` |
| `serviceLocator` | ⬜ needs `begin_public_function` |
| `unregisterDeviceNotification` | ⬜ needs `begin_public_function` |

### `stream_repository` (3 functions)
> `lib/src/public/repo/stream/stream_repository.dart`

| Function | Status |
|----------|--------|
| `getStream` | ⬜ needs `begin_public_function` |
| `getStreams` | ⬜ needs `begin_public_function` |
| `serviceLocator` | ⬜ needs `begin_public_function` |

### `AmityClientGetMentionConfigurations` (1 functions)
> `code_snippet/core/AmityClientGetMentionConfigurations.dart`

| Function | Status |
|----------|--------|
| `getMentionConfigurations` | ⬜ needs `begin_public_function` |

### `AmityClientRegisterPush` (1 functions)
> `code_snippet/notification/AmityClientRegisterPush.dart`

| Function | Status |
|----------|--------|
| `registerPush` | ⬜ needs `begin_public_function` |

### `AmityClientRegisterPushNotification` (1 functions)
> `code_snippet/notification/AmityClientRegisterPushNotification.dart`

| Function | Status |
|----------|--------|
| `registerPushNotification` | ⬜ needs `begin_public_function` |

### `AmityClientUnregisterPush` (1 functions)
> `code_snippet/notification/AmityClientUnregisterPush.dart`

| Function | Status |
|----------|--------|
| `unregisterPush` | ⬜ needs `begin_public_function` |

### `AmityClientUnregisterPushNotification` (1 functions)
> `code_snippet/notification/AmityClientUnregisterPushNotification.dart`

| Function | Status |
|----------|--------|
| `unregisterPushNotification` | ⬜ needs `begin_public_function` |

### `amity_story_repository_get` (1 functions)
> `code_snippet/story/amity_story_repository_get.dart`

| Function | Status |
|----------|--------|
| `initStoryRepository` | ⬜ needs `begin_public_function` |

### `amity_stream_repository_initialization` (1 functions)
> `code_snippet/stream/amity_stream_repository_initialization.dart`

| Function | Status |
|----------|--------|
| `initializeStreamRepository` | ⬜ needs `begin_public_function` |

### `AmityClientGetConfiguration` (1 functions)
> `code_snippet/user/AmityClientGetConfiguration.dart`

| Function | Status |
|----------|--------|
| `getConfiguration` | ⬜ needs `begin_public_function` |

### `AmityClientGetCurrentUser` (1 functions)
> `code_snippet/user/AmityClientGetCurrentUser.dart`

| Function | Status |
|----------|--------|
| `getCurrentUser` | ⬜ needs `begin_public_function` |

### `AmityClientUpdateUser` (1 functions)
> `code_snippet/user/AmityClientUpdateUser.dart`

| Function | Status |
|----------|--------|
| `updateCurrentUser` | ⬜ needs `begin_public_function` |

### `amity_user_repository` (1 functions)
> `code_snippet/user/amity_user_repository.dart`

| Function | Status |
|----------|--------|
| `initUserRepository` | ⬜ needs `begin_public_function` |

### `amity_video_client` (1 functions)
> `lib/src/public/client/amity_video_client.dart`

| Function | Status |
|----------|--------|
| `newStreamRepository` | ⬜ needs `begin_public_function` |

### `amity_file_repository` (1 functions)
> `lib/src/public/repo/amity_file_repository.dart`

| Function | Status |
|----------|--------|
| `cancelUpload` | ⬜ needs `begin_public_function` |

### `channel_moderation_repository` (1 functions)
> `lib/src/public/repo/channel/channel_moderation_repository.dart`

| Function | Status |
|----------|--------|
| `channelId` | ⬜ needs `begin_public_function` |

### `comment_repository` (1 functions)
> `lib/src/public/repo/comment_repository.dart`

| Function | Status |
|----------|--------|
| `updateComment` | ⬜ needs `begin_public_function` |

### `poll_repository` (1 functions)
> `lib/src/public/repo/poll_repository.dart`

| Function | Status |
|----------|--------|
| `createPoll` | ⬜ needs `begin_public_function` |

### `amity_my_user_relationship_repository` (1 functions)
> `lib/src/public/repo/sub_set/follow/amity_my_user_relationship_repository.dart`

| Function | Status |
|----------|--------|
| `getBlockedUsers` | ⬜ needs `begin_public_function` |

## Ios (66 functions across 15 classes)

### `AmityClient` (19 functions)
> `EkoChat/Core/Client/AmityClient.swift`

| Function | Status |
|----------|--------|
| `accessToken` | ⬜ needs `begin_public_function` |
| `currentUserId` | ⬜ needs `begin_public_function` |
| `enableUnreadCount` | ⬜ needs `begin_public_function` |
| `getLinkPreviewMetadata` | ⬜ needs `begin_public_function` |
| `getShareableLinkConfiguration` | ⬜ needs `begin_public_function` |
| `getUserUnread` | ⬜ needs `begin_public_function` |
| `getVisitorDeviceId` | ⬜ needs `begin_public_function` |
| `loginMethod` | ⬜ needs `begin_public_function` |
| `mentionConfigurations` | ⬜ needs `begin_public_function` |
| `notificationTray` | ⬜ needs `begin_public_function` |
| `observeNetworkActivities` | ⬜ needs `begin_public_function` |
| `presence` | ⬜ needs `begin_public_function` |
| `secureLogout` | ⬜ needs `begin_public_function` |
| `sendCustomCommand` | ⬜ needs `begin_public_function` |
| `sendCustomCommandRequest` | ⬜ needs `begin_public_function` |
| `setUploadedFileAccessType` | ⬜ needs `begin_public_function` |
| `setup` | ⬜ needs `begin_public_function` |
| `validateTexts` | ⬜ needs `begin_public_function` |
| `validateUrls` | ⬜ needs `begin_public_function` |

### `AmityFileRepository` (11 functions)
> `EkoChat/Features/File/Public/AmityFileRepository.swift`

| Function | Status |
|----------|--------|
| `cancelFileDownload` | ⬜ needs `begin_public_function` |
| `cancelImageDownload` | ⬜ needs `begin_public_function` |
| `downloadFile` | ⬜ needs `begin_public_function` |
| `downloadFileAsData` | ⬜ needs `begin_public_function` |
| `downloadImage` | ⬜ needs `begin_public_function` |
| `downloadImageAsData` | ⬜ needs `begin_public_function` |
| `getUploadProgress` | ⬜ needs `begin_public_function` |
| `uploadAudio` | ⬜ needs `begin_public_function` |
| `uploadFile` | ⬜ needs `begin_public_function` |
| `uploadImage` | ⬜ needs `begin_public_function` |
| `uploadVideo` | ⬜ needs `begin_public_function` |

### `AmityStoryRepository` (10 functions)
> `EkoChat/Features/Story/Public/AmityStoryRepository.swift`

| Function | Status |
|----------|--------|
| `createImageStory` | ⬜ needs `begin_public_function` |
| `createVideoStory` | ⬜ needs `begin_public_function` |
| `getActiveStoriesByTarget` | ⬜ needs `begin_public_function` |
| `getGlobalStoryTargets` | ⬜ needs `begin_public_function` |
| `getStoriesByTargets` | ⬜ needs `begin_public_function` |
| `getStory` | ⬜ needs `begin_public_function` |
| `getStoryTarget` | ⬜ needs `begin_public_function` |
| `getStoryTargets` | ⬜ needs `begin_public_function` |
| `hardDeleteStory` | ⬜ needs `begin_public_function` |
| `softDeleteStory` | ⬜ needs `begin_public_function` |

### `AmitySubChannelRepository` (5 functions)
> `EkoChat/Features/SubChannel/AmitySubChannelRepository.swift`

| Function | Status |
|----------|--------|
| `channelId` | ⬜ needs `begin_public_function` |
| `excludeDefaultSubChannel` | ⬜ needs `begin_public_function` |
| `isDeleted` | ⬜ needs `begin_public_function` |
| `startMessageReceiptSync` | ⬜ needs `begin_public_function` |
| `stopMessageReceiptSync` | ⬜ needs `begin_public_function` |

### `AmityRoomPresenceRepository` (4 functions)
> `EkoChat/Features/CoHostStream/Presence/AmityRoomPresenceRepository.swift`

| Function | Status |
|----------|--------|
| `getRoomOnlineUsers` | ⬜ needs `begin_public_function` |
| `getRoomUserCount` | ⬜ needs `begin_public_function` |
| `startHeartbeat` | ⬜ needs `begin_public_function` |
| `stopHeartbeat` | ⬜ needs `begin_public_function` |

### `AmityPostRepository` (4 functions)
> `EkoChat/Features/Feed/Public/Repository/Post/AmityPostRepository.swift`

| Function | Status |
|----------|--------|
| `createLiveStreamPost` | ⬜ needs `begin_public_function` |
| `editPost` | ⬜ needs `begin_public_function` |
| `getPosts` | ⬜ needs `begin_public_function` |
| `getReactions` | ⬜ needs `begin_public_function` |

### `AmityMessageRepository` (4 functions)
> `EkoChat/Features/Message/Public/AmityMessageRepository.swift`

| Function | Status |
|----------|--------|
| `deleteFailedMessages` | ⬜ needs `begin_public_function` |
| `flagMessage` | ⬜ needs `begin_public_function` |
| `getReactions` | ⬜ needs `begin_public_function` |
| `setTags` | ⬜ needs `begin_public_function` |

### `AmityReactionRepository` (2 functions)
> `EkoChat/Features/Reaction/Public/AmityReactionRepository.swift`

| Function | Status |
|----------|--------|
| `createReaction` | ⬜ needs `begin_public_function` |
| `getReactions` | ⬜ needs `begin_public_function` |

### `AmityChannelPresenceRepository` (1 functions)
> `EkoChat/Core/Presence/Public/AmityChannelPresenceRepository.swift`

| Function | Status |
|----------|--------|
| `defaultViewId` | ⬜ needs `begin_public_function` |

### `AmityUserPresenceRepository` (1 functions)
> `EkoChat/Core/Presence/Public/AmityUserPresenceRepository.swift`

| Function | Status |
|----------|--------|
| `defaultViewId` | ⬜ needs `begin_public_function` |

### `AmityChannelRepository` (1 functions)
> `EkoChat/Features/Channel/Public/AmityChannelRepository.swift`

| Function | Status |
|----------|--------|
| `getTotalChannelsUnread` | ⬜ needs `begin_public_function` |

### `AmityRoomRepository` (1 functions)
> `EkoChat/Features/CoHostStream/Public/AmityRoomRepository.swift`

| Function | Status |
|----------|--------|
| `generateRoomToken` | ⬜ needs `begin_public_function` |

### `AmityCommentRepository` (1 functions)
> `EkoChat/Features/Comment/Public/AmityCommentRepository.swift`

| Function | Status |
|----------|--------|
| `getReactions` | ⬜ needs `begin_public_function` |

### `AmityFeedRepository` (1 functions)
> `EkoChat/Features/Feed/Public/Repository/Feed/AmityFeedRepository.swift`

| Function | Status |
|----------|--------|
| `getMyFeed` | ⬜ needs `begin_public_function` |

### `AmityStreamRepository` (1 functions)
> `EkoChat/Features/LiveStream/Public/Repositories/AmityStreamRepository.swift`

| Function | Status |
|----------|--------|
| `createStream` | ⬜ needs `begin_public_function` |

## Typescript (66 functions across 17 classes)

### `StoryRepository` (10 functions)
> `packages/sdk/src/storyRepository/api/createImageStory.ts`

| Function | Status |
|----------|--------|
| `createImageStory` | ⬜ needs `begin_public_function` |
| `createVideoStory` | ⬜ needs `begin_public_function` |
| `getActiveStoriesByTarget` | ⬜ needs `begin_public_function` |
| `getGlobalStoryTargets` | ⬜ needs `begin_public_function` |
| `getStoriesByTargetIds` | ⬜ needs `begin_public_function` |
| `getStoryByStoryId` | ⬜ needs `begin_public_function` |
| `getTargetById` | ⬜ needs `begin_public_function` |
| `getTargetsByTargetIds` | ⬜ needs `begin_public_function` |
| `hardDeleteStory` | ⬜ needs `begin_public_function` |
| `softDeleteStory` | ⬜ needs `begin_public_function` |

### `PostRepository` (8 functions)
> `packages/sdk/src/postRepository/api/deletePost.ts`

| Function | Status |
|----------|--------|
| `deletePost` | ⬜ needs `begin_public_function` |
| `generateCommentSubscriptions` | ⬜ needs `begin_public_function` |
| `getGlobalPinnedPosts` | ⬜ needs `begin_public_function` |
| `getPinnedPosts` | ⬜ needs `begin_public_function` |
| `getPost` | ⬜ needs `begin_public_function` |
| `preparePostResponse` | ⬜ needs `begin_public_function` |
| `queryPosts` | ⬜ needs `begin_public_function` |
| `semanticSearchPosts` | ⬜ needs `begin_public_function` |

### `SubChannelRepository` (8 functions)
> `packages/sdk/src/subChannelRepository/api/deleteSubChannel.ts`

| Function | Status |
|----------|--------|
| `deleteSubChannel` | ⬜ needs `begin_public_function` |
| `getSubChannel` | ⬜ needs `begin_public_function` |
| `getSubChannels` | ⬜ needs `begin_public_function` |
| `markAsReadBySegment` | ⬜ needs `begin_public_function` |
| `querySubChannels` | ⬜ needs `begin_public_function` |
| `readingAPI` | ⬜ needs `begin_public_function` |
| `startReadingAPI` | ⬜ needs `begin_public_function` |
| `stopReadingAPI` | ⬜ needs `begin_public_function` |

### `CommunityRepository` (7 functions)
> `packages/sdk/src/communityRepository/api/getCommunities.ts`

| Function | Status |
|----------|--------|
| `getCommunities` | ⬜ needs `begin_public_function` |
| `getCommunity` | ⬜ needs `begin_public_function` |
| `getJoinRequests` | ⬜ needs `begin_public_function` |
| `getTrendingCommunities` | ⬜ needs `begin_public_function` |
| `prepareSemanticCommunitiesReferenceId` | ⬜ needs `begin_public_function` |
| `queryCommunities` | ⬜ needs `begin_public_function` |
| `semanticSearchCommunities` | ⬜ needs `begin_public_function` |

### `ChannelRepository` (5 functions)
> `packages/sdk/src/channelRepository/api/deleteChannel.ts`

| Function | Status |
|----------|--------|
| `deleteChannel` | ⬜ needs `begin_public_function` |
| `getChannelByIds` | ⬜ needs `begin_public_function` |
| `getMyMembership` | ⬜ needs `begin_public_function` |
| `markChannelsAsReadBySegment` | ⬜ needs `begin_public_function` |
| `queryChannels` | ⬜ needs `begin_public_function` |

### `MessageRepository` (5 functions)
> `packages/sdk/src/messageRepository/api/deleteMessage.ts`

| Function | Status |
|----------|--------|
| `deleteMessage` | ⬜ needs `begin_public_function` |
| `getDeliveredUsers` | ⬜ needs `begin_public_function` |
| `getReadUsers` | ⬜ needs `begin_public_function` |
| `markAsDelivered` | ⬜ needs `begin_public_function` |
| `queryMessages` | ⬜ needs `begin_public_function` |

### `RoomRepository` (4 functions)
> `packages/sdk/src/roomRepository/api/analytics/WatchSessionStorage.ts`

| Function | Status |
|----------|--------|
| `convertToRoomEventPayload` | ⬜ needs `begin_public_function` |
| `getRoom` | ⬜ needs `begin_public_function` |
| `getWatchSessionStorage` | ⬜ needs `begin_public_function` |
| `syncWatchSessions` | ⬜ needs `begin_public_function` |

### `UserRepository` (4 functions)
> `packages/sdk/src/userRepository/api/getUser.ts`

| Function | Status |
|----------|--------|
| `getReachedUsers` | ⬜ needs `begin_public_function` |
| `getUser` | ⬜ needs `begin_public_function` |
| `queryBlockedUsers` | ⬜ needs `begin_public_function` |
| `queryUsers` | ⬜ needs `begin_public_function` |

### `EventRepository` (3 functions)
> `packages/sdk/src/eventRepository/observers/getEvents.ts`

| Function | Status |
|----------|--------|
| `getEvents` | ⬜ needs `begin_public_function` |
| `getMyEvents` | ⬜ needs `begin_public_function` |
| `getRSVPs` | ⬜ needs `begin_public_function` |

### `ReactionRepository` (3 functions)
> `packages/sdk/src/reactionRepository/api/constants.ts`

| Function | Status |
|----------|--------|
| `REFERENCE_API_V5` | ⬜ needs `begin_public_function` |
| `queryReactions` | ⬜ needs `begin_public_function` |
| `queryReactor` | ⬜ needs `begin_public_function` |

### `CommentRepository` (2 functions)
> `packages/sdk/src/commentRepository/api/getComment.ts`

| Function | Status |
|----------|--------|
| `getComment` | ⬜ needs `begin_public_function` |
| `queryComments` | ⬜ needs `begin_public_function` |

### `StreamRepository` (2 functions)
> `packages/sdk/src/streamRepository/api/disposeStream.ts`

| Function | Status |
|----------|--------|
| `disposeStream` | ⬜ needs `begin_public_function` |
| `getStreams` | ⬜ needs `begin_public_function` |

### `AdRepository` (1 functions)
> `packages/sdk/src/adRepository/api/getNetworkAds.ts`

| Function | Status |
|----------|--------|
| `getNetworkAds` | ⬜ needs `begin_public_function` |

### `FeedRepository` (1 functions)
> `packages/sdk/src/feedRepository/observers/utils.ts`

| Function | Status |
|----------|--------|
| `getGlobalFeedSubscriptions` | ⬜ needs `begin_public_function` |

### `FileRepository` (1 functions)
> `packages/sdk/src/fileRepository/api/fileUrlWithSize.ts`

| Function | Status |
|----------|--------|
| `fileUrlWithSize` | ⬜ needs `begin_public_function` |

### `InvitationRepository` (1 functions)
> `packages/sdk/src/invitationRepository/observers/getMyCommunityInvitations.ts`

| Function | Status |
|----------|--------|
| `getMyCommunityInvitations` | ⬜ needs `begin_public_function` |

### `LiveReactionRepository` (1 functions)
> `packages/sdk/src/liveReactionRepository/observers/getReactions.ts`

| Function | Status |
|----------|--------|
| `getReactions` | ⬜ needs `begin_public_function` |
