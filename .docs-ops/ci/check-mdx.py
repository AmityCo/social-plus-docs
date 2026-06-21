#!/usr/bin/env python3
"""
check-mdx.py — fast, dependency-free MDX validity gate.

Catches the structural errors that break a Mintlify build BEFORE push/deploy:
  1. UNTERMINATED CODE FENCE — an odd number of ``` fences in a file. This is
     what broke send-a-message.mdx: an unclosed ```swift block swallowed the
     rest of the page, so a later </Accordion> was never seen.
  2. UNBALANCED JSX COMPONENT TAGS — <Accordion>/<Tabs>/<CardGroup>/... opened
     but never closed (or vice versa), counted OUTSIDE code fences.
  3. CODE SNIPPETS INSIDE CARDGROUP — SDK language snippets should use
     <CodeGroup>, while <CardGroup> is reserved for navigation/related cards.

Exit 0 = clean, 1 = problems found (so it can gate locally + in CI).
Needs no SDK source and no token, so it runs anywhere.

Usage:
  python3 .docs-ops/ci/check-mdx.py [paths...]          # default: scan all docs dirs
  python3 .docs-ops/ci/check-mdx.py --changed-since REF  # only .mdx changed vs REF
                                                         # (PR-gate mode; full-scan fallback)
"""
import re
import sys
import subprocess
import pathlib

DOCS_DIRS = ["social-plus-sdk", "analytics-and-moderation", "uikit",
             "use-cases", "api-reference", "essentials", "ai-mcp"]

# Mintlify/MDX components that require a matching close tag.
PAIRED = ["Accordion", "AccordionGroup", "Tabs", "Tab", "CardGroup", "Card",
          "Steps", "Step", "Info", "Warning", "Note", "Tip", "Check",
          "Frame", "Tooltip", "Expandable", "ResponseField", "ParamField",
          "CodeGroup", "Columns"]

FENCE = re.compile(r"^\s*```")
LANGUAGE_FENCE = re.compile(
    r"^\s*```(typescript|ts|tsx|javascript|js|kotlin|java|swift|dart)\b",
    re.IGNORECASE,
)
CARDGROUP_BLOCK = re.compile(r"<CardGroup\b[^>]*>[\s\S]*?</CardGroup>")


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


def code_in_card_groups(text):
    """Return line numbers where language code fences are nested in CardGroup."""
    bad = []
    for block in CARDGROUP_BLOCK.finditer(text):
        for offset, ln in enumerate(block.group(0).splitlines(), 0):
            if LANGUAGE_FENCE.match(ln):
                start_line = text[:block.start()].count("\n") + 1
                bad.append(start_line + offset)
    return bad


def check_file(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    problems = []
    odd = fence_balance(text)
    if odd:
        problems.append(f"unterminated code fence (odd ``` count = {len(odd)}); fence lines: {odd[-3:]}")
    for tag, o, c in tag_balance(text):
        problems.append(f"unbalanced <{tag}>: {o} open vs {c} close")
    for line in code_in_card_groups(text):
        problems.append(
            "language code fence inside <CardGroup> at line "
            f"{line}; use <CodeGroup> for code snippets and reserve <CardGroup> "
            "for navigation or related-topic cards"
        )
    return problems


def changed_mdx(ref):
    """`.mdx` files changed vs `ref` (added/modified, not deleted). None on failure."""
    try:
        out = subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=d", f"{ref}...HEAD", "--", "*.mdx"],
            capture_output=True, text=True, check=True,
        ).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    return [pathlib.Path(p) for p in out.split() if p]


def main(argv):
    files = None
    if argv and argv[0] == "--changed-since":
        ref = argv[1] if len(argv) > 1 else "origin/main"
        argv = []   # consume the flag so the full-scan fallback uses DOCS_DIRS
        changed = changed_mdx(ref)
        if changed is None:
            print(f"⚠️  could not diff against {ref}; falling back to full scan", file=sys.stderr)
        else:
            files = [p for p in changed if p.exists()]
            print(f"PR-gate mode: {len(files)} changed .mdx file(s) vs {ref}")
            if not files:
                print("no .mdx changed; nothing to check")
                return 0
    if files is None:
        roots = [pathlib.Path(a) for a in (argv or DOCS_DIRS)]
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
