// source: social-plus-sdk/core-concepts/user-management/user-operations/get-user-information.mdx:221-255
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
  final userRepo = AmityCoreClient.newUserRepository();

  // Get a single user by ID
  Future<AmityUser?> getSingleUser(String userId) async {
    try {
      final user = await userRepo.getUser(userId);
      print('User: ${user.displayName}');
      return user;
    } catch (error) {
      print('Error getting user: $error');
      return null;
    }
  }

  // Get multiple users by ID — fetch individually (no batch API)
  Future<List<AmityUser>> getUsersByIds(List<String> userIds) async {
    final users = <AmityUser>[];
    for (final id in userIds) {
      try {
        final user = await userRepo.getUser(id);
        users.add(user);
      } catch (error) {
        print('Error getting user $id: $error');
      }
    }
    return users;
  }

  // Get all users with live updates
  final liveCollection = userRepo.getUsers().getLiveCollection();
  liveCollection.getStreamController().stream.listen((userList) {
    for (final user in userList) {
      print('User: ${user.displayName}, ID: ${user.userId}');
    }
  });
}
