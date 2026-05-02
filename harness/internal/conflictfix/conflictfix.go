// Package conflictfix resolves SNIPPET_KEY_PLATFORM_CONFLICT findings by rewriting
// non-android snippet files to use Android's canonical sp_docs_page value.
package conflictfix

import (
	"fmt"
	"os"
	"strings"

	"social-plus/harness/internal/docgen"
	"social-plus/harness/internal/scanner"
)

// Resolution records a single sp_docs_page rewrite.
type Resolution struct {
	SnippetFile   string
	Key           string
	Platform      string
	OldPage       string
	CanonicalPage string
}

// Fix scans each platform directory in dirs (map of platform → absolute snippet dir path),
// identifies keys where platforms disagree on sp_docs_page, uses Android's value as canonical
// (platform priority: android wins per docgen/writer.go), and rewrites the sp_docs_page line
// in divergent non-android files.
//
// Keys with no Android entry are skipped — no canonical can be determined.
// Returns the list of applied resolutions.
func Fix(dirs map[string]string) ([]Resolution, error) {
	type entry struct {
		platform string
		page     string
		file     string
	}

	// Scan all platforms and build key → []entry map
	byKey := make(map[string][]entry)
	for platform, dir := range dirs {
		snips, err := scanner.Scan(dir, platform)
		if err != nil {
			return nil, fmt.Errorf("scan %s (%s): %w", platform, dir, err)
		}
		for _, s := range snips {
			if s.Filename == "" || s.SpDocsPage == "" || strings.Contains(s.SpDocsPage, "://") {
				continue
			}
			key := docgen.DeriveKey(s.Filename)
			if key == "" {
				continue
			}
			byKey[key] = append(byKey[key], entry{
				platform: platform,
				page:     s.SpDocsPage,
				file:     s.File,
			})
		}
	}

	var resolutions []Resolution
	for key, entries := range byKey {
		// Find android's canonical page for this key
		canonicalPage := ""
		for _, e := range entries {
			if e.platform == "android" {
				canonicalPage = e.page
				break
			}
		}
		if canonicalPage == "" {
			continue // no android entry — cannot determine canonical
		}

		// Rewrite non-android entries that differ from canonical
		for _, e := range entries {
			if e.platform == "android" || e.page == canonicalPage {
				continue
			}
			if err := rewriteSpDocsPage(e.file, canonicalPage); err != nil {
				return resolutions, fmt.Errorf("rewrite %s: %w", e.file, err)
			}
			resolutions = append(resolutions, Resolution{
				SnippetFile:   e.file,
				Key:           key,
				Platform:      e.platform,
				OldPage:       e.page,
				CanonicalPage: canonicalPage,
			})
		}
	}
	return resolutions, nil
}

// rewriteSpDocsPage reads the snippet file and replaces the sp_docs_page (or asc_page) line
// with the new canonical value, preserving all other content exactly.
func rewriteSpDocsPage(path, newPage string) error {
	data, err := os.ReadFile(path)
	if err != nil {
		return fmt.Errorf("read: %w", err)
	}
	lines := strings.Split(string(data), "\n")
	replaced := false
	for i, line := range lines {
		trimmed := strings.TrimSpace(line)
		for _, prefix := range []string{"sp_docs_page:", "asc_page:"} {
			if strings.HasPrefix(trimmed, prefix) {
				// Preserve leading whitespace
				leading := line[:len(line)-len(strings.TrimLeft(line, " \t"))]
				lines[i] = leading + "sp_docs_page: " + newPage
				replaced = true
				break
			}
		}
		if replaced {
			break
		}
	}
	if !replaced {
		return fmt.Errorf("sp_docs_page field not found in %s", path)
	}
	return os.WriteFile(path, []byte(strings.Join(lines, "\n")), 0o644)
}
