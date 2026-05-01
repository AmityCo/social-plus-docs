# Harness Validation Framework Design

**Date:** 2026-05-01  
**Status:** Approved  
**Scope:** Cross-platform snippet coverage validation pipeline

---

## Problem

The harness generates SDK documentation snippets from annotated source files across four platforms (Android, iOS, Flutter, TypeScript). Two failure modes exist that are hard to detect:

1. **Structural failures** (broken imports, syntax errors, missing pages) — detectable today by `audit`
2. **Semantic failures** (LLM assigns a Flutter function to the wrong doc page) — currently undetected

A third category exists: features genuinely absent from a platform, or doc pages that need to be created. These require ground truth that no automated system currently provides.

Coverage snapshot at design time:
- Android: 52% of snippet keys covered
- iOS: 47%
- Flutter: 37%
- TypeScript: 18%

87 keys exist in Android+iOS but have no Flutter snippet. The gap is not missing Flutter annotations (Flutter has only 38 unannotated functions) — it's that Flutter SDK has different or absent sample files for those features.

---

## Architecture: Three-Gate Pipeline

```
SDK Source Files
      │
      ▼
[Gate 1: Computational]  ← CI-enforced, binary pass/fail
      │
      ▼
[Gate 2: Inferential + Oracle]  ← LLM proposes, Gate 1 validates
      │
      ▼
[Gate 3: Human Triage]  ← Ground truth (automatable in the future)
```

Each gate's output feeds the next. Gate 1 serves as the oracle that validates Gate 2 output.

---

## Gate 1: Computational (CI-enforced)

**What it checks (deterministic, always binary pass/fail):**

| Finding Type | Description |
|---|---|
| `DOC_BROKEN_IMPORT` | MDX page imports a snippet file that doesn't exist |
| `DOC_PAGE_STALE_IMPORT` | MDX page is missing an import for a snippet it should have |
| `MINTLIFY_SYNTAX_ERROR` | MDX file has a parse error (e.g. imports before frontmatter) |
| `DOC_MISSING` | Snippet references a doc page not in `docs.json` |
| `PUBLIC_FUNC_UNANNOTATED` | SDK public function has no `sp_docs_page` annotation |
| `SNIPPET_KEY_PLATFORM_CONFLICT` | *(new)* Same key, different `sp_docs_page` across platforms |

**New finding: `SNIPPET_KEY_PLATFORM_CONFLICT`**

Added to `differ.go`. For each snippet key with ≥2 platforms, if any two platforms have different `sp_docs_page` values, this finding fires with detail showing the conflict:

```
key "post-semantic-search" — android→social/.../intelligent-search-post, ios→social/.../intelligent-search-post ✓
key "ad-query" — android→social/.../notification-items, ios→core-concepts/.../ads ✗ CONFLICT
```

This fires before `gendocs` runs, catching the root cause (conflicting SDK annotations) rather than the downstream symptom. The deterministic sort in `GroupSnippets` (android→ios→flutter→typescript) means `gendocs` silently picks android's page — this finding surfaces the conflict so it can be resolved in the SDK source.

**CI gate:** `audit` must report `0 open` findings. Any open finding blocks merge.

---

## Gate 2: Inferential + Computational Oracle

**What it does:** LLM (`annotate` command) suggests `sp_docs_page` for unannotated or unmatched functions. Gate 1 then re-runs as the oracle.

**Confidence signal (key alignment):**

| Condition | Confidence | Action |
|---|---|---|
| LLM assigns page → Gate 1 passes → key matches sibling platform key | High | Auto-approve |
| LLM assigns page → Gate 1 passes → no sibling exists to confirm | Medium | Flag for Gate 3 review |
| LLM assigns page → `SNIPPET_KEY_PLATFORM_CONFLICT` fires | Low | Route to Gate 3 |
| Gate 1 fails after LLM annotation | Invalid | Reject, re-annotate |

**Flutter coverage gap workflow:**

1. Run `annotate --platform flutter` on unannotated or new snippet files
2. LLM suggests `sp_docs_page` using Android/iOS sibling context
3. Run `gendocs` → `audit` (Gate 1 oracle)
4. Evaluate confidence signal:
   - Key matches existing sibling → high confidence → commit
   - Conflict or no sibling → Gate 3

**Invariant:** Gate 2 output is only accepted if Gate 1 reports 0 open findings after applying it.

---

## Gate 3: Human Triage (automatable later)

**Current state (human):**

Findings routed here have status `needs_human` in `harness-report.json`. A human resolves each by choosing:
- Reassign `sp_docs_page` in the SDK source file
- Create a new doc page for the feature
- Mark as N/A for this platform (feature genuinely absent)

**Current `needs_human` volume:**
- `ASC_PAGE_INVALID`: 49 (sp_docs_page points to non-existent page)
- `DOC_MISSING`: 65 (snippet references page not in docs.json nav)
- `PUBLIC_FUNC_UNANNOTATED`: 11 (functions with no annotation)

**Future automation path:**

Gate 3 can become an LLM agent with:
1. Input: conflict context + existing doc page content + SDK function signature
2. Decision: reassign, create page, or mark N/A
3. Output: structured patch (SDK annotation change + optional new MDX page)
4. Validation: patch runs through Gate 1 — if 0 open, auto-merge

The interface between Gate 3 and Gate 1 is already clean. Gate 3 just needs to produce valid SDK annotations and doc pages that pass Gate 1. No changes to Gate 1 are required to enable this.

---

## Data Flow

```
SDK .kt/.swift/.dart/.ts files
  │  [sp_docs_page annotations]
  ▼
scanner.go → Snippet{}
  │
  ▼  [Gate 2: annotate adds missing sp_docs_page]
GroupSnippets() (deterministic: android→ios→flutter→ts)
  │
  ▼
gendocs → snippets/*.mdx + manifest.json
  │
  ▼  [Gate 1: differ.go checks all finding types including SNIPPET_KEY_PLATFORM_CONFLICT]
audit → harness-report.json
  │
  ├─ 0 open → ✅ pipeline passes
  └─ open findings → route to Gate 2 (inferential) or Gate 3 (human/future-auto)
```

---

## Coverage Tracking

Coverage metrics (per-platform snippet percentage) are computed and surfaced in the dashboard. They are **informational, not gating** — a platform at 37% is not a CI failure. The goal is to track improvement over time as Gate 2 and Gate 3 work closes gaps.

Coverage is meaningful only for keys where the SDK feature actually exists on that platform. Keys where a platform has no implementation should not count against coverage (Gate 3 marks them N/A).

---

## Implementation Notes

- `SNIPPET_KEY_PLATFORM_CONFLICT` is added to `differ.go` alongside existing `DiffDocPages`
- The `annotate` command already supports per-platform annotation; Gate 2 workflow is operational, just needs the confidence signal logic
- Gate 3 automation requires no Gate 1 changes — it's an additive LLM agent layer
- The deterministic sort in `GroupSnippets` (already implemented) is a prerequisite for Gate 1's `SNIPPET_KEY_PLATFORM_CONFLICT` to be meaningful (without it, the "winner" is random)
