// preamble.swift — context for iOS doc snippets.
// The extractor wraps each block in a function with these parameters in scope.
// Every type here has been verified against .docs-ops/sdk-surface/ios.json and
// against the published AmitySDK 8.1.1 xcframework swiftinterface.
import AmitySDK
import Foundation
import Combine

// Stub helpers used in illustrative doc snippets so they compile without
// any real application infrastructure.
func showSuccessMessage(_ msg: Any = "") {}
func showErrorMessage(_ msg: Any = "", error: Error? = nil) {}
func handleError(_ error: Error) {}
func updateUI() {}
func presentError(_ error: Error) {}

@available(iOS 14.0, *)
func docSnippet(
    apiKey: String = "",
    region: AmityRegion = .SG,
    userId: String = "",
    displayName: String = "",
    channelId: String = "",
    subChannelId: String = "",
    messageId: String = "",
    postId: String = "",
    communityId: String = "",
    commentId: String = "",
    pollId: String = "",
    fileId: String = "",
    client: AmityClient? = nil,
    channel: AmityChannel? = nil,
    message: AmityMessage? = nil,
    post: AmityPost? = nil,
    comment: AmityComment? = nil,
    community: AmityCommunity? = nil,
    storyRepository: AmityStoryRepository = AmityStoryRepository(),
    user: AmityUser? = nil
) async throws {
    // <SNIPPET_BODY> inserted here by extractor
}
