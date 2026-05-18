// preamble.kt — context for Android/Kotlin doc snippets.
// The extractor wraps each block inside a docSnippet function with these params in scope.
// Types verified against .docs-ops/sdk-surface/android.json.

import com.amity.socialcloud.sdk.api.core.AmityCoreClient
import com.amity.socialcloud.sdk.api.chat.AmityChatClient
import com.amity.socialcloud.sdk.api.social.AmitySocialClient
import com.amity.socialcloud.sdk.model.chat.channel.AmityChannel
import com.amity.socialcloud.sdk.model.chat.message.AmityMessage
import com.amity.socialcloud.sdk.model.social.post.AmityPost
import com.amity.socialcloud.sdk.model.social.community.AmityCommunity
import com.amity.socialcloud.sdk.model.social.comment.AmityComment
import com.amity.socialcloud.sdk.model.core.user.AmityUser
import com.amity.socialcloud.sdk.model.social.poll.AmityPoll

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
    channel: AmityChannel? = null,
    message: AmityMessage? = null,
    post: AmityPost? = null,
    comment: AmityComment? = null,
    community: AmityCommunity? = null,
    user: AmityUser? = null,
    poll: AmityPoll? = null
) {
    // <SNIPPET_BODY>
}
