// source: social-plus-sdk/core-concepts/content-handling/files-images-and-videos/file.mdx:148-173
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

  void uploadFile(File uploadingFile) async {
    AmityCoreClient.newFileRepository()
        .uploadFile(uploadingFile)
        .stream
        .listen((AmityUploadResult<AmityFile> amityUploadResult) {
      amityUploadResult.when(
        progress: (uploadInfo, cancelToken) {
          int progress = uploadInfo.getProgressPercentage();
        },
        complete: (file) {
          //check if the upload result is complete

          final AmityFile uploadedFile = file;
          //proceed result with uploadedFile
        },
        error: (error) {
          final AmityException amityException = error;
          //handle error
        },
        cancel: () {
          //upload is cancelled
        },
      );
    });
  }
}
