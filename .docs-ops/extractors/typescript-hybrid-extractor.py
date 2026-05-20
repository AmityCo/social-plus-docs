#!/usr/bin/env python3
"""
TypeScript SDK surface hybrid extractor  (v0.3.0-hybrid)

Merges two passes into a single authoritative surface file:

Pass 1 — TypeDoc JSON (namespaced exports)
  Reads /tmp/typedoc-output.json produced by:
    cd AmityTypescriptSDK/packages/sdk
    npm install --no-save --legacy-peer-deps typedoc
    npx typedoc --json /tmp/typedoc-output.json src/index.ts \\
      --tsconfig tsconfig.json --skipErrorChecking --excludeExternals

  Why TypeDoc for namespaces:
    - Authoritative (compiler-backed — no barrel-following heuristics)
    - Honors @hidden / @private / @internal natively (excludes internal symbols)
    - Captures full signatures (parameters, return types, generics) as bonus

Pass 2 — Targeted @types regex (Amity global namespace)
  Walks AmityTypescriptSDK/packages/sdk/src/@types/domains/*.ts only.
  Extracts declarations inside `declare global { namespace Amity { ... } }` blocks.
  These are ambient global augmentations that TypeDoc does not surface.
  Logic reused from typescript-extractor.py v1.3.

Merge strategy:
  - TypeDoc wins for any namespace present in its output (24 namespaces).
  - The Amity global namespace comes entirely from Pass 2 (TypeDoc has no
    entry for it).
  - Name collisions (same symbol in both passes) → TypeDoc wins; logged in
    merge_notes.

Output schema: same as typescript.json (schema-compatible with validators).
"""
from __future__ import annotations

import importlib.util
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

DOCS_OPS_ROOT = Path(__file__).resolve().parent.parent
DOCS_REPO_ROOT = DOCS_OPS_ROOT.parent
SDKS_ROOT = Path(os.environ.get("SP_SDKS_ROOT", str(DOCS_REPO_ROOT.parent))).resolve()
SDK_ROOT = SDKS_ROOT / "AmityTypescriptSDK" / "packages" / "sdk"
SRC = SDK_ROOT / "src"
ATYPES_DIR = SRC / "@types"

OUTPUT_PATH = DOCS_OPS_ROOT / "sdk-surface" / "typescript.json"
DEFAULT_TYPEDOC_JSON = Path("/tmp/typedoc-output.json")


# ---------------------------------------------------------------------------
# TypeDoc kind constants
# ---------------------------------------------------------------------------
TD_MODULE      = 4
TD_ENUM        = 8
TD_ENUM_MEMBER = 16
TD_VARIABLE    = 32
TD_FUNCTION    = 64
TD_CLASS       = 128
TD_INTERFACE   = 256
TD_PROPERTY    = 1024
TD_METHOD      = 2048
TD_TYPE_ALIAS  = 16384

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
# Pass 1: TypeDoc namespaced extraction
# ---------------------------------------------------------------------------

def _td_source(node: dict) -> tuple[str, int | None]:
    sources = node.get("sources", [])
    if sources:
        s = sources[0]
        return s.get("fileName", ""), s.get("line")
    return "", None


def _td_sig_type(t: dict | None) -> str:
    if t is None:
        return ""
    kind = t.get("type", "")
    if kind == "intrinsic":
        return t.get("name", "unknown")
    if kind == "reference":
        name = t.get("name", "unknown")
        args = t.get("typeArguments", [])
        if args:
            return f"{name}<{', '.join(_td_sig_type(a) for a in args)}>"
        return name
    if kind == "array":
        return f"{_td_sig_type(t.get('elementType'))}[]"
    if kind == "union":
        return " | ".join(_td_sig_type(u) for u in t.get("types", []))
    if kind == "intersection":
        return " & ".join(_td_sig_type(i) for i in t.get("types", []))
    if kind in ("literal",):
        return repr(t.get("value", ""))
    if kind in ("reflection",):
        return "{}"
    if kind == "rest":
        return f"...{_td_sig_type(t.get('elementType'))}"
    if kind == "optional":
        return f"{_td_sig_type(t.get('elementType'))}?"
    if kind == "predicate":
        return f"asserts {t.get('name', '?')}"
    if kind == "query":
        return f"typeof {_td_sig_type(t.get('queryType'))}"
    return t.get("name", kind or "unknown")


def _td_extract_sig(node: dict) -> dict | None:
    sigs = node.get("signatures", [])
    if not sigs:
        return None
    sig = sigs[0]
    params = []
    for p in sig.get("parameters", []):
        pe: dict = {"name": p.get("name", "?")}
        pt = p.get("type")
        if pt:
            pe["type"] = _td_sig_type(pt)
        if p.get("flags", {}).get("isOptional"):
            pe["optional"] = True
        params.append(pe)
    ret = _td_sig_type(sig.get("type"))
    return {"parameters": params, "returns": ret or "void"}


def _td_make_member(node: dict) -> dict:
    kind_str = KIND_MAP.get(node.get("kind", 0), "unknown")
    file_, line = _td_source(node)
    entry: dict = {"name": node["name"], "kind": kind_str, "file": file_, "line": line}
    sig = _td_extract_sig(node)
    if sig and (sig["parameters"] or sig["returns"] not in ("", "void")):
        entry["signature"] = sig
    return entry


def _td_process_namespace(ns_node: dict) -> dict:
    members: list[dict] = []
    sub_namespaces: dict[str, dict] = {}
    source_module, _ = _td_source(ns_node)
    for child in ns_node.get("children", []):
        ck = child.get("kind", 0)
        if ck == TD_MODULE:
            sub_namespaces[child["name"]] = _td_process_namespace(child)
        elif ck in KIND_MAP:
            members.append(_td_make_member(child))
            if ck == TD_ENUM:
                for ec in child.get("children", []):
                    if ec.get("kind") == TD_ENUM_MEMBER:
                        ef, el = _td_source(ec)
                        members.append({
                            "name": f"{child['name']}.{ec['name']}",
                            "kind": "enum_member",
                            "file": ef or source_module,
                            "line": el,
                        })
    if not source_module and members:
        source_module = members[0].get("file", "")
    return {
        "source_module": source_module,
        "member_count": len(members),
        "members": members,
        "sub_namespaces": sub_namespaces,
    }


def run_typedoc_pass(typedoc_path: Path) -> tuple[dict[str, dict], list[dict]]:
    """Return (namespaces, root_exports) from TypeDoc JSON."""
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

    for child in raw.get("children", []):
        ck = child.get("kind", 0)
        if ck == TD_MODULE:
            namespaces[child["name"]] = _td_process_namespace(child)
        elif ck in KIND_MAP:
            file_, line = _td_source(child)
            entry: dict = {
                "name": child["name"],
                "kind": KIND_MAP[ck],
                "file": file_,
                "line": line,
            }
            sig = _td_extract_sig(child)
            if sig and (sig["parameters"] or sig["returns"] not in ("", "void")):
                entry["signature"] = sig
            if ck == TD_ENUM:
                for ec in child.get("children", []):
                    if ec.get("kind") == TD_ENUM_MEMBER:
                        ef, el = _td_source(ec)
                        root_exports.append({
                            "name": f"{child['name']}.{ec['name']}",
                            "kind": "enum_member",
                            "file": ef or file_,
                            "line": el,
                        })
            root_exports.append(entry)

    return namespaces, root_exports


# ---------------------------------------------------------------------------
# Pass 2: Targeted @types regex — Amity global namespace only
# ---------------------------------------------------------------------------

AMITY_NS_DECL_PATTERNS = [
    ("class",     re.compile(r'^\s+(?:abstract\s+)?class\s+(\w+)')),
    ("interface", re.compile(r'^\s+interface\s+(\w+)')),
    ("enum",      re.compile(r'^\s+(?:const\s+)?enum\s+(\w+)')),
    ("type",      re.compile(r'^\s+type\s+(\w+)')),
    ("function",  re.compile(r'^\s+(?:async\s+)?function\s+(\w+)')),
    ("const",     re.compile(r'^\s+(?:declare\s+)?const\s+(\w+)')),
]

CASE_RE = re.compile(r'^\s+([A-Za-z_][A-Za-z0-9_]*)\s*(?:=|,|$)')
TMPL_LIT_RE = re.compile(r'type\s+(\w+)\s*=\s*`\$\{(\w+)\}`')


def _collect_module_enums(lines: list[str]) -> dict[str, tuple[int, list[tuple[str, int]]]]:
    result: dict[str, tuple[int, list[tuple[str, int]]]] = {}
    idx = 0
    while idx < len(lines):
        m = re.match(r'^(?:export\s+)?(?:const\s+)?enum\s+(\w+)\s*\{', lines[idx])
        if m:
            enum_name = m.group(1)
            cases: list[tuple[str, int]] = []
            depth = lines[idx].count("{") - lines[idx].count("}")
            idx += 1
            while idx < len(lines) and depth > 0:
                cl = lines[idx]
                cm = CASE_RE.match(cl)
                if cm and depth == 1:
                    cases.append((cm.group(1), idx + 1))
                depth += cl.count("{") - cl.count("}")
                idx += 1
            result[enum_name] = (idx, cases)
            continue
        idx += 1
    return result


def run_amity_pass() -> tuple[list[dict], int]:
    """Walk @types/domains/*.ts and extract Amity global namespace members.
    Returns (members, enum_cases_total).
    """
    if not ATYPES_DIR.exists():
        print(f"WARNING: @types dir not found at {ATYPES_DIR}", file=sys.stderr)
        return [], 0

    members: list[dict] = []
    seen_names: set[str] = set()
    enum_cases_total = 0

    for f in sorted(ATYPES_DIR.rglob("*.ts")):
        text = f.read_text(encoding="utf-8")
        lines = text.splitlines()
        file_rel = str(f.relative_to(SDKS_ROOT))
        module_enums = _collect_module_enums(lines)

        i = 0
        while i < len(lines):
            stripped = lines[i].strip()
            if not re.match(r'declare\s+global\s*\{', stripped):
                i += 1
                continue

            global_depth = 1
            i += 1
            amity_start = -1
            while i < len(lines) and global_depth > 0:
                l = lines[i]
                stripped_l = l.strip()
                if re.match(r'namespace\s+Amity\s*\{', stripped_l) and global_depth == 1:
                    amity_start = i
                    break
                global_depth += l.count("{") - l.count("}")
                i += 1

            if amity_start == -1:
                continue

            amity_depth = 1
            current_enum: str | None = None
            i = amity_start + 1
            while i < len(lines) and amity_depth > 0:
                l = lines[i]
                stripped_l = l.strip()
                opens = l.count("{")
                closes = l.count("}")

                if amity_depth == 1 and stripped_l:
                    current_enum = None
                    for kind, pat in AMITY_NS_DECL_PATTERNS:
                        mm = pat.match(l)
                        if mm:
                            name = mm.group(1)
                            if name not in seen_names:
                                seen_names.add(name)
                                members.append({
                                    "name": name,
                                    "kind": kind,
                                    "namespace": "Amity",
                                    "file": file_rel,
                                    "line": i + 1,
                                })
                                if kind == "type":
                                    tmpl_m = TMPL_LIT_RE.search(stripped_l)
                                    if tmpl_m and tmpl_m.group(1) == name:
                                        backing_enum = tmpl_m.group(2)
                                        enum_info = module_enums.get(backing_enum)
                                        if enum_info:
                                            for case_name, case_line in enum_info[1]:
                                                dotted = f"{name}.{case_name}"
                                                if dotted not in seen_names:
                                                    seen_names.add(dotted)
                                                    members.append({
                                                        "name": dotted,
                                                        "kind": "enum_case",
                                                        "parent_enum": name,
                                                        "namespace": "Amity",
                                                        "file": file_rel,
                                                        "line": case_line,
                                                    })
                                                    enum_cases_total += 1
                            if kind == "enum" and opens > closes:
                                current_enum = name
                            break

                elif amity_depth == 2 and current_enum is not None:
                    s2 = stripped_l
                    if s2 and not s2.startswith(("//", "/*", "*")):
                        cm = CASE_RE.match(l)
                        if cm:
                            case_name = cm.group(1)
                            dotted = f"{current_enum}.{case_name}"
                            if dotted not in seen_names:
                                seen_names.add(dotted)
                                members.append({
                                    "name": dotted,
                                    "kind": "enum_case",
                                    "parent_enum": current_enum,
                                    "namespace": "Amity",
                                    "file": file_rel,
                                    "line": i + 1,
                                })
                                enum_cases_total += 1

                new_depth = amity_depth + opens - closes
                if new_depth < amity_depth and amity_depth == 2:
                    current_enum = None
                amity_depth = new_depth
                i += 1

    return members, enum_cases_total


# ---------------------------------------------------------------------------
# Merge and emit
# ---------------------------------------------------------------------------

def extract(typedoc_path: Path) -> dict:
    # Pass 1: TypeDoc
    td_namespaces, td_root_exports = run_typedoc_pass(typedoc_path)
    print(f"  Pass 1 (TypeDoc): {len(td_namespaces)} namespaces, {len(td_root_exports)} root_exports")

    # Pass 2: Amity global namespace
    amity_members, amity_enum_cases = run_amity_pass()
    print(f"  Pass 2 (Amity @types): {len(amity_members)} members ({amity_enum_cases} enum cases)")

    # Merge: TypeDoc namespaces + Amity global namespace from Pass 2
    merge_notes: list[str] = []
    namespaces = dict(td_namespaces)  # TypeDoc wins for all 24 namespaces

    if amity_members:
        # Check for any name collision (TypeDoc shouldn't have Amity, but be safe)
        if "Amity" in namespaces:
            merge_notes.append(
                f"Amity namespace found in both passes; TypeDoc wins "
                f"({len(namespaces['Amity'].get('members',[]))} members kept, "
                f"{len(amity_members)} from @types pass discarded)"
            )
        else:
            namespaces["Amity"] = {
                "source_module": str(ATYPES_DIR.relative_to(SDKS_ROOT)),
                "member_count": len(amity_members),
                "members": amity_members,
                "sub_namespaces": {},
            }

    # Stats
    ns_member_total = sum(
        len(v.get("members", [])) + sum(len(sv.get("members", [])) for sv in v.get("sub_namespaces", {}).values())
        for v in namespaces.values()
    )
    sub_ns_total = sum(len(v.get("sub_namespaces", {})) for v in namespaces.values())
    amity_count = len(namespaces.get("Amity", {}).get("members", []))

    stats = {
        "namespaces": len(namespaces),
        "sub_namespaces_total": sub_ns_total,
        "namespaced_members_total": ns_member_total,
        "amity_global_members": amity_count,
        "amity_enum_cases_total": amity_enum_cases,
        "root_exports": len(td_root_exports),
    }

    return {
        "extractor_version": "0.3.0-hybrid",
        "extractor": "typescript-hybrid-extractor.py",
        "extracted_at": datetime.now(timezone.utc).isoformat(),
        "sdk_package": "@amityco/ts-sdk",
        "sources": {
            "typedoc_json_path": str(typedoc_path.resolve()),
            "at_types_glob": str(ATYPES_DIR / "**" / "*.ts"),
            "typedoc_note": "24 namespaced exports; @hidden/@private/@internal honored natively",
            "at_types_note": "Amity global namespace from declare global{} augmentations",
        },
        "merge_notes": merge_notes,
        "namespaces": namespaces,
        "root_exports": td_root_exports,
        "stats": stats,
    }


def main() -> None:
    typedoc_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_TYPEDOC_JSON
    print(f"[typescript-hybrid-extractor] reading TypeDoc JSON from {typedoc_path}")

    result = extract(typedoc_path)

    OUTPUT_PATH.write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    stats = result["stats"]
    print(f"[typescript-hybrid-extractor] wrote {OUTPUT_PATH}")
    print(
        f"[typescript-hybrid-extractor] "
        f"namespaces={stats['namespaces']} "
        f"namespaced_members={stats['namespaced_members_total']} "
        f"amity_global={stats['amity_global_members']} "
        f"root_exports={stats['root_exports']}"
    )
    if result.get("merge_notes"):
        for note in result["merge_notes"]:
            print(f"  [merge] {note}")


if __name__ == "__main__":
    main()
