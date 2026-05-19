# SDK Drift Watcher — PR-bot for TypeScript

Automatically detects surface changes in AmityTypescriptSDK and opens a draft PR in this docs repo with auto-applied renames.

## How it works

```
Daily 8am UTC (or workflow_dispatch)
  │
  ├─ Clone AmityTypescriptSDK @ HEAD
  ├─ Re-run TS extractor → candidate surface
  ├─ Diff candidate vs committed sdk-surface/typescript.json
  │
  ├─ No diff? → exit cleanly (no PR created — most days)
  │
  └─ Diff found?
       ├─ Classify: ADDED / REMOVED / RENAMED
       ├─ Apply auto-renames to .mdx code blocks (conservative: same file:line OR Levenshtein < 0.3)
       ├─ Update sdk-surface/typescript.json to new candidate
       ├─ Commit + push to branch bot/sdk-update-YYYY-MM-DD
       └─ Open (or update existing) draft PR with structured comment
```

## Files

| File | Purpose |
|---|---|
| `auto-update-from-sdk.py` | Main bot script — extract, diff, rename, PR |
| `render-pr-comment.py` | Render `pr-comment-data.json` → markdown comment |
| `results/pr-comment-data.json` | Last run's diff data (gitignored) |
| `results/pr-comment.md` | Last run's rendered comment (gitignored) |
| `.github/workflows/sdk-drift-watcher.yml` | Daily GH Action |

## Manually triggering

Go to **Actions → SDK Drift Watcher → Run workflow** in the GitHub UI, or:

```sh
gh workflow run sdk-drift-watcher.yml
```

## When a draft PR appears

1. **Review the "Needs your review" section** — check removed APIs against customer-facing docs
2. **Spot-check the auto-rewrites** — they're conservative but worth a glance
3. **Run the local gate** (optional): `python3 .docs-ops/ci/check-drift.py --base origin/main`
4. **Convert to ready + merge** — the bot does not auto-merge

## Local dry-run

```sh
# Ensure AmityTypescriptSDK is cloned as a sibling:
# sp-sdks/AmityTypescriptSDK
# sp-sdks/social-plus-docs

cd social-plus-docs
python3 .docs-ops/pr-bot/auto-update-from-sdk.py --platform typescript --dry-run
```

The dry-run logs what would change but makes no commits and opens no PR.

## Disabling temporarily

Comment out the `cron:` line in `.github/workflows/sdk-drift-watcher.yml`. The `workflow_dispatch:` trigger still works for manual runs.

## Rename heuristic

The bot classifies a REMOVED+ADDED pair as a RENAME when:
- **`same_location`** (high confidence): the old and new name map to the same `file:line` in the SDK source
- **`similar_name`** (medium confidence): Levenshtein distance / max(len) < 0.30

When uncertain, the bot leaves the ref as REMOVED (in "Needs your review") rather than auto-rename incorrectly.

## When this WON'T work

- **SDK repo goes private**: add a `token: ${{ secrets.SDK_READ_PAT }}` to the checkout step and create a PAT with `contents: read` on the SDK repo
- **SDK repo moves**: update `repository: AmityCo/AmityTypescriptSDK` in the workflow
- **Extractor breaks on a new SDK barrel pattern**: the extractor may need updating before the bot can diff correctly — check `.docs-ops/extractors/typescript-extractor.py`
- **`GITHUB_TOKEN` lacks PR-write scope**: check the `permissions:` block in the workflow; the token needs `contents: write` + `pull-requests: write`

## Platform expansion

iOS / Android / Flutter bots follow the same shape. After TS proves the pattern, replicate:
1. Add `--platform <platform>` branch to `auto-update-from-sdk.py`
2. Add a job to `sdk-drift-watcher.yml` (or a new workflow per platform)
3. Each platform needs its own extractor and SDK checkout path
