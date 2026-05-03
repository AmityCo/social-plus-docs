package config_test

import (
	"os"
	"path/filepath"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"social-plus/harness/internal/config"
)

func TestLoad(t *testing.T) {
	yml := `
sdks:
  android:
    path: ../../Amity-Social-Cloud-SDK-Android
    snippet_dir: amity-sample-code/src
    compile_cmd: ["./gradlew", "build"]
docs:
  path: ../
llm:
  model: claude-sonnet-4-6
`
	dir := t.TempDir()
	f := filepath.Join(dir, "harness-config.yml")
	require.NoError(t, os.WriteFile(f, []byte(yml), 0o644))

	cfg, err := config.Load(f)
	require.NoError(t, err)
	assert.Equal(t, "claude-sonnet-4-6", cfg.LLM.Model)
	assert.Contains(t, cfg.SDKs, "android")
}

func TestLoadMissing(t *testing.T) {
	_, err := config.Load("/nonexistent/harness-config.yml")
	require.Error(t, err)
	assert.Contains(t, err.Error(), "read config")
}

func TestLoadInvalidYAML(t *testing.T) {
	dir := t.TempDir()
	f := filepath.Join(dir, "bad.yml")
	require.NoError(t, os.WriteFile(f, []byte(":\tinvalid:\n  - yaml: ["), 0o644))

	_, err := config.Load(f)
	require.Error(t, err)
	assert.Contains(t, err.Error(), "parse config")
}

func TestLoadAndSave_WithBaselineCommit(t *testing.T) {
	dir := t.TempDir()
	cfgPath := filepath.Join(dir, "harness-config.yml")
	content := `sdks:
  android:
    path: ../android
    snippet_dir: snippets
    baseline_commit: abc123
docs:
  path: ../docs
llm:
  model: test
`
	require.NoError(t, os.WriteFile(cfgPath, []byte(content), 0o644))
	cfg, err := config.Load(cfgPath)
	require.NoError(t, err)
	require.Equal(t, "abc123", cfg.SDKs["android"].BaselineCommit)

	// Update and save
	updated := cfg.SDKs["android"]
	updated.BaselineCommit = "def456"
	cfg.SDKs["android"] = updated
	require.NoError(t, cfg.Save(cfgPath))

	// Reload and verify
	cfg2, err := config.Load(cfgPath)
	require.NoError(t, err)
	require.Equal(t, "def456", cfg2.SDKs["android"].BaselineCommit)
}
