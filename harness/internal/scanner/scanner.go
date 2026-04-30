package scanner

import (
	"bufio"
	"os"
	"path/filepath"
	"strings"
)

type Snippet struct {
	GistID      string
	Filename    string
	AscPage     string
	Description string
	File        string
	Content     string
	Platform    string
}

func Scan(dir, platform string) ([]Snippet, error) {
	var results []Snippet
	err := filepath.WalkDir(dir, func(path string, d os.DirEntry, err error) error {
		if err != nil || d.IsDir() {
			return err
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
	var current Snippet
	var contentLines []string

	sc := bufio.NewScanner(f)
	for sc.Scan() {
		line := sc.Text()
		trimmed := strings.TrimSpace(line)

		if strings.Contains(trimmed, "begin_sample_code") {
			inBlock = true
			current = Snippet{File: path, Platform: platform}
			contentLines = nil
			continue
		}
		if strings.Contains(trimmed, "end_sample_code") {
			current.Content = strings.TrimSpace(strings.Join(contentLines, "\n"))
			results = append(results, current)
			inBlock = false
			continue
		}
		if inBlock {
			if parseMetaField(trimmed, "gist_id:", &current.GistID) ||
				parseMetaField(trimmed, "filename:", &current.Filename) ||
				parseMetaField(trimmed, "asc_page:", &current.AscPage) ||
				parseMetaField(trimmed, "description:", &current.Description) {
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
