# Harness Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a `harness serve` command that serves a live web dashboard showing pipeline step status (SCRIPT vs AI AGENT), sub-step progress, stdout tail, and findings breakdown — all polled every 3s from `harness-run.json` and `harness-report.json`.

**Architecture:** A new `internal/runstate` package atomically manages `harness-run.json`; each existing command calls `runstate.Start`/`Finish` to record its state. A new `cmd/serve.go` starts an HTTP server serving an embedded `cmd/dashboard.html` plus two JSON API endpoints. The dashboard is vanilla HTML/CSS/JS with no build step — embedded at compile time via `go:embed`.

**Tech Stack:** Go 1.23 stdlib (`net/http`, `embed`, `encoding/json`), `testify` for tests (already in go.mod), vanilla HTML/CSS/JS for dashboard.

**Spec:** `harness/_docs/specs/2026-05-01-harness-dashboard-design.md`

---

## File Map

| File | Action | Responsibility |
|---|---|---|
| `internal/runstate/runstate.go` | CREATE | RunState/Step/Substep types + Start/Finish/Fail/UpdateSubstep/Read (atomic writes) |
| `internal/runstate/runstate_test.go` | CREATE | Unit tests for all runstate functions |
| `cmd/serve.go` | CREATE | `runServe` HTTP handler, `/`, `/api/run`, `/api/report`, `go:embed` |
| `cmd/dashboard.html` | CREATE | Full dashboard HTML/CSS/JS (two-column, polls every 3s) |
| `cmd/serve_test.go` | CREATE | Handler tests for all three routes |
| `cmd/main.go` | MODIFY | Add `serve` case to switch + update usage string |
| `cmd/audit.go` | MODIFY | Add `runstate.Start` / `runstate.Finish` with sub-step emits |
| `cmd/annotate.go` | MODIFY | Add `runstate.Start` / `runstate.Finish` with sub-step emits |
| `cmd/fix.go` | MODIFY | Add `runstate.Start` / `runstate.Finish` (ai_agent type) |
| `cmd/gendocs.go` | MODIFY | Add `runstate.Start` / `runstate.Finish` (ai_agent type) |
| `cmd/genmanifests.go` | MODIFY | Add `runstate.Start` / `runstate.Finish` |
| `cmd/fillmanifests.go` | MODIFY | Add `runstate.Start` / `runstate.Finish` |
| `cmd/migrate.go` | MODIFY | Add `runstate.Start` / `runstate.Finish` |
| `cmd/prompt.go` | MODIFY | Emit Step 0 `harness serve` block at top of generated `harness-tasks.md` |

---

## Task 1: `internal/runstate` package

**Files:**
- Create: `internal/runstate/runstate.go`
- Create: `internal/runstate/runstate_test.go`

- [ ] **Step 1.1: Write failing tests for RunState types and Start/Finish lifecycle**

```go
// internal/runstate/runstate_test.go
package runstate_test

import (
	"encoding/json"
	"os"
	"path/filepath"
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"

	"social-plus/harness/internal/runstate"
)

func TestStartCreatesFile(t *testing.T) {
	dir := t.TempDir()
	err := runstate.Start(dir, "audit", "script", "")
	require.NoError(t, err)

	path := filepath.Join(dir, "harness-run.json")
	_, err = os.Stat(path)
	assert.NoError(t, err, "harness-run.json should exist after Start")
}

func TestStartSetsRunningStatus(t *testing.T) {
	dir := t.TempDir()
	require.NoError(t, runstate.Start(dir, "audit", "script", ""))

	state, err := runstate.Read(dir)
	require.NoError(t, err)
	require.Len(t, state.Steps, 1)
	assert.Equal(t, "audit", state.Steps[0].Command)
	assert.Equal(t, "running", state.Steps[0].Status)
	assert.Equal(t, "script", state.Steps[0].Type)
	assert.Equal(t, "audit", state.CurrentCommand)
}

func TestStartAIAgentSetsModel(t *testing.T) {
	dir := t.TempDir()
	require.NoError(t, runstate.Start(dir, "gendocs", "ai_agent", "claude-sonnet-4-6"))

	state, err := runstate.Read(dir)
	require.NoError(t, err)
	assert.Equal(t, "ai_agent", state.Steps[0].Type)
	assert.Equal(t, "claude-sonnet-4-6", state.Steps[0].Model)
}

func TestFinishSetsDoneAndDuration(t *testing.T) {
	dir := t.TempDir()
	require.NoError(t, runstate.Start(dir, "audit", "script", ""))
	time.Sleep(5 * time.Millisecond) // ensure nonzero duration
	require.NoError(t, runstate.Finish(dir, "audit", "92 findings"))

	state, err := runstate.Read(dir)
	require.NoError(t, err)
	require.Len(t, state.Steps, 1)
	assert.Equal(t, "done", state.Steps[0].Status)
	assert.Equal(t, "92 findings", state.Steps[0].Summary)
	assert.Greater(t, state.Steps[0].DurationMs, int64(0))
	assert.Empty(t, state.CurrentCommand)
}

func TestFailSetsFailedStatus(t *testing.T) {
	dir := t.TempDir()
	require.NoError(t, runstate.Start(dir, "fix", "ai_agent", "claude-sonnet-4-6"))
	require.NoError(t, runstate.Fail(dir, "fix", "LLM timeout"))

	state, err := runstate.Read(dir)
	require.NoError(t, err)
	assert.Equal(t, "failed", state.Steps[0].Status)
	assert.Equal(t, "LLM timeout", state.Steps[0].Summary)
	assert.Empty(t, state.CurrentCommand)
}

func TestUpdateSubstepAddsSubstep(t *testing.T) {
	dir := t.TempDir()
	require.NoError(t, runstate.Start(dir, "audit", "script", ""))
	require.NoError(t, runstate.UpdateSubstep(dir, "audit", runstate.Substep{
		Label: "scan android", Detail: "203 functions", Status: "done",
	}))

	state, err := runstate.Read(dir)
	require.NoError(t, err)
	require.Len(t, state.Steps[0].Substeps, 1)
	assert.Equal(t, "scan android", state.Steps[0].Substeps[0].Label)
	assert.Equal(t, "done", state.Steps[0].Substeps[0].Status)
}

func TestUpdateSubstepUpdatesExisting(t *testing.T) {
	dir := t.TempDir()
	require.NoError(t, runstate.Start(dir, "audit", "script", ""))
	require.NoError(t, runstate.UpdateSubstep(dir, "audit", runstate.Substep{
		Label: "scan android", Status: "running",
	}))
	require.NoError(t, runstate.UpdateSubstep(dir, "audit", runstate.Substep{
		Label: "scan android", Detail: "203 functions", Status: "done",
	}))

	state, err := runstate.Read(dir)
	require.NoError(t, err)
	require.Len(t, state.Steps[0].Substeps, 1, "should update in place, not append")
	assert.Equal(t, "done", state.Steps[0].Substeps[0].Status)
	assert.Equal(t, "203 functions", state.Steps[0].Substeps[0].Detail)
}

func TestMultipleCommandsAccumulate(t *testing.T) {
	dir := t.TempDir()
	require.NoError(t, runstate.Start(dir, "audit", "script", ""))
	require.NoError(t, runstate.Finish(dir, "audit", "92 findings"))
	require.NoError(t, runstate.Start(dir, "annotate", "script", ""))

	state, err := runstate.Read(dir)
	require.NoError(t, err)
	require.Len(t, state.Steps, 2)
	assert.Equal(t, "done", state.Steps[0].Status)
	assert.Equal(t, "running", state.Steps[1].Status)
	assert.Equal(t, "annotate", state.CurrentCommand)
}

func TestReadReturnsEmptyWhenNoFile(t *testing.T) {
	dir := t.TempDir()
	state, err := runstate.Read(dir)
	require.NoError(t, err)
	assert.Empty(t, state.Steps)
	assert.Empty(t, state.CurrentCommand)
}
```

- [ ] **Step 1.2: Run tests to verify they fail**

```bash
cd harness && go test ./internal/runstate/... -v 2>&1 | head -20
```
Expected: compilation error — package `runstate` does not exist yet.

- [ ] **Step 1.3: Implement `internal/runstate/runstate.go`**

```go
// internal/runstate/runstate.go
package runstate

import (
	"crypto/rand"
	"encoding/hex"
	"encoding/json"
	"os"
	"path/filepath"
	"time"
)

const filename = "harness-run.json"

// RunState is the top-level structure written to harness-run.json.
type RunState struct {
	SessionID      string  `json:"session_id"`
	StartedAt      string  `json:"started_at"`
	CurrentCommand string  `json:"current_command"`
	Steps          []Step  `json:"steps"`
}

// Step represents one harness command execution.
type Step struct {
	Command    string    `json:"command"`
	Type       string    `json:"type"`                 // "script" | "ai_agent"
	Model      string    `json:"model,omitempty"`      // set for ai_agent
	Status     string    `json:"status"`               // "running"|"done"|"failed"|"idle"
	StartedAt  string    `json:"started_at,omitempty"`
	FinishedAt string    `json:"finished_at,omitempty"`
	DurationMs int64     `json:"duration_ms,omitempty"`
	Summary    string    `json:"summary,omitempty"`
	Substeps   []Substep `json:"substeps,omitempty"`
}

// Substep is a named phase within a Step.
type Substep struct {
	Label  string `json:"label"`
	Detail string `json:"detail,omitempty"`
	Status string `json:"status"` // "done"|"running"|"waiting"|"failed"
}

// Read loads harness-run.json from dir. Returns empty RunState (no error) if file absent.
func Read(dir string) (RunState, error) {
	data, err := os.ReadFile(filepath.Join(dir, filename))
	if os.IsNotExist(err) {
		return RunState{}, nil
	}
	if err != nil {
		return RunState{}, err
	}
	var state RunState
	if err := json.Unmarshal(data, &state); err != nil {
		return RunState{}, err
	}
	return state, nil
}

// Start records that command has begun. Appends to existing steps (preserves prior runs in session).
func Start(dir, command, stepType, model string) error {
	state, err := Read(dir)
	if err != nil {
		return err
	}
	if state.SessionID == "" {
		b := make([]byte, 8)
		_, _ = rand.Read(b)
		state.SessionID = hex.EncodeToString(b)
		state.StartedAt = time.Now().Format(time.RFC3339)
	}
	state.CurrentCommand = command
	state.Steps = append(state.Steps, Step{
		Command:   command,
		Type:      stepType,
		Model:     model,
		Status:    "running",
		StartedAt: time.Now().Format(time.RFC3339),
	})
	return write(dir, state)
}

// Finish marks command as done with an optional summary message.
func Finish(dir, command, summary string) error {
	return updateStep(dir, command, func(s *Step) {
		now := time.Now()
		s.Status = "done"
		s.Summary = summary
		s.FinishedAt = now.Format(time.RFC3339)
		if t, err := time.Parse(time.RFC3339, s.StartedAt); err == nil {
			s.DurationMs = now.Sub(t).Milliseconds()
		}
	})
}

// Fail marks command as failed with an error message in Summary.
func Fail(dir, command, errMsg string) error {
	return updateStep(dir, command, func(s *Step) {
		now := time.Now()
		s.Status = "failed"
		s.Summary = errMsg
		s.FinishedAt = now.Format(time.RFC3339)
		if t, err := time.Parse(time.RFC3339, s.StartedAt); err == nil {
			s.DurationMs = now.Sub(t).Milliseconds()
		}
	})
}

// UpdateSubstep adds or updates a named substep within command's current Step.
// Matches by Label — updates in place if found, appends otherwise.
func UpdateSubstep(dir, command string, sub Substep) error {
	return updateStep(dir, command, func(s *Step) {
		for i, existing := range s.Substeps {
			if existing.Label == sub.Label {
				s.Substeps[i] = sub
				return
			}
		}
		s.Substeps = append(s.Substeps, sub)
	})
}

// updateStep finds the most recent Step for command and applies fn to it.
func updateStep(dir, command string, fn func(*Step)) error {
	state, err := Read(dir)
	if err != nil {
		return err
	}
	// Find last step matching command
	idx := -1
	for i := len(state.Steps) - 1; i >= 0; i-- {
		if state.Steps[i].Command == command {
			idx = i
			break
		}
	}
	if idx < 0 {
		return nil // no matching step — silently skip
	}
	fn(&state.Steps[idx])
	// Clear CurrentCommand when step is terminal
	if state.Steps[idx].Status == "done" || state.Steps[idx].Status == "failed" {
		if state.CurrentCommand == command {
			state.CurrentCommand = ""
		}
	}
	return write(dir, state)
}

// write atomically writes state to harness-run.json using a temp file + rename.
func write(dir string, state RunState) error {
	data, err := json.MarshalIndent(state, "", "  ")
	if err != nil {
		return err
	}
	tmp := filepath.Join(dir, filename+".tmp")
	if err := os.WriteFile(tmp, data, 0o644); err != nil {
		return err
	}
	return os.Rename(tmp, filepath.Join(dir, filename))
}
```

- [ ] **Step 1.4: Run tests and verify all pass**

```bash
cd harness && go test ./internal/runstate/... -v
```
Expected: all 9 tests pass, output ends with `ok  social-plus/harness/internal/runstate`.

- [ ] **Step 1.5: Commit**

```bash
cd harness
git add internal/runstate/
git commit -m "feat(runstate): new package — atomic pipeline state tracking

Manages harness-run.json with Start/Finish/Fail/UpdateSubstep/Read.
Atomic writes via .tmp+rename to avoid partial reads by the dashboard.
9 tests covering all state transitions and substep upsert logic."
```

---

## Task 2: `cmd/serve.go` + `cmd/dashboard.html`

**Files:**
- Create: `cmd/serve.go`
- Create: `cmd/dashboard.html`
- Create: `cmd/serve_test.go`
- Modify: `cmd/main.go`

- [ ] **Step 2.1: Write failing handler tests**

```go
// cmd/serve_test.go
package main

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"os"
	"path/filepath"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestServeReport_ReturnsJSON(t *testing.T) {
	dir := t.TempDir()
	payload := `{"generated_at":"2026-05-01T00:00:00Z","findings":[]}`
	require.NoError(t, os.WriteFile(filepath.Join(dir, "harness-report.json"), []byte(payload), 0o644))

	h := reportHandler(dir)
	rec := httptest.NewRecorder()
	h.ServeHTTP(rec, httptest.NewRequest("GET", "/api/report", nil))

	assert.Equal(t, http.StatusOK, rec.Code)
	assert.Equal(t, "application/json", rec.Header().Get("Content-Type"))
	var got map[string]any
	require.NoError(t, json.Unmarshal(rec.Body.Bytes(), &got))
	assert.Equal(t, "2026-05-01T00:00:00Z", got["generated_at"])
}

func TestServeReport_NotFound_Returns200Empty(t *testing.T) {
	dir := t.TempDir() // no harness-report.json
	h := reportHandler(dir)
	rec := httptest.NewRecorder()
	h.ServeHTTP(rec, httptest.NewRequest("GET", "/api/report", nil))
	assert.Equal(t, http.StatusOK, rec.Code)
	assert.JSONEq(t, `{}`, rec.Body.String())
}

func TestServeRun_ReturnsJSON(t *testing.T) {
	dir := t.TempDir()
	payload := `{"session_id":"abc","current_command":"audit","steps":[]}`
	require.NoError(t, os.WriteFile(filepath.Join(dir, "harness-run.json"), []byte(payload), 0o644))

	h := runHandler(dir)
	rec := httptest.NewRecorder()
	h.ServeHTTP(rec, httptest.NewRequest("GET", "/api/run", nil))

	assert.Equal(t, http.StatusOK, rec.Code)
	var got map[string]any
	require.NoError(t, json.Unmarshal(rec.Body.Bytes(), &got))
	assert.Equal(t, "audit", got["current_command"])
}

func TestServeRun_NotFound_Returns200Empty(t *testing.T) {
	dir := t.TempDir()
	h := runHandler(dir)
	rec := httptest.NewRecorder()
	h.ServeHTTP(rec, httptest.NewRequest("GET", "/api/run", nil))
	assert.Equal(t, http.StatusOK, rec.Code)
	assert.JSONEq(t, `{}`, rec.Body.String())
}

func TestServeDashboard_Returns200(t *testing.T) {
	// The dashboard handler serves the embedded dashboard.html
	rec := httptest.NewRecorder()
	dashboardHandler().ServeHTTP(rec, httptest.NewRequest("GET", "/", nil))
	assert.Equal(t, http.StatusOK, rec.Code)
	assert.Contains(t, rec.Header().Get("Content-Type"), "text/html")
}
```

- [ ] **Step 2.2: Run tests to verify they fail**

```bash
cd harness && go test ./cmd/... -run "TestServe" -v 2>&1 | head -20
```
Expected: compilation errors — `reportHandler`, `runHandler`, `dashboardHandler` not defined.

- [ ] **Step 2.3: Create `cmd/dashboard.html`**

Create the full dashboard as a single HTML file. It must be self-contained (no external CDN dependencies — all CSS and JS inline). Key behaviors:
- Two-column layout: left = pipeline + findings, right sidebar = live activity
- Polls `/api/run` and `/api/report` every 3 seconds via `fetch`
- Pauses polling when `document.hidden`
- Shows SCRIPT (blue) vs AI AGENT (purple) badges
- Step states: idle (greyed) → running (pulsing border) → done (green) → failed (red)
- Substeps in sidebar with spinner on running step
- Stdout tail in sidebar (last 5 lines from `step.substeps` detail fields)

```html
<!-- cmd/dashboard.html -->
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Harness Dashboard</title>
<style>
/* ── Reset & base ─────────────────────────────────── */
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:#0d1117;color:#e6edf3;font-size:13px}
code{font-family:'SF Mono','Fira Code',monospace;font-size:11px}

/* ── Topbar ───────────────────────────────────────── */
.topbar{background:#161b22;border-bottom:1px solid #30363d;padding:10px 24px;display:flex;align-items:center;justify-content:space-between}
.topbar .logo{font-weight:700;font-size:15px;color:#58a6ff}
.topbar .meta{color:#7d8590;font-size:11px;display:flex;align-items:center;gap:6px}
.pulse{width:7px;height:7px;background:#3fb950;border-radius:50%;animation:pulse 2s infinite;display:inline-block}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}

/* ── Layout ───────────────────────────────────────── */
.layout{display:grid;grid-template-columns:1fr 340px;min-height:calc(100vh - 41px)}
.main-col{padding:20px 24px;border-right:1px solid #21262d;overflow-y:auto}
.side-col{padding:16px;overflow-y:auto}
h2{font-size:11px;font-weight:600;color:#7d8590;text-transform:uppercase;letter-spacing:.5px;margin-bottom:10px}

/* ── Pipeline strip ───────────────────────────────── */
.pipeline{display:flex;gap:6px;margin-bottom:24px;overflow-x:auto;padding-bottom:4px}
.step{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:10px 12px;min-width:110px;flex-shrink:0;transition:border-color .3s}
.step.done{border-color:#238636}
.step.running{border-color:#58a6ff;background:#1a2332;animation:glow 1.5s ease-in-out infinite}
.step.ai-running{border-color:#c084fc;background:#1a1227;animation:glow-ai 1.5s ease-in-out infinite}
.step.failed{border-color:#da3633;background:#1a0000}
.step.idle{opacity:.45}
@keyframes glow{0%,100%{box-shadow:none}50%{box-shadow:0 0 8px rgba(88,166,255,.3)}}
@keyframes glow-ai{0%,100%{box-shadow:none}50%{box-shadow:0 0 8px rgba(192,132,252,.3)}}
.step-name{font-weight:600;font-size:11px;margin-bottom:3px}
.step-badge{font-size:9px;font-weight:700;padding:1px 5px;border-radius:8px;display:inline-block;margin-bottom:5px}
.b-done{background:#1a3a23;color:#3fb950}.b-run{background:#1a2e4a;color:#58a6ff}
.b-ai{background:#2d1a3a;color:#c084fc}.b-idle{background:#21262d;color:#555}
.b-failed{background:#3a1a1a;color:#f85149}
.step-summary{font-size:9px;color:#7d8590;line-height:1.3}
.step-time{font-size:9px;color:#444;margin-top:3px}
.arrow{color:#30363d;font-size:14px;align-self:center;flex-shrink:0}

/* ── Summary bar ──────────────────────────────────── */
.sumbar{display:flex;gap:10px;margin-bottom:20px}
.sc{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:12px 16px;flex:1}
.sc .n{font-size:24px;font-weight:700}.sc .l{font-size:10px;color:#7d8590;margin-top:1px}
.n-o{color:#d29922}.n-f{color:#3fb950}.n-h{color:#f0883e}

/* ── Platform cards ───────────────────────────────── */
.plats{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:22px}
.plat{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:10px}
.ph{display:flex;align-items:center;gap:5px;margin-bottom:8px}
.pi{width:16px;height:16px;border-radius:3px;display:flex;align-items:center;justify-content:center;font-size:9px;font-weight:700}
.ic-android{background:#1c3a2a;color:#3fb950}.ic-ios{background:#2a2a3a;color:#a0a8d8}
.ic-flutter{background:#1a2e4a;color:#58a6ff}.ic-typescript{background:#1a2e3a;color:#3b82f6}
.pn{font-size:11px;font-weight:600}
.pr{display:flex;justify-content:space-between;margin-bottom:3px;font-size:10px;color:#7d8590}
.pr span:last-child{font-weight:600;color:#e6edf3}
.pbar{height:2px;background:#21262d;border-radius:2px;margin-top:6px;overflow:hidden}
.pf{height:100%;border-radius:2px}

/* ── Findings table ───────────────────────────────── */
.ftable{background:#161b22;border:1px solid #30363d;border-radius:8px;overflow:hidden;margin-bottom:8px}
.ftable table{width:100%;border-collapse:collapse}
.ftable th{background:#1c2128;color:#7d8590;font-size:10px;font-weight:600;padding:7px 10px;text-align:left;border-bottom:1px solid #30363d}
.ftable td{padding:6px 10px;border-bottom:1px solid #21262d;font-size:10px}
.ftable tr:last-child td{border-bottom:none}
.tag{font-size:9px;padding:1px 6px;border-radius:8px;font-weight:600}
.to{background:#2d2208;color:#d29922}.tn{background:#2d1f10;color:#f0883e}.tf{background:#1a3a23;color:#3fb950}

/* ── Sidebar activity card ────────────────────────── */
.act-card{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:12px;margin-bottom:14px}
.act-card.script-running{border-color:#58a6ff;background:#1a2332;box-shadow:0 0 12px rgba(88,166,255,.1)}
.act-card.ai-running{border-color:#c084fc;background:#1a1227;box-shadow:0 0 12px rgba(192,132,252,.1)}
.act-card.idle-card{opacity:.6}
.rh{display:flex;align-items:center;gap:6px;margin-bottom:10px;flex-wrap:wrap}
.rh-title{font-weight:700;font-size:13px}
.rh-badge{font-size:9px;font-weight:700;padding:1px 6px;border-radius:8px}
.rb-script{background:#1a2e4a;color:#58a6ff}.rb-ai{background:#2d1a3a;color:#c084fc}
.rb-done{background:#1a3a23;color:#3fb950}.rb-idle{background:#21262d;color:#7d8590}
.type-s{background:#1a2a1a;color:#4ade80;font-size:9px;font-weight:700;padding:1px 6px;border-radius:8px}
.type-a{background:#2d1a3a;color:#c084fc;font-size:9px;font-weight:700;padding:1px 6px;border-radius:8px}
.pdot{width:6px;height:6px;border-radius:50%;flex-shrink:0}
.pdot.s{background:#58a6ff;animation:pulse 1.5s infinite}
.pdot.a{background:#c084fc;animation:pulse 1.5s infinite}
.substeps{border-left:2px solid #30363d;padding-left:10px;margin-bottom:10px}
.ss{display:flex;align-items:flex-start;gap:6px;padding:4px 0;border-bottom:1px solid #21262d}
.ss:last-child{border-bottom:none}
.ss-ic{font-size:11px;flex-shrink:0;margin-top:1px}
.ss-info{flex:1}
.ss-label{font-size:11px;font-weight:500}
.ss-meta{font-size:9px;color:#7d8590;margin-top:1px}
.sst{font-size:9px;padding:1px 5px;border-radius:6px;white-space:nowrap}
.sst-d{background:#1a3a23;color:#3fb950}.sst-r{background:#1a2e4a;color:#58a6ff}
.sst-ra{background:#2d1a3a;color:#c084fc}.sst-w{background:#21262d;color:#555}
.sst-f{background:#3a1a1a;color:#f85149}
.spin{display:inline-block;animation:spin 1s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
.section-lbl{font-size:9px;font-weight:600;color:#7d8590;text-transform:uppercase;letter-spacing:.5px;margin:8px 0 4px}
.log-tail{background:#010409;border:1px solid #21262d;border-radius:5px;padding:8px 10px;font-family:'SF Mono','Fira Code',monospace;font-size:10px;line-height:1.6;max-height:90px;overflow:hidden;position:relative}
.log-tail::after{content:'';position:absolute;bottom:0;left:0;right:0;height:24px;background:linear-gradient(transparent,#010409)}
.ll{color:#7d8590}.ll.ok{color:#3fb950}.ll.info{color:#58a6ff}.ll.ai{color:#c084fc}
.idle-msg{color:#7d8590;font-size:11px;padding:8px 0}
</style>
</head>
<body>

<div class="topbar">
  <div class="logo">⚙ Social Plus Harness</div>
  <div class="meta" id="meta"><span class="pulse"></span> connecting…</div>
</div>

<div class="layout">
  <div class="main-col">
    <h2>Pipeline</h2>
    <div class="pipeline" id="pipeline">
      <div style="color:#7d8590;font-size:11px;padding:10px 0">Waiting for run data…</div>
    </div>

    <h2>Findings</h2>
    <div class="sumbar" id="sumbar">
      <div class="sc"><div class="n" style="color:#555">—</div><div class="l">Open</div></div>
      <div class="sc"><div class="n" style="color:#555">—</div><div class="l">Fixed</div></div>
      <div class="sc"><div class="n" style="color:#555">—</div><div class="l">Needs human</div></div>
    </div>

    <div class="plats" id="plats"></div>

    <h2>Open Findings</h2>
    <div class="ftable">
      <table>
        <thead><tr><th>Type</th><th>Platform</th><th>Detail</th><th>Status</th></tr></thead>
        <tbody id="findings-body"><tr><td colspan="4" style="color:#7d8590;text-align:center;padding:16px">No report loaded</td></tr></tbody>
      </table>
    </div>
  </div>

  <div class="side-col">
    <h2>Live Activity</h2>
    <div id="activity"><div class="idle-msg">No active command</div></div>
  </div>
</div>

<script>
const COMMANDS = ['audit','annotate','fix','gendocs','genmanifests','fillmanifests','migrate','prompt'];
const AI_COMMANDS = new Set(['fix','gendocs']);
const PLATFORM_COLORS = {
  android:  {icon:'An', cls:'ic-android',  bar:'linear-gradient(90deg,#238636,#3fb950)'},
  ios:      {icon:'iOS',cls:'ic-ios',       bar:'linear-gradient(90deg,#4040a0,#a0a8d8)'},
  flutter:  {icon:'Fl', cls:'ic-flutter',   bar:'linear-gradient(90deg,#1a5a9a,#58a6ff)'},
  typescript:{icon:'TS',cls:'ic-typescript',bar:'linear-gradient(90deg,#1a3a5a,#3b82f6)'},
};

let lastUpdated = null;
let hidden = false;
document.addEventListener('visibilitychange', () => { hidden = document.hidden; });

function timeSince(ms) {
  const s = Math.round((Date.now() - ms) / 1000);
  return s < 2 ? 'just now' : s + 's ago';
}

function fmtDuration(ms) {
  if (!ms) return '';
  if (ms < 1000) return ms + 'ms';
  return Math.round(ms / 1000) + 's';
}

// ── Pipeline rendering ───────────────────────────────
function renderPipeline(run) {
  const stepMap = {};
  (run.steps || []).forEach(s => { stepMap[s.command] = s; });

  let html = '';
  COMMANDS.forEach((cmd, i) => {
    const s = stepMap[cmd];
    const status = s ? s.status : 'idle';
    const isAI = (s && s.type === 'ai_agent') || AI_COMMANDS.has(cmd);
    const isRunning = status === 'running';
    let cls = 'step ' + status;
    if (isRunning && isAI) cls = 'step ai-running';
    else if (isRunning) cls = 'step running';

    let badge = '', badgeCls = '';
    if (status === 'done')    { badge = 'done';  badgeCls = 'b-done'; }
    else if (isRunning && isAI) { badge = '🤖 ai agent'; badgeCls = 'b-ai'; }
    else if (isRunning)       { badge = 'running'; badgeCls = 'b-run'; }
    else if (status === 'failed') { badge = 'failed'; badgeCls = 'b-failed'; }
    else if (isAI)            { badge = '🤖 ai agent'; badgeCls = 'b-ai'; }
    else                      { badge = 'idle'; badgeCls = 'b-idle'; }

    const summary = s ? (s.summary || '') : '';
    const dur = s ? fmtDuration(s.duration_ms) : '';
    const timeStr = dur ? dur + (s.finished_at ? ' · ' + s.finished_at.slice(11,16) : '') : '';

    html += `<div class="${cls}">
      <div class="step-name">${cmd}</div>
      <div class="step-badge ${badgeCls}">${badge}</div>
      <div class="step-summary">${summary || '—'}</div>
      ${timeStr ? `<div class="step-time">${timeStr}</div>` : ''}
    </div>`;
    if (i < COMMANDS.length - 1) html += '<div class="arrow">›</div>';
  });
  document.getElementById('pipeline').innerHTML = html;
}

// ── Findings rendering ───────────────────────────────
function renderFindings(report) {
  const findings = report.findings || [];
  const summary = report.summary || {};
  const open = summary.open ?? findings.filter(f => f.status === 'open').length;
  const fixed = summary.fixed ?? findings.filter(f => f.status === 'fixed').length;
  const needsHuman = summary.needs_human ?? findings.filter(f => f.status === 'needs_human').length;

  document.getElementById('sumbar').innerHTML = `
    <div class="sc"><div class="n n-o">${open}</div><div class="l">Open</div></div>
    <div class="sc"><div class="n n-f">${fixed}</div><div class="l">Fixed this run</div></div>
    <div class="sc"><div class="n n-h">${needsHuman}</div><div class="l">Needs human</div></div>`;

  // Platform breakdown
  const byPlat = {};
  findings.forEach(f => {
    const p = f.platform || (f.id || '').split(':')[1] || 'unknown';
    if (!byPlat[p]) byPlat[p] = {open:0,fixed:0,needs_human:0};
    const key = f.status === 'needs_human' ? 'needs_human' : (f.status || 'open');
    if (byPlat[p][key] !== undefined) byPlat[p][key]++;
  });

  let platHtml = '';
  ['android','ios','flutter','typescript'].forEach(p => {
    const d = byPlat[p] || {open:0,fixed:0,needs_human:0};
    const pc = PLATFORM_COLORS[p] || {icon:p.slice(0,2),cls:'',bar:'#3fb950'};
    const total = d.open + d.fixed + d.needs_human;
    const pct = total ? Math.round((d.fixed / total) * 100) : 0;
    platHtml += `<div class="plat">
      <div class="ph"><div class="pi ${pc.cls}">${pc.icon}</div><div class="pn">${p}</div></div>
      <div class="pr"><span>Open</span><span>${d.open}</span></div>
      <div class="pr"><span>Fixed</span><span>${d.fixed}</span></div>
      <div class="pr"><span>Needs human</span><span>${d.needs_human}</span></div>
      <div class="pbar"><div class="pf" style="width:${pct}%;background:${pc.bar}"></div></div>
    </div>`;
  });
  document.getElementById('plats').innerHTML = platHtml;

  // Findings table — show open + needs_human, newest first
  const visible = findings
    .filter(f => f.status === 'open' || f.status === 'needs_human')
    .slice(0, 50);
  const rows = visible.length
    ? visible.map(f => {
        const tagCls = f.status === 'needs_human' ? 'tn' : 'to';
        const label = f.status === 'needs_human' ? 'needs human' : 'open';
        const plat = f.platform || (f.id||'').split(':')[1] || '?';
        return `<tr>
          <td><code>${f.type||'?'}</code></td>
          <td>${plat}</td>
          <td style="max-width:320px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${f.detail||f.id||''}</td>
          <td><span class="tag ${tagCls}">${label}</span></td>
        </tr>`;
      }).join('')
    : '<tr><td colspan="4" style="color:#7d8590;text-align:center;padding:16px">No open findings</td></tr>';
  document.getElementById('findings-body').innerHTML = rows;
}

// ── Sidebar activity ─────────────────────────────────
function renderActivity(run) {
  const steps = run.steps || [];
  const running = steps.find(s => s.status === 'running');

  if (!running) {
    const last = steps[steps.length - 1];
    const html = last
      ? `<div class="act-card idle-card">
           <div class="rh">
             <div class="rh-title">${last.command}</div>
             <div class="rh-badge rb-done">${last.status}</div>
             ${last.type === 'ai_agent' ? '<span class="type-a">🤖 AI AGENT</span>' : '<span class="type-s">SCRIPT</span>'}
           </div>
           <div style="font-size:10px;color:#7d8590">${last.summary || 'Completed'} · ${fmtDuration(last.duration_ms)}</div>
         </div>`
      : '<div class="idle-msg">No active command</div>';
    document.getElementById('activity').innerHTML = html;
    return;
  }

  const isAI = running.type === 'ai_agent';
  const cardCls = 'act-card ' + (isAI ? 'ai-running' : 'script-running');
  const dotCls = 'pdot ' + (isAI ? 'a' : 's');
  const badgeCls = isAI ? 'rb-ai' : 'rb-script';
  const elapsed = running.started_at
    ? Math.round((Date.now() - new Date(running.started_at).getTime()) / 1000) + 's'
    : '';

  // Substeps
  let substepsHtml = '';
  if (running.substeps && running.substeps.length) {
    substepsHtml = '<div class="substeps">';
    running.substeps.forEach(sub => {
      let icon, sstCls;
      if (sub.status === 'done')    { icon = '✓'; sstCls = 'sst-d'; }
      else if (sub.status === 'running') {
        icon = `<span class="spin">⟳</span>`;
        sstCls = isAI ? 'sst-ra' : 'sst-r';
      }
      else if (sub.status === 'failed') { icon = '✗'; sstCls = 'sst-f'; }
      else                           { icon = '○'; sstCls = 'sst-w'; }
      substepsHtml += `<div class="ss">
        <span class="ss-ic">${icon}</span>
        <div class="ss-info">
          <div class="ss-label">${sub.label}</div>
          ${sub.detail ? `<div class="ss-meta">${sub.detail}</div>` : ''}
        </div>
        <span class="sst ${sstCls}">${sub.status}</span>
      </div>`;
    });
    substepsHtml += '</div>';
  }

  // Log tail: use detail from running substep as "stdout"
  const runningSubstep = (running.substeps || []).find(s => s.status === 'running');
  const logLines = runningSubstep && runningSubstep.detail
    ? runningSubstep.detail.split('\n').slice(-5)
    : [];
  const logHtml = logLines.length
    ? `<div class="section-lbl">stdout</div>
       <div class="log-tail">${logLines.map(l => `<div class="ll info">${l}</div>`).join('')}</div>`
    : '';

  document.getElementById('activity').innerHTML = `
    <div class="${cardCls}">
      <div class="rh">
        <div class="${dotCls}"></div>
        <div class="rh-title">${running.command}</div>
        <div class="rh-badge ${badgeCls}">${elapsed}</div>
        ${isAI
          ? `<span class="type-a">🤖 AI AGENT</span><span style="font-size:9px;color:#7d8590">${running.model||''}</span>`
          : `<span class="type-s">SCRIPT</span>`}
      </div>
      ${substepsHtml}
      ${logHtml}
    </div>`;
}

// ── Poll loop ────────────────────────────────────────
async function poll() {
  if (hidden) return;
  try {
    const [runRes, repRes] = await Promise.all([
      fetch('/api/run'),
      fetch('/api/report'),
    ]);
    const [run, rep] = await Promise.all([runRes.json(), repRes.json()]);
    renderPipeline(run);
    renderFindings(rep);
    renderActivity(run);
    lastUpdated = Date.now();
  } catch (e) {
    // server not reachable — keep showing last state
  }
  const ago = lastUpdated ? timeSince(lastUpdated) : 'never';
  document.getElementById('meta').innerHTML =
    `<span class="pulse"></span> polling every 3s · updated ${ago} · <a href="/api/report" style="color:#58a6ff;text-decoration:none">report</a>`;
}

poll();
setInterval(poll, 3000);
setInterval(() => {
  if (lastUpdated) {
    const ago = timeSince(lastUpdated);
    const el = document.getElementById('meta');
    if (el) el.innerHTML = el.innerHTML.replace(/updated [^·]+·/, `updated ${ago} ·`);
  }
}, 1000);
</script>
</body>
</html>
```

- [ ] **Step 2.4: Implement `cmd/serve.go`**

```go
// cmd/serve.go
package main

import (
	_ "embed"
	"encoding/json"
	"flag"
	"fmt"
	"net/http"
	"os"
	"path/filepath"
)

//go:embed dashboard.html
var dashboardHTML []byte

func runServe(args []string) {
	fs := flag.NewFlagSet("serve", flag.ExitOnError)
	cfgPath := fs.String("config", "harness-config.yml", "path to harness-config.yml")
	port := fs.String("port", "8765", "port to listen on")
	_ = fs.Parse(args)

	dir := filepath.Dir(*cfgPath)

	mux := http.NewServeMux()
	mux.Handle("/api/report", reportHandler(dir))
	mux.Handle("/api/run", runHandler(dir))
	mux.Handle("/", dashboardHandler())

	addr := "localhost:" + *port
	fmt.Printf("[serve] Dashboard at http://%s\n", addr)
	fmt.Printf("[serve] Reading from %s\n", dir)
	fmt.Println("[serve] Ctrl-C to stop")
	if err := http.ListenAndServe(addr, corsMiddleware(mux)); err != nil {
		fmt.Fprintf(os.Stderr, "serve: %v\n", err)
		os.Exit(1)
	}
}

// reportHandler serves harness-report.json as JSON.
func reportHandler(dir string) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		data, err := os.ReadFile(filepath.Join(dir, "harness-report.json"))
		if os.IsNotExist(err) {
			w.Write([]byte("{}"))
			return
		}
		if err != nil {
			w.Write([]byte("{}"))
			return
		}
		w.Write(data)
	})
}

// runHandler serves harness-run.json as JSON.
func runHandler(dir string) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		data, err := os.ReadFile(filepath.Join(dir, "harness-run.json"))
		if os.IsNotExist(err) {
			w.Write([]byte("{}"))
			return
		}
		if err != nil {
			w.Write([]byte("{}"))
			return
		}
		w.Write(data)
	})
}

// dashboardHandler serves the embedded dashboard HTML.
func dashboardHandler() http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "text/html; charset=utf-8")
		w.Write(dashboardHTML)
	})
}

// corsMiddleware adds permissive CORS headers so dashboard.html works from file://.
func corsMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Access-Control-Allow-Origin", "*")
		next.ServeHTTP(w, r)
	})
}

// jsonResponse is a helper for writing arbitrary JSON in tests.
func jsonResponse(w http.ResponseWriter, v any) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(v)
}
```

- [ ] **Step 2.5: Add `serve` case to `cmd/main.go`**

```go
// cmd/main.go — update usage string and switch
func main() {
	if len(os.Args) < 2 {
		fmt.Fprintf(os.Stderr, "usage: harness <annotate|audit|fillmanifests|fix|genmanifests|gendocs|migrate|prompt|serve> [--config path]\n")
		os.Exit(1)
	}
	switch os.Args[1] {
	case "annotate":
		runAnnotate(os.Args[2:])
	case "audit":
		runAudit(os.Args[2:])
	case "fillmanifests":
		runFillManifests(os.Args[2:])
	case "fix":
		runFix(os.Args[2:])
	case "prompt":
		runPrompt(os.Args[2:])
	case "gendocs":
		runGendocs(os.Args[2:])
	case "genmanifests":
		runGenManifests(os.Args[2:])
	case "migrate":
		runMigrate(os.Args[2:])
	case "serve":
		runServe(os.Args[2:])
	default:
		fmt.Fprintf(os.Stderr, "unknown command: %s\n", os.Args[1])
		os.Exit(1)
	}
}
```

- [ ] **Step 2.6: Update `cmd/main_test.go` usage assertion**

In `cmd/main_test.go`, find the test that checks the usage string and update it to include `serve`:

```go
// find the line like:
assert.Contains(t, ..., "annotate|audit|fillmanifests|fix|genmanifests|gendocs|migrate|prompt")
// change to:
assert.Contains(t, ..., "annotate|audit|fillmanifests|fix|genmanifests|gendocs|migrate|prompt|serve")
```

- [ ] **Step 2.7: Run all cmd tests**

```bash
cd harness && go test ./cmd/... -v 2>&1 | grep -E "PASS|FAIL|---"
```
Expected: all pass including the 5 new `TestServe*` tests.

- [ ] **Step 2.8: Build and smoke test**

```bash
cd harness && go build -o ./harness-bin ./cmd/... && echo "Build OK"
./harness-bin serve --config harness-config.yml &
sleep 1 && curl -s http://localhost:8765/api/report | python3 -m json.tool | head -5
curl -s http://localhost:8765/api/run
kill %1
```
Expected: `/api/report` returns valid JSON from `harness-report.json`; `/api/run` returns `{}` (no run file yet).

- [ ] **Step 2.9: Commit**

```bash
cd harness
git add cmd/serve.go cmd/dashboard.html cmd/serve_test.go cmd/main.go cmd/main_test.go
git commit -m "feat(serve): harness serve command — live dashboard at localhost:8765

Serves embedded dashboard.html + /api/report + /api/run endpoints.
Dashboard polls every 3s, shows pipeline strip + findings breakdown
+ live activity sidebar (SCRIPT vs AI AGENT differentiation)."
```

---

## Task 3: Instrument `audit` and `annotate` with runstate

**Files:**
- Modify: `cmd/audit.go`
- Modify: `cmd/annotate.go`

These two commands have clear sub-phases worth emitting as substeps.

- [ ] **Step 3.1: Add runstate calls to `cmd/audit.go`**

At the top of `runAudit`, after loading config:

```go
// add import: "social-plus/harness/internal/runstate"

cfgDir := filepath.Dir(*cfgPath)
_ = runstate.Start(cfgDir, "audit", "script", "")
defer func() {
    if r := recover(); r != nil {
        _ = runstate.Fail(cfgDir, "audit", fmt.Sprintf("panic: %v", r))
        panic(r)
    }
}()
```

After `publicscan.Scan` loops (just before writing the report), add:

```go
_ = runstate.UpdateSubstep(cfgDir, "audit", runstate.Substep{
    Label:  "scan SDKs",
    Detail: fmt.Sprintf("%d public functions scanned", totalFuncs),
    Status: "done",
})
```

At the very end of `runAudit`, before `os.Exit` / return:

```go
summary := fmt.Sprintf("%d open, %d fixed, %d needs_human",
    r.Summary.Open, r.Summary.Fixed, r.Summary.NeedsHuman)
_ = runstate.Finish(cfgDir, "audit", summary)
```

For the Fail path (any `os.Exit(1)` after Start), replace with:
```go
_ = runstate.Fail(cfgDir, "audit", "see stderr")
os.Exit(1)
```

> Note: `totalFuncs` needs to be tracked — add a counter in the publicscan loop at line ~287 in audit.go.

- [ ] **Step 3.2: Add runstate calls to `cmd/annotate.go`**

```go
// add import: "social-plus/harness/internal/runstate"

// At top of runAnnotate after loading config:
cfgDir := filepath.Dir(*cfgPath)
_ = runstate.Start(cfgDir, "annotate", "script", "")

// After reading report:
_ = runstate.UpdateSubstep(cfgDir, "annotate", runstate.Substep{
    Label:  "load report",
    Detail: fmt.Sprintf("%d PUBLIC_FUNC_UNANNOTATED findings", len(findings)),
    Status: "done",
})

// After generating patches (before writing YAML):
_ = runstate.UpdateSubstep(cfgDir, "annotate", runstate.Substep{
    Label:  "generate patches",
    Detail: fmt.Sprintf("%d patches, %d skipped", len(patches), skipped),
    Status: "done",
})

// When --apply starts:
_ = runstate.UpdateSubstep(cfgDir, "annotate", runstate.Substep{
    Label:  "apply patches",
    Status: "running",
})

// After applyPatches returns:
_ = runstate.UpdateSubstep(cfgDir, "annotate", runstate.Substep{
    Label:  "apply patches",
    Detail: fmt.Sprintf("applied %d annotations", appliedCount),
    Status: "done",
})

// At the end:
_ = runstate.Finish(cfgDir, "annotate", fmt.Sprintf("%d patches, %d applied", len(patches), appliedCount))
```

> `skipped` and `appliedCount` need to be captured as variables — look at the existing `runAnnotate` function to find where to assign them from the printed output.

- [ ] **Step 3.3: Build and verify no compilation errors**

```bash
cd harness && go build -o ./harness-bin ./cmd/... && echo "Build OK"
```

- [ ] **Step 3.4: Integration test — run audit + check harness-run.json**

```bash
cd harness
./harness-bin audit --config harness-config.yml
cat harness-run.json | python3 -m json.tool | grep -E "command|status|summary" | head -10
```
Expected output includes:
```
"command": "audit",
"status": "done",
"summary": "... open, ... fixed, ... needs_human",
```

- [ ] **Step 3.5: Commit**

```bash
cd harness
git add cmd/audit.go cmd/annotate.go
git commit -m "feat: instrument audit+annotate with runstate substeps"
```

---

## Task 4: Instrument remaining commands with runstate

**Files:**
- Modify: `cmd/fix.go`, `cmd/gendocs.go`, `cmd/genmanifests.go`, `cmd/fillmanifests.go`, `cmd/migrate.go`

These commands get Start/Finish only (no substeps — they don't have distinct phases worth exposing yet).

- [ ] **Step 4.1: Add runstate to `cmd/fix.go`** (ai_agent type)

```go
// add import: "social-plus/harness/internal/runstate"
// At start of runFix, after loading config:
cfgDir := filepath.Dir(*cfgPath)
model := cfg.LLM.Model  // or however the model is accessed in fix.go
_ = runstate.Start(cfgDir, "fix", "ai_agent", model)
// At successful end:
_ = runstate.Finish(cfgDir, "fix", summary)  // use whatever summary string fix produces
// At each os.Exit(1) after Start:
_ = runstate.Fail(cfgDir, "fix", "see stderr"); os.Exit(1)
```

- [ ] **Step 4.2: Add runstate to `cmd/gendocs.go`** (ai_agent type)

```go
cfgDir := filepath.Dir(*cfgPath)
model := cfg.LLM.Model
_ = runstate.Start(cfgDir, "gendocs", "ai_agent", model)
_ = runstate.Finish(cfgDir, "gendocs", summary)
```

- [ ] **Step 4.3: Add runstate to `cmd/genmanifests.go`, `cmd/fillmanifests.go`, `cmd/migrate.go`** (script type)

Same pattern for each — `runstate.Start(cfgDir, "commandname", "script", "")` at start, `runstate.Finish(cfgDir, "commandname", summary)` at end, `runstate.Fail(...)` on error exits.

- [ ] **Step 4.4: Build and test**

```bash
cd harness && go build -o ./harness-bin ./cmd/... && echo "Build OK"
go test ./cmd/... 2>&1 | grep -E "ok|FAIL"
```
Expected: Build OK, all tests pass.

- [ ] **Step 4.5: Commit**

```bash
cd harness
git add cmd/fix.go cmd/gendocs.go cmd/genmanifests.go cmd/fillmanifests.go cmd/migrate.go
git commit -m "feat: instrument fix/gendocs/genmanifests/fillmanifests/migrate with runstate"
```

---

## Task 5: Add Step 0 to `harness-tasks.md` via `prompt.go`

**Files:**
- Modify: `cmd/prompt.go`

- [ ] **Step 5.1: Write failing test for Step 0 in prompt output**

In `cmd/main_test.go` or a new `cmd/prompt_test.go`:

```go
func TestRunPromptIncludesStep0Dashboard(t *testing.T) {
    dir := t.TempDir()
    // minimal harness-config.yml
    cfgContent := "sdks: {}\ndocs:\n  path: .\nllm:\n  model: test\n"
    cfgPath := filepath.Join(dir, "harness-config.yml")
    require.NoError(t, os.WriteFile(cfgPath, []byte(cfgContent), 0o644))
    // minimal harness-report.json
    repContent := `{"generated_at":"2026-05-01T00:00:00Z","findings":[],"summary":{"open":0,"fixed":0,"needs_human":0}}`
    require.NoError(t, os.WriteFile(filepath.Join(dir, "harness-report.json"), []byte(repContent), 0o644))

    outPath := filepath.Join(dir, "harness-tasks.md")
    runPrompt([]string{"--config", cfgPath, "--report", filepath.Join(dir, "harness-report.json"), "--out", outPath})

    content, err := os.ReadFile(outPath)
    require.NoError(t, err)
    assert.Contains(t, string(content), "Step 0")
    assert.Contains(t, string(content), "harness serve")
    assert.Contains(t, string(content), "localhost:8765")
}
```

- [ ] **Step 5.2: Run test to verify it fails**

```bash
cd harness && go test ./cmd/... -run TestRunPromptIncludesStep0Dashboard -v
```
Expected: FAIL — output file doesn't contain "Step 0" yet.

- [ ] **Step 5.3: Add Step 0 block to `cmd/prompt.go`**

In `runPrompt`, find where `out` (the `io.Writer` or file) is written to — it's the section that starts building the task file. Add this block **before** all other content is written:

```go
fmt.Fprintln(out, `## Step 0 — Start Dashboard (optional but recommended)

Run in a separate terminal before starting any other steps:

    ./harness-bin serve --config harness-config.yml

Then open http://localhost:8765 to watch pipeline progress live.
The dashboard auto-refreshes every 3 seconds.
You may skip this step if running headlessly.

---
`)
```

- [ ] **Step 5.4: Run test to verify it passes**

```bash
cd harness && go test ./cmd/... -run TestRunPromptIncludesStep0Dashboard -v
```
Expected: PASS.

- [ ] **Step 5.5: Run full test suite**

```bash
cd harness && go test ./... 2>&1 | grep -E "ok|FAIL"
```
Expected: all packages pass.

- [ ] **Step 5.6: Commit**

```bash
cd harness
git add cmd/prompt.go cmd/prompt_test.go  # or main_test.go if test added there
git commit -m "feat(prompt): add Step 0 harness serve block to generated harness-tasks.md"
```

---

## Task 6: End-to-end smoke test + final build

- [ ] **Step 6.1: Full test suite**

```bash
cd harness && go test ./... -count=1 2>&1 | grep -E "ok|FAIL|---"
```
Expected: all packages `ok`, no `FAIL`.

- [ ] **Step 6.2: Build and test the live loop manually**

In terminal 1:
```bash
cd harness && ./harness-bin serve --config harness-config.yml
# Expected: [serve] Dashboard at http://localhost:8765
```

Open `http://localhost:8765` in browser — should see dashboard with findings from `harness-report.json`.

In terminal 2:
```bash
cd harness && ./harness-bin audit --config harness-config.yml
```

Reload dashboard — pipeline card for `audit` should show `done` with summary.

- [ ] **Step 6.3: Verify `harness-tasks.md` Step 0**

```bash
cd harness && ./harness-bin prompt --config harness-config.yml --out /tmp/tasks-check.md
head -20 /tmp/tasks-check.md
```
Expected: first section is "Step 0 — Start Dashboard".

- [ ] **Step 6.4: Final commit**

```bash
cd harness
go build -o ./harness-bin ./cmd/...
git add harness-bin  # if binary is tracked; skip if gitignored
git commit -m "feat: harness serve dashboard — complete implementation

- internal/runstate: atomic pipeline state tracking
- cmd/serve.go + dashboard.html: live dashboard at localhost:8765
- All 8 commands instrumented with Start/Finish/Fail
- audit + annotate emit substeps for granular progress
- prompt: Step 0 added to harness-tasks.md"
```
