#!/usr/bin/env python3
"""
Rubric scorer — AGGREGATE

Combines 5 LLM-judge dimension scores + derived accuracy dimension into a
per-page weighted overall score per rubric.json weights.

Writes results/overall-latest.json and results/overall-latest-report.md.

Usage:
    python3 .docs-ops/rubric-scorer/aggregate.py
    python3 .docs-ops/rubric-scorer/aggregate.py --archive
"""
from __future__ import annotations
import argparse
import datetime
import json
import pathlib
import shutil
import sys

SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent
RESULTS_DIR = SCRIPT_DIR / "results"
HISTORY_DIR = RESULTS_DIR / "history"
RUBRIC_PATH = SCRIPT_DIR.parent / "rubric.json"

LLM_DIMENSIONS = ["clarity", "parity", "completeness", "examples", "ai-consumability"]
# Map file-slug → rubric key
DIM_KEY_MAP = {
    "clarity": "clarity",
    "parity": "cross_platform_parity",
    "completeness": "completeness",
    "examples": "examples",
    "ai-consumability": "ai_consumability",
}

DRIFT_GLOB = str(REPO_ROOT / ".docs-ops" / "evals" / "*-accuracy-drift.json")
DAT_LATEST_FILES = [
    REPO_ROOT / ".docs-ops" / "integration-tests" / "results" / "latest.json",
    REPO_ROOT / ".docs-ops" / "integration-tests" / "flutter" / "results" / "latest.json",
    REPO_ROOT / ".docs-ops" / "integration-tests" / "android" / "results" / "latest.json",
    REPO_ROOT / ".docs-ops" / "integration-tests" / "ios" / "results" / "latest.json",
]


def load_rubric_weights() -> dict[str, float]:
    rubric = json.loads(RUBRIC_PATH.read_text())
    return {key: val["weight"] for key, val in rubric["dimensions"].items()}


def load_rubric_version() -> str:
    return json.loads(RUBRIC_PATH.read_text())["version"]


def load_llm_scores() -> dict[str, dict[str, int | str]]:
    """Returns {page_path: {dim_rubric_key: score, 'cohort': cohort}}"""
    scores: dict[str, dict[str, int | str]] = {}
    for dim_slug in LLM_DIMENSIONS:
        path = RESULTS_DIR / f"{dim_slug}-latest.json"
        if not path.exists():
            print(f"  WARNING: {path} not found — skipping dimension {dim_slug}", file=sys.stderr)
            continue
        d = json.loads(path.read_text())
        rubric_key = DIM_KEY_MAP[dim_slug]
        for page_entry in d.get("by_page", []):
            page = page_entry["page"]
            scores.setdefault(page, {})
            scores[page][rubric_key] = page_entry["score"]
            if "cohort" not in scores[page] and "cohort" in page_entry:
                scores[page]["cohort"] = page_entry["cohort"]
    return scores


def _load_drift_flagged() -> set[str]:
    """Returns set of page paths that appear in any regex drift report."""
    import glob as _glob
    flagged: set[str] = set()
    for df in _glob.glob(DRIFT_GLOB):
        try:
            d = json.loads(pathlib.Path(df).read_text())
            for item in d.get("drift", []):
                f = item.get("file", "")
                if f:
                    flagged.add(f)
        except Exception:
            pass
    return flagged


def _load_dat_signals() -> tuple[set[str], set[str]]:
    """Returns (failed_pages, warned_pages) — page paths with any failure or warning."""
    failures: set[str] = set()
    warnings: set[str] = set()
    for dat_path in DAT_LATEST_FILES:
        if not dat_path.exists():
            continue
        try:
            d = json.loads(dat_path.read_text())
            for f in d.get("failures", []):
                pg = f.get("source_page", "")
                if pg:
                    failures.add(pg)
            for w in d.get("warnings", []):
                pg = w.get("source_page", "")
                if pg:
                    warnings.add(pg)
        except Exception:
            pass
    return failures, warnings


def derive_accuracy_score(page: str, drift_flagged: set[str], dat_failures: set[str], dat_warnings: set[str]) -> int:
    """Derive 1-5 accuracy score per task spec rules."""
    score = 5
    if page in drift_flagged:
        score -= 2
    if page in dat_failures:
        score -= 2
    if page in dat_warnings:
        score -= 1
    return max(1, score)


def compute_overall(per_dim: dict[str, int], weights: dict[str, float]) -> float:
    """Weighted sum. Missing dimensions default to 3 (middle) with a warning."""
    total = 0.0
    for rubric_key, weight in weights.items():
        score = per_dim.get(rubric_key)
        if score is None:
            print(f"  WARNING: missing score for dimension '{rubric_key}' — defaulting to 3", file=sys.stderr)
            score = 3
        total += score * weight
    return round(total, 2)


def main() -> None:
    parser = argparse.ArgumentParser(description="Aggregate rubric dimension scores into overall-latest.json")
    parser.add_argument("--archive", action="store_true", help="Copy result to results/history/<date>-overall.json")
    args = parser.parse_args()

    weights = load_rubric_weights()
    rubric_version = load_rubric_version()

    assert abs(sum(weights.values()) - 1.0) < 0.001, f"Rubric weights do not sum to 1.0: {sum(weights.values())}"

    llm_scores = load_llm_scores()
    drift_flagged = _load_drift_flagged()
    dat_failures, dat_warnings = _load_dat_signals()

    # Only score pages present in ALL LLM dimension results
    all_pages: set[str] | None = None
    for dim_slug in LLM_DIMENSIONS:
        path = RESULTS_DIR / f"{dim_slug}-latest.json"
        if not path.exists():
            continue
        d = json.loads(path.read_text())
        dim_pages = {e["page"] for e in d.get("by_page", [])}
        all_pages = dim_pages if all_pages is None else all_pages & dim_pages

    if not all_pages:
        print("ERROR: no pages common to all dimension results.", file=sys.stderr)
        sys.exit(1)

    by_page = []
    for page in sorted(all_pages):
        per_dim_raw = llm_scores.get(page, {})
        accuracy = derive_accuracy_score(page, drift_flagged, dat_failures, dat_warnings)
        per_dim_raw["accuracy"] = accuracy

        overall = compute_overall(per_dim_raw, weights)

        per_dimension = {}
        for rubric_key, weight in weights.items():
            score = per_dim_raw.get(rubric_key)
            source = "derived" if rubric_key == "accuracy" else "llm-judge"
            per_dimension[rubric_key] = {"score": score, "source": source}

        by_page.append({
            "page": page,
            "cohort": per_dim_raw.get("cohort", ""),
            "overall": overall,
            "per_dimension": per_dimension,
        })

    # Sort worst-first
    by_page.sort(key=lambda x: x["overall"])

    avg_overall = round(sum(p["overall"] for p in by_page) / len(by_page), 2)
    distribution: dict[str, int] = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0}
    for p in by_page:
        bucket = str(min(5, max(1, int(p["overall"]))))
        distribution[bucket] = distribution.get(bucket, 0) + 1

    output = {
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "rubric_version": rubric_version,
        "weights": weights,
        "pages_scored": len(by_page),
        "avg_overall": avg_overall,
        "distribution": distribution,
        "by_page": by_page,
    }

    out_path = RESULTS_DIR / "overall-latest.json"
    out_path.write_text(json.dumps(output, indent=2) + "\n")
    print(f"Aggregated {len(by_page)} pages → {out_path}")
    print(f"  avg_overall={avg_overall}  dist={distribution}")

    if args.archive:
        HISTORY_DIR.mkdir(exist_ok=True)
        date_str = datetime.date.today().isoformat()
        archive_path = HISTORY_DIR / f"{date_str}-overall.json"
        shutil.copy(out_path, archive_path)
        print(f"  archived → {archive_path}")


if __name__ == "__main__":
    main()
