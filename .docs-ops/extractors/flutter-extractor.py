#!/usr/bin/env python3
"""
Flutter/Dart SDK surface extractor (v0.1.1)
Regex-based Dart public-API extractor.
Mirrors the structure and conventions of android-extractor.py.

Usage:
    python3 .docs-ops/extractors/flutter-extractor.py
Writes:
    .docs-ops/sdk-surface/flutter.json
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
DOCS_OPS_ROOT = SCRIPT_DIR.parent
REPO_ROOT = DOCS_OPS_ROOT.parent.parent  # extractors/ → .docs-ops/ → social-plus-docs/ → sp-sdks/
SDK_ROOT = REPO_ROOT / "Amity-Social-Cloud-SDK-Flutter-Internal"
LIB_ROOT = SDK_ROOT / "lib"
OUTPUT = DOCS_OPS_ROOT / "sdk-surface" / "flutter.json"

EXTRACTOR_VERSION = "0.1.2"

EXCLUDE_PATTERNS = {
    "/test/",
    "/example/",
    "/examples/",
    "/build/",
    "/.dart_tool/",
    "/.git/",
    "/.pub-cache/",
}

GENERATED_SUFFIXES = (".g.dart", ".freezed.dart", ".gr.dart", ".config.dart")

# ---------------------------------------------------------------------------
# Regex patterns
# ---------------------------------------------------------------------------

# Strip Dart annotations (@override, @deprecated, @JsonKey(...), etc.)
DART_ANNOTATION_LINE_RE = re.compile(r'^\s*@\w+(?:\(.*\))?\s*$')

# Type-level declarations
CLASS_RE = re.compile(
    r'^(?P<abstract>abstract\s+)?(?P<sealed>sealed\s+)?'
    r'(?P<kind>class|mixin|enum)\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)'
    r'(?:\s+extends|\s+implements|\s+with|\s+on|\s*\{|$)'
)
EXTENSION_RE = re.compile(
    r'^extension\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s+on\s+(?P<host>[A-Za-z_][A-Za-z0-9_<>?,\s\[\]]*)\s*\{'
)
TYPEDEF_RE = re.compile(
    r'^typedef\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)'
)

# Member patterns (used inside a type body at brace_depth == type_entry_depth + 1)

# Constructors: "ClassName(" or "ClassName.named(" (not preceded by type keyword)
# We detect constructors by name matching the enclosing type name (done in logic, not regex)

# Factory constructor
FACTORY_RE = re.compile(
    r'^\s*(?:const\s+)?factory\s+([A-Za-z_][A-Za-z0-9_]*)(?:\.([A-Za-z_][A-Za-z0-9_]*))?'
    r'\s*[\(<]'
)

# Method / function: return-type (or void/Future/Stream) followed by name(
METHOD_RE = re.compile(
    r'^\s*(?:static\s+)?(?:(?:override\s+|final\s+|late\s+|async\s+)*)'
    r'(?:Future<[^>]*>|Stream<[^>]*>|void|bool|int|double|String|dynamic|'
    r'[A-Z][A-Za-z0-9_<>?,\[\]\s]*(?:\?)?)\s+'
    r'(?P<name>[a-z_][A-Za-z0-9_]*)\s*[\(<]'
)

# Getter
GETTER_RE = re.compile(
    r'^\s*(?:static\s+)?(?:[A-Za-z_][A-Za-z0-9_<>?,\[\]\s]*(?:\?)?)\s+get\s+'
    r'(?P<name>[a-z_][A-Za-z0-9_]*)'
)

# Setter
SETTER_RE = re.compile(
    r'^\s*set\s+(?P<name>[a-z_][A-Za-z0-9_]*)\s*\('
)

# Field / property (final/var/late final at member level)
FIELD_RE = re.compile(
    r'^\s*(?:static\s+)?(?:final\s+|late\s+final\s+|late\s+|var\s+)'
    r'(?:[A-Za-z_][A-Za-z0-9_<>?,\[\]\s]*(?:\?)?)\s+'
    r'(?P<name>[a-z_][A-Za-z0-9_]*)\s*[=;{]'
)

# Static const field (with explicit type: `static const TypeName name = ...`)
STATIC_CONST_RE = re.compile(
    r'^\s*static\s+const\s+(?:[A-Za-z_][A-Za-z0-9_<>?,\[\]\s]*(?:\?)?)\s+'
    r'(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*='
)

# Untyped static const (type-inferred: `static const name = ...`)
STATIC_CONST_UNTYPED_RE = re.compile(
    r'^\s*static\s+const\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*='
)

# Enum value: at the top of an enum body, bare identifier or ClassName.named(
ENUM_VALUE_RE = re.compile(r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)(?:\s*[,;({]|$)')

# Top-level function (at brace_depth==0, line not starting with space)
TOPLEVEL_FUNC_RE = re.compile(
    r'^(?:(?:Future<[^>]*>|Stream<[^>]*>|void|bool|int|double|String|dynamic|'
    r'[A-Z][A-Za-z0-9_<>?,\[\]\s]*)\s+)'
    r'(?P<name>[a-z_][A-Za-z0-9_]*)\s*[\(<]'
)

# Top-level const
TOPLEVEL_CONST_RE = re.compile(
    r'^(?:const|final)\s+(?:[A-Za-z_][A-Za-z0-9_<>?,\[\]\s]*(?:\?)?)\s+'
    r'(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*='
)

EXPORT_RE = re.compile(
    r"^\s*export\s+['\"](?P<path>[^'\"]+)['\"]"
    r"(?:\s+show\s+(?P<show>[^;]+))?"
    r"(?:\s+hide\s+(?P<hide>[^;]+))?",
    re.MULTILINE,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def should_exclude(path_str: str) -> bool:
    for pat in EXCLUDE_PATTERNS:
        if pat in path_str:
            return True
    # Exclude generated files
    for suffix in GENERATED_SUFFIXES:
        if path_str.endswith(suffix):
            return True
    return False


def is_private(name: str) -> bool:
    """Dart private: name starts with underscore."""
    return name.startswith('_')


def normalize_names_filter(names_filter):
    if names_filter is None:
        return None
    return {name.strip() for name in names_filter if name.strip()}


def merge_names_filter(existing, incoming):
    if existing is None or incoming is None:
        return None
    return set(existing) | set(incoming)


def parse_export_names(raw_names: str):
    cleaned = re.sub(r'/\*.*?\*/', '', raw_names, flags=re.DOTALL)
    cleaned = re.sub(r'//[^\n]*', '', cleaned)
    return frozenset(name.strip() for name in cleaned.split(',') if name.strip())


def find_barrel(lib_root: Path):
    candidate = lib_root / 'amity_sdk.dart'
    if candidate.exists():
        return candidate.resolve()

    best = None
    best_count = 0
    for file_path in lib_root.glob('*.dart'):
        text = file_path.read_text(encoding='utf-8', errors='replace')
        count = sum(
            1 for match in EXPORT_RE.finditer(text)
            if not match.group('path').startswith('package:')
        )
        if count > best_count:
            best_count = count
            best = file_path

    return best.resolve() if best else None


def resolve_barrel(barrel_path: Path, lib_root: Path) -> dict:
    """Returns {abs_path_str: None | set_of_names} for all reachable files."""
    result = {}
    parsed = set()
    lib_root_resolved = lib_root.resolve()
    to_visit = [(barrel_path.resolve(), None)]

    while to_visit:
        file_path, names_filter = to_visit.pop()
        file_path = file_path.resolve()
        abs_str = str(file_path)
        normalized_filter = normalize_names_filter(names_filter)

        if abs_str in result:
            result[abs_str] = merge_names_filter(result[abs_str], normalized_filter)
        else:
            result[abs_str] = None if normalized_filter is None else set(normalized_filter)

        if abs_str in parsed:
            continue
        parsed.add(abs_str)

        if not file_path.exists():
            continue

        text = file_path.read_text(encoding='utf-8', errors='replace')
        for match in EXPORT_RE.finditer(text):
            rel_path = match.group('path')
            if rel_path.startswith('package:'):
                continue

            target = (file_path.parent / rel_path).resolve()
            if target != lib_root_resolved and lib_root_resolved not in target.parents:
                continue

            show_str = match.group('show')
            hide_str = match.group('hide')
            if show_str:
                to_visit.append((target, parse_export_names(show_str)))
            elif hide_str:
                to_visit.append((target, None))
            else:
                to_visit.append((target, None))

    return result


def collect_files(public_files=None):
    """Yield (abs_path, rel_path) for .dart files under lib/."""
    if not LIB_ROOT.exists():
        print(f"ERROR: {LIB_ROOT} not found", file=sys.stderr)
        return
    for root, dirs, files in os.walk(LIB_ROOT):
        dirs[:] = [d for d in dirs if not should_exclude(os.path.join(root, d) + '/')]
        root_str = str(root)
        if should_exclude(root_str + '/'):
            continue
        for fname in files:
            if not fname.endswith('.dart'):
                continue
            abs_path = str((Path(root) / fname).resolve())
            if should_exclude(abs_path):
                continue
            if public_files is not None and abs_path not in public_files:
                continue
            rel_path = os.path.relpath(abs_path, REPO_ROOT)
            yield abs_path, rel_path


# ---------------------------------------------------------------------------
# Per-file processing
# ---------------------------------------------------------------------------

def process_dart_file(filepath: str, content: str,
                      types: dict, mixins: dict, extensions_raw: list,
                      global_funcs: list, global_consts: list,
                      typedefs: list, unhandled: list,
                      stats: dict) -> None:
    lines = content.splitlines()
    is_part_of = any(l.strip().startswith('part of') for l in lines[:5])

    brace_depth = 0
    current_type_name = None    # name of the currently open type/mixin/enum
    current_type_kind = None    # 'class'|'abstract_class'|'mixin'|'enum'|'extension'
    current_type_entry_depth = 0
    current_host_type = None    # for extensions: the 'on Type' part
    in_enum_values = False      # True until we see the first ';' or non-enum-value line

    def add_member(name: str, kind: str, lineno: int, sig: str,
                   from_extension: bool = False, from_static: bool = False):
        if is_private(name):
            return
        record = {
            'name': name,
            'kind': kind,
            'file': filepath,
            'line': lineno,
            'signature_hint': sig.strip()[:120],
        }
        if from_extension:
            record['from_extension'] = True
        if from_static:
            record['from_static'] = True

        target = types.get(current_type_name) or mixins.get(current_type_name)
        if target is not None:
            if not any(m['name'] == name for m in target['members']):
                target['members'].append(record)

    for lineno, raw_line in enumerate(lines, 1):
        line = raw_line.strip()

        # Skip comments
        if line.startswith('//') or line.startswith('*') or line.startswith('/*'):
            brace_depth += raw_line.count('{') - raw_line.count('}')
            continue

        # Skip annotation-only lines
        if DART_ANNOTATION_LINE_RE.match(raw_line):
            continue

        old_depth = brace_depth
        brace_depth += raw_line.count('{') - raw_line.count('}')
        brace_depth = max(0, brace_depth)

        # Pop scope when brace depth drops to or below entry depth
        if current_type_name and brace_depth <= current_type_entry_depth:
            current_type_name = None
            current_type_kind = None
            current_host_type = None
            in_enum_values = False

        # ---- Top-level declarations (depth was 0 before this line's braces) ----
        if old_depth == 0:
            # typedef
            td = TYPEDEF_RE.match(line)
            if td:
                name = td.group('name')
                if not is_private(name):
                    typedefs.append({'name': name, 'file': filepath, 'line': lineno,
                                     'signature_hint': line[:120]})
                continue

            # extension
            ext = EXTENSION_RE.match(line)
            if ext:
                ext_name = ext.group('name')
                host = ext.group('host').strip()
                if not is_private(ext_name):
                    entry = {
                        'kind': 'extension',
                        'language': 'dart',
                        'host_type': host,
                        'primary_decl': {'file': filepath, 'line': lineno},
                        'members': [],
                    }
                    extensions_raw.append((ext_name, host, entry))
                    current_type_name = ext_name
                    current_type_kind = 'extension'
                    current_host_type = host
                    current_type_entry_depth = old_depth
                    in_enum_values = False
                    # Register temporarily in types dict so add_member can find it
                    types[ext_name] = entry
                continue

            # class / mixin / enum
            cm = CLASS_RE.match(line)
            if cm:
                is_abstract = bool(cm.group('abstract'))
                kind_raw = cm.group('kind')
                name = cm.group('name')
                if not is_private(name):
                    kind = ('abstract_class' if is_abstract and kind_raw == 'class'
                            else kind_raw)
                    entry = {
                        'kind': kind,
                        'language': 'dart',
                        'is_part_of': is_part_of,
                        'primary_decl': {'file': filepath, 'line': lineno},
                        'members': [],
                        'extensions': [],
                    }
                    if kind == 'mixin':
                        mixins.setdefault(name, entry)
                    else:
                        types.setdefault(name, entry)
                    current_type_name = name
                    current_type_kind = kind
                    current_type_entry_depth = old_depth
                    in_enum_values = (kind == 'enum')

                    # Single-line enum: enum Foo { A, B, C } — body opens and
                    # closes on the same line, so brace_depth returns to 0 and
                    # the scope is immediately popped on the next iteration.
                    # Extract values here while we still know the entry.
                    if kind == 'enum' and '{' in line:
                        body_m = re.search(r'\{([^}]*)\}', line)
                        if body_m:
                            body_text = body_m.group(1)
                            for tok in re.findall(r'\b([A-Za-z_][A-Za-z0-9_]*)\b', body_text):
                                if not is_private(tok) and tok not in ('static', 'final', 'const'):
                                    entry['members'].append({
                                        'name': tok, 'kind': 'enum_value',
                                        'file': filepath, 'line': lineno,
                                        'signature_hint': line[:120],
                                    })
                            in_enum_values = False
                continue

            # Top-level function
            if not line.startswith('@'):
                tf = TOPLEVEL_FUNC_RE.match(line)
                if tf:
                    name = tf.group('name')
                    if not is_private(name):
                        global_funcs.append({'name': name, 'file': filepath,
                                             'line': lineno, 'signature_hint': line[:120]})
                    continue

                # Top-level const
                tc = TOPLEVEL_CONST_RE.match(line)
                if tc:
                    name = tc.group('name')
                    if not is_private(name):
                        global_consts.append({'name': name, 'file': filepath,
                                              'line': lineno, 'signature_hint': line[:120]})

        # ---- Member declarations (inside type body, depth == entry+1) ----
        # Use old_depth (pre-line brace count) so that method declarations that
        # open their body on the same line (e.g. `void foo() {`) are still
        # captured even though brace_depth == entry_depth+2 after the line.
        if current_type_name and old_depth == current_type_entry_depth + 1:
            # Enum values: lines before first ';' are enum entries
            if current_type_kind == 'enum' and in_enum_values:
                if ';' in line:
                    # Extract any values before the semicolon, then end the values section
                    before_semi = line[:line.index(';')]
                    for tok in re.findall(r'\b([A-Za-z_][A-Za-z0-9_]*)\b', before_semi):
                        if not is_private(tok) and tok not in ('static', 'final', 'const'):
                            add_member(tok, 'enum_value', lineno, line)
                    in_enum_values = False
                    continue
                ev = ENUM_VALUE_RE.match(line)
                if ev:
                    val_name = ev.group(1)
                    if not is_private(val_name) and val_name not in ('static', 'final', 'const'):
                        add_member(val_name, 'enum_value', lineno, line)
                continue

            # Factory constructor
            fm = FACTORY_RE.match(raw_line)
            if fm:
                class_part = fm.group(1)
                named_part = fm.group(2)
                name = named_part if named_part else class_part
                if not is_private(name):
                    add_member(name, 'factory' if named_part else 'constructor',
                                lineno, line)
                continue

            # Regular constructor: ClassName( or ClassName.named(
            # Detect: line starts (optionally const) with the exact current type name
            if current_type_name and not is_private(current_type_name):
                ctor_re = re.compile(
                    r'^\s*(?:const\s+)?' + re.escape(current_type_name) +
                    r'(?:\.([A-Za-z_][A-Za-z0-9_]*))?\s*\('
                )
                ctor = ctor_re.match(raw_line)
                if ctor:
                    named = ctor.group(1)
                    if named:
                        if not is_private(named):
                            add_member(named, 'named_constructor', lineno, line)
                    else:
                        add_member(current_type_name, 'constructor', lineno, line)
                    continue

            # Getter
            gm = GETTER_RE.match(raw_line)
            if gm:
                name = gm.group('name')
                if not is_private(name):
                    add_member(name, 'getter', lineno, line)
                continue

            # Setter
            sm = SETTER_RE.match(raw_line)
            if sm:
                name = sm.group('name')
                if not is_private(name):
                    add_member(name, 'setter', lineno, line)
                continue

            # Static const field (with explicit type annotation)
            scm = STATIC_CONST_RE.match(raw_line)
            if scm:
                name = scm.group('name')
                if not is_private(name):
                    from_static = 'static' in raw_line[:raw_line.index(name)]
                    add_member(name, 'const', lineno, line, from_static=from_static)
                continue

            # Untyped static const (type-inferred: `static const name = ...`)
            uscm = STATIC_CONST_UNTYPED_RE.match(raw_line)
            if uscm:
                name = uscm.group('name')
                if not is_private(name):
                    add_member(name, 'const', lineno, line, from_static=True)
                continue

            # Field (final/var/late)
            fld = FIELD_RE.match(raw_line)
            if fld:
                name = fld.group('name')
                if not is_private(name):
                    add_member(name, 'field', lineno, line)
                continue

            # Method
            mm = METHOD_RE.match(raw_line)
            if mm:
                name = mm.group('name')
                # Exclude Dart keywords that can appear as identifiers after a type
                if name not in ('if', 'for', 'while', 'switch', 'return', 'new',
                                'super', 'this', 'class', 'catch', 'else'):
                    if not is_private(name):
                        from_static = bool(re.match(r'^\s*static\b', raw_line))
                        add_member(name, 'func', lineno, line, from_static=from_static)


def apply_names_filter(rel_path: str, names_filter,
                       types: dict, mixins: dict, extensions_raw: list,
                       global_funcs: list, global_consts: list,
                       typedefs: list) -> None:
    if names_filter is None:
        return

    allowed_names = set(names_filter)

    for bucket in (types, mixins):
        for name, entry in list(bucket.items()):
            if entry.get('primary_decl', {}).get('file') == rel_path and name not in allowed_names:
                bucket.pop(name, None)

    extensions_raw[:] = [
        item for item in extensions_raw
        if item[2].get('primary_decl', {}).get('file') != rel_path or item[0] in allowed_names
    ]
    global_funcs[:] = [
        item for item in global_funcs
        if item.get('file') != rel_path or item.get('name') in allowed_names
    ]
    global_consts[:] = [
        item for item in global_consts
        if item.get('file') != rel_path or item.get('name') in allowed_names
    ]
    typedefs[:] = [
        item for item in typedefs
        if item.get('file') != rel_path or item.get('name') in allowed_names
    ]


# ---------------------------------------------------------------------------
# Post-process: aggregate extension members into host types
# ---------------------------------------------------------------------------

def aggregate_extensions(types: dict, mixins: dict, extensions_raw: list,
                          extensions_out: list) -> None:
    """Aggregate extension members into the host type if it's in the surface."""
    for ext_name, host_type, entry in extensions_raw:
        # Strip generic params from host type name (e.g., "AmityPost<T>" → "AmityPost")
        host_base = re.sub(r'<.*', '', host_type).strip()

        # Remove the temporary extension entry from types
        types.pop(ext_name, None)

        target = types.get(host_base) or mixins.get(host_base)
        if target:
            # Annotate extension members and merge
            for m in entry['members']:
                m['from_extension'] = True
                if not any(em['name'] == m['name'] for em in target['members']):
                    target['members'].append(m)
            target.setdefault('extensions', []).append({
                'name': ext_name,
                'file': entry['primary_decl']['file'],
                'line': entry['primary_decl']['line'],
            })
        else:
            # Unknown host — keep as a standalone extension
            extensions_out.append({
                'name': ext_name,
                'host_type': host_type,
                'primary_decl': entry['primary_decl'],
                'members': entry['members'],
            })


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    types: dict = {}
    mixins: dict = {}
    extensions_raw: list = []   # (name, host, entry) — temporary
    extensions_out: list = []   # orphan extensions with unknown host
    global_funcs: list = []
    global_consts: list = []
    typedefs: list = []
    unhandled: list = []
    stats: dict = {}

    barrel_path = find_barrel(LIB_ROOT)
    public_names_by_file = {}
    public_files = None

    all_files = list(collect_files())
    files_scanned_total = len(all_files)

    if barrel_path is None:
        unhandled.append({
            'file': str(LIB_ROOT.relative_to(REPO_ROOT)),
            'reason': 'No public barrel file found; falling back to all lib files',
        })
        files_to_process = all_files
    else:
        public_names_by_file = resolve_barrel(barrel_path, LIB_ROOT)
        public_files = set(public_names_by_file)
        files_to_process = [item for item in all_files if item[0] in public_files]

    public_files_count = len(files_to_process)
    files_scanned = 0
    part_of_files = 0

    for abs_path, rel_path in files_to_process:
        files_scanned += 1
        try:
            with open(abs_path, encoding='utf-8', errors='replace') as f:
                content = f.read()
        except Exception as e:
            unhandled.append({'file': rel_path, 'reason': str(e)})
            continue

        if any(content.lstrip().startswith('part of') or
               line.strip().startswith('part of')
               for line in content.splitlines()[:5]):
            part_of_files += 1

        process_dart_file(rel_path, content, types, mixins, extensions_raw,
                          global_funcs, global_consts, typedefs, unhandled, stats)
        apply_names_filter(
            rel_path,
            public_names_by_file.get(abs_path) if barrel_path else None,
            types,
            mixins,
            extensions_raw,
            global_funcs,
            global_consts,
            typedefs,
        )

    aggregate_extensions(types, mixins, extensions_raw, extensions_out)

    members_total = (
        sum(len(t['members']) for t in types.values()) +
        sum(len(m['members']) for m in mixins.values())
    )
    enum_values_total = sum(
        sum(1 for m in t['members'] if m.get('kind') == 'enum_value')
        for t in types.values()
    )

    output = {
        'extractor_version': EXTRACTOR_VERSION,
        'extractor': 'flutter-extractor.py',
        'extracted_at': datetime.now(timezone.utc).isoformat(),
        'sdk_product': 'amity_sdk',
        'sdk_source_roots': [str(LIB_ROOT.relative_to(REPO_ROOT))],
        'types': types,
        'mixins': mixins,
        'extensions': extensions_out,
        'global_funcs': global_funcs,
        'global_consts': global_consts,
        'typedefs': typedefs,
        'unhandled': unhandled[:50],
        'stats': {
            'files_scanned': files_scanned,
            'part_of_files': part_of_files,
            'types': len(types),
            'mixins': len(mixins),
            'members_total': members_total,
            'enum_values_total': enum_values_total,
            'global_funcs': len(global_funcs),
            'global_consts': len(global_consts),
            'typealiases': len(typedefs),
            'unhandled_lines': len(unhandled),
            'barrel_path': str(barrel_path.relative_to(REPO_ROOT)) if barrel_path else 'FALLBACK_NO_BARREL',
            'public_files_count': public_files_count,
            'files_excluded_not_in_barrel': files_scanned_total - public_files_count,
        },
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, 'w') as f:
        json.dump(output, f, indent=2)
        f.write('\n')

    s = output['stats']
    print(f"Wrote {OUTPUT}", file=sys.stderr)
    print(
        f"Stats: {s['files_scanned']} files ({s['part_of_files']} part-of), "
        f"{s['types']} types, {s['mixins']} mixins, "
        f"{s['members_total']} members total, "
        f"{s['global_funcs']} global funcs, {s['typealiases']} typedefs, "
        f"barrel={s['barrel_path']}",
        file=sys.stderr,
    )

    top_types = sorted(
        [(n, len(t['members'])) for n, t in types.items()],
        key=lambda x: -x[1]
    )[:10]
    if top_types:
        print("Top types by member count:", file=sys.stderr)
        for name, count in top_types:
            print(f"  {count:4d} {name}", file=sys.stderr)


if __name__ == '__main__':
    main()
