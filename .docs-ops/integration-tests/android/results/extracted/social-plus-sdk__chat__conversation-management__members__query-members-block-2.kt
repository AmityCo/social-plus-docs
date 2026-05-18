// source: social-plus-sdk/chat/conversation-management/members/query-members.mdx:190-199
import com.amity.socialcloud.sdk.api.core.AmityCoreClient
import com.amity.socialcloud.sdk.api.chat.AmityChatClient
import com.amity.socialcloud.sdk.api.social.AmitySocialClient
import com.amity.socialcloud.sdk.api.chat.channel.AmityChannelRepository
import com.amity.socialcloud.sdk.api.chat.message.AmityMessageRepository
import com.amity.socialcloud.sdk.api.social.post.AmityPostRepository
import com.amity.socialcloud.sdk.api.core.user.AmityUserRepository
import com.amity.socialcloud.sdk.api.core.file.AmityFileRepository
import com.amity.socialcloud.sdk.model.chat.channel.AmityChannel
import com.amity.socialcloud.sdk.model.chat.channel.AmityChannelFilter
import com.amity.socialcloud.sdk.model.chat.message.AmityMessage
import com.amity.socialcloud.sdk.model.chat.member.AmityChannelMember
import com.amity.socialcloud.sdk.model.chat.member.AmityMembershipType
import com.amity.socialcloud.sdk.model.chat.notification.AmityChannelNotificationSettings
import com.amity.socialcloud.sdk.model.social.post.AmityPost
import com.amity.socialcloud.sdk.model.social.community.AmityCommunity
import com.amity.socialcloud.sdk.model.social.comment.AmityComment
import com.amity.socialcloud.sdk.model.social.notification.AmityCommunityNotificationSettings
import com.amity.socialcloud.sdk.model.social.notification.AmityCommunityNotificationEvent
import com.amity.socialcloud.sdk.model.core.user.AmityUser
import com.amity.socialcloud.sdk.model.social.poll.AmityPoll
import com.amity.socialcloud.sdk.model.core.file.AmityImage
import com.amity.socialcloud.sdk.model.core.file.AmityFile
import com.amity.socialcloud.sdk.model.core.file.AmityVideo
import com.amity.socialcloud.sdk.model.core.file.AmityVideoResolution
import com.amity.socialcloud.sdk.model.core.file.AmityRawFile
import com.amity.socialcloud.sdk.model.core.file.AmityFileType
import com.amity.socialcloud.sdk.model.core.file.upload.AmityUploadResult
import com.amity.socialcloud.sdk.model.core.tag.AmityTags
import com.amity.socialcloud.sdk.model.core.pin.AmityPinnedPost
import com.amity.socialcloud.sdk.model.core.error.AmityException
import com.amity.socialcloud.sdk.model.core.error.AmityError
import com.amity.socialcloud.sdk.model.core.link.AmityLink
import com.amity.socialcloud.sdk.model.core.role.AmityRoles
import com.amity.socialcloud.sdk.model.core.notification.AmityRolesFilter
import com.amity.socialcloud.sdk.model.core.notification.AmityUserNotificationModule
import com.amity.socialcloud.sdk.model.core.producttag.AmityProductTag
import com.amity.socialcloud.sdk.model.core.producttag.AmityAttachmentProductTags
import com.amity.socialcloud.sdk.model.core.content.AmityContentFeedType
import com.amity.socialcloud.sdk.model.core.session.SessionHandler
import com.amity.socialcloud.sdk.model.core.session.AccessTokenHandler
import com.google.gson.JsonObject
import com.amity.socialcloud.sdk.model.video.room.AmityRoom
import com.amity.socialcloud.sdk.model.video.room.AmityRoomStatus
import com.amity.socialcloud.sdk.model.video.stream.AmityStream
import com.amity.socialcloud.sdk.api.core.endpoint.AmityEndpoint
import com.amity.socialcloud.sdk.api.core.encryption.AmityDBEncryption
import com.amity.socialcloud.sdk.api.core.session.AmityAccessTokenEstablisher
import com.amity.socialcloud.sdk.api.core.token.AmityUserTokenManager
import com.amity.socialcloud.sdk.api.core.user.notification.AmityUserNotification
import com.amity.socialcloud.sdk.helper.core.asAmityFile
import com.amity.socialcloud.sdk.helper.core.asAmityImage
import com.amity.socialcloud.sdk.helper.core.asAmityVideo
import com.amity.socialcloud.sdk.api.social.post.query.AmityUserFeedSortOption
import com.amity.socialcloud.sdk.api.social.post.query.AmityCommunityFeedSortOption
import com.amity.socialcloud.sdk.api.social.post.review.AmityReviewStatus
import com.amity.socialcloud.sdk.api.chat.member.query.AmityChannelMembershipFilter
import com.amity.socialcloud.sdk.api.chat.member.query.AmityChannelMembershipSortOption
import com.amity.socialcloud.sdk.core.session.model.SessionState
import com.amity.socialcloud.sdk.core.session.AccessTokenRenewal
import androidx.paging.PagingData
import io.reactivex.rxjava3.android.schedulers.AndroidSchedulers
import io.reactivex.rxjava3.schedulers.Schedulers
import io.reactivex.rxjava3.core.Completable
import io.reactivex.rxjava3.core.Flowable
import io.reactivex.rxjava3.core.Observable
import android.app.Application
import android.content.Context
import android.net.Uri
import android.util.Log
import java.util.Calendar

// Stubs for illustrative helper functions used in doc snippets
@Suppress("UNUSED_PARAMETER")
fun showSuccessMessage(msg: Any = "") {}
@Suppress("UNUSED_PARAMETER")
fun showErrorMessage(msg: Any = "", error: Throwable? = null) {}
@Suppress("UNUSED_PARAMETER")
fun notifyMessageDeleted(id: String = "") {}
@Suppress("UNUSED_PARAMETER")
fun notifyFailedMessagesCleared() {}
@Suppress("UNUSED_PARAMETER")
fun handleFlagSuccess(id: String = "", reason: Any? = null) {}
@Suppress("UNUSED_PARAMETER")
fun handleFlagError(error: Throwable? = null, id: String = "") {}
@Suppress("UNUSED_PARAMETER")
fun handleUnflagSuccess(id: String = "") {}
@Suppress("UNUSED_PARAMETER")
fun handleUnflagError(error: Throwable? = null, id: String = "") {}
@Suppress("UNUSED_PARAMETER")
fun handleBulkDeletionError(error: Throwable? = null) {}
@Suppress("UNUSED_PARAMETER")
fun handleDeletionError(error: Throwable? = null) {}
@Suppress("UNUSED_PARAMETER")
fun handleNetworkError(error: Throwable? = null) {}
@Suppress("UNUSED_PARAMETER")
fun proceedWithNormalOperation() {}
@Suppress("UNUSED_PARAMETER")
fun setup(client: Any? = null) {}
@Suppress("UNUSED_PARAMETER")
fun showLogin() {}
@Suppress("UNUSED_PARAMETER")
fun showBannedWordError(msg: Any = "") {}
@Suppress("UNUSED_PARAMETER")
fun handleGeneralError(error: Throwable? = null) {}
@Suppress("UNUSED_PARAMETER")
fun getPagingData(adapter: Any? = null) {}
@Suppress("UNUSED_PARAMETER")
fun deletePost(id: Any? = null) {}
@Suppress("UNUSED_PARAMETER")
fun updateUserProfile(user: Any? = null) {}
@Suppress("UNUSED_PARAMETER")
fun authenticateToSocialPlus(userId: String = "") {}
@Suppress("UNUSED_PARAMETER")
fun showUnflagSuccessMessage() {}
@Suppress("UNUSED_PARAMETER")
fun updateMessageUI(id: String = "", isFlagged: Boolean = false) {}

@Suppress("UNUSED_VARIABLE", "UNUSED_PARAMETER", "NAME_SHADOWING", "UNREACHABLE_CODE")
fun docSnippet(
    apiKey: String = "",
    userId: String = "user-id",
    displayName: String = "User",
    authToken: String = "token",
    channelId: String = "channel-id",
    subChannelId: String = "sub-channel-id",
    messageId: String = "message-id",
    postId: String = "post-id",
    communityId: String = "community-id",
    commentId: String = "comment-id",
    pollId: String = "poll-id",
    fileId: String = "file-id",
    targetUserId: String = "target-user-id",
    channelRepository: AmityChannelRepository = AmityChatClient.newChannelRepository(),
    messageRepository: AmityMessageRepository = AmityChatClient.newMessageRepository(),
    postRepository: AmityPostRepository = AmitySocialClient.newPostRepository(),
    sessionHandler: SessionHandler? = null,
    channel: AmityChannel? = null,
    message: AmityMessage? = null,
    post: AmityPost? = null,
    comment: AmityComment? = null,
    community: AmityCommunity? = null,
    user: AmityUser? = null,
    poll: AmityPoll? = null,
    amityImage: AmityImage? = null
) {
        // Query members by status with role filtering
        channelRepository.membership(channelId = channelId)
            .getMembers()
            .filter(filter = AmityChannelMembershipFilter.MEMBER)
            .roles(roles = listOf("moderator", "admin"))
            .includeDeleted(includeDeleted = false)
            .sortBy(sortOption = AmityChannelMembershipSortOption.LAST_CREATED)
            .build()
            .query()
            .subscribe()
}
