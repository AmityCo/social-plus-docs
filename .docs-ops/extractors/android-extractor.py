#!/usr/bin/env python3
# DEPRECATED — superseded by android-dokka-extractor.py (Dokka GFM-based, task 0079).
# Retained as a fallback reference. Do not use as primary source.
# Primary surface source is now .docs-ops/sdk-surface/android.json produced by android-dokka-extractor.py.
"""
Android SDK surface extractor (v0.1.0)
Regex-based Kotlin/Java public-API extractor.
Mirrors the structure and conventions of ios-extractor.py.

Usage:
    python3 .docs-ops/extractors/android-extractor.py
Writes:
    .docs-ops/sdk-surface/android.json
"""

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent.parent.parent  # extractors/ → .docs-ops/ → social-plus-docs/ → sp-sdks/
SDK_ROOT = REPO_ROOT / "Amity-Social-Cloud-SDK-Android"
OUTPUT = SCRIPT_DIR.parent / "sdk-surface" / "android.json"

EXTRACTOR_VERSION = "0.1.2"

INTERNAL_EXCLUDE_PATTERNS = {
    "/internal/",
    "/impl/",
    "/dao/",
    "/data/local/",
    "/data/remote/",
    "/di/",
    "/util/internal/",
}

EXCLUDE_PATTERNS = {
    "/src/test/",
    "/src/androidTest/",
    "/build/",
    "/.gradle/",
    "/sample/",
    "/samples/",
    "/example/",
    "/external/",
    "/.cxx/",
    "/generated/",
    "/amity-sample-app/",
    "/amity-sample-code/",
    "/amity-test-kit/",
    *INTERNAL_EXCLUDE_PATTERNS,
}

# ---------------------------------------------------------------------------
# Regex patterns
# ---------------------------------------------------------------------------

# Kotlin visibility keywords (if present before the declaration keyword, it's non-public)
KT_NON_PUBLIC = re.compile(r'\b(private|protected|internal)\b')

# Strip Kotlin annotations like @JvmStatic, @Deprecated, @Suppress(...), etc.
KT_ANNOTATION = re.compile(r'@\w+(?:\([^)]*\))?\s*')

# Kotlin type declarations
KT_TYPE_RE = re.compile(
    r'^(?P<vis>(?:(?:private|protected|internal|public|open|abstract|sealed|data|inline|value|annotation)\s+)*)'
    r'(?P<kind>class|object|interface|enum\s+class|annotation\s+class|sealed\s+class|data\s+class|open\s+class|abstract\s+class|inline\s+class|value\s+class)'
    r'\s+(?P<name>\w+)',
    re.MULTILINE
)

# Kotlin member patterns (func, val, var, companion object, enum entry)
KT_FUN_RE = re.compile(
    r'^(?P<vis>(?:(?:private|protected|internal|public|override|open|abstract|suspend|inline|operator|infix|tailrec|external|actual|expect|final)\s+)*)'
    r'(?:fun\s+)(?P<name>\w+)\s*[\(<]',
    re.MULTILINE
)
KT_PROP_RE = re.compile(
    r'^(?P<vis>(?:(?:private|protected|internal|public|override|open|abstract|final|actual|expect)\s+)*)'
    r'(?:(?:private|protected|internal)\s+set\s+)?'
    r'(?P<kind>val|var)\s+(?P<name>\w+)',
    re.MULTILINE
)
KT_COMPANION_RE = re.compile(r'^\s*companion\s+object\b')
KT_ENUM_ENTRY_RE = re.compile(r'^\s{4,}([A-Z][A-Z0-9_]*)(?:\(|,|$|\s*//)')

# Java type declarations
JAVA_TYPE_RE = re.compile(
    r'^\s*public\s+(?:(?:abstract|final|static|strictfp)\s+)*'
    r'(?P<kind>class|interface|enum|@interface)\s+(?P<name>\w+)',
    re.MULTILINE
)
# Java member
JAVA_MEMBER_RE = re.compile(
    r'^\s+public\s+(?:(?:static|final|abstract|synchronized|native|default|strictfp)\s+)*'
    r'(?:(?:<[^>]+>\s+)?[\w\[\]<>,.?]+\s+)'  # return type (may include generics)
    r'(?P<name>\w+)\s*[\(<;]',
    re.MULTILINE
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def should_exclude(path_str: str) -> bool:
    for pat in EXCLUDE_PATTERNS:
        if pat in path_str:
            return True
    return False


def strip_kt_annotations(line: str) -> str:
    return KT_ANNOTATION.sub('', line).strip()


def kt_is_public(vis_group: str) -> bool:
    """Return True if the captured visibility prefix contains no non-public modifier."""
    return not KT_NON_PUBLIC.search(vis_group or '')


def normalise_kind(kind_str: str) -> str:
    """Normalise multi-word Kotlin kinds like 'enum class' → 'enum_class'."""
    return kind_str.strip().replace(' ', '_')


# ---------------------------------------------------------------------------
# Per-file processing
# ---------------------------------------------------------------------------

def process_kotlin_file(filepath: str, content: str, types: dict, interfaces: dict,
                         global_funcs: list, global_consts: list, typealiases: list,
                         unhandled: list):
    lines = content.splitlines()
    line_map = {}  # char_offset → line_number
    offset = 0
    for i, ln in enumerate(lines, 1):
        line_map[offset] = i
        offset += len(ln) + 1

    def char_to_line(char_pos: int) -> int:
        best = 1
        for o, ln in line_map.items():
            if o <= char_pos:
                best = ln
            else:
                break
        return best

    # ---- Detect top-level types ----
    for m in KT_TYPE_RE.finditer(content):
        vis = m.group('vis') or ''
        raw_line = strip_kt_annotations(m.group(0))
        if KT_NON_PUBLIC.search(vis):
            continue
        kind = normalise_kind(m.group('kind'))
        name = m.group('name')
        lineno = char_to_line(m.start())

        entry = {
            'kind': kind,
            'language': 'kotlin',
            'primary_decl': {'file': filepath, 'line': lineno},
            'members': [],
            'nested_types': [],
        }

        if kind == 'interface':
            interfaces.setdefault(name, entry)
        else:
            types.setdefault(name, entry)

    # ---- Detect top-level functions (file-level, not inside a class) ----
    # Only consider declarations at column 0 — indented members are not top-level
    for i, line in enumerate(lines, 1):
        if not line or line[0] in (' ', '\t'):
            continue
        stripped = strip_kt_annotations(line)
        if stripped.startswith('fun ') or re.match(r'^(?:suspend\s+|inline\s+|operator\s+|infix\s+)*fun\s+', stripped):
            m = re.match(r'^(?:(?:suspend|inline|operator|infix|tailrec)\s+)*fun\s+(\w+)', stripped)
            if m:
                global_funcs.append({
                    'name': m.group(1),
                    'file': filepath,
                    'line': i,
                    'signature_hint': stripped[:120],
                })
        elif stripped.startswith('typealias '):
            m = re.match(r'^typealias\s+(\w+)', stripped)
            if m:
                typealiases.append({
                    'name': m.group(1),
                    'file': filepath,
                    'line': i,
                    'signature_hint': stripped[:120],
                })

    # ---- Detect members inside classes/objects ----
    # Walk line by line, track nested type scopes using brace depth.
    # pending_type: (name, entry) for a type whose opening { hasn't been seen yet.
    # We defer the type_stack push until we find the { that opens the class body.
    # This correctly handles multi-line declarations (class Foo(\n  params\n) : Base() {).
    type_stack = []
    brace_depth = 0
    pending_type = None  # (name, entry) waiting for the opening '{'

    for i, line in enumerate(lines, 1):
        stripped = strip_kt_annotations(line)
        brace_depth += line.count('{') - line.count('}')

        # Pop closed scopes ALWAYS — even when a pending type is active.
        # This ensures that a '}' that closes a parent scope is processed before
        # the pending-type logic runs, preventing sibling types from being wrongly
        # nested inside the pending (leaf) type.
        while type_stack and brace_depth < type_stack[-1]['depth']:
            type_stack.pop()

        # ---- Handle pending type (awaiting its opening '{') ----
        if pending_type is not None:
            pname, pentry = pending_type
            # Check for a new type declaration on this line FIRST.  If another
            # public type starts here, the previous pending was a leaf (no body) —
            # just leave it in nested_types and don't push it.
            tm_check = KT_TYPE_RE.match(stripped)
            has_new_type = (
                tm_check is not None
                and not KT_NON_PUBLIC.search(tm_check.group('vis') or '')
            )
            if has_new_type:
                # Previous pending was a leaf. Clear it and fall through to
                # process this new declaration.
                pending_type = None
            elif '{' in line:
                # No new type declaration on this line: the '{' opens the body
                # of the pending type.
                type_stack.append({'name': pname, 'entry': pentry, 'depth': brace_depth})
                pending_type = None
                # Fall through to normal processing so members/entries on this
                # same line are handled.
            else:
                # Still accumulating the multi-line declaration (constructor
                # params, supertypes, etc.) — skip member detection.
                continue

        tm = KT_TYPE_RE.match(stripped)
        if tm and not KT_NON_PUBLIC.search(tm.group('vis') or ''):
            name = tm.group('name')
            kind = normalise_kind(tm.group('kind'))
            entry = types.get(name) or interfaces.get(name)

            if type_stack:
                parent = type_stack[-1]['entry']
                nested_entry = {
                    'name': name,
                    'kind': kind,
                    'language': 'kotlin',
                    'primary_decl': {'file': filepath, 'line': i},
                    'members': [],
                    'nested_types': [],
                }
                existing_nested = next(
                    (
                        n for n in parent.get('nested_types', [])
                        if n.get('name') == name and n.get('kind') == kind
                        and n.get('primary_decl', {}).get('line') == i
                    ),
                    None,
                )
                if existing_nested is None:
                    parent.setdefault('nested_types', []).append(nested_entry)
                    entry = parent['nested_types'][-1]
                else:
                    entry = existing_nested
                types.pop(name, None)
                interfaces.pop(name, None)

            if entry is not None:
                if '{' in line:
                    # Body opens on this line — push immediately.
                    type_stack.append({'name': name, 'entry': entry, 'depth': brace_depth})
                else:
                    # No '{' on declaration line: could be a multi-line declaration
                    # (body on a future line) or a leaf type (no body at all, e.g. a
                    # sealed class subtype like `class IDLE : Base()`).
                    # Defer the push until we see the '{'; if another type appears first
                    # at the same depth, this is a leaf and we never push.
                    pending_type = (name, entry)

        if not type_stack:
            continue

        target = type_stack[-1]['entry']

        if KT_COMPANION_RE.match(line):
            target['_in_companion'] = True
            continue

        fm = re.match(
            r'^(?P<vis>(?:(?:private|protected|internal|public|override|open|abstract|'
            r'suspend|inline|operator|infix|tailrec|external|actual|expect|final|'
            r'@\w+\s*)*)\s*)*fun\s+(?P<name>\w+)\s*[\(<]',
            stripped
        )
        if fm and not KT_NON_PUBLIC.search(fm.group('vis') or ''):
            member_name = fm.group('name')
            if not any(m['name'] == member_name for m in target['members']):
                target['members'].append({
                    'name': member_name,
                    'kind': 'func',
                    'file': filepath,
                    'line': i,
                    'signature_hint': stripped[:120],
                    'from_companion': target.get('_in_companion', False),
                })
            continue

        pm = KT_PROP_RE.match(stripped)
        if pm and not KT_NON_PUBLIC.search(pm.group('vis') or ''):
            member_name = pm.group('name')
            if not any(m['name'] == member_name for m in target['members']):
                target['members'].append({
                    'name': member_name,
                    'kind': pm.group('kind'),
                    'file': filepath,
                    'line': i,
                    'signature_hint': stripped[:120],
                    'from_companion': target.get('_in_companion', False),
                })

        if (target.get('kind') in ('enum_class',) and
                brace_depth == type_stack[-1]['depth']):
            # Skip lines that clearly aren't enum entry lines
            clean = stripped.split('//')[0].strip()
            if clean and not re.match(
                    r'^(?:fun\s|val\s|var\s|class\s|interface\s|object\s|companion\s|'
                    r'override\s|@|\}|\{|;|private\s|internal\s|protected\s)', clean):
                # Find all UPPER_SNAKE_CASE identifiers on this line that look like
                # enum entries (followed by '(', ',', ';', or end-of-line).
                for em in re.finditer(
                        r'\b([A-Z][A-Z0-9_]{1,})\b(?=\s*[\(,;]|\s*$)', clean):
                    entry_name = em.group(1)
                    if not any(m['name'] == entry_name for m in target['members']):
                        target['members'].append({
                            'name': entry_name,
                            'kind': 'enum_entry',
                            'file': filepath,
                            'line': i,
                            'signature_hint': line.strip()[:80],
                        })


def process_java_file(filepath: str, content: str, types: dict, interfaces: dict,
                      global_funcs: list, global_consts: list, unhandled: list):
    lines = content.splitlines()
    line_map = {}
    offset = 0
    for i, ln in enumerate(lines, 1):
        line_map[offset] = i
        offset += len(ln) + 1

    def char_to_line(char_pos: int) -> int:
        best = 1
        for o, ln in line_map.items():
            if o <= char_pos:
                best = ln
            else:
                break
        return best

    # Top-level public types
    for m in JAVA_TYPE_RE.finditer(content):
        kind_raw = m.group('kind')
        kind = 'interface' if kind_raw == 'interface' else (
               'enum_class' if kind_raw == 'enum' else
               'annotation' if kind_raw == '@interface' else 'class')
        name = m.group('name')
        lineno = char_to_line(m.start())

        entry = {
            'kind': kind,
            'language': 'java',
            'primary_decl': {'file': filepath, 'line': lineno},
            'members': [],
            'nested_types': [],
        }
        if kind == 'interface':
            interfaces.setdefault(name, entry)
        else:
            types.setdefault(name, entry)

    # Public methods/fields + Java enum entries
    current_type = None
    brace_depth = 0
    type_start_depth = {}
    in_enum_entries = {}  # type_name -> True until first ';' after entries

    for i, line in enumerate(lines, 1):
        brace_depth += line.count('{') - line.count('}')

        tm = JAVA_TYPE_RE.match(line)
        if tm:
            name = tm.group('name')
            kind_raw = tm.group('kind')
            kind = 'interface' if kind_raw == 'interface' else (
                   'enum_class' if kind_raw == 'enum' else
                   'annotation' if kind_raw == '@interface' else 'class')
            if name in types or name in interfaces:
                current_type = name
                type_start_depth[name] = brace_depth
                if kind == 'enum_class':
                    in_enum_entries[name] = True  # enum body starts with entries

        if current_type and brace_depth < type_start_depth.get(current_type, 999):
            current_type = None

        if current_type is None:
            continue

        target = types.get(current_type) or interfaces.get(current_type)
        if target is None:
            continue

        # Detect Java enum entries (UPPER_SNAKE or identifier before ( , ;)
        if in_enum_entries.get(current_type):
            stripped_line = line.strip()
            if stripped_line.startswith('}'):
                in_enum_entries[current_type] = False
            elif ';' in stripped_line and not stripped_line.startswith('//'):
                # Semicolon terminates enum constant list
                in_enum_entries[current_type] = False
                # Still try to capture entries on this same line before ;
                entries_part = stripped_line.split(';')[0]
                for candidate in re.split(r'[,\s]+', entries_part):
                    candidate = candidate.strip().split('(')[0].strip()
                    if candidate and re.match(r'^[A-Z][A-Z0-9_]*$', candidate):
                        if not any(m['name'] == candidate for m in target['members']):
                            target['members'].append({
                                'name': candidate,
                                'kind': 'enum_entry',
                                'file': filepath,
                                'line': i,
                                'signature_hint': line.strip()[:80],
                            })
            elif stripped_line and not stripped_line.startswith('//'):
                # Capture comma-separated enum entries
                entries_part = stripped_line.split('//')[0]
                for candidate in re.split(r'[,\s]+', entries_part):
                    candidate = candidate.strip().split('(')[0].strip()
                    if candidate and re.match(r'^[A-Z][A-Z0-9_]*$', candidate):
                        if not any(m['name'] == candidate for m in target['members']):
                            target['members'].append({
                                'name': candidate,
                                'kind': 'enum_entry',
                                'file': filepath,
                                'line': i,
                                'signature_hint': line.strip()[:80],
                            })
            continue

        mm = JAVA_MEMBER_RE.match(line)
        if mm:
            member_name = mm.group('name')
            # Skip constructor (same name as class) and common non-method tokens
            if member_name not in ('class', 'interface', 'enum', 'if', 'for', 'while', 'return'):
                if not any(m['name'] == member_name for m in target['members']):
                    target['members'].append({
                        'name': member_name,
                        'kind': 'func',
                        'file': filepath,
                        'line': i,
                        'signature_hint': line.strip()[:120],
                    })


# ---------------------------------------------------------------------------
# Main walker
# ---------------------------------------------------------------------------

def count_source_files(root_path: str) -> int:
    count = 0
    for walk_root, _, walk_files in os.walk(root_path):
        walk_root_str = str(walk_root)
        if '/src/main/' not in walk_root_str and '\\src\\main\\' not in walk_root_str:
            continue
        for fname in walk_files:
            if fname.endswith(('.kt', '.java')):
                count += 1
    return count



def collect_files():
    """Return source files plus exclusion metadata."""
    collected = []
    files_excluded_internal = 0
    all_files_seen = set()

    for root, dirs, files in os.walk(SDK_ROOT):
        root_str = str(root)
        all_files_seen.add(root_str + '/')

        kept_dirs = []
        for d in dirs:
            dir_path = os.path.join(root, d) + '/'
            all_files_seen.add(dir_path)
            if should_exclude(dir_path):
                if any(pat in dir_path for pat in INTERNAL_EXCLUDE_PATTERNS):
                    files_excluded_internal += count_source_files(os.path.join(root, d))
                continue
            kept_dirs.append(d)
        dirs[:] = kept_dirs

        if should_exclude(root_str + '/'):
            continue
        if '/src/main/' not in root_str and '\\src\\main\\' not in root_str:
            continue

        for fname in files:
            abs_path = os.path.join(root, fname)
            all_files_seen.add(abs_path)
            if any(pat in abs_path for pat in INTERNAL_EXCLUDE_PATTERNS):
                files_excluded_internal += 1
                continue
            if should_exclude(abs_path):
                continue
            if fname.endswith('.kt'):
                lang = 'kotlin'
            elif fname.endswith('.java'):
                lang = 'java'
            else:
                continue
            rel_path = os.path.relpath(abs_path, REPO_ROOT)
            collected.append((abs_path, rel_path, lang))

    return collected, files_excluded_internal, all_files_seen


def main():
    types = {}
    interfaces = {}
    global_funcs = []
    global_consts = []
    typealiases = []
    unhandled = []

    files_scanned = 0
    kt_files = 0
    java_files = 0

    sdk_source_roots = set()
    collected_files, files_excluded_internal, all_files_seen = collect_files()

    for abs_path, rel_path, lang in collected_files:
        files_scanned += 1
        if lang == 'kotlin':
            kt_files += 1
        else:
            java_files += 1

        # Track source roots
        src_root = re.sub(r'(src/main/(?:java|kotlin)/).*', r'\1', rel_path)
        sdk_source_roots.add(src_root)

        try:
            with open(abs_path, encoding='utf-8', errors='replace') as f:
                content = f.read()
        except Exception as e:
            unhandled.append({'file': rel_path, 'reason': str(e)})
            continue

        if lang == 'kotlin':
            process_kotlin_file(rel_path, content, types, interfaces,
                                global_funcs, global_consts, typealiases, unhandled)
        else:
            process_java_file(rel_path, content, types, interfaces,
                              global_funcs, global_consts, unhandled)

    # Clean up internal scratch fields
    for t in list(types.values()) + list(interfaces.values()):
        t.pop('_in_companion', None)

    members_total = sum(len(t['members']) for t in types.values()) + \
                    sum(len(i['members']) for i in interfaces.values())
    nested_types_total = sum(
        len(t.get('nested_types', []))
        for t in list(types.values()) + list(interfaces.values())
    )
    enum_entries_total = sum(
        sum(1 for m in t.get('members', []) if m.get('kind') == 'enum_entry')
        for t in list(types.values()) + list(interfaces.values())
    )

    output = {
        'extractor_version': EXTRACTOR_VERSION,
        'extractor': 'android-extractor.py',
        'extracted_at': datetime.now(timezone.utc).isoformat(),
        'sdk_product': 'AmityAndroidSDK',
        'sdk_source_roots': sorted(sdk_source_roots),
        'types': types,
        'interfaces': interfaces,
        'global_funcs': global_funcs,
        'global_consts': global_consts,
        'typealiases': typealiases,
        'unhandled': unhandled[:50],  # cap to avoid bloat
        'stats': {
            'files_scanned': files_scanned,
            'kotlin_files': kt_files,
            'java_files': java_files,
            'types': len(types),
            'interfaces': len(interfaces),
            'members_total': members_total,
            'global_funcs': len(global_funcs),
            'global_consts': len(global_consts),
            'typealiases': len(typealiases),
            'nested_types_total': nested_types_total,
            'enum_entries_total': enum_entries_total,
            'files_excluded_internal': files_excluded_internal,
            'excluded_path_patterns': [
                p for p in sorted(EXCLUDE_PATTERNS)
                if any(p in str(f) for f in all_files_seen)
            ],
            'unhandled_lines': len(unhandled),
        },
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, 'w') as f:
        json.dump(output, f, indent=2)
        f.write('\n')

    print(f"Wrote {OUTPUT}", file=sys.stderr)
    stats = output['stats']
    print(
        f"Stats: {stats['files_scanned']} files ({stats['kotlin_files']} Kotlin, {stats['java_files']} Java), "
        f"{stats['types']} types, {stats['interfaces']} interfaces, "
        f"{stats['members_total']} members total, "
        f"{stats['global_funcs']} global funcs, {stats['typealiases']} typealiases",
        file=sys.stderr,
    )


if __name__ == '__main__':
    main()
