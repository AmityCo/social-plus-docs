// source: social-plus-sdk/social/content-management/posts/retrieval/viewing-content.mdx:191-219
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
  void getPost(String postId) {
    AmitySocialClient.newPostRepository()
        .getPost(postId)
        .then((AmityPost post) {
      //parent post text is always TextData
      //from this line you can get the post's text data
      //eg 'Hello bob'
      final textContent = post.data as TextData;
      final childrenPosts = post.children;
      //check if the chidren posts exist in the parent post
      if (childrenPosts?.isNotEmpty == true) {
        childrenPosts?.forEach((AmityPost childPost) {
          //check if the current child post is an image post
          if (childPost.type == AmityDataType.IMAGE) {
            //if the current child post is an image post,
            //we can cast its data to ImageData
            final AmityPostData? amityPostData = childPost.data;
            if (amityPostData != null) {
              final imageData = amityPostData as ImageData;
              //to get the full image url without transcoding
              final largeImageUrl = imageData.getUrl(AmityImageSize.FULL);
            }
          }
        });
      }
    }).onError((error, stackTrace) {
      //handle error
    });
  }
}
