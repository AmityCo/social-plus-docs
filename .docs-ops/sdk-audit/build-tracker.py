#!/usr/bin/env python3
"""Build or refresh the SDK page-by-page accuracy tracker."""
from __future__ import annotations

import csv
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent
TRACKER_PATH = SCRIPT_DIR / "tracker.csv"

COLUMNS = [
    "path",
    "area",
    "section",
    "status",
    "source_verified",
    "snippets_verified",
    "info_verified",
    "last_reviewed",
    "reviewer",
    "evidence",
    "notes",
]

REVIEW_COLUMNS = [
    "status",
    "source_verified",
    "snippets_verified",
    "info_verified",
    "last_reviewed",
    "reviewer",
    "evidence",
    "notes",
]

DEFAULT_REVIEW = {
    "status": "not_started",
    "source_verified": "no",
    "snippets_verified": "no",
    "info_verified": "no",
    "last_reviewed": "",
    "reviewer": "",
    "evidence": "",
    "notes": "",
}


def classify(path: str) -> tuple[str, str]:
    parts = path.split("/")
    if len(parts) < 3:
        return "root", ""
    area = parts[1]
    if area == "changelogs":
        return "changelogs", ""
    section = parts[2] if len(parts) > 3 else ""
    return area, section


def existing_reviews() -> dict[str, dict[str, str]]:
    if not TRACKER_PATH.exists():
        return {}
    with TRACKER_PATH.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return {
            row["path"]: {col: row.get(col, DEFAULT_REVIEW[col]) for col in REVIEW_COLUMNS}
            for row in reader
            if row.get("path")
        }


def sdk_pages() -> list[str]:
    return [
        str(path.relative_to(REPO_ROOT))
        for path in sorted((REPO_ROOT / "social-plus-sdk").glob("**/*.mdx"))
    ]


def build_rows() -> list[dict[str, str]]:
    reviews = existing_reviews()
    rows = []
    for path in sdk_pages():
        area, section = classify(path)
        row = {
            "path": path,
            "area": area,
            "section": section,
        }
        row.update(DEFAULT_REVIEW)
        row.update(reviews.get(path, {}))
        rows.append(row)
    return rows


def main() -> int:
    rows = build_rows()
    TRACKER_PATH.parent.mkdir(parents=True, exist_ok=True)
    with TRACKER_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {TRACKER_PATH.relative_to(REPO_ROOT)} with {len(rows)} SDK pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
