#!/usr/bin/env python3
"""
Render a pr-comment-data.json into a structured markdown PR comment.

Usage:
    python3 render-pr-comment.py <input.json> [output.md]
"""
from __future__ import annotations
import json
import sys
from pathlib import Path


def render(data: dict) -> str:
    sdk_sha      = data.get("sdk_sha", "unknown")
    sdk_msg      = data.get("sdk_msg", "")
    baseline_sha = data.get("baseline_sha", "unknown")
    diff         = data.get("diff", {})
    changes      = data.get("changes", [])

    added   = diff.get("added", [])
    removed = diff.get("removed", [])
    renamed = diff.get("renamed", [])

    lines: list[str] = []
    lines.append("## 🤖 SDK Drift Watcher — daily auto-update\n")
    lines.append(f"**SDK**: AmityTypescriptSDK @ `{sdk_sha}` ({sdk_msg})")
    lines.append(f"**Compared against**: `.docs-ops/sdk-surface/typescript.json` @ commit `{baseline_sha}`\n")

    lines.append("### Surface diff\n")
    lines.append(f"- **Added** ({len(added)}): new APIs since last run — not auto-documented; review for whether they need docs")
    lines.append(f"- **Removed** ({len(removed)}): APIs no longer in SDK — may need docs cleanup")
    lines.append(f"- **Renamed** ({len(renamed)}): refs auto-rewritten in docs (clean substitutions only)\n")

    if renamed:
        lines.append("<details><summary>Renamed APIs</summary>\n")
        for r in renamed:
            lines.append(f"- `{r['from']}` → `{r['to']}` _(confidence: {r['confidence']})_")
        lines.append("\n</details>\n")

    lines.append("### Auto-rewrites applied\n")
    if changes:
        # Group by file
        by_file: dict[str, list] = {}
        for c in changes:
            by_file.setdefault(c["file"], []).append(c)
        for fname, file_changes in sorted(by_file.items()):
            for c in file_changes:
                lines.append(f"- `{fname}:{c['line']}` — `{c['from']}` → `{c['to']}`")
    else:
        lines.append("_No auto-rewrites were applied._")
    lines.append("")

    lines.append("### Needs your review\n")
    if removed:
        lines.append("**Removed APIs that may affect documented code blocks:**\n")
        for ref in removed[:20]:
            lines.append(f"- `{ref}`")
        if len(removed) > 20:
            lines.append(f"\n_…and {len(removed) - 20} more. See full diff in `pr-comment-data.json`._")
    else:
        lines.append("_No removed APIs flagged._")
    lines.append("")

    if added:
        lines.append("**New APIs that may warrant new docs:**\n")
        for ref in added[:15]:
            lines.append(f"- `{ref}`")
        if len(added) > 15:
            lines.append(f"\n_…and {len(added) - 15} more._")
        lines.append("")

    lines.append("### What this PR is\n")
    lines.append(
        "This PR was opened by the daily SDK drift watcher. The auto-rewrites are "
        "signature-verified against the new SDK surface. The REMOVED items above are "
        "flagged for your judgment — they may be intentional removals, in which case "
        "the docs need cleanup, or unintentional, in which case the SDK PR needs review.\n"
    )

    lines.append("### How to merge\n")
    lines.append(
        "This is a draft PR. Convert to ready, run the gate locally if needed (`python3 "
        ".docs-ops/ci/check-drift.py --base origin/main`), then merge. No further bot "
        "action needed."
    )

    return "\n".join(lines) + "\n"


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: render-pr-comment.py <input.json> [output.md]", file=sys.stderr)
        sys.exit(1)

    in_path  = Path(sys.argv[1])
    out_path = Path(sys.argv[2]) if len(sys.argv) > 2 else in_path.with_suffix(".md")

    data    = json.loads(in_path.read_text())
    comment = render(data)

    out_path.write_text(comment)
    print(f"Comment written → {out_path}")


if __name__ == "__main__":
    main()
