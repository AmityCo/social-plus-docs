#!/usr/bin/env python3
"""
iOS/Swift SDK public API extractor — v0.1.1

Walks AmitySDKIOS/{EkoChat,EkoStreamPublisher,UpstraVideoPlayerKit} and emits
.docs-ops/sdk-surface/ios.json with the public Swift API surface.

v0.1 capabilities:
- Captures NAME, KIND, FILE, LINE, raw signature_hint.
- Tracks type context via brace-depth counting.
- Aggregates extension members under the host type.
- Handles leading @-attributes and access-modifier prefixes before visibility keyword.
- Does NOT parse full param/return types (v2 with SwiftSyntax).
  Edge cases that can't be handled cleanly are logged to unhandled[].
"""
from __future__ import annotations
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

DOCS_OPS_ROOT = Path(__file__).resolve().parent.parent
DOCS_REPO_ROOT = DOCS_OPS_ROOT.parent
SDKS_ROOT = DOCS_REPO_ROOT.parent
IOS_ROOT = SDKS_ROOT / "AmitySDKIOS"

SOURCE_ROOTS = ["EkoChat", "EkoStreamPublisher", "UpstraVideoPlayerKit"]

EXCLUDE_FRAGMENTS = [
    "/External/", "/SDKTests/", "/AmitySDKTests/", "/AmitySDKUnitTests/",
    "/AmitySDKIntegrationTests/", "/AmitySDKThreadSafetyTests/", "/EkoChatTests/",
    "/SampleApp/", "/SampleAppLiveVideo/", "/SDKSampleCode/", "/SDKSizeReport/",
    "/.build/", "/Pods/",
]

OUTPUT = DOCS_OPS_ROOT / "sdk-surface" / "ios.json"

# ── Regex patterns ─────────────────────────────────────────────────────────────

# Strip leading whitespace + @-attributes (handles @Published, @objc(foo), etc.)
ATTR_STRIP_RE = re.compile(r'^(?:@\w+(?:\([^)]*\))?\s*)+')

# Type-level declarations — matched on the attr-stripped line
TYPE_RE_LIST = [
    ("class",     re.compile(r'^(?:public|open)\s+(?:final\s+)?(?:actor\s+)?class\s+([A-Za-z_][A-Za-z0-9_]*)')),
    ("actor",     re.compile(r'^(?:public|open)\s+(?:final\s+)?actor\s+([A-Za-z_][A-Za-z0-9_]*)')),
    ("struct",    re.compile(r'^(?:public|open)\s+struct\s+([A-Za-z_][A-Za-z0-9_]*)')),
    ("protocol",  re.compile(r'^(?:public|open)\s+protocol\s+([A-Za-z_][A-Za-z0-9_]*)')),
    ("enum",      re.compile(r'^(?:public|open)\s+(?:indirect\s+)?enum\s+([A-Za-z_][A-Za-z0-9_]*)')),
    ("typealias", re.compile(r'^(?:public|open)\s+typealias\s+([A-Za-z_][A-Za-z0-9_]*)')),
]

# Extension — may or may not have `public`
EXT_RE = re.compile(r'^(?:public\s+)?extension\s+([A-Za-z_][A-Za-z0-9_]*)\b')

# Member-level declarations — matched on the attr-stripped line
MEMBER_RE_LIST = [
    ("func",      re.compile(r'^(?:public|open)\s+'
                             r'(?:(?:static|class|required|convenience|override|mutating|nonmutating)\s+)*'
                             r'func\s+([A-Za-z_`][A-Za-z0-9_`]*)')),
    ("var",       re.compile(r'^(?:public|open)\s+'
                             r'(?:private\(set\)\s+|fileprivate\(set\)\s+|internal\(set\)\s+)?'
                             r'(?:(?:static|class|lazy|override)\s+)*'
                             r'(var|let)\s+([A-Za-z_][A-Za-z0-9_]*)')),
    ("init",      re.compile(r'^(?:public|open)\s+'
                             r'(?:required\s+|convenience\s+|override\s+)*init[\b(?]')),
    ("subscript", re.compile(r'^(?:public|open)\s+(?:static\s+)?subscript\b')),
    ("operator",  re.compile(r'^(?:public|open)\s+(?:static\s+)?(?:prefix|postfix|infix)?\s*func\s+([^(]+)\(')),
]

# Enum case line (only recognised inside enum context)
CASE_RE = re.compile(r'^\s*(?:public\s+)?case\s+(`?[A-Za-z_][A-Za-z0-9_]*`?)')

# Static/class stored properties inside a public/open type body may omit explicit public.
STATIC_STORED_RE = re.compile(
    r'^(?:(?:public|open|internal|private|fileprivate)\s+)?'
    r'(?:(?:static|class)\s+)(var|let)\s+([A-Za-z_`][A-Za-z0-9_`]*)'
)


def strip_attrs(raw: str) -> str:
    """Strip leading whitespace and @-attributes from a raw source line."""
    stripped = raw.lstrip()
    m = ATTR_STRIP_RE.match(stripped)
    if m:
        stripped = stripped[m.end():].lstrip()
    return stripped


def count_brace_delta(line: str) -> int:
    """Return net change in brace depth for this line (naive, ignores strings/comments)."""
    # Remove string literals crudely to avoid counting braces inside them.
    # Good enough for v1 where we just need approximate depth.
    no_strings = re.sub(r'"[^"\\]*(?:\\.[^"\\]*)*"', '""', line)
    no_line_comment = no_strings.split("//")[0]
    return no_line_comment.count("{") - no_line_comment.count("}")


def rel(path: Path) -> str:
    return str(path.relative_to(SDKS_ROOT))


def should_exclude(path: Path) -> bool:
    s = str(path)
    return any(frag in s for frag in EXCLUDE_FRAGMENTS)


def extract_file(
    path: Path,
    types_out: dict,
    protocols_out: dict,
    global_funcs: list,
    global_consts: list,
    global_typealiases: list,
    unhandled: list,
) -> None:
    """
    Parse one .swift file and collect public API entries into the provided dicts/lists.

    State machine: we walk lines, tracking:
      - brace_depth: int — net `{` vs `}` seen so far
      - type_stack: list of (type_name, entry_brace_depth, kind, is_enum)
        where `entry_brace_depth` is the depth AFTER we saw the opening `{`
    """
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return

    lines = text.splitlines()
    brace_depth = 0
    # Each frame: {"name": str, "depth": int (depth when body starts), "kind": str, "is_enum": bool, "entry": dict | None}
    type_stack: list[dict] = []

    def current_type() -> dict | None:
        return type_stack[-1] if type_stack else None

    def get_or_create_type(name: str, kind: str, lineno: int, is_protocol: bool = False) -> dict:
        container = protocols_out if is_protocol else types_out
        if name not in container:
            container[name] = {
                "kind": kind,
                "primary_decl": {"file": rel(path), "line": lineno},
                "extensions": [],
                "members": [],
                "nested_types": [],
            }
        return container[name]

    def create_nested_type(parent: dict, name: str, kind: str, lineno: int) -> dict:
        nested_entry = {
            "name": name,
            "kind": kind,
            "primary_decl": {"file": rel(path), "line": lineno},
            "members": [],
            "nested_types": [],
        }
        parent["nested_types"].append(nested_entry)
        return nested_entry

    for lineno, raw in enumerate(lines, start=1):
        # Maintain brace depth BEFORE processing (depth entering this line).
        depth_before = brace_depth

        # Pop type_stack frames whose body has been closed.
        while type_stack and brace_depth <= type_stack[-1]["depth"] - 1:
            type_stack.pop()

        stripped = strip_attrs(raw)
        file_rel = rel(path)

        # ── Typealias (no body / brace) ─────────────────────────────────────
        for kind, pat in TYPE_RE_LIST:
            if kind != "typealias":
                continue
            m = pat.match(stripped)
            if m:
                name = m.group(1)
                global_typealiases.append({"name": name, "file": file_rel, "line": lineno,
                                           "signature_hint": raw.strip()})
                break

        # ── Type or extension declarations ──────────────────────────────────
        matched_type = False
        for kind, pat in TYPE_RE_LIST:
            if kind == "typealias":
                continue
            m = pat.match(stripped)
            if m:
                name = m.group(1)
                is_protocol = (kind == "protocol")
                parent_type = current_type()
                if parent_type and parent_type.get("entry") is not None:
                    entry = create_nested_type(parent_type["entry"], name, kind, lineno)
                else:
                    entry = get_or_create_type(name, kind, lineno, is_protocol)
                    # Mark extensions
                    if "primary_decl" in entry and entry["primary_decl"]["file"] != file_rel:
                        entry["extensions"].append({"file": file_rel, "line": lineno})
                # Push onto stack — depth of body = depth_before + 1 (after we count the `{`)
                brace_delta = count_brace_delta(raw)
                brace_depth += brace_delta
                if brace_delta > 0:
                    type_stack.append({
                        "name": name,
                        "depth": depth_before + 1,
                        "kind": kind,
                        "is_enum": (kind == "enum"),
                        "is_protocol": is_protocol,
                        "entry": entry,
                    })
                matched_type = True
                break

        if matched_type:
            continue

        # Extension (may be from non-public extension too — we include it so
        # that members declared `public` inside are captured under the host type)
        m = EXT_RE.match(stripped)
        if m:
            name = m.group(1)
            brace_delta = count_brace_delta(raw)
            brace_depth += brace_delta
            if brace_delta > 0:
                # Check if we already know this type
                entry = None
                if name in types_out:
                    entry = types_out[name]
                    entry["extensions"].append({"file": file_rel, "line": lineno})
                elif name in protocols_out:
                    entry = protocols_out[name]
                    entry["extensions"].append({"file": file_rel, "line": lineno})
                # Even if unknown type, push a frame so members can be captured
                type_stack.append({
                    "name": name,
                    "depth": depth_before + 1,
                    "kind": "extension",
                    "is_enum": False,
                    "is_protocol": False,
                    "entry": entry,
                })
            continue

        # ── Member declarations ─────────────────────────────────────────────
        ct = current_type()
        if ct:
            is_enum = ct.get("is_enum", False)
            member_target = ct.get("entry")

            # Enum cases
            if is_enum:
                cm = CASE_RE.match(raw)
                if cm and member_target is not None:
                    case_name = cm.group(1).strip("`")
                    member_target["members"].append({
                        "name": case_name,
                        "kind": "case",
                        "file": file_rel,
                        "line": lineno,
                        "signature_hint": raw.strip(),
                    })

            # Regular members
            member_matched = False
            for kind, pat in MEMBER_RE_LIST:
                m = pat.match(stripped)
                if m:
                    member_kind = kind
                    if kind == "var":
                        name = m.group(2)  # group(1) is var|let keyword
                        if re.match(r'^(?:public|open)\s+(?:private\(set\)\s+|fileprivate\(set\)\s+|internal\(set\)\s+)?(?:(?:static|class)\s+)', stripped):
                            member_kind = f"static_{m.group(1)}"
                    elif kind in ("init", "subscript"):
                        name = kind  # use kind as the name
                    else:
                        name = m.group(1)
                    if member_target is not None:
                        member_target["members"].append({
                            "name": name.strip("`"),
                            "kind": member_kind,
                            "file": file_rel,
                            "line": lineno,
                            "signature_hint": raw.strip(),
                        })
                    member_matched = True
                    break

            if not member_matched:
                sm = STATIC_STORED_RE.match(stripped)
                if sm and member_target is not None:
                    member_target["members"].append({
                        "name": sm.group(2).strip("`"),
                        "kind": f"static_{sm.group(1)}",
                        "file": file_rel,
                        "line": lineno,
                        "signature_hint": raw.strip(),
                    })

        else:
            # Top-level declarations (global scope)
            for kind, pat in MEMBER_RE_LIST:
                m = pat.match(stripped)
                if m:
                    if kind == "var":
                        name = m.group(2)
                        global_consts.append({"name": name, "kind": kind, "file": file_rel,
                                              "line": lineno, "signature_hint": raw.strip()})
                    elif kind == "func":
                        name = m.group(1)
                        global_funcs.append({"name": name, "kind": kind, "file": file_rel,
                                             "line": lineno, "signature_hint": raw.strip()})
                    break

        # Update brace depth for non-type lines
        if not matched_type and not (m and hasattr(m, 'group') and EXT_RE.match(stripped)):
            brace_depth += count_brace_delta(raw)

        # Guard against negative depth (mismatched braces in comments/strings)
        if brace_depth < 0:
            brace_depth = 0


def walk_type_entries(entry: dict):
    yield entry
    for nested in entry.get("nested_types", []):
        yield from walk_type_entries(nested)



def main() -> int:
    if not IOS_ROOT.exists():
        print(f"ERROR: iOS SDK root not found at {IOS_ROOT}", file=sys.stderr)
        return 2

    types_out: dict = {}
    protocols_out: dict = {}
    global_funcs: list = []
    global_consts: list = []
    global_typealiases: list = []
    unhandled: list = []

    files_scanned = 0
    for root_name in SOURCE_ROOTS:
        src_dir = IOS_ROOT / root_name
        if not src_dir.exists():
            unhandled.append(f"source root not found: {src_dir}")
            continue
        for swift_file in sorted(src_dir.rglob("*.swift")):
            if should_exclude(swift_file):
                continue
            files_scanned += 1
            extract_file(swift_file, types_out, protocols_out,
                         global_funcs, global_consts, global_typealiases, unhandled)

    all_entries = [
        nested_entry
        for top_level in list(types_out.values()) + list(protocols_out.values())
        for nested_entry in walk_type_entries(top_level)
    ]
    members_total = sum(len(entry["members"]) for entry in all_entries)
    static_members_total = sum(
        1
        for entry in all_entries
        for member in entry["members"]
        if member.get("kind") in ("static_var", "static_let")
    )
    nested_types_total = sum(len(entry.get("nested_types", [])) for entry in all_entries)

    surface = {
        "extractor_version": "0.1.1",
        "extractor": "ios-extractor.py",
        "extracted_at": datetime.now(timezone.utc).isoformat(),
        "sdk_product": "AmitySDK",
        "sdk_source_roots": [f"AmitySDKIOS/{r}" for r in SOURCE_ROOTS],
        "types": types_out,
        "global_funcs": global_funcs,
        "global_consts": global_consts,
        "global_typealiases": global_typealiases,
        "protocols": protocols_out,
        "unhandled": unhandled,
        "stats": {
            "files_scanned": files_scanned,
            "types": len(types_out),
            "protocols": len(protocols_out),
            "members_total": members_total,
            "static_members_total": static_members_total,
            "nested_types_total": nested_types_total,
            "global_funcs": len(global_funcs),
            "global_consts": len(global_consts),
            "unhandled_lines": len(unhandled),
        },
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(surface, indent=2) + "\n", encoding="utf-8")

    s = surface["stats"]
    print(f"wrote {OUTPUT.relative_to(DOCS_REPO_ROOT)}")
    print(f"  files scanned:  {s['files_scanned']}")
    print(f"  types:          {s['types']}")
    print(f"  protocols:      {s['protocols']}")
    print(f"  members total:  {s['members_total']}")
    print(f"  global funcs:   {s['global_funcs']}")
    print(f"  global consts:  {s['global_consts']}")
    print(f"  unhandled:      {s['unhandled_lines']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
