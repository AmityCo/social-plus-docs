#!/usr/bin/env python3
"""
Android Dokka GFM-based surface extractor — v0.2.0-dokka

Reads the `dokkaGfm` output from `amity-sdk/build/dokka/gfm/` and emits
`.docs-ops/sdk-surface/android-from-dokka.json` matching the same schema as
`android.json` produced by `android-extractor.py`.

Invocation approach: `dokkaJson` is not wired in the Android SDK Gradle config
(only `dokkaHtml`, `dokkaGfm`, `dokkaJavadoc` tasks exist as of task 0078).
We use `dokkaGfm` instead — its GFM markdown output is highly structured and
parseable. The perPackageOption suppress rules in `amity-sdk/build.gradle` are
inherited — suppressed packages are not present in the GFM output.

To regenerate the GFM input artifact:
    cd Amity-Social-Cloud-SDK-Android
    ANDROID_HOME=~/Library/Android/sdk ./gradlew :amity-sdk:dokkaGfm
    # Output: amity-sdk/build/dokka/gfm/

Usage (from social-plus-docs/):
    python3 .docs-ops/extractors/android-dokka-extractor.py

Writes:
    .docs-ops/sdk-surface/android-from-dokka.json
    (PARALLEL artifact — android.json is still the primary surface)
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
SCRIPT_DIR   = Path(__file__).resolve().parent
DOCS_OPS     = SCRIPT_DIR.parent
REPO_ROOT    = DOCS_OPS.parent.parent          # sp-sdks/
SDK_ROOT     = REPO_ROOT / "Amity-Social-Cloud-SDK-Android"
GFM_ROOT     = SDK_ROOT / "amity-sdk" / "build" / "dokka" / "gfm" / "amity-sdk"
OUTPUT       = DOCS_OPS / "sdk-surface" / "android-from-dokka.json"

EXTRACTOR_VERSION = "0.2.0-dokka"

# Only include packages under these prefixes (mirrors Dokka suppress rules
# from build.gradle: all com.amity.socialcloud.sdk.{chat,common,core,entity,
# infra,social,video}.* are suppressed; com.ekoapp.* suppressed).
# NOTE: perPackageOption in build.gradle only applies to `dokkaHtml`, not
# `dokkaGfm` — so we apply the same suppressions here explicitly.
# Valid public API packages are: api.*, model.*, helper.*
INCLUDE_PKG_PREFIXES = (
    "com.amity.socialcloud.sdk.api.",
    "com.amity.socialcloud.sdk.model.",
    "com.amity.socialcloud.sdk.helper.",
)

# Package patterns to suppress (mirrors dokkaHtml perPackageOption rules).
# These are the EXACT patterns from amity-sdk/build.gradle applied here.
SUPPRESS_PKG_PATTERNS = (
    "com.amity.socialcloud.sdk.chat.",
    "com.amity.socialcloud.sdk.common",
    "com.amity.socialcloud.sdk.core.",
    "com.amity.socialcloud.sdk.entity.",
    "com.amity.socialcloud.sdk.infra.",
    "com.amity.socialcloud.sdk.social.",
    "com.amity.socialcloud.sdk.video.",
    "com.amity.socialcloud.sdk.dto.",
    "com.ekoapp.",
    "org.amity.",
)

# Dokka-generated synthetic members to skip (boilerplate, not SDK API).
SYNTHETIC_MEMBER_NAMES = {
    "describeContents", "writeToParcel",   # Parcelable boilerplate
    "hashCode", "equals", "toString",      # kotlin data class generated
    "copy", "component1", "component2",    # data class destructuring
    "component3", "component4", "component5",
    "component6", "component7", "component8",
    "valueOf", "values", "entries",        # enum boilerplate
    "name", "ordinal",                     # enum inherited
}

# Declarations that map to "interface" bucket vs "types" bucket
INTERFACE_KINDS = {"interface"}

# Regex for each table row in GFM:
# | [name](local-link.md) | [androidJvm]<br>... |
# We only keep LOCAL members (link is `name.md` or `./name.md`, NOT a cross-ref
# containing `#` or pointing to another type dir).
TABLE_ROW_RE = re.compile(
    r"^\|\s*\[([A-Za-z_][A-Za-z0-9_]*)\]\(([^)]+)\)\s*\|",
)
# Declaration line following [androidJvm]
DECL_KINDS_RE = re.compile(
    r"^(data class|sealed class|abstract class|open class|enum class|"
    r"annotation class|class|interface|object|companion object|typealias|fun|enum)\b"
)
# Strip markdown links from signatures: [Text](url) → Text
STRIP_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")
# Strip angle-bracket generics for simple type names: List<String> → List
STRIP_GENERIC_RE = re.compile(r"<[^>]+>")
# Method signature: fun name(...): ReturnType
SIG_FUN_RE = re.compile(
    r"fun\s+(?:\[[^\]]+\])?\s*(?:\w+\.)*\s*\[?(\w+)\]?[^:]*\)\s*:\s*(.+?)(?:\s*$)",
    re.DOTALL,
)
# Property signature: val/var name: Type
SIG_PROP_RE = re.compile(r"(?:val|var)\s+\[?(\w+)\]?\s*:\s*(.+?)(?:\s*$)", re.DOTALL)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _is_local_link(link: str) -> bool:
    """True if link is a local member file (same type dir), not a cross-ref."""
    # Cross-refs look like: `../../other.package/-OtherType/...#hash`
    # or have `#` fragments (inherited from elsewhere).
    if "#" in link:
        return False
    if link.startswith(".."):
        return False
    if link.startswith("http"):
        return False
    return True


def _clean_sig(raw: str) -> str:
    """Strip markdown links and excessive whitespace from a GFM signature cell."""
    s = STRIP_LINK_RE.sub(r"\1", raw)
    s = s.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
    return " ".join(s.split())


def _extract_return_type(sig_clean: str) -> str | None:
    m = SIG_FUN_RE.search(sig_clean)
    if m:
        return _clean_sig(m.group(2))
    return None


def _extract_params(sig_clean: str) -> list[dict]:
    """Very conservative param extraction from cleaned signature string."""
    paren_m = re.search(r"\(([^)]*)\)", sig_clean)
    if not paren_m:
        return []
    inner = paren_m.group(1).strip()
    if not inner:
        return []
    params = []
    for part in inner.split(","):
        part = part.strip()
        if ":" in part:
            pname, ptype = part.split(":", 1)
            params.append({
                "name": pname.strip().lstrip("*").strip(),
                "type": _clean_sig(ptype.strip()),
            })
    return params


def _parse_type_index(index_path: Path) -> dict | None:
    """Parse a type's index.md and return a surface entry dict, or None."""
    text = index_path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()

    # --- Type name ---
    type_name = None
    for ln in lines[:6]:
        if ln.startswith("# ") and not ln.startswith("# Package"):
            type_name = ln[2:].strip()
            break
    if not type_name:
        return None

    # --- Declaration kind ---
    # Two patterns:
    #   Pattern A: `[androidJvm]` tag then decl on next line (most types)
    #   Pattern B: decl directly after `# TypeName` (some interfaces/sealed)
    decl_kind = "class"
    found_decl = False
    for i, ln in enumerate(lines):
        if ln.strip() == "[androidJvm]":
            for ln2 in lines[i + 1:i + 4]:
                ln2s = ln2.strip()
                if ln2s:
                    m = DECL_KINDS_RE.match(ln2s)
                    if m:
                        decl_kind = m.group(1)
                        found_decl = True
                    break
            break
        # Pattern B: bare declaration line (no [androidJvm] prefix)
        if not found_decl:
            stripped_ln = ln.strip()
            m = DECL_KINDS_RE.match(stripped_ln)
            if m and i > 0:
                # Confirm it's at the top-level decl position (after the # header)
                # by checking that the preceding content is the type header
                decl_kind = m.group(1)
                found_decl = True

    # Normalise
    if decl_kind in ("companion object",):
        decl_kind = "object"
    elif decl_kind == "typealias":
        return None  # handled separately

    # --- Members ---
    members: list[dict] = []
    current_section: str | None = None
    for ln in lines:
        stripped = ln.strip()
        if stripped in ("## Functions", "## Properties", "## Entries", "## Constructors", "## Types"):
            current_section = stripped[3:]  # "Functions" / "Properties" / "Types" / ...
            continue
        if stripped.startswith("## "):
            current_section = None
            continue
        if current_section is None:
            continue

        m = TABLE_ROW_RE.match(stripped)
        if not m:
            continue
        member_name = m.group(1)
        link = m.group(2)

        if not _is_local_link(link):
            continue
        if member_name in SYNTHETIC_MEMBER_NAMES:
            continue

        if current_section == "Functions":
            kind = "method"
        elif current_section == "Properties":
            kind = "property"
        elif current_section == "Entries":
            kind = "enum_entry"
        elif current_section == "Constructors":
            kind = "constructor"
        elif current_section == "Types":
            kind = "nested_type"   # sealed subclasses / objects listed as Types
        else:
            kind = "unknown"

        # Parse raw summary cell from the same table row for signature bonus
        # Row format: `| [name](link) | ... summary ... |`
        row_m = re.match(r"^\|\s*\[[^\]]+\]\([^)]+\)\s*\|\s*(.+)\s*\|", stripped)
        sig_raw = row_m.group(1).strip() if row_m else ""
        sig_clean = _clean_sig(sig_raw)

        # Strip [androidJvm]<br> prefix
        sig_clean = re.sub(r"^\[androidJvm\]<br>", "", sig_clean).strip()

        member_entry: dict = {
            "name": member_name,
            "kind": kind,
        }
        if kind == "method" and sig_clean:
            ret = _extract_return_type(sig_clean)
            params = _extract_params(sig_clean)
            if ret or params:
                member_entry["signature"] = {
                    "parameters": params,
                    "returns": ret,
                }
        elif kind == "property" and sig_clean:
            pm = SIG_PROP_RE.search(sig_clean)
            if pm:
                member_entry["signature"] = {
                    "parameters": [],
                    "returns": _clean_sig(pm.group(2)),
                }

        members.append(member_entry)

    return {
        "name": type_name,
        "kind": decl_kind,
        "members": members,
    }


# ---------------------------------------------------------------------------
# Main extraction
# ---------------------------------------------------------------------------

def extract() -> dict:
    if not GFM_ROOT.exists():
        print(
            f"ERROR: Dokka GFM output not found at {GFM_ROOT}\n"
            "Run: cd Amity-Social-Cloud-SDK-Android && "
            "ANDROID_HOME=~/Library/Android/sdk ./gradlew :amity-sdk:dokkaGfm",
            file=sys.stderr,
        )
        sys.exit(2)

    types: dict[str, dict] = {}
    interfaces: dict[str, dict] = {}
    global_funcs: list[dict] = []
    typealiases: list[dict] = []

    packages_scanned = 0
    types_scanned = 0
    packages_skipped = 0

    # Walk package directories (depth=1 under GFM_ROOT)
    for pkg_dir in sorted(GFM_ROOT.iterdir()):
        if not pkg_dir.is_dir():
            continue
        pkg_name = pkg_dir.name
        if pkg_name in ("[root]", "amity-sdk"):
            continue
        # Apply same suppress rules as dokkaHtml perPackageOption
        if not any(pkg_name.startswith(p) for p in INCLUDE_PKG_PREFIXES):
            packages_skipped += 1
            continue
        if any(pkg_name.startswith(p) for p in SUPPRESS_PKG_PATTERNS):
            packages_skipped += 1
            continue
        packages_scanned += 1

        # Walk type directories (depth=1 under pkg_dir, starts with `-`)
        for type_dir in sorted(pkg_dir.iterdir()):
            if not type_dir.is_dir():
                continue
            if not type_dir.name.startswith("-"):
                continue
            index_md = type_dir / "index.md"
            if not index_md.exists():
                continue
            types_scanned += 1

            entry = _parse_type_index(index_md)
            if entry is None:
                continue

            type_name = entry["name"]
            decl_kind = entry["kind"]
            members = entry["members"]

            # Collect nested types (immediate subdirs that also have index.md)
            nested_types: list[dict] = []
            for nested_dir in sorted(type_dir.iterdir()):
                if not nested_dir.is_dir():
                    continue
                if not nested_dir.name.startswith("-"):
                    continue
                nested_index = nested_dir / "index.md"
                if not nested_index.exists():
                    continue
                nested_entry = _parse_type_index(nested_index)
                if nested_entry:
                    # Flatten Companion object members into the parent type so that
                    # TypeName.companionMethod references resolve correctly (idiomatic Kotlin).
                    if nested_entry["name"] == "Companion":
                        for cm in nested_entry["members"]:
                            cm = dict(cm, from_companion=True)
                            members.append(cm)
                        continue
                    # Flatten Companion object members into the nested type so
                    # NestedType.companionMethod references resolve correctly.
                    companion_dir = nested_dir / "-companion"
                    companion_index = companion_dir / "index.md"
                    if companion_index.exists():
                        comp_entry = _parse_type_index(companion_index)
                        if comp_entry:
                            for cm in comp_entry["members"]:
                                nested_entry["members"].append(dict(cm, from_companion=True))

                    nested_types.append({
                        "name": nested_entry["name"],
                        "kind": nested_entry["kind"],
                        "primary_decl": {"file": str(nested_index.relative_to(SDK_ROOT.parent)), "line": None},
                        "members": nested_entry["members"],
                        "nested_types": [],  # depth limited to 2 levels
                    })

            surface_entry = {
                "kind": decl_kind,
                "language": "kotlin",
                "primary_decl": {
                    "file": str(index_md.relative_to(SDK_ROOT.parent)),
                    "line": None,
                },
                "members": members,
                "nested_types": nested_types,
            }

            if decl_kind in INTERFACE_KINDS:
                interfaces[type_name] = surface_entry
            else:
                types[type_name] = surface_entry

        # Package-level functions (from package index.md ## Functions)
        pkg_index = pkg_dir / "index.md"
        if pkg_index.exists():
            pkg_text = pkg_index.read_text(encoding="utf-8", errors="replace")
            in_funcs = False
            for ln in pkg_text.splitlines():
                stripped = ln.strip()
                if stripped == "## Functions":
                    in_funcs = True
                    continue
                if stripped.startswith("## ") and stripped != "## Functions":
                    in_funcs = False
                if not in_funcs:
                    continue
                m = TABLE_ROW_RE.match(stripped)
                if not m:
                    continue
                if not _is_local_link(m.group(2)):
                    continue
                func_name = m.group(1)
                global_funcs.append({
                    "name": func_name,
                    "kind": "function",
                    "namespace": pkg_name,
                })

    members_total = sum(len(v["members"]) for v in types.values()) + \
                    sum(len(v["members"]) for v in interfaces.values())
    nested_total  = sum(len(v["nested_types"]) for v in types.values())
    enum_entries  = sum(
        sum(1 for m in v["members"] if m["kind"] == "enum_entry")
        for v in types.values()
    )

    output = {
        "extractor_version": EXTRACTOR_VERSION,
        "extractor": "android-dokka-extractor.py",
        "extracted_at": datetime.now(timezone.utc).isoformat(),
        "sdk_product": "AmityAndroidSDK",
        "sdk_dokka_source": str(GFM_ROOT.relative_to(SDK_ROOT.parent)),
        "dokka_invocation": "ANDROID_HOME=~/Library/Android/sdk ./gradlew :amity-sdk:dokkaGfm",
        "types": types,
        "interfaces": interfaces,
        "global_funcs": global_funcs,
        "global_consts": [],
        "typealiases": typealiases,
        "stats": {
            "packages_scanned": packages_scanned,
            "packages_skipped_non_amity": packages_skipped,
            "types": len(types),
            "interfaces": len(interfaces),
            "members_total": members_total,
            "global_funcs": len(global_funcs),
            "nested_types_total": nested_total,
            "enum_entries_total": enum_entries,
        },
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(f"[android-dokka-extractor] wrote {OUTPUT.relative_to(DOCS_OPS.parent)}", file=sys.stderr)
    print(
        f"[android-dokka-extractor] types={len(types)} interfaces={len(interfaces)} "
        f"members={members_total} nested={nested_total}",
        file=sys.stderr,
    )
    return output


if __name__ == "__main__":
    extract()
