#!/usr/bin/env python3
"""
extract-blocks.py (iOS) — Walk pages.json, extract every ```swift fenced code block,
wrap in a standalone async throws function, write one .swift file per block to
results/extracted/.

Handles:
  - ```swift fenced blocks (```objc / ```objective-c are skipped in v1)
  - Wrapped in: @available(iOS 14.0, *) func docSnippet_N(...) async throws { <BODY> }
  - enumerate: entries in pages.json resolved to all .mdx files in that directory
  - Skip markers: <!-- doc-as-test: skip --> or {/* doc-as-test: skip */}
  - Import hoisting: bare `import Foo` lines from block are lifted to file level
"""

import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
DOCS_ROOT = (SCRIPT_DIR / "../../..").resolve()  # social-plus-docs/
OUTPUT_DIR = SCRIPT_DIR / "results" / "extracted"
PAGES_JSON = SCRIPT_DIR / "pages.json"

FENCE_OPEN_RE = re.compile(r'^[ \t]*```swift\b.*$', re.IGNORECASE)
FENCE_CLOSE_RE = re.compile(r'^[ \t]*```\s*$')
SKIP_MARKER_RE = re.compile(r'doc-as-test:\s*skip(?:\s*\(([^)]*)\))?', re.IGNORECASE)
IMPORT_RE = re.compile(r"^\s*import\s+\S+")

PREAMBLE_IMPORTS = """\
import AmitySDK
import Foundation
import Combine
import UIKit
"""

# Stub helpers + global context vars (all at file scope, so local declarations inside
# doc snippet functions can shadow them without a redeclaration error)
SWIFT_STUBS = """\
// ── Shared context vars ───────────────────────────────────────────────────────
// AmitySDK v8+ repositories use init() — no client: parameter
let client = try! AmityClient(apiKey: "")
let channelRepository = AmityChannelRepository()
let messageRepository = AmityMessageRepository()
let postRepository = AmityPostRepository()
let commentRepository = AmityCommentRepository()
let communityRepository = AmityCommunityRepository()
let fileRepository = AmityFileRepository()
let userRepository = AmityUserRepository()
let feedRepository = AmityFeedRepository()
let storyRepository = AmityStoryRepository()
var token: AmityNotificationToken? = nil
let initialAccessToken: String = ""
let imageData = Data()
let channelId: String = ""
let userId: String = ""
let communityId: String = ""
let signature: String = ""
let expiresAt: Date? = Date()
let channelMembership = AmityChannelMembership(channelId: "")
let membershipParticipation = AmityChannelMembership(channelId: "")

// Mock SessionHandler (v8 protocol — no AmitySessionHandler type)
private final class _MockSessionHandler: SessionHandler {
    func sessionWillRenewAccessToken(renewal: any AccessTokenRenewal) {}
}
let sessionHandler: SessionHandler = _MockSessionHandler()

// ── Stub helpers for illustrative doc snippets ────────────────────────────────
@discardableResult
func showSuccessMessage(_ msg: Any = "") -> Void {}
func showErrorMessage(_ msg: Any = "", error: Error? = nil) {}
func handleError(_ error: Error) {}
func updateUI() {}
func presentError(_ error: Error) {}
func showLoadingIndicator(for _: Any = "") {}
func showSentIndicator(for _: Any = "") {}
func showRetryButton(for _: Any = "") {}
func showBannedWordError() {}
func handleGeneralError(_ error: Error) {}
func showInfo(_ msg: String) {}
func showRetryOption(_ msg: String) {}
func updateUIForSyncState(_ state: Any) {}
func displayUserList(_ users: Any) {}
func fetchNewTokenFromBackend(userId: String) async throws -> String { return "" }
func fetchAuthSignature(deviceId: String) async throws -> (String, Date?) { return (signature, expiresAt) }

// ── Upload placeholder stubs (edit-post doc snippets) ────────────────────────
let yourFile = AmityUploadableFile(fileData: Data(), fileName: nil)
let yourImage = UIImage()
let yourVideo = URL(fileURLWithPath: "")
"""


def resolve_pages(pages_json: Path, docs_root: Path) -> list[str]:
    """Resolve pages.json to a flat list of .mdx paths relative to docs_root."""
    with open(pages_json) as f:
        data = json.load(f)

    paths: list[str] = []
    for _section, entries in data.items():
        if _section in ("version", "selection_rationale"):
            continue
        if not isinstance(entries, list):
            continue
        for entry in entries:
            if entry.startswith("enumerate:"):
                dir_rel = entry[len("enumerate:"):]
                dir_abs = docs_root / dir_rel
                if dir_abs.is_dir():
                    for mdx in sorted(dir_abs.glob("*.mdx")):
                        paths.append(str(mdx.relative_to(docs_root)))
            else:
                paths.append(entry)
    return paths


def slug_from_path(rel_path: str) -> str:
    return rel_path.replace("/", "__").replace(".mdx", "").replace(" ", "-")


def extract_blocks(mdx_path: Path) -> list[tuple[str, bool]]:
    """
    Returns list of (block_body, skip) tuples. block_body is the raw lines of the block.
    skip is True if preceded by a skip marker within 3 lines.
    """
    if not mdx_path.exists():
        return []

    lines = mdx_path.read_text(encoding="utf-8").errors("replace" if False else "strict").splitlines() if False else mdx_path.read_text(encoding="utf-8", errors="replace").splitlines()
    blocks = []
    in_block = False
    current_lines: list[str] = []
    pending_skip = False

    for i, line in enumerate(lines):
        if not in_block:
            # Check skip marker in recent lines
            if SKIP_MARKER_RE.search(line):
                pending_skip = True
                continue
            if FENCE_OPEN_RE.match(line):
                in_block = True
                current_lines = []
            else:
                # Reset skip if we've gone 3+ lines without opening a fence
                if pending_skip:
                    # check if any of the last 3 lines were a skip marker
                    look_back = lines[max(0, i-3):i]
                    if not any(SKIP_MARKER_RE.search(l) for l in look_back):
                        pending_skip = False
        else:
            if FENCE_CLOSE_RE.match(line):
                in_block = False
                blocks.append(("\n".join(current_lines), pending_skip))
                current_lines = []
                pending_skip = False
            else:
                current_lines.append(line)

    return blocks


def wrap_block(block_body: str, fn_name: str) -> tuple[str, list[str]]:
    """
    Wrap block in async throws function. Hoist import statements to file level.
    Returns (file_content, hoisted_imports).
    """
    body_lines = block_body.splitlines()
    hoisted: list[str] = []
    kept: list[str] = []

    for line in body_lines:
        if IMPORT_RE.match(line):
            hoisted.append(line.strip())
        else:
            kept.append(line)

    body = "\n".join(f"    {l}" for l in kept)

    content = f"""{PREAMBLE_IMPORTS}
"""
    if hoisted:
        content += "\n".join(hoisted) + "\n\n"

    content += SWIFT_STUBS + "\n"
    content += f"@available(iOS 14.0, *)\nfunc {fn_name}() async throws {{\n{body}\n}}\n"
    return content, hoisted


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Remove old extracted files
    for old in OUTPUT_DIR.glob("*.swift"):
        old.unlink()
    manifest_path = OUTPUT_DIR / "_manifest.json"
    if manifest_path.exists():
        manifest_path.unlink()

    pages = resolve_pages(PAGES_JSON, DOCS_ROOT)
    manifest: list[dict] = []
    total_extracted = 0
    total_skipped = 0

    for rel_path in pages:
        abs_path = DOCS_ROOT / rel_path
        if not abs_path.exists():
            print(f"  MISSING: {rel_path}", file=sys.stderr)
            continue

        slug = slug_from_path(rel_path)
        blocks = extract_blocks(abs_path)
        block_idx = 0

        for body, skip in blocks:
            block_idx += 1
            fn_name = f"docSnippet_{slug.replace('-', '_')}_{block_idx}"
            out_name = f"{slug}-block-{block_idx}.swift"
            out_path = OUTPUT_DIR / out_name

            if skip:
                total_skipped += 1
                manifest.append({
                    "file": out_name,
                    "source_page": rel_path,
                    "block_index": block_idx,
                    "status": "skipped",
                    "fn_name": fn_name,
                })
                continue

            content, hoisted = wrap_block(body, fn_name)
            out_path.write_text(content, encoding="utf-8")
            total_extracted += 1
            manifest.append({
                "file": out_name,
                "source_page": rel_path,
                "block_index": block_idx,
                "status": "extracted",
                "fn_name": fn_name,
                "hoisted_imports": hoisted,
            })

    manifest_path.write_text(json.dumps(manifest, indent=2))

    print(f"Extracted {total_extracted} blocks ({total_skipped} skipped) from {len(pages)} pages")
    print(f"Output: {OUTPUT_DIR}")
    return total_extracted


if __name__ == "__main__":
    main()
