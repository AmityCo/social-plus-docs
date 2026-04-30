package report_test

import (
	"os"
	"path/filepath"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"social-plus/harness/internal/report"
)

func TestWriteAndRead(t *testing.T) {
	dir := t.TempDir()
	path := filepath.Join(dir, "harness-report.json")

	r := &report.Report{
		GeneratedAt: "2026-04-30T00:00:00Z",
		Findings: []report.Finding{
			{ID: "test-1", Type: report.TypeMissingSnippet, Platform: "android", Status: report.StatusOpen},
		},
	}
	r.Recount()

	err := report.Write(r, path)
	require.NoError(t, err)

	got, err := report.Read(path)
	require.NoError(t, err)
	assert.Equal(t, 1, got.Summary.Open)
	assert.Equal(t, "test-1", got.Findings[0].ID)
}

func TestReadMissing(t *testing.T) {
	_, err := report.Read("/nonexistent/path.json")
	assert.Error(t, err)
}

func TestReadInvalidJSON(t *testing.T) {
	dir := t.TempDir()
	path := filepath.Join(dir, "invalid.json")
	require.NoError(t, os.WriteFile(path, []byte("{not valid json"), 0o644))

	_, err := report.Read(path)
	require.Error(t, err)
	assert.Contains(t, err.Error(), "parse report")
}

func TestWriteIssues(t *testing.T) {
	dir := t.TempDir()
	path := filepath.Join(dir, "issues.md")

	findings := []report.Finding{
		{
			ID:          "human-1",
			Type:        report.TypeDocMissing,
			Platform:    "ios",
			FunctionID:  "createPost",
			Detail:      "Cannot auto-fix",
			SnippetFile: "snippets/ios/createPost.swift",
			DocPage:     "docs/social/post-creation.mdx",
			Status:      report.StatusNeedsHuman,
		},
		{
			ID:       "fixed-1",
			Type:     report.TypeMissingSnippet,
			Platform: "android",
			Status:   report.StatusFixed,
		},
	}

	require.NoError(t, report.WriteIssues(findings, path))

	content, err := os.ReadFile(path)
	require.NoError(t, err)
	assert.Contains(t, string(content), "createPost")
	assert.Contains(t, string(content), "Cannot auto-fix")
	assert.Contains(t, string(content), "Snippet: snippets/ios/createPost.swift")
	assert.Contains(t, string(content), "Doc: docs/social/post-creation.mdx")
	assert.NotContains(t, string(content), "android")
}

func TestRecount(t *testing.T) {
	r := &report.Report{
		Findings: []report.Finding{
			{Status: report.StatusOpen},
			{Status: report.StatusFixed},
			{Status: report.StatusFixed},
			{Status: report.StatusNeedsHuman},
		},
	}

	r.Recount()

	assert.Equal(t, 1, r.Summary.Open)
	assert.Equal(t, 2, r.Summary.Fixed)
	assert.Equal(t, 1, r.Summary.NeedsHuman)
}
