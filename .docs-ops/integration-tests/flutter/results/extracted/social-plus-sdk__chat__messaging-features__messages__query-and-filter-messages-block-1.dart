// source: social-plus-sdk/chat/messaging-features/messages/query-and-filter-messages.mdx:140-171
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
      late MessageLiveCollection messageLiveCollection;
      List<AmityMessage> amityMessages = [];
      final scrollController = ScrollController();

      void observeMessages(String channelId) {
        // Initialize message live collection
        messageLiveCollection = AmityChatClient.newMessageRepository()
            .getMessages(channelId)
            .stackFromEnd(true) // Latest messages at bottom
            .getLiveCollection(pageSize: 20);

        // Listen to real-time data changes
        messageLiveCollection.getStreamController().stream.listen((event) {
          setState(() {
            amityMessages = event;
          });
        });

        // Load initial page
        messageLiveCollection.loadNext();

        // Setup pagination listener
        scrollController.addListener(paginationListener);
      }

      void paginationListener() {
        if ((scrollController.position.pixels >=
                (scrollController.position.maxScrollExtent - 100)) &&
            messageLiveCollection.hasNextPage()) {
          messageLiveCollection.loadNext();
        }
      }
}
