#!/usr/bin/env python3
"""
proxy-scan.py — cheap, LLM-free full-corpus quality proxies for the 3 weak
rubric dimensions the 10-page pilot surfaced (parity, clarity, completeness).

The pilot's LLM-judge scores validated that these structural proxies track real
editorial quality. This scans the WHOLE SDK doc corpus (~311 pages) in seconds,
with zero model cost, to show how widespread each problem is and which sections
are weakest.

Proxies (each is a heuristic, intentionally transparent + tunable):
  PARITY        platform code-block counts per page; flag missing/under-covered
                platforms (esp. Flutter), the pilot's #1 finding.
  CLARITY       marketing-register opener (adjectives) and/or a component
                (<Info>/<CardGroup>) before any functional sentence.
  COMPLETENESS  page documents an API (has code) but ships NO parameter table.

Usage:
  python3 .docs-ops/quality-scan/proxy-scan.py [--root social-plus-sdk] [--json-out out.json] [--md-out report.md]
"""
import argparse
import json
import pathlib
import re
import sys
from collections import defaultdict

# fence language -> platform
LANG_PLATFORM = {
    "swift": "iOS", "kotlin": "Android", "java": "Android",
    "typescript": "TypeScript", "ts": "TypeScript",
    "javascript": "TypeScript", "js": "TypeScript",
    "dart": "Flutter",
}
PLATFORMS = ["iOS", "Android", "TypeScript", "Flutter"]

FENCE_RE = re.compile(r"^\s*```([A-Za-z0-9]+)\b", re.MULTILINE)

# Param-table proxy: a markdown table whose header names parameters or has a Type column.
PARAM_TABLE_RE = re.compile(
    r"\|[^\n]*\b(Parameter|Param|Argument|Field|Property|Name)\b[^\n]*\|[^\n]*\n\s*\|[\s:\-|]+\|",
    re.IGNORECASE,
)
TYPE_TABLE_RE = re.compile(
    r"\|[^\n]*\bType\b[^\n]*\|[^\n]*\n\s*\|[\s:\-|]+\|", re.IGNORECASE,
)

# Clarity proxy: marketing adjectives/verbs that signal non-functional prose.
MARKETING = [
    "robust", "seamless", "seamlessly", "powerful", "flexible", "comprehensive",
    "effortless", "effortlessly", "rich", "intuitive", "cutting-edge", "leverage",
    "empower", "unlock", "elevate", "streamline", "enhance", "versatile",
    "sophisticated", "state-of-the-art", "world-class", "delightful", "rich set",
    "powerful set", "wide range", "out of the box", "out-of-the-box",
]
MARKETING_RE = re.compile(r"\b(" + "|".join(re.escape(w) for w in MARKETING) + r")\b", re.IGNORECASE)

# Fenced code body, to search inside code only (not prose).
CODE_BLOCK_RE = re.compile(r"```[^\n]*\n(.*?)```", re.DOTALL)
# A "parameter-bearing call": a call site that passes a real argument list —
#   foo({ ...options... })   |   foo(\n  arg...   |   foo(a, b)
# Zero-arg calls foo() / property access don't qualify (nothing to tabulate).
PARAM_CALL_RE = re.compile(
    r"[A-Za-z_]\w*\s*\(\s*(\{|[A-Za-z_'\"][^)]*,|[\r\n])",
)


def strip_frontmatter(text):
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4:]
    return text


def first_prose(text):
    """Return (opener_line, opened_with_component: bool).

    Skips headings, imports, and the title; returns the first real sentence.
    Flags when the first *content* element is a JSX component (Feature-Overview
    pattern) rather than a sentence.
    """
    body = strip_frontmatter(text)
    opened_with_component = None  # None until we see first content
    for raw in body.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("#"):          # heading / title
            continue
        if line.startswith(("import ", "export ")):
            continue
        if line.startswith("<"):          # JSX component
            if opened_with_component is None:
                opened_with_component = True
            continue
        # first prose line
        if opened_with_component is None:
            opened_with_component = False
        return line, opened_with_component
    return "", bool(opened_with_component)


def scan_page(path, root):
    text = path.read_text(encoding="utf-8", errors="replace")
    rel = str(path.relative_to(root.parent))
    section = path.relative_to(root).parts[0] if len(path.relative_to(root).parts) > 1 else "(root)"

    # --- platform code-block counts ---
    counts = defaultdict(int)
    for lang in FENCE_RE.findall(text):
        p = LANG_PLATFORM.get(lang.lower())
        if p:
            counts[p] += 1
    total_code = sum(counts.values())
    present = [p for p in PLATFORMS if counts[p] > 0]
    # A <CodeGroup> means the page is EXPLICITLY laying platforms out side-by-side,
    # so a missing platform there is a defect by the page's own design intent.
    # Scattered code (no CodeGroup) isn't claiming parity — lower confidence.
    has_codegroup = "<CodeGroup" in text

    # --- parity proxy ---
    parity = None
    if len(present) >= 1 and total_code >= 1:
        missing = [p for p in PLATFORMS if counts[p] == 0]
        # only meaningful when the page clearly documents code for several platforms
        if len(present) >= 2:
            mx = max(counts[p] for p in present)
            mn = min(counts[p] for p in present)
            disparity = (mx >= 2 * mn) and (mx - mn >= 2)
            if missing or disparity:
                parity = {
                    "counts": {p: counts[p] for p in PLATFORMS},
                    "missing": missing,
                    "disparity": disparity,
                    "flutter_gap": ("Flutter" in missing) or (counts["Flutter"] * 2 < mx if present else False),
                    "intent": "codegroup" if has_codegroup else "scattered",
                    "confidence": "high" if has_codegroup else "review",
                }

    # --- completeness proxy ---
    has_param_table = bool(PARAM_TABLE_RE.search(text) or TYPE_TABLE_RE.search(text))
    # Refined: only a real gap if the page shows a parameter-bearing call (there
    # ARE params to document) but ships no table. Excludes conceptual/setup pages
    # whose code is zero-arg calls or initialization — content-based, not slug-based.
    code_body = "\n".join(CODE_BLOCK_RE.findall(text))
    has_param_call = bool(PARAM_CALL_RE.search(code_body))
    completeness_raw = (total_code >= 1) and (not has_param_table)          # old, over-counting
    completeness_flag = has_param_call and (not has_param_table)            # refined, actionable

    # --- clarity proxy ---
    opener, opened_with_component = first_prose(text)
    marketing_hits = MARKETING_RE.findall(opener)
    clarity_flag = bool(marketing_hits) or opened_with_component

    return {
        "page": rel,
        "section": section,
        "total_code": total_code,
        "platform_counts": {p: counts[p] for p in PLATFORMS},
        "parity": parity,
        "has_param_table": has_param_table,
        "has_param_call": has_param_call,
        "completeness_raw": completeness_raw,
        "completeness_flag": completeness_flag,
        "opener": opener[:140],
        "opened_with_component": opened_with_component,
        "marketing_hits": sorted(set(h.lower() for h in marketing_hits)),
        "clarity_flag": clarity_flag,
    }


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="social-plus-sdk")
    ap.add_argument("--json-out")
    ap.add_argument("--md-out")
    ap.add_argument("--docs-json", help="If set, scan only pages present in this docs.json navigation (live pages)")
    args = ap.parse_args(argv)

    root = pathlib.Path(args.root).resolve()
    if not root.is_dir():
        print(f"root not found: {root}", file=sys.stderr)
        return 2

    pages = sorted(root.rglob("*.mdx"))
    if args.docs_json:
        dj = json.load(open(args.docs_json))
        _nav = []
        def _w(o):
            if isinstance(o, str): _nav.append(o)
            elif isinstance(o, dict): [_w(v) for v in o.values()]
            elif isinstance(o, list): [_w(x) for x in o]
        _w(dj.get("navigation", dj))
        navset = set(_nav) | set(p + ".mdx" for p in _nav)
        def _rel(p):
            return str(p.relative_to(root.parent))   # repo-relative, e.g. social-plus-sdk/.../x.mdx
        pages = [p for p in pages if _rel(p) in navset or _rel(p)[:-4] in navset]
        print(f"docs.json scope: {len(pages)} live pages")
    results = [scan_page(p, root) for p in pages]

    n = len(results)
    parity_flagged = [r for r in results if r["parity"]]
    flutter_gap = [r for r in parity_flagged if r["parity"]["flutter_gap"]]
    flutter_gap_high = [r for r in flutter_gap if r["parity"]["confidence"] == "high"]
    flutter_gap_review = [r for r in flutter_gap if r["parity"]["confidence"] == "review"]
    clarity_flagged = [r for r in results if r["clarity_flag"]]
    marketing_flagged = [r for r in results if r["marketing_hits"]]
    component_first = [r for r in results if r["opened_with_component"]]
    code_pages = [r for r in results if r["total_code"] >= 1]
    completeness_flagged = [r for r in code_pages if r["completeness_flag"]]
    completeness_raw_flagged = [r for r in code_pages if r["completeness_raw"]]
    param_call_pages = [r for r in code_pages if r["has_param_call"]]

    # per-section rollup
    by_section = defaultdict(lambda: {"pages": 0, "parity": 0, "clarity": 0, "completeness_of_code": 0, "code_pages": 0})
    for r in results:
        s = by_section[r["section"]]
        s["pages"] += 1
        if r["parity"]: s["parity"] += 1
        if r["clarity_flag"]: s["clarity"] += 1
        if r["total_code"] >= 1:
            s["code_pages"] += 1
            if r["completeness_flag"]: s["completeness_of_code"] += 1

    summary = {
        "root": str(root),
        "total_pages": n,
        "code_pages": len(code_pages),
        "parity": {"flagged": len(parity_flagged), "flutter_gap": len(flutter_gap),
                   "flutter_gap_high_confidence": len(flutter_gap_high),
                   "flutter_gap_needs_review": len(flutter_gap_review),
                   "pct_of_code_pages": round(100 * len(parity_flagged) / max(1, len(code_pages)), 1)},
        "clarity": {"flagged": len(clarity_flagged), "marketing_openers": len(marketing_flagged),
                    "component_first": len(component_first),
                    "pct": round(100 * len(clarity_flagged) / max(1, n), 1)},
        "completeness": {"actionable_param_call_no_table": len(completeness_flagged),
                         "param_call_pages": len(param_call_pages),
                         "pct_of_param_call_pages": round(100 * len(completeness_flagged) / max(1, len(param_call_pages)), 1),
                         "raw_any_code_no_table": len(completeness_raw_flagged)},
        "by_section": {k: v for k, v in sorted(by_section.items(), key=lambda kv: -kv[1]["pages"])},
    }

    # --- console summary ---
    print(f"\n=== Quality proxy scan: {n} pages under {root.name} ({len(code_pages)} with code) ===\n")
    print(f"PARITY       {summary['parity']['flagged']:>3} pages flagged; "
          f"{summary['parity']['flutter_gap']} Flutter gaps = "
          f"{summary['parity']['flutter_gap_high_confidence']} high-confidence (CodeGroup, parallel intent) "
          f"+ {summary['parity']['flutter_gap_needs_review']} needs-review (scattered code)")
    print(f"CLARITY      {summary['clarity']['flagged']:>3} pages flagged "
          f"({summary['clarity']['pct']}%): {summary['clarity']['marketing_openers']} marketing openers, "
          f"{summary['clarity']['component_first']} open with a component")
    print(f"COMPLETENESS {summary['completeness']['actionable_param_call_no_table']:>3} pages show a parameter-bearing call "
          f"but NO table ({summary['completeness']['pct_of_param_call_pages']}% of "
          f"{summary['completeness']['param_call_pages']} param-call pages); raw any-code-no-table was "
          f"{summary['completeness']['raw_any_code_no_table']}")

    print("\n--- Worst sections (by % flagged) ---")
    rows = []
    for sec, v in by_section.items():
        cp = max(1, v["code_pages"])
        rows.append((sec, v["pages"], v["code_pages"],
                     round(100 * v["parity"] / cp, 0),
                     round(100 * v["clarity"] / max(1, v["pages"]), 0),
                     round(100 * v["completeness_of_code"] / cp, 0)))
    print(f"{'section':<40} {'pages':>5} {'code':>5} {'par%':>5} {'cla%':>5} {'cmp%':>5}")
    for sec, p, cp, par, cla, cmp in sorted(rows, key=lambda x: -(x[3] + x[5])):
        print(f"{sec:<40} {p:>5} {cp:>5} {par:>5.0f} {cla:>5.0f} {cmp:>5.0f}")

    out = {"summary": summary, "pages": results}
    if args.json_out:
        pathlib.Path(args.json_out).write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
        print(f"\nJSON written: {args.json_out}")
    if args.md_out:
        write_md(out, args.md_out)
        print(f"Markdown written: {args.md_out}")
    return 0


def write_md(out, path):
    s = out["summary"]
    L = []
    L.append("# Docs Quality — Full-Corpus Proxy Scan\n")
    L.append(f"_LLM-free structural proxies for the 3 weak rubric dimensions. Scanned {s['total_pages']} pages "
             f"under `{pathlib.Path(s['root']).name}` ({s['code_pages']} with code blocks)._\n")
    L.append("## Headline\n")
    L.append(f"- **Parity:** {s['parity']['flagged']} pages flagged ({s['parity']['pct_of_code_pages']}% of code pages); "
             f"**{s['parity']['flutter_gap']} are Flutter coverage gaps**.")
    L.append(f"- **Clarity:** {s['clarity']['flagged']} pages ({s['clarity']['pct']}%) — "
             f"{s['clarity']['marketing_openers']} marketing-register openers, {s['clarity']['component_first']} open with a component before any sentence.")
    L.append(f"- **Completeness:** {s['completeness']['actionable_param_call_no_table']} pages show a parameter-bearing call "
             f"but ship **no parameter table** ({s['completeness']['pct_of_param_call_pages']}% of "
             f"{s['completeness']['param_call_pages']} param-call pages; raw any-code-no-table = {s['completeness']['raw_any_code_no_table']}).\n")
    L.append("## By section\n")
    L.append("| Section | Pages | Code pages | Parity flagged | Clarity flagged | No param table |")
    L.append("|---|---|---|---|---|---|")
    for sec, v in s["by_section"].items():
        L.append(f"| `{sec}` | {v['pages']} | {v['code_pages']} | {v['parity']} | {v['clarity']} | {v['completeness_of_code']} |")
    # worst offenders
    L.append("\n## Flutter coverage gaps (top 25)\n")
    fg = [r for r in out["pages"] if r["parity"] and r["parity"]["flutter_gap"]]
    fg.sort(key=lambda r: r["platform_counts"]["Flutter"] - max(r["platform_counts"].values()))
    for r in fg[:25]:
        c = r["platform_counts"]
        L.append(f"- `{r['page']}` — iOS {c['iOS']}, Android {c['Android']}, TS {c['TypeScript']}, **Flutter {c['Flutter']}**")
    L.append("\n## Marketing-register openers (top 25)\n")
    for r in [r for r in out["pages"] if r["marketing_hits"]][:25]:
        L.append(f"- `{r['page']}` — {', '.join(r['marketing_hits'])} — \"{r['opener'][:90]}…\"")
    pathlib.Path(path).write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
