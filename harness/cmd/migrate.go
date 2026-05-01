package main

import (
	"flag"
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"social-plus/harness/internal/config"
	"social-plus/harness/internal/migrator"
	"social-plus/harness/internal/report"
	"social-plus/harness/internal/manifest"
)

func runMigrate(args []string) {
	fs := flag.NewFlagSet("migrate", flag.ExitOnError)
	cfgPath := fs.String("config", "harness-config.yml", "path to harness-config.yml")
	reportPath := fs.String("report", "harness-report.json", "path to harness-report.json from audit")
	dryRun := fs.Bool("dry-run", false, "print planned changes without modifying files")
	_ = fs.Parse(args)

	cfg, err := config.Load(*cfgPath)
	if err != nil {
		fmt.Fprintf(os.Stderr, "load config: %v\n", err)
		os.Exit(1)
	}

	r, err := report.Read(*reportPath)
	if err != nil {
		fmt.Fprintf(os.Stderr, "read report: %v\n", err)
		os.Exit(1)
	}

	docsBase := filepath.Join(filepath.Dir(*cfgPath), cfg.Docs.Path)

	written, skipped, warned := 0, 0, 0
	for _, f := range r.Findings {
		if f.Type != report.TypeDocPageStaleImport || f.Status != report.StatusOpen {
			continue
		}
		// Skip pages outside configured scope
		if cfg.Docs.Scope != "" && !strings.HasPrefix(f.DocPage, cfg.Docs.Scope+"/") {
			continue
		}

		docPageFile := f.DocPageFile
		if docPageFile == "" {
			docPageFile = filepath.Join(docsBase, filepath.FromSlash(f.DocPage)+".mdx")
		}

		componentName := migrator.KebabToPascal(f.GendocsKey)
		importPath := "/snippets/" + strings.ReplaceAll(f.GendocsPath, string(os.PathSeparator), "/")

		// --- Begin manifest-aware migration logic ---
		content, err := os.ReadFile(docPageFile)
		if err != nil {
			fmt.Fprintf(os.Stderr, "[migrate] ERROR reading %s: %v\n", docPageFile, err)
			warned++
			continue
		}

		updated := migrator.AddImport(string(content), componentName, importPath)
		manifestUsed := false
		if f.HasHardcodedCodeGroup {
			m, found, err := manifest.LoadForPage(docsBase, f.DocPage)
			if err != nil {
				fmt.Fprintf(os.Stderr, "[migrate] ERROR loading manifest for %s: %v\n", f.DocPage, err)
				warned++
				continue
			}
			if found {
				if sectionKey, ok := m.SectionForSnippet(f.GendocsKey); ok {
					sec := m.Sections[sectionKey]
					if replaced, ok := migrator.ReplaceCodeGroupAfterHeading(updated, sec.Heading, componentName); ok {
						updated = replaced
						manifestUsed = true
					}
				}
			}
			if !manifestUsed {
				if replaced, ok := migrator.ReplaceCodeGroup(updated, componentName); ok {
					updated = replaced
				} else {
					fmt.Printf("[migrate] WARN: CodeGroup not found in %s — import added, CodeGroup left in place\n", docPageFile)
				}
			}
		}
		if *dryRun {
			fmt.Printf("[migrate] DRY RUN: would update %s\n  + import %s from '%s'\n", docPageFile, componentName, importPath)
			skipped++
			continue
		}
		if err := os.WriteFile(docPageFile, []byte(updated), 0o644); err != nil {
			fmt.Fprintf(os.Stderr, "[migrate] ERROR writing %s: %v\n", docPageFile, err)
			warned++
			continue
		}
		written++
		fmt.Printf("[migrate] DONE: %s → import %s\n", f.DocPage, componentName)
		// --- End manifest-aware migration logic ---
	}

	fmt.Printf("[migrate] done — written: %d, dry-run skipped: %d, errors: %d\n", written, skipped, warned)
}
