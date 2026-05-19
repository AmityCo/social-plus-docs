#!/usr/bin/env python3
"""
Rubric scorer — Phase 3: COLLECT

Reads all agent-scored files from results/scored/<dimension>-*.json and
aggregates them into results/<dimension>-latest.json.

Run this after the agent has scored all pending files.
Optionally archives the results to results/history/<YYYY-MM-DD>-<dimension>.json.

Usage:
    python3 .docs-ops/rubric-scorer/collect.py --dimension clarity
    python3 .docs-ops/rubric-scorer/collect.py --dimension clarity --archive

Schema of each scored file (written by the agent):
{
  "dimension": "clarity",
  "page": "social-plus-sdk/...",
  "cohort": "eastern",
  "score": 3,
  "rationale": "...",
  "confidence": "low|medium|high",
  "suggestions": ["...", "..."],     // omit if score == 5
  "_prompt_hash": "<sha256>",        // from the pending file
  "_scored_by": "copilot-cli",       // agent identifier
  "_scored_at": "2026-05-19T..."     // ISO timestamp
}
"""
from __future__ import annotations
import argparse
import datetime
import json
import pathlib
import sys

SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent
SCORED_DIR = SCRIPT_DIR / "results" / "scored"
HISTORY_DIR = SCRIPT_DIR / "results" / "history"
RUBRIC_PATH = SCRIPT_DIR.parent / "rubric.json"


def load_rubric_version() -> str:
    if RUBRIC_PATH.exists():
        return json.loads(RUBRIC_PATH.read_text())["version"]
    return "unknown"


def validate_scored_file(data: dict, path: pathlib.Path) -> list[str]:
    """Return list of validation errors (empty = valid)."""
    errors = []
    if not data.get("page"):
        errors.append("missing 'page'")
    score = data.get("score")
    if score is None or not (1 <= int(score) <= 5):
        errors.append(f"invalid score: {score!r}")
    if data.get("confidence") not in ("low", "medium", "high"):
        errors.append(f"invalid confidence: {data.get('confidence')!r}")
    if not data.get("rationale"):
        errors.append("missing 'rationale'")
    if not data.get("_prompt_hash"):
        errors.append("missing '_prompt_hash'")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dimension", required=True, help="Dimension to collect (e.g. clarity)")
    parser.add_argument("--archive", action="store_true", help="Also write to results/history/<date>-<dimension>.json")
    args = parser.parse_args(argv)

    pattern = f"{args.dimension}-*.json"
    scored_files = sorted(SCORED_DIR.glob(pattern))

    if not scored_files:
        print(f"ERROR: no scored files found in {SCORED_DIR.relative_to(REPO_ROOT)} matching {pattern}", file=sys.stderr)
        print("Run the agent scoring step first, then collect.", file=sys.stderr)
        sys.exit(1)

    by_page = []
    scores_seen = []
    errors_found = 0
    rubric_version = load_rubric_version()

    for path in scored_files:
        data = json.loads(path.read_text(encoding="utf-8"))
        errs = validate_scored_file(data, path)
        if errs:
            print(f"  WARN {path.name}: {'; '.join(errs)}")
            errors_found += 1
            continue

        entry: dict = {
            "page": data["page"],
            "cohort": data.get("cohort", "unknown"),
            "score": int(data["score"]),
            "rationale": data["rationale"],
            "confidence": data["confidence"],
        }
        if data.get("suggestions"):
            entry["suggestions"] = data["suggestions"]
        # carry audit fields through
        entry["_prompt_hash"] = data["_prompt_hash"]
        entry["_scored_by"] = data.get("_scored_by", "unknown")
        entry["_scored_at"] = data.get("_scored_at", "unknown")

        by_page.append(entry)
        scores_seen.append(int(data["score"]))

    pages_scored = len(by_page)
    avg_score = round(sum(scores_seen) / len(scores_seen), 2) if scores_seen else None
    distribution = {str(k): scores_seen.count(k) for k in range(1, 6)}

    output = {
        "generated_at": datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "dimension": args.dimension,
        "rubric_version": rubric_version,
        "pages_scored": pages_scored,
        "avg_score": avg_score,
        "distribution": distribution,
        "by_page": by_page,
    }

    out_path = SCRIPT_DIR / "results" / f"{args.dimension}-latest.json"
    out_path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(f"Collected {pages_scored} scores → {out_path.relative_to(REPO_ROOT)}")
    print(f"  avg={avg_score}  dist={distribution}")
    if errors_found:
        print(f"  {errors_found} file(s) had validation errors and were skipped")

    if args.archive:
        HISTORY_DIR.mkdir(parents=True, exist_ok=True)
        date_str = datetime.date.today().isoformat()
        archive_path = HISTORY_DIR / f"{date_str}-{args.dimension}.json"
        archive_path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
        print(f"  archived → {archive_path.relative_to(REPO_ROOT)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
