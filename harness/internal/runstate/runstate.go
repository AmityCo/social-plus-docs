// internal/runstate/runstate.go
package runstate

import (
	"crypto/rand"
	"encoding/hex"
	"encoding/json"
	"errors"
	"os"
	"path/filepath"
	"time"
)

const filename = "harness-run.json"

// RunState is the top-level structure written to harness-run.json.
type RunState struct {
	SessionID      string `json:"session_id"`
	StartedAt      string `json:"started_at"`
	CurrentCommand string `json:"current_command"`
	Steps          []Step `json:"steps"`
}

// Step represents one harness command execution.
type Step struct {
	Command    string    `json:"command"`
	Type       string    `json:"type"`            // "script" | "ai_agent"
	Model      string    `json:"model,omitempty"` // set for ai_agent
	Status     string    `json:"status"`          // "running"|"done"|"failed"|"idle"
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
	if errors.Is(err, os.ErrNotExist) {
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
		// Silently skip — callers are fire-and-forget and should not crash
		// if state tracking was never started (e.g., during local dev without a dashboard).
		return nil
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
