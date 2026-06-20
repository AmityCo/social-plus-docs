#!/usr/bin/env python3
"""
extract-blocks.py — Walk pages.json, extract every TypeScript/JS fenced code block,
write one .ts file per block into results/extracted/.

Handles:
  - Standard fenced blocks: ```typescript, ```ts, ```javascript, ```js
  - Blocks with MDX language+label: ```typescript TypeScript, ```kotlin Android (skip non-TS)
  - Indented blocks inside MDX components (<Step>, <Tab>, <Accordion>, <CodeGroup>)
    by stripping leading whitespace before matching fences
  - enumerate: entries in pages.json (walks the given directory for .mdx files)
  - Skip markers: <!-- doc-as-test: skip (reason) --> or {/* doc-as-test: skip (reason) */}
    placed on the line immediately before a fenced block opening
"""

import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
DOCS_ROOT = (SCRIPT_DIR / "../..").resolve()
OUTPUT_DIR = SCRIPT_DIR / "results" / "extracted"
PAGES_JSON = SCRIPT_DIR / "pages.json"
PREAMBLE_PATH = SCRIPT_DIR / "preamble.d.ts"

FENCE_OPEN_RE = re.compile(
    r'^[ \t]*```(typescript|ts|javascript|js)(?:\s+\S+)?\s*$',
    re.IGNORECASE,
)
FENCE_CLOSE_RE = re.compile(r'^[ \t]*```\s*$')

# Skip markers: HTML comment or JSX comment style, with optional reason in parens
SKIP_MARKER_RE = re.compile(
    r'doc-as-test:\s*skip(?:\s*\(([^)]*)\))?',
    re.IGNORECASE,
)


def resolve_pages(pages_data):
    paths = []
    all_entries = (
        pages_data.get("audited_root", [])
        + pages_data.get("audited_getting_started", [])
        + pages_data.get("audited_user_management", [])
        + pages_data.get("audited_social_entry", [])
        + pages_data.get("audited_community_lifecycle", [])
        + pages_data.get("audited_community_discovery", [])
        + pages_data.get("audited_community_organization", [])
        + pages_data.get("audited_community_admin", [])
        + pages_data.get("audited_content_foundation", [])
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
    seen = set()
    deduped = []
    for p in paths:
        if p not in seen:
            seen.add(p)
            deduped.append(p)
    return deduped


def extract_blocks(page_path):
    """
    Extract all TS/JS code blocks from an .mdx file.
    Returns (extracted_blocks, skipped_blocks).
    Each extracted block: {content, start_line, end_line}.
    Each skipped block: {file, line, reason}.
    """
    full_path = DOCS_ROOT / page_path
    text = full_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    extracted = []
    skipped = []
    in_block = False
    block_lines = []
    block_start = 0
    skip_mode = False
    pending_skip = None  # reason string if previous non-empty line had skip marker

    for i, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not in_block:
            skip_m = SKIP_MARKER_RE.search(stripped) if stripped else None
            if skip_m:
                pending_skip = skip_m.group(1) or "skip"
            elif stripped:
                if FENCE_OPEN_RE.match(line):
                    if pending_skip is not None:
                        skipped.append({
                            "file": page_path,
                            "line": i,
                            "reason": pending_skip,
                        })
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
            # Empty lines: preserve pending_skip across whitespace
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


JSX_RE = re.compile(r"from [\"']react[\"']|<[A-Z][a-zA-Z]* |return\s*\(?\s*<|<video|<div|<input|<span|<button|:\s*JSX\.Element|:\s*React\.FC")



def is_jsx_block(content):
    """Detect JSX/React code that needs .tsx extension."""
    return bool(JSX_RE.search(content))


def write_block(slug, block_index, block, preamble_rel, page_path):
    ext = ".tsx" if is_jsx_block(block["content"]) else ".ts"
    filename = f"{slug}-block-{block_index}{ext}"
    out_path = OUTPUT_DIR / filename
    source_comment = f"// source: {page_path}:{block['start_line']}-{block['end_line']}\n"
    content = (
        f'/// <reference path="{preamble_rel}" />\n'
        f'{source_comment}'
        f'\n{block["content"]}\n'
    )
    out_path.write_text(content, encoding="utf-8")
    return out_path


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for old in list(OUTPUT_DIR.glob("*.ts")) + list(OUTPUT_DIR.glob("*.tsx")):
        old.unlink()

    pages_data = json.loads(PAGES_JSON.read_text())
    pages = resolve_pages(pages_data)
    preamble_rel = "../../preamble.d.ts"

    total_extracted = 0
    total_skipped = 0
    page_stats = {}
    all_skipped = []

    print(f"Extracting from {len(pages)} pages...")
    for page_path in pages:
        ext, skp = extract_blocks(page_path)
        slug = page_to_slug(page_path)
        for i, block in enumerate(ext, start=1):
            write_block(slug, i, block, preamble_rel, page_path)
        all_skipped.extend(skp)
        page_stats[page_path] = {"extracted": len(ext), "skipped": len(skp)}
        total_extracted += len(ext)
        total_skipped += len(skp)
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
