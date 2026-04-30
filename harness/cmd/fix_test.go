package main

import (
	"encoding/json"
	"os"
	"path/filepath"
	"testing"

	"social-plus/harness/internal/report"
)

func TestRunFixEmptyReport(t *testing.T) {
	dir := t.TempDir()

	cfgContent := "sdks: {}\ndocs:\n  path: .\nllm:\n  model: test\n"
	cfgPath := filepath.Join(dir, "harness-config.yml")
	if err := os.WriteFile(cfgPath, []byte(cfgContent), 0o644); err != nil {
		t.Fatal(err)
	}

	// pages.Load requires docs.json at docs.path/docs.json
	docsJSON := `{"navigation": {"tabs": [{"pages": ["social-plus-sdk/overview"]}]}}`
	if err := os.WriteFile(filepath.Join(dir, "docs.json"), []byte(docsJSON), 0o644); err != nil {
		t.Fatal(err)
	}

	r := report.Report{GeneratedAt: "2024-01-01T00:00:00Z", Findings: []report.Finding{}}
	b, err := json.Marshal(r)
	if err != nil {
		t.Fatal(err)
	}
	reportPath := filepath.Join(dir, "harness-report.json")
	if err := os.WriteFile(reportPath, b, 0o644); err != nil {
		t.Fatal(err)
	}

	issuesPath := filepath.Join(dir, "harness-issues.md")

	// Should not panic when invoked with an empty report (no open findings).
	runFix([]string{
		"-config", cfgPath,
		"-report", reportPath,
		"-issues", issuesPath,
		// No api-key flag — Copilot CLI handles AI tasks via 'harness prompt'.
	})

	// Verify the report was written back.
	if _, statErr := os.Stat(reportPath); statErr != nil {
		t.Fatalf("report not written: %v", statErr)
	}
}

// ---- Unit tests for helper functions (Fix 7) ----

func TestSanitizeName(t *testing.T) {
	cases := []struct {
		input string
		want  string
	}{
		{"message.delete", "MessageDelete"},
		{"channel_create", "ChannelCreate"},
		{"", ""},
		{"single", "Single"},
	}
	for _, tc := range cases {
		got := sanitizeName(tc.input)
		if got != tc.want {
			t.Errorf("sanitizeName(%q) = %q, want %q", tc.input, got, tc.want)
		}
	}
}

func TestPlatformLang(t *testing.T) {
	cases := []struct {
		platform string
		want     string
	}{
		{"android", "kotlin"},
		{"ios", "swift"},
		{"flutter", "dart"},
		{"typescript", "typescript"},
		{"unknown", "text"},
	}
	for _, tc := range cases {
		got := platformLang(tc.platform)
		if got != tc.want {
			t.Errorf("platformLang(%q) = %q, want %q", tc.platform, got, tc.want)
		}
	}
}

func TestPlatformExt(t *testing.T) {
	cases := []struct {
		platform string
		want     string
	}{
		{"android", "kt"},
		{"ios", "swift"},
		{"flutter", "dart"},
		{"typescript", "ts"},
		{"unknown", "txt"},
	}
	for _, tc := range cases {
		got := platformExt(tc.platform)
		if got != tc.want {
			t.Errorf("platformExt(%q) = %q, want %q", tc.platform, got, tc.want)
		}
	}
}

func TestExtractAscPageFromSnippet(t *testing.T) {
	t.Run("happy path", func(t *testing.T) {
		dir := t.TempDir()
		content := "/* begin_sample_code\n    asc_page: social-plus-sdk/social/flutter\n    */\nvoid f() {}"
		f := filepath.Join(dir, "snippet.dart")
		if err := os.WriteFile(f, []byte(content), 0o644); err != nil {
			t.Fatal(err)
		}
		got, err := extractAscPageFromSnippet(f)
		if err != nil {
			t.Fatalf("unexpected error: %v", err)
		}
		if got != "social-plus-sdk/social/flutter" {
			t.Errorf("got %q, want %q", got, "social-plus-sdk/social/flutter")
		}
	})

	t.Run("missing field", func(t *testing.T) {
		dir := t.TempDir()
		content := "/* begin_sample_code\n    gist_id: abc\n    */\nvoid f() {}"
		f := filepath.Join(dir, "snippet.dart")
		if err := os.WriteFile(f, []byte(content), 0o644); err != nil {
			t.Fatal(err)
		}
		_, err := extractAscPageFromSnippet(f)
		if err == nil {
			t.Fatal("expected error for missing asc_page field, got nil")
		}
	})

	t.Run("file not found", func(t *testing.T) {
		_, err := extractAscPageFromSnippet("/nonexistent/path/snippet.dart")
		if err == nil {
			t.Fatal("expected error for missing file, got nil")
		}
	})
}
