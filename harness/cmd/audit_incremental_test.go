package main

import (
	"encoding/json"
	"fmt"
	"io"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"testing"

	"github.com/stretchr/testify/require"
	"social-plus/harness/internal/report"
)

func initGitRepoWithSnippet(t *testing.T, snippetDir, filename, content string) (repoDir string, baseline string) {
	t.Helper()
	dir := t.TempDir()
	snipDir := filepath.Join(dir, snippetDir)
	require.NoError(t, os.MkdirAll(snipDir, 0o755))
	require.NoError(t, os.WriteFile(filepath.Join(snipDir, filename), []byte(content), 0o644))
	gitExec := func(args ...string) {
		cmd := exec.Command(args[0], args[1:]...)
		cmd.Dir = dir
		cmd.Env = append(os.Environ(),
			"GIT_AUTHOR_NAME=test", "GIT_AUTHOR_EMAIL=t@t.com",
			"GIT_COMMITTER_NAME=test", "GIT_COMMITTER_EMAIL=t@t.com")
		out, err := cmd.CombinedOutput()
		require.NoError(t, err, "git: %v\n%s", args, out)
	}
	gitExec("git", "init")
	gitExec("git", "config", "user.email", "t@t.com")
	gitExec("git", "config", "user.name", "test")
	gitExec("git", "add", ".")
	gitExec("git", "commit", "-m", "init")
	cmd := exec.Command("git", "rev-parse", "HEAD")
	cmd.Dir = dir
	out, err := cmd.Output()
	require.NoError(t, err)
	return dir, strings.TrimSpace(string(out))
}

func TestRunAudit_IncrementalSkipsUnchangedPlatform(t *testing.T) {
	dir := t.TempDir()

	androidContent := `class AmityFoo {
/* begin_sample_code
   filename: AmityFoo.kt
   sp_docs_page: social-plus-sdk/chat/channels
   description: test
   */
fun foo() {}
/* end_sample_code */
}`
	sdkDir, baseline := initGitRepoWithSnippet(t, "snippets", "AmityFoo.kt", androidContent)

	docsDir := filepath.Join(dir, "docs")
	require.NoError(t, os.MkdirAll(docsDir, 0o755))
	docsJSON := `{"navigation":{"tabs":[{"groups":[{"pages":["social-plus-sdk/chat/channels"]}]}]}}`
	require.NoError(t, os.WriteFile(filepath.Join(docsDir, "docs.json"), []byte(docsJSON), 0o644))

	relSDKPath, err := filepath.Rel(dir, sdkDir)
	require.NoError(t, err)

	cfgData := fmt.Sprintf(`docs:
  path: docs
sdks:
  android:
    path: %s
    snippet_dir: snippets
    baseline_commit: %s
llm:
  model: test
`, relSDKPath, baseline)
	cfgPath := filepath.Join(dir, "harness-config.yml")
	require.NoError(t, os.WriteFile(cfgPath, []byte(cfgData), 0o644))

	reportPath := filepath.Join(dir, "harness-report.json")
	emptyReport := report.Report{GeneratedAt: "2026-01-01T00:00:00Z"}
	b, _ := json.Marshal(emptyReport)
	require.NoError(t, os.WriteFile(reportPath, b, 0o644))

	// Capture stdout to verify skip message
	old := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w
	runAudit([]string{"--config", cfgPath, "--report", reportPath, "--incremental"})
	w.Close()
	os.Stdout = old
	var buf strings.Builder
	io.Copy(&buf, r)
	output := buf.String()
	require.True(t, strings.Contains(output, "no changes") && strings.Contains(output, "android"),
		"expected skip message for android, got: %s", output)
}

func TestRunAudit_IncrementalOrphaned(t *testing.T) {
	dir := t.TempDir()

	snippetContent := `class AmityFoo {
/* begin_sample_code
   filename: AmityFoo.kt
   sp_docs_page: social-plus-sdk/chat/channels
   description: test
   */
fun foo() {}
/* end_sample_code */
}`
	sdkDir, baseline := initGitRepoWithSnippet(t, "snippets", "AmityFoo.kt", snippetContent)

	// Delete the snippet file after baseline
	gitExec := func(args ...string) {
		cmd := exec.Command(args[0], args[1:]...)
		cmd.Dir = sdkDir
		cmd.Env = append(os.Environ(),
			"GIT_AUTHOR_NAME=test", "GIT_AUTHOR_EMAIL=t@t.com",
			"GIT_COMMITTER_NAME=test", "GIT_COMMITTER_EMAIL=t@t.com")
		out, err := cmd.CombinedOutput()
		require.NoError(t, err, "git: %v\n%s", args, out)
	}
	gitExec("git", "rm", "snippets/AmityFoo.kt")
	gitExec("git", "commit", "-m", "delete foo")

	docsDir := filepath.Join(dir, "docs")
	require.NoError(t, os.MkdirAll(docsDir, 0o755))
	docsJSON := `{"navigation":{"tabs":[{"groups":[{"pages":["social-plus-sdk/chat/channels"]}]}]}}`
	require.NoError(t, os.WriteFile(filepath.Join(docsDir, "docs.json"), []byte(docsJSON), 0o644))

	relSDKPath, err := filepath.Rel(dir, sdkDir)
	require.NoError(t, err)

	cfgData := fmt.Sprintf(`docs:
  path: docs
sdks:
  android:
    path: %s
    snippet_dir: snippets
    baseline_commit: %s
llm:
  model: test
`, relSDKPath, baseline)
	cfgPath := filepath.Join(dir, "harness-config.yml")
	require.NoError(t, os.WriteFile(cfgPath, []byte(cfgData), 0o644))

	reportPath := filepath.Join(dir, "harness-report.json")
	emptyReport := report.Report{GeneratedAt: "2026-01-01T00:00:00Z"}
	b, _ := json.Marshal(emptyReport)
	require.NoError(t, os.WriteFile(reportPath, b, 0o644))

	runAudit([]string{"--config", cfgPath, "--report", reportPath, "--incremental"})

	rep, err := report.Read(reportPath)
	require.NoError(t, err)
	var orphaned []report.Finding
	for _, f := range rep.Findings {
		if f.Type == report.TypeSnippetOrphaned {
			orphaned = append(orphaned, f)
		}
	}
	require.Len(t, orphaned, 1, "expected 1 SNIPPET_ORPHANED finding")
	require.Equal(t, "android", orphaned[0].Platform)
	require.Contains(t, orphaned[0].Detail, "AmityFoo")
}
