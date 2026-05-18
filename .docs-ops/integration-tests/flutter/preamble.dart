// preamble.dart — Context variables for doc snippet type-checking.
// NOT used directly; the extractor wraps each extracted block in a
// function that has these parameters in scope.
//
// Types verified against .docs-ops/sdk-surface/flutter.json before declaring.
// ITERATION NOTE: Add missing declarations as failures surface.
import 'package:amity_sdk/amity_sdk.dart';

// ignore_for_file: unused_element, unused_local_variable

Future<void> docSnippet({
  // Setup
  required String apiKey,
  required String region,
  required String userId,
  required String displayName,
  required String authToken,
  // Chat context
  required String channelId,
  required String subChannelId,
  required String messageId,
  required AmityChannel channel,
  required AmityMessage message,
  // Social context
  required String postId,
  required String communityId,
  required String commentId,
  required String pollId,
  required AmityPost post,
  required AmityComment comment,
  required AmityCommunity community,
  // User
  required String targetUserId,
  required AmityUser user,
  // File / media
  required String fileId,
}) async {
  // <SNIPPET_BODY> (extractor inserts each block here)
}
