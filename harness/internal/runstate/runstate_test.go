// internal/runstate/runstate_test.go
package runstate_test

import (
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
	time.Sleep(5 * time.Millisecond) // ensure nonzero duration
	require.NoError(t, runstate.Fail(dir, "fix", "LLM timeout"))

	state, err := runstate.Read(dir)
	require.NoError(t, err)
	assert.Equal(t, "failed", state.Steps[0].Status)
	assert.Equal(t, "LLM timeout", state.Steps[0].Summary)
	assert.Empty(t, state.CurrentCommand)
	assert.Greater(t, state.Steps[0].DurationMs, int64(0))
	assert.NotEmpty(t, state.Steps[0].FinishedAt)
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

// TestSessionIDPersistsAcrossStarts verifies session ID and StartedAt persist across multiple Start calls in a session.
func TestSessionIDPersistsAcrossStarts(t *testing.T) {
	dir := t.TempDir()
	require.NoError(t, runstate.Start(dir, "audit", "script", ""))
	state1, err := runstate.Read(dir)
	require.NoError(t, err)

	require.NoError(t, runstate.Finish(dir, "audit", "done"))
	require.NoError(t, runstate.Start(dir, "annotate", "script", ""))
	state2, err := runstate.Read(dir)
	require.NoError(t, err)

	assert.NotEmpty(t, state2.SessionID)
	assert.Equal(t, state1.SessionID, state2.SessionID, "session ID must not change mid-run")
	assert.Equal(t, state1.StartedAt, state2.StartedAt, "StartedAt must not reset mid-run")
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
