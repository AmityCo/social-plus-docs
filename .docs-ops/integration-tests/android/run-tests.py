#!/usr/bin/env python3
"""
run-tests.py (Android) — Compile every .kt and .java file extracted by extract-blocks.py
using the kotlinc / javac compiler. Reports errors and emits results/latest.json.

Compilation engine:
  - Kotlin: kotlinc (kotlin-compiler-embeddable-1.9.22.jar) with -Xskip-metadata-version-check
    This suppresses Kotlin metadata version mismatch (SDK compiled with 2.2.x) while still
    providing full type-checking at the JVM bytecode level.
  - Java: standard javac with amity JARs on classpath.
"""

import json
import re
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
OUTPUT_DIR = SCRIPT_DIR / "results" / "extracted"
RESULTS_DIR = SCRIPT_DIR / "results"

# Kotlin compiler setup
GRADLE_HOME = Path.home() / ".gradle"
GRADLE_LIB = (
    GRADLE_HOME / "wrapper/dists/gradle-8.7-bin/bhs2wmbdwecv87pi65oeuq5iu/gradle-8.7/lib"
)
GRADLE_CACHE = GRADLE_HOME / "caches/modules-2/files-2.1"

AMITY_SDK_ROOT = Path(__file__).parent.parent.parent.parent.parent / "Amity-Social-Cloud-SDK-Android"


def find_jar(base_path, pattern, required=True):
    matches = list(base_path.glob(f"**/{pattern}"))
    matches = [m for m in matches if "sources" not in m.name and "javadoc" not in m.name]
    if not matches:
        if required:
            raise FileNotFoundError(f"JAR not found matching {pattern} under {base_path}")
        return None
    return sorted(matches)[-1]


def extract_aar_classes(aar_path, label):
    out_dir = Path(f"/tmp/{label}_extracted")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "classes.jar"
    if out_path.exists() and out_path.stat().st_mtime >= aar_path.stat().st_mtime:
        return out_path

    with zipfile.ZipFile(aar_path) as aar:
        try:
            data = aar.read("classes.jar")
        except KeyError as e:
            raise FileNotFoundError(f"{aar_path} does not contain classes.jar") from e
    out_path.write_bytes(data)
    return out_path


def build_classpath():
    """Assemble the compiler runtime classpath. Raises if critical JARs are missing."""
    kotlin_stdlib = find_jar(
        GRADLE_CACHE / "org.jetbrains.kotlin/kotlin-stdlib",
        "kotlin-stdlib-1.9*.jar",
    )
    annotations = find_jar(
        GRADLE_CACHE / "org.jetbrains/annotations",
        "annotations-23.0.0.jar",
    )
    rxjava3 = find_jar(
        GRADLE_CACHE / "io.reactivex.rxjava3/rxjava",
        "rxjava-3.1*.jar",
    )
    rxjava2 = find_jar(
        GRADLE_CACHE / "io.reactivex.rxjava2/rxjava",
        "rxjava-2.2*.jar",
    )
    rxandroid_aar = find_jar(
        GRADLE_CACHE / "io.reactivex.rxjava3/rxandroid",
        "rxandroid-3.0*.aar",
    )
    rxandroid = extract_aar_classes(rxandroid_aar, "rxandroid")
    reactive_streams = find_jar(
        GRADLE_CACHE / "org.reactivestreams/reactive-streams",
        "reactive-streams-1.0.4.jar",
    )
    coroutines_core = find_jar(
        GRADLE_CACHE / "org.jetbrains.kotlinx/kotlinx-coroutines-core-jvm",
        "kotlinx-coroutines-core-jvm-1.9*.jar",
    )
    paging_common_aar = find_jar(
        GRADLE_CACHE / "androidx.paging/paging-common-android",
        "paging-common.aar",
        required=False,
    )
    if paging_common_aar is not None:
        paging_common = extract_aar_classes(paging_common_aar, "paging_common_android")
    else:
        paging_common = find_jar(
            GRADLE_CACHE / "androidx.paging/paging-common",
            "paging-common-3.4*.jar",
            required=False,
        )
    if paging_common is None:
        paging_common = find_jar(
            GRADLE_CACHE / "androidx.paging/paging-common-ktx",
            "paging-common-ktx-3.4*.jar",
        )
    gson = find_jar(
        GRADLE_CACHE / "com.google.code.gson/gson",
        "gson-2.10.1.jar",
    )
    joda_time = find_jar(
        GRADLE_CACHE / "joda-time/joda-time",
        "joda-time-2.10.6.jar",
    )
    amity_sdk = AMITY_SDK_ROOT / "amity-sdk/build/intermediates/compile_library_classes_jar/release/bundleLibCompileToJarRelease/classes.jar"
    amity_rxbridge = AMITY_SDK_ROOT / "amity-rxbridge/build/intermediates/compile_library_classes_jar/release/bundleLibCompileToJarRelease/classes.jar"
    amity_log = AMITY_SDK_ROOT / "amity-log/build/intermediates/compile_library_classes_jar/release/bundleLibCompileToJarRelease/classes.jar"
    core_push = AMITY_SDK_ROOT / "core-push/build/intermediates/compile_library_classes_jar/release/bundleLibCompileToJarRelease/classes.jar"
    amity_push_fcm = AMITY_SDK_ROOT / "amity-push-fcm/build/intermediates/compile_library_classes_jar/release/bundleLibCompileToJarRelease/classes.jar"
    android_jar = Path("/Users/admin/Library/Android/sdk/platforms/android-34/android.jar")

    missing = []
    for jar, name in [
        (kotlin_stdlib, "kotlin-stdlib"),
        (annotations, "annotations"),
        (rxjava3, "rxjava3"),
        (rxjava2, "rxjava2"),
        (rxandroid, "rxandroid"),
        (reactive_streams, "reactive-streams"),
        (coroutines_core, "kotlinx-coroutines-core-jvm"),
        (paging_common, "paging-common"),
        (amity_sdk, "amity-sdk"),
        (amity_rxbridge, "amity-rxbridge"),
        (amity_log, "amity-log"),
        (core_push, "core-push"),
        (amity_push_fcm, "amity-push-fcm"),
        (android_jar, "android.jar"),
    ]:
        if jar is None or not Path(jar).exists():
            missing.append(name)
    if missing:
        raise FileNotFoundError(f"Missing required JARs: {missing}")

    compile_cp = ":".join(str(j) for j in [
        amity_sdk, amity_rxbridge, amity_log, core_push, amity_push_fcm, rxjava3, rxjava2, kotlin_stdlib, android_jar, annotations,
        rxandroid, reactive_streams, coroutines_core, paging_common, gson, joda_time,
    ])
    return compile_cp, kotlin_stdlib, annotations


def build_kotlinc_cmd(source_file, classpath, kotlin_stdlib, annotations):
    compiler_cp = ":".join([
        str(GRADLE_LIB / "kotlin-compiler-embeddable-1.9.22.jar"),
        str(GRADLE_LIB / "kotlin-reflect-1.9.22.jar"),
        str(GRADLE_LIB / "trove4j-1.0.20200330.jar"),
        str(kotlin_stdlib),
        str(annotations),
    ])
    return [
        "java",
        "-cp", compiler_cp,
        "org.jetbrains.kotlin.cli.jvm.K2JVMCompiler",
        "-classpath", classpath,
        "-no-stdlib",
        "-Xskip-metadata-version-check",
        "-d", "/tmp/android_doc_test_out",
        str(source_file),
    ]


def build_javac_cmd(source_file, classpath):
    return [
        "javac",
        "-classpath", classpath,
        "-d", "/tmp/android_doc_test_out",
        str(source_file),
    ]


ERROR_RE = re.compile(r"^(.*\.kt):(\d+):(\d+):\s*(error|warning):\s*(.*)$")
JAVA_ERROR_RE = re.compile(r"^(.*\.java):(\d+):\s*(error):\s*(.*)$")
KOTLIN_ERROR_RE = re.compile(r"^(.*):(\d+):\s*(error|warning):\s*(.*)$")

SKIP_MESSAGES = [
    "w: KLIB",
    "warning: parameter",
    "warning: variable",
    "Kotlin Metadata",
]


def parse_kotlin_output(output, source_file):
    errors = []
    warnings = []
    for line in output.splitlines():
        if any(s in line for s in SKIP_MESSAGES):
            continue
        m = KOTLIN_ERROR_RE.match(line)
        if m:
            kind = m.group(3).lower()
            msg = f"{line.strip()}"
            if kind == "error":
                errors.append(msg)
            else:
                warnings.append(msg)
    return errors, warnings


def parse_java_output(output, source_file):
    errors = []
    for line in output.splitlines():
        line = line.strip()
        if not line:
            continue
        if "error:" in line:
            errors.append(line)
    return errors


def parse_source_meta(source_file):
    """Read // source: <page>:<start>-<end> comment from first line."""
    lines = Path(source_file).read_text().splitlines()
    if lines and lines[0].startswith("// source:"):
        rest = lines[0][len("// source:"):].strip()
        if ":" in rest:
            colon = rest.rfind(":")
            page = rest[:colon]
            lines_part = rest[colon + 1:]
            if "-" in lines_part:
                try:
                    start, end = lines_part.split("-")
                    return page, [int(start), int(end)]
                except ValueError:
                    pass
    return str(source_file), [0, 0]


def compile_kotlin(source_file, classpath, kotlin_stdlib, annotations):
    import os
    os.makedirs("/tmp/android_doc_test_out", exist_ok=True)
    cmd = build_kotlinc_cmd(source_file, classpath, kotlin_stdlib, annotations)
    result = subprocess.run(cmd, capture_output=True, text=True)
    output = result.stderr + result.stdout
    errors, warnings = parse_kotlin_output(output, source_file)
    return errors, warnings, result.returncode


def compile_java(source_file, classpath):
    import os
    os.makedirs("/tmp/android_doc_test_out", exist_ok=True)
    cmd = build_javac_cmd(source_file, classpath)
    result = subprocess.run(cmd, capture_output=True, text=True)
    output = result.stderr + result.stdout
    errors = parse_java_output(output, source_file)
    return errors, [], result.returncode


def run_all():
    print("Android doc-as-test: building classpath...")
    try:
        compile_cp, kotlin_stdlib, annotations = build_classpath()
    except FileNotFoundError as e:
        print(f"FATAL: {e}", file=sys.stderr)
        sys.exit(1)

    manifest_path = OUTPUT_DIR / "_manifest.json"
    if not manifest_path.exists():
        print("No manifest found. Run extract-blocks.py first.", file=sys.stderr)
        sys.exit(1)

    manifest = json.loads(manifest_path.read_text())
    all_kt = sorted(OUTPUT_DIR.glob("*.kt"))
    all_java = sorted(OUTPUT_DIR.glob("*.java"))
    source_files = all_kt + all_java

    print(f"Compiling {len(all_kt)} Kotlin + {len(all_java)} Java files...")

    passed = 0
    failed = 0
    total_warnings = 0
    by_page = {}
    failures = []

    for src in source_files:
        page_path, line_range = parse_source_meta(src)
        is_kt = src.suffix == ".kt"

        if is_kt:
            errors, warnings, rc = compile_kotlin(src, compile_cp, kotlin_stdlib, annotations)
        else:
            errors, warnings, rc = compile_java(src, compile_cp)

        total_warnings += len(warnings)
        page_stat = by_page.setdefault(page_path, {"passed": 0, "failed": 0, "skipped": 0, "warnings": 0})

        if errors:
            failed += 1
            page_stat["failed"] += 1
            block_index = int(re.search(r"-block-(\d+)\.", src.name).group(1)) if re.search(r"-block-(\d+)\.", src.name) else 0
            failures.append({
                "block_file": src.name,
                "source_page": page_path,
                "block_index": block_index,
                "source_line_range": line_range,
                "errors": errors,
                "warnings": warnings,
                "lang": "kotlin" if is_kt else "java",
            })
            print(f"  FAIL  {src.name} ({len(errors)} error(s))")
            for e in errors[:3]:
                print(f"        {e}")
        else:
            passed += 1
            page_stat["passed"] += 1
            if warnings:
                page_stat["warnings"] += len(warnings)

    # Add skipped from manifest
    for skip_info in manifest.get("skipped_blocks", []):
        page_path = skip_info.get("file", "unknown")
        if page_path in by_page:
            by_page[page_path]["skipped"] += 1
        else:
            by_page[page_path] = {"passed": 0, "failed": 0, "skipped": 1, "warnings": 0}

    skipped_count = manifest.get("total_skipped", 0)
    total = passed + failed

    if total > 0:
        pass_rate = round(passed / total * 100, 1)
        effective_total = passed + failed
        effective_rate = round(passed / effective_total * 100, 1) if effective_total > 0 else 0.0
    else:
        pass_rate = 0.0
        effective_rate = 0.0

    print(f"\nResults: {passed}/{total} passed, {skipped_count} skipped, {total_warnings} warnings")
    if failed > 0:
        print(f"FAIL — {failed} block(s) have errors")
    else:
        print("PASS — all extracted blocks compile cleanly")

    result = {
        "run_at": datetime.now(timezone.utc).isoformat(),
        "stats": {
            "blocks_extracted": manifest.get("total_extracted", total),
            "blocks_skipped": skipped_count,
            "blocks_passed": passed,
            "blocks_failed": failed,
            "total_warnings": total_warnings,
            "pass_rate": pass_rate,
            "effective_rate": effective_rate,
        },
        "by_page": by_page,
        "failures": failures,
    }

    RESULTS_DIR.mkdir(exist_ok=True)
    out = RESULTS_DIR / "latest.json"
    out.write_text(json.dumps(result, indent=2))
    print(f"Results saved to {out}")
    return failed == 0


if __name__ == "__main__":
    ok = run_all()
    sys.exit(0 if ok else 1)
