class AmityChannelCreationCommunity {
  /* begin_sample_code
    gist_id: 419b175b2bc54175b29d42c36c346409
    filename: AmityChannelCreationCommunity.dart
    asc_page: social-plus-sdk/chat/conversation-management/channels/create-channel
    description: Flutter create community channel example
    */
  void createCommunityChannel() {
    AmityChatClient.newChannelRepository()
        .createChannel()
        .communityType()
        .create();
  }
  /* end_sample_code */
}
