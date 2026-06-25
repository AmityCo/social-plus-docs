#!/usr/bin/env python3
"""
check-sdk-style.py - changed-page SDK structure/style gate.

This is intentionally narrower than the factual drift gate. It enforces known
SDK page structure/style contracts for pages touched by a PR while the legacy
docs are normalized section by section. Page contracts are archetype-aware:
overview/setup/concept pages are not forced into operation-page structure.

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
PAGE_TYPES = {"overview", "concept", "operation", "setup", "migration", "reference-lite"}
FRONTMATTER_PAGE_TYPE = re.compile(r"^sdk_page_type:\s*[\"']?(.+?)[\"']?\s*$", re.MULTILINE)
FENCE_OPEN = re.compile(r"^\s*```(?P<lang>[A-Za-z0-9+#_.-]+)?(?P<label>.*)$")
TS_LANGS = {"typescript", "ts", "tsx", "javascript", "js", "jsx"}
REACT_SYMBOLS = ("FC", "useEffect", "useState", "useMemo", "useCallback", "React")
LIVE_TERM = re.compile(r"\bLive\s+(Object|Objects|Collection|Collections)\b", re.IGNORECASE)


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


def code_fences(text):
    fences = []
    lines = text.splitlines()
    in_fence = False
    start_line = 0
    lang = ""
    label = ""
    buf = []

    for line_no, line in enumerate(lines, 1):
        if FENCE.match(line):
            if not in_fence:
                match = FENCE_OPEN.match(line)
                lang = (match.group("lang") or "").lower() if match else ""
                label = (match.group("label") or "").strip() if match else ""
                start_line = line_no
                buf = []
                in_fence = True
            else:
                fences.append({
                    "line": start_line,
                    "lang": lang,
                    "label": label,
                    "code": "\n".join(buf),
                })
                in_fence = False
        elif in_fence:
            buf.append(line)

    return fences


def h2_sections(text):
    sections = []
    lines = text.splitlines()
    in_fence = False
    current = None

    for line_no, line in enumerate(lines, 1):
        if FENCE.match(line):
            in_fence = not in_fence
            if current:
                current["lines"].append(line)
            continue
        if not in_fence and (match := H2.match(line)):
            if current:
                sections.append(current)
            current = {"line": line_no, "heading": match.group(1).strip(), "lines": []}
            continue
        if current:
            current["lines"].append(line)

    if current:
        sections.append(current)
    return sections


def frontmatter_page_type(text):
    match = FRONTMATTER_PAGE_TYPE.search(text)
    if not match:
        return ""
    page_type = normalize_heading(match.group(1)).replace(" ", "-")
    return page_type if page_type in PAGE_TYPES else ""


def infer_page_type(path, text):
    explicit = frontmatter_page_type(text)
    if explicit:
        return explicit

    title_match = FRONTMATTER_TITLE.search(text)
    title = normalize_heading(title_match.group(1)) if title_match else ""
    stem = normalize_heading(path.stem)
    parts = {normalize_heading(p) for p in path.parts}
    has_sdk_fence = any(f["lang"] in TS_LANGS or f["lang"] in {"swift", "kotlin", "java", "dart"} for f in code_fences(text))

    if stem == "overview" or title.endswith(" overview") or title == "overview":
        return "overview"
    if "migration" in stem or "migration guide" in title or "migration" in parts:
        return "migration"
    if {"setup", "platform setup", "quick start", "quickstart"} & ({stem, title} | parts):
        return "setup"
    if "authentication" in stem and "getting started" in parts:
        return "setup"
    if not has_sdk_fence:
        return "concept"
    return "operation"


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


def parameters_section(sections):
    for section in sections:
        if normalize_heading(section["heading"]) == "parameters":
            return section
    return None


def first_table_header(section):
    if not section:
        return ""
    for line in section["lines"]:
        stripped = line.strip()
        if stripped.startswith("|") and stripped.endswith("|"):
            return stripped
    return ""


def has_platform_variance(text):
    visible = strip_code(text).lower()
    fences = code_fences(text)
    platform_count = sum(
        1
        for fence in fences
        if fence["lang"] in TS_LANGS or fence["lang"] in {"swift", "kotlin", "java", "dart"}
    )
    signals = [
        "platform-dependent",
        "platform-specific",
        "where supported",
        "where the platform",
        "ios and typescript",
        "android observes",
        "flutter returns",
        "no batch api",
        "live object",
        "live collection",
    ]
    return platform_count >= 2 and any(signal in visible for signal in signals)


def operation_parameter_contract(path, text, page_type, sections):
    problems = []
    if page_type != "operation":
        return problems

    params = parameters_section(sections)
    if not params:
        problems.append(
            "operation page is missing `## Parameters`; add a compact parameter table, "
            "or mark the page with `sdk_page_type: concept` / `overview` if it is not a method page"
        )
        return problems

    header = first_table_header(params)
    if has_platform_variance(text) and "platform" not in header.lower():
        problems.append(
            f"line {params['line']}: Parameters table needs a `Platforms` column because the page "
            "documents platform-dependent behavior"
        )
    return problems


def live_object_claims(text):
    problems = []
    visible_lines = strip_code(text).splitlines()
    paragraphs = []
    current = []
    start_line = 1

    for line_no, line in enumerate(visible_lines, 1):
        if line.strip():
            if not current:
                start_line = line_no
            current.append(line.strip())
        elif current:
            paragraphs.append((start_line, " ".join(current)))
            current = []
    if current:
        paragraphs.append((start_line, " ".join(current)))

    qualifiers = [
        "where supported",
        "platform",
        "ios",
        "typescript",
        "android",
        "flutter",
        "flowable",
        "future",
        "stream",
        "callback",
    ]
    universal_phrases = [
        "returned as",
        "returns as",
        "automatically update",
        "automatically updates",
        "always",
        "all sdk",
        "all platforms",
    ]

    for line_no, paragraph in paragraphs:
        lower = paragraph.lower()
        if not LIVE_TERM.search(paragraph):
            continue
        if any(q in lower for q in qualifiers):
            continue
        if any(phrase in lower for phrase in universal_phrases):
            problems.append(
                f"line {line_no}: qualify Live Object / Live Collection wording by platform; "
                "Flutter and Android expose different observable/future shapes"
            )
    return problems


def typescript_snippet_contract(text):
    problems = []
    for fence in code_fences(text):
        if fence["lang"] not in TS_LANGS:
            continue

        code = fence["code"]
        label = fence["label"].lower()
        uses_react_symbol = any(re.search(rf"\b{symbol}\b", code) for symbol in REACT_SYMBOLS)
        uses_jsx = bool(re.search(r"return\s*\([\s\S]*<[A-Za-z][A-Za-z0-9]*(\s|>|/)", code))
        if not uses_react_symbol and not uses_jsx:
            continue

        if "react" not in label:
            problems.append(
                f"line {fence['line']}: generic TypeScript snippet uses React-specific patterns; "
                "label it as React or rewrite it as framework-neutral SDK code"
            )

        if uses_react_symbol and not re.search(r"from\s+['\"]react['\"]", code):
            problems.append(
                f"line {fence['line']}: React-specific TypeScript snippet references React symbols "
                "without a visible React import"
            )
    return problems


def operation_method_consistency(sections):
    problems = []
    batch_pattern = re.compile(r"\b(getUserByIds|getUsersByIds|by IDs?|user IDs?)\b", re.IGNORECASE)
    query_pattern = re.compile(r"(\bgetUsers\s*\(|\.getUsers\s*\(|getUsers\(\)|query users|all users)", re.IGNORECASE)

    for section in sections:
        heading = normalize_heading(section["heading"])
        body = "\n".join(section["lines"])
        if "multiple" not in heading and "by id" not in heading and "by ids" not in heading:
            continue
        if batch_pattern.search(body) and query_pattern.search(body):
            problems.append(
                f"line {section['line']}: section mixes batch-by-ID lookup with paginated user query; "
                "split these into separate operation sections"
            )
    return problems


def check_file(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    body = strip_code(text)
    problems = []
    page_type = infer_page_type(path, text)
    sections = h2_sections(text)

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
    problems.extend(operation_parameter_contract(path, text, page_type, sections))
    problems.extend(live_object_claims(text))
    problems.extend(typescript_snippet_contract(text))
    problems.extend(operation_method_consistency(sections))
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
