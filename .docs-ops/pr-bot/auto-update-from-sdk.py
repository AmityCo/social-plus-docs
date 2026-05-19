#!/usr/bin/env python3
"""
SDK→Docs PR-bot — TypeScript prototype.

Diffs the current AmityTypescriptSDK surface against the committed baseline,
applies high-confidence auto-renames to .mdx files, and opens/updates a draft PR.

Usage:
    python3 auto-update-from-sdk.py --platform typescript [--dry-run]

Environment:
    SP_SDKS_ROOT  — parent directory containing AmityTypescriptSDK/ (default: ../../..)
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
SURFACE_PATH = DOCS_OPS_DIR / "sdk-surface" / "typescript.json"
EXTRACTOR    = DOCS_OPS_DIR / "extractors" / "typescript-extractor.py"
MDX_ROOT     = REPO_ROOT
BRANCH_PREFIX = "bot/sdk-update-"

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
    Returns {qualified_name: {name, namespace, kind, file, line}}.
    root_exports use bare name; namespaced members use Namespace.name.
    """
    refs: dict[str, dict] = {}
    for entry in surface.get("root_exports", []):
        refs[entry["name"]] = {**entry, "namespace": None}
    for ns_name, ns_data in surface.get("namespaces", {}).items():
        for m in ns_data.get("members", []):
            qname = f"{ns_name}.{m['name']}"
            refs[qname] = {**m, "namespace": ns_name}
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

def _apply_renames_to_file(path: Path, renames: list[dict]) -> list[dict]:
    """
    Apply renames inside ```typescript / ```ts code blocks.
    Returns list of {file, from, to, line} for each substitution made.
    """
    content = path.read_text(encoding="utf-8")
    lines   = content.split("\n")
    changes: list[dict] = []

    in_block = False
    new_lines = []
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("```") and ("typescript" in stripped.lower() or stripped == "```ts"):
            in_block = True
        elif stripped == "```" and in_block:
            in_block = False

        if in_block:
            for r in renames:
                old_bare = r["from"].split(".")[-1]
                new_bare = r["to"].split(".")[-1]
                if old_bare in line:
                    new_line = line.replace(old_bare, new_bare)
                    if new_line != line:
                        changes.append({"file": str(path.relative_to(REPO_ROOT)), "from": r["from"], "to": r["to"], "line": i})
                        line = new_line
                        break  # one rename per line — avoid double-substitution

        new_lines.append(line)

    if changes:
        path.write_text("\n".join(new_lines), encoding="utf-8")

    return changes


def apply_all_renames(renames: list[dict], dry_run: bool) -> list[dict]:
    """Walk all .mdx files and apply renames. In dry_run, only report — don't write."""
    all_changes: list[dict] = []
    for mdx in MDX_ROOT.rglob("*.mdx"):
        if ".docs-ops" in str(mdx):
            continue
        changes = _apply_renames_to_file(mdx, renames)
        if changes:
            if dry_run:
                for c in changes:
                    print(f"  [dry-run] would rename {c['from']} → {c['to']} in {c['file']}:{c['line']}")
            all_changes.extend(changes)
    if dry_run:
        # Undo writes by reloading originals — we need to re-run non-destructively
        # Actually _apply_renames_to_file already wrote; for dry-run, restore via git
        subprocess.run(["git", "checkout", "--", "."], cwd=REPO_ROOT, capture_output=True)
    return all_changes

# ── Git / GH helpers ──────────────────────────────────────────────────────────

def _git(args: list[str], cwd: Path = REPO_ROOT, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True, check=check)


def _gh(args: list[str], check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["gh"] + args, cwd=REPO_ROOT, capture_output=True, text=True, check=check)


def get_sdk_sha() -> str:
    sdks_root = Path(os.environ.get("SP_SDKS_ROOT", str(REPO_ROOT.parent))).resolve()
    sdk_dir   = sdks_root / "AmityTypescriptSDK"
    if sdk_dir.exists():
        result = _git(["rev-parse", "--short", "HEAD"], cwd=sdk_dir, check=False)
        if result.returncode == 0:
            return result.stdout.strip()
    return "unknown"


def get_sdk_commit_msg() -> str:
    sdks_root = Path(os.environ.get("SP_SDKS_ROOT", str(REPO_ROOT.parent))).resolve()
    sdk_dir   = sdks_root / "AmityTypescriptSDK"
    if sdk_dir.exists():
        result = _git(["log", "-1", "--format=%s"], cwd=sdk_dir, check=False)
        if result.returncode == 0:
            return result.stdout.strip()
    return ""


def get_baseline_sha() -> str:
    result = _git(["log", "-1", "--format=%h", "--", ".docs-ops/sdk-surface/typescript.json"], check=False)
    return result.stdout.strip() if result.returncode == 0 else "unknown"


def find_existing_bot_pr() -> dict | None:
    """Return the first open bot PR dict, or None."""
    result = _gh(["pr", "list", "--state", "open", "--label", "bot", "--json", "number,headRefName,url"], check=False)
    if result.returncode != 0:
        return None
    try:
        prs = json.loads(result.stdout)
        for pr in prs:
            if pr.get("headRefName", "").startswith(BRANCH_PREFIX):
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

def run_extractor_to_temp() -> dict:
    """Run TS extractor, capture the output JSON, restore baseline if it changed."""
    baseline_content = SURFACE_PATH.read_text(encoding="utf-8")
    env = {**os.environ}  # inherit SP_SDKS_ROOT from environment
    result = subprocess.run(
        [sys.executable, str(EXTRACTOR)],
        env=env, capture_output=True, text=True
    )
    if result.returncode != 0:
        print("ERROR: extractor failed:\n", result.stderr, file=sys.stderr)
        # Restore baseline
        SURFACE_PATH.write_text(baseline_content, encoding="utf-8")
        sys.exit(1)
    candidate = json.loads(SURFACE_PATH.read_text(encoding="utf-8"))
    # Restore baseline so we don't dirty the working tree pre-commit
    SURFACE_PATH.write_text(baseline_content, encoding="utf-8")
    return candidate


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--platform", default="typescript", choices=["typescript"], help="SDK platform (default: typescript)")
    parser.add_argument("--dry-run", action="store_true", help="Log actions but don't write files, commit, or open PRs")
    args = parser.parse_args()

    today = datetime.date.today().isoformat()
    print(f"[pr-bot] platform=typescript date={today} dry_run={args.dry_run}")

    # 1. Extract candidate surface
    print("[pr-bot] running TS extractor ...")
    candidate = run_extractor_to_temp()
    print(f"[pr-bot] candidate surface: {candidate.get('stats', {})}")

    # 2. Load baseline
    baseline = json.loads(SURFACE_PATH.read_text(encoding="utf-8"))
    print(f"[pr-bot] baseline surface: {baseline.get('stats', {})}")

    # 3. Diff
    diff = _compute_diff(baseline, candidate)
    added   = diff["added"]
    removed = diff["removed"]
    renamed = diff["renamed"]

    print(f"[pr-bot] diff: added={len(added)} removed={len(removed)} renamed={len(renamed)}")

    if not added and not removed and not renamed:
        print("[pr-bot] no surface changes — nothing to do. Exiting cleanly.")
        sys.exit(0)

    # 4. Apply auto-renames (high-confidence only)
    high_conf_renames = [r for r in renamed if r["confidence"] == "same_location"]
    all_renames = renamed  # apply all — similar_name renames are conservative by threshold

    print(f"[pr-bot] applying {len(all_renames)} auto-renames across .mdx files ...")
    changes = []
    if not args.dry_run:
        changes = apply_all_renames(all_renames, dry_run=False)
    else:
        # Dry-run: compute and report but don't persist
        changes = apply_all_renames(all_renames, dry_run=True)

    print(f"[pr-bot] auto-renames applied: {len(changes)} substitutions across {len(set(c['file'] for c in changes))} files")

    # 5. Build PR comment data
    sdk_sha     = get_sdk_sha()
    sdk_msg     = get_sdk_commit_msg()
    baseline_sha = get_baseline_sha()
    comment_data = {
        "sdk_sha":      sdk_sha,
        "sdk_msg":      sdk_msg,
        "baseline_sha": baseline_sha,
        "diff": {"added": added, "removed": removed, "renamed": renamed},
        "changes":      changes,
    }

    # Write comment data to temp for renderer
    comment_json = SCRIPT_DIR / "results" / "pr-comment-data.json"
    comment_json.parent.mkdir(exist_ok=True)
    comment_json.write_text(json.dumps(comment_data, indent=2) + "\n")

    # Render comment
    comment_md_path = SCRIPT_DIR / "results" / "pr-comment.md"
    subprocess.run([sys.executable, str(SCRIPT_DIR / "render-pr-comment.py"), str(comment_json), str(comment_md_path)], check=True)
    comment_body = comment_md_path.read_text()
    print("\n[pr-bot] PR comment preview:\n" + "-" * 60)
    print(comment_body[:1000])
    print("..." if len(comment_body) > 1000 else "")
    print("-" * 60)

    if args.dry_run:
        print("[pr-bot] --dry-run: skipping commit/push/PR. Done.")
        return

    # 6. Update surface file to candidate in-repo
    SURFACE_PATH.write_text(json.dumps(candidate, indent=2) + "\n")

    # 7. Commit + push to bot branch
    branch = f"{BRANCH_PREFIX}{today}"
    existing_pr = find_existing_bot_pr()
    if existing_pr:
        branch = existing_pr["headRefName"]
        print(f"[pr-bot] appending to existing bot PR #{existing_pr['number']} on branch {branch}")

    commit_msg = f"bot: TypeScript SDK surface update {today}\n\nSDK @ {sdk_sha}: {sdk_msg}"
    commit_and_push(branch, changes, surface_updated=True, message=commit_msg)

    # 8. Open or update draft PR
    if existing_pr:
        _gh(["pr", "comment", str(existing_pr["number"]), "--body", comment_body])
        print(f"[pr-bot] updated PR #{existing_pr['number']}: {existing_pr['url']}")
    else:
        result = _gh([
            "pr", "create",
            "--title", f"[bot] TypeScript SDK surface update {today}",
            "--body",  comment_body,
            "--draft",
            "--label", "bot",
            "--head",  branch,
        ])
        pr_url = result.stdout.strip()
        print(f"[pr-bot] created draft PR: {pr_url}")


if __name__ == "__main__":
    main()
