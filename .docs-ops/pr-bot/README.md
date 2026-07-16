# SDK Drift Watcher — PR-bot (all 4 platforms)

Automatically detects surface changes in all 4 Amity SDK repos and opens a draft PR in this docs repo with auto-applied renames. Runs daily as a 4-platform matrix GH Action.

## Supported platforms

| Platform | SDK repo | Surface file |
|---|---|---|
| TypeScript | `AmityCo/AmityTypescriptSDK` | `sdk-surface/typescript.json` |
| iOS | `AmityCo/AmitySDKIOS` | `sdk-surface/ios.json` |
| Android | `AmityCo/Amity-Social-Cloud-SDK-Android` | `sdk-surface/android.json` |
| Flutter | `AmityCo/Amity-Social-Cloud-SDK-Flutter-Internal` | `sdk-surface/flutter.json` |

## How it works

```
Daily 8am UTC (or workflow_dispatch)
  │
  ├─ [Matrix: typescript / ios / android / flutter — runs in parallel]
  │
  ├─ Clone SDK repo @ HEAD
  ├─ Re-run platform extractor → candidate surface
  ├─ Diff candidate vs committed sdk-surface/<platform>.json
  │
  ├─ No diff? → exit cleanly (no PR — most days)
  │
  └─ Diff found?
       ├─ Classify: ADDED / REMOVED / RENAMED
       ├─ Apply auto-renames to .mdx code blocks
       │   (conservative: same file:line OR Levenshtein < 0.30)
       ├─ Update sdk-surface/<platform>.json to new candidate
       ├─ Commit + push to branch bot/sdk-update-<platform>-YYYY-MM-DD
       └─ Open (or update existing) draft PR with structured comment
```

## Files

| File | Purpose |
|---|---|
| `auto-update-from-sdk.py` | Main bot script — extract, diff, rename, PR |
| `render-pr-comment.py` | Render `pr-comment-data-<platform>.json` → markdown comment |
| `results/pr-comment-data-<platform>.json` | Last run's diff data (gitignored) |
| `results/pr-comment-<platform>.md` | Last run's rendered comment (gitignored) |
| `.github/workflows/sdk-drift-watcher.yml` | Daily GH Action (matrix) |

## Required secrets

All 4 SDK repos are private. The workflow needs:

| Secret | Value |
|---|---|
| `SDK_READONLY_PAT` | GitHub PAT with `contents: read` on all 4 SDK repos |

Create the PAT under the bot account or a service account. Set it in **Settings → Secrets → Actions → New repository secret**.

## Manually triggering

Go to **Actions → SDK Drift Watcher → Run workflow** in the GitHub UI. Choose **all** or a single platform from the dropdown, or use:

```sh
gh workflow run sdk-drift-watcher.yml -f platform=all       # all 4 platforms
gh workflow run sdk-drift-watcher.yml -f platform=ios       # one platform
```

## When a draft PR appears

1. **Review the "Needs your review" section** — check removed APIs against customer-facing docs
2. **Spot-check the auto-rewrites** — they're conservative but worth a glance
3. **Run the local gate** (optional): `python3 .docs-ops/ci/check-drift.py --base origin/main`
4. **Convert to ready + merge** — the bot does not auto-merge

## Local dry-run

All 4 SDK repos must be cloned as siblings of `social-plus-docs/`:

```
sp-sdks/
  social-plus-docs/          ← this repo
  AmityTypescriptSDK/
  AmitySDKIOS/
  Amity-Social-Cloud-SDK-Android/
  Amity-Social-Cloud-SDK-Flutter-Internal/
```

Then:

```sh
cd social-plus-docs
python3 .docs-ops/pr-bot/auto-update-from-sdk.py --platform typescript --dry-run
python3 .docs-ops/pr-bot/auto-update-from-sdk.py --platform ios --dry-run
python3 .docs-ops/pr-bot/auto-update-from-sdk.py --platform android --dry-run
python3 .docs-ops/pr-bot/auto-update-from-sdk.py --platform flutter --dry-run
```

Each dry-run logs what would change but makes no commits and opens no PR.

## Disabling a platform temporarily

To skip one platform, comment out its entry in the `matrix.include` list in `.github/workflows/sdk-drift-watcher.yml`. The other platforms continue to run unaffected.

## Rename heuristic

The bot classifies a REMOVED+ADDED pair as a RENAME when:
- **`same_location`** (high confidence): the old and new name map to the same `file:line` in the SDK source
- **`similar_name`** (medium confidence): Levenshtein distance / max(len) < 0.30

When uncertain, the bot leaves the ref as REMOVED (in "Needs your review") rather than auto-rename incorrectly.

## When this WON'T work

- **`SDK_READONLY_PAT` missing or expired**: workflow will fail at the SDK checkout step — renew the PAT and update the secret
- **SDK repo moves**: update the `sdk_repo` value in the relevant matrix entry in the workflow
- **Extractor breaks on a new SDK pattern**: the per-platform extractor may need updating — check `.docs-ops/extractors/<platform>-extractor.py`
- **`GITHUB_TOKEN` lacks PR-write scope**: check the `permissions:` block in the workflow; the token needs `contents: write` + `pull-requests: write`
