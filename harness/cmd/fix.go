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

	// Load pages registry once — used by all ASC_PAGE_INVALID fixes.
	docsJSON := filepath.Join(filepath.Dir(*cfgPath), cfg.Docs.Path, "docs.json")
	reg, err := pages.Load(docsJSON)
	if err != nil {
		fmt.Fprintf(os.Stderr, "load pages registry: %v\n", err)
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
			// Fix 4: guard against empty snippet_file field.
			if f.SnippetFile == "" {
				r.Findings[i].Status = report.StatusNeedsHuman
				r.Findings[i].Detail += " | missing snippet_file field"
				continue
			}
			// Resolve snippet path relative to the config dir (SnippetFile is already relative).
			snippetAbs := filepath.Clean(filepath.Join(filepath.Dir(*cfgPath), f.SnippetFile))
			// Fix 6: extractAscPageFromSnippet now returns (string, error).
			currentAscPage, extractErr := extractAscPageFromSnippet(snippetAbs)
			if extractErr != nil {
				r.Findings[i].Status = report.StatusNeedsHuman
				r.Findings[i].Detail += " | " + extractErr.Error()
				continue
			}
			newPath, fixErr := fixer.FixAscPage(snippetAbs, currentAscPage, reg)
			if fixErr != nil {
				fmt.Printf("  FAILED: %v\n", fixErr)
				r.Findings[i].Status = report.StatusNeedsHuman
				r.Findings[i].Detail += " | auto-fix failed: " + fixErr.Error()
			} else {
				// Fix 1: handle sealErr instead of discarding it.
				sealed, sealErr := verifier.Seal(f, snippetAbs, "PASS", "n/a")
				if sealErr != nil {
					fmt.Printf("  FAILED to seal: %v\n", sealErr)
					r.Findings[i].Status = report.StatusNeedsHuman
					r.Findings[i].Detail += " | seal failed: " + sealErr.Error()
				} else {
					r.Findings[i] = sealed
					fmt.Printf("  → %s\n", newPath)
					fixedCount++
				}
			}

		case report.TypeSnippetContentDrift:
			fmt.Printf("[fix] SNIPPET_CONTENT_DRIFT %s\n", f.SnippetFile)
			// Fix 4: guard against empty snippet_file or doc_page fields.
			if f.SnippetFile == "" || f.DocPage == "" {
				r.Findings[i].Status = report.StatusNeedsHuman
				r.Findings[i].Detail += " | missing snippet_file or doc_page field"
				continue
			}
			// Resolve snippet path relative to the config dir (SnippetFile is already relative).
			snippetAbs := filepath.Clean(filepath.Join(filepath.Dir(*cfgPath), f.SnippetFile))
			mdxAbs := filepath.Join(filepath.Dir(*cfgPath), cfg.Docs.Path, f.DocPage+".mdx")
			code, syncErr := fixer.ExtractSnippetContent(snippetAbs)
			if syncErr == nil {
				syncErr = fixer.SyncSnippetToMDX(mdxAbs, f.Platform, platformLang(f.Platform), code)
			}
			if syncErr != nil {
				r.Findings[i].Status = report.StatusNeedsHuman
				r.Findings[i].Detail += " | " + syncErr.Error()
			} else {
				// Fix 1: handle sealErr instead of discarding it.
				sealed, sealErr := verifier.Seal(f, mdxAbs, "PASS", "n/a")
				if sealErr != nil {
					fmt.Printf("  FAILED to seal: %v\n", sealErr)
					r.Findings[i].Status = report.StatusNeedsHuman
					r.Findings[i].Detail += " | seal failed: " + sealErr.Error()
				} else {
					r.Findings[i] = sealed
					fmt.Printf("  → fixed\n")
					fixedCount++
				}
			}

		case report.TypeMissingSnippet:
			fmt.Printf("[fix] MISSING_SNIPPET %s/%s\n", f.Platform, f.FunctionID)
			// Fix 4: guard against empty function_id field.
			if f.FunctionID == "" {
				r.Findings[i].Status = report.StatusNeedsHuman
				r.Findings[i].Detail += " | missing function_id field"
				continue
			}
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
			// Fix 3: log compiler exec setup errors.
			result, outHash, compileErr := compiler.Run(sdkPath, sdkCfg)
			if compileErr != nil {
				fmt.Printf("  compiler exec error: %v\n", compileErr)
			}
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
			// Fix 4: guard against empty doc_page field.
			if f.DocPage == "" {
				r.Findings[i].Status = report.StatusNeedsHuman
				r.Findings[i].Detail += " | missing doc_page field"
				continue
			}
			mdxAbs := filepath.Join(filepath.Dir(*cfgPath), cfg.Docs.Path, f.DocPage+".mdx")
			surfaceErr := surfaceFixer.FixSurfaceDrift(ctx, mdxAbs, f.Detail, "")
			if surfaceErr != nil {
				r.Findings[i].Status = report.StatusNeedsHuman
				r.Findings[i].Detail += " | " + surfaceErr.Error()
			} else {
				// Fix 1: handle sealErr instead of discarding it.
				sealed, sealErr := verifier.Seal(f, mdxAbs, "PASS", "n/a")
				if sealErr != nil {
					fmt.Printf("  FAILED to seal: %v\n", sealErr)
					r.Findings[i].Status = report.StatusNeedsHuman
					r.Findings[i].Detail += " | seal failed: " + sealErr.Error()
				} else {
					r.Findings[i] = sealed
					fmt.Printf("  → fixed\n")
					fixedCount++
				}
			}

		default:
			r.Findings[i].Status = report.StatusNeedsHuman
		}
	}

	if writeErr := report.Write(r, *reportPath); writeErr != nil {
		fmt.Fprintf(os.Stderr, "write report: %v\n", writeErr)
		os.Exit(1)
	}
	if writeErr := report.WriteIssues(r.Findings, *issuesPath); writeErr != nil {
		fmt.Fprintf(os.Stderr, "write issues: %v\n", writeErr)
		os.Exit(1)
	}

	fmt.Printf("\nFixed %d findings. Run 'audit' to verify.\n", fixedCount)
}

// extractAscPageFromSnippet reads a snippet file and returns the value of the
// asc_page metadata field, or an error if the file cannot be read or the field
// is absent.
func extractAscPageFromSnippet(path string) (string, error) {
	b, err := os.ReadFile(path)
	if err != nil {
		return "", fmt.Errorf("read snippet file: %w", err)
	}
	for _, line := range strings.Split(string(b), "\n") {
		trimmed := strings.TrimSpace(line)
		if strings.HasPrefix(trimmed, "asc_page:") {
			return strings.TrimSpace(strings.TrimPrefix(trimmed, "asc_page:")), nil
		}
	}
	return "", fmt.Errorf("asc_page field not found in snippet")
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
