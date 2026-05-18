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

- **iOS / Android / Flutter validators**: those extractors still have known noise (`.shared` not captured on iOS; internal types leak on Android; no public marker on Flutter). They run for informational purposes but don't gate. We'll expand the gate as those validators mature.
- **Prose, structure, IA**: the gate is API-accuracy-only. The 6-dimension rubric is broader; per-PR scoring is a future addition.
- **SDK changes**: the gate compares docs against the SDK surface AS COMMITTED in this repo. When the upstream SDK changes, someone must re-run the extractor and commit the new `sdk-surface/*.json`. A separate workflow (TBD) will detect SDK changes and open docs PRs to update.

## Doc-as-test layer

In addition to the regex-based drift check, the gate runs a **doc-as-test** step that type-checks TypeScript code blocks from the top-traffic doc pages against the real `@amityco/ts-sdk` source using `tsc --noEmit --strict`.

### What it catches (and what the regex validator misses)

| Problem type | Regex validator | Doc-as-test |
|---|---|---|
| Stale API name (renamed method) | ✓ catches | ✓ catches |
| Wrong argument type | ✗ misses | ✓ catches |
| Missing required argument | ✗ misses | ✓ catches |
| Wrong async/await pattern | ✗ misses | ✓ catches |
| Broken syntax (copy-paste error) | ✗ misses | ✓ catches |

### Gate policy

**Blocks the push** if any failure contains a `TS2xxx` error — these are TypeScript type errors indicating real API drift (wrong property, wrong argument type, incompatible return type).

**Warns but does NOT block** on `TS1xxx`-only errors — these are parser errors that occur in intentionally partial/illustrative code examples. Keeping these non-blocking prevents the gate from becoming high-friction for pedagogical content.

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

- **TypeScript only** (v1) — iOS/Android/Flutter doc-as-test is out of scope until those platforms have comparable coverage.
- **Top 28 pages** — cohort-balanced selection (chat-heavy Eastern + social-heavy Western customer hot paths), covering ~80% of code-path traffic. Defined in `.docs-ops/integration-tests/pages.json`.
- **Candidate only** — doc-as-test runs against the current working tree, not a baseline comparison. Any TS2xxx in the candidate blocks, regardless of baseline state.

### Running locally

```bash
# Full doc-as-test run (extract + type-check):
python3 .docs-ops/integration-tests/extract-blocks.py
python3 .docs-ops/integration-tests/run-tests.py

# Read the report:
cat .docs-ops/integration-tests/results/latest.json | python3 -m json.tool
```


## Layers of enforcement

The same `check-drift.py` script powers three layers — each one is independent, each one increases assurance:

| Layer | Where it runs | Bypassable? | Who sets up |
|---|---|---|---|
| **Local pre-push hook** | Contributor's machine on `git push` | Yes (`--no-verify`) | Each contributor, one-time |
| **GitHub Action** (final step, not yet wired) | Server on every PR | No (without branch protection edit) | Repo admin |
| **Branch protection** (final step) | Server on merge | No without repo-admin role | Repo admin in GitHub UI |

**Today (Phase 2.1)** — local layer is live. Awareness depends on contributors running `pre-commit install`.

**Next (Phase 2.2)** — GitHub Action will call the same script in CI, post the delta as a PR comment, and (with branch protection enabled) block merges. At that point local enforcement is best-effort; server enforcement is the true gate.

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

Once you're happy with the local layer, enable the server layer:

1. Wire `.github/workflows/docs-ops-drift-check.yml` (TBD — Phase 2.2).
2. In GitHub → Settings → Branches → branch protection rule for `main` → require status check `docs-ops-drift-check` to pass before merge.

After that, the gate is genuinely enforced. Contributors who bypass locally still get caught at PR time.
