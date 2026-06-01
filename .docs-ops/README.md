# .docs-ops — Multi-agent docs improvement protocol

This directory is the coordination surface between AI agents (Claude, Copilot CLI, future agents) working on the social.plus docs. **File-based, no orchestrator.** Agents claim work by atomic rename and drop results back as JSON.

> **Source-of-truth boundary:** `sdk-surface/*` is the *factual* layer (machine-extracted SDK symbols) — **regenerate it, never hand-edit it.** The *opinion* layer (enforced SDK best-practices) lives in the Vise repo (`social-plus-foundry`), not here. The full facts-vs-opinion ownership map — what each source owns and which way truth flows on a conflict — is in Vise's `docs/ARCHITECTURE.md` → "Sources of Truth".

## Layout

```
.docs-ops/
  README.md                  ← this file
  AGENT_PROMPT.md            ← paste-into-agent brief explaining the protocol
  rubric.json                ← scoring rubric (6 dimensions × 5 levels). Single source of truth.
  glossary.json              ← canonical terms (generated; not yet present)
  sdk-surface/               ← parsed public API surfaces per SDK (generated; not yet present)
    ios.json
    android.json
    typescript.json
    flutter.json
  schemas/
    task.schema.json         ← JSON schema for a task
    result.schema.json       ← JSON schema for a task result
    score.schema.json        ← JSON schema for a per-page rubric score
  tasks/
    pending/                 ← unclaimed task files
    in_progress/             ← claimed (filename includes agent_id + claimed_at)
    done/                    ← completed; contains result blob alongside original task
    failed/                  ← needs human triage; contains failure reason
  evals/
    scores.jsonl             ← append-only rubric scores, one JSON object per line
    parity-matrix.json       ← cross-platform parity report (generated)
```

## How agents work

**Claim**: `mv tasks/pending/<id>.json tasks/in_progress/<id>.<agent_id>.<unix_ts>.json`. The rename is atomic on a POSIX filesystem — if two agents race, only one wins. The loser sees its source file gone and moves on.

**Execute**: Read the task JSON. Do the work. Write changes to the target files. Run the `success_criteria.validators` listed in the task — these are shell commands that exit 0 on pass.

**Report**: Write `tasks/done/<id>.result.json` matching `schemas/result.schema.json`. Move the in-progress task alongside it (`tasks/done/<id>.json`). If validators fail and you can't fix it, move to `tasks/failed/` with `failure_reason` populated.

**Don't**:
- Don't open a PR. A separate batcher script (see `scripts/`, not yet present) groups successful results into PRs by section.
- Don't touch files outside `target_files` unless the task explicitly says you may.
- Don't modify `rubric.json`, `glossary.json`, or `sdk-surface/*` from a task — those are inputs.

## Division of labor (current)

| Agent | Owns |
|-------|------|
| **Claude** | Rubric scoring, SDK-grounding analysis, task generation (writing the JSON specs), Tier B/C planning, IA decisions, anything needing deep cross-file context |
| **Copilot CLI** | Tier A workhorse — burns through high-volume mechanical task files, one fix at a time |

Tiers are defined in `rubric.json` under `fix_tiers`.

## Pilot scope

First pilot section: `social-plus-sdk/getting-started/` (7 pages, ~3200 lines). Once the protocol holds up here we generalize.

## CI gate — keeping the cleanup durable

See [CI_GATE.md](CI_GATE.md) for the drift-regression check that gates pushes (and, in a follow-up phase, PRs). One-time contributor setup:

```bash
pip install pre-commit
pre-commit install --hook-type pre-push
```

After that, every `git push` is compared against `origin/main` and blocked if it introduces new (file, API-ref) pairs to the drift report.
