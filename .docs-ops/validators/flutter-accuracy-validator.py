#!/usr/bin/env python3
"""
Flutter docs-accuracy validator.

Scans all .mdx files for Dart/Flutter references to the Flutter social.plus SDK
public APIs and diffs them against `.docs-ops/sdk-surface/flutter.json`.
Emits a drift report at `.docs-ops/evals/flutter-accuracy-drift.json`.
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

DOCS_OPS_ROOT = Path(__file__).resolve().parent.parent
DOCS_REPO_ROOT = DOCS_OPS_ROOT.parent
SURFACE_PATH = DOCS_OPS_ROOT / "sdk-surface" / "flutter.json"
REPORT_PATH = DOCS_OPS_ROOT / "evals" / "flutter-accuracy-drift.json"

DART_LANGS = {"dart", "flutter"}
BUILTIN_TYPES = {"Future", "Stream", "List", "Map", "Set", "String", "int", "double", "bool", "dynamic"}
FLUTTER_ENUM_ENTRY_ATTRS = {"name", "index", "toString", "hashCode"}

FENCE_RE = re.compile(
    r"^```([A-Za-z0-9_\-]+)[^\n]*\n(.*?)^```",
    re.MULTILINE | re.DOTALL,
)
TYPE_CTOR_RE = re.compile(
    r"\b(Amity[A-Za-z_][A-Za-z0-9_]*)\s*(?:\.\s*([A-Za-z_][A-Za-z0-9_]*))?\s*\(",
)


def load_surface() -> tuple[dict, dict]:
    if not SURFACE_PATH.exists():
        print(f"ERROR: {SURFACE_PATH} not found. Run flutter-extractor.py first.", file=sys.stderr)
        sys.exit(2)
    surface = json.loads(SURFACE_PATH.read_text(encoding="utf-8"))
    return surface.get("types", {}), surface.get("mixins", {})


def build_member_index(types: dict, mixins: dict) -> dict[str, list[str]]:
    index: dict[str, list[str]] = {}
    for container in (types, mixins):
        for type_name, info in container.items():
            for member in info.get("members", []):
                index.setdefault(member["name"], []).append(type_name)
    for refs in index.values():
        refs.sort()
    return index


def has_allowed_enum_entry_attr(info: dict, entry_name: str, attr_name: str) -> bool:
    if info.get("kind") != "enum":
        return False
    if attr_name not in FLUTTER_ENUM_ENTRY_ATTRS:
        return False
    return any(
        member.get("kind") == "enum_value" and member.get("name") == entry_name
        for member in info.get("members", [])
    )



def lookup_path(types: dict, mixins: dict, type_name: str, parts: list[str]) -> bool:
    info = types.get(type_name) or mixins.get(type_name)
    if not info:
        return False
    if not parts:
        return True
    if len(parts) == 2 and has_allowed_enum_entry_attr(info, parts[0], parts[1]):
        return True
    return len(parts) == 1 and any(m["name"] == parts[0] for m in info.get("members", []))


def find_fenced_blocks(text: str) -> list[tuple[str, str, int]]:
    blocks = []
    for match in FENCE_RE.finditer(text):
        lang = match.group(1).lower()
        body = match.group(2)
        start_line = text.count("\n", 0, match.start()) + 1
        blocks.append((lang, body, start_line))
    return blocks


def compile_type_member_re(type_names: set[str]) -> re.Pattern[str] | None:
    if not type_names:
        return None
    ordered_names = sorted(type_names, key=lambda n: (-len(n), n))
    return re.compile(
        r"\b(" + "|".join(re.escape(name) for name in ordered_names) + r")"
        r"((?:[ \t]*\.[ \t]*[A-Za-z_][A-Za-z0-9_]*)+)"
    )


def line_for_offset(text: str, offset: int, start_line: int) -> int:
    return start_line + text.count("\n", 0, offset)


def scan_block(
    body: str,
    start_line: int,
    types: dict,
    mixins: dict,
    member_index: dict[str, list[str]],
    known_type_names: set[str],
    type_member_re: re.Pattern[str] | None,
) -> list[dict]:
    issues: list[dict] = []

    if type_member_re is not None:
        for match in type_member_re.finditer(body):
            type_name = match.group(1)
            member_path = re.sub(r"[ \t]+", "", match.group(2)).lstrip(".")
            parts = member_path.split(".")
            if lookup_path(types, mixins, type_name, parts):
                continue
            issues.append({
                "kind": "unknown_type_member",
                "ref": f"{type_name}.{member_path}",
                "line": line_for_offset(body, match.start(), start_line),
                "hint_present_at": member_index.get(parts[0], []),
            })

    for match in TYPE_CTOR_RE.finditer(body):
        type_name = match.group(1)
        if type_name in BUILTIN_TYPES or type_name in known_type_names:
            continue
        named_ctor = match.group(2)
        ref = f"{type_name}.{named_ctor}" if named_ctor else type_name
        issues.append({
            "kind": "unknown_type",
            "ref": ref,
            "line": line_for_offset(body, match.start(), start_line),
            "hint_present_at": [],
        })

    return issues


def main() -> int:
    types, mixins = load_surface()
    known_type_names = set(types.keys()) | set(mixins.keys())
    member_index = build_member_index(types, mixins)
    type_member_re = compile_type_member_re(known_type_names)

    mdx_files = sorted(DOCS_REPO_ROOT.glob("**/*.mdx"))
    # Exclude paths that document other SDK packages (UIKit, Live Streaming SDK) —
    # those contain Flutter UIKit / Flutter Video SDK API calls that are not part of
    # the Flutter social SDK surface and would always appear as false drift.
    EXCLUDED_PREFIXES = ("uikit/", "social-plus-sdk/video-new/")
    mdx_files = [
        path for path in mdx_files
        if ".docs-ops/" not in str(path.relative_to(DOCS_REPO_ROOT))
        and "node_modules/" not in str(path)
        and ".pytest_cache/" not in str(path)
        and not str(path.relative_to(DOCS_REPO_ROOT)).startswith(EXCLUDED_PREFIXES)
    ]

    per_file_issues: dict[str, list[dict]] = {}
    files_scanned = 0
    dart_blocks_scanned = 0
    total_issues = 0

    for path in mdx_files:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        files_scanned += 1
        file_issues: list[dict] = []
        for lang, body, start_line in find_fenced_blocks(text):
            if lang not in DART_LANGS:
                continue
            dart_blocks_scanned += 1
            file_issues.extend(
                scan_block(body, start_line, types, mixins, member_index, known_type_names, type_member_re)
            )
        if file_issues:
            rel_path = str(path.relative_to(DOCS_REPO_ROOT))
            per_file_issues[rel_path] = file_issues
            total_issues += len(file_issues)

    missing_counts: dict[str, int] = {}
    for issues in per_file_issues.values():
        for issue in issues:
            ref = issue.get("ref", "")
            if ref:
                missing_counts[ref] = missing_counts.get(ref, 0) + 1
    top_missing_refs = sorted(missing_counts.items(), key=lambda kv: (-kv[1], kv[0]))[:20]

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "validator": "flutter-accuracy-validator.py",
        "surface_used": str(SURFACE_PATH.relative_to(DOCS_REPO_ROOT)),
        "stats": {
            "files_scanned": files_scanned,
            "dart_blocks_scanned": dart_blocks_scanned,
            "files_with_issues": len(per_file_issues),
            "total_issues": total_issues,
        },
        "top_missing_refs": [
            {"ref": ref, "doc_occurrences": count} for ref, count in top_missing_refs
        ],
        "issues_by_file": per_file_issues,
    }

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    print(f"wrote {REPORT_PATH.relative_to(DOCS_REPO_ROOT)}", file=sys.stderr)
    print(f"  files scanned: {files_scanned}", file=sys.stderr)
    print(f"  dart blocks: {dart_blocks_scanned}", file=sys.stderr)
    print(f"  files with issues: {len(per_file_issues)}", file=sys.stderr)
    print(f"  total issues: {total_issues}", file=sys.stderr)
    if top_missing_refs:
        print("  top missing refs:", file=sys.stderr)
        for ref, count in top_missing_refs[:10]:
            print(f"    {count:3d}x {ref}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
