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

		docPageFile := f.DocPageFile
		if docPageFile == "" {
			docPageFile = filepath.Join(docsBase, filepath.FromSlash(f.DocPage)+".mdx")
		}

		componentName := migrator.KebabToPascal(f.GendocsKey)
		importPath := "/snippets/" + strings.ReplaceAll(f.GendocsPath, string(os.PathSeparator), "/")

		if err := migrator.Run(docPageFile, componentName, importPath, f.HasHardcodedCodeGroup, *dryRun); err != nil {
			fmt.Fprintf(os.Stderr, "[migrate] ERROR %s: %v\n", f.DocPage, err)
			warned++
			continue
		}
		if *dryRun {
			skipped++
		} else {
			written++
			fmt.Printf("[migrate] DONE: %s → import %s\n", f.DocPage, componentName)
		}
	}

	fmt.Printf("[migrate] done — written: %d, dry-run skipped: %d, errors: %d\n", written, skipped, warned)
}
