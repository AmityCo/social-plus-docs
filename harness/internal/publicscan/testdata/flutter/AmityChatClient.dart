class AmityChatClient {
  Future<String> createChannel(String channelId) async {
    return channelId;
  }

  Stream<List<String>> getMessages(String channelId) {
    return Stream.empty();
  }

  void _privateHelper() {}

  bool isConnected() {
    return false;
  }
}
