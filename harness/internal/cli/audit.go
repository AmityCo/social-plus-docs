package cli

import (
	"flag"
	"fmt"
	"os"
	"path/filepath"
	"time"

	"social-plus/harness/internal/config"
	"social-plus/harness/internal/differ"
	"social-plus/harness/internal/extractor"
	"social-plus/harness/internal/pages"
	"social-plus/harness/internal/report"
	"social-plus/harness/internal/scanner"
)

func RunAudit(args []string) {
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

		findings := differ.Diff(fns, snips, reg, platform)

		newCount := 0
		for _, f := range findings {
			if alreadyResolved(allFindings, f.ID) {
				continue
			}
			allFindings = append(allFindings, f)
			newCount++
		}

		fmt.Printf("[%s] %d public functions, %d snippets, %d new findings\n",
			platform, len(fns), len(snips), newCount)
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

func alreadyResolved(findings []report.Finding, id string) bool {
	for _, f := range findings {
		if f.ID == id {
			return true
		}
	}
	return false
}
