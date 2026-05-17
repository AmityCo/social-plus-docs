#!/usr/bin/env python3
"""
TypeScript SDK surface extractor — v1 (regex-based).

Walks the @amityco/ts-sdk barrel and emits .docs-ops/sdk-surface/typescript.json
with the public API surface: namespaces, classes, functions, interfaces, types,
enums, consts.

v1.1 capabilities:
- Captures NAME, KIND, NAMESPACE, FILE, LINE.
- Follows nested `export * as Sub from '...'` re-exports as sub_namespaces.
- Does NOT capture full signatures, parameter types, or return types.
- Default exports not captured (the SDK barrel uses named/namespace re-exports only).

v1.2 additions:
- Adds second pass: walks all .ts files under packages/sdk/src/@types/ and
  captures declarations inside `declare global { namespace Amity { ... } }` blocks.
- Aggregates all Amity-namespace declarations across files into a synthetic top-level
  `Amity` namespace entry in the surface JSON.
- Adds `amity_global_members` stat.

Why regex instead of ts-morph: zero install, no dependency on the SDK building.
ts-morph upgrade is tracked as a follow-up task (see .docs-ops/README.md).
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

# Resolve from this script's location: .docs-ops/extractors/ -> repo root is two up
DOCS_OPS_ROOT = Path(__file__).resolve().parent.parent
DOCS_REPO_ROOT = DOCS_OPS_ROOT.parent
SDKS_ROOT = DOCS_REPO_ROOT.parent
SDK_ROOT = SDKS_ROOT / "AmityTypescriptSDK" / "packages" / "sdk"
SRC = SDK_ROOT / "src"
OUTPUT = DOCS_OPS_ROOT / "sdk-surface" / "typescript.json"

# Patterns for the barrel re-export forms we expect to see.
RE_NAMESPACE_EXPORT = re.compile(r'^export\s+\*\s+as\s+(\w+)\s+from\s+[\'"]([^\'"]+)[\'"]')
RE_WILDCARD_EXPORT = re.compile(r'^export\s+\*\s+from\s+[\'"]([^\'"]+)[\'"]')
RE_NAMED_EXPORT_FROM = re.compile(r'^export\s+\{([^}]+)\}\s+from\s+[\'"]([^\'"]+)[\'"]')

# Patterns for declarations inside leaf modules.
DECL_PATTERNS = [
    ("class",     re.compile(r'^export\s+(?:abstract\s+)?class\s+(\w+)')),
    ("interface", re.compile(r'^export\s+interface\s+(\w+)')),
    ("enum",      re.compile(r'^export\s+(?:const\s+)?enum\s+(\w+)')),
    ("type",      re.compile(r'^export\s+type\s+(\w+)')),
    ("function",  re.compile(r'^export\s+(?:async\s+)?function\s+(\w+)')),
    ("const",     re.compile(r'^export\s+(?:declare\s+)?const\s+(\w+)')),
    ("let",       re.compile(r'^export\s+let\s+(\w+)')),
    ("namespace", re.compile(r'^export\s+namespace\s+(\w+)')),
]

# Cap on barrel-following depth to avoid infinite loops on circular re-exports.
MAX_DEPTH = 4

# Patterns for declarations inside a `namespace Amity { ... }` block.
# Inside the block, declarations are NOT prefixed with `export`.
AMITY_NS_DECL_PATTERNS = [
    ("class",     re.compile(r'^\s+(?:abstract\s+)?class\s+(\w+)')),
    ("interface", re.compile(r'^\s+interface\s+(\w+)')),
    ("enum",      re.compile(r'^\s+(?:const\s+)?enum\s+(\w+)')),
    ("type",      re.compile(r'^\s+type\s+(\w+)')),
    ("function",  re.compile(r'^\s+(?:async\s+)?function\s+(\w+)')),
    ("const",     re.compile(r'^\s+(?:declare\s+)?const\s+(\w+)')),
]

ATYPES_DIR = SRC / "@types"

unhandled: list[str] = []


def resolve_module(from_file: Path, spec: str) -> Path | None:
    """Resolve a relative ES module spec to a .ts file or barrel index."""
    base = (from_file.parent / spec).resolve()
    candidates = [
        base.with_suffix(".ts"),
        base.with_suffix(".tsx"),
        base / "index.ts",
        base / "index.tsx",
    ]
    for c in candidates:
        if c.exists():
            return c
    return None


def extract_local_declarations(file: Path) -> list[dict]:
    """Find top-level `export class/interface/function/...` declarations in a single file."""
    items: list[dict] = []
    try:
        text = file.read_text(encoding="utf-8")
    except (UnicodeDecodeError, FileNotFoundError):
        return items
    for lineno, line in enumerate(text.splitlines(), start=1):
        for kind, pat in DECL_PATTERNS:
            m = pat.match(line.strip())
            if m:
                items.append({
                    "name": m.group(1),
                    "kind": kind,
                    "file": str(file.relative_to(SDKS_ROOT)),
                    "line": lineno,
                })
                break
    return items


def walk_module(file: Path, depth: int = 0, visited: set[str] | None = None) -> tuple[list[dict], dict[str, dict]]:
    """Recursively collect (members, sub_namespaces) reachable from `file`.

    Returns:
      - members: flat list of class/interface/function/etc. declarations
      - sub_namespaces: {name -> {source_module, members, sub_namespaces}} for nested
        `export * as Sub from '...'` re-exports.
    """
    if visited is None:
        visited = set()
    key = str(file)
    if key in visited or depth > MAX_DEPTH:
        return [], {}
    visited.add(key)

    collected: list[dict] = []
    sub_ns: dict[str, dict] = {}
    collected.extend(extract_local_declarations(file))

    try:
        lines = file.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, FileNotFoundError):
        return collected, sub_ns

    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("export"):
            continue
        if m := RE_NAMESPACE_EXPORT.match(stripped):
            # Nested namespace: `export * as Sub from './path'`
            sub_name, spec = m.group(1), m.group(2)
            target = resolve_module(file, spec)
            if target:
                sub_members, sub_subs = walk_module(target, depth + 1, set(visited))
                sub_ns[sub_name] = {
                    "source_module": str(target.relative_to(SDKS_ROOT)),
                    "member_count": len(sub_members),
                    "members": sub_members,
                    "sub_namespaces": sub_subs,
                }
            else:
                unhandled.append(f"unresolved nested namespace target: {stripped} (from {file})")
            continue
        if m := RE_WILDCARD_EXPORT.match(stripped):
            target = resolve_module(file, m.group(1))
            if target:
                child_members, child_subs = walk_module(target, depth + 1, visited)
                collected.extend(child_members)
                # Merge any sub-namespaces the child exposed (rare but possible).
                for k, v in child_subs.items():
                    sub_ns.setdefault(k, v)
            else:
                unhandled.append(f"unresolved wildcard re-export: {stripped} (from {file})")
            continue
        if m := RE_NAMED_EXPORT_FROM.match(stripped):
            names = [n.strip().split(" as ")[-1].strip() for n in m.group(1).split(",") if n.strip()]
            target = resolve_module(file, m.group(2))
            if target:
                target_members, _ = walk_module(target, depth + 1, visited)
                target_decls = {d["name"]: d for d in target_members}
                for n in names:
                    if n in target_decls:
                        collected.append(target_decls[n])
                    else:
                        unhandled.append(f"named export not found: {n} from {target}")
            continue
    return collected, sub_ns


def extract_amity_namespace() -> tuple[list[dict], list[str]]:
    """Walk all .ts files under @types/ and collect declarations in namespace Amity blocks.

    Returns (members, source_files) where members are deduplicated by name, keeping the
    first occurrence (files are processed in sorted order for determinism).

    v1.3: also captures enum cases as dotted members (e.g. SessionStates.ESTABLISHED).
    Also handles template-literal type aliases like ``type Foo = `${FooEnum}` `` by
    resolving the referenced enum's cases and adding synthetic Foo.CaseName members.
    """
    members: list[dict] = []
    seen_names: set[str] = set()
    source_files: list[str] = []
    duplicates: list[str] = []
    enum_cases_total = 0

    # Matches an enum case: optional whitespace, identifier, then = or , or end-of-body.
    CASE_RE = re.compile(r'^\s+([A-Za-z_][A-Za-z0-9_]*)\s*(?:=|,|$)')
    # Matches a template-literal type alias: type Foo = `${FooEnum}`
    TMPL_LIT_RE = re.compile(r'type\s+(\w+)\s*=\s*`\$\{(\w+)\}`')

    def collect_module_enums(lines: list[str]) -> dict[str, tuple[int, list[tuple[str, int]]]]:
        """Return {enum_name: (start_line, [(case_name, line_no), ...])} for top-level enums."""
        result: dict[str, tuple[int, list[tuple[str, int]]]] = {}
        idx = 0
        while idx < len(lines):
            l = lines[idx]
            m = re.match(r'^(?:export\s+)?(?:const\s+)?enum\s+(\w+)\s*\{', l)
            if m:
                enum_name = m.group(1)
                cases: list[tuple[str, int]] = []
                depth = l.count("{") - l.count("}")
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

    ts_files = sorted(ATYPES_DIR.rglob("*.ts"))
    for f in ts_files:
        text = f.read_text(encoding="utf-8")
        lines = text.splitlines()
        file_rel = str(f.relative_to(SDKS_ROOT))

        # Pre-pass: collect module-level enum definitions for template-literal resolution.
        module_enums = collect_module_enums(lines)

        # Locate `declare global {` then `namespace Amity {` using brace-depth tracking.
        i = 0
        while i < len(lines):
            stripped = lines[i].strip()

            # Find `declare global {`
            if not re.match(r'declare\s+global\s*\{', stripped):
                i += 1
                continue

            # Now scan forward for `namespace Amity {`
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

            # Found `namespace Amity {`. Track declarations at depth == amity_depth+1.
            amity_depth = 1  # we're inside namespace Amity { at depth 1
            file_contributed = False
            current_enum: str | None = None  # set when inside an enum body at depth 2
            i = amity_start + 1
            while i < len(lines) and amity_depth > 0:
                l = lines[i]
                stripped_l = l.strip()
                opens = l.count("{")
                closes = l.count("}")

                if amity_depth == 1 and stripped_l:
                    # At depth 1, check for a top-level declaration.
                    current_enum = None  # leaving any previous enum body
                    for kind, pat in AMITY_NS_DECL_PATTERNS:
                        mm = pat.match(l)
                        if mm:
                            name = mm.group(1)
                            if name in seen_names:
                                duplicates.append(f"{name} (also in {file_rel})")
                            else:
                                seen_names.add(name)
                                members.append({
                                    "name": name,
                                    "kind": kind,
                                    "namespace": "Amity",
                                    "file": file_rel,
                                    "line": i + 1,
                                })
                                file_contributed = True
                                # For template-literal type aliases like `type Foo = \`${FooEnum}\``,
                                # add synthetic dotted members from the backing enum's cases.
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
                            # If this is an enum declaration that opens its body on this line,
                            # track the enum name so we can capture cases at depth 2.
                            if kind == "enum" and opens > closes:
                                current_enum = name
                            break

                elif amity_depth == 2 and current_enum is not None:
                    # Inside an enum body — capture case names.
                    s2 = stripped_l
                    if not s2 or s2.startswith("//") or s2.startswith("/*") or s2.startswith("*"):
                        pass  # skip comments and blank lines
                    else:
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

                # Track depth change; if leaving an enum body, clear current_enum.
                new_depth = amity_depth + opens - closes
                if new_depth < amity_depth and amity_depth == 2:
                    current_enum = None
                amity_depth = new_depth
                i += 1

            if file_contributed:
                source_files.append(file_rel)

    if duplicates:
        unhandled.extend([f"Amity namespace duplicate: {d}" for d in duplicates])

    # Store enum_cases_total in a module-level var for stats reporting.
    extract_amity_namespace._enum_cases_total = enum_cases_total  # type: ignore[attr-defined]
    return members, source_files


def main() -> int:
    barrel = SRC / "index.ts"
    if not barrel.exists():
        print(f"ERROR: barrel not found at {barrel}", file=sys.stderr)
        return 2

    surface: dict = {
        "extractor_version": "0.1.3",
        "extractor": "typescript-extractor.py",
        "extracted_at": "2026-05-17T00:00:00Z",
        "sdk_package": "@amityco/ts-sdk",
        "sdk_source_root": str(SDK_ROOT.relative_to(SDKS_ROOT)),
        "barrel": str(barrel.relative_to(SDKS_ROOT)),
        "namespaces": {},
        "root_exports": [],
        "unhandled": [],
        "stats": {},
    }

    barrel_lines = barrel.read_text(encoding="utf-8").splitlines()
    for line in barrel_lines:
        stripped = line.strip()
        if not stripped.startswith("export"):
            continue

        if m := RE_NAMESPACE_EXPORT.match(stripped):
            ns_name, spec = m.group(1), m.group(2)
            target = resolve_module(barrel, spec)
            if not target:
                unhandled.append(f"unresolved namespace target: {stripped}")
                continue
            members, subs = walk_module(target)
            surface["namespaces"][ns_name] = {
                "source_module": str(target.relative_to(SDKS_ROOT)),
                "member_count": len(members),
                "members": members,
                "sub_namespaces": subs,
            }
            continue

        if m := RE_WILDCARD_EXPORT.match(stripped):
            target = resolve_module(barrel, m.group(1))
            if target:
                members, _ = walk_module(target)
                surface["root_exports"].extend(members)
            else:
                unhandled.append(f"unresolved wildcard at barrel: {stripped}")
            continue

        if m := RE_NAMED_EXPORT_FROM.match(stripped):
            names = [n.strip().split(" as ")[-1].strip() for n in m.group(1).split(",") if n.strip()]
            target = resolve_module(barrel, m.group(2))
            if target:
                members, _ = walk_module(target)
                decls = {d["name"]: d for d in members}
                for n in names:
                    if n in decls:
                        surface["root_exports"].append(decls[n])
                    else:
                        unhandled.append(f"named export not found at barrel: {n} from {target}")
            continue

    # Dedupe root_exports by (name, kind, file, line).
    seen = set()
    deduped = []
    for e in surface["root_exports"]:
        key = (e["name"], e["kind"], e["file"], e["line"])
        if key not in seen:
            seen.add(key)
            deduped.append(e)
    surface["root_exports"] = deduped

    # v1.2: second pass — @types/ Amity global namespace declarations.
    amity_members, amity_sources = extract_amity_namespace()
    if amity_members:
        surface["namespaces"]["Amity"] = {
            "source_module": str(ATYPES_DIR.relative_to(SDKS_ROOT)),
            "source_files": amity_sources,
            "member_count": len(amity_members),
            "members": amity_members,
            "sub_namespaces": {},
            "notes": (
                "Synthesised from declare global { namespace Amity { ... } } blocks "
                "across all @types/ files. v1.2 flattens nested namespaces if present."
            ),
        }

    def count_recursive(ns_dict: dict) -> tuple[int, int]:
        """Return (member_total, sub_namespace_total) across nested namespaces."""
        members = 0
        subs = 0
        for ns in ns_dict.values():
            members += ns["member_count"]
            subs += len(ns.get("sub_namespaces", {}))
            sub_m, sub_s = count_recursive(ns.get("sub_namespaces", {}))
            members += sub_m
            subs += sub_s
        return members, subs

    nested_members, nested_subs = count_recursive(surface["namespaces"])
    surface["unhandled"] = unhandled
    surface["stats"] = {
        "namespaces": len(surface["namespaces"]),
        "sub_namespaces_total": nested_subs,
        "namespaced_members_total": nested_members,
        "amity_global_members": len(amity_members),
        "amity_enum_cases_total": getattr(extract_amity_namespace, '_enum_cases_total', 0),
        "root_exports": len(surface["root_exports"]),
        "unhandled_lines": len(unhandled),
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(surface, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(DOCS_REPO_ROOT)}")
    print(f"  namespaces: {surface['stats']['namespaces']}")
    print(f"  namespaced members: {surface['stats']['namespaced_members_total']}")
    print(f"  amity global members: {surface['stats']['amity_global_members']}")
    print(f"  amity enum cases: {surface['stats']['amity_enum_cases_total']}")
    print(f"  root exports: {surface['stats']['root_exports']}")
    print(f"  unhandled lines: {surface['stats']['unhandled_lines']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
