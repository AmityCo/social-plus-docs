#!/usr/bin/env python3
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

EXTRACTOR_VERSION = "0.1.0"

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
    # A simple heuristic: fun declarations with no leading indent are top-level
    for i, line in enumerate(lines, 1):
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
    # Walk line by line, track brace depth to know which type scope we're in
    current_type = None
    brace_depth = 0
    type_start_depth = {}  # type_name → brace_depth at entry

    for i, line in enumerate(lines, 1):
        # Stripped for matching, but count braces in raw line
        stripped = strip_kt_annotations(line)

        # Update brace depth
        brace_depth += line.count('{') - line.count('}')

        # Check if this line opens a new type (to track scope)
        tm = KT_TYPE_RE.match(stripped)
        if tm and not KT_NON_PUBLIC.search(tm.group('vis') or ''):
            name = tm.group('name')
            kind = normalise_kind(tm.group('kind'))
            if name in types or name in interfaces:
                current_type = name
                type_start_depth[name] = brace_depth

        # Pop type scope when brace depth falls below entry depth
        if current_type and brace_depth < type_start_depth.get(current_type, 999):
            current_type = None

        if current_type is None:
            continue

        target = types.get(current_type) or interfaces.get(current_type)
        if target is None:
            continue

        # Companion object: mark a flag on type
        if KT_COMPANION_RE.match(line):
            target['_in_companion'] = True
            continue

        # Fun member
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

        # Val/var property
        pm = KT_PROP_RE.match(stripped)
        if pm and not KT_NON_PUBLIC.search(pm.group('vis') or ''):
            member_name = pm.group('name')
            if not any(m['name'] == member_name for m in target['members']):
                target['members'].append({
                    'name': member_name,
                    'kind': pm.group('kind'),  # 'val' or 'var'
                    'file': filepath,
                    'line': i,
                    'signature_hint': stripped[:120],
                    'from_companion': target.get('_in_companion', False),
                })

        # Enum entries (all caps, at class body depth)
        if (target.get('kind') in ('enum_class',) and
                brace_depth == type_start_depth.get(current_type, 0) + 1):
            em = KT_ENUM_ENTRY_RE.match(line)
            if em:
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

    # Public methods/fields
    current_type = None
    brace_depth = 0
    type_start_depth = {}

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

        if current_type and brace_depth < type_start_depth.get(current_type, 999):
            current_type = None

        if current_type is None:
            continue

        target = types.get(current_type) or interfaces.get(current_type)
        if target is None:
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

def collect_files():
    """Yield (absolute_path_str, relative_path_str, lang) for all source files."""
    for root, dirs, files in os.walk(SDK_ROOT):
        # Prune excluded dirs in-place
        dirs[:] = [d for d in dirs if not should_exclude(os.path.join(root, d) + '/')]
        root_str = str(root)
        if should_exclude(root_str + '/'):
            continue
        # Only process files under src/main/
        if '/src/main/' not in root_str and '\\src\\main\\' not in root_str:
            continue
        for fname in files:
            if fname.endswith('.kt'):
                lang = 'kotlin'
            elif fname.endswith('.java'):
                lang = 'java'
            else:
                continue
            abs_path = os.path.join(root, fname)
            rel_path = os.path.relpath(abs_path, REPO_ROOT)
            yield abs_path, rel_path, lang


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

    for abs_path, rel_path, lang in collect_files():
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
