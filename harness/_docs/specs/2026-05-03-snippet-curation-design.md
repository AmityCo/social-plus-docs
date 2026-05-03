# Snippet Curation & Annotation QA Gate — Design Spec

**Date:** 2026-05-03  
**Status:** Approved  
**Scope:** `harness curate` command (Phase 2B) + `harness annotate --qa` gate (Phase 2B+)

---

## Problem

The current `place` command dumps all snippets whose `asc_page` annotation matches a page — without asking whether each snippet is genuinely relevant, whether it's redundant with another already on the page, or which section it belongs in.

This produces two symptoms:

1. **Wrong-page placements** — functions annotated to the wrong page appear inline in irrelevant sections. Example: `PostApprove`, `ProductGet`, `PostIsFlaggedByMe` placed on `edit-post.mdx`.

2. **Variant flooding** — many platform-specific functions (all correctly annotated) are dumped as a raw list after "Related Topics" with no curation. Example: 50+ reaction snippets (`PostLike`, `StoryLike`, `ReactToAComment`, etc.) appended after the structured content on `reactions.mdx`, despite the page already covering the concept clearly in named sections.

Neither is a bug in placement mechanics — the snippets match. The system lacks an LLM reasoning pass to ask: *"Is this snippet actually useful here, and if so, where?"*

---

## Solution Overview

Two additions to the pipeline:

```
annotate  →  [annotate --qa gate]  →  audit  →  place  →  [harness curate]
```

- **`harness curate`** (Phase 2B, immediate): post-placement LLM pass that reviews each page's placed snippets, decides KEEP/REMOVE/MOVE/FLAG per snippet with confidence gating, and applies high-confidence decisions.
- **`annotate --qa`** (Phase 2B+, wired into annotate): a second LLM check at annotation time that validates each `asc_page` assignment against the target page's prose. Emits non-blocking findings for suspect annotations.

---

## Approach A: `harness curate` Command

### Inputs per page

- Page MDX prose (stripped of import/component lines — LLM sees intent, not boilerplate)
- Per placed snippet: name, platform, and rendered code content
- Page section headings (extracted `##` headings to anchor KEEP decisions)

### LLM Prompt

```
Page: social-plus-sdk/core-concepts/content-handling/reactions
Sections: [## Query Reactions, ## Add / Remove Reactions, ## Common Reaction Types, ## Best Practices, ## Related Topics]
Purpose (prose): [first 800 chars of page prose]

Placed snippets:
  1. ReactToAComment — flutter — [code]
  2. PostLike — android — [code]
  ...

For each snippet return a JSON array element:
{
  "name": "ReactToAComment",
  "action": "KEEP" | "REMOVE" | "MOVE" | "FLAG",
  "section": "## Add / Remove Reactions",  // if KEEP
  "target_page": "...",                     // if MOVE
  "reason": "one sentence",
  "confidence": "high" | "medium" | "low"
}
```

### Confidence-Gated Auto-Apply

| Action | Confidence | Behavior |
|--------|-----------|----------|
| KEEP | any | Auto-applied; snippet tag moved to correct `##` section if needed |
| REMOVE | high | Auto-removed from MDX (import + component tag) |
| REMOVE | medium / low | Written to `curate-review.json` for human approval |
| MOVE | high | Removed from this page; `SNIPPET_CURATED_MOVED` finding created pointing at target page |
| MOVE | medium / low | Written to `curate-review.json` |
| FLAG | any | Always written to `curate-review.json` |

### Output Artifacts

- **Modified MDX files** — auto-applied decisions only
- **`curate-review.json`** — all FLAG and low/medium-confidence decisions with reasoning, ready for human approval
- **`harness-report.json`** — three new finding types:
  - `SNIPPET_CURATED_REMOVED` — snippet was removed with high confidence
  - `SNIPPET_CURATED_MOVED` — snippet removed from this page, should be placed on target page
  - `SNIPPET_CURATION_FLAGGED` — needs human review

### CLI

```bash
# Curate all pages
harness curate --config harness-config.yml

# Curate a single page
harness curate --config harness-config.yml --page social-plus-sdk/core-concepts/content-handling/reactions

# Dry-run: print decisions and write curate-review.json, but don't touch MDX
harness curate --config harness-config.yml --dry-run
```

### Re-sectioning

When a KEEP snippet is placed in the wrong section (e.g., dumped at the bottom when it belongs under `## Add Reaction`), `curate` moves the `<Component />` tag to the first position after the target section heading. The import is left at the top of the file (already correct). This is the primary fix for the "dumped after Related Topics" pattern.

### Safe Defaults

- LLM call fails for a page → page is skipped entirely, warning logged, no MDX modified
- MDX parse fails → skip that page, emit `SNIPPET_CURATION_FLAGGED` finding
- `--dry-run` → write `curate-review.json`, print all decisions, touch no MDX

---

## Approach B: `annotate --qa` Gate

### Purpose

Fix the annotation root cause: after `harness annotate` assigns `asc_page` to a function, a second LLM pass validates the assignment against the actual page prose. This prevents wrong-page placements from being created in the first place.

### Trigger

Opt-in via `--qa` flag on `harness annotate`. Existing annotation runs without `--qa` are unaffected.

```bash
harness annotate --qa --config harness-config.yml
```

### Inputs per function

- Function signature + existing `asc_page` annotation
- First 500 words of prose from the target page file (fetched from docs repo path)

### LLM Prompt

```
Function: addReaction(referenceId, referenceType, reactionName)
Annotated page: social-plus-sdk/core-concepts/content-handling/reactions
Page summary: [first 500 words of page prose]

Does this function's behavior clearly belong on this page?
{
  "match": true | false,
  "confidence": "high" | "medium" | "low",
  "reason": "one sentence",
  "suggested_page": "..."   // optional, if match=false and LLM can infer better page
}
```

### Finding Types

| Outcome | Finding |
|---------|---------|
| `match: false, confidence: high` | `ANNOTATION_SUSPECT` — with suggested_page if available |
| `match: false/true, confidence: medium/low` | `ANNOTATION_UNCERTAIN` — informational only |
| `match: true, confidence: high` | No finding |

Both finding types are **non-blocking** (Gate 2, not Gate 1). They surface for human triage.

### Safe Defaults

- LLM fails → emit `ANNOTATION_UNCERTAIN`, never hard-fail
- Target page not found → skip QA for that function, log warning

---

## Data Flow

```
SDK source
    │
    ▼
harness annotate [--qa]
    │  writes: begin_public_function annotations with asc_page
    │  [--qa]: emits ANNOTATION_SUSPECT / ANNOTATION_UNCERTAIN findings
    ▼
harness audit
    │  writes: harness-report.json (MISSING_SNIPPET, PUBLIC_FUNC_UNANNOTATED, etc.)
    ▼
harness place
    │  writes: MDX files with snippet imports + component tags placed
    ▼
harness curate [--dry-run]
    │  reads: MDX + snippet content
    │  writes: modified MDX, curate-review.json, new findings in harness-report.json
    ▼
harness serve
    └  dashboard shows curate findings + review queue
```

---

## New Packages

### `internal/curator`

Responsibilities:
- Parse MDX: extract prose, section headings, existing snippet component tags
- Build LLM request per page
- Parse LLM response (JSON array of decisions)
- Apply decisions: remove import/tag, move tag to section, write curate-review.json
- Emit findings

Key types:
```go
type Decision struct {
    Name       string
    Action     CurateAction  // Keep, Remove, Move, Flag
    Section    string        // target ## heading (if Keep)
    TargetPage string        // target page slug (if Move)
    Reason     string
    Confidence Confidence    // High, Medium, Low
}

type CurateResult struct {
    Page      string
    Applied   []Decision
    Flagged   []Decision
}
```

### No new package for annotate --qa

The QA gate is implemented as an additional function in the existing `cmd/annotate.go`, calling into `internal/llm` (or existing prompt infrastructure). No new internal package needed.

---

## Testing

### `internal/curator`

- Unit tests with mock LLM responses (no real API calls)
- Table-driven cases:
  - All-KEEP page: MDX unchanged, no curate-review.json written
  - All-REMOVE (high confidence): all imports + tags removed, findings emitted
  - Mixed confidence: high auto-applied, medium/low go to review file
  - MOVE cross-page: removed from current page, finding created
  - Dry-run: review file written, MDX untouched
  - LLM failure: page skipped, no MDX change
  - Re-sectioning: KEEP snippet moved from bottom to correct `##` section

### `cmd/curate.go`

- Integration test: real MDX with 5 placed snippets, mock LLM, verify output MDX + review file

### `annotate --qa`

- Unit test: mock page content + mock LLM returning suspect/clean/uncertain
- Verify correct finding types emitted, no hard-fail on LLM error

---

## Rollout Sequence

1. Implement `internal/curator` + `cmd/curate.go` with full test coverage
2. Wire `harness curate` into `main.go`
3. Run `harness curate --dry-run` across all pages → review `curate-review.json`
4. Apply approved decisions from review file
5. Wire `--qa` gate into `harness annotate` (separate PR)
6. Run `harness annotate --qa` on changed SDK files as part of incremental delta flow
