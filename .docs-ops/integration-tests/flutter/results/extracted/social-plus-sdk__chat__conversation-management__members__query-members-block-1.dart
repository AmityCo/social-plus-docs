// source: social-plus-sdk/chat/conversation-management/members/query-members.mdx:131-156
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
      final _amityChannelMembers = <AmityChannelMember>[];
      late PagingController<AmityChannelMember> _channelMembersController;

      void queryChannelMembers(String channelId, String keyword) {
        _channelMembersController = PagingController(
          pageFuture: (token) => AmityChatClient.newChannelRepository()
              .membership(channelId)
              .searchMembers(keyword)
              .includeDeleted(false) // optional to filter deleted users from the result
              .getPagingData(token: token, limit: 20),
          pageSize: 20,
        )..addListener(
            () {
              if (_channelMembersController.error == null) {
                //handle results, we suggest to clear the previous items
                //and add with the latest _controller.loadedItems
                _amityChannelMembers.clear();
                _amityChannelMembers.addAll(_channelMembersController.loadedItems);
                //update widgets
              } else {
                //error on pagination controller
                //update widgets
              }
            },
          );
      }
}
