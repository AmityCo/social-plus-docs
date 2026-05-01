package main

import (
	"flag"
	"fmt"
	"os"
	"path/filepath"
	"sort"

	"social-plus/harness/internal/config"
	"social-plus/harness/internal/paritymap"
	"social-plus/harness/internal/scanner"
)

func runParity(args []string) {
	fs := flag.NewFlagSet("parity", flag.ExitOnError)
	cfgPath := fs.String("config", "harness-config.yml", "path to harness-config.yml")
	outPath := fs.String("out", "function-parity.json", "output parity file path")
	if err := fs.Parse(args); err != nil {
		fmt.Fprintf(os.Stderr, "parse flags: %v\n", err)
		os.Exit(1)
	}

	cfg, err := config.Load(*cfgPath)
	if err != nil {
		fmt.Fprintf(os.Stderr, "load config: %v\n", err)
		os.Exit(1)
	}
	cfgDir := filepath.Dir(*cfgPath)

	platforms := sortedPlatforms(cfg)
	var allSnips []scanner.Snippet
	for _, platform := range platforms {
		sdkCfg := cfg.SDKs[platform]
		snippetPath := filepath.Join(cfgDir, sdkCfg.Path, sdkCfg.SnippetDir)
		snips, err := scanner.Scan(snippetPath, platform)
		if err != nil {
			fmt.Fprintf(os.Stderr, "warning: skipping %s: %v\n", platform, err)
			continue
		}
		allSnips = append(allSnips, snips...)
	}

	pm := paritymap.Build(allSnips, platforms)

	dest := filepath.Join(cfgDir, *outPath)
	if err := paritymap.Write(dest, pm); err != nil {
		fmt.Fprintf(os.Stderr, "write parity: %v\n", err)
		os.Exit(1)
	}

	fmt.Printf("wrote %s (%d keys across %d platforms)\n", dest, pm.TotalKeys, len(platforms))
}

// sortedPlatforms returns cfg.SDKs keys in deterministic alphabetical order.
func sortedPlatforms(cfg *config.Config) []string {
	ps := make([]string, 0, len(cfg.SDKs))
	for p := range cfg.SDKs {
		ps = append(ps, p)
	}
	sort.Strings(ps)
	return ps
}
