#!/usr/bin/env python3
"""
Rubric scorer — Phase 1: PREPARE

Reads pages from a pages JSON file, renders one prompt file per page into
results/pending/<dimension>-<slug>.json. The pending files are the scoring
tasks for the agent to complete (Copilot CLI, Claude Code, or any agent).

Pending files are gitignored (regenerable). Scored files are committed.

Usage:
    python3 .docs-ops/rubric-scorer/prepare.py --dimension clarity
    python3 .docs-ops/rubric-scorer/prepare.py --dimension clarity --pages pages-pilot.json

After running, the agent reads each results/pending/<dimension>-<slug>.json
and writes a score to results/scored/<dimension>-<slug>.json.
Then run collect.py to aggregate.
"""
from __future__ import annotations
import argparse
import datetime
import hashlib
import json
import pathlib
import re
import sys

SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent
PENDING_DIR = SCRIPT_DIR / "results" / "pending"
RUBRIC_PATH = SCRIPT_DIR.parent / "rubric.json"


def load_rubric_version() -> str:
    if RUBRIC_PATH.exists():
        return json.loads(RUBRIC_PATH.read_text())["version"]
    return "unknown"


def load_prompt_template(dimension: str) -> str:
    prompt_path = SCRIPT_DIR / "prompts" / f"{dimension}.md"
    if not prompt_path.exists():
        print(f"ERROR: no prompt file for dimension '{dimension}' at {prompt_path}", file=sys.stderr)
        sys.exit(1)
    return prompt_path.read_text(encoding="utf-8")


def load_pages(pages_file: pathlib.Path) -> list[dict]:
    return json.loads(pages_file.read_text(encoding="utf-8"))["pages"]


def page_slug(page_path: str) -> str:
    """Convert a page path to a short file-safe slug."""
    name = pathlib.Path(page_path).stem  # e.g. send-a-message
    parent = pathlib.Path(page_path).parent.name  # e.g. message-creation
    return re.sub(r"[^a-z0-9-]", "-", f"{parent}-{name}".lower())[:60]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dimension", required=True, help="Dimension to score (e.g. clarity)")
    parser.add_argument("--pages", default=None, help="Pages JSON file (default: pages-pilot.json)")
    args = parser.parse_args(argv)

    pages_file = pathlib.Path(args.pages) if args.pages else SCRIPT_DIR / "pages-pilot.json"
    if not pages_file.is_absolute():
        pages_file = SCRIPT_DIR / pages_file

    template = load_prompt_template(args.dimension)
    pages = load_pages(pages_file)
    rubric_version = load_rubric_version()
    created_at = datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z"

    PENDING_DIR.mkdir(parents=True, exist_ok=True)

    written = 0
    skipped = 0

    for page_entry in pages:
        page_path = page_entry.get("page") or page_entry.get("path")
        cohort = page_entry.get("cohort", "unknown")
        full_path = REPO_ROOT / page_path

        if not full_path.exists():
            print(f"  SKIP (not found): {page_path}")
            skipped += 1
            continue

        content = full_path.read_text(encoding="utf-8")
        prompt = template.replace("{page_content}", content)
        prompt_hash = hashlib.sha256(prompt.encode("utf-8")).hexdigest()

        slug = page_slug(page_path)
        out_path = PENDING_DIR / f"{args.dimension}-{slug}.json"

        payload = {
            "dimension": args.dimension,
            "rubric_version": rubric_version,
            "page": page_path,
            "cohort": cohort,
            "prompt": prompt,
            "prompt_hash": prompt_hash,
            "created_at": created_at,
            "scored_file": f"results/scored/{args.dimension}-{slug}.json",
        }

        out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"  prepared: {out_path.name}")
        written += 1

    print(f"\nPrepared {written} prompt file(s) → {PENDING_DIR.relative_to(REPO_ROOT)}")
    if skipped:
        print(f"Skipped {skipped} page(s) (file not found)")
    print("Next: agent reads each pending file and writes scored/<dimension>-<slug>.json")
    print("Then: python3 collect.py --dimension clarity")
    return 0


if __name__ == "__main__":
    sys.exit(main())
