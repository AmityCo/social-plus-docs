package fixer

import (
	"fmt"
	"os"
	"strings"

	"social-plus/harness/internal/pages"
)

// FixAscPage rewrites the asc_page field in snippetFile from a legacy URL
// to a docs.json relative path using fuzzy matching.
func FixAscPage(snippetFile, currentAscPage string, reg *pages.Registry) (string, error) {
	newPath := fuzzyMatch(currentAscPage, reg)
	if newPath == "" {
		return "", fmt.Errorf("no fuzzy match found for %q in docs.json", currentAscPage)
	}

	content, err := os.ReadFile(snippetFile)
	if err != nil {
		return "", fmt.Errorf("read snippet: %w", err)
	}

	updated := strings.ReplaceAll(string(content), "asc_page: "+currentAscPage, "asc_page: "+newPath)
	if updated == string(content) {
		return "", fmt.Errorf("asc_page %q not found in snippet %q", currentAscPage, snippetFile)
	}
	if err := os.WriteFile(snippetFile, []byte(updated), 0o644); err != nil {
		return "", fmt.Errorf("write snippet: %w", err)
	}

	return newPath, nil
}

func fuzzyMatch(legacyURL string, reg *pages.Registry) string {
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

	segments := strings.Split(clean, "/")
	bestScore := 0
	bestPath := ""
	minScore := requiredScore(segments)
	for _, path := range reg.All() {
		score := matchScore(strings.ToLower(path), segments)
		if score > bestScore {
			bestScore = score
			bestPath = path
		}
	}
	if bestScore < minScore {
		return ""
	}

	return bestPath
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
	meaningful := 0
	for _, segment := range segments {
		if segment != "" {
			meaningful++
		}
	}
	if meaningful == 0 {
		return 1
	}
	return meaningful
}
