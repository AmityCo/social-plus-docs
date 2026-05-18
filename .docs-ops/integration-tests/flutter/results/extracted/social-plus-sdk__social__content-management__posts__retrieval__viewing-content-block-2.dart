// source: social-plus-sdk/social/content-management/posts/retrieval/viewing-content.mdx:321-330
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
  void getImage(AmityPost post) {
    final AmityPostData? amityPostData = post.data;
    if (amityPostData != null) {
      final imageData = amityPostData as ImageData;
      //for large image url
      final largeImageUrl = imageData.getUrl(AmityImageSize.LARGE);
      //for small image url
      final smallImageUrl = imageData.getUrl(AmityImageSize.SMALL);
    }
  }
}
