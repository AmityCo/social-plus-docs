package main

import (
	"encoding/json"
	"os"
	"path/filepath"
	"strings"
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

// ---

// TestExtractAscPageFromSnippet_SpDocsPage tests sp_docs_page: field
func TestExtractAscPageFromSnippet_SpDocsPage(t *testing.T) {
	dir := t.TempDir()
	snippetPath := filepath.Join(dir, "AmityTest.kt")
	content := `package com.example

class AmityTest {
    /* begin_sample_code
       filename: AmityTest.kt
       sp_docs_page: social-plus-sdk/chat/channels
       description: Test snippet
       */
    fun test() {}
    /* end_sample_code */
}
`
	if err := os.WriteFile(snippetPath, []byte(content), 0o644); err != nil {
		t.Fatal(err)
	}
	got, err := extractAscPageFromSnippet(snippetPath)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if got != "social-plus-sdk/chat/channels" {
		t.Errorf("got %q, want %q", got, "social-plus-sdk/chat/channels")
	}
}

func TestExtractAscPageFromSnippet_Missing(t *testing.T) {
	dir := t.TempDir()
	snippetPath := filepath.Join(dir, "AmityNoPage.kt")
	content := `package com.example
class AmityNoPage {}`
	if err := os.WriteFile(snippetPath, []byte(content), 0o644); err != nil {
		t.Fatal(err)
	}
	_, err := extractAscPageFromSnippet(snippetPath)
	if err == nil {
		t.Fatal("expected error for missing sp_docs_page, got nil")
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

func TestRunFix_ConflictResolution(t *testing.T) {
	dir := t.TempDir()
	androidSnipDir := filepath.Join(dir, "android-sdk", "snippets")
	flutterSnipDir := filepath.Join(dir, "flutter-sdk", "snippets")
	docsDir := filepath.Join(dir, "docs")
	if err := os.MkdirAll(androidSnipDir, 0o755); err != nil {
		t.Fatal(err)
	}
	if err := os.MkdirAll(flutterSnipDir, 0o755); err != nil {
		t.Fatal(err)
	}
	if err := os.MkdirAll(docsDir, 0o755); err != nil {
		t.Fatal(err)
	}

	// docs.json
	docsJSON := `{"navigation":{"tabs":[{"groups":[{"pages":["social-plus-sdk/chat/ban-management"]}]}]}}`
	if err := os.WriteFile(filepath.Join(docsDir, "docs.json"), []byte(docsJSON), 0o644); err != nil {
		t.Fatal(err)
	}

	// Android snippet (canonical page)
	androidSnip := "/* begin_sample_code\n   filename: AmityBanChannelMembers\n   sp_docs_page: social-plus-sdk/chat/ban-management\n   description: test\n   */\nfun ban() {}\n/* end_sample_code */"
	if err := os.WriteFile(filepath.Join(androidSnipDir, "AmityBanChannelMembers.kt"), []byte(androidSnip), 0o644); err != nil {
		t.Fatal(err)
	}

	// Flutter snippet (wrong page — conflicts with android)
	flutterSnip := "/* begin_sample_code\n   filename: AmityBanChannelMembers\n   sp_docs_page: social-plus-sdk/chat/archive-channels\n   description: test\n   */\nvoid ban() {}\n/* end_sample_code */"
	flutterFile := filepath.Join(flutterSnipDir, "AmityBanChannelMembers.dart")
	if err := os.WriteFile(flutterFile, []byte(flutterSnip), 0o644); err != nil {
		t.Fatal(err)
	}

	// Config pointing to the snippet dirs
	cfgData := "docs:\n  path: docs\nsdks:\n  android:\n    path: android-sdk\n    snippet_dir: snippets\n  flutter:\n    path: flutter-sdk\n    snippet_dir: snippets\nllm:\n  model: test\n"
	cfgPath := filepath.Join(dir, "harness-config.yml")
	if err := os.WriteFile(cfgPath, []byte(cfgData), 0o644); err != nil {
		t.Fatal(err)
	}

	// Report with one open conflict finding
	reportData := `{"generated_at":"2026-01-01T00:00:00Z","findings":[{"id":"key-conflict:ban-channel-members","type":"SNIPPET_KEY_PLATFORM_CONFLICT","status":"open","gendocs_key":"ban-channel-members","detail":"key conflict"}]}`
	reportPath := filepath.Join(dir, "harness-report.json")
	if err := os.WriteFile(reportPath, []byte(reportData), 0o644); err != nil {
		t.Fatal(err)
	}

	runFix([]string{"--config", cfgPath, "--report", reportPath, "--issues", filepath.Join(dir, "issues.md")})

	// Flutter file must be rewritten to use android's canonical page
	data, err := os.ReadFile(flutterFile)
	if err != nil {
		t.Fatalf("read flutter file: %v", err)
	}
	if !strings.Contains(string(data), "sp_docs_page: social-plus-sdk/chat/ban-management") {
		t.Errorf("flutter file not rewritten: %s", string(data))
	}

	// Conflict finding must be marked fixed
	r, err := report.Read(reportPath)
	if err != nil {
		t.Fatalf("read report: %v", err)
	}
	if len(r.Findings) != 1 {
		t.Fatalf("expected 1 finding, got %d", len(r.Findings))
	}
	if r.Findings[0].Status != report.StatusFixed {
		t.Errorf("expected finding status=fixed, got %q", r.Findings[0].Status)
	}
}

func TestRunFix_DocMissing(t *testing.T) {
	dir := t.TempDir()

	// Create a minimal harness-config.yml
	cfgContent := "sdks:\n  android:\n    path: ./sdk\n    snippet_dir: snippets\n    compile_cmd: []\ndocs:\n  path: .\nllm:\n  model: test\n"
	cfgPath := filepath.Join(dir, "harness-config.yml")
	if err := os.WriteFile(cfgPath, []byte(cfgContent), 0o644); err != nil {
		t.Fatal(err)
	}

	// docs.json with the NEW (correct) path
	docsJSON := `{"navigation":{"tabs":[{"pages":["social-plus-sdk/chat/message-creation/send-a-message"]}]}}`
	if err := os.WriteFile(filepath.Join(dir, "docs.json"), []byte(docsJSON), 0o644); err != nil {
		t.Fatal(err)
	}

	// Create the SDK snippet directory and a snippet file with the OLD path
	snippetDir := filepath.Join(dir, "sdk", "snippets")
	if err := os.MkdirAll(snippetDir, 0o755); err != nil {
		t.Fatal(err)
	}
	snippetFile := filepath.Join(snippetDir, "AmitySendMessage.kt")
	snippetContent := `/* begin_sample_code
   filename: AmitySendMessage.kt
   sp_docs_page: social-plus-sdk/chat/messages/send-a-message
   description: Send a message
   */
fun sendMessage() {}
/* end_sample_code */
`
	if err := os.WriteFile(snippetFile, []byte(snippetContent), 0o644); err != nil {
		t.Fatal(err)
	}

	// Create report with one DOC_MISSING finding using the old path and relative snippet_file
	snippetRel := filepath.Join("sdk", "snippets", "AmitySendMessage.kt")
	r := report.Report{
		GeneratedAt: "2024-01-01T00:00:00Z",
		Findings: []report.Finding{
			{
				ID:          "android-doc-missing-AmitySendMessage.kt",
				Type:        report.TypeDocMissing,
				Platform:    "android",
				SnippetFile: snippetRel,
				DocPage:     "social-plus-sdk/chat/messages/send-a-message",
				Detail:      `sp_docs_page "social-plus-sdk/chat/messages/send-a-message" not found in docs.json`,
				Status:      report.StatusOpen,
			},
		},
	}
	b, err := json.Marshal(r)
	if err != nil {
		t.Fatalf("marshal report: %v", err)
	}
	reportPath := filepath.Join(dir, "harness-report.json")
	if err := os.WriteFile(reportPath, b, 0o644); err != nil {
		t.Fatal(err)
	}
	issuesPath := filepath.Join(dir, "harness-issues.md")

	runFix([]string{"-config", cfgPath, "-report", reportPath, "-issues", issuesPath})

	// Check that the finding was fixed
	data, err := os.ReadFile(reportPath)
	if err != nil {
		t.Fatalf("read report: %v", err)
	}
	var result report.Report
	if err := json.Unmarshal(data, &result); err != nil {
		t.Fatal(err)
	}
	if len(result.Findings) != 1 {
		t.Fatalf("expected 1 finding, got %d", len(result.Findings))
	}
	if result.Findings[0].Status != report.StatusFixed {
		t.Errorf("expected status fixed, got %q (detail: %s)", result.Findings[0].Status, result.Findings[0].Detail)
	}

	// Check that the snippet file was updated
	updated, err := os.ReadFile(snippetFile)
	if err != nil {
		t.Fatalf("read snippet: %v", err)
	}
	if !strings.Contains(string(updated), "social-plus-sdk/chat/message-creation/send-a-message") {
		t.Errorf("snippet file not updated: %s", string(updated))
	}
}
