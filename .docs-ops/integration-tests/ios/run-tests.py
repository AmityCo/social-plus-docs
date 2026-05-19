#!/usr/bin/env python3
"""
run-tests.py (iOS) — Type-check every .swift block extracted by extract-blocks.py
using swiftc against the published AmitySDK xcframework.

Toolchain: Option C — swiftc -typecheck per file
  - Downloads AmitySDK.xcframework from the published SwiftPM release (8.1.1) if not cached.
  - Uses the ios-arm64_x86_64-simulator slice for typechecking (no device needed).
  - ~0.2s per block (fast since the framework binary is pre-compiled).
  - Works on macOS without Xcode project or xcworkspace.

Usage:
    python3 run-tests.py [--extract]  # --extract re-runs extract-blocks.py first
"""

import argparse
import json
import re
import subprocess
import sys
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
EXTRACTED_DIR = SCRIPT_DIR / "results" / "extracted"
RESULTS_DIR = SCRIPT_DIR / "results"
MANIFEST_PATH = EXTRACTED_DIR / "_manifest.json"
VENDOR_DIR = SCRIPT_DIR / "vendor"

# AmitySDK xcframework — published binary, pinned to v8.1.1 for reproducibility
XCFW_URL = "https://sdk.amity.co/sdk-release/ios-frameworks/8.1.1/AmitySDK.xcframework.zip"
XCFW_CHECKSUM = "1757caf25b3f69dfb06c2fb5004f464b5aecb673705872cd52d12c50fc120bd8"
XCFW_ZIP = VENDOR_DIR / "AmitySDK.xcframework.zip"
XCFW_PATH = VENDOR_DIR / "AmitySDK.xcframework"
# simulator slice used for typechecking on macOS
XCFW_SIM_SLICE = XCFW_PATH / "ios-arm64_x86_64-simulator"

SWIFT_ERROR_RE = re.compile(
    r'^(?P<file>.+?):(?P<line>\d+):(?P<col>\d+):\s*(?P<severity>error|warning|note):\s*(?P<msg>.+)$'
)


def get_ios_sdk() -> str:
    result = subprocess.run(
        ["xcrun", "--sdk", "iphonesimulator", "--show-sdk-path"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"xcrun failed: {result.stderr.strip()}")
    return result.stdout.strip()


def ensure_xcframework():
    """Download and extract the xcframework if not already cached."""
    if XCFW_SIM_SLICE.exists():
        print(f"  xcframework cached at {XCFW_PATH}")
        return

    VENDOR_DIR.mkdir(parents=True, exist_ok=True)
    print(f"  Downloading AmitySDK.xcframework from {XCFW_URL} ...")
    urllib.request.urlretrieve(XCFW_URL, XCFW_ZIP)
    print(f"  Extracting ...")
    with zipfile.ZipFile(XCFW_ZIP, "r") as zf:
        zf.extractall(VENDOR_DIR)
    print(f"  xcframework ready at {XCFW_PATH}")


def typecheck_file(swift_file: Path, ios_sdk: str, fw_dir: Path) -> dict:
    """Run swiftc -typecheck on a single .swift file. Returns result dict."""
    result = subprocess.run(
        [
            "swiftc", "-typecheck",
            "-sdk", ios_sdk,
            "-target", "arm64-apple-ios14.0-simulator",
            "-F", str(fw_dir),
            str(swift_file),
        ],
        capture_output=True,
        text=True,
    )
    stderr = result.stderr
    errors: list[dict] = []
    warnings: list[dict] = []

    for line in stderr.splitlines():
        m = SWIFT_ERROR_RE.match(line)
        if not m:
            continue
        # Only report diagnostics from our snippet file (not from SDK internals)
        if Path(m.group("file")).resolve() != swift_file.resolve():
            continue
        entry = {
            "line": int(m.group("line")),
            "col": int(m.group("col")),
            "severity": m.group("severity"),
            "message": m.group("msg"),
        }
        if m.group("severity") == "error":
            errors.append(entry)
        elif m.group("severity") == "warning":
            warnings.append(entry)

    return {
        "exit_code": result.returncode,
        "errors": errors,
        "warnings": warnings,
        "raw_stderr": stderr.strip() if errors else "",
    }


def main():
    parser = argparse.ArgumentParser(description="iOS doc-as-test runner")
    parser.add_argument("--extract", action="store_true",
                        help="Re-run extract-blocks.py before testing")
    parser.add_argument("--no-download", action="store_true",
                        help="Skip xcframework download (fail if not cached)")
    args = parser.parse_args()

    if args.extract:
        print("Running extract-blocks.py ...")
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "extract_blocks", SCRIPT_DIR / "extract-blocks.py"
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        mod.main()

    # Ensure xcframework is available
    if not args.no_download:
        ensure_xcframework()
    elif not XCFW_SIM_SLICE.exists():
        print("ERROR: xcframework not cached and --no-download set.", file=sys.stderr)
        sys.exit(1)

    ios_sdk = get_ios_sdk()
    fw_dir = XCFW_SIM_SLICE
    print(f"  SDK: {ios_sdk}")
    print(f"  Framework: {fw_dir}")

    # Load manifest
    if not MANIFEST_PATH.exists():
        print("ERROR: No manifest found. Run with --extract first.", file=sys.stderr)
        sys.exit(1)

    with open(MANIFEST_PATH) as f:
        manifest: list[dict] = json.load(f)

    extracted = [e for e in manifest if e["status"] == "extracted"]
    skipped = [e for e in manifest if e["status"] == "skipped"]

    print(f"\nTypechecking {len(extracted)} blocks ({len(skipped)} skipped) ...")

    passed = []
    failed = []
    warned = []

    for entry in extracted:
        swift_file = EXTRACTED_DIR / entry["file"]
        if not swift_file.exists():
            failed.append({**entry, "errors": [{"message": "file not found after extraction"}], "warnings": []})
            continue

        result = typecheck_file(swift_file, ios_sdk, fw_dir)
        entry_result = {
            **entry,
            "errors": result["errors"],
            "warnings": result["warnings"],
        }

        if result["exit_code"] == 0:
            if result["warnings"]:
                warned.append(entry_result)
                print(f"  WARN  {entry['file']} ({len(result['warnings'])} warnings)")
            else:
                passed.append(entry_result)
                print(f"  OK    {entry['file']}")
        else:
            failed.append({**entry_result, "raw_stderr": result.get("raw_stderr", "")})
            err_summary = result["errors"][0]["message"] if result["errors"] else "unknown error"
            print(f"  FAIL  {entry['file']} — {err_summary}")

    # Emit results/latest.json
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "toolchain": "swiftc -typecheck",
        "sdk_version": "AmitySDK 8.1.1 (xcframework binary)",
        "xcfw_url": XCFW_URL,
        "stats": {
            "blocks_extracted": len(extracted),
            "blocks_passed": len(passed) + len(warned),
            "blocks_warned": len(warned),
            "blocks_failed": len(failed),
            "blocks_skipped": len(skipped),
        },
        "failures": [
            {
                "file": e["file"],
                "source_page": e["source_page"],
                "block_index": e["block_index"],
                "severity": "error",
                "errors": e.get("errors", []),
            }
            for e in failed
        ],
        "warnings": [
            {
                "file": e["file"],
                "source_page": e["source_page"],
                "block_index": e["block_index"],
                "severity": "warning",
                "warnings": e.get("warnings", []),
            }
            for e in warned
        ],
        "passed": [
            {"file": e["file"], "source_page": e["source_page"]}
            for e in passed + warned
        ],
        "skipped": [
            {"file": e["file"], "source_page": e["source_page"]}
            for e in skipped
        ],
    }

    report_path = RESULTS_DIR / "latest.json"
    report_path.write_text(json.dumps(report, indent=2))

    # Summary
    print(f"\n{'='*60}")
    print(f"iOS doc-as-test results:")
    print(f"  Extracted : {len(extracted)}")
    print(f"  Passed    : {len(passed) + len(warned)}  ({len(warned)} with warnings)")
    print(f"  Failed    : {len(failed)}")
    print(f"  Skipped   : {len(skipped)}")
    print(f"  Report    : {report_path}")
    print(f"{'='*60}")

    if failed:
        print("\nTop failures:")
        for e in failed[:10]:
            err_msg = e["errors"][0]["message"] if e.get("errors") else "unknown"
            print(f"  {e['file']}: {err_msg}")

    return len(failed)


if __name__ == "__main__":
    sys.exit(main())
