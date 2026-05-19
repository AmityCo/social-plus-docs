#!/usr/bin/env python3
"""
Render a rubric-scorer results JSON into a human-readable markdown report.

Usage:
    python3 .docs-ops/rubric-scorer/render-report.py --dimension clarity
    python3 .docs-ops/rubric-scorer/render-report.py --input results/clarity-latest.json
"""
from __future__ import annotations
import argparse
import json
import pathlib
import sys
from collections import Counter

SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent


def sparkline_bar(distribution: dict[str, int]) -> str:
    """ASCII histogram bar for score distribution."""
    total = sum(distribution.values())
    if total == 0:
        return "_No data._"
    lines = []
    for score in ("5", "4", "3", "2", "1"):
        count = distribution.get(score, 0)
        bar = "█" * count
        lines.append(f"  {score} | {bar} ({count})")
    return "\n".join(lines)


def extract_suggestions_themes(by_page: list[dict]) -> list[str]:
    """Collect all suggestions; surface the most common themes by prefix dedup."""
    seen: list[str] = []
    for page in by_page:
        for s in page.get("suggestions", []):
            seen.append(s)
    # Simple dedup — keep first occurrence of each suggestion (case-insensitive)
    unique: list[str] = []
    seen_lower: set[str] = set()
    for s in seen:
        key = s.lower()[:60]
        if key not in seen_lower:
            seen_lower.add(key)
            unique.append(s)
    return unique[:10]


def render(data: dict) -> str:
    lines: list[str] = []

    dim = data.get("dimension", "unknown").capitalize()
    model = data.get("model", "?")
    rubric_ver = data.get("rubric_version", "?")
    generated = data.get("generated_at", "?")
    pages_scored = data.get("pages_scored", 0)
    avg = data.get("avg_score")
    dist = data.get("distribution", {})
    by_page = data.get("by_page", [])

    lines.append(f"# Rubric Scorer — {dim} Dimension\n")
    lines.append(f"_Generated: {generated} · model: {model} · rubric: v{rubric_ver}_\n")

    # ── Headline ──────────────────────────────────────────────────────────────
    lines.append("## Headline\n")
    avg_str = f"{avg:.2f} / 5" if avg is not None else "n/a"
    lines.append(f"**Average score:** {avg_str} across {pages_scored} pages\n")
    lines.append("**Score distribution:**\n")
    lines.append("```")
    lines.append(sparkline_bar(dist))
    lines.append("```\n")

    # ── Per-page table (lowest first) ─────────────────────────────────────────
    lines.append("## Per-page scores (lowest first)\n")

    scored_pages = [p for p in by_page if "score" in p]
    failed_pages = [p for p in by_page if "_error" in p]

    scored_pages.sort(key=lambda p: (p["score"], p["confidence"] == "high"))

    lines.append("| Page | Cohort | Score | Confidence | Rationale |")
    lines.append("|---|---|---|---|---|")
    for p in scored_pages:
        short_path = p["page"].replace("social-plus-sdk/", "")
        score_emoji = {1: "🔴", 2: "🟠", 3: "🟡", 4: "🟢", 5: "✅"}.get(p["score"], "⚪")
        lines.append(
            f"| `{short_path}` | {p['cohort']} "
            f"| {score_emoji} {p['score']} | {p['confidence']} "
            f"| {p['rationale'][:120]}{'…' if len(p['rationale']) > 120 else ''} |"
        )

    if failed_pages:
        lines.append("")
        lines.append(f"> ⚠️ {len(failed_pages)} page(s) failed to score: {', '.join(p['page'].split('/')[-1] for p in failed_pages)}")

    lines.append("")

    # ── Immediate action items (score ≤ 3) ────────────────────────────────────
    action_pages = [p for p in scored_pages if p["score"] <= 3]
    if action_pages:
        lines.append("## Immediate action items (score ≤ 3)\n")
        for p in action_pages:
            short = p["page"].replace("social-plus-sdk/", "")
            lines.append(f"### `{short}` — score {p['score']}\n")
            lines.append(f"**Rationale:** {p['rationale']}\n")
            if p.get("suggestions"):
                lines.append("**Suggestions:**")
                for s in p["suggestions"]:
                    lines.append(f"- {s}")
            lines.append("")

    # ── Top suggestions (deduplicated themes) ─────────────────────────────────
    lines.append("## Top suggestions across all pages\n")
    themes = extract_suggestions_themes(scored_pages)
    if themes:
        for t in themes:
            lines.append(f"- {t}")
    else:
        lines.append("_No suggestions — all pages scored 5._")
    lines.append("")

    # ── Per-page detail (all pages with suggestions) ──────────────────────────
    pages_with_suggestions = [p for p in scored_pages if p.get("suggestions")]
    if pages_with_suggestions:
        lines.append("## Detailed suggestions by page\n")
        for p in pages_with_suggestions:
            short = p["page"].replace("social-plus-sdk/", "")
            lines.append(f"**`{short}`** (score {p['score']}, {p['confidence']} confidence)")
            for s in p["suggestions"]:
                lines.append(f"- {s}")
            lines.append("")

    lines.append("---")
    lines.append(f"_Generated by `.docs-ops/rubric-scorer/render-report.py`_")

    return "\n".join(lines) + "\n"


HEAT = {5: "✓", 4: "✓", 3: "~", 2: "✗", 1: "✗"}
DIM_ORDER = ["accuracy", "clarity", "cross_platform_parity", "completeness", "examples", "ai_consumability"]
DIM_SHORT = {
    "accuracy": "Acc",
    "clarity": "Cla",
    "cross_platform_parity": "Par",
    "completeness": "Cmp",
    "examples": "Exm",
    "ai_consumability": "AIc",
}


def render_overall(data: dict) -> str:
    lines: list[str] = []

    rubric_ver = data.get("rubric_version", "?")
    generated = data.get("generated_at", "?")
    pages_scored = data.get("pages_scored", 0)
    avg_overall = data.get("avg_overall")
    dist = data.get("distribution", {})
    weights = data.get("weights", {})
    by_page = data.get("by_page", [])  # already sorted worst-first by aggregate.py

    lines.append("# Rubric Scorer — Overall (Weighted)\n")
    lines.append(f"_Generated: {generated} · rubric: v{rubric_ver}_\n")

    # ── Headline ──────────────────────────────────────────────────────────────
    lines.append("## Headline\n")
    avg_str = f"{avg_overall:.2f} / 5" if avg_overall is not None else "n/a"
    lines.append(f"**Average overall score:** {avg_str} across {pages_scored} pages\n")

    lines.append("**Score distribution (floor of weighted overall):**\n")
    lines.append("```")
    lines.append(sparkline_bar(dist))
    lines.append("```\n")

    lines.append("**Weights:**\n")
    for dim in DIM_ORDER:
        w = weights.get(dim, 0)
        lines.append(f"- {DIM_SHORT.get(dim, dim)}: {w:.0%}")
    lines.append("")

    # ── Per-page table ─────────────────────────────────────────────────────────
    lines.append("## Per-page scores (worst first)\n")
    # Header with dimension columns
    dim_headers = " | ".join(f"{DIM_SHORT[d]}" for d in DIM_ORDER)
    lines.append(f"| Page | Cohort | Overall | {dim_headers} |")
    lines.append("|---|---|---|" + "---|" * len(DIM_ORDER))

    for p in by_page:
        short = p["page"].replace("social-plus-sdk/", "")
        overall = p["overall"]
        overall_emoji = {5: "✅", 4: "🟢", 3: "🟡", 2: "🟠", 1: "🔴"}.get(int(overall), "⚪")
        cohort = p.get("cohort", "")
        per_dim = p.get("per_dimension", {})
        dim_cells = " | ".join(
            f"{HEAT.get(per_dim.get(d, {}).get('score', 0), '?')} {per_dim.get(d, {}).get('score', '?')}"
            for d in DIM_ORDER
        )
        lines.append(f"| `{short}` | {cohort} | {overall_emoji} {overall:.2f} | {dim_cells} |")

    lines.append("")

    # ── Action priority section ────────────────────────────────────────────────
    lines.append("## Action priority (3 worst pages)\n")
    for p in by_page[:3]:
        short = p["page"].replace("social-plus-sdk/", "")
        lines.append(f"### `{short}` — overall {p['overall']:.2f}\n")
        per_dim = p.get("per_dimension", {})
        lines.append("| Dimension | Score | Weight | Weighted |")
        lines.append("|---|---|---|---|")
        for dim in DIM_ORDER:
            score = per_dim.get(dim, {}).get("score", "?")
            weight = weights.get(dim, 0)
            weighted = f"{score * weight:.2f}" if isinstance(score, (int, float)) else "?"
            heat = HEAT.get(score, "?") if isinstance(score, int) else "?"
            lines.append(f"| {DIM_SHORT.get(dim, dim)} | {heat} {score} | {weight:.0%} | {weighted} |")
        lines.append("")

    lines.append("---")
    lines.append("_Generated by `.docs-ops/rubric-scorer/aggregate.py` + `render-report.py --overall`_")

    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dimension", default="clarity", help="Dimension name (default: clarity)")
    parser.add_argument("--overall", action="store_true", help="Render overall-latest.json instead of a single dimension")
    parser.add_argument("--input", default=None, help="Input JSON path")
    parser.add_argument("--output", default=None, help="Output markdown path")
    args = parser.parse_args(argv)

    if args.overall:
        in_path = pathlib.Path(args.input) if args.input else SCRIPT_DIR / "results" / "overall-latest.json"
        out_path = pathlib.Path(args.output) if args.output else SCRIPT_DIR / "results" / "overall-latest-report.md"
        if not in_path.exists():
            print(f"ERROR: {in_path} not found — run aggregate.py first.", file=sys.stderr)
            sys.exit(1)
        data = json.loads(in_path.read_text(encoding="utf-8"))
        report = render_overall(data)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(report, encoding="utf-8")
        print(f"Report written → {out_path.relative_to(REPO_ROOT)}")
        return 0

    in_path = (
        pathlib.Path(args.input)
        if args.input
        else SCRIPT_DIR / "results" / f"{args.dimension}-latest.json"
    )
    out_path = (
        pathlib.Path(args.output)
        if args.output
        else SCRIPT_DIR / "results" / f"{args.dimension}-latest-report.md"
    )

    if not in_path.exists():
        print(f"ERROR: input file not found: {in_path}", file=sys.stderr)
        print("Run score.py first.", file=sys.stderr)
        sys.exit(1)

    data = json.loads(in_path.read_text(encoding="utf-8"))
    report = render(data)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(report, encoding="utf-8")
    print(f"Report written → {out_path.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
