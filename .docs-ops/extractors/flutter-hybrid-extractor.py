#!/usr/bin/env python3
"""Flutter hybrid extractor (v0.3.0-hybrid).

Two-pass design mirroring typescript-hybrid-extractor.py:
  Pass 1 — dartdoc index.json  (primary: types, extensions, members)
  Pass 2 — targeted enum-value regex  (fills the one gap dartdoc can't: named enum constants)

Merge rule: dartdoc wins for all type-level + class-member data.
Enum value members are appended per type from Pass 2. No collisions expected
(dartdoc emits only the synthetic .values; regex emits named constants).

Usage:
  # Prereq: run dartdoc once to produce /tmp/flutter-dartdoc-out/index.json
  #   cd <SP_ROOT>/Amity-Social-Cloud-SDK-Flutter-Internal
  #   dart pub global activate dartdoc  (one-time)
  #   dartdoc --output /tmp/flutter-dartdoc-out --no-include-source
  python3 .docs-ops/extractors/flutter-hybrid-extractor.py

Writes:
  .docs-ops/sdk-surface/flutter.json
"""

import json
import os
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
DOCS_OPS_ROOT = SCRIPT_DIR.parent
REPO_ROOT = DOCS_OPS_ROOT.parent.parent   # extractors/ → .docs-ops/ → social-plus-docs/ → sp-sdks/
SDK_ROOT = REPO_ROOT / "Amity-Social-Cloud-SDK-Flutter-Internal"
LIB_ROOT = SDK_ROOT / "lib"
DARTDOC_DIR = Path("/tmp/flutter-dartdoc-out")
OUTPUT = DOCS_OPS_ROOT / "sdk-surface" / "flutter.json"

EXTRACTOR_VERSION = "0.3.0-hybrid"

# ---------------------------------------------------------------------------
# Shared config
# ---------------------------------------------------------------------------
EXCLUDE_PATTERNS = {
    "/test/", "/example/", "/examples/", "/build/",
    "/.dart_tool/", "/.git/", "/.pub-cache/",
}
GENERATED_SUFFIXES = (".g.dart", ".freezed.dart", ".gr.dart", ".config.dart")

# dartdoc kind constants (empirically verified)
KIND_CONST = 1
KIND_CTOR = 2
KIND_CLASS = 3
KIND_ENUM = 5
KIND_EXT = 6
KIND_LIB = 9
KIND_METHOD = 10
KIND_GETTER = 16
KIND_TYPEDEF = 21
MEMBER_KINDS = {KIND_CONST, KIND_CTOR, KIND_METHOD, KIND_GETTER}

# ---------------------------------------------------------------------------
# Pass 1 — dartdoc index.json
# ---------------------------------------------------------------------------

def _member_kind_str(dartdoc_kind: int, parent_kind: int) -> str:
    if dartdoc_kind == KIND_CTOR:
        return "constructor"
    if dartdoc_kind == KIND_METHOD:
        return "func"
    if dartdoc_kind == KIND_GETTER:
        return "getter"
    if dartdoc_kind == KIND_CONST:
        return "enum_value" if parent_kind == KIND_ENUM else "const"
    return "unknown"


def pass1_dartdoc(index_path: Path) -> tuple[dict, list, list, str]:
    """Parse dartdoc index.json. Returns (types, extensions, typedefs, lib_name)."""
    index = json.loads(index_path.read_text())
    print(f"  [pass1] {len(index)} entries", file=sys.stderr)

    by_parent: dict[str, list] = defaultdict(list)
    for e in index:
        parent = e.get("enclosedBy", {}).get("name")
        if parent:
            by_parent[parent].append(e)

    lib_entries = [e for e in index if e.get("kind") == KIND_LIB]
    lib_names = [e["name"] for e in lib_entries]
    # Prefer the package library (matches pubspec `name: amity_sdk`) over incidental
    # part-libraries (e.g. `access_token_renewal`) that can sort first in the index.
    lib_name = "amity_sdk" if "amity_sdk" in lib_names else (lib_names[0] if lib_names else "amity_sdk")

    types: dict[str, dict] = {}
    extensions: list[dict] = []
    typedefs: list[dict] = []

    for e in index:
        if e.get("enclosedBy", {}).get("kind") != KIND_LIB:
            continue
        name = e["name"]
        kind_num = e.get("kind")

        if kind_num in (KIND_CLASS, KIND_ENUM):
            kind_str = "enum" if kind_num == KIND_ENUM else "class"
            children = by_parent.get(name, [])
            members = [
                {
                    "name": c["name"],
                    "kind": _member_kind_str(c.get("kind", 0), kind_num),
                    "overridden_depth": c.get("overriddenDepth", 0),
                }
                for c in children
                if c.get("kind") in MEMBER_KINDS
            ]
            types[name] = {"kind": kind_str, "language": "dart", "members": members}

        elif kind_num == KIND_EXT:
            children = by_parent.get(name, [])
            members = [
                {"name": c["name"], "kind": _member_kind_str(c.get("kind", 0), KIND_CLASS)}
                for c in children
                if c.get("kind") in MEMBER_KINDS
            ]
            extensions.append({"name": name, "members": members})

        elif kind_num == KIND_TYPEDEF:
            typedefs.append({"name": name})

    enum_count = sum(1 for t in types.values() if t["kind"] == "enum")
    print(f"  [pass1] types={len(types)} (enums={enum_count}), exts={len(extensions)}, typedefs={len(typedefs)}", file=sys.stderr)
    return types, extensions, typedefs, lib_name


# ---------------------------------------------------------------------------
# Pass 2 — targeted enum-value regex scan
# ---------------------------------------------------------------------------

DART_ANNOTATION_LINE_RE = re.compile(r'^\s*@\w+(?:\(.*\))?\s*$')
CLASS_RE = re.compile(
    r'^(?:abstract\s+)?(?:sealed\s+)?(?:class|mixin|enum)\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)'
    r'(?:\s+extends|\s+implements|\s+with|\s+on|\s*\{|$)'
)
ENUM_VALUE_RE = re.compile(r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)(?:\s*[,;({]|$)')
EXPORT_RE = re.compile(
    r"export\s+'(?P<path>[^']+)'(?:\s+show\s+(?P<show>[^;]+))?(?:\s+hide\s+(?P<hide>[^;]+))?",
    re.MULTILINE,
)


def _should_exclude(path_str: str) -> bool:
    for pat in EXCLUDE_PATTERNS:
        if pat in path_str:
            return True
    for suffix in GENERATED_SUFFIXES:
        if path_str.endswith(suffix):
            return True
    return False


def _is_private(name: str) -> bool:
    return name.startswith("_")


def _find_barrel(lib_root: Path) -> Path | None:
    candidate = lib_root / "amity_sdk.dart"
    if candidate.exists():
        return candidate.resolve()
    best, best_count = None, 0
    for f in lib_root.glob("*.dart"):
        count = sum(1 for m in EXPORT_RE.finditer(f.read_text(encoding="utf-8", errors="replace"))
                    if not m.group("path").startswith("package:"))
        if count > best_count:
            best_count, best = count, f
    return best.resolve() if best else None


def _resolve_barrel(barrel: Path, lib_root: Path) -> set[str]:
    """Returns set of abs_path strings for all barrel-reachable files."""
    result: set[str] = set()
    visited: set[str] = set()
    lib_root_resolved = lib_root.resolve()
    queue = [barrel.resolve()]
    while queue:
        p = queue.pop()
        ps = str(p)
        if ps in visited:
            continue
        visited.add(ps)
        result.add(ps)
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        for m in EXPORT_RE.finditer(text):
            rel = m.group("path")
            if rel.startswith("package:"):
                continue
            target = (p.parent / rel).resolve()
            if target == lib_root_resolved or lib_root_resolved in target.parents:
                queue.append(target)
    return result


def _extract_enum_values_from_file(filepath: str, content: str, enum_names: set[str]) -> dict[str, list[str]]:
    """Returns {enum_name: [value_name, ...]} for enums found in this file."""
    results: dict[str, list[str]] = {}
    lines = content.splitlines()
    brace_depth = 0
    current_enum: str | None = None
    entry_depth = 0
    in_enum_values = False

    for raw_line in lines:
        line = raw_line.strip()

        if line.startswith("//") or line.startswith("*") or line.startswith("/*"):
            brace_depth += raw_line.count("{") - raw_line.count("}")
            continue
        if DART_ANNOTATION_LINE_RE.match(raw_line):
            continue

        old_depth = brace_depth
        brace_depth += raw_line.count("{") - raw_line.count("}")
        brace_depth = max(0, brace_depth)

        # Pop scope
        if current_enum and brace_depth <= entry_depth:
            current_enum = None
            in_enum_values = False

        # Top-level enum declaration
        if old_depth == 0:
            m = CLASS_RE.match(line)
            if m:
                name = m.group("name")
                if name in enum_names and "enum" in line.split()[0:3]:
                    current_enum = name
                    entry_depth = old_depth
                    in_enum_values = True
                    results[name] = []
                    # Single-line enum: enum Foo { A, B }
                    if "{" in line:
                        body_m = re.search(r'\{([^}]*)\}', line)
                        if body_m:
                            for tok in re.findall(r'\b([A-Za-z_][A-Za-z0-9_]*)\b', body_m.group(1)):
                                if not _is_private(tok) and tok not in ("static", "final", "const"):
                                    results[name].append(tok)
                            in_enum_values = False  # body already consumed
                continue

        # Inside enum body
        if current_enum and in_enum_values and old_depth == entry_depth + 1:
            if ";" in line:
                before = line[:line.index(";")]
                for tok in re.findall(r'\b([A-Za-z_][A-Za-z0-9_]*)\b', before):
                    if not _is_private(tok) and tok not in ("static", "final", "const"):
                        results[current_enum].append(tok)
                in_enum_values = False
                continue
            ev = ENUM_VALUE_RE.match(line)
            if ev:
                val = ev.group(1)
                if not _is_private(val) and val not in ("static", "final", "const"):
                    results[current_enum].append(val)

    return results


def pass2_enum_values(enum_names: set[str]) -> dict[str, list[dict]]:
    """Scan barrel-reachable files; return {enum_name: [member_dicts]}."""
    if not LIB_ROOT.exists():
        print(f"  [pass2] ERROR: {LIB_ROOT} not found", file=sys.stderr)
        return {}

    barrel = _find_barrel(LIB_ROOT)
    if not barrel:
        print("  [pass2] ERROR: no barrel file found", file=sys.stderr)
        return {}

    public_files = _resolve_barrel(barrel, LIB_ROOT)
    print(f"  [pass2] {len(public_files)} barrel-reachable files", file=sys.stderr)

    all_values: dict[str, list[dict]] = {name: [] for name in enum_names}
    files_scanned = 0

    for root, dirs, files in os.walk(LIB_ROOT):
        dirs[:] = [d for d in dirs if not _should_exclude(os.path.join(root, d) + "/")]
        for fname in files:
            if not fname.endswith(".dart"):
                continue
            abs_path = str((Path(root) / fname).resolve())
            if _should_exclude(abs_path) or abs_path not in public_files:
                continue
            try:
                content = Path(abs_path).read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            found = _extract_enum_values_from_file(abs_path, content, enum_names)
            for ename, vals in found.items():
                for v in vals:
                    all_values[ename].append({"name": v, "kind": "enum_value"})
            files_scanned += 1

    enum_vals_total = sum(len(v) for v in all_values.values())
    print(f"  [pass2] scanned {files_scanned} files, found {enum_vals_total} enum values across {sum(1 for v in all_values.values() if v)} enums", file=sys.stderr)
    return all_values


# ---------------------------------------------------------------------------
# Merge
# ---------------------------------------------------------------------------

def merge(types: dict, extensions: list, typedefs: list, enum_values: dict[str, list]) -> dict:
    """Merge Pass 1 (dartdoc) with Pass 2 (enum values). dartdoc wins; enum values appended."""
    merge_notes: list[str] = []

    for ename, vals in enum_values.items():
        if ename not in types:
            merge_notes.append(f"ENUM_NOT_IN_DARTDOC: {ename} (had {len(vals)} values — skipped)")
            continue
        t = types[ename]
        existing_names = {m["name"] for m in t["members"]}
        added = 0
        for v in vals:
            if v["name"] not in existing_names:
                t["members"].append(v)
                added += 1
            elif v["name"] == "values":
                pass  # skip synthetic; keep dartdoc's .values
        if added:
            merge_notes.append(f"ADDED_ENUM_VALUES: {ename} +{added}")

    return merge_notes


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    index_path = DARTDOC_DIR / "index.json"
    if not index_path.exists():
        print(f"ERROR: {index_path} not found.", file=sys.stderr)
        print("Run: cd <FlutterSDK> && dartdoc --output /tmp/flutter-dartdoc-out --no-include-source", file=sys.stderr)
        sys.exit(1)

    print("Pass 1 — dartdoc index.json …", file=sys.stderr)
    types, extensions, typedefs, lib_name = pass1_dartdoc(index_path)

    enum_names = {name for name, t in types.items() if t["kind"] == "enum"}
    print(f"Pass 2 — enum-value regex ({len(enum_names)} enums) …", file=sys.stderr)
    enum_values = pass2_enum_values(enum_names)

    print("Merging …", file=sys.stderr)
    merge_notes = merge(types, extensions, typedefs, enum_values)
    if merge_notes:
        print(f"  merge_notes: {merge_notes[:5]}", file=sys.stderr)

    # Build final output (schema-compatible with existing flutter.json)
    members_total = sum(len(t["members"]) for t in types.values())
    ext_member_total = sum(len(x["members"]) for x in extensions)
    enum_vals_total = sum(
        sum(1 for m in t["members"] if m["kind"] == "enum_value")
        for t in types.values()
        if t["kind"] == "enum"
    )

    surface = {
        "extractor_version": EXTRACTOR_VERSION,
        "extractor": "flutter-hybrid-extractor.py",
        "extracted_at": datetime.now(timezone.utc).isoformat(),
        "sdk_product": lib_name,
        "sdk_source_roots": [str(SDK_ROOT)],
        "sources": {
            "pass1": "dartdoc index.json (types, extensions, class members)",
            "pass2": "barrel-constrained regex (enum values only)",
        },
        "types": types,
        "mixins": {},
        "extensions": extensions,
        "global_funcs": [],
        "global_consts": [],
        "typedefs": typedefs,
        "unhandled": [],
        "merge_notes": merge_notes,
        "stats": {
            "types": len(types),
            "enums": sum(1 for t in types.values() if t["kind"] == "enum"),
            "classes": sum(1 for t in types.values() if t["kind"] == "class"),
            "mixins": 0,
            "extensions": len(extensions),
            "typedefs": len(typedefs),
            "members_total": members_total,
            "extension_members_total": ext_member_total,
            "enum_values_total": enum_vals_total,
            "global_funcs": 0,
            "global_consts": 0,
        },
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(surface, indent=2, ensure_ascii=False))
    print(f"Written → {OUTPUT}", file=sys.stderr)
    print(f"  types={len(types)}, extensions={len(extensions)}, members_total={members_total}, enum_values={enum_vals_total}", file=sys.stderr)


if __name__ == "__main__":
    main()
