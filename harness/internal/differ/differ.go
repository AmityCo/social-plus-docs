package differ

import (
	"fmt"
	"path/filepath"
	"strings"

	"social-plus/harness/internal/extractor"
	"social-plus/harness/internal/pages"
	"social-plus/harness/internal/report"
	"social-plus/harness/internal/scanner"
)

// Diff runs all finding checks except DOC_SURFACE_DRIFT (needs MDX content).
func Diff(fns []extractor.PublicFunction, snips []scanner.Snippet, reg *pages.Registry, platform string) []report.Finding {
	return DiffWithMDX(fns, snips, reg, platform, nil)
}

// DiffWithMDX runs all finding checks including DOC_SURFACE_DRIFT.
func DiffWithMDX(fns []extractor.PublicFunction, snips []scanner.Snippet, reg *pages.Registry, platform string, mdxContent map[string]string) []report.Finding {
	var findings []report.Finding

	coveredMethods := make(map[string]bool)
	for _, s := range snips {
		for _, call := range extractMethodCalls(s.Content) {
			coveredMethods[strings.ToLower(call)] = true
		}
	}

	for _, fn := range fns {
		for _, id := range fn.IDs {
			method := methodName(id)
			if coveredMethods[strings.ToLower(method)] {
				continue
			}

			findings = append(findings, report.Finding{
				ID:         fmt.Sprintf("%s-missing-%s", platform, id),
				Type:       report.TypeMissingSnippet,
				Platform:   platform,
				FunctionID: id,
				Detail:     fmt.Sprintf("no snippet covers method %q", method),
				Status:     report.StatusOpen,
			})
		}
	}

	for _, s := range snips {
		base := filepath.Base(s.File)

		if strings.HasPrefix(s.AscPage, "http") {
			findings = append(findings, report.Finding{
				ID:          fmt.Sprintf("%s-asc-invalid-%s", platform, base),
				Type:        report.TypeAscPageInvalid,
				Platform:    platform,
				SnippetFile: s.File,
				Detail:      fmt.Sprintf("asc_page %q is a legacy URL, not a docs.json relative path", s.AscPage),
				Status:      report.StatusOpen,
			})
			continue
		}

		if s.AscPage == "" {
			continue
		}

		if !reg.Contains(s.AscPage) {
			findings = append(findings, report.Finding{
				ID:          fmt.Sprintf("%s-doc-missing-%s", platform, base),
				Type:        report.TypeDocMissing,
				Platform:    platform,
				SnippetFile: s.File,
				DocPage:     s.AscPage,
				Detail:      fmt.Sprintf("asc_page %q not found in docs.json", s.AscPage),
				Status:      report.StatusOpen,
			})
			continue
		}

		if mdxContent != nil {
			mdx, ok := mdxContent[s.AscPage]
			if ok {
				for _, call := range extractMethodCalls(s.Content) {
					if strings.Contains(mdx, call) {
						continue
					}

					findings = append(findings, report.Finding{
						ID:          fmt.Sprintf("%s-surface-drift-%s-%s", platform, base, call),
						Type:        report.TypeDocSurfaceDrift,
						Platform:    platform,
						SnippetFile: s.File,
						DocPage:     s.AscPage,
						Detail:      fmt.Sprintf("snippet calls %q but not found in doc page content", call),
						Status:      report.StatusOpen,
					})
				}

				// SNIPPET_CONTENT_DRIFT: MDX code block has drifted from SDK snippet content
				if s.Content != "" {
					firstLine := firstNonEmptyLine(s.Content)
					if firstLine != "" && !strings.Contains(mdx, firstLine) {
						findings = append(findings, report.Finding{
							ID:          fmt.Sprintf("%s-snippet-drift-%s", platform, base),
							Type:        report.TypeSnippetContentDrift,
							Platform:    platform,
							SnippetFile: s.File,
							DocPage:     s.AscPage,
							Detail:      fmt.Sprintf("snippet content not found in MDX page %q", s.AscPage),
							Status:      report.StatusOpen,
						})
					}
				}
			}
		}
	}

	return findings
}

func methodName(id string) string {
	parts := strings.SplitN(id, ".", 2)
	if len(parts) == 2 {
		return parts[1]
	}
	return id
}

func extractMethodCalls(content string) []string {
	var calls []string
	seen := make(map[string]bool)

	words := strings.FieldsFunc(content, func(r rune) bool {
		switch r {
		case '(', ')', '\n', ' ', '\t', '.', ';', ',', '{', '}', '[', ']':
			return true
		default:
			return false
		}
	})

	for _, word := range words {
		word = strings.TrimSpace(word)
		if len(word) <= 3 || strings.HasPrefix(word, "//") || strings.HasPrefix(word, "/*") || seen[word] {
			continue
		}
		calls = append(calls, word)
		seen[word] = true
	}

	return calls
}

// firstNonEmptyLine returns the first non-empty, non-comment line from content.
func firstNonEmptyLine(content string) string {
	for _, line := range strings.Split(content, "\n") {
		trimmed := strings.TrimSpace(line)
		if trimmed != "" && !strings.HasPrefix(trimmed, "//") && !strings.HasPrefix(trimmed, "/*") && !strings.HasPrefix(trimmed, "*") {
			return trimmed
		}
	}
	return ""
}
