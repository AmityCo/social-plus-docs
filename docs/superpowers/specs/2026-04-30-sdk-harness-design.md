# SDK Documentation Harness — Design Spec

**Date:** 2026-04-30  
**Status:** Approved  
**Phase:** 1 — Local harness (CI/CD extensibility by design)

---

## Problem

The social.plus docs can become incorrect in two independent ways:

1. **Written wrong at the start** — a doc page is authored with incorrect method names, wrong behavioral descriptions, or missing gotchas
2. **Drift after SDK changes** — a doc page was correct when written but the SDK evolves (renamed methods, new parameters, new functions added) and the doc silently falls behind

Both failure modes need to be addressed. Surface errors (wrong method names, wrong params) can be auto-fixed. Behavioral errors (wrong description of what a function does) require human judgment.

---

## Approach: Snippet-Driven Harness

The four SDKs (Android/Kotlin, iOS/Swift, Flutter/Dart, TypeScript) all contain curated, compilable code snippets with structured metadata:

```
/* begin_sample_code
   gist_id: 8d0f4f0da7500573cd67be5fe3d1bd2c
   filename: play_a_livestream.swift
   asc_page: https://docs.amity.co/amity-sdk/video/ios/view-play
   description: Play a livestream
*/
```

These snippets:
- Compile against the real SDK (ground truth for API surface)
- Have `asc_page` links to the exact doc page they correspond to
- Are organized by feature area matching the doc structure

The snippets are used as the source of truth — not raw SDK internals, which are complex and language-specific. A snippet that compiles is proof the API call is valid. A snippet with an `asc_page` link is a direct mapping to the doc page that must describe it.

---

## Architecture

Two pipelines run sequentially:

```
Pipeline 1: Coverage
  SDK source (public API) ──► Coverage Checker ──► MISSING_SNIPPET findings

Pipeline 2: Correctness  
  Snippet manifest (asc_page) ──► Drift Detector ──► DOC_SURFACE_DRIFT / DOC_MISSING findings
```

Both pipelines write into a single `harness-report.json`. The fix command reads this report, resolves what it can, and the loop repeats until the report is clean.

### The Iteration Loop

```
audit → harness-report.json
          ↓ (findings exist)
         fix → resolves findings, writes harness-issues.md for human-review items
          ↓
audit → harness-report.json (fewer findings each pass)
          ↓
         fix → ...
          ↓
audit → ✅ zero open findings = done
```

---

## Commands

```bash
# Step 1: Detect everything wrong
go run ./harness/cmd/main.go audit

# Step 2: Fix what can be fixed automatically
go run ./harness/cmd/main.go fix

# Repeat until clean
```

### `audit` command (fully computational, deterministic)

1. Runs public API extractor per platform → function manifest
2. Scans existing snippets → snippet manifest (method calls + `asc_page` links)
3. Diffs the two → three finding categories:
   - `MISSING_SNIPPET` — public function exists, no snippet covers it
   - `DOC_MISSING` — snippet has `asc_page` but that doc page doesn't exist
   - `DOC_SURFACE_DRIFT` — snippet method name doesn't appear in the linked doc page
4. For findings with `status: fixed` — re-verifies evidence chain (see Evidence Chain section)
5. Writes `harness-report.json`
6. Exits non-zero if any `open` findings exist (CI/CD extension point)

### `fix` command (inferential + computational validation)

1. Reads `harness-report.json`, processes `open` findings
2. For `MISSING_SNIPPET`: AI generates snippet → compile check validates → writes to SDK snippet dir → seals evidence
3. For `DOC_SURFACE_DRIFT`: AI rewrites affected MDX section → MDX structural check → seals evidence
4. For `DOC_MISSING` and behavioral issues: writes to `harness-issues.md` with `status: needs_human`
5. Updates `harness-report.json` with new statuses and evidence bundles

---

## Finding Lifecycle

```
open → (fix runs) → fixed    (evidence sealed, re-verified by next audit)
                 → needs_human  (written to harness-issues.md, excluded from loop)
```

`needs_human` findings do not block loop termination. They are the intentional human review gate.

---

## `harness-report.json` Schema

```json
{
  "generated_at": "2026-04-30T13:45:00+07:00",
  "summary": {
    "open": 12,
    "fixed": 3,
    "needs_human": 2
  },
  "findings": [
    {
      "id": "android-chat-AmityMessageRepository.deleteMessage",
      "type": "MISSING_SNIPPET",
      "platform": "android",
      "function": "AmityMessageRepository.deleteMessage()",
      "status": "open"
    },
    {
      "id": "flutter-channel-create-community-communityType",
      "type": "DOC_SURFACE_DRIFT",
      "platform": "flutter",
      "snippet_file": "code_snippet/channel/amity_channel_creation_community.dart",
      "doc_page": "social-plus-sdk/chat/conversation-management/channels/create-channel.mdx",
      "detail": "snippet calls `communityType()` but doc page has no mention of it",
      "status": "fixed",
      "evidence": {
        "before_hash": "sha256:a1b2c3...",
        "after_hash": "sha256:d4e5f6...",
        "artifact": "social-plus-sdk/chat/conversation-management/channels/create-channel.mdx",
        "compile_result": "PASS",
        "compile_output_hash": "sha256:g7h8i9..."
      }
    }
  ]
}
```

---

## Evidence Chain (Tamper-Proof Verification)

The AI agent cannot mark a finding `fixed` by assertion. Every fix must produce a cryptographic evidence bundle. The `audit` command re-verifies this bundle on every run.

### Three proofs required

| Claim | Proof |
|-------|-------|
| "I wrote the artifact" | `SHA256(file on disk)` must equal `evidence.after_hash` |
| "It compiles" | Compile command re-runs; output hash must match `evidence.compile_output_hash` |
| "The doc was updated" | `SHA256(doc page)` must differ from `evidence.before_hash` |

### Seal (called by `fix`)

```
verifier.Seal(finding, artifactPath):
  1. Compute SHA256 of artifact file content
  2. Run platform compile command
  3. Compute SHA256 of compile stdout+stderr
  4. If compile result != PASS → finding stays "open"
  5. If PASS → write evidence bundle, set status "fixed"
```

### Verify (called by `audit` on re-run)

```
verifier.Verify(finding):
  1. Recompute SHA256 of artifact on disk
  2. Compare against evidence.after_hash
  3. Re-run compile command
  4. Compare output hash against evidence.compile_output_hash
  5. Any mismatch → reset status to "open"
```

This means: the AI cannot hallucinate a fix, silently revert a change, or skip the compile step. Every claimed fix is independently verifiable by anyone running `audit`.

---

## Go Tool Structure

Lives at `social-plus-docs/harness/` — same pattern as `llmstxt/`.

```
harness/
  cmd/main.go
  harness-config.yml
  internal/
    config/        # Parse harness-config.yml
    extractor/     # Per-platform public API surface extraction
      android.go       # Regex: public fun in Amity*Repository classes
      ios.go           # Regex: public func in AmitySDK classes  
      flutter.go       # Regex: non-_ methods in Amity* public classes
      typescript.go    # Parse index.ts export* statements
    scanner/       # Scan begin_sample_code blocks → snippet manifest
      scanner.go
    differ/        # API surface vs snippet manifest → findings
      differ.go
    verifier/      # Evidence chain: Seal + Verify
      verifier.go
    compiler/      # Platform-specific compile validation
      android.go       # ./gradlew amity-sample-code:compileDebugKotlin
      flutter.go       # dart analyze code_snippet/
      typescript.go    # npx tsc --noEmit
      ios.go           # xcodebuild -scheme SDKSampleCode build
    generator/     # AI: generate missing snippet
      generator.go
    fixer/         # AI: fix doc surface drift in MDX
      fixer.go
    report/        # Read/write harness-report.json + harness-issues.md
      report.go
```

### `harness-config.yml`

```yaml
sdks:
  android:
    path: ../../Amity-Social-Cloud-SDK-Android
    snippet_dir: amity-sample-code/src/main/java/com/amity/snipet/verifier
    compile_cmd: ["./gradlew", "amity-sample-code:compileDebugKotlin"]
  flutter:
    path: ../../Amity-Social-Cloud-SDK-Flutter-Internal
    snippet_dir: code_snippet
    compile_cmd: ["dart", "analyze", "code_snippet/"]
  typescript:
    path: ../../AmityTypescriptSDK
    snippet_dir: packages/sdk/src
    compile_cmd: ["npx", "tsc", "--noEmit"]
  ios:
    path: ../../AmitySDKIOS
    snippet_dir: SDKSampleCode/SDKSampleCode
    compile_cmd: ["xcodebuild", "-scheme", "SDKSampleCode", "build"]
docs:
  path: ../
llm:
  model: claude-sonnet-4-6
```

### Extractor design

Extractors are regex-based, not full AST parsers. All 4 SDKs follow consistent naming conventions (`Amity*Repository`, `Amity*Client`). Regex is fast, zero dependencies, and handles the public API surface reliably. Any missed function will surface on the next audit cycle.

---

## Output Files

| File | Written by | Purpose |
|------|-----------|---------|
| `harness-report.json` | `audit` | Machine-readable findings + evidence chain |
| `harness-issues.md` | `fix` | Human-readable items requiring manual attention |

---

## CI/CD Extension (Phase 2)

The `audit` command already exits non-zero when open findings exist. No changes to the tool are needed for CI integration:

```yaml
# .github/workflows/sdk-harness.yml (Phase 2)
- name: Audit SDK documentation
  run: go run ./harness/cmd/main.go audit --fail-on-findings
```

Phase 2 additions (out of scope for Phase 1):
- Post `harness-report.json` as PR comment
- Open GitHub Issues from `needs_human` findings automatically
- Run on SDK repo webhooks (trigger when SDK commit detected)

---

## What is NOT in scope (Phase 1)

- Automatic PR creation (local fix only)
- GitHub Issues from `needs_human` items (manual review via `harness-issues.md`)
- Full AST parsing of SDK internals (regex extractors only)
- Mathematical formal verification (evidence chain provides content-addressed verification, not logical proof)
- UIKit snippet coverage (SDK snippets only for Phase 1)
