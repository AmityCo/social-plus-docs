#!/usr/bin/env python3
"""
iOS docs-accuracy validator.

Scans all .mdx files for Swift/Obj-C references to the iOS social.plus SDK
public APIs and diffs them against `.docs-ops/sdk-surface/ios.json`.
Emits a drift report at `.docs-ops/evals/ios-accuracy-drift.json`.

Detection scope (conservative, low false-positive):
  1. Inside ```swift fenced code blocks:
       a. Static/type-level refs: `<TypeName>.<member>` where TypeName is in
          `types` or `protocols` from ios.json.
       b. Imports: flag `import Xxx` where Xxx starts with 'Amity' or 'Eko'
          but is NOT a known valid module.
  2. Inside ```objc / ```objective-c blocks: same checks, severity=objc.
  3. v1 out of scope: signature validation, inferred-type property access,
     closures, generics, SwiftUI patterns.
"""
from __future__ import annotations
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

DOCS_OPS_ROOT = Path(__file__).resolve().parent.parent
DOCS_REPO_ROOT = DOCS_OPS_ROOT.parent
SURFACE_PATH = DOCS_OPS_ROOT / "sdk-surface" / "ios.json"
REPORT_PATH = DOCS_OPS_ROOT / "evals" / "ios-accuracy-drift.json"

# Swift fenced block languages
SWIFT_LANGS = {"swift"}
OBJC_LANGS = {"objc", "objective-c"}
ALL_IOS_LANGS = SWIFT_LANGS | OBJC_LANGS

# Known valid import modules (SDK umbrella + well-known system frameworks)
KNOWN_VALID_IMPORTS = {
    # SDK modules
    "AmitySDK", "EkoChat", "EkoStreamPublisher", "UpstraVideoPlayerKit",
    # Apple system frameworks
    "UIKit", "Foundation", "AVFoundation", "Combine", "SwiftUI", "CoreData",
    "CoreLocation", "MapKit", "CoreGraphics", "QuartzCore", "CoreMotion",
    "CoreBluetooth", "CoreNFC", "SafariServices", "MessageUI",
    "UserNotifications", "AuthenticationServices", "WebKit", "StoreKit",
    "CloudKit", "GameKit", "ARKit", "RealityKit", "SceneKit",
    "SpriteKit", "Metal", "MetalKit", "ModelIO", "Vision", "NaturalLanguage",
    "CreateML", "CoreML", "Speech", "Accelerate", "simd",
    "XCTest", "os", "Darwin", "Swift",
    # Common third-party used with Amity
    "RxSwift", "RxCocoa", "Alamofire", "SDWebImage", "Kingfisher",
    "livekit_client", "LiveKitClient",
}

# Fenced code block RE — mirrors ts-accuracy-validator.py pattern
FENCE_RE = re.compile(
    r"^```([A-Za-z0-9_\-]+)[^\n]*\n(.*?)^```",
    re.MULTILINE | re.DOTALL,
)

# Import statement in Swift/ObjC
SWIFT_IMPORT_RE = re.compile(r"^\s*import\s+([A-Za-z_][A-Za-z0-9_]*)", re.MULTILINE)
OBJC_IMPORT_RE = re.compile(r'^\s*#import\s+[<"]([A-Za-z_][A-Za-z0-9_]*)', re.MULTILINE)


def load_surface() -> tuple[dict, dict]:
    """Return (types_dict, protocols_dict) from ios.json."""
    if not SURFACE_PATH.exists():
        print(f"ERROR: {SURFACE_PATH} not found. Run ios-extractor.py first.", file=sys.stderr)
        sys.exit(2)
    surface = json.loads(SURFACE_PATH.read_text(encoding="utf-8"))
    return surface.get("types", {}), surface.get("protocols", {})


def build_member_index(types: dict, protocols: dict) -> dict[str, list[str]]:
    """Map member_name → [TypeName, ...] for hint lookups."""
    index: dict[str, list[str]] = {}
    for container in (types, protocols):
        for type_name, info in container.items():
            for m in info.get("members", []):
                member_name = m["name"]
                index.setdefault(member_name, []).append(type_name)
    return index


def lookup_member(types: dict, protocols: dict, type_name: str, member_name: str) -> bool:
    """Return True if member_name exists on type_name (in types or protocols)."""
    info = types.get(type_name) or protocols.get(type_name)
    if not info:
        return False  # unknown type — skip (not our job to flag unknown types)
    member_names = {m["name"] for m in info.get("members", [])}
    return member_name in member_names


def find_fenced_blocks(text: str) -> list[tuple[str, str, int]]:
    """Return list of (lang, body, start_line_1indexed) for each fenced code block."""
    blocks = []
    for m in FENCE_RE.finditer(text):
        lang = m.group(1).lower().replace("-", "")  # 'objective-c' → 'objectivec'
        if lang == "objectivec":
            lang = "objc"
        body = m.group(2)
        start_line = text.count("\n", 0, m.start()) + 1
        blocks.append((lang, body, start_line))
    return blocks


def scan_swift_block(
    body: str,
    start_line: int,
    types: dict,
    protocols: dict,
    member_index: dict[str, list[str]],
    lang: str,
) -> list[dict]:
    """Scan one Swift code block. Return list of issue dicts."""
    issues: list[dict] = []
    all_type_names = set(types.keys()) | set(protocols.keys())

    # --- 1. Dotted refs: TypeName.member ---
    # Pattern: word boundary, known type name, dot, identifier
    # We build a single alternation regex for all type names.
    if all_type_names:
        type_name_pat = re.compile(
            r"\b(" + "|".join(re.escape(n) for n in all_type_names) + r")"
            r"\.([A-Za-z_][A-Za-z0-9_]*)"
        )
        seen_pairs: set[tuple[str, str]] = set()
        for m in type_name_pat.finditer(body):
            type_name = m.group(1)
            member_name = m.group(2)
            pair = (type_name, member_name)
            if pair in seen_pairs:
                continue
            seen_pairs.add(pair)

            # Skip method call patterns that are likely instance method calls on
            # a local variable that happens to share a type name — heuristic: if
            # the match is preceded by a lowercase letter or closing bracket we
            # can't tell, so we'd have too many false positives. Focus only on
            # UPPERCASE-starting type names (Swift convention: types are PascalCase).
            if not type_name[0].isupper():
                continue

            if not lookup_member(types, protocols, type_name, member_name):
                line_in_block = body.count("\n", 0, m.start()) + 1
                issues.append({
                    "kind": "unknown_type_member",
                    "ref": f"{type_name}.{member_name}",
                    "type_name": type_name,
                    "member_name": member_name,
                    "line": start_line + line_in_block - 1,
                    "hint_present_at": member_index.get(member_name, []),
                    "severity": lang,  # 'swift' or 'objc'
                })

    # --- 2. Import checks (only flag Amity*/Eko* modules we don't recognise) ---
    import_re = OBJC_IMPORT_RE if lang == "objc" else SWIFT_IMPORT_RE
    for m in import_re.finditer(body):
        module = m.group(1)
        if module in KNOWN_VALID_IMPORTS:
            continue
        # Only flag SDK-namespace-looking imports (Amity* or Eko*)
        if not (module.startswith("Amity") or module.startswith("Eko")):
            continue
        line_in_block = body.count("\n", 0, m.start()) + 1
        issues.append({
            "kind": "unknown_import",
            "ref": f"import {module}",
            "module": module,
            "line": start_line + line_in_block - 1,
            "hint_present_at": [],
            "severity": lang,
        })

    return issues


def main() -> int:
    types, protocols = load_surface()
    member_index = build_member_index(types, protocols)

    mdx_files = sorted(DOCS_REPO_ROOT.glob("**/*.mdx"))
    mdx_files = [
        f for f in mdx_files
        if ".docs-ops/" not in str(f.relative_to(DOCS_REPO_ROOT))
        and "node_modules/" not in str(f)
        and ".pytest_cache/" not in str(f)
    ]

    per_file_issues: dict[str, list[dict]] = {}
    total_issues = 0
    files_scanned = 0
    swift_blocks_scanned = 0
    objc_blocks_scanned = 0

    for path in mdx_files:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        files_scanned += 1
        blocks = find_fenced_blocks(text)
        file_issues: list[dict] = []
        for lang, body, start_line in blocks:
            if lang in SWIFT_LANGS:
                swift_blocks_scanned += 1
            elif lang in OBJC_LANGS:
                objc_blocks_scanned += 1
            else:
                continue
            file_issues.extend(
                scan_swift_block(body, start_line, types, protocols, member_index, lang)
            )
        if file_issues:
            rel = str(path.relative_to(DOCS_REPO_ROOT))
            per_file_issues[rel] = file_issues
            total_issues += len(file_issues)

    # Aggregate top missing refs
    missing_counts: dict[str, int] = {}
    for issues in per_file_issues.values():
        for i in issues:
            key = i.get("ref", "")
            missing_counts[key] = missing_counts.get(key, 0) + 1
    top_missing = sorted(missing_counts.items(), key=lambda kv: -kv[1])[:20]

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "validator": "ios-accuracy-validator.py",
        "surface_used": str(SURFACE_PATH.relative_to(DOCS_REPO_ROOT)),
        "stats": {
            "files_scanned": files_scanned,
            "swift_blocks_scanned": swift_blocks_scanned,
            "objc_blocks_scanned": objc_blocks_scanned,
            "files_with_issues": len(per_file_issues),
            "total_issues": total_issues,
        },
        "top_missing_refs": [{"ref": k, "doc_occurrences": v} for k, v in top_missing],
        "issues_by_file": per_file_issues,
    }

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    print(f"wrote {REPORT_PATH.relative_to(DOCS_REPO_ROOT)}", file=sys.stderr)
    print(f"  files scanned: {files_scanned}", file=sys.stderr)
    print(f"  swift blocks: {swift_blocks_scanned}, objc blocks: {objc_blocks_scanned}", file=sys.stderr)
    print(f"  files with issues: {len(per_file_issues)}", file=sys.stderr)
    print(f"  total issues: {total_issues}", file=sys.stderr)
    if top_missing:
        print(f"  top missing refs:", file=sys.stderr)
        for ref, count in top_missing[:10]:
            print(f"    {count:3d}x {ref}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
