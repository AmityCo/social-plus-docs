#!/usr/bin/env python3
"""
run-tests.py (Flutter) — Type-check every extracted .dart block with `dart analyze`.
Emits results/latest.json with pass/fail stats and failure details.

Usage:
    cd .docs-ops/integration-tests/flutter
    dart pub get          # one-time setup
    python3 run-tests.py
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
DOCS_ROOT = (SCRIPT_DIR / "../../..").resolve()
EXTRACTED_DIR = SCRIPT_DIR / "results" / "extracted"
MANIFEST_PATH = EXTRACTED_DIR / "_manifest.json"
PREAMBLE_PATH = SCRIPT_DIR / "preamble.dart"
OUTPUT_PATH = SCRIPT_DIR / "results" / "latest.json"

SDKS_ROOT = Path(os.environ.get("SP_SDKS_ROOT", str(DOCS_ROOT.parent))).resolve()
SDK_ROOT = SDKS_ROOT / "Amity-Social-Cloud-SDK-Flutter-Internal"

# Dart analyze error line pattern: "  filename.dart:line:col • message • code • severity"
# Or: "error • message • file.dart:line:col • code"
DART_ERROR_RE = re.compile(
    r'^\s*(error|warning|info|hint)\s+[•·]\s+(.+?)\s+[•·]\s+\S+:(\d+):\d+\s+[•·]\s+(\w+)',
    re.IGNORECASE,
)
# Alternate format: "file.dart:line:col: severity: message"
DART_ERROR_RE2 = re.compile(
    r'^(\S+\.dart):(\d+):\d+:\s+(Error|Warning|Info|Hint):\s+(.+)',
    re.IGNORECASE,
)

SOURCE_COMMENT_RE = re.compile(r'^// source: (.+):(\d+)-(\d+)$')


def find_dart():
    # Prefer the actual dart binary (not the bash wrapper) for subprocess calls
    candidates = [
        Path("/Users/admin/Documents/development/flutter/bin/cache/dart-sdk/bin/dart"),
        Path("/usr/local/bin/dart"),
        Path("/Users/admin/Documents/development/flutter/bin/dart"),
    ]
    for c in candidates:
        if c.exists() and not c.is_symlink():
            return str(c)
    for c in candidates:
        if c.exists():
            return str(c)
    result = subprocess.run(["which", "dart"], capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.strip()
    return "dart"


def ensure_pub_get(dart_bin):
    """Run dart pub get if .dart_tool/package_config.json doesn't exist."""
    pkg_config = SCRIPT_DIR / ".dart_tool" / "package_config.json"
    if not pkg_config.exists():
        print("Running dart pub get...")
        result = subprocess.run(
            [dart_bin, "pub", "get"],
            cwd=str(SCRIPT_DIR),
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(f"WARNING: dart pub get failed:\n{result.stderr[:500]}", file=sys.stderr)
            return False
    return True


def read_source_range(dart_file):
    try:
        for line in dart_file.read_text(encoding="utf-8").splitlines()[:2]:
            m = SOURCE_COMMENT_RE.match(line.strip())
            if m:
                return m.group(2) + "-" + m.group(3)
    except Exception:
        pass
    return "?"


def analyze_file(dart_file, dart_bin):
    """Run dart analyze on a single file. Returns {passed, errors, warnings}."""
    result = subprocess.run(
        [dart_bin, "analyze", "--no-fatal-warnings", str(dart_file)],
        cwd=str(SCRIPT_DIR),
        capture_output=True,
        text=True,
    )
    output = result.stdout + result.stderr

    errors = []
    warnings = []

    for line in output.splitlines():
        # Try format 1: "  error • message • file:line:col • code"
        m = DART_ERROR_RE.match(line)
        if m:
            severity = m.group(1).lower()
            msg = m.group(2).strip()
            code = m.group(4).strip()
            entry = f"{code}: {msg}"
            if severity == "error":
                errors.append(entry)
            elif severity == "warning":
                warnings.append(entry)
            continue
        # Try format 2: "file.dart:line:col: Error: message"
        m2 = DART_ERROR_RE2.match(line)
        if m2:
            severity = m2.group(3).lower()
            msg = m2.group(4).strip()
            entry = msg
            if severity == "error":
                errors.append(entry)
            elif severity == "warning":
                warnings.append(entry)

    # If exit code != 0 and no structured errors found, use raw output
    if result.returncode != 0 and not errors:
        for line in output.splitlines():
            line = line.strip()
            if line and "error" in line.lower() and len(line) < 200:
                errors.append(line)
                if len(errors) >= 3:
                    break

    passed = result.returncode == 0 or len(errors) == 0
    return {"passed": passed, "errors": errors[:5], "warnings": warnings[:3]}


def load_manifest():
    if not MANIFEST_PATH.exists():
        print("ERROR: manifest not found. Run extract-blocks.py first.", file=sys.stderr)
        sys.exit(1)
    return json.loads(MANIFEST_PATH.read_text())


def block_file_to_page(filename, manifest):
    m = re.match(r'^(.+)-block-(\d+)\.dart$', filename)
    if not m:
        return "unknown", "?"
    slug = m.group(1)
    block_n = m.group(2)
    page = slug.replace("__", "/") + ".mdx"
    return page, block_n


def main():
    dart_bin = find_dart()
    print(f"Using dart: {dart_bin}")

    if not ensure_pub_get(dart_bin):
        print("WARNING: pub get failed; analysis may not resolve packages.", file=sys.stderr)

    manifest = load_manifest()
    dart_files = sorted(EXTRACTED_DIR.glob("*.dart"))

    if not dart_files:
        print("ERROR: No extracted .dart files. Run extract-blocks.py first.", file=sys.stderr)
        sys.exit(1)

    print(f"Analyzing {len(dart_files)} blocks with dart analyze...")

    results_map = {}
    for dart_file in dart_files:
        res = analyze_file(dart_file, dart_bin)
        results_map[dart_file.name] = res

    failures = []
    by_page = {}
    passed_total = 0
    failed_total = 0
    warning_total = 0

    for dart_file in dart_files:
        key = dart_file.name
        res = results_map.get(key, {"passed": True, "errors": [], "warnings": []})
        page, block_n = block_file_to_page(key, manifest)

        if page not in by_page:
            by_page[page] = {"blocks": 0, "passed": 0, "failed": 0}
        by_page[page]["blocks"] += 1
        warning_total += len(res.get("warnings", []))

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
                "source_line_range": read_source_range(dart_file),
                "errors": res["errors"],
                "warnings": res.get("warnings", []),
            })

    blocks_skipped = manifest.get("total_skipped", 0)
    total = passed_total + failed_total
    pass_rate = round(passed_total / total, 4) if total > 0 else 0.0
    effective_rate = round((passed_total + blocks_skipped) / max(total + blocks_skipped, 1), 4)

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
            "total_warnings": warning_total,
            "pass_rate": pass_rate,
            "effective_rate": effective_rate,
        },
        "by_page": by_page,
        "failures": failures,
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(report, indent=2))

    print(f"\n{'='*60}")
    print(f"Pages scanned:    {report['stats']['pages_scanned']}")
    print(f"Blocks extracted: {total}")
    print(f"Blocks skipped:   {blocks_skipped}")
    print(f"Passed:           {passed_total}  ({pass_rate*100:.1f}%)")
    print(f"Failed:           {failed_total}")
    print(f"Effective rate:   {effective_rate*100:.1f}% (passed+skipped / total)")
    print(f"Report:           {OUTPUT_PATH}")
    print(f"{'='*60}")

    if failed_total > 0:
        print(f"\nTop failures by page:")
        sorted_pages = sorted(
            [(p, d) for p, d in by_page.items() if d["failed"] > 0],
            key=lambda x: -x[1]["failed"],
        )
        for page, stats in sorted_pages[:10]:
            print(f"  {stats['failed']}/{stats['blocks']} failed  {page}")

        print(f"\nFailure details (first error per block):")
        for f in failures[:10]:
            print(f"  {f['source_page']}:{f['source_line_range']} block {f['block_index']}")
            if f["errors"]:
                print(f"    {f['errors'][0][:120]}")


if __name__ == "__main__":
    main()
