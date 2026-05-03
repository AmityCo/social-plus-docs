package main

import (
	"flag"
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"sort"
	"strings"

	"gopkg.in/yaml.v3"

	"social-plus/harness/internal/config"
	"social-plus/harness/internal/docgen"
	"social-plus/harness/internal/paritymap"
	"social-plus/harness/internal/patchgen"
	"social-plus/harness/internal/report"
	"social-plus/harness/internal/runstate"
	"social-plus/harness/internal/scanner"
)

// PatchFile is the top-level structure written to annotation-patches.yml.
type PatchFile struct {
	GeneratedBy string           `yaml:"generated_by"`
	Note        string           `yaml:"note"`
	Patches     []patchgen.Patch `yaml:"patches"`
}

var detailClassRe = regexp.MustCompile(`in (\S+) \(`)

func runAnnotate(args []string) {
	fs := flag.NewFlagSet("annotate", flag.ExitOnError)
	cfgPath := fs.String("config", "harness-config.yml", "path to harness-config.yml")
	apply := fs.Bool("apply", false, "insert annotations into SDK source files")
	outPath := fs.String("out", "annotation-patches.yml", "output patch file path")
	qa := fs.Bool("qa", false, "generate annotation-qa-tasks.md for AI agent review of asc_page assignments")
	qaOut := fs.String("qa-out", "annotation-qa-tasks.md", "output path for QA tasks file")
	if err := fs.Parse(args); err != nil {
		fmt.Fprintf(os.Stderr, "parse flags: %v\n", err)
		os.Exit(1)
	}

	if *qa {
		cfgDir2 := filepath.Dir(*cfgPath)
		cfg2, err2 := config.Load(*cfgPath)
		docsBase2 := filepath.Join(cfgDir2, "docs")
		if err2 == nil {
			docsBase2 = filepath.Join(cfgDir2, cfg2.Docs.Path)
		}
		patchFile := filepath.Join(cfgDir2, *outPath)
		if err2 = runAnnotateQA(docsBase2, patchFile, filepath.Join(cfgDir2, *qaOut)); err2 != nil {
			fmt.Fprintf(os.Stderr, "annotate --qa: %v\n", err2)
			os.Exit(1)
		}
		return
	}

	cfg, err := config.Load(*cfgPath)
	if err != nil {
		fmt.Fprintf(os.Stderr, "load config: %v\n", err)
		os.Exit(1)
	}
	cfgDir := filepath.Dir(*cfgPath)
	_ = runstate.Start(cfgDir, "annotate", "script", "")

	repPath := filepath.Join(cfgDir, "harness-report.json")
	rep, err := report.Read(repPath)
	if err != nil {
		fmt.Fprintf(os.Stderr, "load report: %v\n", err)
		_ = runstate.Fail(cfgDir, "annotate", "see stderr")
		os.Exit(1)
	}
	_ = runstate.UpdateSubstep(cfgDir, "annotate", runstate.Substep{
		Label:  "load report",
		Detail: fmt.Sprintf("%d PUBLIC_FUNC_UNANNOTATED findings", len(rep.Findings)),
		Status: "done",
	})

	var patches []patchgen.Patch
	skipped := 0

	// Build parity map for Gate 2 confidence signals.
	var allSnips []scanner.Snippet
	allPlatforms := make([]string, 0, len(cfg.SDKs))
	for p := range cfg.SDKs {
		allPlatforms = append(allPlatforms, p)
	}
	sort.Strings(allPlatforms)
	for _, platform := range allPlatforms {
		sdkCfg := cfg.SDKs[platform]
		snippetPath := filepath.Join(cfgDir, sdkCfg.Path, sdkCfg.SnippetDir)
		snips, err := scanner.Scan(snippetPath, platform)
		if err != nil {
			fmt.Fprintf(os.Stderr, "warning: skipping %s snippets: %v\n", platform, err)
		}
		allSnips = append(allSnips, snips...)
	}
	pm := paritymap.Build(allSnips, allPlatforms)

	for _, f := range rep.Findings {
		if f.Type != report.TypePublicFuncUnannotated {
			continue
		}

		parts := strings.SplitN(f.ID, ":", 4)
		if len(parts) != 4 {
			fmt.Fprintf(os.Stderr, "[annotate] skipping malformed id: %s\n", f.ID)
			skipped++
			continue
		}
		platform := parts[1]
		relPath := parts[2]
		funcName := parts[3]

		sdkCfg, ok := cfg.SDKs[platform]
		if !ok || sdkCfg.Path == "" {
			skipped++
			continue
		}
		sdkRoot := filepath.Join(cfgDir, sdkCfg.Path)
		absFile := filepath.Join(sdkRoot, relPath)

		lines, err := patchgen.ReadLines(absFile)
		if err != nil {
			fmt.Fprintf(os.Stderr, "[annotate] skip %s: %v\n", absFile, err)
			skipped++
			continue
		}

		lineNo, err := patchgen.FindFuncLine(lines, funcName, platform)
		if err != nil {
			fmt.Fprintf(os.Stderr, "[annotate] skip %s:%s: %v\n", relPath, funcName, err)
			skipped++
			continue
		}

		className := extractClassName(f.Detail)
		if className == "" {
			fmt.Fprintf(os.Stderr, "[annotate] warn: cannot extract class from detail, skipping: %q\n", f.Detail)
			skipped++
			continue
		}
		suggestedID := patchgen.InferID(className, funcName)
		annotation := patchgen.BuildAnnotation(suggestedID, platform)

		patches = append(patches, patchgen.Patch{
			Platform:    platform,
			File:        relPath,
			ClassName:   className,
			FuncName:    funcName,
			SuggestedID: suggestedID,
			InsertLine:  lineNo,
			Annotation:  annotation,
			EndMarker:   "/* end_public_function */",
			Confidence:  pm.Confidence(docgen.DeriveKey(className+"."+platformExt(platform)), platform),
		})
	}

	pf := PatchFile{
		GeneratedBy: "harness annotate",
		Note:        "Review 'id' values before applying. Run with --apply to insert annotations into SDK source.",
		Patches:     patches,
	}
	b, err := yaml.Marshal(pf)
	if err != nil {
		fmt.Fprintf(os.Stderr, "marshal patches: %v\n", err)
		_ = runstate.Fail(cfgDir, "annotate", "see stderr")
		os.Exit(1)
	}
	if err := os.WriteFile(*outPath, b, 0o644); err != nil {
		fmt.Fprintf(os.Stderr, "write patches: %v\n", err)
		_ = runstate.Fail(cfgDir, "annotate", "see stderr")
		os.Exit(1)
	}

	_ = runstate.UpdateSubstep(cfgDir, "annotate", runstate.Substep{
		Label:  "generate patches",
		Detail: fmt.Sprintf("%d patches, %d skipped", len(patches), skipped),
		Status: "done",
	})
	fmt.Printf("[annotate] %d patches written to %s (%d skipped)\n", len(patches), *outPath, skipped)

	if *apply {
		_ = runstate.UpdateSubstep(cfgDir, "annotate", runstate.Substep{
			Label:  "apply patches",
			Status: "running",
		})
		applyPatches(cfg, cfgDir, patches)
		_ = runstate.UpdateSubstep(cfgDir, "annotate", runstate.Substep{
			Label:  "apply patches",
			Status: "done",
		})
	} else {
		fmt.Printf("[annotate] Review %s then re-run with --apply to insert annotations\n", *outPath)
	}
	_ = runstate.Finish(cfgDir, "annotate", fmt.Sprintf("%d patches, %d skipped", len(patches), skipped))
}

func extractClassName(detail string) string {
	m := detailClassRe.FindStringSubmatch(detail)
	if len(m) >= 2 {
		return m[1]
	}
	return ""
}

// applyPatches inserts annotation text into SDK source files.
func applyPatches(cfg *config.Config, cfgDir string, patches []patchgen.Patch) {
	// Build platform → sdkRoot map
	sdkRoots := make(map[string]string)
	for platform, sdkCfg := range cfg.SDKs {
		sdkRoots[platform] = filepath.Join(cfgDir, sdkCfg.Path)
	}

	// Group patches by file (using platform+relPath as key)
	type fileKey struct{ platform, file string }
	grouped := make(map[fileKey][]patchgen.Patch)
	for _, p := range patches {
		k := fileKey{p.Platform, p.File}
		grouped[k] = append(grouped[k], p)
	}

	appliedFiles := 0
	appliedTotal := 0

	for k, fps := range grouped {
		sdkRoot, ok := sdkRoots[k.platform]
		if !ok {
			continue
		}
		absFile := filepath.Join(sdkRoot, k.file)

		lines, err := patchgen.ReadLines(absFile)
		if err != nil {
			fmt.Fprintf(os.Stderr, "[annotate] apply: read %s: %v\n", absFile, err)
			continue
		}

		// Sort descending by InsertLine so later insertions don't shift earlier indices
		sort.Slice(fps, func(i, j int) bool {
			return fps[i].InsertLine > fps[j].InsertLine
		})

		for _, p := range fps {
			idx := p.InsertLine - 1 // 0-indexed position to insert before
			if idx < 0 {
				idx = 0
			}
			if idx > len(lines) {
				fmt.Fprintf(os.Stderr, "[annotate] apply: InsertLine %d > file length %d for %s, clamping\n",
					p.InsertLine, len(lines), k.file)
				idx = len(lines)
			}
			annotLines := strings.Split(p.Annotation, "\n")
			// Remove trailing empty string from split
			if len(annotLines) > 0 && annotLines[len(annotLines)-1] == "" {
				annotLines = annotLines[:len(annotLines)-1]
			}
			// Insert annotation lines before idx
			newLines := make([]string, 0, len(lines)+len(annotLines))
			newLines = append(newLines, lines[:idx]...)
			newLines = append(newLines, annotLines...)
			newLines = append(newLines, lines[idx:]...)
			lines = newLines

			// Insert end_public_function after the function body
			funcDeclLine := idx + len(annotLines) // 0-indexed line of function declaration
			endLine := findFuncBodyEnd(lines, funcDeclLine)
			endMarkerLines := []string{"/* end_public_function */"}
			newLines2 := make([]string, 0, len(lines)+1)
			newLines2 = append(newLines2, lines[:endLine+1]...)
			newLines2 = append(newLines2, endMarkerLines...)
			newLines2 = append(newLines2, lines[endLine+1:]...)
			lines = newLines2

			appliedTotal++
		}

		content := strings.Join(lines, "\n") + "\n"
		if err := os.WriteFile(absFile, []byte(content), 0o644); err != nil {
			fmt.Fprintf(os.Stderr, "[annotate] apply: write %s: %v\n", absFile, err)
			continue
		}
		appliedFiles++
	}

	fmt.Printf("[annotate] Applied %d annotations to %d files\n", appliedTotal, appliedFiles)
}

// findFuncBodyEnd returns the 0-indexed line of the closing '}' for the function
// whose declaration begins at startLine. If no '{' is found, returns startLine
// (for single-expression functions — caller inserts end on the next line).
func findFuncBodyEnd(lines []string, startLine int) int {
	depth := 0
	opened := false
	for i := startLine; i < len(lines); i++ {
		for _, ch := range lines[i] {
			if ch == '{' {
				depth++
				opened = true
			} else if ch == '}' {
				depth--
				if opened && depth == 0 {
					return i
				}
			}
		}
	}
	return startLine
}

// QAPatch is a minimal view of one patch entry for QA purposes.
type QAPatch struct {
	File     string `yaml:"file"`
	Function string `yaml:"function"`
	AscPage  string `yaml:"asc_page"`
}

// QAPatchFile is the minimal structure of annotation-patches.yml for QA reading.
type QAPatchFile struct {
	Patches []QAPatch `yaml:"patches"`
}

// runAnnotateQA reads annotation-patches.yml, loads each asc_page's prose,
// and generates annotation-qa-tasks.md for the AI agent to assess asc_page correctness.
func runAnnotateQA(docsBase, patchPath, outPath string) error {
	data, err := os.ReadFile(patchPath)
	if err != nil {
		return fmt.Errorf("read patches: %w", err)
	}
	var pf QAPatchFile
	if err := yaml.Unmarshal(data, &pf); err != nil {
		return fmt.Errorf("parse patches: %w", err)
	}

	// Group by asc_page to avoid re-reading the same page multiple times.
	byPage := map[string][]QAPatch{}
	for _, p := range pf.Patches {
		if p.AscPage == "" {
			continue
		}
		byPage[p.AscPage] = append(byPage[p.AscPage], p)
	}

	// Load prose per page (first 500 words).
	pageProse := map[string]string{}
	for page := range byPage {
		mdxPath := filepath.Join(docsBase, filepath.FromSlash(page)+".mdx")
		raw, err := os.ReadFile(mdxPath)
		if err != nil {
			pageProse[page] = "(page file not found: " + mdxPath + ")"
			continue
		}
		pageProse[page] = extractProse(string(raw), 500)
	}

	return writeAnnotationQATasks(outPath, byPage, pageProse)
}

// extractProse strips MDX frontmatter and import lines, returning up to maxWords words of prose.
func extractProse(content string, maxWords int) string {
	lines := strings.Split(content, "\n")
	inFrontmatter := false
	fmDone := false
	var proseLines []string
	for _, line := range lines {
		trimmed := strings.TrimSpace(line)
		if !fmDone && trimmed == "---" {
			if !inFrontmatter {
				inFrontmatter = true
				continue
			}
			inFrontmatter = false
			fmDone = true
			continue
		}
		if inFrontmatter {
			continue
		}
		if strings.HasPrefix(trimmed, "import ") {
			continue
		}
		proseLines = append(proseLines, line)
	}
	full := strings.Join(proseLines, "\n")
	words := strings.Fields(full)
	if len(words) > maxWords {
		words = words[:maxWords]
	}
	return strings.Join(words, " ")
}

func writeAnnotationQATasks(outPath string, byPage map[string][]QAPatch, pageProse map[string]string) error {
	var sb strings.Builder
	sb.WriteString("# Annotation QA Tasks\n\n")
	sb.WriteString("For each function below, assess whether it belongs on its annotated page.\n\n")
	sb.WriteString("Write findings to `annotation-qa-findings.json`:\n")
	sb.WriteString("```json\n{\"findings\": [{\"function\": \"addReaction\", \"file\": \"...\", \"asc_page\": \"...\", \"verdict\": \"ANNOTATION_SUSPECT\" | \"ANNOTATION_UNCERTAIN\" | \"OK\", \"reason\": \"...\", \"suggested_page\": \"...\"}]}\n```\n\n")
	sb.WriteString("- `ANNOTATION_SUSPECT`: function clearly does NOT belong on this page\n")
	sb.WriteString("- `ANNOTATION_UNCERTAIN`: hard to tell — needs human review\n")
	sb.WriteString("- `OK`: function clearly belongs on this page\n\n")
	sb.WriteString("---\n\n")

	// Sort pages for deterministic output.
	pages := make([]string, 0, len(byPage))
	for p := range byPage {
		pages = append(pages, p)
	}
	sort.Strings(pages)

	for _, page := range pages {
		patches := byPage[page]
		sb.WriteString(fmt.Sprintf("## Page: `%s`\n\n", page))
		sb.WriteString("**Page prose:**\n")
		prose := pageProse[page]
		if len(prose) > 500 {
			prose = prose[:500] + "…"
		}
		sb.WriteString("> " + strings.ReplaceAll(strings.TrimSpace(prose), "\n", "\n> ") + "\n\n")
		sb.WriteString("**Functions to assess:**\n\n")
		for _, p := range patches {
			sb.WriteString(fmt.Sprintf("- `%s` (file: `%s`)\n", p.Function, p.File))
		}
		sb.WriteString("\n---\n\n")
	}

	return os.WriteFile(outPath, []byte(sb.String()), 0o644)
}
