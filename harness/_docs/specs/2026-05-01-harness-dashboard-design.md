# Harness Dashboard — Design Spec
**Date:** 2026-05-01  
**Status:** Approved

---

## Problem

The harness runs AI agents and scripts across 8 commands and 4 SDK repos. There is no visibility into what is running, what has completed, or what the current finding state is — unless you read raw JSON files or watch terminal output. Teams sharing a harness instance have no shared view.

## Goal

A web dashboard — served by the harness binary itself — that shows:
1. **Pipeline status**: which command is running, which have completed, which are queued
2. **Live activity**: sub-steps within the current command, stdout tail, SCRIPT vs AI AGENT type
3. **Findings**: open/fixed/needs_human counts broken down by platform and finding type

Near-real-time via polling (3s interval). No websockets, no external dependencies.

---

## Architecture

### New command: `harness serve`

```
./harness-bin serve --config harness-config.yml [--port 8765] [--report harness-report.json]
```

Starts an HTTP server on `localhost:8765` (configurable). Serves:

| Route | Description |
|---|---|
| `GET /` | Dashboard HTML (embedded via `go:embed`) |
| `GET /api/report` | Returns `harness-report.json` as-is |
| `GET /api/run` | Returns `harness-run.json` (current pipeline state) |

CORS headers included so the dashboard can be opened as `file://` too.  
Server exits cleanly on Ctrl-C. Intended to run in a second terminal alongside the harness pipeline.

### New package: `internal/runstate`

Manages `harness-run.json` — atomic writes (write to `.tmp` then rename).

```go
// harness-run.json structure
type RunState struct {
    SessionID      string    `json:"session_id"`       // random hex, reset each new session
    StartedAt      string    `json:"started_at"`
    CurrentCommand string    `json:"current_command"`  // "" if idle
    Steps          []Step    `json:"steps"`
}

type Step struct {
    Command    string  `json:"command"`
    Type       string  `json:"type"`        // "script" | "ai_agent"
    Model      string  `json:"model,omitempty"` // set for ai_agent steps
    Status     string  `json:"status"`      // "running" | "done" | "failed" | "idle"
    StartedAt  string  `json:"started_at,omitempty"`
    FinishedAt string  `json:"finished_at,omitempty"`
    DurationMs int64   `json:"duration_ms,omitempty"`
    Summary    string  `json:"summary,omitempty"`  // e.g. "81 patches, 11 skipped"
    Substeps   []Substep `json:"substeps,omitempty"`
}

type Substep struct {
    Label  string `json:"label"`
    Detail string `json:"detail,omitempty"`
    Status string `json:"status"` // "done" | "running" | "waiting" | "failed"
}
```

**API:**
- `runstate.Start(cfgDir, command, stepType, model)` — writes step with `status: running`
- `runstate.UpdateSubstep(cfgDir, command, substep)` — appends/updates a substep in the current step  
- `runstate.Finish(cfgDir, command, summary)` — sets `status: done`, records duration
- `runstate.Fail(cfgDir, command, errMsg)` — sets `status: failed`

### Instrumentation in existing commands

Each `cmd/*.go` gets 3 calls — Start at top, Finish/Fail at end:

| Command | Type | Notes |
|---|---|---|
| `audit` | `script` | Summary: "X findings, Y new" |
| `annotate` | `script` | Summary: "X patches, Y applied" |
| `fix` | `ai_agent` | Model from config |
| `gendocs` | `ai_agent` | Model from config |
| `genmanifests` | `script` | |
| `fillmanifests` | `script` | |
| `migrate` | `script` | |
| `prompt` | `script` | |

Sub-steps are optional. `audit` and `annotate` emit them (they have distinct phases). Others just emit Start/Finish.

### Dashboard HTML (`cmd/dashboard.html`)

Embedded with `//go:embed dashboard.html`. Single HTML file, no build step, no framework.

**Layout:** Two-column
- **Left (main):** Pipeline strip → Findings summary bar → Platform breakdown (4 cards) → Open findings table
- **Right (sidebar):** Live Activity panel — currently-running step card with sub-steps + stdout tail + type badge

**Polling:** `setInterval` every 3s hits `/api/run` and `/api/report`. Pauses when `document.hidden` (tab in background). Shows "last updated Xs ago" in topbar.

**Visual differentiation:**
- `script` steps: blue accent (`#58a6ff`), `SCRIPT` badge
- `ai_agent` steps: purple accent (`#c084fc`), `🤖 AI AGENT` badge + model name shown

**Step states:** `idle` (greyed) → `running` (pulsing glow) → `done` (green border) → `failed` (red border)

**No persistence:** The dashboard only reads the two JSON files. Run history is not tracked (out of scope for v1).

---

## Harness Tasks Integration

`harness prompt` generates `harness-tasks.md` — the task file that AI agents (and humans) follow when running the pipeline. `harness serve` is added as **Step 0** in that file so anyone executing the pipeline can open the dashboard and watch progress in real-time.

`prompt.go` emits this block at the top of the task file, before any other steps:

```markdown
## Step 0 — Start Dashboard (optional but recommended)

Run in a separate terminal before starting any other steps:

    ./harness-bin serve --config harness-config.yml

Then open http://localhost:8765 to watch pipeline progress live.
The dashboard auto-refreshes every 3 seconds.
You may skip this step if running headlessly.
```

The dashboard URL and port are included so a human reviewer can open it immediately. The step is marked optional so automated/CI runs aren't blocked if no browser is available.

---

## Data Flow

```
[harness audit]  →  runstate.Start()  →  harness-run.json
                     ... work ...
                 →  runstate.Finish() →  harness-run.json

[harness serve]  →  GET /api/run      →  reads harness-run.json → dashboard JS
                 →  GET /api/report   →  reads harness-report.json → dashboard JS
                 ← polls every 3s ←
```

---

## Files Changed / Created

| File | Change |
|---|---|
| `cmd/serve.go` | NEW — `runServe`, HTTP handlers, `go:embed` |
| `cmd/dashboard.html` | NEW — full dashboard (HTML/CSS/JS, no build step) |
| `cmd/main.go` | Add `serve` case |
| `internal/runstate/runstate.go` | NEW — Start/UpdateSubstep/Finish/Fail, atomic writes |
| `internal/runstate/runstate_test.go` | NEW — tests for state transitions, concurrent writes |
| `cmd/audit.go` | Add runstate.Start/Finish + 4 sub-step emits |
| `cmd/annotate.go` | Add runstate.Start/Finish + 3 sub-step emits |
| `cmd/fix.go` | Add runstate.Start/Finish (ai_agent type) |
| `cmd/gendocs.go` | Add runstate.Start/Finish (ai_agent type) |
| `cmd/genmanifests.go` | Add runstate.Start/Finish |
| `cmd/fillmanifests.go` | Add runstate.Start/Finish |
| `cmd/prompt.go` | Add Step 0 `harness serve` block at top of generated task file |
| `cmd/migrate.go` | Add runstate.Start/Finish |
| `cmd/prompt.go` | Add runstate.Start/Finish |

---

## Out of Scope (v1)

- Run history / trend charts (no `harness-runs/` archive)
- Authentication (localhost-only, no auth needed)
- WebSocket live streaming
- Filtering/searching the findings table
- Dark/light mode toggle (dark only)

---

## Testing

- `internal/runstate`: unit tests for Start→Finish lifecycle, concurrent write safety (atomic rename), Fail path
- `cmd/serve.go`: handler tests for `/api/report` (file not found, valid JSON), `/api/run` (same)
- Dashboard HTML: manual smoke test — `harness serve` then open browser, run `harness audit` in another terminal and confirm pipeline card updates within 3s
