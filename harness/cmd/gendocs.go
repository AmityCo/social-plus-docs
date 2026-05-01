package main

import (
	"flag"
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"social-plus/harness/internal/config"
	"social-plus/harness/internal/docgen"
	"social-plus/harness/internal/fixer"
	"social-plus/harness/internal/pages"
	"social-plus/harness/internal/scanner"
	"social-plus/harness/internal/runstate"
)

func runGendocs(args []string) {
	fs := flag.NewFlagSet("gendocs", flag.ExitOnError)
	cfgPath := fs.String("config", "harness-config.yml", "path to harness-config.yml")
	dryRun := fs.Bool("dry-run", false, "print planned writes without touching files")
	outOverride := fs.String("out", "", "override output directory (default: <docs_path>/snippets)")
	clean := fs.Bool("clean", false, "remove all AUTO-GENERATED files in outDir before writing")
	_ = fs.Parse(args)

	cfg, err := config.Load(*cfgPath)
	if err != nil {
		fmt.Fprintf(os.Stderr, "load config: %v\n", err)
		os.Exit(1)
	}
	cfgDir := filepath.Dir(*cfgPath)
	_ = runstate.Start(cfgDir, "gendocs", "ai_agent", cfg.LLM.Model)

	var allSnips []scanner.Snippet
	for platform, sdkCfg := range cfg.SDKs {
		sdkBase := filepath.Join(filepath.Dir(*cfgPath), sdkCfg.Path)
		snippetDir := filepath.Join(sdkBase, sdkCfg.SnippetDir)
		snips, scanErr := scanner.Scan(snippetDir, platform)
		if scanErr != nil {
			fmt.Fprintf(os.Stderr, "[%s] scan error (skipping): %v\n", platform, scanErr)
			continue
		}
		allSnips = append(allSnips, snips...)
	}

	// Normalize absolute URL asc_pages to docs.json relative paths.
	docsJSONPath := filepath.Join(filepath.Dir(*cfgPath), cfg.Docs.Path, "docs.json")
	reg, regErr := pages.Load(docsJSONPath)
	if regErr != nil {
		fmt.Fprintf(os.Stderr, "load pages registry: %v\n", regErr)
		_ = runstate.Fail(cfgDir, "gendocs", "see stderr")
		os.Exit(1)
	}
	normalizedCount := 0
	skippedURLCount := 0
	for i, s := range allSnips {
		if strings.Contains(s.SpDocsPage, "://") {
			newPage := fixer.NormalizeAscPage(s.SpDocsPage, reg)
			if newPage != "" {
				allSnips[i].SpDocsPage = newPage
				normalizedCount++
			} else {
				skippedURLCount++
			}
		}
	}
	if normalizedCount > 0 || skippedURLCount > 0 {
		fmt.Printf("[gendocs] URL sp_docs_pages: %d normalized, %d unmappable (skipped)\n", normalizedCount, skippedURLCount)
	}

	groups := docgen.GroupSnippets(allSnips)
	fmt.Printf("[gendocs] %d snippets → %d groups\n", len(allSnips), len(groups))

	outDir := *outOverride
	if outDir == "" {
		outDir = filepath.Join(filepath.Dir(*cfgPath), cfg.Docs.Path, "snippets")
	}
	if *dryRun {
		fmt.Println("[gendocs] DRY RUN — no files will be written")
	}

	if *clean {
		removed, cleanErr := docgen.CleanDir(outDir)
		if cleanErr != nil {
			fmt.Fprintf(os.Stderr, "clean error: %v\n", cleanErr)
			_ = runstate.Fail(cfgDir, "gendocs", "see stderr")
			os.Exit(1)
		}
		fmt.Printf("[gendocs] --clean: removed %d stale AUTO-GENERATED files\n", removed)
	}

	written, skipped, err := docgen.Write(outDir, groups, *dryRun, os.Stdout)
	if err != nil {
		fmt.Fprintf(os.Stderr, "write error: %v\n", err)
		_ = runstate.Fail(cfgDir, "gendocs", "see stderr")
		os.Exit(1)
	}
	if err := docgen.WriteManifest(outDir, groups, *dryRun, os.Stdout); err != nil {
		fmt.Fprintf(os.Stderr, "manifest error: %v\n", err)
		_ = runstate.Fail(cfgDir, "gendocs", "see stderr")
		os.Exit(1)
	}

	_ = runstate.Finish(cfgDir, "gendocs", fmt.Sprintf("written: %d, skipped: %d", written, skipped))
	fmt.Printf("[gendocs] done — written: %d, skipped (human-edited): %d\n", written, skipped)
}
