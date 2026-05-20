#!/usr/bin/env python3
"""
TypeDoc-based TypeScript SDK surface extractor  (v0.2.0-typedoc)

Reads the JSON output from TypeDoc run against the @amityco/ts-sdk source and
produces `.docs-ops/sdk-surface/typescript-from-typedoc.json` with the same
schema shape as the existing `typescript.json` (regex-based), so downstream
validators and comparison scripts can do direct diffs.

## How to generate the TypeDoc input

From the TS SDK repo root (AmityTypescriptSDK/):

    cd packages/sdk
    npm install --no-save --legacy-peer-deps typedoc
    npx typedoc --json /tmp/typedoc-output.json src/index.ts \\
      --tsconfig tsconfig.json \\
      --skipErrorChecking \\
      --excludeExternals

This takes ~10s and produces a ~2.4 MB JSON file.  The flag `--excludeExternals`
keeps vendor type definitions out of the surface.

## Known structural gap vs regex extractor

The `declare global { namespace Amity { ... } }` declarations spread across
`src/@types/domains/*.ts` are ambient module augmentations.  TypeDoc
`--skipErrorChecking` mode does not surface them as a named `Amity` namespace.
The regex extractor scraped these directly and produced 946 `Amity.*` members.

This means typescript-from-typedoc.json will NOT contain an "Amity" namespace.
That is documented in the comparison artifact.  Workaround candidates:
  - Post-process the TypeDoc JSON with a secondary pass over `@types/` files
  - Use TypeDoc's `--entryPoints` with a wrapper that re-exports `Amity`
  - Accept the gap and rely on doc-as-test for Amity.* ref validation

## Output schema

Same as typescript.json:

    {
      "extractor_version": "0.2.0-typedoc",
      "extractor": "typescript-typedoc-extractor.py",
      "extracted_at": "<iso>",
      "sdk_package": "@amityco/ts-sdk",
      "sdk_typedoc_source": "<abs path to typedoc JSON>",
      "namespaces": {
        "<NsName>": {
          "source_module": "<fileName>",
          "member_count": N,
          "members": [
            { "name": "...", "kind": "function|const|class|interface|enum|type",
              "file": "...", "line": N,
              "signature": { "parameters": [...], "returns": "..." }  // BONUS
            }
          ],
          "sub_namespaces": { ... same shape ... }
        }
      },
      "root_exports": [ { "name": "...", "kind": "...", "file": "...", "line": N } ],
      "stats": { ... }
    }
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

DOCS_OPS_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = DOCS_OPS_ROOT / "sdk-surface" / "typescript-from-typedoc.json"

# TypeDoc JSON path — can be overridden via CLI arg
DEFAULT_TYPEDOC_JSON = Path("/tmp/typedoc-output.json")

# ---------------------------------------------------------------------------
# TypeDoc kind constants (TypeDoc 0.26.x)
# ---------------------------------------------------------------------------
TD_MODULE       = 4
TD_ENUM         = 8
TD_ENUM_MEMBER  = 16
TD_VARIABLE     = 32
TD_FUNCTION     = 64
TD_CLASS        = 128
TD_INTERFACE    = 256
TD_CONSTRUCTOR  = 512
TD_PROPERTY     = 1024
TD_METHOD       = 2048
TD_CALL_SIG     = 4096
TD_TYPE_ALIAS   = 16384

# Mapping from TypeDoc kind → schema kind string
KIND_MAP: dict[int, str] = {
    TD_ENUM:       "enum",
    TD_ENUM_MEMBER:"enum_member",
    TD_VARIABLE:   "const",
    TD_FUNCTION:   "function",
    TD_CLASS:      "class",
    TD_INTERFACE:  "interface",
    TD_PROPERTY:   "property",
    TD_METHOD:     "method",
    TD_TYPE_ALIAS: "type",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _source(node: dict) -> tuple[str, int | None]:
    """Return (fileName, line) from a TypeDoc node's sources list."""
    sources = node.get("sources", [])
    if sources:
        s = sources[0]
        return s.get("fileName", ""), s.get("line")
    return "", None


def _sig_type_str(t: dict | None) -> str:
    """Recursively render a TypeDoc type node to a compact string."""
    if t is None:
        return ""
    kind = t.get("type", "")
    if kind == "intrinsic":
        return t.get("name", "unknown")
    if kind == "reference":
        name = t.get("name", "unknown")
        args = t.get("typeArguments", [])
        if args:
            return f"{name}<{', '.join(_sig_type_str(a) for a in args)}>"
        return name
    if kind == "array":
        return f"{_sig_type_str(t.get('elementType'))}[]"
    if kind == "union":
        return " | ".join(_sig_type_str(u) for u in t.get("types", []))
    if kind == "intersection":
        return " & ".join(_sig_type_str(i) for i in t.get("types", []))
    if kind == "tuple":
        return f"[{', '.join(_sig_type_str(el.get('element', el)) for el in t.get('elements', []))}]"
    if kind == "literal":
        return repr(t.get("value", ""))
    if kind == "predicate":
        return f"asserts {t.get('name', '?')}"
    if kind == "query":
        return f"typeof {_sig_type_str(t.get('queryType'))}"
    if kind == "templateLiteral":
        return "string"
    if kind == "mapped":
        return "object"
    if kind == "conditional":
        return _sig_type_str(t.get("trueType"))
    if kind == "reflection":
        return "{}"
    if kind == "rest":
        return f"...{_sig_type_str(t.get('elementType'))}"
    if kind == "optional":
        return f"{_sig_type_str(t.get('elementType'))}?"
    if kind == "named-tuple-member":
        elem = t.get("element", {})
        return f"{t.get('name', '?')}: {_sig_type_str(elem)}"
    if kind == "void" or t.get("name") == "void":
        return "void"
    return t.get("name", kind or "unknown")


def _extract_signature(node: dict) -> dict | None:
    """Extract signature info (parameters + return type) from a function/method node."""
    sigs = node.get("signatures", [])
    if not sigs:
        return None
    sig = sigs[0]
    params = []
    for p in sig.get("parameters", []):
        param_entry = {"name": p.get("name", "?")}
        ptype = p.get("type")
        if ptype:
            param_entry["type"] = _sig_type_str(ptype)
        if p.get("flags", {}).get("isOptional"):
            param_entry["optional"] = True
        params.append(param_entry)
    ret_type = _sig_type_str(sig.get("type"))
    return {
        "parameters": params,
        "returns": ret_type or "void",
    }


def _make_member(node: dict) -> dict:
    """Convert a TypeDoc leaf node into a surface member entry."""
    kind_int = node.get("kind", 0)
    kind_str = KIND_MAP.get(kind_int, "unknown")
    file_, line = _source(node)

    entry: dict = {
        "name": node["name"],
        "kind": kind_str,
        "file": file_,
        "line": line,
    }

    # Bonus: capture signature when available
    sig = _extract_signature(node)
    if sig and (sig["parameters"] or sig["returns"] not in ("", "void")):
        entry["signature"] = sig

    return entry


def _process_namespace(ns_node: dict) -> dict:
    """
    Recurse into a TypeDoc Module node and build the namespace surface entry.
    Sub-modules (kind=TD_MODULE) become sub_namespaces.
    Everything else becomes a member.
    """
    members: list[dict] = []
    sub_namespaces: dict[str, dict] = {}

    source_module, _ = _source(ns_node)

    for child in ns_node.get("children", []):
        ckind = child.get("kind", 0)
        if ckind == TD_MODULE:
            # Recursive sub-namespace
            sub_namespaces[child["name"]] = _process_namespace(child)
        elif ckind in KIND_MAP:
            members.append(_make_member(child))
            # For enums: also emit enum members as flattened "EnumName.MemberName" entries
            if ckind == TD_ENUM:
                for ec in child.get("children", []):
                    if ec.get("kind") == TD_ENUM_MEMBER:
                        ec_file, ec_line = _source(ec)
                        members.append({
                            "name": f"{child['name']}.{ec['name']}",
                            "kind": "enum_member",
                            "file": ec_file or source_module,
                            "line": ec_line,
                        })
        # Skip constructors, call signatures, etc. — implementation details

    # Prefer the source of the first non-empty source among members
    if not source_module and members:
        source_module = members[0].get("file", "")

    return {
        "source_module": source_module,
        "member_count": len(members),
        "members": members,
        "sub_namespaces": sub_namespaces,
    }


# ---------------------------------------------------------------------------
# Main extraction
# ---------------------------------------------------------------------------

def extract(typedoc_path: Path) -> dict:
    if not typedoc_path.exists():
        print(
            f"ERROR: TypeDoc JSON not found at {typedoc_path}\n"
            "Run from AmityTypescriptSDK/packages/sdk/:\n"
            "  npm install --no-save --legacy-peer-deps typedoc\n"
            "  npx typedoc --json /tmp/typedoc-output.json src/index.ts "
            "--tsconfig tsconfig.json --skipErrorChecking --excludeExternals",
            file=sys.stderr,
        )
        sys.exit(2)

    raw = json.loads(typedoc_path.read_text(encoding="utf-8"))

    namespaces: dict[str, dict] = {}
    root_exports: list[dict] = []

    # Top-level children of the project node
    for child in raw.get("children", []):
        ckind = child.get("kind", 0)
        if ckind == TD_MODULE:
            namespaces[child["name"]] = _process_namespace(child)
        elif ckind in KIND_MAP:
            file_, line = _source(child)
            entry: dict = {
                "name": child["name"],
                "kind": KIND_MAP[ckind],
                "file": file_,
                "line": line,
            }
            sig = _extract_signature(child)
            if sig and (sig["parameters"] or sig["returns"] not in ("", "void")):
                entry["signature"] = sig
            # Flatten top-level enum members
            if ckind == TD_ENUM:
                for ec in child.get("children", []):
                    if ec.get("kind") == TD_ENUM_MEMBER:
                        ec_f, ec_l = _source(ec)
                        root_exports.append({
                            "name": f"{child['name']}.{ec['name']}",
                            "kind": "enum_member",
                            "file": ec_f or file_,
                            "line": ec_l,
                        })
            root_exports.append(entry)

    # Stats
    ns_member_total = sum(
        v["member_count"] + sum(sv["member_count"] for sv in v["sub_namespaces"].values())
        for v in namespaces.values()
    )
    sub_ns_total = sum(len(v["sub_namespaces"]) for v in namespaces.values())

    stats = {
        "namespaces": len(namespaces),
        "sub_namespaces_total": sub_ns_total,
        "namespaced_members_total": ns_member_total,
        "amity_global_members": 0,   # TypeDoc gap — see docstring
        "root_exports": len(root_exports),
        "typedoc_note": (
            "declare global namespace Amity{} augmentations (~946 members in regex extractor) "
            "are NOT captured by TypeDoc --skipErrorChecking against src/index.ts. "
            "amity_global_members=0 reflects this structural gap."
        ),
    }

    return {
        "extractor_version": "0.2.0-typedoc",
        "extractor": "typescript-typedoc-extractor.py",
        "extracted_at": datetime.now(timezone.utc).isoformat(),
        "sdk_package": "@amityco/ts-sdk",
        "sdk_typedoc_source": str(typedoc_path.resolve()),
        "namespaces": namespaces,
        "root_exports": root_exports,
        "stats": stats,
    }


def main() -> None:
    typedoc_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_TYPEDOC_JSON
    result = extract(typedoc_path)

    OUTPUT_PATH.write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    stats = result["stats"]
    print(f"[typescript-typedoc-extractor] wrote {OUTPUT_PATH}")
    print(
        f"[typescript-typedoc-extractor] "
        f"namespaces={stats['namespaces']} "
        f"sub_namespaces={stats['sub_namespaces_total']} "
        f"namespaced_members={stats['namespaced_members_total']} "
        f"root_exports={stats['root_exports']} "
        f"amity_global_members={stats['amity_global_members']} (gap: see stats.typedoc_note)"
    )


if __name__ == "__main__":
    main()
