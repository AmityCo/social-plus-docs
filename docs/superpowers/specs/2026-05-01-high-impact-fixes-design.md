# High-Impact Harness Fixes Design

**Date:** 2026-05-01  
**Status:** Approved  
**Branch:** feat/doc-agent

---

## Goal

Close three high-impact quality gaps in the social-plus-docs harness:
1. Fix 79 `DOC_MISSING` findings (renamed doc page paths in snippet files)
2. Fix 47 `ASC_PAGE_INVALID` findings (legacy full URLs in snippet files)
3. Improve TypeScript function key parity from 15% → ~40%+ (create new TS snippet files using LLM)

---

## Background

### DOC_MISSING (79 open)
Snippet files contain `sp_docs_page` values that point to paths that no longer exist in `docs.json`.
These pages **do exist** but were renamed/reorganized during a Mintlify navigation restructure.

Example:
- Old (in snippet): `social-plus-sdk/chat/messaging-features/messages/send-a-message`
- New (in docs.json): `social-plus-sdk/chat/messaging-features/message-creation/send-a-message`

The `docs.json` navigation tree contains 392 valid paths. The old paths are close matches — the last path segment is usually preserved.

### ASC_PAGE_INVALID (47 open)
Snippet files contain full legacy URLs like:
```
https://docs.amity.co/chat/android/channels/channel-management#channel-query
```
These predate the Mintlify migration. They need to be converted to relative doc paths like:
```
social-plus-sdk/chat/channels/channel-management
```

### TypeScript Parity (15%)
- 192 of 1,254 function keys have TypeScript snippets
- There are 193 dedicated `Amity*.ts` snippet files in `packages/sdk/src/` — 192 are annotated (99%)
- The gap is not missing annotations on existing files; it is **missing snippet files** for functions covered by Android/iOS/Flutter but not TypeScript
- The TS SDK source lives in `AmityTypescriptSDK/packages/sdk/src/` alongside the snippet files

---

## Task A: Path Repair Script

### File
`harness/scripts/repair-paths.py`

### What It Does

**Step 1 — Load valid paths**  
Parse `docs.json` navigation tree recursively. Collect all string values that look like relative paths (no `http`, no `#`). Result: set of ~392 valid doc paths.

**Step 2 — Build fuzzy-match index**  
For each valid path, index by last segment and by last-two-segments.

**Step 3 — Process DOC_MISSING findings**  
From `harness-report.json`, collect all `DOC_MISSING` open findings. For each:
- Exact match: if old path is already in valid set → skip (shouldn't happen but guard anyway)
- Last-segment exact match: find valid paths whose last segment equals the old path's last segment
  - If exactly 1 result → **high confidence** → patch
  - If multiple results → pick the one with the most matching intermediate segments → **medium confidence** → patch with note
  - If no match → **low confidence** → log to review report, skip

**Step 4 — Process ASC_PAGE_INVALID findings**  
From `harness-report.json`, collect all `ASC_PAGE_INVALID` open findings. For each legacy URL:
1. Strip `https://docs.amity.co/` prefix
2. Strip platform segment (`android`, `ios`, `flutter`, `typescript`) from path
3. Strip URL fragment (`#...`)
4. Try last-segment and last-two-segments fuzzy match against valid paths
5. Apply same high/medium/low confidence classification

**Step 5 — Apply patches**  
For high and medium confidence matches: open the snippet file, replace the old `sp_docs_page` value with the new path. Uses the same in-place Python replacement approach used in the Task 6 `SNIPPET_KEY_PLATFORM_CONFLICT` fix.

**Step 6 — Emit repair report**  
Write `harness/repair-report.json`:
```json
{
  "patched": [
    {"file": "...", "old": "...", "new": "...", "confidence": "high"}
  ],
  "needs_review": [
    {"file": "...", "old": "...", "candidates": [...]}
  ]
}
```

**Step 7 — Re-run audit**  
After patching, re-run `./harness-bin audit --config harness-config.yml` to verify finding counts drop. Print before/after summary.

### Success Criteria
- `DOC_MISSING` open count drops from 79 to ≤10 (low-confidence remainder)
- `ASC_PAGE_INVALID` open count drops from 47 to ≤5
- No new findings introduced (other finding counts unchanged)

---

## Task B: TypeScript Gap Filler

### Approach
New harness command `ts-fill` (registered in `cmd/main.go`), implemented in `cmd/ts_fill.go`.

Alternative: standalone script `harness/scripts/fill-ts-gaps.py`. This is simpler and avoids adding a permanent command for a one-time backfill.

**Decision: standalone script** — this is a one-time/periodic operation, not a routine command. `harness/scripts/fill-ts-gaps.py`

### What It Does

**Step 1 — Identify gaps**  
Read `function-parity.json`. Find keys where:
- TypeScript status = `unknown`
- ≥2 other platforms have status = `exists`

Sort by number of `exists` platforms descending (3-platform coverage first = highest priority).

**Step 2 — First batch**  
Process the top 30 gaps (configurable via `--batch-size`).

**Step 3 — For each gap key**
1. Find the Android reference snippet file from parity data (platform `android`, status `exists`, `file` field)
2. Read the Android snippet content as the reference example
3. Derive the expected TypeScript class/function name:  
   - Convert key `send-a-message` → `AmitySendAMessage.ts` (kebab-to-Pascal + Amity prefix)
   - Or use the key → look for matching pattern in existing TS files as a hint
4. Search TypeScript SDK source (`packages/sdk/src/`) for the relevant Repository/function using the key segments as search terms
5. Call the harness LLM (Claude, via `llm.model` config) with a structured prompt:
   ```
   Reference Android snippet: <android content>
   TypeScript SDK source for this function: <ts source excerpt>
   Key: <key>, sp_docs_page: <page from android snippet>
   
   Generate a TypeScript snippet file following the pattern of the reference.
   File must start with // @ts-nocheck and begin_sample_code block.
   Use TypeScript SDK imports (@amityco/ts-sdk).
   ```
6. Write the generated file to `AmityTypescriptSDK/packages/sdk/src/<ClassName>.ts`
7. Log: `created <filename>` or `skipped <key>: <reason>`

**Step 4 — Post-generation**  
After creating the batch:
- Re-run `harness parity --config harness-config.yml` to update `function-parity.json`
- Print new TypeScript coverage stats

### LLM Integration
Use the existing `internal/llm` package (or equivalent) already used by `annotate` command.
The prompt should include:
- System: "You are a TypeScript SDK documentation assistant. Generate minimal, correct code snippets."
- User: structured template above
- Max tokens: 500 (snippets are short)
- Temperature: 0 (deterministic)

### Success Criteria
- 30 new `Amity*.ts` files created in TypeScript snippet directory
- TypeScript parity improves from 15% to ≥25%
- Generated snippets compile (no TypeScript errors)
- `harness parity` updates `function-parity.json` with new `exists` entries

---

## Execution Order

1. Task A first (path repair) — reduces noise in findings, makes audit cleaner
2. Task B second (TS gap filler) — parity improvement on a cleaner baseline

---

## Files Created/Modified

**Task A:**
- Create: `harness/scripts/repair-paths.py`
- Modified (by script): SDK snippet files across Android, Flutter, iOS, TypeScript repos
- Create (generated): `harness/repair-report.json`

**Task B:**
- Create: `harness/scripts/fill-ts-gaps.py`
- Create (generated): up to 30 new `Amity*.ts` files in `AmityTypescriptSDK/packages/sdk/src/`
- Modified (regenerated): `harness/function-parity.json`

---

## Out of Scope

- Creating missing Mintlify doc pages (the DOC_MISSING pages that can't be fuzzy-matched)
- CI integration (separate initiative)
- Gate 3 automation
- UIKit snippet coverage
