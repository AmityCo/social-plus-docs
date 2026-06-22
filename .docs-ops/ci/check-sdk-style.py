#!/usr/bin/env python3
"""
check-sdk-style.py - changed-page SDK structure/style gate.

This is intentionally narrower than the factual drift gate. It enforces the
cosmetic structure contract for pages touched by a PR while the legacy docs are
normalized section by section.

Usage:
  python3 .docs-ops/ci/check-sdk-style.py [paths...]
  python3 .docs-ops/ci/check-sdk-style.py --changed-since origin/main
"""
import argparse
import pathlib
import re
import subprocess
import sys

SDK_ROOT = pathlib.Path("social-plus-sdk")
FENCE = re.compile(r"^\s*```")
SDK_LANG_FENCE = re.compile(
    r"^\s*```(typescript|ts|tsx|javascript|js|kotlin|java|swift|dart)\b",
    re.IGNORECASE,
)
H1 = re.compile(r"^#\s+(.+?)\s*$")
H2 = re.compile(r"^##\s+(.+?)\s*$")
FRONTMATTER_TITLE = re.compile(r'^title:\s*["\']?(.+?)["\']?\s*$', re.MULTILINE)
PLATFORM_HEADINGS = {"typescript", "ios", "android", "flutter"}


def normalize_heading(text):
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def strip_code(text):
    out = []
    in_fence = False
    for line in text.splitlines():
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if not in_fence:
            out.append(line)
    return "\n".join(out)


def changed_mdx(ref):
    try:
        committed = subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=d", f"{ref}...HEAD", "--", "*.mdx"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
        worktree = subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=d", "--", "*.mdx"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    paths = {
        pathlib.Path(p)
        for output in (committed, worktree)
        for p in output.splitlines()
        if p.startswith("social-plus-sdk/")
    }
    return sorted(paths)


def collect_files(paths, changed_since):
    if changed_since:
        changed = changed_mdx(changed_since)
        if changed is None:
            print(f"warning: could not diff against {changed_since}; falling back to provided paths", file=sys.stderr)
        else:
            return [p for p in changed if p.exists()]

    roots = [pathlib.Path(p) for p in paths] if paths else [SDK_ROOT]
    files = []
    for root in roots:
        if root.is_dir():
            files.extend(sorted(root.rglob("*.mdx")))
        elif root.suffix == ".mdx" and root.exists():
            files.append(root)
    return [p for p in files if str(p).startswith("social-plus-sdk/")]


def codegroup_depth_before_fences(text):
    problems = []
    in_fence = False
    codegroup_depth = 0

    for line_no, line in enumerate(text.splitlines(), 1):
        if not in_fence:
            opens = len(re.findall(r"<CodeGroup(?:\s[^>]*)?>", line))
            self_closes = len(re.findall(r"<CodeGroup(?:\s[^>]*)?/>", line))
            closes = len(re.findall(r"</CodeGroup>", line))
            codegroup_depth += opens - self_closes - closes
            if codegroup_depth < 0:
                codegroup_depth = 0

        if FENCE.match(line):
            if not in_fence and SDK_LANG_FENCE.match(line) and codegroup_depth <= 0:
                problems.append(
                    f"line {line_no}: SDK language code fence is outside <CodeGroup>; "
                    "wrap platform snippets in CodeGroup"
                )
            in_fence = not in_fence

    return problems


def codegroup_without_intro(text):
    problems = []
    lines = text.splitlines()
    in_fence = False
    for idx, line in enumerate(lines):
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence or not re.search(r"<CodeGroup(?:\s[^>]*)?>", line):
            continue

        prev = ""
        for j in range(idx - 1, -1, -1):
            candidate = lines[j].strip()
            if candidate:
                prev = candidate
                break
        if prev.startswith("#"):
            problems.append(
                f"line {idx + 1}: add a short method explanation before <CodeGroup>"
            )
    return problems


def check_file(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    body = strip_code(text)
    problems = []

    title_match = FRONTMATTER_TITLE.search(text)
    title = title_match.group(1).strip() if title_match else ""
    normalized_title = normalize_heading(title)

    h1s = [(i + 1, m.group(1).strip()) for i, line in enumerate(body.splitlines()) if (m := H1.match(line))]
    for line_no, heading in h1s:
        problems.append(
            f"line {line_no}: remove body H1 '# {heading}'; Mintlify renders the frontmatter title"
        )

    h2s = [(i + 1, m.group(1).strip()) for i, line in enumerate(body.splitlines()) if (m := H2.match(line))]
    if title and h2s:
        first_line, first_h2 = h2s[0]
        if normalize_heading(first_h2) == normalized_title:
            problems.append(
                f"line {first_line}: first H2 repeats page title; start with parameters or a task/method section"
            )

    platform_h2s = [(line_no, heading) for line_no, heading in h2s if normalize_heading(heading) in PLATFORM_HEADINGS]
    if len(platform_h2s) >= 2:
        joined = ", ".join(f"{heading} at line {line_no}" for line_no, heading in platform_h2s)
        problems.append(
            "platform-specific H2 sections found "
            f"({joined}); group platform snippets inside one method section with CodeGroup"
        )

    problems.extend(codegroup_depth_before_fences(text))
    problems.extend(codegroup_without_intro(text))
    return problems


def main(argv):
    parser = argparse.ArgumentParser(description="Check SDK docs page structure and cosmetic style.")
    parser.add_argument("paths", nargs="*", help="Files or directories to scan. Defaults to social-plus-sdk/.")
    parser.add_argument("--changed-since", help="Scan only changed SDK .mdx files versus this git ref.")
    args = parser.parse_args(argv)

    files = collect_files(args.paths, args.changed_since)
    if args.changed_since:
        print(f"SDK style mode: {len(files)} changed social-plus-sdk .mdx file(s) vs {args.changed_since}")
    if not files:
        print("no SDK .mdx files to check")
        return 0

    bad = 0
    for path in files:
        problems = check_file(path)
        if not problems:
            continue
        bad += 1
        print(f"\nFAIL {path}")
        for problem in problems:
            print(f"    - {problem}")

    print(f"\nchecked {len(files)} SDK .mdx files; {bad} with style problems")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
