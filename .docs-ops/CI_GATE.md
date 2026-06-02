# Docs-Ops CI Gate

The CI gate is what makes the cleanup work in this directory *durable*. Without it, any PR that lands stale API names re-introduces drift and we never converge. With it, every push is compared against the baseline and blocked if it introduces new (file, API-ref) pairs.

## How it works

```
                ┌────────────────────────────────────┐
                │  YOU PUSH                           │
                └─────────────────┬──────────────────┘
                                  │
                                  ▼
                ┌────────────────────────────────────┐
                │  pre-push hook                      │
                │  → .docs-ops/ci/check-drift.py     │
                └─────────────────┬──────────────────┘
                                  │
                ┌─────────────────┴──────────────────┐
                │                                     │
                ▼                                     ▼
        [ baseline pass ]                    [ candidate pass ]
        git worktree @ origin/main           working tree
        run extractor + validator            run extractor + validator
        capture drift report                 capture drift report
                │                                     │
                └─────────────────┬──────────────────┘
                                  ▼
                ┌────────────────────────────────────┐
                │  diff drift reports                 │
                │  regression = NEW (file, ref) pair  │
                │  appears in candidate but not        │
                │  baseline                            │
                └─────────────────┬──────────────────┘
                                  │
                  ┌───────────────┴────────────────┐
                  │                                 │
                  ▼                                 ▼
            no new pairs                    new pairs exist
            ✓ push proceeds                 ✗ push blocked
                                            list of new pairs printed
```

## What counts as regression

The gate blocks on **any new (file, API-ref) pair** introduced — even if the total drift count is flat or lower. This catches *net-zero churn*: fixing 5 old issues while introducing 5 new ones holds the count but moves the bug surface, which is still a regression.

Reduction in count with no new pairs → **PASS**.
Reduction in count but some new pairs → **FAIL** (fix the new pairs; the resolves don't excuse them).
Increase in count → **FAIL** by definition (always includes new pairs).

## What it doesn't gate (yet)

- **Prose, structure, IA**: the gate is API-accuracy-only. The 6-dimension rubric is broader; per-PR scoring is a future addition.
- **SDK changes**: the gate compares docs against the SDK surface AS COMMITTED in this repo. When the upstream SDK changes, someone must re-run the extractor and commit the new `sdk-surface/*.json`. A separate workflow (TBD) will detect SDK changes and open docs PRs to update.

## Doc-as-test layer

In addition to the regex-based drift check, the gate runs **doc-as-test** steps that type-check code blocks from the top-traffic doc pages against the real SDK source. Four languages are currently covered: **TypeScript** (via `tsc --noEmit --strict`), **Flutter/Dart** (via `dart analyze`), **Android/Kotlin** (via `kotlinc`), and **iOS/Swift** (via `swiftc`). iOS requires macOS — on Linux machines, the iOS check reports `unavailable` and does not block the gate.

### What it catches (and what the regex validator misses)

| Problem type | Regex validator | Doc-as-test |
|---|---|---|
| Stale API name (renamed method) | ✓ catches | ✓ catches |
| Wrong argument type | ✗ misses | ✓ catches |
| Missing required argument | ✗ misses | ✓ catches |
| Wrong async/await pattern | ✗ misses | ✓ catches |
| Broken syntax (copy-paste error) | ✗ misses | ✓ catches |

### Gate policy

**TypeScript** — **Blocks the push** if any failure contains a `TS2xxx` error (type error = real API drift). **Warns but does NOT block** on `TS1xxx`-only errors (parser errors in intentionally partial/illustrative snippets).

**Flutter/Dart** — **Blocks the push** if `dart analyze` reports any `error`-severity issue on a block. **Warns but does NOT block** on `warning`-severity issues. `info`/lint hints are ignored entirely.

**Android/Kotlin** — **Blocks the push** if `kotlinc` reports any error-severity compile failure on a block. Warnings (e.g., deprecation notices) are counted but do NOT block.

**iOS/Swift** — **Blocks the push** if `swiftc` reports any error-severity compile failure on a block. Warnings are counted but do NOT block. iOS requires macOS (`swiftc`); on Linux the check reports `unavailable` (non-blocking). Phase 2.2 GitHub Actions must use macOS runners for iOS coverage.

Runner crashes (e.g., `dart` CLI not installed, Kotlin compiler not found) are **non-blocking** — infra failures shouldn't block pushes.

### Opting out per block

If a code block is intentionally illustrative (e.g., a class method body shown without its class shell), add a skip marker on the line **immediately before** the opening fence:

```mdx
{/* doc-as-test: skip (illustrative partial snippet — class method body without enclosing class) */}
```typescript
async myMethod() {
  // ...
}
```

Both HTML comment (`<!-- doc-as-test: skip -->`) and JSX comment (`{/* doc-as-test: skip */}`) styles are supported. An optional parenthetical reason is captured in the manifest for auditability.

### Scope

- **TypeScript** — 28 pages (cohort-balanced selection covering chat + social hot paths). Defined in `.docs-ops/integration-tests/pages.json`.
- **Flutter/Dart** — 29 pages (same 28 + `flutter-quick-start.mdx`). Defined in `.docs-ops/integration-tests/flutter/pages.json`.
- **Android/Kotlin** — 29 pages (same coverage as Flutter). Defined in `.docs-ops/integration-tests/android/pages.json`.
- **iOS** — 29 pages (same coverage as Android). Defined in `.docs-ops/integration-tests/ios/pages.json`. Requires macOS (`swiftc`).
- **Candidate only** — all checks run against the current working tree, not a baseline comparison.

### Running locally

```bash
# TypeScript doc-as-test (extract + type-check):
python3 .docs-ops/integration-tests/extract-blocks.py
python3 .docs-ops/integration-tests/run-tests.py
cat .docs-ops/integration-tests/results/latest.json | python3 -m json.tool

# Flutter doc-as-test (extract + analyze):
cd .docs-ops/integration-tests/flutter
dart pub get   # once, resolves amity_sdk from local path
cd -
python3 .docs-ops/integration-tests/flutter/extract-blocks.py
python3 .docs-ops/integration-tests/flutter/run-tests.py
cat .docs-ops/integration-tests/flutter/results/latest.json | python3 -m json.tool

# Android doc-as-test (extract + compile):
python3 .docs-ops/integration-tests/android/extract-blocks.py
python3 .docs-ops/integration-tests/android/run-tests.py
cat .docs-ops/integration-tests/android/results/latest.json | python3 -m json.tool

# iOS doc-as-test (extract + type-check, macOS only):
python3 .docs-ops/integration-tests/ios/extract-blocks.py
python3 .docs-ops/integration-tests/ios/run-tests.py
cat .docs-ops/integration-tests/ios/results/latest.json | python3 -m json.tool
```


## Layers of enforcement

The same `check-drift.py` script powers three layers — each one is independent, each one increases assurance:

| Layer | Where it runs | Bypassable? | Who sets up |
|---|---|---|---|
| **Local pre-push hook** | Contributor's machine on `git push` | Yes (`--no-verify`) | Each contributor, one-time |
| **GitHub Action** (`docs-ops-drift-check.yml`) | Server on every PR into `main` | No (with branch protection on) | ✅ wired |
| **Branch protection** | Server on merge | No without repo-admin role | Repo admin in GitHub UI (one toggle — see below) |

**Today (Phase 2.2)** — the GitHub Action `.github/workflows/docs-ops-drift-check.yml` runs `check-drift.py` on every PR into `main`, posts a sticky delta comment, and exits non-zero on any regression. It becomes a *merge blocker* the moment the branch-protection rule below is enabled — that toggle is the only remaining step, and it's a repo-admin action in the GitHub UI.

### What the Action enforces (coverage scope)

The Action runs on `ubuntu-latest` in **two tiers**:

**Tier 1 — always, no token, BLOCKS.** Pure Python, runs on every PR regardless of secrets:

| Check | Why |
|---|---|
| **MDX validity** (`check-mdx.py`) | unterminated code fences + unbalanced JSX tags (`Accordion`/`Tabs`/`CardGroup`/…) — i.e. **Mintlify build-breakers**. This is the layer that catches the class of bug that took down `send-a-message.mdx`. |

**Tier 2 — only when `secrets.SDK_READONLY_PAT` is configured (needs the private TS SDK), BLOCKS:**

| Check | Enforced? | Why |
|---|---|---|
| TS regex drift delta | ✅ | reads TS SDK source (sibling checkout) |
| MDX structure | ✅ | pure Python (runs inside `check-drift.py`) |
| TS doc-as-test (`tsc`) | ✅ when `tsc` is set up | best-effort node install in the job |
| Flutter / Android doc-as-test | ⚪ *unavailable* | needs `dart` / `kotlinc` |
| iOS doc-as-test | ⚪ *unavailable* | needs **macOS** + `swiftc` |

**If `SDK_READONLY_PAT` is NOT set, Tier 2 is SKIPPED with a notice in the PR comment — it does not fail the PR.** This is deliberate: a missing-secret config state is not a regression, and Tier 1 (MDX validity) still guards every PR. Add the secret to switch Tier 2 on. (The same checks run locally via the pre-push hook — see "For contributors" — where the SDK sibling is already present, so the full set runs with no token.)

Uncovered Tier-2 layers are **surfaced in the PR comment** as `unavailable` — never silently assumed green.

### Extending coverage

To enforce more platforms server-side, add toolchains to the job (and a matrix for iOS):

- **Flutter** — add a Dart/Flutter setup step (`subosito/flutter-action`) + `dart pub get` in `.docs-ops/integration-tests/flutter/`; check out the Flutter SDK sibling.
- **Android** — install a Kotlin compiler (`kotlinc`) and check out the Android SDK sibling.
- **iOS** — add a second job on `runs-on: macos-latest` (macOS runners cost ~10× ubuntu minutes — a deliberate cost decision) running only the iOS doc-as-test leg, and require it as a separate status check.

Each added platform flips its row from *unavailable* to *blocks* automatically — `check-drift.py` already orchestrates all four; it's purely a question of which toolchains the runner has.

## For contributors

**One-time setup** (after cloning):
```bash
pip install pre-commit
pre-commit install --hook-type pre-push
```

**Daily**: just `git push`. The hook runs in a few seconds against `origin/main`. If it fails, the output tells you exactly which (file, ref) pairs are new.

**Running manually** at any time:
```bash
python3 .docs-ops/ci/check-drift.py              # against origin/main
python3 .docs-ops/ci/check-drift.py --base main  # against local main
python3 .docs-ops/ci/check-drift.py --quiet      # one-line summary only
python3 .docs-ops/ci/check-drift.py --json-out /tmp/delta.json  # for tooling
```

**Bypass** (sparingly — only when you have a legitimate exception and have documented why):
```bash
git push --no-verify
```

If you find yourself wanting to bypass, please file an issue or ping #docs-ops first — it usually means either the validator has a false positive (we should fix the validator) or there's a docs change pattern the gate doesn't understand (we should update the rubric).

## For reviewers

When you review a docs PR:
- Look at the PR check status. The drift gate either passed or didn't.
- If it failed, the PR comment (from the future GH Action) will list new pairs. Don't approve until they're addressed or there's a documented bypass reason.
- If the PR resolves a lot of pairs, the comment will list those too — verify they look like real cleanups, not gaming the gate by deleting flagged code without rewriting.

## For repo admins

The Action (`.github/workflows/docs-ops-drift-check.yml`) is wired and runs on every PR into `main`. It does **not** block merges until you require it as a status check. To turn it into a real merge blocker:

1. Open one PR so the check runs at least once (GitHub only lists checks it has seen).
2. GitHub → **Settings → Branches → Branch protection rules → `main`** (add a rule if none).
3. Enable **"Require status checks to pass before merging."**
4. In the search box, add the status check named **`drift-gate`** (the job id).
5. (Recommended) also enable **"Require branches to be up to date before merging"** so the gate runs against current `main`.
6. Save.

Prerequisite: the repo secret **`SDK_READONLY_PAT`** must exist (it already does — `sdk-drift-watcher.yml` uses it). It needs read access to `AmityCo/AmityTypescriptSDK`.

After that, the gate is genuinely enforced. Contributors who bypass the local hook with `--no-verify` still get caught at PR time.
