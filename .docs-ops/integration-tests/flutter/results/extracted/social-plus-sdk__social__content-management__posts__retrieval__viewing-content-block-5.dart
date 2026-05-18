// source: social-plus-sdk/social/content-management/posts/retrieval/viewing-content.mdx:700-723
// ignore_for_file: unused_local_variable, unused_import, dead_code
import 'package:amity_sdk/amity_sdk.dart';

// Stub functions for illustrative UI pseudocode in doc snippets
void showLoginScreen() {}
void showLoadingIndicator() {}
void hideLoadingIndicator() {}
void proceedToApp() {}
void showTokenRefreshIndicator() {}
void handleSessionTermination() {}
void showError(Object e) {}

Future<void> docSnippet({
  String apiKey = 'key',
  String region = 'sg',
  String userId = 'user-id',
  String displayName = 'User',
  String authToken = 'token',
  String channelId = 'channel-id',
  String subChannelId = 'sub-channel-id',
  String messageId = 'message-id',
  String postId = 'post-id',
  String communityId = 'community-id',
  String commentId = 'comment-id',
  String pollId = 'poll-id',
  String fileId = 'file-id',
  String targetUserId = 'target-user-id',
}) async {
  void getPollPost(AmityPost post) {
    //parent post text is always TextData
    //from this line you can get the post's text data
    //eg 'What are your favorite songs?'
    final textContent = post.data as TextData;
    final childrenPosts = post.children;
    //check if the chidren posts exist in the parent post
    if (childrenPosts?.isNotEmpty == true) {
      childrenPosts?.forEach((AmityPost childPost) {
        //check if the current child post is an poll post
        if (childPost.type == AmityDataType.POLL) {
          //if the current child post is an poll post,
          //we can cast its data to PollData
          final AmityPostData? amityPostData = childPost.data;
          if (amityPostData != null) {
            final pollData = amityPostData as PollData;
            pollData.getPoll().then((AmityPoll poll) {
              //handle poll data here
            });
          }
        }
      });
    }
  }
}
