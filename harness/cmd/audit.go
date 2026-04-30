package main

import (
	"flag"
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"time"

	"social-plus/harness/internal/config"
	"social-plus/harness/internal/differ"
	"social-plus/harness/internal/docgen"
	"social-plus/harness/internal/extractor"
	"social-plus/harness/internal/fixer"
	"social-plus/harness/internal/matcher"
	"social-plus/harness/internal/pages"
	"social-plus/harness/internal/report"
	"social-plus/harness/internal/scanner"
	"social-plus/harness/internal/manifest"
)

func runAudit(args []string) {
	fs := flag.NewFlagSet("audit", flag.ExitOnError)
	cfgPath := fs.String("config", "harness-config.yml", "path to harness-config.yml")
	reportPath := fs.String("report", "harness-report.json", "output report path")
	failOnFindings := fs.Bool("fail-on-findings", false, "exit non-zero if open findings exist")
	if err := fs.Parse(args); err != nil {
		fmt.Fprintf(os.Stderr, "parse flags: %v\n", err)
		os.Exit(1)
	}

	cfg, err := config.Load(*cfgPath)
	if err != nil {
		fmt.Fprintf(os.Stderr, "load config: %v\n", err)
		os.Exit(1)
	}

	docsJSON := filepath.Join(filepath.Dir(*cfgPath), cfg.Docs.Path, "docs.json")
	reg, err := pages.Load(docsJSON)
	if err != nil {
		fmt.Fprintf(os.Stderr, "load pages: %v\n", err)
		os.Exit(1)
	}

	var existing *report.Report
	if r, err := report.Read(*reportPath); err == nil {
		existing = r
	}

	var allFindings []report.Finding
	if existing != nil {
		for _, f := range existing.Findings {
			if f.Status == report.StatusFixed || f.Status == report.StatusNeedsHuman {
				allFindings = append(allFindings, f)
			}
		}
	}

	var allSnips []scanner.Snippet
	for platform, sdkCfg := range cfg.SDKs {
		sdkPath := filepath.Join(filepath.Dir(*cfgPath), sdkCfg.Path)
		snippetPath := filepath.Join(sdkPath, sdkCfg.SnippetDir)

		fns, err := extractor.Scan(sdkPath, platform)
		if err != nil {
			fmt.Fprintf(os.Stderr, "extract %s: %v\n", platform, err)
			continue
		}

		snips, err := scanner.Scan(snippetPath, platform)
		if err != nil {
			fmt.Fprintf(os.Stderr, "scan snippets %s: %v\n", platform, err)
			continue
		}
		allSnips = append(allSnips, snips...) // collect for DOC_PAGE_STALE_IMPORT below

		// TODO: Load MDX content for each snippet's asc_page and call differ.DiffWithMDX
		// to enable DOC_SURFACE_DRIFT and SNIPPET_CONTENT_DRIFT detection.
		// For now, only MISSING_SNIPPET, ASC_PAGE_INVALID, and DOC_MISSING are active.
		findings := differ.Diff(fns, snips, reg, platform)

		newCount := 0
		for _, f := range findings {
			if isAlreadyInReport(allFindings, f.ID) {
				continue
			}
			allFindings = append(allFindings, f)
			newCount++
		}

		fmt.Printf("[%s] %d public functions, %d snippets, %d new findings\n",
			platform, len(fns), len(snips), newCount)
	}

	// Audit doc pages for stale imports (DOC_PAGE_STALE_IMPORT)
	{
		// Normalize absolute URL sp_docs_pages before grouping
		for i, s := range allSnips {
			if strings.Contains(s.SpDocsPage, "://") {
				if norm := fixer.NormalizeAscPage(s.SpDocsPage, reg); norm != "" {
					allSnips[i].SpDocsPage = norm
				}
			}
		}
		allGroups := docgen.GroupSnippets(allSnips)
		m := matcher.New(allGroups)
		snippetsDir := "snippets"
		docsBase := filepath.Join(filepath.Dir(*cfgPath), cfg.Docs.Path)

		_ = filepath.WalkDir(docsBase, func(path string, d os.DirEntry, walkErr error) error {
			if walkErr != nil || d.IsDir() || !strings.HasSuffix(path, ".mdx") {
				return walkErr
			}
			rel, relErr := filepath.Rel(docsBase, path)
			if relErr != nil {
				return nil
			}
			docPagePath := filepath.ToSlash(strings.TrimSuffix(rel, ".mdx"))
			docFindings := differ.DiffDocPages(docPagePath, path, m, snippetsDir)
			for _, f := range docFindings {
				if !isAlreadyInReport(allFindings, f.ID) {
					allFindings = append(allFindings, f)
				}
			}
			return nil
		})

		staleCount := 0
		for _, f := range allFindings {
			if f.Type == report.TypeDocPageStaleImport && f.Status == report.StatusOpen {
				staleCount++
			}
		}
		if staleCount > 0 {
			fmt.Printf("[audit] %d DOC_PAGE_STALE_IMPORT findings\n", staleCount)
		}
	}

	// Manifest coverage block
	{
		docsBase := filepath.Join(filepath.Dir(*cfgPath), cfg.Docs.Path)
		snippetsAbsDir := filepath.Join(docsBase, "snippets")
		manifestCount := 0
		addedCount := 0
		_ = filepath.WalkDir(docsBase, func(path string, d os.DirEntry, walkErr error) error {
			if walkErr != nil {
				return walkErr
			}
			if d.IsDir() {
				rel, _ := filepath.Rel(docsBase, path)
				if rel == "harness" || strings.HasPrefix(filepath.ToSlash(rel)+"/", "harness/") {
					return filepath.SkipDir
				}
				return nil
			}
			if !strings.HasSuffix(path, ".manifest.yml") {
				return nil
			}
			rel, relErr := filepath.Rel(docsBase, path)
			if relErr != nil {
				return nil
			}
			pagePath := strings.TrimSuffix(rel, ".manifest.yml")
			pagePath = filepath.ToSlash(pagePath)
			m, _, err := manifest.LoadForPage(docsBase, pagePath)
			if err != nil {
				fmt.Fprintf(os.Stderr, "manifest load error: %v\n", err)
				return nil
			}
			findings := differ.DiffManifestCoverage(pagePath, m, snippetsAbsDir)
			for _, f := range findings {
				if !isAlreadyInReport(allFindings, f.ID) {
					allFindings = append(allFindings, f)
					addedCount++
				}
			}
			manifestCount++
			return nil
		})
		if addedCount > 0 {
			fmt.Printf("[audit] %d manifest coverage findings from %d manifests\n", addedCount, manifestCount)
		}
	}

	r := &report.Report{
		GeneratedAt: time.Now().Format(time.RFC3339),
		Findings:    allFindings,
	}
	r.Recount()

	if err := report.Write(r, *reportPath); err != nil {
		fmt.Fprintf(os.Stderr, "write report: %v\n", err)
		os.Exit(1)
	}

	fmt.Printf("\nSummary: %d open, %d fixed, %d needs_human\n",
		r.Summary.Open, r.Summary.Fixed, r.Summary.NeedsHuman)

	if *failOnFindings && r.Summary.Open > 0 {
		os.Exit(1)
	}
}

func isAlreadyInReport(findings []report.Finding, id string) bool {
	for _, f := range findings {
		if f.ID == id {
			return true
		}
	}
	return false
}
