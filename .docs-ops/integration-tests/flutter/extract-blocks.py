#!/usr/bin/env python3
"""
extract-blocks.py (Flutter) — Walk pages.json, extract every ```dart fenced code block,
wrap in preamble function body, write one .dart file per block into results/extracted/.

Handles:
  - Only ```dart fenced blocks (not typescript/js/etc.)
  - Indented blocks inside MDX components (<Tab>, <Step>, <Accordion>)
  - enumerate: entries in pages.json
  - Skip markers: <!-- doc-as-test: skip --> or {/* doc-as-test: skip */}
  - Hoists import statements from block body to file-level (above the wrapper)
"""

import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
DOCS_ROOT = (SCRIPT_DIR / "../../..").resolve()  # social-plus-docs/
OUTPUT_DIR = SCRIPT_DIR / "results" / "extracted"
PAGES_JSON = SCRIPT_DIR / "pages.json"

FENCE_OPEN_RE = re.compile(r'^[ \t]*```dart\b.*$', re.IGNORECASE)
FENCE_CLOSE_RE = re.compile(r'^[ \t]*```\s*$')
SKIP_MARKER_RE = re.compile(r'doc-as-test:\s*skip(?:\s*\(([^)]*)\))?', re.IGNORECASE)
IMPORT_RE = re.compile(r"^\s*import\s+['\"].*?['\"]")

PREAMBLE_PARAMS = """\
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
  String targetUserId = 'target-user-id',"""


def resolve_pages(pages_data):
    paths = []
    all_entries = (
        pages_data.get("flutter_specific", [])
        + pages_data.get("audited_root", [])
        + pages_data.get("audited_getting_started", [])
        + pages_data.get("audited_user_management", [])
        + pages_data.get("audited_social_entry", [])
        + pages_data.get("audited_community_lifecycle", [])
        + pages_data.get("chat_track", [])
        + pages_data.get("social_track", [])
        + pages_data.get("shared", [])
    )
    for entry in all_entries:
        if entry.startswith("enumerate:"):
            dir_path = DOCS_ROOT / entry[len("enumerate:"):]
            if dir_path.is_dir():
                for mdx in sorted(dir_path.glob("*.mdx")):
                    paths.append(str(mdx.relative_to(DOCS_ROOT)))
            else:
                print(f"  WARN: enumerate dir not found: {dir_path}", file=sys.stderr)
        else:
            full = DOCS_ROOT / entry
            if full.exists():
                paths.append(entry)
            else:
                print(f"  WARN: page not found: {entry}", file=sys.stderr)
    # Deduplicate while preserving order
    seen = set()
    deduped = []
    for p in paths:
        if p not in seen:
            seen.add(p)
            deduped.append(p)
    return deduped


def extract_blocks(page_path):
    """Returns (extracted_blocks, skipped_blocks)."""
    full_path = DOCS_ROOT / page_path
    text = full_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    extracted = []
    skipped = []
    in_block = False
    block_lines = []
    block_start = 0
    skip_mode = False
    pending_skip = None

    for i, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not in_block:
            skip_m = SKIP_MARKER_RE.search(stripped) if stripped else None
            if skip_m:
                pending_skip = skip_m.group(1) or "skip"
            elif stripped:
                if FENCE_OPEN_RE.match(line):
                    if pending_skip is not None:
                        skipped.append({"file": page_path, "line": i, "reason": pending_skip})
                        in_block = True
                        skip_mode = True
                        block_lines = []
                        block_start = 0
                    else:
                        in_block = True
                        skip_mode = False
                        block_lines = []
                        block_start = i + 1
                    pending_skip = None
                else:
                    pending_skip = None
        else:
            if FENCE_CLOSE_RE.match(line):
                if not skip_mode and block_start != 0 and block_lines:
                    extracted.append({
                        "content": "\n".join(block_lines),
                        "start_line": block_start,
                        "end_line": i - 1,
                    })
                in_block = False
                skip_mode = False
                block_lines = []
                block_start = 0
            else:
                block_lines.append(line)

    return extracted, skipped


def page_to_slug(page_path):
    return page_path.replace("/", "__").replace(".mdx", "")


def split_imports(content):
    """Split block content into (imports, body). Imports are hoisted to file level."""
    import_lines = []
    body_lines = []
    for line in content.splitlines():
        if IMPORT_RE.match(line):
            import_lines.append(line.rstrip())
        else:
            body_lines.append(line)
    return "\n".join(import_lines), "\n".join(body_lines)


def write_block(slug, block_index, block, page_path):
    filename = f"{slug}-block-{block_index}.dart"
    out_path = OUTPUT_DIR / filename

    imports_str, body = split_imports(block["content"])

    # Deduplicate with the base import
    extra_imports = []
    for imp in imports_str.splitlines():
        imp = imp.strip()
        if imp and "package:amity_sdk/amity_sdk.dart" not in imp:
            extra_imports.append(imp)

    source_comment = f"// source: {page_path}:{block['start_line']}-{block['end_line']}"
    extra_import_block = ("\n" + "\n".join(extra_imports)) if extra_imports else ""

    # Indent body by 2 spaces for function wrapper
    indented_body = "\n".join("  " + l if l.strip() else "" for l in body.splitlines())

    content = f"""{source_comment}
// ignore_for_file: unused_local_variable, unused_import, dead_code
import 'package:amity_sdk/amity_sdk.dart';{extra_import_block}

// Stub functions for illustrative UI pseudocode in doc snippets
void showLoginScreen() {{}}
void showLoadingIndicator() {{}}
void hideLoadingIndicator() {{}}
void proceedToApp() {{}}
void showTokenRefreshIndicator() {{}}
void handleSessionTermination() {{}}
void showError(Object e) {{}}

Future<void> docSnippet({{
{PREAMBLE_PARAMS}
}}) async {{
{indented_body}
}}
"""
    out_path.write_text(content, encoding="utf-8")
    return out_path


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for old in OUTPUT_DIR.glob("*.dart"):
        old.unlink()

    pages_data = json.loads(PAGES_JSON.read_text())
    pages = resolve_pages(pages_data)

    total_extracted = 0
    total_skipped = 0
    page_stats = {}
    all_skipped = []

    print(f"Extracting dart blocks from {len(pages)} pages...")
    for page_path in pages:
        ext, skp = extract_blocks(page_path)
        slug = page_to_slug(page_path)
        for i, block in enumerate(ext, start=1):
            write_block(slug, i, block, page_path)
        all_skipped.extend(skp)
        page_stats[page_path] = {"extracted": len(ext), "skipped": len(skp)}
        total_extracted += len(ext)
        total_skipped += len(skp)
        if ext or skp:
            skip_note = f" (skipped {len(skp)})" if skp else ""
            print(f"  {page_path}: {len(ext)} block(s){skip_note}")

    print(f"\nTotal: {total_extracted} extracted, {total_skipped} skipped, from {len(pages)} pages")
    print(f"Output: {OUTPUT_DIR}")

    manifest = {
        "pages": pages,
        "page_stats": page_stats,
        "total_extracted": total_extracted,
        "total_skipped": total_skipped,
        "skipped_blocks": all_skipped,
    }
    manifest_path = OUTPUT_DIR / "_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))
    print(f"Manifest: {manifest_path}")


if __name__ == "__main__":
    main()
