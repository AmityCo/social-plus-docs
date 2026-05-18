// source: social-plus-sdk/core-concepts/user-management/user-operations/update-user-information.mdx:82-96
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
  // Update user profile information
  Future<void> updateUser() async {
      try {
          final user = await AmityCoreClient.newUserRepository()
              .updateUser('userId')
              .displayName('Batman')
              .description('Hero that Gotham needs')
              .avatarFileId(avatarFileId)
              .update();

          print('User updated: ${user.displayName}');
      } on AmityException catch (error) {
          print('Update failed: ${error.message}');
      }
  }
}
