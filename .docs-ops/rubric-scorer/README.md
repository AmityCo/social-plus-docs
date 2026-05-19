# Rubric Scorer

Agent-as-judge harness for scoring doc pages on the 6-dimension quality rubric in `.docs-ops/rubric.json`.

## Design: agent-as-judge

The LLM doing the scoring **is the running agent** (Copilot CLI, Claude Code, or any future agent). No API keys. No SDK dependencies. The agent reads prompt files and writes score files — exactly the same protocol as `.docs-ops/tasks/`.

## Three-phase workflow

```
Phase 1 — PREPARE  (deterministic, run by script)
  python3 prepare.py --dimension clarity
  → writes results/pending/<dimension>-<slug>.json per page
     { page, cohort, prompt, prompt_hash, ... }
  (pending/ is gitignored — regenerable)

Phase 2 — SCORE  (agent does this)
  Agent reads each results/pending/<dimension>-<slug>.json
  Scores using its own judgment against the rubric in the prompt
  Writes results/scored/<dimension>-<slug>.json
     { page, cohort, score, rationale, confidence, suggestions,
       _prompt_hash, _scored_by, _scored_at }
  (scored/ is committed — audit trail)

Phase 3 — COLLECT  (deterministic, run by script)
  python3 collect.py --dimension clarity
  → reads all scored/<dimension>-*.json
  → writes results/<dimension>-latest.json
  python3 render-report.py --dimension clarity
  → writes results/<dimension>-latest-report.md
```

**Full run (Copilot CLI example):**
```sh
cd social-plus-docs/
python3 .docs-ops/rubric-scorer/prepare.py --dimension clarity
# → agent reads pending/ files and writes scored/ files (this step is the agent)
python3 .docs-ops/rubric-scorer/collect.py --dimension clarity --archive
python3 .docs-ops/rubric-scorer/render-report.py --dimension clarity
cat .docs-ops/rubric-scorer/results/clarity-latest-report.md
```

## File layout

```
.docs-ops/rubric-scorer/
  prepare.py                 ← Phase 1: renders prompt files into results/pending/
  collect.py                 ← Phase 3: aggregates scored/ into latest.json
  render-report.py           ← renders latest.json → latest-report.md
  pages-pilot.json           ← 10 pilot pages (cohort-balanced)
  prompts/
    clarity.md               ← Clarity prompt template ({page_content} placeholder)
    # future: completeness.md, parity.md, examples.md, ai-consumability.md
  results/
    pending/                 ← GITIGNORED — prompt files for agent to score
    scored/                  ← COMMITTED  — agent's scores (audit trail)
    history/                 ← COMMITTED  — archived dated snapshots
    clarity-latest.json      ← aggregated scores (committed)
    clarity-latest-report.md ← rendered report (committed)
```

## Scored file schema (agent writes this)

```json
{
  "dimension": "clarity",
  "page": "social-plus-sdk/...",
  "cohort": "eastern",
  "score": 3,
  "rationale": "<one sentence citing specific evidence>",
  "confidence": "low|medium|high",
  "suggestions": ["<actionable improvement>"],
  "_prompt_hash": "<sha256 of the prompt the agent saw>",
  "_scored_by": "copilot-cli",
  "_scored_at": "2026-05-19T..."
}
```

The `_prompt_hash` lets future runs detect if the prompt template or page content changed between scoring rounds — important for calibration consistency.

## Adding a new dimension

1. Copy `prompts/clarity.md` to `prompts/<dimension>.md`
2. Replace the rubric section with the new dimension's 1-5 levels from `rubric.json`
3. Run `prepare.py --dimension <name>`, score, `collect.py --dimension <name>`

## Pilot scope

10 pages, cohort-balanced:
- 4 **Eastern** (chat-heavy): send-a-message, query-channels, query-and-filter-messages, flag-unflag-a-message
- 4 **Western** (social-heavy): file, image-handling, update-user-information, query-posts
- 2 **Shared** (universal): authentication, get-user-information

## Prompt design principles

- Rubric levels quoted **verbatim** from `rubric.json` — the rubric IS the contract.
- Conservative by default: when unsure, score lower.
- Rationale must cite specific evidence (section/line/quote).
- Suggestions must be actionable within 30 minutes.
- Strict JSON response format for reliable parsing.

## Future plans

- Score remaining 5 dimensions once Clarity is calibrated
- Extend beyond pilot to all ~300 doc pages
- Trend tracking: compare `_prompt_hash` across runs to detect calibration drift
- CI gate integration (after calibration confidence is established)
