package config

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"gopkg.in/yaml.v3"
)

// Page is a single documentation page entry.
type Page struct {
	Path        string `yaml:"path"`
	Description string `yaml:"description,omitempty"`
}

// Section groups pages under a heading.
type Section struct {
	Title string `yaml:"title"`
	Pages []Page `yaml:"pages"`
}

// Config is the top-level structure of llms-config.yml.
type Config struct {
	SiteURL     string    `yaml:"site_url"`
	Title       string    `yaml:"title"`
	Description string    `yaml:"description"`
	DocsRoot    string    `yaml:"docs_root"`
	OutputDir   string    `yaml:"output_dir"`
	Sections    []Section `yaml:"sections"`

	configDir string // directory of the loaded config file
}

// ResolvedDocsRoot returns the absolute path to the docs root.
func (c *Config) ResolvedDocsRoot() string {
	return resolve(c.configDir, c.DocsRoot)
}

// ResolvedOutputDir returns the absolute path to the output directory.
func (c *Config) ResolvedOutputDir() string {
	return resolve(c.configDir, c.OutputDir)
}

// NormalisedSiteURL returns SiteURL without a trailing slash.
func (c *Config) NormalisedSiteURL() string {
	return strings.TrimRight(c.SiteURL, "/")
}

// Load reads and validates the config file at path.
func Load(path string) (*Config, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, fmt.Errorf("read config %q: %w", path, err)
	}

	var cfg Config
	if err := yaml.Unmarshal(data, &cfg); err != nil {
		return nil, fmt.Errorf("parse config %q: %w", path, err)
	}

	if err := cfg.validate(); err != nil {
		return nil, err
	}

	cfg.configDir = filepath.Dir(filepath.Clean(path))
	return &cfg, nil
}

// New creates a Config directly from pre-resolved paths.
// docsRoot and outputDir must be absolute paths; relative paths are stored
// as-is and will not be resolved against any base directory (no configDir is set).
// Intended for tests and programmatic generation.
func New(siteURL, title, description, docsRoot, outputDir string, sections []Section) (*Config, error) {
	cfg := &Config{
		SiteURL:     siteURL,
		Title:       title,
		Description: description,
		DocsRoot:    docsRoot,
		OutputDir:   outputDir,
		Sections:    sections,
	}
	if err := cfg.validate(); err != nil {
		return nil, err
	}
	return cfg, nil
}

func (c *Config) validate() error {
	if c.SiteURL == "" {
		return fmt.Errorf("config: site_url is required")
	}
	if c.Title == "" {
		return fmt.Errorf("config: title is required")
	}
	if c.DocsRoot == "" {
		return fmt.Errorf("config: docs_root is required")
	}
	if c.OutputDir == "" {
		return fmt.Errorf("config: output_dir is required")
	}
	if len(c.Sections) == 0 {
		return fmt.Errorf("config: at least one section is required")
	}
	return nil
}

// resolve returns the absolute path of rel, resolved against base.
// If rel is already absolute, it is returned unchanged.
func resolve(base, rel string) string {
	if filepath.IsAbs(rel) {
		return rel
	}
	if base == "" {
		return rel
	}
	return filepath.Clean(filepath.Join(base, rel))
}
