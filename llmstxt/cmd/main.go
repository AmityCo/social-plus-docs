package main

import (
	"flag"
	"fmt"
	"os"

	"social-plus/llmstxt/internal/config"
	"social-plus/llmstxt/internal/generator"
)

func main() {
	configPath := flag.String("config", "./llms-config.yml", "path to llms-config.yml")
	dryRun := flag.Bool("dry-run", false, "print output to stdout instead of writing files")
	verbose := flag.Bool("verbose", false, "log each page as it is processed")
	flag.Parse()

	cfg, err := config.Load(*configPath)
	if err != nil {
		fmt.Fprintf(os.Stderr, "error: %v\n", err)
		os.Exit(1)
	}

	if *dryRun {
		llmsTxt, llmsFullTxt := generator.Render(cfg, *verbose)
		fmt.Println("=== llms.txt ===")
		fmt.Print(llmsTxt)
		fmt.Println("\n=== llms-full.txt (first 3000 chars) ===")
		preview := llmsFullTxt
		if len(preview) > 3000 {
			preview = preview[:3000] + "\n...(truncated, run without -dry-run to write full output)"
		}
		fmt.Print(preview)
		return
	}

	if err := generator.Generate(cfg, *verbose); err != nil {
		fmt.Fprintf(os.Stderr, "error: %v\n", err)
		os.Exit(2)
	}

	fmt.Printf("Done. llms.txt and llms-full.txt written to %s\n", cfg.ResolvedOutputDir())
}
