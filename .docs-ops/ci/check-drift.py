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

# Doc-as-test paths, relative to repo root.
DAT_DIR = REPO_ROOT / ".docs-ops/integration-tests"
DAT_EXTRACTOR = DAT_DIR / "extract-blocks.py"
DAT_RUNNER = DAT_DIR / "run-tests.py"
DAT_REPORT = DAT_DIR / "results" / "latest.json"


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


def run_doc_as_test_check() -> dict:
    """Run doc-as-test framework on the candidate working tree.

    Returns:
      available:          False if the framework isn't set up yet
      crashed:            True if runner itself threw an error (non-blocking)
      stats:              raw stats from latest.json
      blocking_failures:  failures with any TS2xxx error (type drift — BLOCKS)
      warning_failures:   failures with only TS1xxx errors (parser-only — warns)
    """
    if not DAT_EXTRACTOR.exists() or not DAT_RUNNER.exists():
        return {"available": False, "crashed": False, "crash_reason": "",
                "stats": {}, "blocking_failures": [], "warning_failures": []}

    env = os.environ.copy()
    env["SP_SDKS_ROOT"] = str(REPO_ROOT.parent)

    try:
        run(["python3", str(DAT_EXTRACTOR)], cwd=REPO_ROOT, env=env)
        run(["python3", str(DAT_RUNNER)], cwd=REPO_ROOT, env=env)
    except subprocess.CalledProcessError as e:
        return {
            "available": True, "crashed": True,
            "crash_reason": f"runner failed (exit {e.returncode}): {(e.stderr or '').strip()[:200]}",
            "stats": {}, "blocking_failures": [], "warning_failures": [],
        }

    if not DAT_REPORT.exists():
        return {
            "available": True, "crashed": True,
            "crash_reason": "report not produced after runner completed",
            "stats": {}, "blocking_failures": [], "warning_failures": [],
        }

    try:
        report = json.loads(DAT_REPORT.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return {
            "available": True, "crashed": True,
            "crash_reason": f"report JSON invalid: {e}",
            "stats": {}, "blocking_failures": [], "warning_failures": [],
        }

    import re as _re
    ts2_re = _re.compile(r'\bTS2\d+\b')
    ts1_re = _re.compile(r'\bTS1\d+\b')

    blocking = []
    warning = []
    for f in report.get("failures", []):
        errors = f.get("errors", [])
        has_ts2 = any(ts2_re.search(e) for e in errors)
        has_ts1 = any(ts1_re.search(e) for e in errors)
        entry = {
            "source_page": f.get("source_page", "?"),
            "source_line_range": f.get("source_line_range", "?"),
            "errors": errors[:3],
        }
        if has_ts2:
            blocking.append(entry)
        elif has_ts1:
            warning.append(entry)

    return {
        "available": True,
        "crashed": False,
        "crash_reason": "",
        "stats": report.get("stats", {}),
        "blocking_failures": blocking,
        "warning_failures": warning,
    }


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


def print_summary(delta: dict, dat: dict | None = None) -> None:
    bar = "═" * 60
    print(bar)
    print("  Docs-Ops Drift Check")
    print(bar)
    print(f"  Base: {delta['base_ref']}")
    if delta["baseline_predates_system"]:
        print("        (baseline predates docs-ops; treated as zero drift)")

    # Regex drift line
    sign = "+" if delta["delta_total"] > 0 else ""
    drift_status = "✓ No new drift" if not delta["regressed"] else "✗ New drift introduced"
    print(f"  Regex drift:    baseline={delta['baseline_total']}  candidate={delta['candidate_total']}  "
          f"delta={sign}{delta['delta_total']}  {drift_status}")

    # Doc-as-test line
    if dat is None or not dat.get("available"):
        print("  Doc-as-test:    (not available)")
    elif dat.get("crashed"):
        print(f"  Doc-as-test:    ⚠ runner crashed (non-blocking): {dat['crash_reason']}")
    else:
        s = dat["stats"]
        b = len(dat["blocking_failures"])
        w = len(dat["warning_failures"])
        status = "✓" if b == 0 else "✗"
        print(f"  Doc-as-test:    blocks_passed={s.get('blocks_passed',0)}  "
              f"blocks_skipped={s.get('blocks_skipped',0)}  "
              f"warnings={w}  blocking={b}  {status}")

    print()

    # Regex drift details
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

    # Doc-as-test details
    if dat and dat.get("available") and not dat.get("crashed"):
        if dat["blocking_failures"]:
            print(f"  ✗ DOC-AS-TEST TYPE ERRORS (BLOCKING):")
            for f in dat["blocking_failures"]:
                page = f["source_page"].split("/")[-1]
                lr = f["source_line_range"]
                err = f["errors"][0] if f["errors"] else "?"
                print(f"    - {page}:{lr}  {err}")
            print()
            print("  Fix the type errors above. Run locally:")
            print("    python3 .docs-ops/integration-tests/run-tests.py")
            print()

        if dat["warning_failures"]:
            print(f"  ⚠ {len(dat['warning_failures'])} doc-as-test warning(s) (parser-only, non-blocking):")
            for f in dat["warning_failures"]:
                page = f["source_page"].split("/")[-1]
                lr = f["source_line_range"]
                errs = ", ".join(e.split(":")[0] for e in f["errors"][:2])
                print(f"    - {page}:{lr} ({errs})")
            print()

    # Final verdict
    regressed = delta["regressed"]
    dat_blocking = dat and dat.get("available") and not dat.get("crashed") and len(dat.get("blocking_failures", [])) > 0
    if regressed or dat_blocking:
        if regressed:
            print("  FAIL — fix new drift above, or run the validator locally:")
            print(f"           python3 {TS_VALIDATOR}")
            print(f"           jq . {TS_DRIFT_REPORT}")
        if dat_blocking:
            print("  FAIL — fix doc-as-test type errors above.")
    else:
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

    # Run doc-as-test on candidate working tree
    dat = run_doc_as_test_check()

    dat_blocking = dat.get("available") and not dat.get("crashed") and len(dat.get("blocking_failures", [])) > 0
    overall_fail = delta["regressed"] or dat_blocking

    if args.quiet:
        sign = "+" if delta["delta_total"] > 0 else ""
        verdict = "FAIL" if overall_fail else "PASS"
        s = dat.get("stats", {})
        b = len(dat.get("blocking_failures", []))
        w = len(dat.get("warning_failures", []))
        print(f"docs-ops drift: baseline={delta['baseline_total']} candidate={delta['candidate_total']} "
              f"delta={sign}{delta['delta_total']} new_pairs={len(delta['new_pairs'])} "
              f"dat_passed={s.get('blocks_passed',0)} dat_skipped={s.get('blocks_skipped',0)} "
              f"dat_blocking={b} dat_warnings={w} verdict={verdict}")
    else:
        print_summary(delta, dat)

    if args.json_out:
        out_path = Path(args.json_out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        combined = {"drift_delta": delta, "doc_as_test": dat}
        out_path.write_text(json.dumps(combined, indent=2) + "\n", encoding="utf-8")

    return 1 if overall_fail else 0


if __name__ == "__main__":
    sys.exit(main())
