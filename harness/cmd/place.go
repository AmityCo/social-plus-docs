package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"social-plus/harness/internal/config"
	"social-plus/harness/internal/placer"
	"social-plus/harness/internal/runstate"
)

func runPlace(args []string) {
	fs := flag.NewFlagSet("place", flag.ExitOnError)
	cfgPath := fs.String("config", "harness-config.yml", "path to harness-config.yml")
	outPath := fs.String("out", "placement-tasks.json", "output task file path")
	dryRun := fs.Bool("dry-run", false, "print summary without writing task file")
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
	_ = runstate.Start(cfgDir, "place", "script", "")

	docsBase := filepath.Join(cfgDir, cfg.Docs.Path)

	var tasks []placer.PageTask

	_ = filepath.WalkDir(docsBase, func(path string, d os.DirEntry, walkErr error) error {
		if walkErr != nil {
			return walkErr
		}
		if d.IsDir() {
			rel, _ := filepath.Rel(docsBase, path)
			relSlash := filepath.ToSlash(rel)
			if rel == "harness" || strings.HasPrefix(relSlash+"/", "harness/") ||
				rel == "essentials" || strings.HasPrefix(relSlash+"/", "essentials/") ||
				rel == "snippets" || strings.HasPrefix(relSlash+"/", "snippets/") {
				return filepath.SkipDir
			}
			return nil
		}
		if !strings.HasSuffix(path, ".mdx") {
			return nil
		}
		rel, _ := filepath.Rel(docsBase, path)
		relSlash := filepath.ToSlash(rel)
		if cfg.Docs.Scope != "" && !strings.HasPrefix(relSlash, cfg.Docs.Scope+"/") {
			return nil
		}
		pagePath := strings.TrimSuffix(relSlash, ".mdx")

		task, err := placer.FindUnplaced(path, pagePath, docsBase)
		if err != nil {
			fmt.Fprintf(os.Stderr, "[place] warning: %s: %v\n", rel, err)
			return nil
		}
		if len(task.Components) > 0 {
			tasks = append(tasks, task)
		}
		return nil
	})

	totalComponents := 0
	for _, t := range tasks {
		totalComponents += len(t.Components)
	}

	if *dryRun {
		fmt.Printf("[place] DRY RUN: %d pages, %d unplaced components — no file written\n",
			len(tasks), totalComponents)
		_ = runstate.Finish(cfgDir, "place", fmt.Sprintf("dry-run: %d pages", len(tasks)))
		return
	}

	dest := filepath.Join(cfgDir, *outPath)
	data, err := json.MarshalIndent(tasks, "", "  ")
	if err != nil {
		fmt.Fprintf(os.Stderr, "marshal tasks: %v\n", err)
		_ = runstate.Fail(cfgDir, "place", "marshal error")
		os.Exit(1)
	}
	if err := os.WriteFile(dest, data, 0o644); err != nil {
		fmt.Fprintf(os.Stderr, "write %s: %v\n", dest, err)
		_ = runstate.Fail(cfgDir, "place", "write error")
		os.Exit(1)
	}

	_ = runstate.Finish(cfgDir, "place", fmt.Sprintf("%d pages, %d components", len(tasks), totalComponents))
	fmt.Printf("[place] %d pages with unplaced components → %s\n", len(tasks), dest)
	fmt.Printf("[place] %d total components to place\n", totalComponents)
	fmt.Printf("[place] dispatch Copilot CLI agents to execute placements\n")
}
