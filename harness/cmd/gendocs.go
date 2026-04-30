package main

import (
	"flag"
	"fmt"
	"os"
	"path/filepath"

	"social-plus/harness/internal/config"
	"social-plus/harness/internal/docgen"
	"social-plus/harness/internal/scanner"
)

func runGendocs(args []string) {
	fs := flag.NewFlagSet("gendocs", flag.ExitOnError)
	cfgPath := fs.String("config", "harness-config.yml", "path to harness-config.yml")
	dryRun := fs.Bool("dry-run", false, "print planned writes without touching files")
	outOverride := fs.String("out", "", "override output directory (default: <docs_path>/snippets)")
	if err := fs.Parse(args); err != nil {
		fmt.Fprintf(os.Stderr, "parse flags: %v\n", err)
		os.Exit(1)
	}

	cfg, err := config.Load(*cfgPath)
	if err != nil {
		fmt.Fprintf(os.Stderr, "load config: %v\n", err)
		os.Exit(1)
	}

	var allSnips []scanner.Snippet
	for platform, sdkCfg := range cfg.SDKs {
		sdkBase := filepath.Join(filepath.Dir(*cfgPath), sdkCfg.Path)
		snippetDir := filepath.Join(sdkBase, sdkCfg.SnippetDir)
		snips, scanErr := scanner.Scan(snippetDir, platform)
		if scanErr != nil {
			fmt.Fprintf(os.Stderr, "[%s] scan error: %v\n", platform, scanErr)
			os.Exit(1)
		}
		allSnips = append(allSnips, snips...)
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

	written, skipped, err := docgen.Write(outDir, groups, *dryRun, os.Stdout)
	if err != nil {
		fmt.Fprintf(os.Stderr, "write error: %v\n", err)
		os.Exit(1)
	}
	if err := docgen.WriteManifest(outDir, groups, *dryRun, os.Stdout); err != nil {
		fmt.Fprintf(os.Stderr, "manifest error: %v\n", err)
		os.Exit(1)
	}

	fmt.Printf("[gendocs] done — written: %d, skipped (human-edited): %d\n", written, skipped)
}
