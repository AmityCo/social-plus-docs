class AmityChannelCreationCommunity {
  /* begin_sample_code
    filename: AmityChannelCreationCommunity.dart
    sp_docs_page: social-plus-sdk/chat/conversation-management/channels/create-channel
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
