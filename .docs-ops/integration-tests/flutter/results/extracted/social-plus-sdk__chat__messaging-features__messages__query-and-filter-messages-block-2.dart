// source: social-plus-sdk/chat/messaging-features/messages/query-and-filter-messages.mdx:258-272
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
      void observeThreadMessages(String channelId, String parentId) {
        messageLiveCollection = AmityChatClient.newMessageRepository()
            .getMessages(channelId)
            .parentId(parentId) // Filter by parent message
            .stackFromEnd(true)
            .getLiveCollection(pageSize: 20);

        messageLiveCollection.getStreamController().stream.listen((event) {
          setState(() {
            amityMessages = event;
          });
        });

        messageLiveCollection.loadNext();
      }
}
