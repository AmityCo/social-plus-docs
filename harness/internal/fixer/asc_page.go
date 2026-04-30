package fixer

import (
	"fmt"
	"os"
	"sort"
	"strings"

	"social-plus/harness/internal/pages"
)

// FixAscPage rewrites the asc_page field in snippetFile from a legacy URL
// to a docs.json relative path using fuzzy matching.
func FixAscPage(snippetFile, currentAscPage string, reg *pages.Registry) (string, error) {
	newPath, bestCandidate := fuzzyMatchWithDiag(currentAscPage, reg)
	if newPath == "" {
		if bestCandidate != "" {
			return "", fmt.Errorf("no fuzzy match found for %q in docs.json (best candidate: %q)", currentAscPage, bestCandidate)
		}
		return "", fmt.Errorf("no fuzzy match found for %q in docs.json", currentAscPage)
	}

	content, err := os.ReadFile(snippetFile)
	if err != nil {
		return "", fmt.Errorf("read snippet: %w", err)
	}

	lines := strings.Split(string(content), "\n")
	found := false
	for j, line := range lines {
		trimmedLine := strings.TrimSpace(line)
		if strings.HasPrefix(trimmedLine, "asc_page:") {
			val := strings.TrimSpace(strings.TrimPrefix(trimmedLine, "asc_page:"))
			if val == currentAscPage {
				// Preserve leading whitespace (indentation)
				indent := line[:len(line)-len(strings.TrimLeft(line, " \t"))]
				lines[j] = indent + "asc_page: " + newPath
				found = true
				break
			}
		}
	}
	if !found {
		return "", fmt.Errorf("asc_page %q not found in snippet %q", currentAscPage, snippetFile)
	}

	updated := strings.Join(lines, "\n")
	if err := os.WriteFile(snippetFile, []byte(updated), 0o644); err != nil {
		return "", fmt.Errorf("write snippet: %w", err)
	}
	return newPath, nil
}

// platformStopWords are URL segments that identify SDK platforms but never
// appear in docs.json paths (which are cross-platform). Skipped during scoring.
var platformStopWords = map[string]bool{
	"ios": true, "android": true, "flutter": true,
	"typescript": true, "web": true, "javascript": true,
	"kotlin": true, "swift": true, "dart": true,
	"amity": true, "docs": true, "co": true,
}

// fuzzyMatchWithDiag returns (matched path, best candidate even if below threshold).
func fuzzyMatchWithDiag(legacyURL string, reg *pages.Registry) (string, string) {
	return fuzzyMatchWithMinScore(legacyURL, reg, requiredScore)
}

// fuzzyMatchWithMinScore is the core fuzzy match implementation with a configurable
// minimum-score function, enabling different strictness levels for different callers.
func fuzzyMatchWithMinScore(legacyURL string, reg *pages.Registry, minScoreFn func([]string) int) (string, string) {
	clean := strings.TrimSpace(strings.ToLower(legacyURL))
	for _, prefix := range []string{"https://", "http://"} {
		if strings.HasPrefix(clean, prefix) {
			clean = strings.TrimPrefix(clean, prefix)
			if idx := strings.Index(clean, "/"); idx >= 0 {
				clean = clean[idx+1:]
			}
			break
		}
	}

	// Filter out platform stop-words and URL fragments — they don't appear in docs.json paths.
	var segments []string
	for _, s := range strings.Split(clean, "/") {
		// Strip URL fragments (e.g. "channel-management#metadata" → "channel-management")
		if idx := strings.Index(s, "#"); idx >= 0 {
			s = s[:idx]
		}
		if s != "" && !platformStopWords[s] {
			segments = append(segments, s)
		}
	}
	if len(segments) == 0 {
		return "", ""
	}

	paths := reg.All()
	sort.Strings(paths) // deterministic tie-breaking: alphabetically first wins

	bestScore := 0
	bestPath := ""
	minScore := minScoreFn(segments)
	for _, path := range paths {
		score := matchScore(strings.ToLower(path), segments)
		if score > bestScore {
			bestScore = score
			bestPath = path
		}
	}
	if bestScore < minScore {
		return "", bestPath // bestPath is best candidate even if no match
	}
	return bestPath, ""
}

// fuzzyMatch is a simple wrapper kept for backward compatibility.
func fuzzyMatch(legacyURL string, reg *pages.Registry) string {
	p, _ := fuzzyMatchWithDiag(legacyURL, reg)
	return p
}

// strictRequiredScore requires at least 2 matching segments (for automated, unreviewed normalization).
// This prevents spurious single-segment matches (e.g. "social" matching any social-plus-sdk page).
func strictRequiredScore(segments []string) int {
	if len(segments) <= 1 {
		return 1
	}
	return 2
}

// NormalizeAscPage normalizes an asc_page value to a docs.json relative path.
// If rawPage is already a relative path (no "://"), it is returned as-is.
// If rawPage is an absolute URL, strict fuzzy matching (min 2 segments) is used.
// Returns "" if the URL cannot be matched confidently to any known docs.json path.
func NormalizeAscPage(rawPage string, reg *pages.Registry) string {
	if !strings.Contains(rawPage, "://") {
		return rawPage
	}
	p, _ := fuzzyMatchWithMinScore(rawPage, reg, strictRequiredScore)
	return p
}

func matchScore(path string, segments []string) int {
	pathSegments := strings.Split(path, "/")
	seen := make(map[string]bool, len(pathSegments))
	for _, segment := range pathSegments {
		if segment == "" {
			continue
		}
		seen[segment] = true
	}

	score := 0
	for _, segment := range segments {
		if segment != "" && seen[segment] {
			score++
		}
	}
	return score
}

func requiredScore(segments []string) int {
	// With only ~81 pages in docs.json vs. highly specific legacy URLs,
	// require just 1 matching segment — best match wins.
	return 1
}
