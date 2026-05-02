package differ

import (
	"fmt"
	"os"
	"path/filepath"
	"sort"
	"strings"

	"social-plus/harness/internal/docgen"
	"social-plus/harness/internal/extractor"
	"social-plus/harness/internal/manifest"
	"social-plus/harness/internal/matcher"
	"social-plus/harness/internal/pages"
	"social-plus/harness/internal/report"
	"social-plus/harness/internal/scanner"
)

// DiffManifestCoverage checks that every snippet GendocsKey declared in the manifest
// has a corresponding *.mdx file under snippetsAbsDir.
// snippetsAbsDir is the absolute path to the snippets/ directory.
// docPage is the relative page path (e.g. "social-plus-sdk/getting-started/authentication").
//
// The expected snippet file path is:
//
//	snippetsAbsDir / <seg0> / <seg1> / <gendocsKey>.mdx
//
// where seg0 and seg1 are the first two "/" segments of docPage.
//
// Returns MISSING_SNIPPET findings (platform="", status=open) for any key with no file.
// Detail includes the section key, heading, and expected file path.
func DiffManifestCoverage(docPage string, m *manifest.Manifest, snippetsAbsDir string) []report.Finding {
	var findings []report.Finding
	if m == nil || len(m.Sections) == 0 {
		return nil
	}
	// Split docPage into segments
	parts := strings.Split(docPage, "/")
	for sectionKey, section := range m.Sections {
		for _, gendocsKey := range section.Snippets {
			// Build expected snippet path
			snippetPath := filepath.Join(snippetsAbsDir)
			if len(parts) >= 2 {
				snippetPath = filepath.Join(snippetPath, parts[0], parts[1], gendocsKey+".mdx")
			} else if len(parts) == 1 {
				snippetPath = filepath.Join(snippetPath, parts[0], gendocsKey+".mdx")
			} else {
				snippetPath = filepath.Join(snippetPath, gendocsKey+".mdx")
			}
			if _, err := os.Stat(snippetPath); os.IsNotExist(err) {
				findings = append(findings, report.Finding{
					ID:         fmt.Sprintf("manifest-missing:%s:%s:%s", docPage, sectionKey, gendocsKey),
					Type:       report.TypeMissingSnippet,
					Platform:   "",
					DocPage:    docPage,
					GendocsKey: gendocsKey,
					Detail:     fmt.Sprintf("Section %q (%s): missing snippet file %s", sectionKey, section.Heading, snippetPath),
					Status:     report.StatusOpen,
				})
			}
		}
	}
	return findings
}

func splitFirstTwo(docPage string) []string {
	parts := []string{}
	for _, seg := range filepath.SplitList(filepath.FromSlash(docPage)) {
		if seg != "" {
			parts = append(parts, seg)
		}
	}
	if len(parts) == 0 {
		parts = append(parts, docPage)
	}
	// If still not enough, try splitting by "/"
	if len(parts) < 2 {
		parts = []string{}
		for _, seg := range splitBySlash(docPage) {
			if seg != "" {
				parts = append(parts, seg)
			}
		}
	}
	return parts
}

func splitBySlash(s string) []string {
	var out []string
	for _, seg := range filepath.SplitList(filepath.FromSlash(s)) {
		if seg != "" {
			out = append(out, seg)
		}
	}
	if len(out) == 0 {
		for _, seg := range splitRaw(s) {
			if seg != "" {
				out = append(out, seg)
			}
		}
	}
	return out
}

func splitRaw(s string) []string {
	var out []string
	for _, seg := range splitOnRune(s, '/') {
		if seg != "" {
			out = append(out, seg)
		}
	}
	return out
}

func splitOnRune(s string, r rune) []string {
	var out []string
	curr := ""
	for _, c := range s {
		if c == r {
			if curr != "" {
				out = append(out, curr)
				curr = ""
			}
		} else {
			curr += string(c)
		}
	}
	if curr != "" {
		out = append(out, curr)
	}
	return out
}

// Diff runs all finding checks except DOC_SURFACE_DRIFT (needs MDX content).
func Diff(fns []extractor.PublicFunction, snips []scanner.Snippet, reg *pages.Registry, platform string) []report.Finding {
	return DiffWithMDX(fns, snips, reg, platform, nil)
}

// DiffWithMDX runs all finding checks including DOC_SURFACE_DRIFT.
func DiffWithMDX(fns []extractor.PublicFunction, snips []scanner.Snippet, reg *pages.Registry, platform string, mdxContent map[string]string) []report.Finding {
	var findings []report.Finding

	// Primary: content-based matching (method calls found in snippet code).
	coveredMethods := make(map[string]bool)
	for _, s := range snips {
		for _, call := range extractMethodCalls(s.Content) {
			coveredMethods[strings.ToLower(call)] = true
		}
	}

	// Secondary: filename-based matching.
	// Agents create files named Amity<PascalCaseFunctionID>.<ext> — this is more
	// reliable than content matching for compound/short IDs (e.g. channel.get →
	// AmityChannelGet.kt, channel.moderation.add_roles → AmityChannelModerationAddRoles.kt).
	coveredByFile := make(map[string]bool)
	for _, s := range snips {
		base := strings.TrimSuffix(filepath.Base(s.File), filepath.Ext(s.File))
		coveredByFile[strings.ToLower(base)] = true
	}

	for _, fn := range fns {
		for _, id := range fn.IDs {
			method := methodName(id)
			expectedClass := strings.ToLower(fnIDToClassName(id)) // e.g. "amitychannelget"
			if coveredMethods[strings.ToLower(method)] || coveredByFile[expectedClass] {
				continue
			}

			findings = append(findings, report.Finding{
				ID:         fmt.Sprintf("%s-missing-%s", platform, id),
				Type:       report.TypeMissingSnippet,
				Platform:   platform,
				FunctionID: id,
				Detail:     fmt.Sprintf("no snippet covers method %q", method),
				Status:     report.StatusOpen,
			})
		}
	}

	for _, s := range snips {
		base := filepath.Base(s.File)

		if strings.HasPrefix(s.SpDocsPage, "http") {
			findings = append(findings, report.Finding{
				ID:          fmt.Sprintf("%s-asc-invalid-%s", platform, base),
				Type:        report.TypeAscPageInvalid,
				Platform:    platform,
				SnippetFile: s.File,
				Detail:      fmt.Sprintf("sp_docs_page %q is a legacy URL, not a docs.json relative path", s.SpDocsPage),
				Status:      report.StatusOpen,
			})
			continue
		}

		if s.SpDocsPage == "" {
			continue
		}

		if !reg.Contains(s.SpDocsPage) {
			findings = append(findings, report.Finding{
				ID:          fmt.Sprintf("%s-doc-missing-%s", platform, base),
				Type:        report.TypeDocMissing,
				Platform:    platform,
				SnippetFile: s.File,
				DocPage:     s.SpDocsPage,
				Detail:      fmt.Sprintf("sp_docs_page %q not found in docs.json", s.SpDocsPage),
				Status:      report.StatusOpen,
			})
			continue
		}

		if mdxContent != nil {
			mdx, ok := mdxContent[s.SpDocsPage]
			if ok {
				for _, call := range extractMethodCalls(s.Content) {
					if strings.Contains(mdx, call) {
						continue
					}

					findings = append(findings, report.Finding{
						ID:          fmt.Sprintf("%s-surface-drift-%s-%s", platform, base, call),
						Type:        report.TypeDocSurfaceDrift,
						Platform:    platform,
						SnippetFile: s.File,
						DocPage:     s.SpDocsPage,
						Detail:      fmt.Sprintf("snippet calls %q but not found in doc page content", call),
						Status:      report.StatusOpen,
					})
				}

				// SNIPPET_CONTENT_DRIFT: MDX code block has drifted from SDK snippet content
				if s.Content != "" {
					firstLine := firstNonEmptyLine(s.Content)
					if firstLine != "" && !strings.Contains(mdx, firstLine) {
						findings = append(findings, report.Finding{
							ID:          fmt.Sprintf("%s-snippet-drift-%s", platform, base),
							Type:        report.TypeSnippetContentDrift,
							Platform:    platform,
							SnippetFile: s.File,
							DocPage:     s.SpDocsPage,
							Detail:      fmt.Sprintf("snippet content not found in MDX page %q", s.SpDocsPage),
							Status:      report.StatusOpen,
						})
					}
				}
			}
		}
	}

	return findings
}

func methodName(id string) string {
	parts := strings.SplitN(id, ".", 2)
	if len(parts) == 2 {
		return parts[1]
	}
	return id
}

func extractMethodCalls(content string) []string {
	var calls []string
	seen := make(map[string]bool)

	words := strings.FieldsFunc(content, func(r rune) bool {
		switch r {
		case '(', ')', '\n', ' ', '\t', '.', ';', ',', '{', '}', '[', ']':
			return true
		default:
			return false
		}
	})

	for _, word := range words {
		word = strings.TrimSpace(word)
		if len(word) <= 3 || strings.HasPrefix(word, "//") || strings.HasPrefix(word, "/*") || seen[word] {
			continue
		}
		calls = append(calls, word)
		seen[word] = true
	}

	return calls
}

// firstNonEmptyLine returns the first non-empty, non-comment line from content.
func firstNonEmptyLine(content string) string {
	for _, line := range strings.Split(content, "\n") {
		trimmed := strings.TrimSpace(line)
		if trimmed != "" && !strings.HasPrefix(trimmed, "//") && !strings.HasPrefix(trimmed, "/*") && !strings.HasPrefix(trimmed, "*") {
			return trimmed
		}
	}
	return ""
}

// fnIDToClassName converts a function ID like "channel.moderation.add_roles"
// to its expected class name "AmityChannelModerationAddRoles".
// This matches the naming convention used when generating snippet files.
func fnIDToClassName(id string) string {
	parts := strings.FieldsFunc(id, func(r rune) bool {
		return r == '.' || r == '_' || r == ' ' || r == '-'
	})
	result := "Amity"
	for _, p := range parts {
		if len(p) > 0 {
			result += strings.ToUpper(p[:1]) + p[1:]
		}
	}
	return result
}

// DiffDocImports scans an MDX file for `import X from '/snippets/...'` lines
// and returns a DOC_BROKEN_IMPORT finding for each import whose target file
// does not exist under docsBase.
func DiffDocImports(mdxPath, docsBase string) []report.Finding {
	data, err := os.ReadFile(mdxPath)
	if err != nil {
		return nil
	}
	var findings []report.Finding
	for i, line := range strings.Split(string(data), "\n") {
		trimmed := strings.TrimSpace(line)
		if !strings.HasPrefix(trimmed, "import ") || !strings.Contains(trimmed, "'/snippets/") {
			continue
		}
		start := strings.Index(trimmed, "'/snippets/")
		if start == -1 {
			continue
		}
		rest := trimmed[start+1:]
		end := strings.Index(rest, "'")
		if end == -1 {
			continue
		}
		importPath := rest[:end] // e.g. /snippets/social-plus-sdk/getting-started/client-login.mdx
		absTarget := filepath.Join(docsBase, filepath.FromSlash(strings.TrimPrefix(importPath, "/")))
		if _, statErr := os.Stat(absTarget); os.IsNotExist(statErr) {
			rel, _ := filepath.Rel(docsBase, mdxPath)
			findings = append(findings, report.Finding{
				ID:      fmt.Sprintf("broken-import:%s:%d", filepath.ToSlash(rel), i+1),
				Type:    report.TypeDocBrokenImport,
				DocPage: filepath.ToSlash(strings.TrimSuffix(rel, ".mdx")),
				Detail:  fmt.Sprintf("import %q not found (line %d)", importPath, i+1),
				Status:  report.StatusOpen,
			})
		}
	}
	return findings
}

// DiffDocPages checks a single doc page for DOC_PAGE_STALE_IMPORT findings.
// docPagePath is the page's docs.json-relative path (e.g. "social-plus-sdk/social/...").
// docPageFile is the absolute path to the MDX file on disk.
// snippetsDir is the relative prefix used in import paths (e.g. "snippets").
func DiffDocPages(docPagePath, docPageFile string, m *matcher.Matcher, snippetsDir string) []report.Finding {
	groups := m.Lookup(docPagePath)
	if len(groups) == 0 {
		return nil
	}

	content, err := os.ReadFile(docPageFile)
	if err != nil {
		return nil // unreadable file: skip
	}
	contentStr := string(content)

	var findings []report.Finding
	for _, g := range groups {
		gendocsPath := docgen.DeriveMDXPath(g.SpDocsPage, g.Key)
		importPath := "/" + snippetsDir + "/" + gendocsPath

		// Already imported → no finding
		if strings.Contains(contentStr, importPath) {
			continue
		}

		findings = append(findings, report.Finding{
			ID:                    fmt.Sprintf("doc-stale-%s-%s", docPagePath, g.Key),
			Type:                  report.TypeDocPageStaleImport,
			DocPage:               docPagePath,
			DocPageFile:           docPageFile,
			GendocsKey:            g.Key,
			GendocsPath:           gendocsPath,
			HasHardcodedCodeGroup: strings.Contains(contentStr, "<CodeGroup>"),
			Detail:                fmt.Sprintf("doc page %q has gendocs snippet %q but does not import it", docPagePath, gendocsPath),
			Status:                report.StatusOpen,
		})
	}
	return findings
}

// DiffSnippetKeyConflicts checks that all platforms for a given snippet key
// agree on the same sp_docs_page. When platforms disagree, the deterministic
// sort in GroupSnippets silently picks android's page — this finding surfaces
// the conflict so it can be resolved in the SDK source.
//
// Snippets with blank or absolute-URL SpDocsPage are skipped.
func DiffSnippetKeyConflicts(snips []scanner.Snippet) []report.Finding {
	type entry struct {
		platform string
		page     string
	}
	// key → list of (platform, page) pairs with non-empty page
	byKey := make(map[string][]entry)
	for _, s := range snips {
		if s.Filename == "" || s.SpDocsPage == "" || strings.Contains(s.SpDocsPage, "://") {
			continue
		}
		key := docgen.DeriveKey(s.Filename)
		if key == "" {
			continue
		}
		byKey[key] = append(byKey[key], entry{platform: s.Platform, page: s.SpDocsPage})
	}

	var findings []report.Finding
	for key, entries := range byKey {
		if len(entries) < 2 {
			continue
		}
		canonical := entries[0].page
		conflicted := false
		for _, e := range entries {
			if e.page != canonical {
				conflicted = true
				break
			}
		}
		if !conflicted {
			continue
		}
		// Build detail: list all platform→page pairs
		var parts []string
		for _, e := range entries {
			parts = append(parts, fmt.Sprintf("%s→%s", e.platform, e.page))
		}
		findings = append(findings, report.Finding{
			ID:         fmt.Sprintf("key-conflict:%s", key),
			Type:       report.TypeSnippetKeyPlatformConflict,
			GendocsKey: key,
			Detail:     fmt.Sprintf("key %q has conflicting sp_docs_page across platforms: %s", key, strings.Join(parts, ", ")),
			Status:     report.StatusOpen,
		})
	}
	sort.Slice(findings, func(i, j int) bool {
		return findings[i].ID < findings[j].ID
	})
	return findings
}
