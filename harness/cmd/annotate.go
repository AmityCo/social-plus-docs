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
