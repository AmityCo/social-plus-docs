package main

import (
	"flag"
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"time"

	"social-plus/harness/internal/config"
	"social-plus/harness/internal/curator"
)

func runCurate(args []string) {
	fs := flag.NewFlagSet("curate", flag.ExitOnError)
	cfgPath := fs.String("config", "harness-config.yml", "path to harness-config.yml")
	apply := fs.Bool("apply", false, "apply decisions from curate-decisions.json")
	decisionsPath := fs.String("decisions", "curate-decisions.json", "decisions file to read when --apply is set")
	outPath := fs.String("out", "curate-tasks.md", "output tasks file (gen mode)")
	reviewPath := fs.String("review", "curate-review.json", "output review file (apply mode)")
	dryRun := fs.Bool("dry-run", false, "print decisions without modifying MDX files")
	pageFilter := fs.String("page", "", "only process this page slug")
	_ = fs.Parse(args)

	cfg, err := config.Load(*cfgPath)
	if err != nil {
		fmt.Fprintf(os.Stderr, "load config: %v\n", err)
		os.Exit(1)
	}
	cfgDir := filepath.Dir(*cfgPath)
	docsBase := filepath.Join(cfgDir, cfg.Docs.Path)

	if *apply {
		if err := runCurateApply(cfgDir, docsBase, *decisionsPath, *reviewPath, *dryRun); err != nil {
			fmt.Fprintf(os.Stderr, "curate apply: %v\n", err)
			os.Exit(1)
		}
		return
	}

	if err := runCurateGenTasks(cfgDir, docsBase, *pageFilter, filepath.Join(cfgDir, *outPath)); err != nil {
		fmt.Fprintf(os.Stderr, "curate gen-tasks: %v\n", err)
		os.Exit(1)
	}
}

func runCurateGenTasks(cfgDir, docsBase, pageFilter, outPath string) error {
	return runCurateGenTasksForTest(cfgDir, "", pageFilter, outPath)
}

// runCurateGenTasksForTest is the testable core of gen-tasks mode.
// If cfgPath is non-empty, it loads config from that path to resolve docsBase.
func runCurateGenTasksForTest(cfgDir, cfgPath, pageFilter, outPath string) error {
	docsBase := filepath.Join(cfgDir, "docs")
	if cfgPath != "" {
		if cfg, err := config.Load(cfgPath); err == nil {
			docsBase = filepath.Join(cfgDir, cfg.Docs.Path)
		}
	}

	snippetReader := func(importPath string) string {
		rel := strings.TrimPrefix(importPath, "/")
		abs := filepath.Join(docsBase, filepath.FromSlash(rel))
		data, err := os.ReadFile(abs)
		if err != nil {
			return ""
		}
		content := string(data)
		if len(content) > 800 {
			content = content[:800]
		}
		return content
	}

	var pages []curator.ParsedPage
	err := filepath.WalkDir(docsBase, func(path string, d os.DirEntry, walkErr error) error {
		if walkErr != nil {
			return walkErr
		}
		if d.IsDir() {
			rel, _ := filepath.Rel(docsBase, path)
			relSlash := filepath.ToSlash(rel)
			if rel == "snippets" || strings.HasPrefix(relSlash+"/", "snippets/") ||
				rel == "harness" || strings.HasPrefix(relSlash+"/", "harness/") {
				return filepath.SkipDir
			}
			return nil
		}
		if !strings.HasSuffix(path, ".mdx") {
			return nil
		}
		rel, _ := filepath.Rel(docsBase, path)
		pagePath := filepath.ToSlash(strings.TrimSuffix(rel, ".mdx"))

		if pageFilter != "" && pagePath != pageFilter {
			return nil
		}

		data, err := os.ReadFile(path)
		if err != nil {
			fmt.Fprintf(os.Stderr, "warning: read %s: %v\n", path, err)
			return nil
		}
		p := curator.ParsePage(path, pagePath, string(data), snippetReader)
		if len(p.Placed) > 0 {
			pages = append(pages, p)
		}
		return nil
	})
	if err != nil {
		return fmt.Errorf("walk docs: %w", err)
	}

	return writeCurateTasks(outPath, pages)
}

func writeCurateTasks(outPath string, pages []curator.ParsedPage) error {
	var sb strings.Builder
	sb.WriteString("# Curate Tasks\n\n")
	sb.WriteString(fmt.Sprintf("Generated: %s\n\n", time.Now().UTC().Format("2006-01-02T15:04:05Z")))
	sb.WriteString("Review each page's placed snippets and write decisions to `curate-decisions.json`.\n\n")
	sb.WriteString("**Decision format per snippet:**\n")
	sb.WriteString("- `KEEP` (specify `section`: which `##` heading it belongs under)\n")
	sb.WriteString("- `REMOVE` (irrelevant or redundant)\n")
	sb.WriteString("- `MOVE` (specify `target_page`: docs slug where it belongs)\n")
	sb.WriteString("- `FLAG` (ambiguous, needs human review)\n\n")
	sb.WriteString("**Confidence:** `high` (auto-apply), `medium`/`low` (goes to review file)\n\n")
	sb.WriteString("---\n\n")

	if len(pages) == 0 {
		sb.WriteString("_No pages with placed snippets found._\n")
	}

	for _, p := range pages {
		sb.WriteString(fmt.Sprintf("## Page: `%s`\n\n", p.PagePath))
		sb.WriteString(fmt.Sprintf("**Sections:** %s\n\n", strings.Join(p.Sections, " · ")))

		prose := p.Prose
		if len(prose) > 600 {
			prose = prose[:600] + "…"
		}
		sb.WriteString("**Page purpose:**\n")
		sb.WriteString("> " + strings.ReplaceAll(strings.TrimSpace(prose), "\n", "\n> ") + "\n\n")

		sb.WriteString(fmt.Sprintf("**Placed snippets (%d):**\n\n", len(p.Placed)))
		for i, s := range p.Placed {
			sb.WriteString(fmt.Sprintf("### %d. `%s`\n", i+1, s.Name))
			sb.WriteString(fmt.Sprintf("Import: `%s`\n\n", s.ImportPath))
			if s.Content != "" {
				sb.WriteString("```\n")
				content := s.Content
				if len(content) > 400 {
					content = content[:400] + "\n// ... (truncated)"
				}
				sb.WriteString(content + "\n```\n\n")
			}
		}
		sb.WriteString("---\n\n")
	}

	return os.WriteFile(outPath, []byte(sb.String()), 0o644)
}

// runCurateApply reads curate-decisions.json, applies high-confidence decisions to MDX files,
// and writes flagged decisions to curate-review.json.
func runCurateApply(cfgDir, docsBase, decisionsPath, reviewPath string, dryRun bool) error {
	df, err := curator.ReadDecisions(decisionsPath)
	if err != nil {
		return fmt.Errorf("read decisions: %w", err)
	}

	var reviewPages []curator.PageDecisions
	totalApplied, totalFlagged := 0, 0

	for _, pd := range df.Pages {
		mdxFile := filepath.Join(docsBase, filepath.FromSlash(pd.PagePath)+".mdx")
		data, err := os.ReadFile(mdxFile)
		if err != nil {
			fmt.Fprintf(os.Stderr, "warning: read %s: %v\n", mdxFile, err)
			continue
		}

		modified, applied, flagged := curator.Apply(string(data), pd.Decisions)
		totalApplied += len(applied)
		totalFlagged += len(flagged)

		if len(flagged) > 0 {
			reviewPages = append(reviewPages, curator.PageDecisions{
				PagePath:  pd.PagePath,
				Decisions: flagged,
			})
		}

		for _, d := range applied {
			action := "removed"
			if d.Action == curator.ActionKeep {
				action = "kept (re-sectioned)"
			} else if d.Action == curator.ActionMove {
				action = fmt.Sprintf("moved → %s", d.TargetPage)
			}
			fmt.Printf("[curate] %s: %s %s\n", pd.PagePath, d.Name, action)
		}

		if !dryRun && modified != string(data) {
			if err := os.WriteFile(mdxFile, []byte(modified), 0o644); err != nil {
				return fmt.Errorf("write %s: %w", mdxFile, err)
			}
		}
	}

	if len(reviewPages) > 0 {
		if err := curator.WriteReview(reviewPath, reviewPages); err != nil {
			return fmt.Errorf("write review: %w", err)
		}
		fmt.Printf("[curate] %d decisions flagged for review → %s\n", totalFlagged, reviewPath)
	}

	if dryRun {
		fmt.Printf("[curate] dry-run: would apply %d, flag %d\n", totalApplied, totalFlagged)
	} else {
		fmt.Printf("[curate] applied %d, flagged %d\n", totalApplied, totalFlagged)
	}
	return nil
}
