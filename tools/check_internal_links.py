#!/usr/bin/env python3
"""
Internal link checker for MD/MDX documentation.

Resolves and validates links in markdown/MDX files:
 - HTML href="..."
 - Markdown [text](link)

Resolution rules:
 - Skip external (http/https/mailto) and anchor-only (#...) links
 - Absolute paths starting with '/' map to repo root (strip leading slash)
 - Relative paths resolved against the source file's directory
 - For a logical path without extension we try these candidates in order:
      <path>.mdx, <path>.md, <path>/overview.mdx, <path>/README.mdx, <path>/index.mdx
 - For a path WITH extension (.mdx/.md) we test as-is
 - Anchor fragments after '#' are ignored during existence check

Outputs a report listing unique missing targets and referencing files/lines.
Exit code 0 if no broken links, 1 otherwise.
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent
CONTENT_EXTS = {'.mdx'}  # Only scan MDX per updated requirement
LINK_PATTERN = re.compile(r'href="([^"]+)"|\[[^\]]+\]\(([^)]+)\)')

def candidate_paths(logical: Path):
    """Yield possible file candidates for a logical (extension-less) path."""
    yield logical.with_suffix('.mdx')
    yield logical.with_suffix('.md')
    yield logical / 'overview.mdx'
    yield logical / 'README.mdx'
    yield logical / 'index.mdx'

def resolve_link(src_file: Path, link: str) -> Path | None:
    # Strip anchor
    anchor_split = link.split('#', 1)
    path_part = anchor_split[0]
    if not path_part:
        return None

    # Handle absolute
    if path_part.startswith('/'):
        logical = ROOT / path_part.lstrip('/')
    else:
        logical = (src_file.parent / path_part).resolve()

    # If path has extension directly (md/mdx) or any existing asset file
    if logical.suffix:
        if logical.suffix in CONTENT_EXTS:
            return logical if logical.exists() else None
        # Non-doc assets: treat as valid if the file exists
        return logical if logical.exists() else None

    # If path ends with a slash treat as directory
    if path_part.endswith('/'):
        logical = logical / ''  # ensure directory form

    # Try candidate resolution
    for c in candidate_paths(logical):
        if c.exists():
            return c
    return None

def is_ignored(link: str) -> bool:
    link = link.strip()
    if not link:
        return True
    if link.startswith('#'):
        return True
    if re.match(r'^[a-zA-Z]+://', link):  # external
        return True
    if link.startswith('mailto:'):
        return True
    return False

def load_docs_json_pages() -> set[str]:
    """Parse docs.json and return set of declared page slugs (without extension)."""
    docs_path = ROOT / 'docs.json'
    if not docs_path.exists():
        return set()
    try:
        data = json.loads(docs_path.read_text(encoding='utf-8'))
    except Exception as e:
        print(f"WARN: Failed to parse docs.json: {e}")
        return set()

    pages = set()

    def walk(node):
        if isinstance(node, dict):
            # Node may have 'pages' or nested groups
            if 'pages' in node and isinstance(node['pages'], list):
                for p in node['pages']:
                    walk(p)
            # group/openapi/etc. just ignore other keys
            for k, v in node.items():
                if k not in {'pages'}:
                    walk(v)
        elif isinstance(node, list):
            for item in node:
                walk(item)
        elif isinstance(node, str):
            pages.add(node)
        # else ignore other primitive types

    nav = (data.get('navigation') or {}).get('tabs') or []
    walk(nav)
    return pages

NAV_PAGES = load_docs_json_pages()

def file_slug(path: Path) -> str:
    rel = path.relative_to(ROOT)
    return str(rel.with_suffix(''))

def collect_md_files():
    """Return only MDX files that are declared in docs.json navigation."""
    files = []
    for p in ROOT.rglob('*.mdx'):
        if file_slug(p) in NAV_PAGES:
            files.append(p)
    return files

def main():
    broken = defaultdict(list)  # logical link -> list[(file, line_no)]
    total_links = 0
    files = collect_md_files()
    for f in files:
        try:
            text = f.read_text(encoding='utf-8')
        except Exception as e:
            print(f"WARN: Could not read {f}: {e}", file=sys.stderr)
            continue
        for i, line in enumerate(text.splitlines(), start=1):
            for m in LINK_PATTERN.finditer(line):
                link = m.group(1) or m.group(2)
                if not link:
                    continue
                total_links += 1
                if is_ignored(link):
                    continue
                target = resolve_link(f, link)
                if target is None:
                    # Determine if this logical link is within navigation scope; if not, ignore
                    # Normalize logical slug removal of extension if present
                    logical = link.split('#', 1)[0]
                    if logical.startswith('/'):
                        logical_rel = logical.lstrip('/')
                    else:
                        # Resolve relative to source directory and express relative slug
                        logical_rel_path = (f.parent / logical).resolve()
                        try:
                            logical_rel = str(logical_rel_path.relative_to(ROOT))
                        except ValueError:
                            # Outside repo
                            logical_rel = logical
                    # Strip extension for slug comparison
                    slug_no_ext = logical_rel.rsplit('.', 1)[0]
                    if slug_no_ext not in NAV_PAGES:
                        continue  # ignore targets not in docs.json navigation
                    broken[link].append((f.relative_to(ROOT), i))

    if not broken:
        print(f"✅ No broken internal links found across {len(files)} files (scanned {total_links} links).")
        return 0

    print(f"❌ Broken internal links detected: {len(broken)} unique paths (navigation-scoped)\n")
    for link, refs in sorted(broken.items()):
        print(f"Link: {link}")
        for ref_file, line in refs[:10]:  # cap to 10 refs for brevity
            print(f"  - {ref_file}:{line}")
        if len(refs) > 10:
            print(f"  (+{len(refs)-10} more occurrences)")
        print()
    print("Summary: " + ", ".join(f"{k} ({len(v)})" for k,v in broken.items()))
    return 1

if __name__ == '__main__':
    sys.exit(main())
