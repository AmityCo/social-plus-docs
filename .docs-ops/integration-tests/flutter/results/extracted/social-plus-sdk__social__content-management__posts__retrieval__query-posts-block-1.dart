// source: social-plus-sdk/social/content-management/posts/retrieval/query-posts.mdx:274-309
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
  late PostLiveCollection postLiveCollection;
  List<AmityPost> amityPosts = [];
  final scrollcontroller = ScrollController();

  void observePosts(String userId) {
    //initialize post live collection
    postLiveCollection = AmitySocialClient.newPostRepository()
        .getPosts()
        .targetUser(userId)
        .getLiveCollection(pageSize: 20);

    //listen to data changes from live collection
    postLiveCollection.getStreamController().stream.listen((event) {
      // update latest results here
      // setState(() {
      amityPosts = event;
      // });
    });

    //load first page when initiating widget
    postLiveCollection.loadNext();

    //add pagination listener when srolling to top/bottom
    scrollcontroller.addListener(paginationListener);
  }

  void paginationListener() {
    //check if
    //#1 scrolling reached top/bottom
    //#2 live collection has next page to load more
    if ((scrollcontroller.position.pixels ==
            (scrollcontroller.position.maxScrollExtent)) &&
        postLiveCollection.hasNextPage()) {
      postLiveCollection.loadNext();
    }
  }
}
