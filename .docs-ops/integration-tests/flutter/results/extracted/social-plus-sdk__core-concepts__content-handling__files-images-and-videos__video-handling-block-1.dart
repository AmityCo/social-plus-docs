// source: social-plus-sdk/core-concepts/content-handling/files-images-and-videos/video-handling.mdx:159-179
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
  void uploadVideo(File uploadingVideo) async {
    AmityCoreClient.newFileRepository()
        .uploadVideo(uploadingVideo , feedtype: AmityContentFeedType.POST)
        .stream
        .listen((AmityUploadResult<AmityVideo> amityResult) {
      amityResult.when(
        progress: (uploadInfo, cancelToken) {},
        complete: (file) {
          //handle result
          AmityVideo uploadedVideo = file;
        },
        error: (error) {
          final AmityException amityException = error;
          // handle error
        },
        cancel: () {
          // handle cancel request
        },
      );
    });
  }
}
