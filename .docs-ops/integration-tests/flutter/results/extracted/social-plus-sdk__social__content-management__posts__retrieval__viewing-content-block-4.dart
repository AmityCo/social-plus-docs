// source: social-plus-sdk/social/content-management/posts/retrieval/viewing-content.mdx:577-590
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
  void getVideo(AmityPost post) {
    final AmityPostData? amityPostData = post.data;
    if (amityPostData != null) {
      final videoData = amityPostData as VideoData;
      //for high quality video
      videoData.getVideo(AmityVideoQuality.HIGH).then((AmityVideo video) {
        //handle result
      });
      //for low quality video
      videoData.getVideo(AmityVideoQuality.LOW).then((AmityVideo video) {
        //handle result
      });
    }
  }
}
