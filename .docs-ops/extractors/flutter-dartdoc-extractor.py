#!/usr/bin/env python3
"""Flutter dartdoc extractor (v0.2.0-dartdoc).

Approach: dart doc index.json parsing (Approach 2).
- Run: cd <FlutterSDK>/ && dart pub global activate dartdoc
        && dartdoc --output /tmp/flutter-dartdoc-out --no-include-source
- This extractor reads /tmp/flutter-dartdoc-out/index.json

Approach 1 (dartdoc --output-format json) was tested but --output-format
is not a valid flag in dartdoc 9.0.4.
Approach 2 (dart doc + parse index.json) succeeded in ~40s.
Approach 3 (dart analyzer programmatic API) was not needed.

dartdoc kind number mapping (empirically verified):
  1  = constant / enum_value (child of class or enum)
  2  = constructor
  3  = class
  5  = enum
  6  = extension
  9  = library
  10 = method
  16 = getter / property / field
  21 = typedef

Output schema: matches flutter.json but adds a top-level 'libraries' key
(required by pilot validator) that wraps the amity_sdk library data.
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from collections import defaultdict

DARTDOC_DIR = Path("/tmp/flutter-dartdoc-out")
SP_ROOT = Path(__file__).resolve().parents[3]
DOCS_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_PATH = DOCS_ROOT / ".docs-ops" / "sdk-surface" / "flutter-from-dartdoc.json"

# dartdoc kind constants
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
TYPE_KINDS = {KIND_CLASS, KIND_ENUM}


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


def build_surface(index: list[dict]) -> dict:
    # Split by parent
    by_parent: dict[str, list[dict]] = defaultdict(list)
    entries_by_qn: dict[str, dict] = {}
    for e in index:
        entries_by_qn[e["qualifiedName"]] = e
        parent = e.get("enclosedBy", {}).get("name")
        if parent:
            by_parent[parent].append(e)

    types: dict[str, dict] = {}
    extensions: list[dict] = []
    typedefs: list[dict] = []

    lib_entries = [e for e in index if e.get("kind") == KIND_LIB]
    lib_name = lib_entries[0]["name"] if lib_entries else "amity_sdk"

    for e in index:
        if e.get("enclosedBy", {}).get("kind") != KIND_LIB:
            continue
        name = e["name"]
        kind_num = e.get("kind")

        if kind_num in TYPE_KINDS:
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
            types[name] = {
                "kind": kind_str,
                "language": "dart",
                "members": members,
            }

        elif kind_num == KIND_EXT:
            children = by_parent.get(name, [])
            members = [
                {
                    "name": c["name"],
                    "kind": _member_kind_str(c.get("kind", 0), KIND_CLASS),
                }
                for c in children
                if c.get("kind") in MEMBER_KINDS
            ]
            extensions.append(
                {
                    "name": name,
                    "members": members,
                }
            )

        elif kind_num == KIND_TYPEDEF:
            typedefs.append({"name": name})

    # Stats
    total_members = sum(len(t["members"]) for t in types.values())
    total_ext_members = sum(len(x["members"]) for x in extensions)
    enum_values = sum(
        sum(1 for m in t["members"] if m["kind"] == "enum_value")
        for t in types.values()
        if t["kind"] == "enum"
    )

    stats = {
        "types": len(types),
        "enums": sum(1 for t in types.values() if t["kind"] == "enum"),
        "classes": sum(1 for t in types.values() if t["kind"] == "class"),
        "extensions": len(extensions),
        "typedefs": len(typedefs),
        "members_total": total_members,
        "extension_members_total": total_ext_members,
        "enum_values_total": enum_values,
        "library": lib_name,
    }

    return {
        "extractor_version": "0.2.0-dartdoc",
        "extractor": "flutter-dartdoc-extractor.py",
        "extracted_at": datetime.now(timezone.utc).isoformat(),
        "sdk_package": lib_name,
        "sdk_source": f"dartdoc/index.json @ {DARTDOC_DIR}",
        "libraries": {
            lib_name: {
                "types": types,
                "extensions": extensions,
                "typedefs": typedefs,
            }
        },
        "stats": stats,
    }


def main():
    index_path = DARTDOC_DIR / "index.json"
    if not index_path.exists():
        print(f"ERROR: {index_path} not found.", file=sys.stderr)
        print("Run: cd <FlutterSDK> && dartdoc --output /tmp/flutter-dartdoc-out --no-include-source", file=sys.stderr)
        sys.exit(1)

    print(f"Loading {index_path} …", file=sys.stderr)
    index = json.loads(index_path.read_text())
    print(f"  {len(index)} entries loaded", file=sys.stderr)

    surface = build_surface(index)

    stats = surface["stats"]
    print(f"  types={stats['types']} (classes={stats['classes']}, enums={stats['enums']})", file=sys.stderr)
    print(f"  extensions={stats['extensions']}, typedefs={stats['typedefs']}", file=sys.stderr)
    print(f"  members_total={stats['members_total']}, enum_values={stats['enum_values_total']}", file=sys.stderr)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(surface, indent=2, ensure_ascii=False))
    print(f"Written → {OUTPUT_PATH}", file=sys.stderr)


if __name__ == "__main__":
    main()
