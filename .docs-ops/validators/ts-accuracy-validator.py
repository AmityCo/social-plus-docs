#!/usr/bin/env python3
"""
TypeScript docs-accuracy validator.

Scans all .mdx files for TypeScript/JavaScript references to social.plus SDK
public APIs and diffs them against `.docs-ops/sdk-surface/typescript.json`.
Emits a drift report at `.docs-ops/evals/ts-accuracy-drift.json`.

Detection scope (conservative, low false-positive):
  1. Inside ```typescript|ts|tsx|javascript|js|jsx fenced blocks:
       a. Namespaced refs: `<Namespace>.<member>` where Namespace is one of the
          24 known namespaces from typescript.json.
       b. Import names: `import { X, Y } from '@amityco/ts-sdk'` — X/Y must be
          a known namespace OR a known root export.
  2. Findings are reported per-file with file:line for triage.

Out of scope (v1):
  - Signature/parameter validation (extractor v1 doesn't emit signatures).
  - References outside fenced code blocks (prose mentions are noisy).
  - Renames across versions (we report against current SDK; legacy SDKs are
    a separate concern, handled by versioned snapshots if we ever add them).
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

DOCS_OPS_ROOT = Path(__file__).resolve().parent.parent
DOCS_REPO_ROOT = DOCS_OPS_ROOT.parent
SURFACE_PATH = DOCS_OPS_ROOT / "sdk-surface" / "typescript.json"
REPORT_PATH = DOCS_OPS_ROOT / "evals" / "ts-accuracy-drift.json"

# Languages we treat as TS-SDK consumers.
TS_LANGS = {"typescript", "ts", "tsx", "javascript", "js", "jsx"}

# Fence pattern: ``` followed by lang token, capturing the body until the closing ```
FENCE_RE = re.compile(
    r"^[ \t]*```([A-Za-z0-9_]+)[^\n]*\n(.*?)^[ \t]*```",
    re.MULTILINE | re.DOTALL,
)
IMPORT_RE = re.compile(
    r"""import\s*(?:type\s+)?\{([^}]+)\}\s*from\s*['"]@amityco/ts-sdk['"]""",
    re.DOTALL,
)


def load_surface() -> tuple[dict, set[str]]:
    """Return (namespaces_tree, root_exports_set).

    namespaces_tree mirrors the structure from typescript-extractor.py v1.1:
      {ns_name: {"members": [...], "sub_namespaces": {...}}}
    """
    if not SURFACE_PATH.exists():
        print(f"ERROR: {SURFACE_PATH} not found. Run typescript-extractor.py first.", file=sys.stderr)
        sys.exit(2)
    surface = json.loads(SURFACE_PATH.read_text(encoding="utf-8"))
    root_exports = {e["name"] for e in surface["root_exports"]}
    return surface["namespaces"], root_exports


def lookup_path(namespaces: dict, parts: list[str]) -> str | None:
    """Walk a dotted path `parts` through the namespace tree.

    Returns the kind of the final part: 'namespace' | 'member' | None (not found).
    Sub-namespaces matched as final part return 'namespace'; member matches return 'member'.
    """
    if not parts:
        return None
    head, *rest = parts
    node = namespaces.get(head)
    if not node:
        return None
    if not rest:
        return "namespace"
    for i, part in enumerate(rest):
        is_last = (i == len(rest) - 1)
        member_names = {m["name"] for m in node.get("members", [])}
        sub_ns = node.get("sub_namespaces", {})
        # Check if the remaining dotted path is a dotted member name (e.g. "SessionStates.ESTABLISHED").
        remaining_dotted = ".".join(rest[i:])
        if remaining_dotted in member_names:
            return "member"
        if is_last:
            if part in member_names:
                return "member"
            if part in sub_ns:
                return "namespace"
            return None
        # not last: must be a sub-namespace to keep descending
        if part in sub_ns:
            node = sub_ns[part]
        else:
            return None
    return None


def find_fenced_blocks(text: str) -> list[tuple[str, str, int]]:
    """Return list of (lang, body, start_line) for each fenced code block."""
    blocks = []
    for m in FENCE_RE.finditer(text):
        lang = m.group(1).lower()
        body = m.group(2)
        start_line = text.count("\n", 0, m.start()) + 1
        blocks.append((lang, body, start_line))
    return blocks


def all_member_names(namespaces: dict) -> dict[str, list[str]]:
    """Map each member name to the list of dotted paths where it appears (for hints)."""
    out: dict[str, list[str]] = {}
    def walk(prefix: list[str], ns_dict: dict) -> None:
        for ns_name, info in ns_dict.items():
            for m in info.get("members", []):
                path = ".".join(prefix + [ns_name])
                out.setdefault(m["name"], []).append(path)
            walk(prefix + [ns_name], info.get("sub_namespaces", {}))
    walk([], namespaces)
    return out


_JEST_SUFFIXES: frozenset[str] = frozenset({
    "mockResolvedValue", "mockRejectedValue", "mockImplementation",
    "mockReturnValue", "mockReturnValueOnce", "mockResolvedValueOnce",
    "mockRejectedValueOnce", "mockReset", "mockClear", "mockRestore",
    "mockImplementationOnce", "toHaveBeenCalled", "toHaveBeenCalledWith",
    "toHaveBeenCalledTimes", "toBe", "toEqual", "toStrictEqual",
    "toBeNull", "toBeUndefined", "toBeDefined", "toBeInstanceOf",
})


def scan_block(body: str, start_line: int, namespaces: dict, roots: set[str], member_index: dict[str, list[str]]) -> list[dict]:
    """Scan one code block body. Return list of issue dicts."""
    issues: list[dict] = []
    known_ns_names = set(namespaces.keys())

    # 1. Dotted refs starting with a known top-level namespace.
    # Capture up to 3 dotted segments after the namespace (handles Namespace.Sub.method).
    ns_pat = re.compile(
        r"\b(" + "|".join(re.escape(n) for n in known_ns_names) + r")"
        r"(?:\.([A-Za-z_][A-Za-z0-9_]*))"
        r"(?:\.([A-Za-z_][A-Za-z0-9_]*))?"
        r"(?:\.([A-Za-z_][A-Za-z0-9_]*))?"
    )
    seen_in_block: set[tuple[str, ...]] = set()
    for m in ns_pat.finditer(body):
        parts = tuple(p for p in m.groups() if p)
        # Skip Jest/testing method suffixes — not SDK refs.
        if parts[-1] in _JEST_SUFFIXES:
            continue
        if parts in seen_in_block:
            continue
        seen_in_block.add(parts)
        result = lookup_path(namespaces, list(parts))
        if result is None:
            # Try progressively shorter prefixes to find the first failing segment.
            last_valid_depth = 0
            for depth in range(1, len(parts) + 1):
                if lookup_path(namespaces, list(parts[:depth])) is not None:
                    last_valid_depth = depth
                else:
                    break
            failing_part = parts[last_valid_depth] if last_valid_depth < len(parts) else parts[-1]
            line_in_block = body.count("\n", 0, m.start()) + 1
            issues.append({
                "kind": "unknown_namespace_path",
                "ref": ".".join(parts),
                "first_unknown_part": failing_part,
                "valid_prefix_depth": last_valid_depth,
                "line": start_line + line_in_block - 1,
                "hint_present_at": member_index.get(failing_part, []),
            })

    # 2. Named imports from '@amityco/ts-sdk'
    for m in IMPORT_RE.finditer(body):
        names_raw = m.group(1)
        line_in_block = body.count("\n", 0, m.start()) + 1
        for raw in names_raw.split(","):
            name = raw.strip().split(" as ")[0].strip()
            if not name or not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", name):
                continue
            if name in known_ns_names or name in roots:
                continue
            issues.append({
                "kind": "unknown_import_from_sdk",
                "import_name": name,
                "line": start_line + line_in_block - 1,
                "hint_present_at": member_index.get(name, []),
            })

    return issues


def main() -> int:
    namespaces, roots = load_surface()
    member_index = all_member_names(namespaces)

    mdx_files = sorted(DOCS_REPO_ROOT.glob("**/*.mdx"))
    # Exclude .docs-ops/ itself and node_modules / build artifacts.
    mdx_files = [
        f for f in mdx_files
        if ".docs-ops/" not in str(f.relative_to(DOCS_REPO_ROOT))
        and "node_modules/" not in str(f)
        and ".pytest_cache/" not in str(f)
    ]

    per_file_issues: dict[str, list[dict]] = {}
    total_issues = 0
    files_scanned = 0
    blocks_scanned = 0

    for path in mdx_files:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        files_scanned += 1
        blocks = find_fenced_blocks(text)
        file_issues: list[dict] = []
        for lang, body, start_line in blocks:
            if lang not in TS_LANGS:
                continue
            blocks_scanned += 1
            file_issues.extend(scan_block(body, start_line, namespaces, roots, member_index))
        if file_issues:
            rel = str(path.relative_to(DOCS_REPO_ROOT))
            per_file_issues[rel] = file_issues
            total_issues += len(file_issues)

    # Aggregate: most-mentioned missing refs (likely renamed/removed APIs).
    missing_member_counts: dict[str, int] = {}
    for issues in per_file_issues.values():
        for i in issues:
            if i["kind"] == "unknown_namespace_path":
                key = i["ref"]
                missing_member_counts[key] = missing_member_counts.get(key, 0) + 1
            elif i["kind"] == "unknown_import_from_sdk":
                key = f'import {i["import_name"]}'
                missing_member_counts[key] = missing_member_counts.get(key, 0) + 1

    top_missing = sorted(missing_member_counts.items(), key=lambda kv: -kv[1])[:20]

    report = {
        "generated_at": "2026-05-17T11:00:00Z",
        "validator": "ts-accuracy-validator.py",
        "surface_used": str(SURFACE_PATH.relative_to(DOCS_REPO_ROOT)),
        "stats": {
            "files_scanned": files_scanned,
            "ts_blocks_scanned": blocks_scanned,
            "files_with_issues": len(per_file_issues),
            "total_issues": total_issues,
        },
        "top_missing_apis": [{"ref": k, "doc_occurrences": v} for k, v in top_missing],
        "issues_by_file": per_file_issues,
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    print(f"wrote {REPORT_PATH.relative_to(DOCS_REPO_ROOT)}")
    print(f"  files scanned: {files_scanned}")
    print(f"  TS code blocks scanned: {blocks_scanned}")
    print(f"  files with issues: {len(per_file_issues)}")
    print(f"  total issues: {total_issues}")
    if top_missing:
        print(f"  top missing refs:")
        for ref, count in top_missing[:10]:
            print(f"    {count:3d}× {ref}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
