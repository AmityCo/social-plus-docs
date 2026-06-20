#!/usr/bin/env python3
"""
Docs-quality snapshot script.

Reads all 8 drift/doc-as-test reports, groups issues by customer cohort,
and writes a structured snapshot to .docs-ops/dashboards/snapshots/<YYYY-MM-DD>.json.

Usage:
    python3 .docs-ops/dashboards/snapshot.py
    python3 .docs-ops/dashboards/snapshot.py --date 2026-05-19   # override date

Run weekly (or on demand). Snapshots are committed for historical audit.
"""
from __future__ import annotations
import argparse
import json
import pathlib
import datetime
import sys

SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent  # social-plus-docs/

COHORT_TAGS = SCRIPT_DIR / "cohort-tags.json"
SNAPSHOTS_DIR = SCRIPT_DIR / "snapshots"

# Drift report paths
DRIFT_REPORTS = {
    "typescript": REPO_ROOT / ".docs-ops/evals/ts-accuracy-drift.json",
    "ios":        REPO_ROOT / ".docs-ops/evals/ios-accuracy-drift.json",
    "android":    REPO_ROOT / ".docs-ops/evals/android-accuracy-drift.json",
    "flutter":    REPO_ROOT / ".docs-ops/evals/flutter-accuracy-drift.json",
}

# Doc-as-test report paths
DAT_REPORTS = {
    "typescript": REPO_ROOT / ".docs-ops/integration-tests/results/latest.json",
    "flutter":    REPO_ROOT / ".docs-ops/integration-tests/flutter/results/latest.json",
    "android":    REPO_ROOT / ".docs-ops/integration-tests/android/results/latest.json",
    "ios":        REPO_ROOT / ".docs-ops/integration-tests/ios/results/latest.json",
}

COHORT_KEYS = ["eastern", "western", "shared", "other"]


def resolve_cohort_tags(repo_root: pathlib.Path) -> dict[str, set[str]]:
    """Load cohort-tags.json and resolve enumerate: entries."""
    raw = json.loads(COHORT_TAGS.read_text(encoding="utf-8"))
    cohorts: dict[str, set[str]] = {"eastern": set(), "western": set(), "shared": set()}

    mapping = {
        "eastern_chat_heavy": "eastern",
        "western_social_heavy": "western",
        "shared": "shared",
    }

    for tag_key, cohort in mapping.items():
        for entry in raw.get(tag_key, []):
            if entry.startswith("enumerate:"):
                subdir = repo_root / entry[len("enumerate:"):]
                if subdir.exists():
                    for mdx in sorted(subdir.glob("*.mdx")):
                        cohorts[cohort].add(str(mdx.relative_to(repo_root)))
            else:
                cohorts[cohort].add(entry)

    return cohorts


def classify_page(page: str, cohorts: dict[str, set[str]]) -> str:
    for cohort in ("eastern", "western", "shared"):
        if page in cohorts[cohort]:
            return cohort
    return "other"


def empty_cohort_counts() -> dict:
    return {k: 0 for k in COHORT_KEYS}


def snapshot_drift(cohorts: dict[str, set[str]]) -> dict:
    """Read all 4 regex-drift reports and group by cohort."""
    result = {}
    for platform, path in DRIFT_REPORTS.items():
        total = 0
        by_cohort = empty_cohort_counts()
        if path.exists():
            report = json.loads(path.read_text(encoding="utf-8"))
            issues_by_file = report.get("issues_by_file", {})
            for file_path, issues in issues_by_file.items():
                count = len(issues) if isinstance(issues, list) else int(issues)
                total += count
                cohort = classify_page(file_path, cohorts)
                by_cohort[cohort] += count
        result[platform] = {"total": total, "by_cohort": by_cohort}
    return result


def build_by_page_ios(report: dict) -> dict[str, dict]:
    """Construct a by_page map for the iOS report (which lacks a by_page key)."""
    by_page: dict[str, dict] = {}

    def ensure(page: str) -> dict:
        if page not in by_page:
            by_page[page] = {"passed": 0, "failed": 0, "skipped": 0, "warnings": 0}
        return by_page[page]

    for item in report.get("passed", []):
        ensure(item["source_page"])["passed"] += 1
    for item in report.get("skipped", []):
        ensure(item["source_page"])["skipped"] += 1
    for item in report.get("failures", []):
        ensure(item["source_page"])["failed"] += 1
    for item in report.get("warnings", []):
        ensure(item["source_page"])["warnings"] += 1

    return by_page


def snapshot_dat(cohorts: dict[str, set[str]]) -> dict:
    """Read all 4 doc-as-test reports and group by cohort."""
    result = {}
    for platform, path in DAT_REPORTS.items():
        if not path.exists():
            result[platform] = {
                "passed": 0, "skipped": 0, "failed": 0, "warnings": 0,
                "by_cohort": {k: {"passed": 0, "failed": 0, "skipped": 0} for k in COHORT_KEYS},
            }
            continue

        report = json.loads(path.read_text(encoding="utf-8"))
        stats = report.get("stats", {})

        passed = stats.get("blocks_passed", 0)
        skipped = stats.get("blocks_skipped", 0)
        failed = stats.get("blocks_failed", 0)
        warnings = (
            stats.get("total_warnings", 0)
            or stats.get("blocks_warned", 0)
        )

        # by_page: use native field or construct for iOS
        if platform == "ios":
            by_page = build_by_page_ios(report)
        else:
            by_page = report.get("by_page", {})

        by_cohort = {k: {"passed": 0, "failed": 0, "skipped": 0} for k in COHORT_KEYS}
        for page, page_stats in by_page.items():
            cohort = classify_page(page, cohorts)
            by_cohort[cohort]["passed"] += page_stats.get("passed", 0)
            by_cohort[cohort]["failed"] += page_stats.get("failed", 0)
            by_cohort[cohort]["skipped"] += page_stats.get("skipped", 0)

        result[platform] = {
            "passed": passed,
            "skipped": skipped,
            "failed": failed,
            "warnings": warnings,
            "by_cohort": by_cohort,
        }
    return result


def health_score(dat_by_cohort: dict, cohort: str) -> float | None:
    """Compute health score for a cohort across all platforms: 1.0 - (failures / total_blocks)."""
    total = 0
    failures = 0
    for platform_dat in dat_by_cohort.values():
        bc = platform_dat.get("by_cohort", {}).get(cohort, {})
        total += bc.get("passed", 0) + bc.get("failed", 0)
        failures += bc.get("failed", 0)
    if total == 0:
        return None
    return round(1.0 - failures / total, 4)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", default=None, help="Override snapshot date (YYYY-MM-DD)")
    args = parser.parse_args(argv)

    snap_date = args.date or datetime.date.today().isoformat()
    run_at = datetime.datetime.now(datetime.UTC).isoformat(timespec="seconds").replace("+00:00", "Z")

    cohorts = resolve_cohort_tags(REPO_ROOT)
    print(f"Cohort pages resolved: eastern={len(cohorts['eastern'])} western={len(cohorts['western'])} shared={len(cohorts['shared'])}")

    drift = snapshot_drift(cohorts)
    dat = snapshot_dat(cohorts)

    total_drift = sum(v["total"] for v in drift.values())
    total_failures = sum(v["failed"] for v in dat.values())

    snapshot = {
        "snapshot_date": snap_date,
        "snapshot_run_at": run_at,
        "regex_drift": drift,
        "doc_as_test": dat,
        "summary": {
            "total_drift_issues": total_drift,
            "total_doc_as_test_failures": total_failures,
            "healthy": total_drift == 0 and total_failures == 0,
            "eastern_health_score": health_score(dat, "eastern"),
            "western_health_score": health_score(dat, "western"),
        },
    }

    SNAPSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = SNAPSHOTS_DIR / f"{snap_date}.json"
    out_path.write_text(json.dumps(snapshot, indent=2) + "\n", encoding="utf-8")
    print(f"Snapshot written → {out_path.relative_to(REPO_ROOT)}")
    print(f"  total_drift={total_drift}  total_failures={total_failures}  healthy={snapshot['summary']['healthy']}")
    print(f"  eastern_health={snapshot['summary']['eastern_health_score']}  western_health={snapshot['summary']['western_health_score']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
