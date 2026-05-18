#!/usr/bin/env python3
"""
Docs-ops drift gate.

Compares the docs-accuracy drift report between a baseline ref (default
`origin/main`) and the current working tree. Blocks if NEW drift was
introduced — even if total count is flat/lower, any new (file, ref) pair
that didn't exist on baseline counts as regression.

Why "new pairs" not just total: net-zero churn (fix 5 old issues, add 5
new ones) is a real failure mode — the surface area of bugs shifts even
though the count holds. The gate catches that.

Usage:
  python3 .docs-ops/ci/check-drift.py                      # default: base origin/main
  python3 .docs-ops/ci/check-drift.py --base main          # base local main
  python3 .docs-ops/ci/check-drift.py --json-out delta.json # write delta JSON
  python3 .docs-ops/ci/check-drift.py --skip-fetch         # skip git fetch step

Exit codes:
  0 — no regression (drift held or improved AND no new pairs)
  1 — regression detected (new pairs introduced OR script failure)
  2 — environmental failure (extractor crashed, can't reach base, etc.)
"""
from __future__ import annotations
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent  # .docs-ops/ci
DOCS_OPS_ROOT = SCRIPT_DIR.parent              # .docs-ops
REPO_ROOT = DOCS_OPS_ROOT.parent               # repo root (social-plus-docs)

# Extractor + validator paths, relative to repo root.
TS_EXTRACTOR = ".docs-ops/extractors/typescript-extractor.py"
TS_VALIDATOR = ".docs-ops/validators/ts-accuracy-validator.py"
TS_DRIFT_REPORT = ".docs-ops/evals/ts-accuracy-drift.json"


class ScriptError(Exception):
    """Raised for environmental / non-drift failures (exit code 2)."""


def run(cmd: list[str], cwd: Path, capture: bool = True, check: bool = True, env: dict | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=capture,
        text=True,
        check=check,
        env=env,
    )


def resolve_base(base: str, skip_fetch: bool) -> str:
    """Resolve the base ref to a commit SHA. Fetch if needed and not skipped."""
    if not skip_fetch and base.startswith("origin/"):
        try:
            run(["git", "fetch", "origin", base.removeprefix("origin/")], cwd=REPO_ROOT, check=False)
        except FileNotFoundError as e:
            raise ScriptError(f"git not found: {e}") from e
    try:
        result = run(["git", "rev-parse", "--verify", base], cwd=REPO_ROOT)
    except subprocess.CalledProcessError as e:
        raise ScriptError(
            f"can't resolve base ref '{base}'. Run `git fetch` and verify the ref exists. "
            f"git stderr: {e.stderr.strip()}"
        ) from e
    return result.stdout.strip()


@contextmanager
def temp_worktree(ref: str):
    """Create a temp git worktree at `ref`. Cleans up on exit even if extractor crashes."""
    tmp = Path(tempfile.mkdtemp(prefix="docs-ops-baseline-"))
    try:
        run(["git", "worktree", "add", "--detach", str(tmp), ref], cwd=REPO_ROOT)
        yield tmp
    finally:
        # Force-remove, then prune in case the dir was already gone.
        try:
            run(["git", "worktree", "remove", "--force", str(tmp)], cwd=REPO_ROOT, check=False)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
            run(["git", "worktree", "prune"], cwd=REPO_ROOT, check=False)


def run_drift_pipeline(at: Path) -> dict | None:
    """Run extractor + validator inside `at`. Return parsed drift report, or None if not present.

    Sets SP_SDKS_ROOT env var so the extractor finds the real SDK source even when `at`
    is a temp worktree (in which case the worktree's parent dir is NOT the sp-sdks repo
    layout the extractor assumes by default).
    """
    extractor = at / TS_EXTRACTOR
    validator = at / TS_VALIDATOR
    report_path = at / TS_DRIFT_REPORT

    if not extractor.exists() or not validator.exists():
        # Baseline predates the docs-ops system. Treat as empty drift.
        return None

    # The real SDK source root is the parent of the actual docs repo (not the worktree's parent).
    env = os.environ.copy()
    env["SP_SDKS_ROOT"] = str(REPO_ROOT.parent)

    try:
        run(["python3", str(extractor)], cwd=at, capture=True, env=env)
        run(["python3", str(validator)], cwd=at, capture=True, env=env)
    except subprocess.CalledProcessError as e:
        raise ScriptError(
            f"extractor or validator failed in {at}:\n"
            f"  cmd: {e.cmd}\n"
            f"  exit: {e.returncode}\n"
            f"  stderr: {e.stderr.strip() if e.stderr else '(none)'}"
        ) from e

    if not report_path.exists():
        raise ScriptError(f"expected drift report at {report_path} after validator run, not found")

    try:
        return json.loads(report_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ScriptError(f"drift report at {report_path} is not valid JSON: {e}") from e


def pair_set(report: dict | None) -> set[tuple[str, str]]:
    """Return the set of (file, ref) pairs in the report. Line numbers excluded (they shift)."""
    if not report:
        return set()
    out = set()
    for file, issues in report.get("issues_by_file", {}).items():
        for i in issues:
            ref = i.get("ref") or f"import {i.get('import_name', '?')}"
            out.add((file, ref))
    return out


def total_count(report: dict | None) -> int:
    if not report:
        return 0
    return report.get("stats", {}).get("total_issues", 0)


def file_count(report: dict | None) -> int:
    if not report:
        return 0
    return report.get("stats", {}).get("files_with_issues", 0)


def compute_delta(baseline: dict | None, candidate: dict | None, base_ref: str) -> dict:
    base_pairs = pair_set(baseline)
    cand_pairs = pair_set(candidate)
    new_pairs = sorted(cand_pairs - base_pairs)
    resolved_pairs = sorted(base_pairs - cand_pairs)

    base_total = total_count(baseline)
    cand_total = total_count(candidate)

    regressed = len(new_pairs) > 0
    return {
        "base_ref": base_ref,
        "baseline_total": base_total,
        "candidate_total": cand_total,
        "delta_total": cand_total - base_total,
        "baseline_files": file_count(baseline),
        "candidate_files": file_count(candidate),
        "new_pairs": [{"file": f, "ref": r} for f, r in new_pairs],
        "resolved_pairs": [{"file": f, "ref": r} for f, r in resolved_pairs],
        "regressed": regressed,
        "baseline_predates_system": baseline is None,
    }


def print_summary(delta: dict) -> None:
    bar = "═" * 60
    print(bar)
    print("  Docs-Ops Drift Check")
    print(bar)
    print(f"  Base: {delta['base_ref']}")
    if delta["baseline_predates_system"]:
        print("        (baseline predates docs-ops; treated as zero drift)")
    print(f"  Baseline:  {delta['baseline_total']:4d} issues across {delta['baseline_files']:3d} files")
    print(f"  Candidate: {delta['candidate_total']:4d} issues across {delta['candidate_files']:3d} files")
    sign = "+" if delta["delta_total"] > 0 else ""
    print(f"  Delta:     {sign}{delta['delta_total']} issues")
    print()

    if delta["resolved_pairs"]:
        print(f"  Resolved ({len(delta['resolved_pairs'])}):")
        for p in delta["resolved_pairs"][:10]:
            print(f"    - {p['ref']:50s}  in {p['file']}")
        if len(delta["resolved_pairs"]) > 10:
            print(f"    ... and {len(delta['resolved_pairs']) - 10} more")
        print()

    if delta["new_pairs"]:
        print(f"  ✗ NEW DRIFT INTRODUCED ({len(delta['new_pairs'])}):")
        for p in delta["new_pairs"]:
            print(f"    + {p['ref']:50s}  in {p['file']}")
        print()
        print("  FAIL — see new issues above. Fix them, or run the validator")
        print("         locally for full context:")
        print(f"           python3 {TS_VALIDATOR}")
        print(f"           jq . {TS_DRIFT_REPORT}")
    else:
        print("  ✓ No new drift introduced.")
        print()
        print("  PASS — okay to push.")
    print(bar)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--base", default="origin/main", help="Base ref to compare against (default: origin/main)")
    parser.add_argument("--json-out", help="Write the delta as JSON to this path")
    parser.add_argument("--skip-fetch", action="store_true", help="Skip `git fetch` before resolving base ref")
    parser.add_argument("--quiet", action="store_true", help="Suppress per-pair lists; print summary only")
    args = parser.parse_args(argv)

    try:
        base_sha = resolve_base(args.base, args.skip_fetch)
    except ScriptError as e:
        print(f"docs-ops drift check: {e}", file=sys.stderr)
        return 2

    base_label = f"{args.base} ({base_sha[:8]})"

    try:
        with temp_worktree(base_sha) as wt:
            baseline = run_drift_pipeline(wt)
        candidate = run_drift_pipeline(REPO_ROOT)
    except ScriptError as e:
        print(f"docs-ops drift check: {e}", file=sys.stderr)
        return 2

    if candidate is None:
        print("docs-ops drift check: docs-ops system not present in candidate. Nothing to check.", file=sys.stderr)
        return 0

    delta = compute_delta(baseline, candidate, base_label)

    if args.quiet:
        sign = "+" if delta["delta_total"] > 0 else ""
        verdict = "FAIL" if delta["regressed"] else "PASS"
        print(f"docs-ops drift: baseline={delta['baseline_total']} candidate={delta['candidate_total']} "
              f"delta={sign}{delta['delta_total']} new_pairs={len(delta['new_pairs'])} verdict={verdict}")
    else:
        print_summary(delta)

    if args.json_out:
        out_path = Path(args.json_out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(delta, indent=2) + "\n", encoding="utf-8")

    return 1 if delta["regressed"] else 0


if __name__ == "__main__":
    sys.exit(main())
