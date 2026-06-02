#!/usr/bin/env python3
"""
check-mdx.py — fast, dependency-free MDX validity gate.

Catches the structural errors that break a Mintlify build BEFORE push/deploy:
  1. UNTERMINATED CODE FENCE — an odd number of ``` fences in a file. This is
     what broke send-a-message.mdx: an unclosed ```swift block swallowed the
     rest of the page, so a later </Accordion> was never seen.
  2. UNBALANCED JSX COMPONENT TAGS — <Accordion>/<Tabs>/<CardGroup>/... opened
     but never closed (or vice versa), counted OUTSIDE code fences.

Exit 0 = clean, 1 = problems found (so it can gate locally + in CI).
Needs no SDK source and no token, so it runs anywhere.

Usage:
  python3 .docs-ops/ci/check-mdx.py [paths...]   # default: scan all docs dirs
"""
import re
import sys
import pathlib

DOCS_DIRS = ["social-plus-sdk", "analytics-and-moderation", "uikit",
             "use-cases", "api-reference", "essentials", "ai-mcp"]

# Mintlify/MDX components that require a matching close tag.
PAIRED = ["Accordion", "AccordionGroup", "Tabs", "Tab", "CardGroup", "Card",
          "Steps", "Step", "Info", "Warning", "Note", "Tip", "Check",
          "Frame", "Tooltip", "Expandable", "ResponseField", "ParamField",
          "CodeGroup", "Columns"]

FENCE = re.compile(r"^\s*```")


def fence_balance(text):
    """Return list of fence line-numbers if unbalanced (odd), else []."""
    fences = [i + 1 for i, ln in enumerate(text.splitlines()) if FENCE.match(ln)]
    return fences if len(fences) % 2 else []


def strip_code(text):
    """Remove fenced code blocks so we don't count tags inside code."""
    out, in_fence = [], False
    for ln in text.splitlines():
        if FENCE.match(ln):
            in_fence = not in_fence
            continue
        if not in_fence:
            out.append(ln)
    return "\n".join(out)


def tag_balance(text):
    """Return list of (tag, open_count, close_count) for unbalanced paired tags."""
    body = strip_code(text)
    bad = []
    for tag in PAIRED:
        opens = len(re.findall(r"<" + tag + r"(?:\s[^>]*?)?>", body))
        selfclose = len(re.findall(r"<" + tag + r"(?:\s[^>]*?)?/>", body))
        closes = len(re.findall(r"</" + tag + r">", body))
        if (opens - selfclose) != closes:
            bad.append((tag, opens - selfclose, closes))
    return bad


def check_file(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    problems = []
    odd = fence_balance(text)
    if odd:
        problems.append(f"unterminated code fence (odd ``` count = {len(odd)}); fence lines: {odd[-3:]}")
    for tag, o, c in tag_balance(text):
        problems.append(f"unbalanced <{tag}>: {o} open vs {c} close")
    return problems


def main(argv):
    args = argv or DOCS_DIRS
    roots = [pathlib.Path(a) for a in args]
    files = []
    for r in roots:
        if r.is_dir():
            files.extend(sorted(r.rglob("*.mdx")))
        elif r.suffix == ".mdx" and r.exists():
            files.append(r)
    total_bad = 0
    for f in files:
        probs = check_file(f)
        if probs:
            total_bad += 1
            print(f"\n✗ {f}")
            for p in probs:
                print(f"    - {p}")
    print(f"\nchecked {len(files)} .mdx files; {total_bad} with problems")
    return 1 if total_bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
