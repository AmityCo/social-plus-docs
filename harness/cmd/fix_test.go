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
		"-api-key", "test-key",
	})

	// Verify the report was written back.
	if _, statErr := os.Stat(reportPath); statErr != nil {
		t.Fatalf("report not written: %v", statErr)
	}
}
