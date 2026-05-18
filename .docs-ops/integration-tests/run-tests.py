#!/usr/bin/env python3
"""
run-tests.py — Type-check every extracted .ts block with tsc --noEmit --strict.
Emits results/latest.json with pass/fail stats and failure details.

Usage:
    cd social-plus-docs
    python3 .docs-ops/integration-tests/run-tests.py

Requires: tsc on PATH (npm install -g typescript  OR  npx tsc)
"""

import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
DOCS_ROOT = (SCRIPT_DIR / "../..").resolve()
EXTRACTED_DIR = SCRIPT_DIR / "results" / "extracted"
TSCONFIG = SCRIPT_DIR / "tsconfig.json"
MANIFEST_PATH = EXTRACTED_DIR / "_manifest.json"
PREAMBLE_PATH = SCRIPT_DIR / "preamble.d.ts"
OUTPUT_PATH = SCRIPT_DIR / "results" / "latest.json"

SDKS_ROOT = Path(os.environ.get("SP_SDKS_ROOT", str(DOCS_ROOT.parent))).resolve()
SDK_ROOT = SDKS_ROOT / "AmityTypescriptSDK"

# Matches: // source: <page>:<start>-<end>
SOURCE_COMMENT_RE = re.compile(r'^// source: (.+):(\d+)-(\d+)$')


def find_tsc():
    candidates = [
        SDKS_ROOT / "AmityTypescriptSDK" / "node_modules" / ".bin" / "tsc",
        DOCS_ROOT / "node_modules" / ".bin" / "tsc",
    ]
    for c in candidates:
        if c.exists():
            return str(c)
    result = subprocess.run(["which", "tsc"], capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.strip()
    return "npx tsc"


def read_source_range(ts_file):
    """Read // source: <page>:<start>-<end> comment from extracted .ts file."""
    try:
        for line in ts_file.read_text(encoding="utf-8").splitlines()[:3]:
            m = SOURCE_COMMENT_RE.match(line.strip())
            if m:
                return m.group(2) + "-" + m.group(3)
    except Exception:
        pass
    return "?"


def run_tsc_project(ts_files, tsc_bin):
    """
    Run tsc once on the whole project and parse per-file errors.
    Returns {filename: {passed: bool, errors: [str]}}.
    """
    cmd = [tsc_bin, "--noEmit", "--project", str(TSCONFIG)]
    result = subprocess.run(
        cmd, capture_output=True, text=True, cwd=str(SCRIPT_DIR)
    )

    file_errors = {}
    error_re = re.compile(r'^(.*?)\((\d+),(\d+)\):\s*(error TS\d+:.*)')

    for line in (result.stdout + result.stderr).splitlines():
        m = error_re.match(line)
        if m:
            raw_file = m.group(1).strip()
            file_key = Path(raw_file).name
            err_text = m.group(4).strip()
            file_errors.setdefault(file_key, []).append(err_text)

    results = {}
    for ts_file in ts_files:
        key = ts_file.name
        errs = file_errors.get(key, [])
        results[key] = {
            "passed": len(errs) == 0,
            "errors": errs[:5],
        }
    return results


def load_manifest():
    if not MANIFEST_PATH.exists():
        print("ERROR: manifest not found. Run extract-blocks.py first.", file=sys.stderr)
        sys.exit(1)
    return json.loads(MANIFEST_PATH.read_text())


def block_file_to_page(filename, manifest):
    m = re.match(r'^(.+)-block-(\d+)\.tsx?$', filename)
    if not m:
        return "unknown", "?"
    slug = m.group(1)
    block_n = m.group(2)
    page = slug.replace("__", "/") + ".mdx"
    return page, block_n


def main():
    tsc_bin = find_tsc()
    print(f"Using tsc: {tsc_bin}")

    manifest = load_manifest()
    ts_files = sorted(list(EXTRACTED_DIR.glob("*.ts")) + list(EXTRACTED_DIR.glob("*.tsx")))

    if not ts_files:
        print("ERROR: No extracted .ts files. Run extract-blocks.py first.", file=sys.stderr)
        sys.exit(1)

    print(f"Type-checking {len(ts_files)} blocks...")
    tsc_results = run_tsc_project(ts_files, tsc_bin)

    failures = []
    by_page = {}
    passed_total = 0
    failed_total = 0

    for ts_file in ts_files:
        key = ts_file.name
        res = tsc_results.get(key, {"passed": True, "errors": []})
        page, block_n = block_file_to_page(key, manifest)

        if page not in by_page:
            by_page[page] = {"blocks": 0, "passed": 0, "failed": 0}
        by_page[page]["blocks"] += 1

        if res["passed"]:
            passed_total += 1
            by_page[page]["passed"] += 1
        else:
            failed_total += 1
            by_page[page]["failed"] += 1
            failures.append({
                "block_file": f"results/extracted/{key}",
                "source_page": page,
                "block_index": block_n,
                "source_line_range": read_source_range(ts_file),
                "errors": res["errors"],
            })

    # Include skipped blocks in stats
    blocks_skipped = manifest.get("total_skipped", 0)
    total = passed_total + failed_total
    pass_rate = round(passed_total / total, 4) if total > 0 else 0.0

    preamble_hash = hashlib.md5(PREAMBLE_PATH.read_bytes()).hexdigest()[:8]

    report = {
        "run_at": datetime.now(timezone.utc).isoformat(),
        "sdk_root": str(SDK_ROOT),
        "preamble_version": preamble_hash,
        "stats": {
            "pages_scanned": len(manifest.get("pages", [])),
            "blocks_extracted": total,
            "blocks_skipped": blocks_skipped,
            "blocks_passed": passed_total,
            "blocks_failed": failed_total,
            "pass_rate": pass_rate,
        },
        "by_page": by_page,
        "failures": failures,
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(report, indent=2))

    effective_rate = round((passed_total + blocks_skipped) / max(total + blocks_skipped, 1), 4)

    print(f"\n{'='*60}")
    print(f"Pages scanned:    {report['stats']['pages_scanned']}")
    print(f"Blocks extracted: {total}")
    print(f"Blocks skipped:   {blocks_skipped}")
    print(f"Passed:           {passed_total}  ({pass_rate*100:.1f}% of extracted)")
    print(f"Failed:           {failed_total}")
    print(f"Effective rate:   {effective_rate*100:.1f}% (passed+skipped / total)")
    print(f"Report:           {OUTPUT_PATH}")
    print(f"{'='*60}")

    if failed_total > 0:
        print(f"\nTop failures by page:")
        sorted_pages = sorted(
            [(p, d) for p, d in by_page.items() if d["failed"] > 0],
            key=lambda x: -x[1]["failed"]
        )
        for page, stats in sorted_pages[:10]:
            print(f"  {stats['failed']}/{stats['blocks']} failed  {page}")

        print(f"\nFailure details:")
        for f in failures:
            print(f"  {f['source_page']}:{f['source_line_range']} block {f['block_index']}")
            for e in f["errors"][:2]:
                print(f"    {e}")


if __name__ == "__main__":
    main()
