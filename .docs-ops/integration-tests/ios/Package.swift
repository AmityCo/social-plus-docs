// swift-tools-version: 5.9
// NOTE: This Package.swift is present for documentation purposes.
// The actual doc-as-test compilation uses `swiftc -typecheck` directly
// (see run-tests.py) against the AmitySDK.xcframework binary cached in vendor/.
//
// To build with SPM instead (Option B):
//   swift package resolve && swift build --target DocSnippets
// Currently blocked by SwiftPM git libgit2 safe.bareRepository issue on this host.
//
// Option C (active): swiftc -typecheck per block — 0.2s per snippet, no SPM needed.
import PackageDescription

let package = Package(
    name: "docs-ops-ios-snippets",
    platforms: [.iOS(.v14)],
    products: [],
    targets: []
)
