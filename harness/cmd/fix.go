package main

import (
	"context"
	"flag"
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"social-plus/harness/internal/compiler"
	"social-plus/harness/internal/config"
	"social-plus/harness/internal/fixer"
	"social-plus/harness/internal/generator"
	"social-plus/harness/internal/pages"
	"social-plus/harness/internal/report"
	"social-plus/harness/internal/verifier"
)

func runFix(args []string) {
	fs := flag.NewFlagSet("fix", flag.ExitOnError)
	cfgPath := fs.String("config", "harness-config.yml", "path to harness-config.yml")
	reportPath := fs.String("report", "harness-report.json", "report path")
	issuesPath := fs.String("issues", "harness-issues.md", "issues output path")
	apiKey := fs.String("api-key", os.Getenv("ANTHROPIC_API_KEY"), "Anthropic API key")
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

	gen := generator.New(cfg.LLM.Model, *apiKey)
	surfaceFixer := fixer.NewSurfaceDriftFixer(cfg.LLM.Model, *apiKey)
	ctx := context.Background()

	fixedCount := 0
	for i, f := range r.Findings {
		if f.Status != report.StatusOpen {
			continue
		}

		sdkCfg, ok := cfg.SDKs[f.Platform]
		if !ok {
			fmt.Printf("  [skip] unknown platform %s\n", f.Platform)
			continue
		}
		sdkPath := filepath.Join(filepath.Dir(*cfgPath), sdkCfg.Path)

		switch f.Type {
		case report.TypeAscPageInvalid:
			fmt.Printf("[fix] ASC_PAGE_INVALID %s\n", f.SnippetFile)
			snippetAbs := filepath.Join(sdkPath, sdkCfg.SnippetDir, filepath.Base(f.SnippetFile))
			docsJSON := filepath.Join(filepath.Dir(*cfgPath), cfg.Docs.Path, "docs.json")
			reg, regErr := pages.Load(docsJSON)
			if regErr != nil {
				r.Findings[i].Status = report.StatusNeedsHuman
				r.Findings[i].Detail += " | load registry failed: " + regErr.Error()
				continue
			}
			// Read the actual asc_page value from the snippet file rather than
			// parsing it from the formatted Detail message.
			currentAscPage := extractAscPageFromSnippet(snippetAbs)
			if currentAscPage == "" {
				r.Findings[i].Status = report.StatusNeedsHuman
				r.Findings[i].Detail += " | could not extract asc_page from snippet"
				continue
			}
			newPath, fixErr := fixer.FixAscPage(snippetAbs, currentAscPage, reg)
			if fixErr != nil {
				fmt.Printf("  FAILED: %v\n", fixErr)
				r.Findings[i].Status = report.StatusNeedsHuman
				r.Findings[i].Detail += " | auto-fix failed: " + fixErr.Error()
			} else {
				sealed, _ := verifier.Seal(f, snippetAbs, "PASS", "n/a")
				r.Findings[i] = sealed
				fmt.Printf("  → %s\n", newPath)
				fixedCount++
			}

		case report.TypeSnippetContentDrift:
			fmt.Printf("[fix] SNIPPET_CONTENT_DRIFT %s\n", f.SnippetFile)
			snippetAbs := filepath.Join(sdkPath, sdkCfg.SnippetDir, filepath.Base(f.SnippetFile))
			mdxAbs := filepath.Join(filepath.Dir(*cfgPath), cfg.Docs.Path, f.DocPage+".mdx")
			code, extractErr := fixer.ExtractSnippetContent(snippetAbs)
			if extractErr == nil {
				extractErr = fixer.SyncSnippetToMDX(mdxAbs, f.Platform, platformLang(f.Platform), code)
			}
			if extractErr != nil {
				r.Findings[i].Status = report.StatusNeedsHuman
				r.Findings[i].Detail += " | " + extractErr.Error()
			} else {
				sealed, _ := verifier.Seal(f, mdxAbs, "PASS", "n/a")
				r.Findings[i] = sealed
				fixedCount++
			}

		case report.TypeMissingSnippet:
			fmt.Printf("[fix] MISSING_SNIPPET %s/%s\n", f.Platform, f.FunctionID)
			snippet, genErr := gen.Generate(ctx, f.Platform, f.FunctionID, "", "")
			if genErr != nil {
				r.Findings[i].Status = report.StatusNeedsHuman
				r.Findings[i].Detail += " | AI failed: " + genErr.Error()
				continue
			}
			filename := fmt.Sprintf("Amity%s.%s", sanitizeName(f.FunctionID), platformExt(f.Platform))
			destPath := filepath.Join(sdkPath, sdkCfg.SnippetDir, filename)
			if writeErr := os.WriteFile(destPath, []byte(snippet), 0o644); writeErr != nil {
				r.Findings[i].Status = report.StatusNeedsHuman
				r.Findings[i].Detail += " | write failed: " + writeErr.Error()
				continue
			}
			result, outHash, _ := compiler.Run(sdkPath, sdkCfg)
			sealed, sealErr := verifier.Seal(f, destPath, result, outHash)
			if sealErr != nil {
				fmt.Printf("  compile FAIL — needs human review\n")
				r.Findings[i].Status = report.StatusNeedsHuman
				r.Findings[i].Detail += " | compile failed"
			} else {
				r.Findings[i] = sealed
				fixedCount++
			}

		case report.TypeDocSurfaceDrift:
			fmt.Printf("[fix] DOC_SURFACE_DRIFT %s\n", f.DocPage)
			mdxAbs := filepath.Join(filepath.Dir(*cfgPath), cfg.Docs.Path, f.DocPage+".mdx")
			surfaceErr := surfaceFixer.FixSurfaceDrift(ctx, mdxAbs, f.Detail, "")
			if surfaceErr != nil {
				r.Findings[i].Status = report.StatusNeedsHuman
				r.Findings[i].Detail += " | " + surfaceErr.Error()
			} else {
				sealed, _ := verifier.Seal(f, mdxAbs, "PASS", "n/a")
				r.Findings[i] = sealed
				fixedCount++
			}

		default:
			r.Findings[i].Status = report.StatusNeedsHuman
		}
	}

	if writeErr := report.Write(r, *reportPath); writeErr != nil {
		fmt.Fprintf(os.Stderr, "write report: %v\n", writeErr)
	}
	if writeErr := report.WriteIssues(r.Findings, *issuesPath); writeErr != nil {
		fmt.Fprintf(os.Stderr, "write issues: %v\n", writeErr)
	}

	fmt.Printf("\nFixed %d findings. Run 'audit' to verify.\n", fixedCount)
}

// extractAscPageFromSnippet reads a snippet file and returns the value of the
// asc_page metadata field, or empty string if not found.
func extractAscPageFromSnippet(path string) string {
	b, err := os.ReadFile(path)
	if err != nil {
		return ""
	}
	for _, line := range strings.Split(string(b), "\n") {
		trimmed := strings.TrimSpace(line)
		if strings.HasPrefix(trimmed, "asc_page:") {
			return strings.TrimSpace(strings.TrimPrefix(trimmed, "asc_page:"))
		}
	}
	return ""
}

func platformLang(platform string) string {
	switch platform {
	case "android":
		return "kotlin"
	case "ios":
		return "swift"
	case "flutter":
		return "dart"
	case "typescript":
		return "typescript"
	}
	return "text"
}

func platformExt(platform string) string {
	switch platform {
	case "android":
		return "kt"
	case "ios":
		return "swift"
	case "flutter":
		return "dart"
	case "typescript":
		return "ts"
	}
	return "txt"
}

func sanitizeName(id string) string {
	result := ""
	for _, part := range splitDotOrUnderscore(id) {
		if len(part) > 0 {
			result += strings.ToUpper(part[:1]) + part[1:]
		}
	}
	return result
}

func splitDotOrUnderscore(s string) []string {
	var parts []string
	current := ""
	for _, r := range s {
		if r == '.' || r == '_' {
			if current != "" {
				parts = append(parts, current)
			}
			current = ""
		} else {
			current += string(r)
		}
	}
	if current != "" {
		parts = append(parts, current)
	}
	return parts
}
