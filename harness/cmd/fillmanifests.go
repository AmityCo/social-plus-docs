package main

import (
	"flag"
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"social-plus/harness/internal/config"
	"social-plus/harness/internal/docgen"
	"social-plus/harness/internal/manifest"
	"social-plus/harness/internal/scanner"
)

func runFillManifests(args []string) {
	fs := flag.NewFlagSet("fillmanifests", flag.ExitOnError)
	cfgPath := fs.String("config", "harness-config.yml", "path to harness-config.yml")
	dryRun := fs.Bool("dry-run", false, "preview changes without writing files")
	_ = fs.Parse(args)

	cfg, err := config.Load(*cfgPath)
	if err != nil {
		fmt.Fprintf(os.Stderr, "load config: %v\n", err)
		os.Exit(1)
	}
	docsBase := filepath.Join(filepath.Dir(*cfgPath), cfg.Docs.Path)

	// Build page → []GendocsKey map from all SDK snippet dirs.
	pageKeys := map[string][]string{}
	for platform, sdkCfg := range cfg.SDKs {
		sdkBase := filepath.Join(filepath.Dir(*cfgPath), sdkCfg.Path)
		snippetDir := filepath.Join(sdkBase, sdkCfg.SnippetDir)
		snips, scanErr := scanner.Scan(snippetDir, platform)
		if scanErr != nil {
			fmt.Fprintf(os.Stderr, "[%s] scan error: %v\n", platform, scanErr)
			continue
		}
		for _, s := range snips {
			if s.SpDocsPage == "" || strings.Contains(s.SpDocsPage, "://") {
				continue
			}
			key := docgen.DeriveKey(s.Filename)
			pageKeys[s.SpDocsPage] = appendUnique(pageKeys[s.SpDocsPage], key)
		}
	}

	// Walk manifests and fill.
	totalAssigned := 0
	totalEmpty := 0
	manifestsUpdated := 0

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

		rel, _ := filepath.Rel(docsBase, path)
		pagePath := filepath.ToSlash(strings.TrimSuffix(rel, ".manifest.yml"))

		m, found, err := manifest.LoadForPage(docsBase, pagePath)
		if !found || err != nil {
			return nil
		}

		candidates := pageKeys[pagePath]
		hints := manifest.PageHintsFromPath(pagePath)
		filled := manifest.FillFromSnippets(m, candidates, hints...)

		// If sections are still empty, supplement with hint-matched snippet directory candidates.
		// Uses leaf (last-segment) tokens with score ≥ 2 to avoid false positives from
		// generic tokens like "message" that appear in hundreds of snippet names.
		if hasSectionWithNoSnippets(m) {
			leafHints := pageLeafHints(pagePath)
			threshold := 2
			if len(leafHints) < 2 {
				threshold = 1
			}
			if len(leafHints) > 0 {
				segs := strings.SplitN(pagePath, "/", 3)
				dir1, dir2 := "", ""
				if len(segs) > 0 {
					dir1 = segs[0]
				}
				if len(segs) > 1 {
					dir2 = segs[1]
				}
				snipDir := filepath.Join(docsBase, "snippets", dir1, dir2)
				var dirCandidates []string
				if entries, readErr := os.ReadDir(snipDir); readErr == nil {
					for _, e := range entries {
						if !strings.HasSuffix(e.Name(), ".mdx") {
							continue
						}
						key := strings.TrimSuffix(e.Name(), ".mdx")
						if manifest.ScoreKeyAgainstHints(key, leafHints) >= threshold {
							dirCandidates = appendUnique(dirCandidates, key)
						}
					}
				}
				if len(dirCandidates) > 0 {
					filled += manifest.FillFromSnippets(m, dirCandidates, hints...)
				}
			}
		}

		if len(candidates) > 0 {
			for _, sec := range m.Sections {
				if len(sec.Snippets) == 0 {
					totalEmpty++
				}
			}
		}

		if filled > 0 {
			totalAssigned += filled
			manifestsUpdated++
			if !*dryRun {
				if writeErr := manifest.SaveManifest(docsBase, pagePath, m); writeErr != nil {
					fmt.Fprintf(os.Stderr, "write %s: %v\n", path, writeErr)
				}
			}
		}
		return nil
	})

	if *dryRun {
		fmt.Printf("[fillmanifests] DRY RUN: would assign %d keys in %d manifests; %d sections still need AI\n",
			totalAssigned, manifestsUpdated, totalEmpty)
	} else {
		fmt.Printf("[fillmanifests] done — assigned %d keys in %d manifests; %d sections still need AI (run prompt)\n",
			totalAssigned, manifestsUpdated, totalEmpty)
	}
}

func appendUnique(slice []string, item string) []string {
	for _, s := range slice {
		if s == item {
			return slice
		}
	}
	return append(slice, item)
}

func hasSectionWithNoSnippets(m *manifest.Manifest) bool {
	for _, sec := range m.Sections {
		if len(sec.Snippets) == 0 {
			return true
		}
	}
	return false
}

// pageLeafHints returns meaningful tokens from the last path segment only.
// Using only the leaf avoids false positives from generic ancestor-path tokens.
func pageLeafHints(pagePath string) []string {
	segs := strings.Split(filepath.ToSlash(pagePath), "/")
	leaf := segs[len(segs)-1]
	var hints []string
	for _, tok := range strings.FieldsFunc(leaf, func(r rune) bool { return r == '-' || r == '_' }) {
		tok = strings.ToLower(tok)
		if len(tok) > 2 {
			hints = append(hints, tok)
		}
	}
	return hints
}
