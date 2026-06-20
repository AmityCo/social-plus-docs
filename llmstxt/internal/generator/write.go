package generator

import (
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"social-plus/llmstxt/internal/config"
	"social-plus/llmstxt/internal/parser"
)

type renderedPage struct {
	URL         string
	Title       string
	Description string
	Body        string
}

type renderedSection struct {
	Title string
	Pages []renderedPage
}

// Generate loads all pages, strips MDX, and writes llms.txt and llms-full.txt
// to cfg.ResolvedOutputDir().
func Generate(cfg *config.Config, verbose bool) error {
	if err := ValidatePages(cfg); err != nil {
		return err
	}

	llmsTxt, llmsFullTxt := Render(cfg, verbose)

	outDir := cfg.ResolvedOutputDir()
	if err := os.MkdirAll(outDir, 0755); err != nil {
		return fmt.Errorf("create output dir %q: %w", outDir, err)
	}
	if err := writeAtomic(filepath.Join(outDir, "llms.txt"), llmsTxt); err != nil {
		return fmt.Errorf("write llms.txt: %w", err)
	}
	if err := writeAtomic(filepath.Join(outDir, "llms-full.txt"), llmsFullTxt); err != nil {
		return fmt.Errorf("write llms-full.txt: %w", err)
	}
	return nil
}

// ValidatePages returns an error if any configured page path does not exist.
func ValidatePages(cfg *config.Config) error {
	missing := MissingPages(cfg)
	if len(missing) == 0 {
		return nil
	}

	var sb strings.Builder
	sb.WriteString("llms config references missing page(s):")
	for _, path := range missing {
		sb.WriteString("\n  - " + path)
	}
	return errors.New(sb.String())
}

// MissingPages returns the configured page paths that cannot be read.
func MissingPages(cfg *config.Config) []string {
	docsRoot := cfg.ResolvedDocsRoot()
	var missing []string
	for _, sec := range cfg.Sections {
		for _, pg := range sec.Pages {
			fullPath := filepath.Join(docsRoot, pg.Path)
			if _, err := os.Stat(fullPath); err != nil {
				missing = append(missing, pg.Path)
			}
		}
	}
	return missing
}

// Render returns both output file contents as strings without writing them.
// Used by dry-run mode and tests.
func Render(cfg *config.Config, verbose bool) (llmsTxt, llmsFullTxt string) {
	sections := loadSections(cfg, verbose)
	return trimTrailingWhitespace(buildIndex(cfg, sections)), trimTrailingWhitespace(buildFull(cfg, sections))
}

func loadSections(cfg *config.Config, verbose bool) []renderedSection {
	docsRoot := cfg.ResolvedDocsRoot()
	siteURL := cfg.NormalisedSiteURL()

	var out []renderedSection
	for _, sec := range cfg.Sections {
		rs := renderedSection{Title: sec.Title}
		for _, pg := range sec.Pages {
			fullPath := filepath.Join(docsRoot, pg.Path)
			data, err := os.ReadFile(fullPath)
			if err != nil {
				fmt.Fprintf(os.Stderr, "warning: skipping %q: %v\n", pg.Path, err)
				continue
			}

			parsed := parser.Parse(data)

			// Config-level description overrides frontmatter.
			if pg.Description != "" {
				parsed.Description = pg.Description
			}
			// Final fallback: derive title from file path.
			if parsed.Title == "" {
				parsed.Title = parser.TitleFromPath(pg.Path)
			}

			urlPath := strings.TrimSuffix(pg.Path, ".mdx")
			url := siteURL + "/" + urlPath

			if verbose {
				fmt.Printf("  processed: %s\n", pg.Path)
			}

			rs.Pages = append(rs.Pages, renderedPage{
				URL:         url,
				Title:       parsed.Title,
				Description: parsed.Description,
				Body:        parsed.Body,
			})
		}
		out = append(out, rs)
	}
	return out
}

// buildIndex assembles the concise llms.txt index.
func buildIndex(cfg *config.Config, sections []renderedSection) string {
	var sb strings.Builder
	sb.WriteString("# " + cfg.Title + "\n\n")
	if cfg.Description != "" {
		for _, line := range strings.Split(strings.TrimSpace(cfg.Description), "\n") {
			sb.WriteString("> " + strings.TrimSpace(line) + "\n")
		}
		sb.WriteString("\n")
	}
	for _, sec := range sections {
		sb.WriteString("## " + sec.Title + "\n\n")
		for _, pg := range sec.Pages {
			entry := fmt.Sprintf("- [%s](%s)", pg.Title, pg.URL)
			if pg.Description != "" {
				entry += ": " + pg.Description
			}
			sb.WriteString(entry + "\n")
		}
		sb.WriteString("\n")
	}
	return sb.String()
}

// buildFull assembles llms-full.txt with each page's complete content inlined.
func buildFull(cfg *config.Config, sections []renderedSection) string {
	var sb strings.Builder
	sb.WriteString("# " + cfg.Title + "\n\n")
	if cfg.Description != "" {
		for _, line := range strings.Split(strings.TrimSpace(cfg.Description), "\n") {
			sb.WriteString("> " + strings.TrimSpace(line) + "\n")
		}
		sb.WriteString("\n")
	}
	for _, sec := range sections {
		sb.WriteString("## " + sec.Title + "\n\n")
		for i, pg := range sec.Pages {
			sb.WriteString(fmt.Sprintf("### [%s](%s)\n\n", pg.Title, pg.URL))
			if pg.Description != "" {
				sb.WriteString("> " + pg.Description + "\n\n")
			}
			if pg.Body != "" {
				sb.WriteString(pg.Body + "\n")
			}
			if i < len(sec.Pages)-1 {
				sb.WriteString("\n---\n\n")
			}
		}
		sb.WriteString("\n")
	}
	return sb.String()
}

func trimTrailingWhitespace(s string) string {
	var sb strings.Builder
	sb.Grow(len(s))
	for _, line := range strings.SplitAfter(s, "\n") {
		if strings.HasSuffix(line, "\n") {
			sb.WriteString(strings.TrimRight(strings.TrimSuffix(line, "\n"), " \t"))
			sb.WriteString("\n")
			continue
		}
		sb.WriteString(strings.TrimRight(line, " \t"))
	}
	return sb.String()
}

// writeAtomic writes content to a temp file in the same directory as path,
// then renames it atomically to path.
func writeAtomic(path, content string) error {
	dir := filepath.Dir(path)
	tmp, err := os.CreateTemp(dir, ".llmstxt-tmp-*")
	if err != nil {
		return err
	}
	tmpPath := tmp.Name()
	if _, err := tmp.WriteString(content); err != nil {
		tmp.Close()
		os.Remove(tmpPath)
		return err
	}
	if err := tmp.Close(); err != nil {
		os.Remove(tmpPath)
		return err
	}
	if err := os.Rename(tmpPath, path); err != nil {
		os.Remove(tmpPath)
		return err
	}
	return nil
}
