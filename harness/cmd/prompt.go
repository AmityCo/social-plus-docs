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
	"social-plus/harness/internal/manifest"
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

	docsBaseForManifest := filepath.Join(filepath.Dir(*cfgPath), cfg.Docs.Path)
	snippetsDir := filepath.Join(docsBaseForManifest, "snippets")

	type manifestFillTask struct {
		pagePath    string
		sectionSlug string
		heading     string
		candidates  []string
	}
	var manifestFillTasks []manifestFillTask

	_ = filepath.WalkDir(docsBaseForManifest, func(mpath string, d os.DirEntry, walkErr error) error {
		if walkErr != nil {
			return walkErr
		}
		if d.IsDir() {
			rel, _ := filepath.Rel(docsBaseForManifest, mpath)
			if rel == "harness" || strings.HasPrefix(filepath.ToSlash(rel)+"/", "harness/") {
				return filepath.SkipDir
			}
			return nil
		}
		if !strings.HasSuffix(mpath, ".manifest.yml") {
			return nil
		}
		rel, _ := filepath.Rel(docsBaseForManifest, mpath)
		pagePath := filepath.ToSlash(strings.TrimSuffix(rel, ".manifest.yml"))
		if cfg.Docs.Scope != "" && !strings.HasPrefix(pagePath, cfg.Docs.Scope+"/") {
			return nil // outside scope
		}
		m, found, err := manifest.LoadForPage(docsBaseForManifest, pagePath)
		if !found || err != nil {
			return nil
		}
		for slug, sec := range m.Sections {
			if len(sec.Snippets) > 0 {
				continue
			}
			// Derive snippet dir from first 2 segments of page path
			segs := strings.SplitN(pagePath, "/", 3)
			dir1, dir2 := "unknown", "unknown"
			if len(segs) > 0 {
				dir1 = segs[0]
			}
			if len(segs) > 1 {
				dir2 = segs[1]
			}
			snipDir := filepath.Join(snippetsDir, dir1, dir2)
			var candidates []string
			if entries, readErr := os.ReadDir(snipDir); readErr == nil {
				for _, e := range entries {
					if strings.HasSuffix(e.Name(), ".mdx") {
						candidates = append(candidates, strings.TrimSuffix(e.Name(), ".mdx"))
					}
				}
			}
			manifestFillTasks = append(manifestFillTasks, manifestFillTask{
				pagePath:    pagePath,
				sectionSlug: slug,
				heading:     sec.Heading,
				candidates:  candidates,
			})
		}
		return nil
	})

	r, err := report.Read(*reportPath)
	if err != nil {
		fmt.Fprintf(os.Stderr, "read report: %v\n", err)
		os.Exit(1)
	}

	// Collect AI-required findings (open or needs_human for AI types) grouped by type and platform.
	type task struct {
	section    string
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
	staleImportCount := 0

	// Collect PUBLIC_FUNC_UNANNOTATED findings grouped by platform→class
	type unannotatedFunc struct {
		platform  string
		className string
		funcName  string
		file      string
		id        string
	}
	var unannotatedFuncs []unannotatedFunc

	for _, f := range r.Findings {
		// Include open findings and needs_human AI-type findings.
		isAIType := f.Type == report.TypeMissingSnippet || f.Type == report.TypeDocSurfaceDrift ||
			f.Type == report.TypePublicFuncUnannotated
		if f.Status == report.StatusFixed {
			continue
		}
		if f.Status == report.StatusNeedsHuman && !isAIType {
			continue
		}

		switch f.Type {
		case report.TypeDocPageStaleImport:
			if f.Status == report.StatusOpen {
				staleImportCount++
			}
			continue
		case report.TypePublicFuncUnannotated:
			// Extract className and funcName from detail
			// Format: "Public function 'funcName' in ClassName (file)"
			className, funcName, file := "", "", ""
			if d := f.Detail; d != "" {
				if i := strings.Index(d, "'"); i >= 0 {
					if j := strings.Index(d[i+1:], "'"); j >= 0 {
						funcName = d[i+1 : i+1+j]
					}
				}
				if i := strings.Index(d, " in "); i >= 0 {
					rest := d[i+4:]
					if j := strings.Index(rest, " ("); j >= 0 {
						className = rest[:j]
						afterParen := rest[j+2:]
						// File path is everything up to the closing ')'
						if k := strings.Index(afterParen, ")"); k >= 0 {
							file = afterParen[:k]
						} else {
							file = afterParen
						}
					}
				}
			}
			unannotatedFuncs = append(unannotatedFuncs, unannotatedFunc{
				platform:  f.Platform,
				className: className,
				funcName:  funcName,
				file:      file,
				id:        f.ID,
			})
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
			sectionHeading := ""
			if strings.HasPrefix(f.Detail, "manifest section") {
				if start := strings.Index(f.Detail, `(heading: "`); start != -1 {
					rest := f.Detail[start+len(`(heading: "`):]
					if end := strings.Index(rest, `")`); end != -1 {
						sectionHeading = rest[:end]
					}
				}
			}
			missing = append(missing, task{
				platform:   f.Platform,
				functionID: f.FunctionID,
				snippetDir: snippetAbsDir,
				lang:       platformLang(f.Platform),
				ext:        platformExt(f.Platform),
				detail:     f.Detail,
				section:    sectionHeading,
			})
		case report.TypeDocSurfaceDrift:
			driftTasks = append(driftTasks, task{
				platform: f.Platform,
				docPage:  f.DocPage,
				detail:   f.Detail,
			})
		}
	}

	if len(missing) == 0 && len(driftTasks) == 0 && staleImportCount == 0 && len(manifestFillTasks) == 0 {
		fmt.Println("No AI-required open findings. Run 'audit' first.")
		return
	}

	var sb strings.Builder

	sb.WriteString("# SDK Harness — Agent Runbook\n\n")
	sb.WriteString(fmt.Sprintf("_Generated %s — %d findings requiring AI_\n\n", time.Now().Format("2006-01-02 15:04"), len(missing)+len(driftTasks)+staleImportCount))
	sb.WriteString("## Step 0 — Start Dashboard (optional but recommended)\n\n")
	sb.WriteString("Run in a separate terminal before starting any other steps:\n\n")
	sb.WriteString("```bash\n")
	sb.WriteString("./harness-bin serve --config harness-config.yml\n")
	sb.WriteString("```\n\n")
	sb.WriteString("Then open http://localhost:8765 to watch pipeline progress live.\n")
	sb.WriteString("The dashboard auto-refreshes every 3 seconds.\n")
	sb.WriteString("You may skip this step if running headlessly.\n\n")
	sb.WriteString("---\n\n")
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
		sb.WriteString("```\n/* begin_sample_code\n   filename: <filename>\n   sp_docs_page: <docs.json relative path, e.g. social-plus-sdk/chat/overview>\n   description: <one line>\n   */\n<working code>\n/* end_sample_code */\n```\n\n")
		sb.WriteString("Rules:\n")
		sb.WriteString("- Use real Amity/social.plus SDK class names from the platform source\n")
		sb.WriteString("- Keep it minimal — just enough to demonstrate the function\n")
		sb.WriteString("- `sp_docs_page` must be a path from `docs.json` (not a full URL)\n\n")

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

	if len(manifestFillTasks) > 0 {
	sb.WriteString(fmt.Sprintf("\n---\n\n## MANIFEST_FILL (%d sections need assignment)\n\n", len(manifestFillTasks)))
	sb.WriteString("For each section below, open the manifest file and assign candidate snippet keys\n")
	sb.WriteString("to the matching `snippets:` array. Use the manifest file as your data source —\n")
	sb.WriteString("candidate keys are listed in the `_candidates:` block inside it.\n\n")
	sb.WriteString("### How to verify\n\n")
	sb.WriteString("```bash\ncd social-plus-docs/harness\n./harness-bin audit --config harness-config.yml\n```\n\n")
	sb.WriteString("MANIFEST_FILL findings disappear when all sections have at least one snippet assigned.\n\n")
	sb.WriteString("### Sections to fill\n\n")
	for _, mt := range manifestFillTasks {
		sb.WriteString(fmt.Sprintf("- **`%s`** → section `%s`  \n", mt.pagePath, mt.heading))
		sb.WriteString(fmt.Sprintf("  Manifest: `%s.manifest.yml`\n", mt.pagePath))
	}
	sb.WriteString("\n")
}

if staleImportCount > 0 {

		sb.WriteString(fmt.Sprintf("## DOC_PAGE_STALE_IMPORT (%d)\n\n", staleImportCount))
		sb.WriteString("These doc pages reference gendocs snippet files that are not yet imported.\n")
		sb.WriteString("Run the migrate command to automatically add the missing imports:\n\n")
		sb.WriteString("```bash\n")
		sb.WriteString("cd social-plus-docs/harness\n")
		sb.WriteString("./harness-bin migrate --config harness-config.yml\n")
		sb.WriteString("```\n\n")
		sb.WriteString("Or preview changes first with `--dry-run`:\n\n")
		sb.WriteString("```bash\n")
		sb.WriteString("./harness-bin migrate --config harness-config.yml --dry-run\n")
		sb.WriteString("```\n\n")
	}

	// PUBLIC_FUNC_UNANNOTATED section
	if len(unannotatedFuncs) > 0 {
		sb.WriteString(fmt.Sprintf("\n---\n\n## PUBLIC_FUNC_UNANNOTATED (%d functions)\n\n", len(unannotatedFuncs)))
		sb.WriteString("**Full list:** `harness/unannotated-functions-report.md`\n\n")
		sb.WriteString("Use the `annotate` command to generate annotation patches automatically, then review and apply.\n\n")
		sb.WriteString("### Step 1 — Generate annotation patches\n\n")
		sb.WriteString("```bash\ncd social-plus-docs/harness\n./harness-bin annotate --config harness-config.yml\n```\n\n")
		sb.WriteString("This writes `annotation-patches.yml` with one entry per unannotated function,\n")
		sb.WriteString("including a suggested `id:` value (e.g. `post.create`, `comment.get`).\n\n")
		sb.WriteString("### Step 2 — Review and correct id values\n\n")
		sb.WriteString("Open `annotation-patches.yml` and verify each `id:` follows the `feature.action` convention.\n")
		sb.WriteString("Check existing ids in the SDK source for consistency (search for `begin_public_function`).\n\n")
		sb.WriteString("### Step 3 — Apply patches\n\n")
		sb.WriteString("```bash\n./harness-bin annotate --config harness-config.yml --apply\n```\n\n")
		sb.WriteString("This inserts `begin_public_function` + `end_public_function` markers directly into SDK source files.\n\n")
		sb.WriteString("### Step 4 — Verify\n\n")
		sb.WriteString("```bash\n./harness-bin audit --config harness-config.yml\n```\n\n")
		sb.WriteString("**Expected:** `PUBLIC_FUNC_UNANNOTATED` count drops. The audit reads SDK source directly —\n")
		sb.WriteString("only actual source file changes count as proof. You cannot satisfy this check by editing\n")
		sb.WriteString("`harness-tasks.md`, `annotation-patches.yml`, or `unannotated-functions-report.md`.\n")
	}

	sb.WriteString("---\n\n")
	sb.WriteString("## After completion\n\n")
	sb.WriteString("Run the full audit to verify all tasks are resolved:\n\n")
	sb.WriteString("```bash\n")
	sb.WriteString("cd social-plus-docs/harness\n")
	sb.WriteString("./harness-bin audit --config harness-config.yml\n")
	sb.WriteString("```\n\n")
	sb.WriteString("**Expected result:** zero `open` findings. The audit is the authoritative proof —\n")
	sb.WriteString("it re-reads source files directly and cannot be satisfied by editing task or report files.\n\n")
	sb.WriteString("If findings remain, run `./harness-bin prompt` to regenerate this file with the remaining work.\n")

	content := sb.String()

	if *outPath == "-" {
		fmt.Print(content)
		return
	}

	if err := os.WriteFile(*outPath, []byte(content), 0o644); err != nil {
		fmt.Fprintf(os.Stderr, "write tasks: %v\n", err)
		os.Exit(1)
	}
	fmt.Printf("Tasks written to %s (%d missing snippets, %d drift fixes, %d stale imports, %d manifest fills, %d unannotated funcs)\n",
		*outPath, len(missing), len(driftTasks), staleImportCount, len(manifestFillTasks), len(unannotatedFuncs))
	fmt.Printf("\nTell Copilot CLI:\n  \"Fix the tasks in %s\"\n", *outPath)
}
