package manifest

import (
	"errors"
	"os"
	"path/filepath"

	"gopkg.in/yaml.v3"
)

// Section describes one section of a doc page and the snippet GendocsKeys that belong there.
type Section struct {
	Heading  string   `yaml:"heading"`
	Snippets []string `yaml:"snippets"`
}

// Manifest is the parsed content of a *.manifest.yml file.
type Manifest struct {
	Sections map[string]Section `yaml:"sections"`
}

// SectionForSnippet returns the section key that contains the given GendocsKey, and whether found.
func (m *Manifest) SectionForSnippet(gendocsKey string) (string, bool) {
	for key, sec := range m.Sections {
		for _, s := range sec.Snippets {
			if s == gendocsKey {
				return key, true
			}
		}
	}
	return "", false
}

// PathForPage returns the expected manifest file path for a doc page.
// docsDir is the absolute path to the docs directory; pagePath is the relative
// doc page path without extension (e.g. "social-plus-sdk/getting-started/authentication").
func PathForPage(docsDir, pagePath string) string {
	return filepath.Join(docsDir, filepath.FromSlash(pagePath)+".manifest.yml")
}

// LoadForPage loads the manifest for a doc page.
// Returns (manifest, true, nil) if found, (nil, false, nil) if not found,
// or (nil, false, err) if found but malformed.
func LoadForPage(docsDir, pagePath string) (*Manifest, bool, error) {
	path := PathForPage(docsDir, pagePath)
	data, err := os.ReadFile(path)
	if errors.Is(err, os.ErrNotExist) {
		return nil, false, nil
	}
	if err != nil {
		return nil, false, err
	}
	var m Manifest
	if err := yaml.Unmarshal(data, &m); err != nil {
		return nil, false, err
	}
	if m.Sections == nil {
		m.Sections = map[string]Section{}
	}
	return &m, true, nil
}
