package main

import (
	"os"
	"path/filepath"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestRunPromptIncludesStep0Dashboard(t *testing.T) {
	dir := t.TempDir()

	cfgPath := filepath.Join(dir, "harness-config.yml")
	require.NoError(t, os.WriteFile(cfgPath, []byte(`
sdks:
  android:
    path: sdk
    snippet_dir: snippets
docs:
  path: docs
llm:
  model: test
`), 0o644))

	// One MISSING_SNIPPET finding with platform=android so it bypasses early return.
	repPath := filepath.Join(dir, "harness-report.json")
	require.NoError(t, os.WriteFile(repPath, []byte(`{
  "generated_at": "2026-05-01T00:00:00Z",
  "findings": [{
    "id": "MISSING_SNIPPET:android:AmityClient:getUser",
    "type": "MISSING_SNIPPET",
    "platform": "android",
    "status": "open",
    "function_id": "getUser",
    "snippet_file": "",
    "doc_page": "social-plus-sdk/user/overview",
    "detail": "no snippet found for getUser"
  }],
  "summary": {"open": 1, "fixed": 0, "needs_human": 0}
}`), 0o644))

	outPath := filepath.Join(dir, "harness-tasks.md")
	runPrompt([]string{
		"--config", cfgPath,
		"--report", repPath,
		"--out", outPath,
	})

	content, err := os.ReadFile(outPath)
	require.NoError(t, err, "harness-tasks.md should be written")

	s := string(content)
	assert.Contains(t, s, "Step 0")
	assert.Contains(t, s, "harness-bin serve")
	assert.Contains(t, s, "localhost:8765")
}
