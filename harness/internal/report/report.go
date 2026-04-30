package report

import (
	"encoding/json"
	"fmt"
	"os"
	"strings"
)

func Write(r *Report, path string) error {
	snapshot := *r
	snapshot.Recount()
	b, err := json.MarshalIndent(&snapshot, "", "  ")
	if err != nil {
		return fmt.Errorf("marshal report: %w", err)
	}
	return os.WriteFile(path, b, 0o644)
}

func Read(path string) (*Report, error) {
	b, err := os.ReadFile(path)
	if err != nil {
		return nil, fmt.Errorf("read report %s: %w", path, err)
	}
	var r Report
	if err := json.Unmarshal(b, &r); err != nil {
		return nil, fmt.Errorf("parse report: %w", err)
	}
	return &r, nil
}

func WriteIssues(findings []Finding, path string) error {
	var sb strings.Builder
	count := 0
	for _, f := range findings {
		if f.Status != StatusNeedsHuman {
			continue
		}
		count++
		sb.WriteString(fmt.Sprintf("### [%s] %s · %s\n", f.Type, f.Platform, f.FunctionID))
		if f.Detail != "" {
			sb.WriteString(f.Detail + "\n")
		}
		if f.SnippetFile != "" {
			sb.WriteString(fmt.Sprintf("Snippet: %s\n", f.SnippetFile))
		}
		if f.DocPage != "" {
			sb.WriteString(fmt.Sprintf("Doc: %s\n", f.DocPage))
		}
		sb.WriteString("\n---\n\n")
	}
	if count == 0 {
		return nil
	}
	header := "# Items Needing Human Review\n\n"
	return os.WriteFile(path, []byte(header+sb.String()), 0o644)
}
