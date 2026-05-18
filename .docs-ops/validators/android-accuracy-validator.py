#!/usr/bin/env python3
"""
Android docs-accuracy validator.

Scans all .mdx files for Kotlin/Java references to the Android social.plus SDK
public APIs and diffs them against `.docs-ops/sdk-surface/android.json`.
Emits a drift report at `.docs-ops/evals/android-accuracy-drift.json`.

Detection scope (conservative, low false-positive):
  1. Inside ```kotlin fenced code blocks:
       a. Type-level refs: `<TypeName>.<member>` where TypeName is in `types`
          or `interfaces` from android.json.
       b. Imports: flag `import com.amity...Xxx` / `import co.amity...Xxx`
          where the leaf name looks SDK-ish (Amity*/Eko*) but is not known.
  2. Inside ```java fenced code blocks: same checks.
  3. v1 out of scope: signature validation, inferred-type member access,
     generics-aware resolution, references outside fenced code blocks.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

DOCS_OPS_ROOT = Path(__file__).resolve().parent.parent
DOCS_REPO_ROOT = DOCS_OPS_ROOT.parent
SURFACE_PATH = DOCS_OPS_ROOT / "sdk-surface" / "android.json"
REPORT_PATH = DOCS_OPS_ROOT / "evals" / "android-accuracy-drift.json"

KOTLIN_LANGS = {"kotlin"}
JAVA_LANGS = {"java"}
ALL_ANDROID_LANGS = KOTLIN_LANGS | JAVA_LANGS

# Path prefixes (relative to repo root) to skip entirely.
# uikit/ contains Android UIKit SDK docs — different product, not in android.json surface.
# social-plus-sdk/video-new/ uses AmityStream* types in a separate video SDK context.
EXCLUDED_PATH_PREFIXES = {"uikit/", "social-plus-sdk/video-new/"}

# Android platform / system classes that are NOT Amity SDK types.
# The Android surface has an unrelated `Environment` class (sdk-versioning enum);
# the platform class android.os.Environment should never be flagged.
ANDROID_PLATFORM_TYPES = {
    "Environment", "Context", "Activity", "Intent", "Bundle",
    "Uri", "View", "Application", "Fragment", "Service",
}

ANDROID_ENUM_ENTRY_ATTRS = {
    "code", "name", "ordinal", "value", "displayName", "toString", "apply",
}

# Refs confirmed valid in source but not captured by extractor v1.2.
# "TypeName.path" -> reason. These are NOT flagged even if lookup fails.
#   AmityRoom.ParticipantType.CoHost — real PascalCase enum entry in AmityRoom.kt;
#     extractor only captures UPPER_SNAKE entries (regex [A-Z][A-Z0-9_]+).
#   AmityPinnedPost.post — real `var post: AmityPost?` data class constructor param;
#     extractor does not capture auto-generated data class properties (v1.3 gap).
KNOWN_VALID_REFS: dict[str, str] = {
    "AmityRoom.ParticipantType.CoHost": "real PascalCase enum entry in AmityRoom.kt; extractor v1.2 only captures UPPER_SNAKE entries",
    "AmityPinnedPost.post": "real data class property `var post: AmityPost?` in AmityPinnedPost.kt; extractor v1.x does not capture data class constructor params (v1.3 gap)",
}

FENCE_RE = re.compile(
    r"^```([A-Za-z0-9_\-]+)[^\n]*\n(.*?)^```",
    re.MULTILINE | re.DOTALL,
)
IMPORT_RE = re.compile(
    r"^\s*import\s+(?:com|co)\.amity(?:\.[A-Za-z_]\w*)+\.(\w+)\b",
    re.MULTILINE,
)


def load_surface() -> tuple[dict, dict]:
    """Return (types_dict, interfaces_dict) from android.json."""
    if not SURFACE_PATH.exists():
        print(f"ERROR: {SURFACE_PATH} not found. Run android-extractor.py first.", file=sys.stderr)
        sys.exit(2)
    surface = json.loads(SURFACE_PATH.read_text(encoding="utf-8"))
    return surface.get("types", {}), surface.get("interfaces", {})


def build_hint_index(types: dict, interfaces: dict) -> dict[str, list[str]]:
    """Map member/nested-type name -> list of containing type paths for hints."""
    index: dict[str, list[str]] = {}
    for container in (types, interfaces):
        for type_name, info in container.items():
            for member in info.get("members", []):
                index.setdefault(member["name"], []).append(type_name)
            for nested in info.get("nested_types", []):
                nested_name = nested.get("name")
                if nested_name:
                    index.setdefault(nested_name, []).append(f"{type_name}.{nested_name}")
    for locations in index.values():
        locations.sort()
    return index


def has_allowed_enum_entry_attr(info: dict, entry_name: str, attr_name: str) -> bool:
    if info.get("kind") not in {"enum", "enum_class"}:
        return False
    if attr_name not in ANDROID_ENUM_ENTRY_ATTRS:
        return False
    return any(
        member.get("kind") == "enum_entry" and member.get("name") == entry_name
        for member in info.get("members", [])
    )



def lookup_path(types: dict, interfaces: dict, type_name: str, parts: list[str]) -> bool:
    """Walk a dotted member path from type_name through nested types.

    lookup_path(types, interfaces, "AmityFoo", ["NestedBar"]) → True if NestedBar is
    a member or nested_type of AmityFoo.
    lookup_path(types, interfaces, "AmityFoo", ["NestedBar", "method"]) → True if method
    is a member of AmityFoo.nested_types[NestedBar], OR if method is a nested_type of
    AmityFoo.nested_types[NestedBar].
    """
    info = types.get(type_name) or interfaces.get(type_name)
    if not info:
        return False
    if not parts:
        return True
    if len(parts) == 2 and has_allowed_enum_entry_attr(info, parts[0], parts[1]):
        return True
    head, *rest = parts
    # Check direct members (includes enum_entry, func, val, var)
    if not rest and any(m["name"] == head for m in info.get("members", [])):
        return True
    # Check nested_types by name
    nested = next((nt for nt in info.get("nested_types", []) if nt.get("name") == head), None)
    if nested is not None:
        if not rest:
            return True
        tail = rest[0]
        # Check nested type's members
        if any(m["name"] == tail for m in nested.get("members", [])):
            return True
        # Check nested type's nested_types (3-level: TypeName.NestedType.InnerType)
        if any(nn.get("name") == tail for nn in nested.get("nested_types", [])):
            return True
    return False


def lookup_member(types: dict, interfaces: dict, type_name: str, member_name: str) -> bool:
    return lookup_path(types, interfaces, type_name, [member_name])


def find_fenced_blocks(text: str) -> list[tuple[str, str, int]]:
    """Return list of (lang, body, start_line_1indexed) for each fenced code block."""
    blocks = []
    for match in FENCE_RE.finditer(text):
        lang = match.group(1).lower()
        body = match.group(2)
        start_line = text.count("\n", 0, match.start()) + 1
        blocks.append((lang, body, start_line))
    return blocks


def build_type_member_regex(type_names: set[str]) -> re.Pattern[str] | None:
    if not type_names:
        return None
    ordered_names = sorted(type_names)
    # Capture TypeName followed by one or more dotted segments
    return re.compile(
        r"\b(" + "|".join(re.escape(name) for name in ordered_names) + r")"
        r"((?:\.[A-Za-z_][A-Za-z0-9_]*)+)"
    )


def scan_block(
    body: str,
    start_line: int,
    types: dict,
    interfaces: dict,
    type_member_re: re.Pattern[str] | None,
    hint_index: dict[str, list[str]],
) -> list[dict]:
    issues: list[dict] = []

    if type_member_re is not None:
        for match in type_member_re.finditer(body):
            type_name = match.group(1)
            # Skip Android platform types — they're not Amity SDK types
            if type_name in ANDROID_PLATFORM_TYPES:
                continue
            member_path = match.group(2).lstrip(".")  # strip leading dot
            parts = member_path.split(".")
            if lookup_path(types, interfaces, type_name, parts):
                continue
            full_ref = f"{type_name}.{member_path}"
            # Skip refs confirmed valid in source but not captured by extractor
            if full_ref in KNOWN_VALID_REFS:
                continue
            line_in_block = body.count("\n", 0, match.start()) + 1
            issues.append({
                "kind": "unknown_type_member",
                "ref": full_ref,
                "line": start_line + line_in_block - 1,
                "hint_present_at": hint_index.get(parts[0], []),
            })

    for match in IMPORT_RE.finditer(body):
        leaf_name = match.group(1)
        if not (leaf_name.startswith("Amity") or leaf_name.startswith("Eko")):
            continue
        if leaf_name in types or leaf_name in interfaces:
            continue
        line_in_block = body.count("\n", 0, match.start()) + 1
        issues.append({
            "kind": "unknown_import",
            "ref": leaf_name,
            "line": start_line + line_in_block - 1,
            "hint_present_at": [],
        })

    return issues


def main() -> int:
    types, interfaces = load_surface()
    type_names = set(types.keys()) | set(interfaces.keys())
    type_member_re = build_type_member_regex(type_names)
    hint_index = build_hint_index(types, interfaces)

    mdx_files = sorted(DOCS_REPO_ROOT.glob("**/*.mdx"))
    mdx_files = [
        path for path in mdx_files
        if ".docs-ops/" not in str(path.relative_to(DOCS_REPO_ROOT))
        and "node_modules/" not in str(path)
        and ".pytest_cache/" not in str(path)
        and not any(str(path.relative_to(DOCS_REPO_ROOT)).startswith(p) for p in EXCLUDED_PATH_PREFIXES)
    ]

    per_file_issues: dict[str, list[dict]] = {}
    files_scanned = 0
    kotlin_blocks_scanned = 0
    java_blocks_scanned = 0

    for path in mdx_files:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        files_scanned += 1
        file_issues: list[dict] = []
        for lang, body, start_line in find_fenced_blocks(text):
            if lang in KOTLIN_LANGS:
                kotlin_blocks_scanned += 1
            elif lang in JAVA_LANGS:
                java_blocks_scanned += 1
            else:
                continue
            file_issues.extend(
                scan_block(body, start_line, types, interfaces, type_member_re, hint_index)
            )
        if file_issues:
            per_file_issues[str(path.relative_to(DOCS_REPO_ROOT))] = file_issues

    missing_counts = Counter()
    for issues in per_file_issues.values():
        for issue in issues:
            missing_counts[issue["ref"]] += 1
    top_missing = [
        {"ref": ref, "doc_occurrences": count}
        for ref, count in sorted(missing_counts.items(), key=lambda item: (-item[1], item[0]))[:20]
    ]

    total_issues = sum(len(issues) for issues in per_file_issues.values())
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "validator": "android-accuracy-validator.py",
        "surface_used": str(SURFACE_PATH.relative_to(DOCS_REPO_ROOT)),
        "stats": {
            "files_scanned": files_scanned,
            "kotlin_blocks_scanned": kotlin_blocks_scanned,
            "java_blocks_scanned": java_blocks_scanned,
            "files_with_issues": len(per_file_issues),
            "total_issues": total_issues,
        },
        "top_missing_refs": top_missing,
        "issues_by_file": per_file_issues,
    }

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    print(f"wrote {REPORT_PATH.relative_to(DOCS_REPO_ROOT)}", file=sys.stderr)
    print(f"  files scanned: {files_scanned}", file=sys.stderr)
    print(
        f"  kotlin blocks: {kotlin_blocks_scanned}, java blocks: {java_blocks_scanned}",
        file=sys.stderr,
    )
    print(f"  files with issues: {len(per_file_issues)}", file=sys.stderr)
    print(f"  total issues: {total_issues}", file=sys.stderr)
    if top_missing:
        print("  top missing refs:", file=sys.stderr)
        for item in top_missing[:10]:
            print(f"    {item['doc_occurrences']:3d}x {item['ref']}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
