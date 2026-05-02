package placer

import (
	"os"
	"path/filepath"
	"regexp"
	"strings"
)

// Component is one unplaced import found in an MDX page.
type Component struct {
	Name           string `json:"name"`
	Key            string `json:"key"`
	ImportPath     string `json:"import_path"`
	SnippetPreview string `json:"snippet_preview"`
}

// PageTask is the placement job for one MDX page.
type PageTask struct {
	PageFile   string      `json:"page_file"`
	PagePath   string      `json:"page_path"`
	Components []Component `json:"components"`
}

var importRe = regexp.MustCompile(`(?m)^import\s+(\w+)\s+from\s+'(/snippets/[^']+\.mdx)'\s*;`)

// FindUnplaced scans mdxFile and returns all imported snippet components whose
// <Name /> tag is absent from the file body. docsBase is the absolute path to
// the docs root (used to resolve snippet preview files). pageRelPath is the
// docs-relative page path (no .mdx extension).
func FindUnplaced(mdxFile, pageRelPath, docsBase string) (PageTask, error) {
	data, err := os.ReadFile(mdxFile)
	if err != nil {
		return PageTask{}, err
	}
	content := string(data)

	// Strip all import lines to get the body for tag-presence checks.
	body := importRe.ReplaceAllString(content, "")

	var components []Component
	for _, m := range importRe.FindAllStringSubmatch(content, -1) {
		name, importPath := m[1], m[2]
		if strings.Contains(body, "<"+name) {
			continue
		}
		preview := resolveSnippetPreview(importPath, docsBase)
		components = append(components, Component{
			Name:           name,
			Key:            importPathToKey(importPath),
			ImportPath:     importPath,
			SnippetPreview: preview,
		})
	}

	return PageTask{
		PageFile:   mdxFile,
		PagePath:   pageRelPath,
		Components: components,
	}, nil
}

func importPathToKey(importPath string) string {
	base := filepath.Base(importPath)
	return strings.TrimSuffix(base, ".mdx")
}

func resolveSnippetPreview(importPath, docsBase string) string {
	rel := strings.TrimPrefix(importPath, "/")
	absPath := filepath.Join(docsBase, filepath.FromSlash(rel))
	data, err := os.ReadFile(absPath)
	if err != nil {
		return ""
	}
	lines := strings.Split(string(data), "\n")
	if len(lines) > 40 {
		lines = lines[:40]
	}
	return strings.Join(lines, "\n")
}
