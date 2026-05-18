// source: social-plus-sdk/chat/conversation-management/channels/query-channels.mdx:126-148
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
      List<AmityChannel> _amityChannel = <AmityChannel>[];
      late ChannelLiveCollection liveCollection;
      final scrollcontroller = ScrollController();

      // Available Channel Type options
      // AmityChannelType.COMMUNITY;
      // AmityChannelType.LIVE;
      // AmityChannelType.BROADCAST;
      // AmityChannelType.CONVERSATION;

      void queryChannels() {
        // Query for Multiple types
        final types = <AmityChannelType>[
          AmityChannelType.LIVE,
          AmityChannelType.COMMUNITY
        ];
        liveCollection = AmityChatClient.newChannelRepository()
          .getChannels()
          .types(types)
          .excludeArchives(true) // boolean value to exclude archived channels, default is false
          .getLiveCollection(); 

      }
}
