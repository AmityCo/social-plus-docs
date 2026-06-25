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
import re
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

# Doc-as-test paths (TypeScript), relative to repo root.
DAT_DIR = REPO_ROOT / ".docs-ops/integration-tests"
DAT_EXTRACTOR = DAT_DIR / "extract-blocks.py"
DAT_RUNNER = DAT_DIR / "run-tests.py"
DAT_REPORT = DAT_DIR / "results" / "latest.json"

# Doc-as-test paths (Flutter), relative to repo root.
FL_DAT_DIR = REPO_ROOT / ".docs-ops/integration-tests/flutter"
FL_DAT_EXTRACTOR = FL_DAT_DIR / "extract-blocks.py"
FL_DAT_RUNNER = FL_DAT_DIR / "run-tests.py"
FL_DAT_REPORT = FL_DAT_DIR / "results" / "latest.json"

# Doc-as-test paths (Android), relative to repo root.
AN_DAT_DIR = REPO_ROOT / ".docs-ops/integration-tests/android"
AN_DAT_EXTRACTOR = AN_DAT_DIR / "extract-blocks.py"
AN_DAT_RUNNER = AN_DAT_DIR / "run-tests.py"
AN_DAT_REPORT = AN_DAT_DIR / "results" / "latest.json"

# Doc-as-test paths (iOS), relative to repo root.
IOS_DAT_DIR = REPO_ROOT / ".docs-ops/integration-tests/ios"
IOS_DAT_EXTRACTOR = IOS_DAT_DIR / "extract-blocks.py"
IOS_DAT_RUNNER = IOS_DAT_DIR / "run-tests.py"
IOS_DAT_REPORT = IOS_DAT_DIR / "results" / "latest.json"


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


def run_flutter_doc_as_test_check() -> dict:
    """Run Flutter doc-as-test framework on the candidate working tree.

    Returns same schema as run_doc_as_test_check().
    Blocking = Dart error-severity failures (already filtered in run-tests.py).
    Warnings  = stats.total_warnings (non-blocking, counted but not per-failure).
    """
    if not FL_DAT_EXTRACTOR.exists() or not FL_DAT_RUNNER.exists():
        return {"available": False, "crashed": False, "crash_reason": "",
                "stats": {}, "blocking_failures": [], "warning_failures": []}

    env = os.environ.copy()
    env["SP_SDKS_ROOT"] = str(REPO_ROOT.parent)

    try:
        run(["python3", str(FL_DAT_EXTRACTOR)], cwd=REPO_ROOT, env=env)
        run(["python3", str(FL_DAT_RUNNER)], cwd=REPO_ROOT, env=env)
    except subprocess.CalledProcessError as e:
        return {
            "available": True, "crashed": True,
            "crash_reason": f"runner failed (exit {e.returncode}): {(e.stderr or '').strip()[:200]}",
            "stats": {}, "blocking_failures": [], "warning_failures": [],
        }

    if not FL_DAT_REPORT.exists():
        return {
            "available": True, "crashed": True,
            "crash_reason": "report not produced after runner completed",
            "stats": {}, "blocking_failures": [], "warning_failures": [],
        }

    try:
        report = json.loads(FL_DAT_REPORT.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return {
            "available": True, "crashed": True,
            "crash_reason": f"report JSON invalid: {e}",
            "stats": {}, "blocking_failures": [], "warning_failures": [],
        }

    # Flutter: failures[] only contains error-severity blocks (dart analyze `error`).
    # Warnings are aggregated in stats.total_warnings, not per-failure.
    blocking = []
    for f in report.get("failures", []):
        blocking.append({
            "source_page": f.get("source_page", "?"),
            "source_line_range": f.get("source_line_range", "?"),
            "errors": f.get("errors", [])[:3],
        })

    return {
        "available": True,
        "crashed": False,
        "crash_reason": "",
        "stats": report.get("stats", {}),
        "blocking_failures": blocking,
        "warning_failures": [],  # warnings counted in stats.total_warnings
    }


def run_android_doc_as_test_check() -> dict:
    """Run Android doc-as-test framework on the candidate working tree.

    Returns same schema as run_flutter_doc_as_test_check().
    Blocking = Kotlin compiler error-severity failures.
    Warnings  = stats.blocks_warned (non-blocking).
    """
    if not AN_DAT_EXTRACTOR.exists() or not AN_DAT_RUNNER.exists():
        return {"available": False, "crashed": False, "crash_reason": "",
                "stats": {}, "blocking_failures": [], "warning_failures": []}

    env = os.environ.copy()
    env["SP_SDKS_ROOT"] = str(REPO_ROOT.parent)

    try:
        run(["python3", str(AN_DAT_EXTRACTOR)], cwd=REPO_ROOT, env=env)
        run(["python3", str(AN_DAT_RUNNER)], cwd=REPO_ROOT, env=env)
    except subprocess.CalledProcessError as e:
        return {
            "available": True, "crashed": True,
            "crash_reason": f"runner failed (exit {e.returncode}): {(e.stderr or '').strip()[:200]}",
            "stats": {}, "blocking_failures": [], "warning_failures": [],
        }

    if not AN_DAT_REPORT.exists():
        return {
            "available": True, "crashed": True,
            "crash_reason": "report not produced after runner completed",
            "stats": {}, "blocking_failures": [], "warning_failures": [],
        }

    try:
        report = json.loads(AN_DAT_REPORT.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return {
            "available": True, "crashed": True,
            "crash_reason": f"report JSON invalid: {e}",
            "stats": {}, "blocking_failures": [], "warning_failures": [],
        }

    # Android: failures[] only contains error-severity blocks (Kotlin compiler errors).
    # Warnings are aggregated in stats.blocks_warned, not per-failure.
    blocking = []
    for f in report.get("failures", []):
        blocking.append({
            "source_page": f.get("source_page", "?"),
            "source_line_range": f.get("source_line_range", "?"),
            "errors": f.get("errors", [])[:3],
        })

    return {
        "available": True,
        "crashed": False,
        "crash_reason": "",
        "stats": report.get("stats", {}),
        "blocking_failures": blocking,
        "warning_failures": [],  # warnings counted in stats.blocks_warned
    }


def ios_developer_dir_candidates() -> list[str | None]:
    candidates: list[str | None] = [os.environ.get("DEVELOPER_DIR")]
    for path in [
        "/Applications/Xcode.app/Contents/Developer",
        "/Applications/Xcode-beta.app/Contents/Developer",
        str(Path.home() / "Downloads/Xcode.app/Contents/Developer"),
        str(Path.home() / "Applications/Xcode.app/Contents/Developer"),
    ]:
        if Path(path).exists():
            candidates.append(path)

    for apps_dir in [
        Path("/Applications"),
        Path.home() / "Downloads",
        Path.home() / "Applications",
    ]:
        if apps_dir.exists():
            for developer_dir in sorted(apps_dir.glob("Xcode*.app/Contents/Developer")):
                candidates.append(str(developer_dir))

    seen = set()
    unique: list[str | None] = []
    for candidate in candidates:
        key = candidate or ""
        if key not in seen:
            seen.add(key)
            unique.append(candidate)
    return unique


def resolve_iphonesimulator_env() -> tuple[dict[str, str] | None, str]:
    errors = []
    base_env = os.environ.copy()
    for developer_dir in ios_developer_dir_candidates():
        env = base_env.copy()
        label = "active developer directory"
        if developer_dir:
            env["DEVELOPER_DIR"] = developer_dir
            label = developer_dir

        try:
            result = run(
                ["xcrun", "--sdk", "iphonesimulator", "--show-sdk-path"],
                cwd=REPO_ROOT,
                check=False,
                env=env,
            )
        except FileNotFoundError as e:
            errors.append(f"{label}: xcrun not found ({e})")
            continue

        if result.returncode == 0 and result.stdout.strip():
            return env, ""
        errors.append(f"{label}: {(result.stderr or result.stdout).strip()}")

    return None, (
        "iPhoneSimulator SDK not found. Install/select full Xcode, or set "
        "DEVELOPER_DIR to an Xcode.app Contents/Developer path. "
        f"Tried: {' | '.join(errors)}"
    )


def run_ios_doc_as_test_check() -> dict:
    """Run iOS doc-as-test framework on the candidate working tree.

    Returns same schema as run_flutter_doc_as_test_check().
    Blocking = swiftc error-severity failures.
    Warnings  = stats.blocks_warned (non-blocking).

    iOS uses macOS-only swiftc. If swiftc is not on PATH, returns
    available=False so the gate reports 'unavailable' and continues
    without blocking — makes the gate usable on Linux dev machines.
    """
    if shutil.which("swiftc") is None:
        return {"available": False, "crashed": False,
                "crash_reason": "swiftc not found — install Xcode CLI tools",
                "stats": {}, "blocking_failures": [], "warning_failures": []}

    ios_env, ios_unavailable_reason = resolve_iphonesimulator_env()
    if ios_env is None:
        return {"available": False, "crashed": False,
                "crash_reason": ios_unavailable_reason,
                "stats": {}, "blocking_failures": [], "warning_failures": []}

    if not IOS_DAT_EXTRACTOR.exists() or not IOS_DAT_RUNNER.exists():
        return {"available": False, "crashed": False, "crash_reason": "",
                "stats": {}, "blocking_failures": [], "warning_failures": []}

    env = ios_env.copy()
    env["SP_SDKS_ROOT"] = str(REPO_ROOT.parent)

    try:
        run(["python3", str(IOS_DAT_EXTRACTOR)], cwd=REPO_ROOT, env=env)
        run(["python3", str(IOS_DAT_RUNNER)], cwd=REPO_ROOT, env=env)
    except subprocess.CalledProcessError as e:
        return {
            "available": True, "crashed": True,
            "crash_reason": f"runner failed (exit {e.returncode}): {(e.stderr or '').strip()[:200]}",
            "stats": {}, "blocking_failures": [], "warning_failures": [],
        }

    if not IOS_DAT_REPORT.exists():
        return {
            "available": True, "crashed": True,
            "crash_reason": "report not produced after runner completed",
            "stats": {}, "blocking_failures": [], "warning_failures": [],
        }

    try:
        report = json.loads(IOS_DAT_REPORT.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return {
            "available": True, "crashed": True,
            "crash_reason": f"report JSON invalid: {e}",
            "stats": {}, "blocking_failures": [], "warning_failures": [],
        }

    # iOS: failures[] only contains error-severity blocks (swiftc errors).
    # Warnings are aggregated in stats.blocks_warned, not per-failure.
    blocking = []
    for f in report.get("failures", []):
        blocking.append({
            "source_page": f.get("source_page", "?"),
            "source_line_range": f.get("source_line_range", "?"),
            "errors": f.get("errors", [])[:3],
        })

    return {
        "available": True,
        "crashed": False,
        "crash_reason": "",
        "stats": report.get("stats", {}),
        "blocking_failures": blocking,
        "warning_failures": [],  # warnings counted in stats.blocks_warned
    }


def run_mdx_structure_check() -> dict:
    """Scan all MDX files for HTML comments (<!-- -->) inside JSX component context.

    HTML comments are invalid JSX syntax. Inside components like <CodeGroup>,
    <Tabs>, <Tab>, <Accordion> etc. they cause MDX parse errors that break page
    rendering entirely. The correct form is {/* JSX comment */}.

    Returns:
        violations: list of {file, line, content} dicts
        blocking: True if any violations found
    """
    JSX_OPEN_RE = re.compile(
        r"<(Tabs|Tab|CodeGroup|CardGroup|Card|Accordion|AccordionGroup|Info|Warning|Note|Callout)[> /]"
    )
    JSX_CLOSE_RE = re.compile(
        r"</(Tabs|Tab|CodeGroup|CardGroup|Card|Accordion|AccordionGroup|Info|Warning|Note|Callout)>"
    )
    HTML_COMMENT_RE = re.compile(r"<!--")
    FENCE_RE = re.compile(r"^```")

    violations = []
    mdx_root = REPO_ROOT / "social-plus-sdk"
    if not mdx_root.exists():
        mdx_root = REPO_ROOT  # fallback

    for mdx_path in sorted(mdx_root.rglob("*.mdx")):
        try:
            lines = mdx_path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        depth = 0
        in_fence = False
        for lineno, line in enumerate(lines, 1):
            if FENCE_RE.match(line):
                in_fence = not in_fence
            if in_fence:
                continue  # code fence content is safe — <!-- is just code text
            if JSX_OPEN_RE.search(line):
                depth += 1
            if JSX_CLOSE_RE.search(line):
                depth -= 1
            if depth > 0 and HTML_COMMENT_RE.search(line):
                violations.append({
                    "file": str(mdx_path.relative_to(REPO_ROOT)),
                    "line": lineno,
                    "content": line.strip()[:120],
                })

    return {
        "violations": violations,
        "blocking": len(violations) > 0,
        "files_scanned": sum(1 for _ in mdx_root.rglob("*.mdx")),
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


def print_summary(
    delta: dict,
    ts_dat: dict | None = None,
    fl_dat: dict | None = None,
    an_dat: dict | None = None,
    ios_dat: dict | None = None,
    mdx_chk: dict | None = None,
    required_runner_failures: list[str] | None = None,
) -> None:
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
    print(f"  Regex drift:           baseline={delta['baseline_total']}  candidate={delta['candidate_total']}  "
          f"delta={sign}{delta['delta_total']}  {drift_status}")

    # Doc-as-test (TS) line
    def _dat_line(label: str, dat: dict | None) -> None:
        if dat is None or not dat.get("available"):
            unavail_reason = (dat or {}).get("crash_reason", "")
            if unavail_reason:
                print(f"  {label}  unavailable ({unavail_reason})")
            else:
                print(f"  {label}  (not available)")
        elif dat.get("crashed"):
            print(f"  {label}  ⚠ runner crashed (non-blocking): {dat['crash_reason']}")
        else:
            s = dat["stats"]
            b = len(dat["blocking_failures"])
            w = len(dat["warning_failures"]) + s.get("total_warnings", 0) + s.get("blocks_warned", 0)
            status = "✓" if b == 0 else "✗"
            print(f"  {label}  passed={s.get('blocks_passed', 0)}  "
                  f"skipped={s.get('blocks_skipped', 0)}  "
                  f"warnings={w}  blocking={b}  {status}")

    _dat_line("Doc-as-test (TS):     ", ts_dat)
    _dat_line("Doc-as-test (Flutter):", fl_dat)
    _dat_line("Doc-as-test (Android):", an_dat)
    _dat_line("Doc-as-test (iOS):    ", ios_dat)

    # MDX structure line
    if mdx_chk is not None:
        n = len(mdx_chk["violations"])
        scanned = mdx_chk["files_scanned"]
        status = "✓" if n == 0 else "✗"
        print(f"  MDX structure:         files_scanned={scanned}  html_comments_in_jsx={n}  {status}")

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

    # Doc-as-test details (TS + Flutter + Android + iOS)
    for label, dat in [("TS", ts_dat), ("Flutter", fl_dat), ("Android", an_dat), ("iOS", ios_dat)]:
        if not dat or not dat.get("available") or dat.get("crashed"):
            continue
        if dat["blocking_failures"]:
            print(f"  ✗ DOC-AS-TEST ({label}) TYPE ERRORS (BLOCKING):")
            for f in dat["blocking_failures"]:
                page = f["source_page"].split("/")[-1]
                lr = f["source_line_range"]
                err = f["errors"][0] if f["errors"] else "?"
                print(f"    - {page}:{lr}  {err}")
            print()
            runner = "run-tests.py" if label == "TS" else f"{label.lower()}/run-tests.py"
            print(f"  Fix the type errors above. Run locally:")
            print(f"    python3 .docs-ops/integration-tests/{runner}")
            print()

        if dat["warning_failures"]:
            print(f"  ⚠ {len(dat['warning_failures'])} doc-as-test ({label}) warning(s) (parser-only, non-blocking):")
            for f in dat["warning_failures"]:
                page = f["source_page"].split("/")[-1]
                lr = f["source_line_range"]
                errs = ", ".join(e.split(":")[0] for e in f["errors"][:2])
                print(f"    - {page}:{lr} ({errs})")
            print()

    # MDX structure violation details
    if mdx_chk and mdx_chk["violations"]:
        print(f"  ✗ MDX STRUCTURE VIOLATIONS (BLOCKING) — {len(mdx_chk['violations'])} HTML comment(s) inside JSX:")
        for v in mdx_chk["violations"]:
            print(f"    - {v['file']}:{v['line']}  {v['content'][:80]}")
        print()
        print("  HTML comments (<!-- -->) inside JSX components break MDX rendering.")
        print("  Replace with JSX comments: {/* your comment */}")
        print()

    # Final verdict
    regressed = delta["regressed"]
    ts_blocking = ts_dat and ts_dat.get("available") and not ts_dat.get("crashed") and len(ts_dat.get("blocking_failures", [])) > 0
    fl_blocking = fl_dat and fl_dat.get("available") and not fl_dat.get("crashed") and len(fl_dat.get("blocking_failures", [])) > 0
    an_blocking = an_dat and an_dat.get("available") and not an_dat.get("crashed") and len(an_dat.get("blocking_failures", [])) > 0
    ios_blocking = ios_dat and ios_dat.get("available") and not ios_dat.get("crashed") and len(ios_dat.get("blocking_failures", [])) > 0
    mdx_blocking = mdx_chk and mdx_chk["blocking"]
    required_runner_blocking = bool(required_runner_failures)
    if regressed or ts_blocking or fl_blocking or an_blocking or ios_blocking or mdx_blocking or required_runner_blocking:
        if regressed:
            print("  FAIL — fix new drift above, or run the validator locally:")
            print(f"           python3 {TS_VALIDATOR}")
            print(f"           jq . {TS_DRIFT_REPORT}")
        if ts_blocking:
            print("  FAIL — fix TS doc-as-test type errors above.")
        if fl_blocking:
            print("  FAIL — fix Flutter doc-as-test type errors above.")
        if an_blocking:
            print("  FAIL — fix Android doc-as-test compile errors above.")
        if ios_blocking:
            print("  FAIL — fix iOS doc-as-test compile errors above.")
        if mdx_blocking:
            print("  FAIL — fix MDX structure violations above (<!-- --> → {/* */} inside JSX).")
        if required_runner_blocking:
            print("  FAIL — required doc-as-test runner(s) did not complete:")
            for failure in required_runner_failures:
                print(f"           - {failure}")
    else:
        print("  PASS — okay to push.")
    print(bar)


def parse_required_doc_as_test(value: str) -> set[str]:
    if not value:
        return set()
    allowed = {"ts", "flutter", "android", "ios"}
    requested = {p.strip().lower() for p in value.split(",") if p.strip()}
    if "all" in requested:
        requested.remove("all")
        requested |= allowed
    invalid = requested - allowed
    if invalid:
        raise ValueError(f"unknown doc-as-test platform(s): {', '.join(sorted(invalid))}")
    return requested


def required_doc_as_test_failures(required: set[str], checks: list[tuple[str, str, dict]]) -> list[str]:
    failures = []
    for key, label, dat in checks:
        if key not in required:
            continue
        if not dat.get("available"):
            reason = dat.get("crash_reason") or "not available"
            failures.append(f"{label} unavailable ({reason})")
        elif dat.get("crashed"):
            failures.append(f"{label} crashed ({dat.get('crash_reason', 'unknown reason')})")
    return failures


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--base", default="origin/main", help="Base ref to compare against (default: origin/main)")
    parser.add_argument("--json-out", help="Write the delta as JSON to this path")
    parser.add_argument("--skip-fetch", action="store_true", help="Skip `git fetch` before resolving base ref")
    parser.add_argument("--quiet", action="store_true", help="Suppress per-pair lists; print summary only")
    parser.add_argument(
        "--require-doc-as-test",
        default="",
        help="Comma-separated platforms that must run successfully: ts,flutter,android,ios,all",
    )
    args = parser.parse_args(argv)

    try:
        required_doc_as_test = parse_required_doc_as_test(args.require_doc_as_test)
    except ValueError as e:
        parser.error(str(e))

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

    # Run doc-as-test on candidate working tree (TS + Flutter + Android + iOS)
    ts_dat = run_doc_as_test_check()
    fl_dat = run_flutter_doc_as_test_check()
    an_dat = run_android_doc_as_test_check()
    ios_dat = run_ios_doc_as_test_check()
    mdx_chk = run_mdx_structure_check()
    required_runner_failures = required_doc_as_test_failures(required_doc_as_test, [
        ("ts", "TS doc-as-test", ts_dat),
        ("flutter", "Flutter doc-as-test", fl_dat),
        ("android", "Android doc-as-test", an_dat),
        ("ios", "iOS doc-as-test", ios_dat),
    ])

    ts_blocking = ts_dat.get("available") and not ts_dat.get("crashed") and len(ts_dat.get("blocking_failures", [])) > 0
    fl_blocking = fl_dat.get("available") and not fl_dat.get("crashed") and len(fl_dat.get("blocking_failures", [])) > 0
    an_blocking = an_dat.get("available") and not an_dat.get("crashed") and len(an_dat.get("blocking_failures", [])) > 0
    ios_blocking = ios_dat.get("available") and not ios_dat.get("crashed") and len(ios_dat.get("blocking_failures", [])) > 0
    mdx_blocking = mdx_chk["blocking"]
    overall_fail = delta["regressed"] or ts_blocking or fl_blocking or an_blocking or ios_blocking or mdx_blocking or bool(required_runner_failures)

    if args.quiet:
        sign = "+" if delta["delta_total"] > 0 else ""
        verdict = "FAIL" if overall_fail else "PASS"
        ts_s = ts_dat.get("stats", {})
        fl_s = fl_dat.get("stats", {})
        an_s = an_dat.get("stats", {})
        ios_s = ios_dat.get("stats", {})
        ts_b = len(ts_dat.get("blocking_failures", []))
        fl_b = len(fl_dat.get("blocking_failures", []))
        an_b = len(an_dat.get("blocking_failures", []))
        ios_b = len(ios_dat.get("blocking_failures", []))
        ts_w = len(ts_dat.get("warning_failures", []))
        fl_w = fl_s.get("total_warnings", 0)
        an_w = an_s.get("blocks_warned", 0)
        ios_w = ios_s.get("blocks_warned", 0)
        print(f"docs-ops drift: baseline={delta['baseline_total']} candidate={delta['candidate_total']} "
              f"delta={sign}{delta['delta_total']} new_pairs={len(delta['new_pairs'])} "
              f"ts_passed={ts_s.get('blocks_passed', 0)} ts_skipped={ts_s.get('blocks_skipped', 0)} "
              f"ts_blocking={ts_b} fl_passed={fl_s.get('blocks_passed', 0)} "
              f"fl_skipped={fl_s.get('blocks_skipped', 0)} fl_blocking={fl_b} "
              f"an_passed={an_s.get('blocks_passed', 0)} an_skipped={an_s.get('blocks_skipped', 0)} "
              f"an_blocking={an_b} "
              f"ios_passed={ios_s.get('blocks_passed', 0)} ios_skipped={ios_s.get('blocks_skipped', 0)} "
              f"ios_blocking={ios_b} "
              f"required_runner_failures={len(required_runner_failures)} "
              f"mdx_html_comments_in_jsx={len(mdx_chk['violations'])} mdx_blocking={int(mdx_blocking)} "
              f"verdict={verdict}")
    else:
        print_summary(delta, ts_dat, fl_dat, an_dat, ios_dat, mdx_chk, required_runner_failures)

    if args.json_out:
        out_path = Path(args.json_out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        combined = {"drift_delta": delta, "doc_as_test_ts": ts_dat, "doc_as_test_flutter": fl_dat, "doc_as_test_android": an_dat, "doc_as_test_ios": ios_dat, "mdx_structure": mdx_chk, "required_doc_as_test": sorted(required_doc_as_test), "required_runner_failures": required_runner_failures}
        out_path.write_text(json.dumps(combined, indent=2) + "\n", encoding="utf-8")

    return 1 if overall_fail else 0


if __name__ == "__main__":
    sys.exit(main())
