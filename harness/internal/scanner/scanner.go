package scanner

import (
	"bufio"
	"os"
	"path/filepath"
	"strings"
)

type Snippet struct {
	Filename    string
	SpDocsPage  string
	Description string
	File        string
	Content     string
	Platform    string
}

// matchesPlatform returns true if the file extension matches the expected platform.
func matchesPlatform(path, platform string) bool {
	lower := strings.ToLower(path)
	switch platform {
	case "android":
		return strings.HasSuffix(lower, ".kt") || strings.HasSuffix(lower, ".java")
	case "ios":
		return strings.HasSuffix(lower, ".swift")
	case "flutter":
		return strings.HasSuffix(lower, ".dart")
	case "typescript":
		return strings.HasSuffix(lower, ".ts") || strings.HasSuffix(lower, ".tsx")
	default:
		return true
	}
}

func Scan(dir, platform string) ([]Snippet, error) {
	var results []Snippet
	err := filepath.WalkDir(dir, func(path string, d os.DirEntry, err error) error {
		if err != nil || d.IsDir() {
			return err
		}
		if !matchesPlatform(path, platform) {
			return nil
		}
		snips, err := scanFile(path, platform)
		if err != nil {
			return err
		}
		results = append(results, snips...)
		return nil
	})
	return results, err
}

func scanFile(path, platform string) ([]Snippet, error) {
	f, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer f.Close()

	var results []Snippet
	var inBlock bool
	var inMeta bool
	var current Snippet
	var contentLines []string

	sc := bufio.NewScanner(f)
	for sc.Scan() {
		line := sc.Text()
		trimmed := strings.TrimSpace(line)

		if strings.Contains(trimmed, "begin_sample_code") {
			inBlock = true
			inMeta = true
			current = Snippet{File: path, Platform: platform}
			contentLines = nil
			continue
		}
		if strings.Contains(trimmed, "end_sample_code") {
			current.Content = strings.TrimSpace(strings.Join(contentLines, "\n"))
			results = append(results, current)
			inBlock = false
			inMeta = false
			continue
		}
		if inBlock {
			if inMeta {
				if parseMetaField(trimmed, "sp_docs_page:", &current.SpDocsPage) ||
					parseMetaField(trimmed, "asc_page:", &current.SpDocsPage) || // backward compat
					parseMetaField(trimmed, "filename:", &current.Filename) ||
					parseMetaField(trimmed, "description:", &current.Description) {
					continue
				}
				if strings.HasSuffix(trimmed, "*/") {
					inMeta = false
					continue
				}
				continue
			}
			contentLines = append(contentLines, line)
		}
	}
	return results, sc.Err()
}

func parseMetaField(line, prefix string, target *string) bool {
	if strings.HasPrefix(line, prefix) {
		*target = strings.TrimSpace(strings.TrimPrefix(line, prefix))
		return true
	}
	return false
}
