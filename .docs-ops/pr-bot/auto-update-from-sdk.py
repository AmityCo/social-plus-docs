#!/usr/bin/env python3
"""
SDK→Docs PR-bot — all 4 platforms (TypeScript, iOS, Android, Flutter).

Diffs the current SDK surface against the committed baseline, applies
high-confidence auto-renames to .mdx files, and opens/updates a draft PR.

Usage:
    python3 auto-update-from-sdk.py --platform <typescript|ios|android|flutter> [--dry-run]

Environment:
    SP_SDKS_ROOT  — parent directory containing SDK repos (default: ../../..)
    GH_TOKEN      — GitHub token for gh CLI (needed in CI; local `gh auth login` also works)
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# ── Paths ─────────────────────────────────────────────────────────────────────

SCRIPT_DIR   = Path(__file__).resolve().parent
DOCS_OPS_DIR = SCRIPT_DIR.parent
REPO_ROOT    = DOCS_OPS_DIR.parent
MDX_ROOT     = REPO_ROOT
BRANCH_PREFIX = "bot/sdk-update-"

# ── Platform config ───────────────────────────────────────────────────────────

PLATFORM_CONFIG = {
    "typescript": {
        "surface_file": "typescript.json",
        "extractor":    "typescript-extractor.py",
        "code_fences":  ["typescript", "ts"],
        "branch_tag":   "ts",
    },
    "ios": {
        "surface_file": "ios.json",
        "extractor":    "ios-extractor.py",
        "code_fences":  ["swift"],
        "branch_tag":   "ios",
    },
    "android": {
        "surface_file": "android.json",
        "extractor":    "android-extractor.py",
        "code_fences":  ["kotlin", "java"],
        "branch_tag":   "android",
    },
    "flutter": {
        "surface_file": "flutter.json",
        "extractor":    "flutter-extractor.py",
        "code_fences":  ["dart"],
        "branch_tag":   "flutter",
    },
}

# ── Levenshtein (stdlib-only) ─────────────────────────────────────────────────

def _levenshtein(a: str, b: str) -> int:
    if len(a) < len(b):
        a, b = b, a
    row = list(range(len(b) + 1))
    for c in a:
        new_row = [row[0] + 1]
        for j, d in enumerate(b):
            new_row.append(min(new_row[-1] + 1, row[j + 1] + 1, row[j] + (c != d)))
        row = new_row
    return row[-1]


def _similar(a: str, b: str, threshold: float = 0.3) -> bool:
    """True if Levenshtein distance / max(len) < threshold."""
    if not a or not b:
        return False
    dist = _levenshtein(a, b)
    return dist / max(len(a), len(b)) < threshold

# ── Surface helpers ───────────────────────────────────────────────────────────

def _flat_refs(surface: dict) -> dict[str, dict]:
    """
    Returns {qualified_name: entry_dict} for any platform surface format.

    TypeScript: uses namespaces + root_exports.
    iOS/Android/Flutter: uses types dict {TypeName: {members: [...]}}.
    """
    refs: dict[str, dict] = {}

    # TypeScript format
    for entry in surface.get("root_exports", []):
        refs[entry["name"]] = {**entry, "namespace": None}
    for ns_name, ns_data in surface.get("namespaces", {}).items():
        for m in ns_data.get("members", []):
            refs[f"{ns_name}.{m['name']}"] = {**m, "namespace": ns_name}

    # iOS / Android / Flutter format (types dict)
    for type_name, type_data in surface.get("types", {}).items():
        pd = type_data.get("primary_decl", {})
        refs[type_name] = {"name": type_name, "kind": type_data.get("kind"), "file": pd.get("file", ""), "line": pd.get("line")}
        for m in type_data.get("members", []):
            refs[f"{type_name}.{m['name']}"] = {**m, "namespace": type_name}
        # nested_types can be a list (iOS) or a dict (future platforms)
        nested = type_data.get("nested_types", {})
        if isinstance(nested, dict):
            for nested_name, nested_data in nested.items():
                npd = nested_data.get("primary_decl", {})
                refs[f"{type_name}.{nested_name}"] = {"name": nested_name, "kind": nested_data.get("kind"), "file": npd.get("file", ""), "line": npd.get("line")}
        elif isinstance(nested, list):
            for nested_data in nested:
                nested_name = nested_data.get("name", "")
                if nested_name:
                    npd = nested_data.get("primary_decl", {})
                    refs[f"{type_name}.{nested_name}"] = {"name": nested_name, "kind": nested_data.get("kind"), "file": npd.get("file", ""), "line": npd.get("line")}

    # iOS top-level functions/consts
    for entry in surface.get("global_funcs", []):
        refs[entry["name"]] = {**entry, "namespace": None}
    for entry in surface.get("global_consts", []):
        refs[entry["name"]] = {**entry, "namespace": None}

    # Android interfaces
    for iface_name, iface_data in surface.get("interfaces", {}).items():
        pd = iface_data.get("primary_decl", {})
        refs[iface_name] = {"name": iface_name, "kind": "interface", "file": pd.get("file", ""), "line": pd.get("line")}
        for m in iface_data.get("members", []):
            refs[f"{iface_name}.{m['name']}"] = {**m, "namespace": iface_name}

    # Flutter mixins (dict) / extensions (list)
    for section in ("mixins", "extensions"):
        section_data = surface.get(section, {})
        if isinstance(section_data, dict):
            items: list = [(k, v) for k, v in section_data.items()]
        elif isinstance(section_data, list):
            items = [(e.get("name", ""), e) for e in section_data if e.get("name")]
        else:
            items = []
        for type_name, type_data in items:
            pd = type_data.get("primary_decl", {})
            refs[type_name] = {"name": type_name, "kind": section[:-1], "file": pd.get("file", ""), "line": pd.get("line")}

    return refs


def _compute_diff(baseline: dict, candidate: dict) -> dict:
    """Compute ADDED / REMOVED / RENAMED between two surfaces."""
    base_refs = _flat_refs(baseline)
    cand_refs = _flat_refs(candidate)

    base_keys = set(base_refs)
    cand_keys = set(cand_refs)

    raw_added   = cand_keys - base_keys
    raw_removed = base_keys - cand_keys

    renamed: list[dict] = []
    confirmed_added:   set[str] = set()
    confirmed_removed: set[str] = set()

    # Build rename pairs: same file:line OR similar name
    for rem in raw_removed:
        rem_entry = base_refs[rem]
        for add in raw_added:
            if add in confirmed_added:
                continue
            add_entry = cand_refs[add]
            same_location = (
                rem_entry.get("file", "").split("/")[-1] == add_entry.get("file", "").split("/")[-1]
                and rem_entry.get("line") == add_entry.get("line")
            )
            similar_name = _similar(rem.split(".")[-1], add.split(".")[-1])
            if same_location or similar_name:
                renamed.append({"from": rem, "to": add, "confidence": "same_location" if same_location else "similar_name"})
                confirmed_added.add(add)
                confirmed_removed.add(rem)
                break

    added   = raw_added   - confirmed_added
    removed = raw_removed - confirmed_removed

    return {
        "added":   sorted(added),
        "removed": sorted(removed),
        "renamed": renamed,
    }

# ── Auto-rename in MDX files ──────────────────────────────────────────────────

def _apply_renames_to_file(path: Path, renames: list[dict], code_fences: list[str]) -> list[dict]:
    """
    Apply renames inside the platform's code blocks.
    Skips blocks marked with <!-- doc-as-test: skip -->.
    Returns list of {file, from, to, line} for each substitution made.
    """
    content = path.read_text(encoding="utf-8")
    lines   = content.split("\n")
    changes: list[dict] = []

    in_block  = False
    skip_block = False
    new_lines = []
    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        # Check for skip marker on previous line
        if stripped.startswith("```"):
            lang_part = stripped[3:].split()[0].lower() if len(stripped) > 3 else ""
            if lang_part in code_fences and not in_block:
                # Check previous non-empty line for skip marker
                prev_content = "\n".join(new_lines[-5:]) if new_lines else ""
                skip_block = "doc-as-test: skip" in prev_content
                in_block = True
            elif in_block and stripped == "```":
                in_block = False
                skip_block = False

        if in_block and not skip_block:
            for r in renames:
                old_bare = r["from"].split(".")[-1]
                new_bare = r["to"].split(".")[-1]
                if old_bare in line:
                    new_line = line.replace(old_bare, new_bare)
                    if new_line != line:
                        changes.append({"file": str(path.relative_to(REPO_ROOT)), "from": r["from"], "to": r["to"], "line": i})
                        line = new_line
                        break  # one rename per line

        new_lines.append(line)

    if changes:
        path.write_text("\n".join(new_lines), encoding="utf-8")

    return changes


def apply_all_renames(renames: list[dict], code_fences: list[str], dry_run: bool) -> list[dict]:
    """Walk all .mdx files and apply renames. In dry_run, report and restore."""
    all_changes: list[dict] = []
    for mdx in MDX_ROOT.rglob("*.mdx"):
        if ".docs-ops" in str(mdx):
            continue
        changes = _apply_renames_to_file(mdx, renames, code_fences)
        if changes:
            if dry_run:
                for c in changes:
                    print(f"  [dry-run] would rename {c['from']} → {c['to']} in {c['file']}:{c['line']}")
            all_changes.extend(changes)
    if dry_run:
        subprocess.run(["git", "checkout", "--", "."], cwd=REPO_ROOT, capture_output=True)
    return all_changes

# ── Git / GH helpers ──────────────────────────────────────────────────────────

def _git(args: list[str], cwd: Path = REPO_ROOT, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True, check=check)


def _gh(args: list[str], check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["gh"] + args, cwd=REPO_ROOT, capture_output=True, text=True, check=check)


SDK_REPO_NAMES = {
    "typescript": "AmityTypescriptSDK",
    "ios":        "AmitySDKIOS",
    "android":    "Amity-Social-Cloud-SDK-Android",
    "flutter":    "Amity-Social-Cloud-SDK-Flutter-Internal",
}


def get_sdk_sha(platform: str = "typescript") -> str:
    sdks_root = Path(os.environ.get("SP_SDKS_ROOT", str(REPO_ROOT.parent))).resolve()
    sdk_dir   = sdks_root / SDK_REPO_NAMES[platform]
    if sdk_dir.exists():
        result = _git(["rev-parse", "--short", "HEAD"], cwd=sdk_dir, check=False)
        if result.returncode == 0:
            return result.stdout.strip()
    return "unknown"


def get_sdk_commit_msg(platform: str = "typescript") -> str:
    sdks_root = Path(os.environ.get("SP_SDKS_ROOT", str(REPO_ROOT.parent))).resolve()
    sdk_dir   = sdks_root / SDK_REPO_NAMES[platform]
    if sdk_dir.exists():
        result = _git(["log", "-1", "--format=%s"], cwd=sdk_dir, check=False)
        if result.returncode == 0:
            return result.stdout.strip()
    return ""


def get_baseline_sha(platform: str = "typescript") -> str:
    cfg = PLATFORM_CONFIG[platform]
    result = _git(["log", "-1", "--format=%h", "--", f".docs-ops/sdk-surface/{cfg['surface_file']}"], check=False)
    return result.stdout.strip() if result.returncode == 0 else "unknown"


def find_existing_bot_pr(platform: str = "typescript") -> dict | None:
    """Return the first open bot PR for this platform, or None."""
    result = _gh(["pr", "list", "--state", "open", "--label", "bot", "--json", "number,headRefName,url"], check=False)
    if result.returncode != 0:
        return None
    try:
        prs = json.loads(result.stdout)
        tag = PLATFORM_CONFIG[platform]["branch_tag"]
        for pr in prs:
            branch = pr.get("headRefName", "")
            if branch.startswith(f"{BRANCH_PREFIX}{tag}-"):
                return pr
    except (json.JSONDecodeError, KeyError):
        pass
    return None


def commit_and_push(branch: str, changes: list[dict], surface_updated: bool, message: str) -> None:
    _git(["checkout", "-B", branch])
    _git(["add", "--", "*.mdx"])
    if surface_updated:
        _git(["add", "--", ".docs-ops/sdk-surface/typescript.json"])
    _git(["commit", "-m", message,
          "--trailer", "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"])
    _git(["push", "--force-with-lease", "--set-upstream", "origin", branch])

# ── Main ──────────────────────────────────────────────────────────────────────

def run_extractor_to_temp(platform: str) -> dict:
    """Run platform extractor, capture the output JSON, restore baseline."""
    cfg = PLATFORM_CONFIG[platform]
    surface_path = DOCS_OPS_DIR / "sdk-surface" / cfg["surface_file"]
    extractor    = DOCS_OPS_DIR / "extractors" / cfg["extractor"]

    baseline_content = surface_path.read_text(encoding="utf-8")
    env = {**os.environ}
    result = subprocess.run(
        [sys.executable, str(extractor)],
        env=env, capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"ERROR: {platform} extractor failed:\n", result.stderr, file=sys.stderr)
        surface_path.write_text(baseline_content, encoding="utf-8")
        sys.exit(1)
    candidate = json.loads(surface_path.read_text(encoding="utf-8"))
    # Restore baseline — don't dirty working tree pre-commit
    surface_path.write_text(baseline_content, encoding="utf-8")
    return candidate


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--platform", default="typescript",
                        choices=list(PLATFORM_CONFIG.keys()),
                        help="SDK platform (default: typescript)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Log actions but don't write files, commit, or open PRs")
    args = parser.parse_args()

    platform = args.platform
    cfg      = PLATFORM_CONFIG[platform]
    today    = datetime.date.today().isoformat()

    surface_path = DOCS_OPS_DIR / "sdk-surface" / cfg["surface_file"]

    print(f"[pr-bot] platform={platform} date={today} dry_run={args.dry_run}")

    # 1. Extract candidate surface
    print(f"[pr-bot] running {platform} extractor ...")
    candidate = run_extractor_to_temp(platform)
    print(f"[pr-bot] candidate surface: {candidate.get('stats', {})}")

    # 2. Load baseline
    baseline = json.loads(surface_path.read_text(encoding="utf-8"))
    print(f"[pr-bot] baseline surface: {baseline.get('stats', {})}")

    # 3. Diff
    diff    = _compute_diff(baseline, candidate)
    added   = diff["added"]
    removed = diff["removed"]
    renamed = diff["renamed"]

    print(f"[pr-bot] diff: added={len(added)} removed={len(removed)} renamed={len(renamed)}")

    if not added and not removed and not renamed:
        print("[pr-bot] no surface changes — nothing to do. Exiting cleanly.")
        sys.exit(0)

    # 4. Apply auto-renames
    code_fences = cfg["code_fences"]
    print(f"[pr-bot] applying {len(renamed)} auto-renames in {code_fences} blocks ...")
    changes = apply_all_renames(renamed, code_fences, dry_run=args.dry_run)
    print(f"[pr-bot] auto-renames applied: {len(changes)} substitutions across {len(set(c['file'] for c in changes))} files")

    # 5. Build PR comment data
    sdk_sha      = get_sdk_sha(platform)
    sdk_msg      = get_sdk_commit_msg(platform)
    baseline_sha = get_baseline_sha(platform)
    existing_pr  = find_existing_bot_pr(platform)
    comment_data = {
        "platform":     platform,
        "sdk_sha":      sdk_sha,
        "sdk_msg":      sdk_msg,
        "baseline_sha": baseline_sha,
        "diff": {"added": added, "removed": removed, "renamed": renamed},
        "changes":      changes,
    }

    comment_json = SCRIPT_DIR / "results" / f"pr-comment-data-{platform}.json"
    comment_json.parent.mkdir(exist_ok=True)
    comment_json.write_text(json.dumps(comment_data, indent=2) + "\n")

    comment_md_path = SCRIPT_DIR / "results" / f"pr-comment-{platform}.md"
    subprocess.run([sys.executable, str(SCRIPT_DIR / "render-pr-comment.py"), str(comment_json), str(comment_md_path)], check=True)
    comment_body = comment_md_path.read_text()
    print("\n[pr-bot] PR comment preview:\n" + "-" * 60)
    print(comment_body[:800])
    print("..." if len(comment_body) > 800 else "")
    print("-" * 60)

    if args.dry_run:
        print(f"[pr-bot] --dry-run: skipping commit/push/PR for {platform}. Done.")
        return

    # 6. Update surface file to candidate in-repo
    surface_path.write_text(json.dumps(candidate, indent=2) + "\n")

    # 7. Commit + push to platform-tagged bot branch
    branch = f"{BRANCH_PREFIX}{cfg['branch_tag']}-{today}"
    if existing_pr:
        branch = existing_pr["headRefName"]
        print(f"[pr-bot] appending to existing bot PR #{existing_pr['number']} on branch {branch}")

    commit_msg = f"bot: {platform} SDK surface update {today}\n\nSDK @ {sdk_sha}: {sdk_msg}"
    commit_and_push(branch, changes, surface_updated=True, message=commit_msg)

    # 8. Open or update draft PR
    if existing_pr:
        _gh(["pr", "comment", str(existing_pr["number"]), "--body", comment_body])
        print(f"[pr-bot] updated PR #{existing_pr['number']}: {existing_pr['url']}")
    else:
        result = _gh([
            "pr", "create",
            "--title", f"[bot] {platform} SDK surface update {today}",
            "--body",  comment_body,
            "--draft",
            "--label", "bot",
            "--head",  branch,
        ])
        pr_url = result.stdout.strip()
        print(f"[pr-bot] created draft PR: {pr_url}")


if __name__ == "__main__":
    main()
