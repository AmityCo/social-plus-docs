package main

import (
	"flag"
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"social-plus/harness/internal/config"
	"social-plus/harness/internal/fixer"
	"social-plus/harness/internal/pages"
	"social-plus/harness/internal/report"
	"social-plus/harness/internal/verifier"
	"social-plus/harness/internal/runstate"
)

func runFix(args []string) {
	fs := flag.NewFlagSet("fix", flag.ExitOnError)
	cfgPath := fs.String("config", "harness-config.yml", "path to harness-config.yml")
	reportPath := fs.String("report", "harness-report.json", "report path")
	issuesPath := fs.String("issues", "harness-issues.md", "issues output path")
	_ = fs.Parse(args)

	cfg, err := config.Load(*cfgPath)
	if err != nil {
		fmt.Fprintf(os.Stderr, "load config: %v\n", err)
		os.Exit(1)
	}
	cfgDir := filepath.Dir(*cfgPath)
	_ = runstate.Start(cfgDir, "fix", "ai_agent", cfg.LLM.Model)

	r, err := report.Read(*reportPath)
	if err != nil {
		fmt.Fprintf(os.Stderr, "read report: %v\n", err)
		_ = runstate.Fail(cfgDir, "fix", "see stderr")
		os.Exit(1)
	}

	// Load pages registry once — used by all ASC_PAGE_INVALID fixes.
	docsJSON := filepath.Join(filepath.Dir(*cfgPath), cfg.Docs.Path, "docs.json")
	reg, err := pages.Load(docsJSON)
	if err != nil {
		fmt.Fprintf(os.Stderr, "load pages registry: %v\n", err)
		_ = runstate.Fail(cfgDir, "fix", "see stderr")
		os.Exit(1)
	}

	fixedCount := 0
	aiCount := 0
	for i, f := range r.Findings {
		if f.Status != report.StatusOpen {
			continue
		}

		_, ok := cfg.SDKs[f.Platform]
		if !ok {
			fmt.Printf("  [skip] unknown platform %s\n", f.Platform)
			continue
		}
		sdkCfg := cfg.SDKs[f.Platform]
		sdkPath := filepath.Join(filepath.Dir(*cfgPath), sdkCfg.Path)
		_ = sdkPath

		switch f.Type {
		case report.TypeDocMissing:
			fmt.Printf("[fix] DOC_MISSING %s\n", f.SnippetFile)
			if f.SnippetFile == "" || f.DocPage == "" {
				r.Findings[i].Status = report.StatusNeedsHuman
				r.Findings[i].Detail += " | missing snippet_file or doc_page field"
				continue
			}
			snippetAbs := filepath.Clean(filepath.Join(filepath.Dir(*cfgPath), f.SnippetFile))
			liveDocPage, extractErr := extractAscPageFromSnippet(snippetAbs)
if extractErr != nil {
    liveDocPage = f.DocPage
}
newPath, fixErr := fixer.FixAscPage(snippetAbs, liveDocPage, reg)
			if fixErr != nil {
				fmt.Printf("  FAILED: %v\n", fixErr)
				r.Findings[i].Status = report.StatusNeedsHuman
				r.Findings[i].Detail += " | auto-fix failed: " + fixErr.Error()
			} else {
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
			// AI-required: delegate to Copilot CLI via 'harness prompt'.
			aiCount++
			fmt.Printf("[ai-needed] MISSING_SNIPPET %s/%s — run 'harness prompt'\n", f.Platform, f.FunctionID)

		case report.TypeDocSurfaceDrift:
			// AI-required: delegate to Copilot CLI via 'harness prompt'.
			aiCount++
			fmt.Printf("[ai-needed] DOC_SURFACE_DRIFT %s — run 'harness prompt'\n", f.DocPage)

		default:
			r.Findings[i].Status = report.StatusNeedsHuman
		}
	}

	if writeErr := report.Write(r, *reportPath); writeErr != nil {
		fmt.Fprintf(os.Stderr, "write report: %v\n", writeErr)
		_ = runstate.Fail(cfgDir, "fix", "see stderr")
		os.Exit(1)
	}
	if writeErr := report.WriteIssues(r.Findings, *issuesPath); writeErr != nil {
		fmt.Fprintf(os.Stderr, "write issues: %v\n", writeErr)
		_ = runstate.Fail(cfgDir, "fix", "see stderr")
		os.Exit(1)
	}

	_ = runstate.Finish(cfgDir, "fix", fmt.Sprintf("fixed %d, %d need AI", fixedCount, aiCount))
	fmt.Printf("\nFixed %d findings deterministically. %d findings need Copilot CLI (run 'harness prompt').\n", fixedCount, aiCount)
}

// extractAscPageFromSnippet reads a snippet file and returns the value of the
// sp_docs_page (or legacy asc_page) metadata field.
func extractAscPageFromSnippet(path string) (string, error) {
	b, err := os.ReadFile(path)
	if err != nil {
		return "", fmt.Errorf("read snippet file: %w", err)
	}
	for _, line := range strings.Split(string(b), "\n") {
		trimmed := strings.TrimSpace(line)
		for _, key := range []string{"sp_docs_page:", "asc_page:"} {
			if strings.HasPrefix(trimmed, key) {
				return strings.TrimSpace(strings.TrimPrefix(trimmed, key)), nil
			}
		}
	}
	return "", fmt.Errorf("sp_docs_page field not found in snippet %q", path)
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
