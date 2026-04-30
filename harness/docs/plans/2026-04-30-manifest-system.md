# Manifest System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add page manifests as the source of truth for what code groups each doc page needs, enabling section-level CodeGroup targeting in `migrate`, manifest-driven `MISSING_SNIPPET` detection in `audit`, and structured section context in `prompt` tasks.

**Architecture:** A `*.manifest.yml` file lives alongside each MDX doc page. It defines sections (slugified `###` heading keys), their heading text, and which snippet GendocsKeys belong there. The `genmanifests` command bootstraps these manifests from existing MDX pages. `migrate`, `audit`, and `prompt` are updated to read manifests. No changes to SDK repos.

**Tech Stack:** Go 1.22, `gopkg.in/yaml.v3`, existing harness patterns (config, report, scanner, migrator).

---

## File Map

| Action | Path | Purpose |
|---|---|---|
| Create | `internal/manifest/manifest.go` | Parse `*.manifest.yml`; load for a given page path |
| Create | `internal/manifest/manifest_test.go` | Tests for load, parse, missing, malformed |
| Create | `internal/manifest/testdata/sample.manifest.yml` | Valid fixture |
| Create | `internal/manifest/testdata/malformed.manifest.yml` | Invalid YAML fixture |
| Create | `internal/mdxparse/mdxparse.go` | Extract `###` headings + `<CodeGroup>` positions from MDX |
| Create | `internal/mdxparse/mdxparse_test.go` | Tests |
| Create | `cmd/genmanifests.go` | `genmanifests` CLI command |
| Modify | `internal/migrator/migrator.go` | Add `ReplaceCodeGroupAfterHeading` |
| Modify | `internal/migrator/migrator_test.go` | Tests for section-targeted replacement |
| Modify | `cmd/migrate.go` | Load manifest per page; use section-targeted replace |
| Modify | `internal/differ/differ.go` | Add `DiffManifestCoverage` |
| Modify | `internal/differ/differ_test.go` | Tests for manifest diff |
| Modify | `cmd/audit.go` | Wire manifest differ; emit `MISSING_SNIPPET` with section context |
| Modify | `cmd/prompt.go` | Include section heading in MISSING_SNIPPET task output |
| Modify | `cmd/main.go` | Register `genmanifests` command |
| Modify | `cmd/main_test.go` | Update usage string assertion |
| Modify | `harness/docs/BIG-PICTURE.md` | Update current state table |

---

## Task 1: `internal/manifest` package

Parses `*.manifest.yml` files. Each manifest lives at `<page-path>.manifest.yml`
alongside the MDX file (e.g. `authentication.manifest.yml` next to `authentication.mdx`).

**Files:**
- Create: `internal/manifest/manifest.go`
- Create: `internal/manifest/manifest_test.go`
- Create: `internal/manifest/testdata/sample.manifest.yml`
- Create: `internal/manifest/testdata/malformed.manifest.yml`

### Manifest YAML format (reference)

```yaml
# authentication.manifest.yml
sections:
  step-1-initialize-the-sdk:
    heading: "### Step 1: Initialize the SDK"
    snippets:
      - client-setup           # GendocsKey: DeriveKey("AmityClientSetup.kt")
  step-2-login-user:
    heading: "### Step 2: Login User"
    snippets:
      - client-login
  step-3-check-authentication-status:
    heading: "### Step 3: Check Authentication Status"
    snippets:
      - client-read-session-state
  step-4-logout:
    heading: "### Step 4: Logout"
    snippets:
      - client-logout
```

- [ ] **Step 1: Create testdata fixtures**

`internal/manifest/testdata/sample.manifest.yml`:
```yaml
sections:
  step-1-initialize:
    heading: "### Step 1: Initialize"
    snippets:
      - client-setup
  step-2-login:
    heading: "### Step 2: Login"
    snippets:
      - client-login
      - client-login-with-access-token
```

`internal/manifest/testdata/malformed.manifest.yml`:
```yaml
sections:
  bad: [unclosed
```

- [ ] **Step 2: Write failing tests**

`internal/manifest/manifest_test.go`:
```go
package manifest_test

import (
	"path/filepath"
	"testing"

	"social-plus/harness/internal/manifest"
)

func TestLoad_valid(t *testing.T) {
	m, ok, err := manifest.LoadForPage("testdata", "sample")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if !ok {
		t.Fatal("expected manifest to be found")
	}
	if len(m.Sections) != 2 {
		t.Fatalf("want 2 sections, got %d", len(m.Sections))
	}
	sec, exists := m.Sections["step-1-initialize"]
	if !exists {
		t.Fatal("expected section step-1-initialize")
	}
	if sec.Heading != "### Step 1: Initialize" {
		t.Errorf("heading: got %q", sec.Heading)
	}
	if len(sec.Snippets) != 1 || sec.Snippets[0] != "client-setup" {
		t.Errorf("snippets: got %v", sec.Snippets)
	}
}

func TestLoad_missing(t *testing.T) {
	_, ok, err := manifest.LoadForPage("testdata", "nonexistent")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if ok {
		t.Fatal("expected not found")
	}
}

func TestLoad_malformed(t *testing.T) {
	_, _, err := manifest.LoadForPage("testdata", "malformed")
	if err == nil {
		t.Fatal("expected error for malformed YAML")
	}
}

func TestSectionForSnippet(t *testing.T) {
	m, _, _ := manifest.LoadForPage("testdata", "sample")
	sectionKey, found := m.SectionForSnippet("client-login")
	if !found {
		t.Fatal("expected to find client-login")
	}
	if sectionKey != "step-2-login" {
		t.Errorf("got section key %q", sectionKey)
	}
}

func TestSnippetPathFromDir(t *testing.T) {
	got := manifest.PathForPage(filepath.Join("testdata"), "sample")
	want := filepath.Join("testdata", "sample.manifest.yml")
	if got != want {
		t.Errorf("got %q want %q", got, want)
	}
}
```

- [ ] **Step 3: Run tests to verify they fail**

```bash
cd social-plus-docs/harness && go test ./internal/manifest/... 2>&1 | head -20
```
Expected: compile error (package doesn't exist yet)

- [ ] **Step 4: Implement `internal/manifest/manifest.go`**

```go
package manifest

import (
	"errors"
	"os"
	"path/filepath"

	"gopkg.in/yaml.v3"
)

// Section describes one section of a doc page and the snippet keys that belong there.
type Section struct {
	Heading  string   `yaml:"heading"`
	Snippets []string `yaml:"snippets"`
}

// Manifest is the parsed content of a *.manifest.yml file.
type Manifest struct {
	Sections map[string]Section `yaml:"sections"`
}

// SectionForSnippet returns the section key that contains the given snippet GendocsKey,
// and whether it was found.
func (m *Manifest) SectionForSnippet(gendocsKey string) (string, bool) {
	for key, sec := range m.Sections {
		for _, s := range sec.Snippets {
			if s == gendocsKey {
				return key, true
			}
		}
	}
	return "", false
}

// PathForPage returns the expected manifest file path for a doc page.
// docsDir is the absolute path to the docs directory; pagePath is the relative
// doc page path without extension (e.g. "social-plus-sdk/getting-started/authentication").
func PathForPage(docsDir, pagePath string) string {
	return filepath.Join(docsDir, filepath.FromSlash(pagePath)+".manifest.yml")
}

// LoadForPage loads the manifest for a doc page.
// Returns (manifest, true, nil) if found, (nil, false, nil) if not found,
// or (nil, false, err) if found but malformed.
func LoadForPage(docsDir, pagePath string) (*Manifest, bool, error) {
	path := PathForPage(docsDir, pagePath)
	data, err := os.ReadFile(path)
	if errors.Is(err, os.ErrNotExist) {
		return nil, false, nil
	}
	if err != nil {
		return nil, false, err
	}
	var m Manifest
	if err := yaml.Unmarshal(data, &m); err != nil {
		return nil, false, err
	}
	if m.Sections == nil {
		m.Sections = map[string]Section{}
	}
	return &m, true, nil
}
```

- [ ] **Step 5: Run tests to verify they pass**

```bash
cd social-plus-docs/harness && go test ./internal/manifest/... -v
```
Expected: all 5 tests PASS

- [ ] **Step 6: Commit**

```bash
cd social-plus-docs/harness
git add internal/manifest/
git commit -m "feat(manifest): add manifest package for page-level snippet specs"
```

---

## Task 2: `internal/mdxparse` package

Parses MDX files to extract `###` headings and the `<CodeGroup>` blocks that follow them.
Used by `genmanifests` to bootstrap manifest skeletons.

**Files:**
- Create: `internal/mdxparse/mdxparse.go`
- Create: `internal/mdxparse/mdxparse_test.go`
- Create: `internal/mdxparse/testdata/sample.mdx`

- [ ] **Step 1: Create testdata**

`internal/mdxparse/testdata/sample.mdx`:
```mdx
---
title: "Auth"
---

## Overview

Some prose here.

### Step 1: Initialize the SDK

Some description.

<CodeGroup>

```kotlin Android
fun init() {}
```

```swift iOS
func init() {}
```

</CodeGroup>

### Step 2: Login User

<CodeGroup>

```kotlin Android
fun login() {}
```

</CodeGroup>

### Just Prose Section

No CodeGroup here.
```

- [ ] **Step 2: Write failing tests**

`internal/mdxparse/mdxparse_test.go`:
```go
package mdxparse_test

import (
	"testing"

	"social-plus/harness/internal/mdxparse"
)

func TestExtractSections(t *testing.T) {
	sections, err := mdxparse.ExtractSections("testdata/sample.mdx")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	// Only headings followed by a CodeGroup should appear
	if len(sections) != 2 {
		t.Fatalf("want 2 sections with CodeGroups, got %d: %v", len(sections), sections)
	}
	if sections[0].Heading != "### Step 1: Initialize the SDK" {
		t.Errorf("heading[0]: %q", sections[0].Heading)
	}
	if sections[0].Slug != "step-1-initialize-the-sdk" {
		t.Errorf("slug[0]: %q", sections[0].Slug)
	}
	if sections[1].Heading != "### Step 2: Login User" {
		t.Errorf("heading[1]: %q", sections[1].Heading)
	}
}

func TestExtractSections_noCodeGroup(t *testing.T) {
	// File with no ### heading + CodeGroup combos should return empty
	sections, err := mdxparse.ExtractSections("testdata/sample.mdx")
	if err != nil {
		t.Fatal(err)
	}
	// Just prose section has no CodeGroup — shouldn't be in results
	for _, s := range sections {
		if s.Slug == "just-prose-section" {
			t.Error("prose-only section should not appear")
		}
	}
}
```

- [ ] **Step 3: Run tests to verify they fail**

```bash
cd social-plus-docs/harness && go test ./internal/mdxparse/... 2>&1 | head -10
```
Expected: compile error

- [ ] **Step 4: Implement `internal/mdxparse/mdxparse.go`**

```go
package mdxparse

import (
	"bufio"
	"os"
	"strings"
	"unicode"
)

// Section represents a ### heading that is directly followed (within 5 lines) by a <CodeGroup>.
type Section struct {
	Heading string // e.g. "### Step 1: Initialize the SDK"
	Slug    string // e.g. "step-1-initialize-the-sdk"
}

// ExtractSections scans an MDX file and returns all ### headings
// that are followed by a <CodeGroup> block within 5 lines.
func ExtractSections(path string) ([]Section, error) {
	f, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer f.Close()

	var lines []string
	sc := bufio.NewScanner(f)
	for sc.Scan() {
		lines = append(lines, sc.Text())
	}
	if err := sc.Err(); err != nil {
		return nil, err
	}

	var sections []Section
	for i, line := range lines {
		if !strings.HasPrefix(strings.TrimSpace(line), "### ") {
			continue
		}
		heading := strings.TrimSpace(line)
		// Look ahead up to 5 lines for a <CodeGroup>
		for j := i + 1; j < len(lines) && j <= i+5; j++ {
			trimmed := strings.TrimSpace(lines[j])
			if trimmed == "" {
				continue
			}
			if trimmed == "<CodeGroup>" {
				sections = append(sections, Section{
					Heading: heading,
					Slug:    slugify(strings.TrimPrefix(heading, "### ")),
				})
			}
			break // stop at first non-blank line after heading
		}
	}
	return sections, nil
}

// slugify converts "Step 1: Initialize the SDK" → "step-1-initialize-the-sdk"
func slugify(s string) string {
	var b strings.Builder
	prevDash := false
	for _, r := range strings.ToLower(s) {
		if unicode.IsLetter(r) || unicode.IsDigit(r) {
			b.WriteRune(r)
			prevDash = false
		} else if !prevDash && b.Len() > 0 {
			b.WriteRune('-')
			prevDash = true
		}
	}
	return strings.TrimRight(b.String(), "-")
}
```

- [ ] **Step 5: Run tests to verify they pass**

```bash
cd social-plus-docs/harness && go test ./internal/mdxparse/... -v
```
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add internal/mdxparse/
git commit -m "feat(mdxparse): extract ### headings with CodeGroups from MDX pages"
```

---

## Task 3: `genmanifests` command

Bootstraps `*.manifest.yml` skeleton files for all MDX pages in the docs tree.
For each page, scans for `###` headings that have a `<CodeGroup>` and writes a manifest
with empty `snippets: []` for each section. The AI agent fills in the snippet keys.
Skips pages that already have a manifest (idempotent).

**Files:**
- Create: `cmd/genmanifests.go`
- Modify: `cmd/main.go`
- Modify: `cmd/main_test.go`

- [ ] **Step 1: Write failing test for usage string**

In `cmd/main_test.go`, find the existing usage assertion and update it to include `genmanifests`:
```go
// In TestMain_usage, update the expected usage string to include:
// "  genmanifests  Bootstrap *.manifest.yml skeleton files for all doc pages"
```

Check current assertion:
```bash
grep -n "genmanifests\|migrate\|gendocs" /Users/admin/Documents/GitHub/sp-ai-agent/sp/social-plus-docs/harness/cmd/main_test.go
```

- [ ] **Step 2: Create `cmd/genmanifests.go`**

```go
package main

import (
	"flag"
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"social-plus/harness/internal/config"
	"social-plus/harness/internal/manifest"
	"social-plus/harness/internal/mdxparse"
	"gopkg.in/yaml.v3"
)

func runGenManifests(args []string) {
	fs := flag.NewFlagSet("genmanifests", flag.ExitOnError)
	cfgPath := fs.String("config", "harness-config.yml", "path to harness-config.yml")
	dryRun := fs.Bool("dry-run", false, "print what would be written without creating files")
	_ = fs.Parse(args)

	cfg, err := config.Load(*cfgPath)
	if err != nil {
		fmt.Fprintf(os.Stderr, "load config: %v\n", err)
		os.Exit(1)
	}

	docsBase := filepath.Join(filepath.Dir(*cfgPath), cfg.Docs.Path)

	created, skipped, errors := 0, 0, 0

	err = filepath.WalkDir(docsBase, func(path string, d os.DirEntry, err error) error {
		if err != nil || d.IsDir() {
			return err
		}
		if !strings.HasSuffix(path, ".mdx") {
			return nil
		}
		// Derive relative page path (without .mdx extension)
		rel, _ := filepath.Rel(docsBase, path)
		pagePath := strings.TrimSuffix(rel, ".mdx")

		// Skip if manifest already exists
		manifestPath := manifest.PathForPage(docsBase, pagePath)
		if _, statErr := os.Stat(manifestPath); statErr == nil {
			skipped++
			return nil
		}

		sections, parseErr := mdxparse.ExtractSections(path)
		if parseErr != nil {
			fmt.Fprintf(os.Stderr, "[genmanifests] WARN: parse %s: %v\n", path, parseErr)
			errors++
			return nil
		}
		if len(sections) == 0 {
			return nil // No CodeGroup sections — no manifest needed
		}

		if *dryRun {
			fmt.Printf("[genmanifests] DRY RUN: would create %s (%d sections)\n", manifestPath, len(sections))
			created++
			return nil
		}

		content := buildManifestYAML(sections)
		if writeErr := os.WriteFile(manifestPath, []byte(content), 0o644); writeErr != nil {
			fmt.Fprintf(os.Stderr, "[genmanifests] ERROR: write %s: %v\n", manifestPath, writeErr)
			errors++
			return nil
		}
		fmt.Printf("[genmanifests] CREATED: %s (%d sections)\n", manifestPath, len(sections))
		created++
		return nil
	})
	if err != nil {
		fmt.Fprintf(os.Stderr, "walk: %v\n", err)
		os.Exit(1)
	}

	fmt.Printf("[genmanifests] done — created: %d, skipped (exists): %d, errors: %d\n", created, skipped, errors)
}

// buildManifestYAML produces a manifest YAML with empty snippets for AI to fill in.
func buildManifestYAML(sections []mdxparse.Section) string {
	type sectionYAML struct {
		Heading  string   `yaml:"heading"`
		Snippets []string `yaml:"snippets"`
	}
	type manifestYAML struct {
		Sections map[string]sectionYAML `yaml:"sections"`
	}

	m := manifestYAML{Sections: make(map[string]sectionYAML)}
	for _, s := range sections {
		m.Sections[s.Slug] = sectionYAML{
			Heading:  s.Heading,
			Snippets: []string{},
		}
	}

	out, _ := yaml.Marshal(m)
	header := "# AUTO-GENERATED by harness genmanifests — fill in snippets: with GendocsKeys\n" +
		"# GendocsKey = DeriveKey(filename): strip 'Amity' prefix, PascalCase → kebab-case\n" +
		"# Example: AmityClientLogin.kt → client-login\n\n"
	return header + string(out)
}
```

- [ ] **Step 3: Register in `cmd/main.go`**

Add `genmanifests` to the switch in `runMain` and to the usage string:
```go
case "genmanifests":
    runGenManifests(args[1:])
```

And add to usage:
```
  genmanifests  Bootstrap *.manifest.yml skeleton files for all doc pages
```

- [ ] **Step 4: Update `cmd/main_test.go` usage assertion**

Find the expected usage string in the test and add the `genmanifests` line.

- [ ] **Step 5: Build and smoke-test**

```bash
cd social-plus-docs/harness
go build -o harness-bin ./cmd/
./harness-bin genmanifests --config harness-config.yml --dry-run 2>&1 | head -20
```
Expected: lines like `[genmanifests] DRY RUN: would create ...authentication.manifest.yml (4 sections)`

- [ ] **Step 6: Run all tests**

```bash
go test ./... 2>&1 | tail -20
```
Expected: all packages PASS

- [ ] **Step 7: Commit**

```bash
git add cmd/genmanifests.go cmd/main.go cmd/main_test.go
git commit -m "feat(genmanifests): bootstrap manifest skeleton files from MDX pages"
```

---

## Task 4: Section-level CodeGroup replacement in migrator

Adds `ReplaceCodeGroupAfterHeading` which finds a `<CodeGroup>` block that comes
after a specific `###` heading and replaces only that block.

**Files:**
- Modify: `internal/migrator/migrator.go`
- Modify: `internal/migrator/migrator_test.go`

- [ ] **Step 1: Write failing tests**

Add to `internal/migrator/migrator_test.go`:
```go
func TestReplaceCodeGroupAfterHeading_found(t *testing.T) {
	content := `### Step 1: Init

<CodeGroup>
` + "```kotlin\nfun init() {}\n```" + `
</CodeGroup>

### Step 2: Login

<CodeGroup>
` + "```kotlin\nfun login() {}\n```" + `
</CodeGroup>
`
	result, ok := ReplaceCodeGroupAfterHeading(content, "### Step 2: Login", "LoginUser")
	if !ok {
		t.Fatal("expected replacement to succeed")
	}
	if strings.Contains(result, "fun login()") {
		t.Error("login CodeGroup should have been replaced")
	}
	if !strings.Contains(result, "<LoginUser />") {
		t.Error("expected <LoginUser /> in result")
	}
	if strings.Contains(result, "fun init()") == false {
		// init CodeGroup should still be there
		t.Error("init CodeGroup should be untouched")
	}
}

func TestReplaceCodeGroupAfterHeading_notFound(t *testing.T) {
	content := `### Step 1: Init

<CodeGroup>
` + "```kotlin\nfun init() {}\n```" + `
</CodeGroup>
`
	_, ok := ReplaceCodeGroupAfterHeading(content, "### Step 99: Missing", "Something")
	if ok {
		t.Error("expected no replacement for missing heading")
	}
}

func TestReplaceCodeGroupAfterHeading_noCodeGroup(t *testing.T) {
	content := `### Step 1: Just Prose

Some text here, no code group.

### Step 2: Login

<CodeGroup>
` + "```kotlin\nfun login() {}\n```" + `
</CodeGroup>
`
	// heading exists but no immediate CodeGroup
	_, ok := ReplaceCodeGroupAfterHeading(content, "### Step 1: Just Prose", "Prose")
	if ok {
		t.Error("expected no replacement for heading with no CodeGroup")
	}
}
```

Note: the test file imports `strings` — verify it's already imported or add it.

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd social-plus-docs/harness && go test ./internal/migrator/... 2>&1 | head -20
```
Expected: compile error (function not defined)

- [ ] **Step 3: Implement `ReplaceCodeGroupAfterHeading` in `migrator.go`**

Add after the existing `ReplaceCodeGroup` function:

```go
// ReplaceCodeGroupAfterHeading finds the first <CodeGroup>...</CodeGroup> block that
// appears after the given heading line (exact match) and replaces it with <ComponentName />.
// Returns (updated content, true) if replaced, (original, false) if the heading or
// CodeGroup were not found.
func ReplaceCodeGroupAfterHeading(content, heading, componentName string) (string, bool) {
	lines := strings.Split(content, "\n")
	headingIdx := -1
	for i, line := range lines {
		if strings.TrimSpace(line) == strings.TrimSpace(heading) {
			headingIdx = i
			break
		}
	}
	if headingIdx == -1 {
		return content, false
	}

	// Find the next <CodeGroup> after the heading (skip blanks and prose)
	codeGroupStart := -1
	for i := headingIdx + 1; i < len(lines); i++ {
		trimmed := strings.TrimSpace(lines[i])
		if trimmed == "<CodeGroup>" {
			codeGroupStart = i
			break
		}
		// Stop if we hit another heading at the same level or higher
		if strings.HasPrefix(trimmed, "### ") || strings.HasPrefix(trimmed, "## ") {
			return content, false
		}
	}
	if codeGroupStart == -1 {
		return content, false
	}

	// Find the matching </CodeGroup>
	codeGroupEnd := -1
	for i := codeGroupStart + 1; i < len(lines); i++ {
		if strings.TrimSpace(lines[i]) == "</CodeGroup>" {
			codeGroupEnd = i
			break
		}
	}
	if codeGroupEnd == -1 {
		return content, false
	}

	// Rebuild: lines before CodeGroup + replacement + lines after
	var out []string
	out = append(out, lines[:codeGroupStart]...)
	out = append(out, "<"+componentName+" />")
	out = append(out, lines[codeGroupEnd+1:]...)
	return strings.Join(out, "\n"), true
}
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
cd social-plus-docs/harness && go test ./internal/migrator/... -v
```
Expected: all tests PASS

- [ ] **Step 5: Commit**

```bash
git add internal/migrator/
git commit -m "feat(migrator): add ReplaceCodeGroupAfterHeading for section-level targeting"
```

---

## Task 5: Update `migrate` command to use manifests

When a manifest exists for a page, use `ReplaceCodeGroupAfterHeading` for section-targeted
replacement. Fall back to the existing `ReplaceCodeGroup` (first CodeGroup) if no manifest.

**Files:**
- Modify: `cmd/migrate.go`

- [ ] **Step 1: Update `runMigrate` to load and use manifests**

Replace the existing `runMigrate` function body with:

```go
func runMigrate(args []string) {
	fs := flag.NewFlagSet("migrate", flag.ExitOnError)
	cfgPath := fs.String("config", "harness-config.yml", "path to harness-config.yml")
	reportPath := fs.String("report", "harness-report.json", "path to harness-report.json from audit")
	dryRun := fs.Bool("dry-run", false, "print planned changes without modifying files")
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

	docsBase := filepath.Join(filepath.Dir(*cfgPath), cfg.Docs.Path)

	written, skipped, warned := 0, 0, 0
	for _, f := range r.Findings {
		if f.Type != report.TypeDocPageStaleImport || f.Status != report.StatusOpen {
			continue
		}

		docPageFile := f.DocPageFile
		if docPageFile == "" {
			docPageFile = filepath.Join(docsBase, filepath.FromSlash(f.DocPage)+".mdx")
		}

		componentName := migrator.KebabToPascal(f.GendocsKey)
		importPath := "/snippets/" + strings.ReplaceAll(f.GendocsPath, string(os.PathSeparator), "/")

		if err := runMigrateFile(docPageFile, f.DocPage, f.GendocsKey, componentName, importPath, f.HasHardcodedCodeGroup, docsBase, *dryRun); err != nil {
			fmt.Fprintf(os.Stderr, "[migrate] ERROR %s: %v\n", f.DocPage, err)
			warned++
			continue
		}
		if *dryRun {
			skipped++
		} else {
			written++
			fmt.Printf("[migrate] DONE: %s → import %s\n", f.DocPage, componentName)
		}
	}

	fmt.Printf("[migrate] done — written: %d, dry-run skipped: %d, errors: %d\n", written, skipped, warned)
}

func runMigrateFile(docPageFile, docPage, gendocsKey, componentName, importPath string, hasCodeGroup bool, docsBase string, dryRun bool) error {
	content, err := os.ReadFile(docPageFile)
	if err != nil {
		return fmt.Errorf("read %s: %w", docPageFile, err)
	}

	updated := migrator.AddImport(string(content), componentName, importPath)

	if hasCodeGroup {
		// Try manifest-based section targeting first
		m, ok, manifestErr := manifest.LoadForPage(docsBase, docPage)
		replaced := false
		if manifestErr == nil && ok {
			sectionKey, inManifest := m.SectionForSnippet(gendocsKey)
			if inManifest {
				sec := m.Sections[sectionKey]
				newContent, ok2 := migrator.ReplaceCodeGroupAfterHeading(updated, sec.Heading, componentName)
				if ok2 {
					updated = newContent
					replaced = true
				}
			}
		}
		// Fall back to first CodeGroup if manifest didn't help
		if !replaced {
			newContent, ok2 := migrator.ReplaceCodeGroup(updated, componentName)
			if ok2 {
				updated = newContent
			} else {
				fmt.Printf("[migrate] WARN: CodeGroup not found in %s — import added, CodeGroup left\n", docPageFile)
			}
		}
	}

	if dryRun {
		fmt.Printf("[migrate] DRY RUN: would update %s\n  + import %s from '%s'\n", docPageFile, componentName, importPath)
		return nil
	}

	return os.WriteFile(docPageFile, []byte(updated), 0o644)
}
```

Add `"social-plus/harness/internal/manifest"` to the import block.

- [ ] **Step 2: Build and verify**

```bash
cd social-plus-docs/harness && go build -o harness-bin ./cmd/ && echo "BUILD OK"
```

- [ ] **Step 3: Run all tests**

```bash
go test ./... 2>&1 | tail -20
```
Expected: all PASS

- [ ] **Step 4: Commit**

```bash
git add cmd/migrate.go
git commit -m "feat(migrate): use manifest for section-targeted CodeGroup replacement"
```

---

## Task 6: Manifest-based `MISSING_SNIPPET` detection in differ

Adds `DiffManifestCoverage` which, for each manifest function key, checks whether
a snippet MDX file exists in `snippets/`. Missing ones become `MISSING_SNIPPET` findings
with section context (page + section key + heading).

**Files:**
- Modify: `internal/differ/differ.go`
- Modify: `internal/differ/differ_test.go`

- [ ] **Step 1: Write failing tests**

Add to `internal/differ/differ_test.go`:
```go
func TestDiffManifestCoverage_missingSnippet(t *testing.T) {
	// Create a temp dir simulating a snippets dir with one file
	tmpDir := t.TempDir()
	snippetsDir := filepath.Join(tmpDir, "snippets", "social-plus-sdk", "getting-started")
	_ = os.MkdirAll(snippetsDir, 0o755)
	// client-login.mdx exists
	_ = os.WriteFile(filepath.Join(snippetsDir, "client-login.mdx"), []byte("content"), 0o644)

	m := &manifest.Manifest{
		Sections: map[string]manifest.Section{
			"step-1-initialize": {
				Heading:  "### Step 1: Initialize",
				Snippets: []string{"client-setup"},    // MISSING — no file
			},
			"step-2-login": {
				Heading:  "### Step 2: Login",
				Snippets: []string{"client-login"},    // EXISTS
			},
		},
	}

	findings := differ.DiffManifestCoverage("social-plus-sdk/getting-started/authentication", m, filepath.Join(tmpDir, "snippets"))
	if len(findings) != 1 {
		t.Fatalf("want 1 finding, got %d", len(findings))
	}
	f := findings[0]
	if f.Type != report.TypeMissingSnippet {
		t.Errorf("type: got %s", f.Type)
	}
	if f.GendocsKey != "client-setup" {
		t.Errorf("gendocs_key: got %s", f.GendocsKey)
	}
	if f.DocPage != "social-plus-sdk/getting-started/authentication" {
		t.Errorf("doc_page: got %s", f.DocPage)
	}
	// Detail should mention the section heading
	if !strings.Contains(f.Detail, "Step 1: Initialize") {
		t.Errorf("detail should mention heading, got: %s", f.Detail)
	}
}
```

Make sure `differ_test.go` imports `"social-plus/harness/internal/manifest"` and `"path/filepath"` and `"os"`.

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd social-plus-docs/harness && go test ./internal/differ/... 2>&1 | head -20
```

- [ ] **Step 3: Add `DiffManifestCoverage` to `differ.go`**

Add to `internal/differ/differ.go`:

```go
// DiffManifestCoverage checks that every snippet key declared in a page manifest
// has a corresponding MDX file in the snippets directory.
// Returns MISSING_SNIPPET findings for any snippet key that lacks a file.
func DiffManifestCoverage(docPage string, m *manifest.Manifest, snippetsAbsDir string) []report.Finding {
	var findings []report.Finding
	for sectionKey, sec := range m.Sections {
		for _, gendocsKey := range sec.Snippets {
			// Expected file: snippetsAbsDir/<first2segs of docPage>/<key>.mdx
			// Use the same DeriveMDXPath logic
			segs := strings.SplitN(docPage, "/", 3)
			dir1, dir2 := "", ""
			if len(segs) > 0 { dir1 = segs[0] }
			if len(segs) > 1 { dir2 = segs[1] }
			mdxPath := filepath.Join(snippetsAbsDir, dir1, dir2, gendocsKey+".mdx")

			if _, err := os.Stat(mdxPath); err == nil {
				continue // exists — no finding
			}

			id := fmt.Sprintf("manifest-missing:%s:%s:%s", docPage, sectionKey, gendocsKey)
			findings = append(findings, report.Finding{
				ID:         id,
				Type:       report.TypeMissingSnippet,
				DocPage:    docPage,
				GendocsKey: gendocsKey,
				Detail:     fmt.Sprintf("manifest section %q (heading: %q) declares snippet %q — no MDX found at %s", sectionKey, sec.Heading, gendocsKey, mdxPath),
				Status:     report.StatusOpen,
			})
		}
	}
	return findings
}
```

Add imports: `"os"`, `"path/filepath"`, `"social-plus/harness/internal/manifest"` to differ.go.

- [ ] **Step 4: Run tests to verify they pass**

```bash
cd social-plus-docs/harness && go test ./internal/differ/... -v 2>&1 | tail -20
```

- [ ] **Step 5: Commit**

```bash
git add internal/differ/
git commit -m "feat(differ): add DiffManifestCoverage for manifest-based MISSING_SNIPPET"
```

---

## Task 7: Wire manifest differ into `audit` + update `prompt` section context

Updates `cmd/audit.go` to call `DiffManifestCoverage` for each page that has a manifest.
Updates `cmd/prompt.go` to include section heading in MISSING_SNIPPET task output.

**Files:**
- Modify: `cmd/audit.go`
- Modify: `cmd/prompt.go`

- [ ] **Step 1: Add manifest scan block to `cmd/audit.go`**

After the existing `DOC_PAGE_STALE_IMPORT` block, add a manifest coverage block:

```go
// --- Manifest coverage: MISSING_SNIPPET from page manifests ---
snippetsAbsDir := filepath.Join(docsBase, "snippets")
err = filepath.WalkDir(docsBase, func(path string, d os.DirEntry, err error) error {
    if err != nil || d.IsDir() || !strings.HasSuffix(path, ".manifest.yml") {
        return err
    }
    rel, _ := filepath.Rel(docsBase, path)
    pagePath := strings.TrimSuffix(filepath.ToSlash(rel), ".manifest.yml")

    m, ok, loadErr := manifest.LoadForPage(docsBase, pagePath)
    if loadErr != nil || !ok {
        return nil
    }
    manifestFindings := differ.DiffManifestCoverage(pagePath, m, snippetsAbsDir)
    for _, f := range manifestFindings {
        if !isAlreadyInReport(allFindings, f.ID) {
            allFindings = append(allFindings, f)
        }
    }
    return nil
})
if err != nil {
    fmt.Fprintf(os.Stderr, "manifest walk: %v\n", err)
}
```

Add imports: `"social-plus/harness/internal/manifest"` to `cmd/audit.go`.

- [ ] **Step 2: Update `cmd/prompt.go` to include section context**

In the `MISSING_SNIPPET` task generation, find where `detail` is set and add section context.
In the `missing` task struct add a `section` field; populate it from `f.Detail` when it
contains manifest context (detail starts with `"manifest section"`):

In the task struct:
```go
type task struct {
    platform   string
    functionID string
    snippetDir string
    lang       string
    ext        string
    docPage    string
    detail     string
    section    string  // NEW: section heading from manifest (if known)
}
```

When processing `TypeMissingSnippet` findings, extract section from detail:
```go
case report.TypeMissingSnippet:
    sectionHeading := ""
    if strings.HasPrefix(f.Detail, "manifest section") {
        // Extract heading from: manifest section "x" (heading: "### Foo") declares...
        if start := strings.Index(f.Detail, `heading: "`); start != -1 {
            rest := f.Detail[start+len(`heading: "`):]
            if end := strings.Index(rest, `"`); end != -1 {
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
        docPage:    f.DocPage,
        section:    sectionHeading,
    })
```

In the table output, add a `Section` column when section is known:
```go
sb.WriteString("| Function ID | Write to filename | Doc Page | Section |\n")
sb.WriteString("|-------------|-------------------|----------|----------|\n")
for _, t := range platTasks {
    filename := fmt.Sprintf("Amity%s.%s", sanitizeName(t.functionID), t.ext)
    sb.WriteString(fmt.Sprintf("| `%s` | `%s` | `%s` | %s |\n",
        t.functionID, filename, t.docPage, t.section))
}
```

- [ ] **Step 3: Build and run all tests**

```bash
cd social-plus-docs/harness && go build -o harness-bin ./cmd/ && go test ./... 2>&1 | tail -20
```
Expected: BUILD OK, all tests PASS

- [ ] **Step 4: Smoke-test the full pipeline**

```bash
cd social-plus-docs/harness

# Bootstrap manifest skeletons for all doc pages
./harness-bin genmanifests --config harness-config.yml --dry-run 2>&1 | tail -5

# Run audit — should show 0 manifest MISSING_SNIPPET (no manifests filled in yet)
./harness-bin audit --config harness-config.yml 2>&1 | tail -10
```

- [ ] **Step 5: Commit**

```bash
git add cmd/audit.go cmd/prompt.go
git commit -m "feat(audit,prompt): wire manifest coverage diff + section context in tasks"
```

---

## Task 8: End-to-end validation + BIG-PICTURE.md update

Run the full pipeline on a sample page (authentication) to verify section-level migration works.

**Files:**
- Modify: `harness/docs/BIG-PICTURE.md`

- [ ] **Step 1: Create a sample manifest for the authentication page**

```bash
cat > /path/to/social-plus-docs/social-plus-sdk/getting-started/authentication.manifest.yml << 'EOF'
# Sample manifest — fill snippets: with GendocsKeys from harness-report.json
sections:
  step-1-initialize-the-sdk:
    heading: "### Step 1: Initialize the SDK"
    snippets:
      - client-setup
  step-2-login-user:
    heading: "### Step 2: Login User"
    snippets:
      - client-login
  step-3-check-authentication-status:
    heading: "### Step 3: Check Authentication Status"
    snippets:
      - client-read-session-state
  step-4-logout:
    heading: "### Step 4: Logout"
    snippets:
      - client-logout
EOF
```

- [ ] **Step 2: Run audit to verify manifest findings are detected**

```bash
cd social-plus-docs/harness && ./harness-bin audit --config harness-config.yml 2>&1 | grep -i "manifest\|missing"
```
Expected: 0 MISSING_SNIPPET (all 4 snippet MDX files should already exist from gendocs)

- [ ] **Step 3: Run migrate with dry-run on authentication page**

```bash
./harness-bin migrate --config harness-config.yml --dry-run 2>&1 | grep -i "authentication"
```
Expected: lines showing which imports would be added with section targeting

- [ ] **Step 4: Update BIG-PICTURE.md current state table**

In `harness/docs/BIG-PICTURE.md`, update the current state table:
- `Page manifests` → ✅ (genmanifests bootstraps skeletons; AI fills snippet keys)
- `Section-level migration` → ✅ (migrate uses manifest heading for CodeGroup targeting)
- `Manifest-based MISSING_SNIPPET` → ✅ (audit reads manifests, emits findings with section context)

- [ ] **Step 5: Final commit**

```bash
git add harness/docs/BIG-PICTURE.md social-plus-sdk/getting-started/authentication.manifest.yml
git commit -m "feat: end-to-end manifest system — genmanifests, section-level migrate, manifest audit

Phase 1 manifest system complete:
- internal/manifest: parse *.manifest.yml files
- internal/mdxparse: extract ### headings with CodeGroups
- genmanifests command: bootstrap skeleton manifests for all doc pages  
- migrator: section-level ReplaceCodeGroupAfterHeading
- migrate: uses manifest heading for CodeGroup targeting, falls back to first
- differ: DiffManifestCoverage emits MISSING_SNIPPET per manifest entry
- audit: wires manifest coverage diff
- prompt: includes section heading in AI task output
- Sample manifest for authentication page

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

---

## Self-Review

**Spec coverage:**
- ✅ `internal/manifest` package with `LoadForPage`, `SectionForSnippet`, `PathForPage`
- ✅ `internal/mdxparse` with `ExtractSections` (headings with CodeGroup detection)
- ✅ `genmanifests` command (bootstrap skeleton manifests, idempotent)
- ✅ `ReplaceCodeGroupAfterHeading` in migrator
- ✅ `migrate` updated: manifest → section-targeted, fallback to first CodeGroup
- ✅ `DiffManifestCoverage` in differ
- ✅ `audit` wired to manifest diff
- ✅ `prompt` includes section context
- ✅ `BIG-PICTURE.md` updated
- ✅ All tests TDD-first, all commands have build verification

**Type consistency check:**
- `manifest.Section.Snippets []string` = GendocsKeys → used in `SectionForSnippet(gendocsKey string)` ✅
- `manifest.LoadForPage(docsDir, pagePath string)` → called in migrate with `docsBase, f.DocPage` ✅
- `mdxparse.Section.Slug` → used as manifest section key ✅
- `differ.DiffManifestCoverage(docPage string, m *manifest.Manifest, snippetsAbsDir string)` → called in audit with `pagePath, m, snippetsAbsDir` ✅
- `migrator.ReplaceCodeGroupAfterHeading(content, heading, componentName string)` → called in migrate with `updated, sec.Heading, componentName` ✅
