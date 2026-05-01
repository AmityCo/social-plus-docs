package main

import (
	"flag"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"regexp"
	"strings"
	"time"

	"social-plus/harness/internal/config"
	"social-plus/harness/internal/differ"
	"social-plus/harness/internal/docgen"
	"social-plus/harness/internal/extractor"
	"social-plus/harness/internal/fixer"
	"social-plus/harness/internal/manifest"
	"social-plus/harness/internal/matcher"
	"social-plus/harness/internal/pages"
	"social-plus/harness/internal/publicscan"
	"social-plus/harness/internal/report"
	"social-plus/harness/internal/runstate"
	"social-plus/harness/internal/scanner"
)

func runAudit(args []string) {
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

	cfgDir := filepath.Dir(*cfgPath)
	_ = runstate.Start(cfgDir, "audit", "script", "")
	defer func() {
		if r := recover(); r != nil {
			_ = runstate.Fail(cfgDir, "audit", fmt.Sprintf("panic: %v", r))
			panic(r)
		}
	}()

	docsJSON := filepath.Join(cfgDir, cfg.Docs.Path, "docs.json")
	reg, err := pages.Load(docsJSON)
	if err != nil {
		fmt.Fprintf(os.Stderr, "load pages: %v\n", err)
		_ = runstate.Fail(cfgDir, "audit", "see stderr")
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

	var allSnips []scanner.Snippet
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
		allSnips = append(allSnips, snips...) // collect for DOC_PAGE_STALE_IMPORT below

		// TODO: Load MDX content for each snippet's asc_page and call differ.DiffWithMDX
		// to enable DOC_SURFACE_DRIFT and SNIPPET_CONTENT_DRIFT detection.
		// For now, only MISSING_SNIPPET, ASC_PAGE_INVALID, and DOC_MISSING are active.
		findings := differ.Diff(fns, snips, reg, platform)

		newCount := 0
		for _, f := range findings {
			if isAlreadyInReport(allFindings, f.ID) {
				continue
			}
			allFindings = append(allFindings, f)
			newCount++
		}

		fmt.Printf("[%s] %d public functions, %d snippets, %d new findings\n",
			platform, len(fns), len(snips), newCount)
	}

	// Audit doc pages for stale imports (DOC_PAGE_STALE_IMPORT)
	{
		// Normalize absolute URL sp_docs_pages before grouping
		for i, s := range allSnips {
			if strings.Contains(s.SpDocsPage, "://") {
				if norm := fixer.NormalizeAscPage(s.SpDocsPage, reg); norm != "" {
					allSnips[i].SpDocsPage = norm
				}
			}
		}
		allGroups := docgen.GroupSnippets(allSnips)
		m := matcher.New(allGroups)
		snippetsDir := "snippets"
		docsBase := filepath.Join(filepath.Dir(*cfgPath), cfg.Docs.Path)

		_ = filepath.WalkDir(docsBase, func(path string, d os.DirEntry, walkErr error) error {
			if walkErr != nil || d.IsDir() || !strings.HasSuffix(path, ".mdx") {
				return walkErr
			}
			rel, relErr := filepath.Rel(docsBase, path)
			if relErr != nil {
				return nil
			}
			relSlash := filepath.ToSlash(rel)
			if cfg.Docs.Scope != "" && !strings.HasPrefix(relSlash, cfg.Docs.Scope+"/") {
				return nil // outside scope
			}
			docPagePath := filepath.ToSlash(strings.TrimSuffix(rel, ".mdx"))
			docFindings := differ.DiffDocPages(docPagePath, path, m, snippetsDir)
			for _, f := range docFindings {
				if !isAlreadyInReport(allFindings, f.ID) {
					allFindings = append(allFindings, f)
				}
			}
			return nil
		})

		staleCount := 0
		for _, f := range allFindings {
			if f.Type == report.TypeDocPageStaleImport && f.Status == report.StatusOpen {
				staleCount++
			}
		}
		if staleCount > 0 {
			fmt.Printf("[audit] %d DOC_PAGE_STALE_IMPORT findings\n", staleCount)
		}
	}

	// Manifest coverage block
	{
		docsBase := filepath.Join(filepath.Dir(*cfgPath), cfg.Docs.Path)
		snippetsAbsDir := filepath.Join(docsBase, "snippets")
		manifestCount := 0
		addedCount := 0
		_ = filepath.WalkDir(docsBase, func(path string, d os.DirEntry, walkErr error) error {
			if walkErr != nil {
				return walkErr
			}
			if d.IsDir() {
				rel, _ := filepath.Rel(docsBase, path)
				if rel == "harness" || strings.HasPrefix(filepath.ToSlash(rel)+"/", "harness/") {
					return filepath.SkipDir
				}
				return nil
			}
			if !strings.HasSuffix(path, ".manifest.yml") {
				return nil
			}
			rel, relErr := filepath.Rel(docsBase, path)
			if relErr != nil {
				return nil
			}
			pagePath := strings.TrimSuffix(rel, ".manifest.yml")
			pagePath = filepath.ToSlash(pagePath)
			m, _, err := manifest.LoadForPage(docsBase, pagePath)
			if err != nil {
				fmt.Fprintf(os.Stderr, "manifest load error: %v\n", err)
				return nil
			}
			findings := differ.DiffManifestCoverage(pagePath, m, snippetsAbsDir)
			for _, f := range findings {
				if !isAlreadyInReport(allFindings, f.ID) {
					allFindings = append(allFindings, f)
					addedCount++
				}
			}
			manifestCount++
			return nil
		})
		if addedCount > 0 {
			fmt.Printf("[audit] %d manifest coverage findings from %d manifests\n", addedCount, manifestCount)
		}
	}

	// Check for broken import paths in MDX files (post-migration validation).
	{
		docsBase := filepath.Join(filepath.Dir(*cfgPath), cfg.Docs.Path)
		importErrCount := 0
		_ = filepath.WalkDir(docsBase, func(path string, d os.DirEntry, walkErr error) error {
			if walkErr != nil {
				return walkErr
			}
			if d.IsDir() {
				rel, _ := filepath.Rel(docsBase, path)
				relSlash := filepath.ToSlash(rel)
				// Skip harness/ (testdata) and essentials/ (Mintlify starter tutorials with placeholder imports)
				if rel == "harness" || strings.HasPrefix(relSlash+"/", "harness/") ||
					rel == "essentials" || strings.HasPrefix(relSlash+"/", "essentials/") {
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
				return nil // outside scope
			}
			for _, f := range differ.DiffDocImports(path, docsBase) {
				if !isAlreadyInReport(allFindings, f.ID) {
					allFindings = append(allFindings, f)
					importErrCount++
				}
			}
			return nil
		})
		if importErrCount > 0 {
			fmt.Printf("[audit] %d broken import findings\n", importErrCount)
		}
	}

	// --- Mintlify broken-links check (computational: parse errors are open findings) ---
	{
		docsRoot := filepath.Join(filepath.Dir(*cfgPath), cfg.Docs.Path)
		fmt.Printf("[audit] running mintlify broken-links ...\n")
		cmd := exec.Command("npx", "mintlify", "broken-links")
		cmd.Dir = docsRoot
		out, _ := cmd.CombinedOutput()
		output := string(out)
		// Parse syntax errors — these are critical (MDX won't render)
		mintlifyErrCount := 0
		for _, line := range strings.Split(output, "\n") {
			line = strings.TrimSpace(line)
			if !strings.HasPrefix(line, "erro Syntax error") {
				continue
			}
			// Extract file path from next token after "Unable to parse"
			parts := strings.SplitN(line, " - ", 2)
			filePart := ""
			if len(parts) == 2 {
				filePart = strings.Fields(parts[0])[len(strings.Fields(parts[0]))-1]
			}
			findingID := "mintlify-syntax:" + filePart
			if !isAlreadyInReport(allFindings, findingID) {
				allFindings = append(allFindings, report.Finding{
					ID:      findingID,
					Type:    "MINTLIFY_SYNTAX_ERROR",
					Status:  report.StatusOpen,
					Detail:  line,
					DocPage: filePart,
				})
				mintlifyErrCount++
			}
		}
		if mintlifyErrCount > 0 {
			fmt.Printf("[audit] %d Mintlify syntax error findings\n", mintlifyErrCount)
		} else {
			fmt.Printf("[audit] Mintlify: no syntax errors\n")
		}
	}

	// --- PUBLIC_FUNC_UNANNOTATED check ---
	// A function is annotated if its source file wraps it with /* begin_public_function */.
	// publicscan.Scan sets IsAnnotated=true for those functions.
	{
		pubFuncCount := 0
		reVerifiedFixed := 0
		for platform, sdkCfg := range cfg.SDKs {
			sdkPath := filepath.Join(filepath.Dir(*cfgPath), sdkCfg.Path)
			if _, err := os.Stat(sdkPath); os.IsNotExist(err) {
				continue // SDK not present in this environment
			}
			pubFuncs, err := publicscan.Scan(sdkPath, platform, sdkCfg.SnippetDir)
			if err != nil {
				fmt.Fprintf(os.Stderr, "publicscan %s: %v\n", platform, err)
				continue
			}
			_ = runstate.UpdateSubstep(cfgDir, "audit", runstate.Substep{
				Label:  fmt.Sprintf("scan %s", platform),
				Detail: fmt.Sprintf("%d public functions", len(pubFuncs)),
				Status: "done",
			})
			// Build a set of annotated function IDs from the current scan.
			nowAnnotated := map[string]bool{}
			for _, pf := range pubFuncs {
				if pf.IsAnnotated {
					rel, _ := filepath.Rel(sdkPath, pf.File)
					rel = filepath.ToSlash(rel)
					nowAnnotated["public-func-unannotated:"+platform+":"+rel+":"+pf.FuncName] = true
				}
			}
			// Re-verify existing needs_human findings: mark fixed if now annotated.
			for i, f := range allFindings {
				if f.Type != report.TypePublicFuncUnannotated || f.Status != report.StatusNeedsHuman {
					continue
				}
				if nowAnnotated[f.ID] {
					allFindings[i].Status = report.StatusFixed
					reVerifiedFixed++
				}
			}
			for _, pf := range pubFuncs {
				if pf.IsAnnotated {
					continue // already annotated with begin_public_function
				}
				rel, _ := filepath.Rel(sdkPath, pf.File)
				rel = filepath.ToSlash(rel)
				findingID := "public-func-unannotated:" + platform + ":" + rel + ":" + pf.FuncName
				if isAlreadyInReport(allFindings, findingID) {
					continue
				}
				allFindings = append(allFindings, report.Finding{
					ID:       findingID,
					Type:     report.TypePublicFuncUnannotated,
					Status:   report.StatusNeedsHuman,
					Platform: platform,
					DocPage:  "",
					Detail:   fmt.Sprintf("Public function '%s' in %s (%s) has no begin_public_function annotation", pf.FuncName, pf.ClassName, rel),
				})
				pubFuncCount++
			}
		}
		if pubFuncCount > 0 {
			fmt.Printf("[audit] %d PUBLIC_FUNC_UNANNOTATED findings\n", pubFuncCount)
		}
		if reVerifiedFixed > 0 {
			fmt.Printf("[audit] %d PUBLIC_FUNC_UNANNOTATED findings re-verified as fixed\n", reVerifiedFixed)
		}
	}

	r := &report.Report{
		GeneratedAt: time.Now().Format(time.RFC3339),
		Findings:    allFindings,
	}
	r.Recount()

	if err := report.Write(r, *reportPath); err != nil {
		fmt.Fprintf(os.Stderr, "write report: %v\n", err)
		_ = runstate.Fail(cfgDir, "audit", "see stderr")
		os.Exit(1)
	}

	_ = runstate.Finish(cfgDir, "audit", fmt.Sprintf("%d open, %d fixed, %d needs_human",
		r.Summary.Open, r.Summary.Fixed, r.Summary.NeedsHuman))
	fmt.Printf("\nSummary: %d open, %d fixed, %d needs_human\n",
		r.Summary.Open, r.Summary.Fixed, r.Summary.NeedsHuman)

	if *failOnFindings && r.Summary.Open > 0 {
		os.Exit(1)
	}
}

func isAlreadyInReport(findings []report.Finding, id string) bool {
	for _, f := range findings {
		if f.ID == id {
			return true
		}
	}
	return false
}

// extractFuncNamesFromSnippet extracts function names from a snippet's content
// using platform-specific heuristics for cross-referencing.
func extractFuncNamesFromSnippet(content, platform string) []string {
	var names []string
	seen := make(map[string]struct{})
	add := func(name string) {
		if name == "" {
			return
		}
		if _, ok := seen[name]; !ok {
			seen[name] = struct{}{}
			names = append(names, name)
		}
	}

	switch strings.ToLower(platform) {
	case "android":
		re := regexp.MustCompile(`\bfun\s+(\w+)\s*[(<]`)
		for _, m := range re.FindAllStringSubmatch(content, -1) {
			add(m[1])
		}
	case "ios":
		re := regexp.MustCompile(`\bfunc\s+(\w+)\s*[(<]`)
		for _, m := range re.FindAllStringSubmatch(content, -1) {
			add(m[1])
		}
	case "flutter":
		re := regexp.MustCompile(`\b([a-z]\w+)\s*\(`)
		for _, m := range re.FindAllStringSubmatch(content, -1) {
			add(m[1])
		}
	case "typescript":
		re := regexp.MustCompile(`(?:function|async\s+function)\s+(\w+)\s*[(<]`)
		for _, m := range re.FindAllStringSubmatch(content, -1) {
			add(m[1])
		}
		re2 := regexp.MustCompile(`^\s+(?:async\s+)?(\w+)\s*\(`)
		for _, m := range re2.FindAllStringSubmatch(content, -1) {
			add(m[1])
		}
	}
	return names
}
