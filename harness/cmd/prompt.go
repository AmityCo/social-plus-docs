package main

import (
	"flag"
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"time"

	"social-plus/harness/internal/config"
	"social-plus/harness/internal/report"
)

// capitalise returns s with the first character uppercased.
func capitalise(s string) string {
	if s == "" {
		return ""
	}
	return strings.ToUpper(s[:1]) + s[1:]
}

func runPrompt(args []string) {
	fs := flag.NewFlagSet("prompt", flag.ExitOnError)
	cfgPath := fs.String("config", "harness-config.yml", "path to harness-config.yml")
	reportPath := fs.String("report", "harness-report.json", "report path")
	outPath := fs.String("out", "harness-tasks.md", "output task file (default: print to stdout if '-')")
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

	// Collect AI-required findings (open or needs_human for AI types) grouped by type and platform.
	type task struct {
		platform   string
		functionID string
		snippetDir string
		lang       string
		ext        string
		docPage    string
		detail     string
	}

	var missing []task
	var driftTasks []task

	for _, f := range r.Findings {
		// Include open findings and needs_human AI-type findings (failed API attempt from old harness version).
		isAIType := f.Type == report.TypeMissingSnippet || f.Type == report.TypeDocSurfaceDrift
		if f.Status == report.StatusFixed {
			continue
		}
		if f.Status == report.StatusNeedsHuman && !isAIType {
			continue
		}
		sdkCfg, ok := cfg.SDKs[f.Platform]
		if !ok {
			continue
		}
		sdkAbsPath := filepath.Join(filepath.Dir(*cfgPath), sdkCfg.Path)
		snippetAbsDir := filepath.Join(sdkAbsPath, sdkCfg.SnippetDir)

		switch f.Type {
		case report.TypeMissingSnippet:
			missing = append(missing, task{
				platform:   f.Platform,
				functionID: f.FunctionID,
				snippetDir: snippetAbsDir,
				lang:       platformLang(f.Platform),
				ext:        platformExt(f.Platform),
				detail:     f.Detail,
			})
		case report.TypeDocSurfaceDrift:
			driftTasks = append(driftTasks, task{
				platform: f.Platform,
				docPage:  f.DocPage,
				detail:   f.Detail,
			})
		}
	}

	if len(missing) == 0 && len(driftTasks) == 0 {
		fmt.Println("No AI-required open findings. Run 'audit' first.")
		return
	}

	var sb strings.Builder

	sb.WriteString("# SDK Harness — Agent Runbook\n\n")
	sb.WriteString(fmt.Sprintf("_Generated %s — %d findings requiring AI_\n\n", time.Now().Format("2006-01-02 15:04"), len(missing)+len(driftTasks)))
	sb.WriteString("## Agent Instructions\n\n")
	sb.WriteString("You are an autonomous agent. Execute ALL tasks in this file without stopping for confirmation.\n\n")
	sb.WriteString("**For each MISSING_SNIPPET task:**\n")
	sb.WriteString("1. Look up the function in the SDK source (search by function ID in the SDK path)\n")
	sb.WriteString("2. Generate a minimal working snippet using the `begin_sample_code` format below\n")
	sb.WriteString("3. Write the file to the specified snippet directory\n")
	sb.WriteString("4. Continue to the next task immediately\n\n")
	sb.WriteString("**After ALL snippets are written:**\n")
	sb.WriteString("```bash\n")
	sb.WriteString("cd social-plus-docs/harness && ./harness-bin audit --config harness-config.yml\n")
	sb.WriteString("```\n")
	sb.WriteString("Then run `./harness-bin prompt` again if there are still open findings.\n\n")
	sb.WriteString("**Snippet format (MUST match exactly):**\n")
	sb.WriteString("```\n/* begin_sample_code\n   filename: <filename>\n   sp_docs_page: <path from docs.json, e.g. social-plus-sdk/chat/overview>\n   description: <one line>\n   */\n<working code>\n/* end_sample_code */\n```\n\n")
	sb.WriteString("**Rules:**\n")
	sb.WriteString("- Use real Amity SDK class names (look them up in the SDK source)\n")
	sb.WriteString("- Keep it minimal — just enough to demonstrate the function\n")
	sb.WriteString("- `sp_docs_page` must be a relative path (not a full URL)\n")
	sb.WriteString("- Do not ask for confirmation between tasks — work through all of them\n\n")
	sb.WriteString("---\n\n")

	if len(missing) > 0 {
		sb.WriteString(fmt.Sprintf("## MISSING_SNIPPET (%d)\n\n", len(missing)))
		sb.WriteString("For each entry below, create a SDK code snippet file at the given path.\n")
		sb.WriteString("The snippet **must** use this exact format:\n\n")
		sb.WriteString("```\n/* begin_sample_code\n   gist_id: PLACEHOLDER\n   filename: <filename>\n   asc_page: <docs.json relative path, e.g. social-plus-sdk/chat/overview>\n   description: <one line>\n   */\n<working code>\n/* end_sample_code */\n```\n\n")
		sb.WriteString("Rules:\n")
		sb.WriteString("- Use real Amity/social.plus SDK class names from the platform source\n")
		sb.WriteString("- Keep it minimal — just enough to demonstrate the function\n")
		sb.WriteString("- `asc_page` must be a path from `docs.json` (not a full URL)\n\n")

		// Group by platform
		platforms := []string{"android", "ios", "flutter", "typescript"}
		for _, plat := range platforms {
			var platTasks []task
			for _, t := range missing {
				if t.platform == plat {
					platTasks = append(platTasks, t)
				}
			}
			if len(platTasks) == 0 {
				continue
			}
			langLabel := map[string]string{
				"android":    "Kotlin",
				"ios":        "Swift",
				"flutter":    "Dart",
				"typescript": "TypeScript",
			}[plat]
			sb.WriteString(fmt.Sprintf("### %s (%s) — %d functions\n\n", capitalise(plat), langLabel, len(platTasks)))
			sb.WriteString(fmt.Sprintf("Snippet directory: `%s`\n\n", platTasks[0].snippetDir))
			sb.WriteString("| Function ID | Write to filename |\n")
			sb.WriteString("|-------------|-------------------|\n")
			for _, t := range platTasks {
				filename := fmt.Sprintf("Amity%s.%s", sanitizeName(t.functionID), t.ext)
				sb.WriteString(fmt.Sprintf("| `%s` | `%s` |\n", t.functionID, filename))
			}
			sb.WriteString("\n")
		}
	}

	if len(driftTasks) > 0 {
		sb.WriteString(fmt.Sprintf("## DOC_SURFACE_DRIFT (%d)\n\n", len(driftTasks)))
		sb.WriteString("For each entry, update the MDX file to include the missing method reference.\n\n")
		for _, t := range driftTasks {
			sb.WriteString(fmt.Sprintf("- **%s** (`%s`): %s\n", t.platform, t.docPage, t.detail))
		}
		sb.WriteString("\n")
	}

	sb.WriteString("---\n\n")
	sb.WriteString("## After completion\n\n")
	sb.WriteString("```bash\n")
	sb.WriteString("cd social-plus-docs/harness\n")
	sb.WriteString("./harness-bin audit --config harness-config.yml\n")
	sb.WriteString("# If open findings remain: ./harness-bin prompt --config harness-config.yml\n")
	sb.WriteString("```\n")

	content := sb.String()

	if *outPath == "-" {
		fmt.Print(content)
		return
	}

	if err := os.WriteFile(*outPath, []byte(content), 0o644); err != nil {
		fmt.Fprintf(os.Stderr, "write tasks: %v\n", err)
		os.Exit(1)
	}
	fmt.Printf("Tasks written to %s (%d missing snippets, %d drift fixes)\n", *outPath, len(missing), len(driftTasks))
	fmt.Printf("\nTell Copilot CLI:\n  \"Fix the tasks in %s\"\n", *outPath)
}
