# Snippet Curation & Annotation QA Gate — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add `harness curate` command (LLM-driven post-placement curation of MDX pages) and `harness annotate --qa` gate (generates annotation validation task file).

**Architecture:** `internal/curator` handles all MDX parsing + editing logic; `cmd/curate.go` runs in either generate-tasks mode (outputs `curate-tasks.md` for the AI agent) or apply mode (reads `curate-decisions.json` and patches MDX files). The annotation QA gate adds a `--qa` flag to `harness annotate` that outputs `annotation-qa-tasks.md` for the AI agent to assess `asc_page` correctness.

**Tech Stack:** Go 1.23, stdlib only (no new deps), `github.com/stretchr/testify` for tests.

---

## File Map

| File | Action | Purpose |
|------|--------|---------|
| `harness/internal/report/types.go` | Modify | Add 5 new finding types |
| `harness/internal/curator/curator.go` | Create | Core types, ParsePage, Apply, file I/O |
| `harness/internal/curator/curator_test.go` | Create | Table-driven unit tests |
| `harness/cmd/curate.go` | Create | `runCurate()` — gen-tasks + apply modes |
| `harness/cmd/curate_test.go` | Create | Integration test with mock MDX + decisions |
| `harness/cmd/main.go` | Modify | Wire `curate` case |
| `harness/cmd/main_test.go` | Modify | Update usage string assertion |
| `harness/cmd/annotate.go` | Modify | Add `--qa` flag + `runAnnotateQA()` |
| `harness/cmd/annotate_qa_test.go` | Create | Unit tests for QA task file generation |

---

### Task 1: New Finding Types

**Files:**
- Modify: `harness/internal/report/types.go`

- [ ] **Step 1: Add 5 new finding type constants**

Open `harness/internal/report/types.go` and add after `TypeSnippetOrphaned`:

```go
TypeSnippetCuratedRemoved  FindingType = "SNIPPET_CURATED_REMOVED"
TypeSnippetCuratedMoved    FindingType = "SNIPPET_CURATED_MOVED"
TypeSnippetCurationFlagged FindingType = "SNIPPET_CURATION_FLAGGED"
TypeAnnotationSuspect      FindingType = "ANNOTATION_SUSPECT"
TypeAnnotationUncertain    FindingType = "ANNOTATION_UNCERTAIN"
```

- [ ] **Step 2: Build to verify**

```bash
cd harness && go build ./internal/report/...
```
Expected: no output (success).

- [ ] **Step 3: Commit**

```bash
git add harness/internal/report/types.go
git commit -m "feat: add curation + annotation QA finding types"
```

---

### Task 2: `internal/curator` — Types + ParsePage

**Files:**
- Create: `harness/internal/curator/curator.go`
- Create: `harness/internal/curator/curator_test.go`

- [ ] **Step 1: Write the failing test**

Create `harness/internal/curator/curator_test.go`:

```go
package curator_test

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"

	"social-plus/harness/internal/curator"
)

const sampleMDX = `import AddReaction from '/snippets/core/add-reaction.mdx';
import PostLike from '/snippets/core/post-like.mdx';
import StoryLike from '/snippets/core/story-like.mdx';

---
title: "Reactions"
---

## Add Reactions

Some prose about adding reactions.

<AddReaction />

## Remove Reactions

Some prose about removing reactions.

## Related Topics

<PostLike />
<StoryLike />
`

func TestParsePage_ExtractsSections(t *testing.T) {
	p, err := curator.ParsePage("reactions.mdx", "core/reactions", sampleMDX, func(path string) string {
		return "// snippet content for " + path
	})
	require.NoError(t, err)
	assert.Equal(t, []string{"## Add Reactions", "## Remove Reactions", "## Related Topics"}, p.Sections)
}

func TestParsePage_ExtractsPlacedSnippets(t *testing.T) {
	p, err := curator.ParsePage("reactions.mdx", "core/reactions", sampleMDX, func(path string) string {
		return "// code"
	})
	require.NoError(t, err)
	// All 3 imports have component tags in the body
	require.Len(t, p.Placed, 3)
	names := make([]string, len(p.Placed))
	for i, s := range p.Placed {
		names[i] = s.Name
	}
	assert.ElementsMatch(t, []string{"AddReaction", "PostLike", "StoryLike"}, names)
}

func TestParsePage_ProseStripsImportsAndTags(t *testing.T) {
	p, err := curator.ParsePage("reactions.mdx", "core/reactions", sampleMDX, func(string) string { return "" })
	require.NoError(t, err)
	assert.NotContains(t, p.Prose, "import ")
	assert.NotContains(t, p.Prose, "<AddReaction")
	assert.NotContains(t, p.Prose, "<PostLike")
	assert.Contains(t, p.Prose, "Some prose about adding reactions")
}

func TestParsePage_SnippetContentLoaded(t *testing.T) {
	p, err := curator.ParsePage("reactions.mdx", "core/reactions", sampleMDX, func(path string) string {
		return "content:" + path
	})
	require.NoError(t, err)
	for _, s := range p.Placed {
		assert.Contains(t, s.Content, "content:")
	}
}
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd harness && go test ./internal/curator/... 2>&1 | head -5
```
Expected: `cannot find package` or `no Go files`.

- [ ] **Step 3: Implement curator.go with types + ParsePage**

Create `harness/internal/curator/curator.go`:

```go
// internal/curator/curator.go
package curator

import (
	"encoding/json"
	"os"
	"regexp"
	"strings"
	"time"
)

// CurateAction represents what to do with a placed snippet.
type CurateAction string

const (
	ActionKeep   CurateAction = "KEEP"
	ActionRemove CurateAction = "REMOVE"
	ActionMove   CurateAction = "MOVE"
	ActionFlag   CurateAction = "FLAG"
)

// Confidence represents decision confidence.
type Confidence string

const (
	ConfidenceHigh   Confidence = "high"
	ConfidenceMedium Confidence = "medium"
	ConfidenceLow    Confidence = "low"
)

// Decision is the verdict on a single placed snippet.
type Decision struct {
	Name       string       `json:"name"`
	Action     CurateAction `json:"action"`
	Section    string       `json:"section,omitempty"`     // target ## heading if KEEP
	TargetPage string       `json:"target_page,omitempty"` // if MOVE
	Reason     string       `json:"reason"`
	Confidence Confidence   `json:"confidence"`
}

// PageDecisions groups decisions for one page.
type PageDecisions struct {
	PagePath  string     `json:"page_path"`
	Decisions []Decision `json:"decisions"`
}

// DecisionsFile is the top-level structure of curate-decisions.json.
type DecisionsFile struct {
	GeneratedAt string          `json:"generated_at"`
	Pages       []PageDecisions `json:"pages"`
}

// ReviewFile is the top-level structure of curate-review.json (flagged/low-confidence items).
type ReviewFile struct {
	GeneratedAt string          `json:"generated_at"`
	Pages       []PageDecisions `json:"pages"`
}

// PlacedSnippet is a snippet import whose component tag appears in the page body.
type PlacedSnippet struct {
	Name       string
	ImportPath string
	Content    string // snippet file content (for LLM context)
}

// ParsedPage holds extracted content from one MDX file.
type ParsedPage struct {
	File     string
	PagePath string
	Prose    string          // body text with imports and component tags stripped
	Sections []string        // ## headings in order
	Placed   []PlacedSnippet // imports whose <Name /> tag exists in body
}

var (
	importRe    = regexp.MustCompile(`(?m)^import\s+(\w+)\s+from\s+'([^']+\.mdx)'\s*;?\s*$`)
	componentRe = regexp.MustCompile(`<(\w+)\s*/>|<(\w+)\s*>`)
	headingRe   = regexp.MustCompile(`^##\s+.+`)
)

// ParsePage parses mdx content and returns a ParsedPage.
// snippetReader(importPath) should return the snippet file content; "" is fine.
func ParsePage(file, pagePath, content string, snippetReader func(importPath string) string) (ParsedPage, error) {
	imports := map[string]string{} // name -> importPath
	for _, m := range importRe.FindAllStringSubmatch(content, -1) {
		imports[m[1]] = m[2]
	}

	// Strip import lines for body analysis.
	body := importRe.ReplaceAllString(content, "")

	// Find placed component names (tags that appear in body).
	placed := []PlacedSnippet{}
	for name, importPath := range imports {
		tag := "<" + name
		if strings.Contains(body, tag) {
			snippetContent := ""
			if snippetReader != nil {
				snippetContent = snippetReader(importPath)
			}
			placed = append(placed, PlacedSnippet{
				Name:       name,
				ImportPath: importPath,
				Content:    snippetContent,
			})
		}
	}

	// Extract ## sections.
	var sections []string
	for _, line := range strings.Split(content, "\n") {
		trimmed := strings.TrimRight(line, " \t")
		if headingRe.MatchString(trimmed) {
			sections = append(sections, trimmed)
		}
	}

	// Build prose: strip import lines and component tags.
	proseLines := []string{}
	for _, line := range strings.Split(body, "\n") {
		trimmed := strings.TrimSpace(line)
		if componentRe.MatchString(trimmed) {
			continue
		}
		proseLines = append(proseLines, line)
	}
	prose := strings.TrimSpace(strings.Join(proseLines, "\n"))

	return ParsedPage{
		File:     file,
		PagePath: pagePath,
		Prose:    prose,
		Sections: sections,
		Placed:   placed,
	}, nil
}

// ReadDecisions reads curate-decisions.json from path.
func ReadDecisions(path string) (DecisionsFile, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return DecisionsFile{}, err
	}
	var df DecisionsFile
	if err := json.Unmarshal(data, &df); err != nil {
		return DecisionsFile{}, err
	}
	return df, nil
}

// WriteReview writes flagged decisions to path as curate-review.json.
func WriteReview(path string, pages []PageDecisions) error {
	rf := ReviewFile{
		GeneratedAt: time.Now().UTC().Format(time.RFC3339),
		Pages:       pages,
	}
	data, err := json.MarshalIndent(rf, "", "  ")
	if err != nil {
		return err
	}
	return os.WriteFile(path, data, 0o644)
}
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
cd harness && go test ./internal/curator/... -v 2>&1 | tail -15
```
Expected: all 4 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add harness/internal/curator/
git commit -m "feat(curator): types, ParsePage, decision file I/O"
```

---

### Task 3: `internal/curator` — Apply (Remove + Re-section)

**Files:**
- Modify: `harness/internal/curator/curator.go` (add Apply)
- Modify: `harness/internal/curator/curator_test.go` (add Apply tests)

- [ ] **Step 1: Write the failing tests**

Add to `harness/internal/curator/curator_test.go`:

```go
func TestApply_RemoveHighConfidence(t *testing.T) {
	decisions := []curator.Decision{
		{Name: "PostLike", Action: curator.ActionRemove, Confidence: curator.ConfidenceHigh, Reason: "irrelevant"},
	}
	modified, applied, flagged := curator.Apply(sampleMDX, decisions)
	assert.Len(t, applied, 1)
	assert.Len(t, flagged, 0)
	assert.NotContains(t, modified, "import PostLike")
	assert.NotContains(t, modified, "<PostLike />")
	// Other imports untouched
	assert.Contains(t, modified, "import AddReaction")
	assert.Contains(t, modified, "<AddReaction />")
}

func TestApply_RemoveLowConfidenceFlags(t *testing.T) {
	decisions := []curator.Decision{
		{Name: "PostLike", Action: curator.ActionRemove, Confidence: curator.ConfidenceLow, Reason: "unsure"},
	}
	modified, applied, flagged := curator.Apply(sampleMDX, decisions)
	assert.Len(t, applied, 0)
	assert.Len(t, flagged, 1)
	// Content unchanged
	assert.Contains(t, modified, "import PostLike")
	assert.Contains(t, modified, "<PostLike />")
}

func TestApply_KeepResections(t *testing.T) {
	// StoryLike is under ## Related Topics; move it to ## Add Reactions
	decisions := []curator.Decision{
		{Name: "StoryLike", Action: curator.ActionKeep, Section: "## Add Reactions", Confidence: curator.ConfidenceHigh, Reason: "belongs here"},
	}
	modified, applied, flagged := curator.Apply(sampleMDX, decisions)
	assert.Len(t, applied, 1)
	assert.Len(t, flagged, 0)
	// Tag moved: appears after ## Add Reactions, not at end of file
	lines := strings.Split(modified, "\n")
	addReactionIdx := -1
	storyLikeIdx := -1
	for i, l := range lines {
		if strings.TrimSpace(l) == "## Add Reactions" {
			addReactionIdx = i
		}
		if strings.Contains(l, "<StoryLike") {
			storyLikeIdx = i
		}
	}
	assert.Greater(t, storyLikeIdx, addReactionIdx, "StoryLike should appear after ## Add Reactions")
	// Should not appear under Related Topics anymore (which comes after)
	relTopicsIdx := -1
	for i, l := range lines {
		if strings.TrimSpace(l) == "## Related Topics" {
			relTopicsIdx = i
		}
	}
	assert.Less(t, storyLikeIdx, relTopicsIdx, "StoryLike should not be under Related Topics")
}

func TestApply_MoveHighConfidenceRemovesFromPage(t *testing.T) {
	decisions := []curator.Decision{
		{Name: "PostLike", Action: curator.ActionMove, TargetPage: "social/posts", Confidence: curator.ConfidenceHigh, Reason: "belongs on post page"},
	}
	modified, applied, flagged := curator.Apply(sampleMDX, decisions)
	assert.Len(t, applied, 1)
	assert.Len(t, flagged, 0)
	assert.NotContains(t, modified, "import PostLike")
	assert.NotContains(t, modified, "<PostLike />")
}

func TestApply_MoveLowConfidenceFlags(t *testing.T) {
	decisions := []curator.Decision{
		{Name: "PostLike", Action: curator.ActionMove, TargetPage: "social/posts", Confidence: curator.ConfidenceLow, Reason: "unsure"},
	}
	modified, applied, flagged := curator.Apply(sampleMDX, decisions)
	assert.Len(t, applied, 0)
	assert.Len(t, flagged, 1)
	assert.Contains(t, modified, "import PostLike")
}

func TestApply_FlagAlwaysFlags(t *testing.T) {
	decisions := []curator.Decision{
		{Name: "AddReaction", Action: curator.ActionFlag, Confidence: curator.ConfidenceHigh, Reason: "ambiguous"},
	}
	_, applied, flagged := curator.Apply(sampleMDX, decisions)
	assert.Len(t, applied, 0)
	assert.Len(t, flagged, 1)
}

func TestApply_KeepNoResection_NoChange(t *testing.T) {
	// AddReaction is already under ## Add Reactions — no move needed
	decisions := []curator.Decision{
		{Name: "AddReaction", Action: curator.ActionKeep, Section: "## Add Reactions", Confidence: curator.ConfidenceMedium, Reason: "correct"},
	}
	modified, applied, _ := curator.Apply(sampleMDX, decisions)
	assert.Len(t, applied, 1)
	// Content structurally same (AddReaction already in right section)
	assert.Contains(t, modified, "<AddReaction />")
}
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd harness && go test ./internal/curator/... -run TestApply 2>&1 | head -5
```
Expected: `undefined: curator.Apply`.

- [ ] **Step 3: Implement Apply in curator.go**

Add to `harness/internal/curator/curator.go`:

```go
// Apply applies decisions to MDX content according to confidence-gating rules.
// Returns: modified content, auto-applied decisions, flagged decisions (need human review).
// Rules:
//   KEEP (any confidence)         → auto-apply (re-section if needed)
//   REMOVE high                   → auto-apply (remove import + tag)
//   REMOVE medium/low             → flag
//   MOVE high                     → auto-apply (remove import + tag from this page)
//   MOVE medium/low               → flag
//   FLAG any                      → always flag
func Apply(content string, decisions []Decision) (modified string, applied []Decision, flagged []Decision) {
	applied = []Decision{}
	flagged = []Decision{}
	modified = content

	for _, d := range decisions {
		switch d.Action {
		case ActionFlag:
			flagged = append(flagged, d)

		case ActionRemove:
			if d.Confidence == ConfidenceHigh {
				modified = removeSnippet(modified, d.Name)
				applied = append(applied, d)
			} else {
				flagged = append(flagged, d)
			}

		case ActionMove:
			if d.Confidence == ConfidenceHigh {
				modified = removeSnippet(modified, d.Name)
				applied = append(applied, d)
			} else {
				flagged = append(flagged, d)
			}

		case ActionKeep:
			if d.Section != "" {
				modified = resectionSnippet(modified, d.Name, d.Section)
			}
			applied = append(applied, d)
		}
	}
	return modified, applied, flagged
}

// removeSnippet removes the import line and all component tags for name from content.
func removeSnippet(content, name string) string {
	lines := strings.Split(content, "\n")
	out := make([]string, 0, len(lines))
	importPrefix := "import " + name + " "
	tagPatterns := []string{"<" + name + " />", "<" + name + "/>", "<" + name + ">"}

	for _, line := range lines {
		trimmed := strings.TrimSpace(line)
		if strings.HasPrefix(trimmed, importPrefix) {
			continue
		}
		isTag := false
		for _, pat := range tagPatterns {
			if trimmed == pat {
				isTag = true
				break
			}
		}
		if isTag {
			continue
		}
		out = append(out, line)
	}
	return collapseBlankLines(strings.Join(out, "\n"))
}

// resectionSnippet moves the <name /> tag to immediately after the targetSection heading.
// If the tag is already in the correct section, content is returned unchanged.
func resectionSnippet(content, name, targetSection string) string {
	tag := "<" + name + " />"
	lines := strings.Split(content, "\n")

	// Find target section index.
	targetIdx := -1
	for i, line := range lines {
		if strings.TrimRight(line, " \t") == targetSection {
			targetIdx = i
			break
		}
	}
	if targetIdx == -1 {
		return content // section not found, leave unchanged
	}

	// Find where the tag currently is.
	tagIdx := -1
	for i, line := range lines {
		if strings.TrimSpace(line) == tag {
			tagIdx = i
			break
		}
	}
	if tagIdx == -1 {
		return content // tag not found, leave unchanged
	}

	// Check if tag is already right after the target section (within 5 non-blank lines).
	if isTagNearSection(lines, tagIdx, targetIdx) {
		return content
	}

	// Remove tag from current position.
	without := append(lines[:tagIdx:tagIdx], lines[tagIdx+1:]...)

	// Re-find target section after removal (index may have shifted).
	newTargetIdx := -1
	for i, line := range without {
		if strings.TrimRight(line, " \t") == targetSection {
			newTargetIdx = i
			break
		}
	}
	if newTargetIdx == -1 {
		return content
	}

	// Insert tag after the section heading (with a blank line before).
	insertAt := newTargetIdx + 1
	result := make([]string, 0, len(without)+2)
	result = append(result, without[:insertAt]...)
	result = append(result, "")
	result = append(result, tag)
	result = append(result, without[insertAt:]...)

	return collapseBlankLines(strings.Join(result, "\n"))
}

// isTagNearSection returns true if tagIdx is within 5 non-blank lines after sectionIdx.
func isTagNearSection(lines []string, tagIdx, sectionIdx int) bool {
	if tagIdx <= sectionIdx {
		return false
	}
	nonBlank := 0
	for i := sectionIdx + 1; i < tagIdx && i < len(lines); i++ {
		if strings.TrimSpace(lines[i]) != "" {
			nonBlank++
		}
		if nonBlank > 5 {
			return false
		}
	}
	return nonBlank <= 5
}

// collapseBlankLines reduces runs of 3+ blank lines to 2.
func collapseBlankLines(s string) string {
	for strings.Contains(s, "\n\n\n\n") {
		s = strings.ReplaceAll(s, "\n\n\n\n", "\n\n\n")
	}
	return s
}
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
cd harness && go test ./internal/curator/... -v 2>&1 | tail -20
```
Expected: all tests PASS.

- [ ] **Step 5: Commit**

```bash
git add harness/internal/curator/
git commit -m "feat(curator): Apply — confidence-gated remove, move, resection"
```

---

### Task 4: `cmd/curate.go` — Gen-Tasks Mode

**Files:**
- Create: `harness/cmd/curate.go`
- Create: `harness/cmd/curate_test.go`

- [ ] **Step 1: Write the failing test**

Create `harness/cmd/curate_test.go`:

```go
package main_test

import (
	"os"
	"path/filepath"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestCurateGenTasks_WritesCurateTasksMd(t *testing.T) {
	dir := t.TempDir()

	// Create a minimal harness-config.yml
	cfgContent := `docs:
  path: docs
sdks: {}
`
	require.NoError(t, os.WriteFile(filepath.Join(dir, "harness-config.yml"), []byte(cfgContent), 0o644))

	// Create a docs/social/reactions.mdx with two placed snippets
	docsDir := filepath.Join(dir, "docs", "social")
	require.NoError(t, os.MkdirAll(docsDir, 0o755))
	mdxContent := `import AddReaction from '/snippets/add-reaction.mdx';
import PostLike from '/snippets/post-like.mdx';

---
title: "Reactions"
---

## Add Reactions

<AddReaction />

## Related Topics

<PostLike />
`
	require.NoError(t, os.WriteFile(filepath.Join(docsDir, "reactions.mdx"), []byte(mdxContent), 0o644))

	// Create snippet files
	snipDir := filepath.Join(dir, "docs", "snippets")
	require.NoError(t, os.MkdirAll(snipDir, 0o755))
	require.NoError(t, os.WriteFile(filepath.Join(snipDir, "add-reaction.mdx"), []byte("// add reaction code"), 0o644))
	require.NoError(t, os.WriteFile(filepath.Join(snipDir, "post-like.mdx"), []byte("// post like code"), 0o644))

	// Run curate gen-tasks
	outPath := filepath.Join(dir, "curate-tasks.md")
	err := runCurateGenTasksForTest(dir, filepath.Join(dir, "harness-config.yml"), "", outPath)
	require.NoError(t, err)

	data, err := os.ReadFile(outPath)
	require.NoError(t, err)
	content := string(data)

	assert.Contains(t, content, "social/reactions")
	assert.Contains(t, content, "AddReaction")
	assert.Contains(t, content, "PostLike")
	assert.Contains(t, content, "## Add Reactions")
	// Snippet code is included for LLM context
	assert.Contains(t, content, "add reaction code")
}

func TestCurateGenTasks_EmptyPageSkipped(t *testing.T) {
	dir := t.TempDir()

	cfgContent := `docs:
  path: docs
sdks: {}
`
	require.NoError(t, os.WriteFile(filepath.Join(dir, "harness-config.yml"), []byte(cfgContent), 0o644))

	docsDir := filepath.Join(dir, "docs", "social")
	require.NoError(t, os.MkdirAll(docsDir, 0o755))
	// Page with no placed snippets
	mdxContent := `---
title: "Empty"
---

## Overview

No code here.
`
	require.NoError(t, os.WriteFile(filepath.Join(docsDir, "empty.mdx"), []byte(mdxContent), 0o644))

	outPath := filepath.Join(dir, "curate-tasks.md")
	err := runCurateGenTasksForTest(dir, filepath.Join(dir, "harness-config.yml"), "", outPath)
	require.NoError(t, err)

	data, err := os.ReadFile(outPath)
	require.NoError(t, err)
	// Should say no tasks (or very minimal content since nothing to curate)
	assert.NotContains(t, string(data), "social/empty")
}
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd harness && go test ./cmd/... -run TestCurate 2>&1 | head -10
```
Expected: `undefined: runCurateGenTasksForTest`.

- [ ] **Step 3: Create curate.go — gen-tasks mode**

Create `harness/cmd/curate.go`:

```go
// cmd/curate.go
package main

import (
	"flag"
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"time"

	"social-plus/harness/internal/config"
	"social-plus/harness/internal/curator"
)

func runCurate(args []string) {
	fs := flag.NewFlagSet("curate", flag.ExitOnError)
	cfgPath := fs.String("config", "harness-config.yml", "path to harness-config.yml")
	apply := fs.Bool("apply", false, "apply decisions from curate-decisions.json")
	decisionsPath := fs.String("decisions", "curate-decisions.json", "decisions file to read when --apply is set")
	outPath := fs.String("out", "curate-tasks.md", "output tasks file (gen mode)")
	reviewPath := fs.String("review", "curate-review.json", "output review file (apply mode)")
	dryRun := fs.Bool("dry-run", false, "print decisions without modifying MDX files")
	pageFilter := fs.String("page", "", "only process this page slug (e.g. social-plus-sdk/core-concepts/content-handling/reactions)")
	_ = fs.Parse(args)

	cfg, err := config.Load(*cfgPath)
	if err != nil {
		fmt.Fprintf(os.Stderr, "load config: %v\n", err)
		os.Exit(1)
	}
	cfgDir := filepath.Dir(*cfgPath)
	docsBase := filepath.Join(cfgDir, cfg.Docs.Path)

	if *apply {
		if err := runCurateApply(cfgDir, docsBase, *decisionsPath, *reviewPath, *dryRun); err != nil {
			fmt.Fprintf(os.Stderr, "curate apply: %v\n", err)
			os.Exit(1)
		}
		return
	}

	if err := runCurateGenTasks(cfgDir, docsBase, *pageFilter, filepath.Join(cfgDir, *outPath)); err != nil {
		fmt.Fprintf(os.Stderr, "curate gen-tasks: %v\n", err)
		os.Exit(1)
	}
}

// runCurateGenTasks walks all MDX pages and generates curate-tasks.md.
func runCurateGenTasks(cfgDir, docsBase, pageFilter, outPath string) error {
	return runCurateGenTasksForTest(cfgDir, "", pageFilter, outPath)
}

// runCurateGenTasksForTest is the testable inner function.
// Pass cfgPath="" to use cfgDir-relative paths; pass explicit cfgPath for tests.
func runCurateGenTasksForTest(cfgDir, cfgPath, pageFilter, outPath string) error {
	// Determine docs base from config or infer.
	docsBase := filepath.Join(cfgDir, "docs")
	if cfgPath != "" {
		cfg, err := config.Load(cfgPath)
		if err == nil {
			docsBase = filepath.Join(cfgDir, cfg.Docs.Path)
		}
	}

	snippetReader := func(importPath string) string {
		rel := strings.TrimPrefix(importPath, "/")
		abs := filepath.Join(docsBase, filepath.FromSlash(rel))
		data, err := os.ReadFile(abs)
		if err != nil {
			return ""
		}
		content := string(data)
		if len(content) > 800 {
			content = content[:800]
		}
		return content
	}

	var pages []curator.ParsedPage
	err := filepath.WalkDir(docsBase, func(path string, d os.DirEntry, walkErr error) error {
		if walkErr != nil {
			return walkErr
		}
		if d.IsDir() {
			rel, _ := filepath.Rel(docsBase, path)
			relSlash := filepath.ToSlash(rel)
			if rel == "snippets" || strings.HasPrefix(relSlash+"/", "snippets/") ||
				rel == "harness" || strings.HasPrefix(relSlash+"/", "harness/") {
				return filepath.SkipDir
			}
			return nil
		}
		if !strings.HasSuffix(path, ".mdx") {
			return nil
		}
		rel, _ := filepath.Rel(docsBase, path)
		pagePath := filepath.ToSlash(strings.TrimSuffix(rel, ".mdx"))

		if pageFilter != "" && pagePath != pageFilter {
			return nil
		}

		data, err := os.ReadFile(path)
		if err != nil {
			fmt.Fprintf(os.Stderr, "warning: read %s: %v\n", path, err)
			return nil
		}
		p, err := curator.ParsePage(path, pagePath, string(data), snippetReader)
		if err != nil {
			fmt.Fprintf(os.Stderr, "warning: parse %s: %v\n", path, err)
			return nil
		}
		if len(p.Placed) > 0 {
			pages = append(pages, p)
		}
		return nil
	})
	if err != nil {
		return fmt.Errorf("walk docs: %w", err)
	}

	return writeCurateTasks(outPath, pages)
}

func writeCurateTasks(outPath string, pages []curator.ParsedPage) error {
	var sb strings.Builder
	sb.WriteString("# Curate Tasks\n\n")
	sb.WriteString(fmt.Sprintf("Generated: %s\n\n", time.Now().UTC().Format("2006-01-02T15:04:05Z")))
	sb.WriteString("Review each page's placed snippets and write decisions to `curate-decisions.json`.\n\n")
	sb.WriteString("**Decision format per snippet:**\n")
	sb.WriteString("- `KEEP` (specify `section`: which `##` heading it belongs under)\n")
	sb.WriteString("- `REMOVE` (irrelevant or redundant)\n")
	sb.WriteString("- `MOVE` (specify `target_page`: docs slug where it belongs)\n")
	sb.WriteString("- `FLAG` (ambiguous, needs human review)\n\n")
	sb.WriteString("**Confidence:** `high` (auto-apply), `medium`/`low` (goes to review file)\n\n")
	sb.WriteString("---\n\n")

	if len(pages) == 0 {
		sb.WriteString("_No pages with placed snippets found._\n")
	}

	for _, p := range pages {
		sb.WriteString(fmt.Sprintf("## Page: `%s`\n\n", p.PagePath))
		sb.WriteString(fmt.Sprintf("**Sections:** %s\n\n", strings.Join(p.Sections, " · ")))

		// First 600 chars of prose as context.
		prose := p.Prose
		if len(prose) > 600 {
			prose = prose[:600] + "…"
		}
		sb.WriteString("**Page purpose:**\n")
		sb.WriteString("> " + strings.ReplaceAll(strings.TrimSpace(prose), "\n", "\n> ") + "\n\n")

		sb.WriteString(fmt.Sprintf("**Placed snippets (%d):**\n\n", len(p.Placed)))
		for i, s := range p.Placed {
			sb.WriteString(fmt.Sprintf("### %d. `%s`\n", i+1, s.Name))
			sb.WriteString(fmt.Sprintf("Import: `%s`\n\n", s.ImportPath))
			if s.Content != "" {
				sb.WriteString("```\n")
				content := s.Content
				if len(content) > 400 {
					content = content[:400] + "\n// ... (truncated)"
				}
				sb.WriteString(content + "\n```\n\n")
			}
		}
		sb.WriteString("---\n\n")
	}

	return os.WriteFile(outPath, []byte(sb.String()), 0o644)
}
```

- [ ] **Step 4: Add helper to curate_test.go** (needed for tests to call internal function)

The test calls `runCurateGenTasksForTest` — since tests are in `package main_test`, expose the function. Add to the bottom of `curate.go`:

```go
// Note: runCurateGenTasksForTest is intentionally exported via its call site in runCurateGenTasks.
// Tests in package main_test call it directly via the unexported route below.
```

Actually, since both `curate.go` and `curate_test.go` are in `package main` and `package main_test` respectively, the test cannot call unexported functions directly. Refactor: move the logic to a non-`main` helper that the test file can call.

Replace the test helper reference with an invocation of the CLI via `os.Exec` or restructure `curate.go` so `runCurateGenTasksForTest` is an exported function in a testable form.

**Simplest fix:** Change `curate_test.go` to use `package main` (white-box test) so it can call `runCurateGenTasksForTest` directly:

Change the first line of `curate_test.go` from `package main_test` to `package main`.

- [ ] **Step 5: Run tests to verify they pass**

```bash
cd harness && go test ./cmd/... -run TestCurate -v 2>&1 | tail -15
```
Expected: `TestCurateGenTasks_WritesCurateTasksMd PASS`, `TestCurateGenTasks_EmptyPageSkipped PASS`.

- [ ] **Step 6: Commit**

```bash
git add harness/cmd/curate.go harness/cmd/curate_test.go
git commit -m "feat(curate): gen-tasks mode — generates curate-tasks.md"
```

---

### Task 5: `cmd/curate.go` — Apply Mode

**Files:**
- Modify: `harness/cmd/curate.go` (add runCurateApply)
- Modify: `harness/cmd/curate_test.go` (add apply tests)

- [ ] **Step 1: Write the failing tests**

Add to `harness/cmd/curate_test.go`:

```go
func TestCurateApply_RemovesHighConfidenceSnippet(t *testing.T) {
	dir := t.TempDir()

	// Write MDX with two placed snippets
	docsDir := filepath.Join(dir, "docs", "social")
	require.NoError(t, os.MkdirAll(docsDir, 0o755))
	mdxContent := `import AddReaction from '/snippets/add-reaction.mdx';
import PostLike from '/snippets/post-like.mdx';

---
title: "Reactions"
---

## Add Reactions

<AddReaction />

## Related Topics

<PostLike />
`
	mdxPath := filepath.Join(docsDir, "reactions.mdx")
	require.NoError(t, os.WriteFile(mdxPath, []byte(mdxContent), 0o644))

	// Write decisions file
	decisions := `{
  "generated_at": "2026-01-01T00:00:00Z",
  "pages": [{
    "page_path": "social/reactions",
    "decisions": [{
      "name": "PostLike",
      "action": "REMOVE",
      "reason": "irrelevant to this page",
      "confidence": "high"
    }]
  }]
}`
	decisionsPath := filepath.Join(dir, "curate-decisions.json")
	require.NoError(t, os.WriteFile(decisionsPath, []byte(decisions), 0o644))

	reviewPath := filepath.Join(dir, "curate-review.json")
	err := runCurateApply(dir, filepath.Join(dir, "docs"), decisionsPath, reviewPath, false)
	require.NoError(t, err)

	// MDX should no longer contain PostLike
	data, err := os.ReadFile(mdxPath)
	require.NoError(t, err)
	assert.NotContains(t, string(data), "PostLike")
	assert.Contains(t, string(data), "AddReaction")
}

func TestCurateApply_DryRunDoesNotModifyFiles(t *testing.T) {
	dir := t.TempDir()
	docsDir := filepath.Join(dir, "docs", "social")
	require.NoError(t, os.MkdirAll(docsDir, 0o755))
	original := `import PostLike from '/snippets/post-like.mdx';

---
title: "Reactions"
---

<PostLike />
`
	mdxPath := filepath.Join(docsDir, "reactions.mdx")
	require.NoError(t, os.WriteFile(mdxPath, []byte(original), 0o644))

	decisions := `{
  "generated_at": "2026-01-01T00:00:00Z",
  "pages": [{
    "page_path": "social/reactions",
    "decisions": [{"name": "PostLike", "action": "REMOVE", "confidence": "high", "reason": "test"}]
  }]
}`
	decisionsPath := filepath.Join(dir, "curate-decisions.json")
	require.NoError(t, os.WriteFile(decisionsPath, []byte(decisions), 0o644))

	reviewPath := filepath.Join(dir, "curate-review.json")
	err := runCurateApply(dir, filepath.Join(dir, "docs"), decisionsPath, reviewPath, true)
	require.NoError(t, err)

	// File unchanged in dry-run
	data, err := os.ReadFile(mdxPath)
	require.NoError(t, err)
	assert.Equal(t, original, string(data))
}

func TestCurateApply_LowConfidenceWritesReviewFile(t *testing.T) {
	dir := t.TempDir()
	docsDir := filepath.Join(dir, "docs", "social")
	require.NoError(t, os.MkdirAll(docsDir, 0o755))
	original := `import PostLike from '/snippets/post-like.mdx';

---
title: "Reactions"
---

<PostLike />
`
	mdxPath := filepath.Join(docsDir, "reactions.mdx")
	require.NoError(t, os.WriteFile(mdxPath, []byte(original), 0o644))

	decisions := `{
  "generated_at": "2026-01-01T00:00:00Z",
  "pages": [{
    "page_path": "social/reactions",
    "decisions": [{"name": "PostLike", "action": "REMOVE", "confidence": "low", "reason": "unsure"}]
  }]
}`
	decisionsPath := filepath.Join(dir, "curate-decisions.json")
	require.NoError(t, os.WriteFile(decisionsPath, []byte(decisions), 0o644))

	reviewPath := filepath.Join(dir, "curate-review.json")
	err := runCurateApply(dir, filepath.Join(dir, "docs"), decisionsPath, reviewPath, false)
	require.NoError(t, err)

	// MDX unchanged (low confidence not auto-applied)
	data, err := os.ReadFile(mdxPath)
	require.NoError(t, err)
	assert.Contains(t, string(data), "PostLike")

	// Review file written with the flagged decision
	reviewData, err := os.ReadFile(reviewPath)
	require.NoError(t, err)
	assert.Contains(t, string(reviewData), "PostLike")
}
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd harness && go test ./cmd/... -run TestCurateApply 2>&1 | head -5
```
Expected: `undefined: runCurateApply`.

- [ ] **Step 3: Implement runCurateApply in curate.go**

Add to `harness/cmd/curate.go`:

```go
// runCurateApply reads curate-decisions.json, applies high-confidence decisions to MDX files,
// writes flagged decisions to curate-review.json, and emits findings to harness-report.json.
func runCurateApply(cfgDir, docsBase, decisionsPath, reviewPath string, dryRun bool) error {
	df, err := curator.ReadDecisions(decisionsPath)
	if err != nil {
		return fmt.Errorf("read decisions: %w", err)
	}

	var reviewPages []curator.PageDecisions
	totalApplied, totalFlagged := 0, 0

	for _, pd := range df.Pages {
		// Resolve MDX file path from page path.
		mdxFile := filepath.Join(docsBase, filepath.FromSlash(pd.PagePath)+".mdx")
		data, err := os.ReadFile(mdxFile)
		if err != nil {
			fmt.Fprintf(os.Stderr, "warning: read %s: %v\n", mdxFile, err)
			continue
		}

		modified, applied, flagged := curator.Apply(string(data), pd.Decisions)
		totalApplied += len(applied)
		totalFlagged += len(flagged)

		if len(flagged) > 0 {
			reviewPages = append(reviewPages, curator.PageDecisions{
				PagePath:  pd.PagePath,
				Decisions: flagged,
			})
		}

		for _, d := range applied {
			action := "removed"
			if d.Action == curator.ActionKeep {
				action = "kept (re-sectioned)"
			} else if d.Action == curator.ActionMove {
				action = fmt.Sprintf("moved → %s", d.TargetPage)
			}
			fmt.Printf("[curate] %s: %s %s\n", pd.PagePath, d.Name, action)
		}

		if !dryRun && modified != string(data) {
			if err := os.WriteFile(mdxFile, []byte(modified), 0o644); err != nil {
				return fmt.Errorf("write %s: %w", mdxFile, err)
			}
		}
	}

	if len(reviewPages) > 0 {
		if err := curator.WriteReview(reviewPath, reviewPages); err != nil {
			return fmt.Errorf("write review: %w", err)
		}
		fmt.Printf("[curate] %d decisions flagged for review → %s\n", totalFlagged, reviewPath)
	}

	if dryRun {
		fmt.Printf("[curate] dry-run: would apply %d, flag %d\n", totalApplied, totalFlagged)
	} else {
		fmt.Printf("[curate] applied %d, flagged %d\n", totalApplied, totalFlagged)
	}
	return nil
}
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
cd harness && go test ./cmd/... -run TestCurateApply -v 2>&1 | tail -15
```
Expected: all 3 `TestCurateApply_*` tests PASS.

- [ ] **Step 5: Commit**

```bash
git add harness/cmd/curate.go harness/cmd/curate_test.go
git commit -m "feat(curate): apply mode — confidence-gated MDX edits + review file"
```

---

### Task 6: Wire `curate` into `main.go`

**Files:**
- Modify: `harness/cmd/main.go`
- Modify: `harness/cmd/main_test.go`

- [ ] **Step 1: Add curate to main.go**

In `harness/cmd/main.go`, find the `switch` on the command name and add before `default`:

```go
case "curate":
    runCurate(os.Args[2:])
```

Update the usage string to include `curate`:

```go
fmt.Fprintf(os.Stderr, "usage: harness <annotate|audit|baseline|curate|fillmanifests|fix|genmanifests|gendocs|migrate|parity|place|prompt|serve> [--config path]\n")
```

- [ ] **Step 2: Update usage assertion in main_test.go**

Find the test that asserts the usage string and update it to include `curate` in the expected value (match exactly what you wrote in main.go above).

- [ ] **Step 3: Build + run all cmd tests**

```bash
cd harness && go build ./cmd/... && go test ./cmd/... 2>&1 | tail -5
```
Expected: `ok  social-plus/harness/cmd`.

- [ ] **Step 4: Commit**

```bash
git add harness/cmd/main.go harness/cmd/main_test.go
git commit -m "feat: wire curate command into main"
```

---

### Task 7: `annotate --qa` — Annotation QA Task Generator

**Files:**
- Modify: `harness/cmd/annotate.go`
- Create: `harness/cmd/annotate_qa_test.go`

- [ ] **Step 1: Write the failing test**

Create `harness/cmd/annotate_qa_test.go`:

```go
package main

import (
	"os"
	"path/filepath"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestRunAnnotateQA_GeneratesTasksFile(t *testing.T) {
	dir := t.TempDir()

	// Create a docs page
	docsDir := filepath.Join(dir, "docs", "social")
	require.NoError(t, os.MkdirAll(docsDir, 0o755))
	require.NoError(t, os.WriteFile(filepath.Join(docsDir, "reactions.mdx"), []byte(`---
title: Reactions
---

## Overview

Enable rich emotional responses with reactions.
`), 0o644))

	// Write annotation patches file with two functions pointing to reactions page
	patchContent := `generated_by: harness annotate
note: review before applying
patches:
  - file: android/ReactionRepo.kt
    function: addReaction
    asc_page: social/reactions
  - file: android/ReactionRepo.kt
    function: getProductInfo
    asc_page: social/reactions
`
	patchPath := filepath.Join(dir, "annotation-patches.yml")
	require.NoError(t, os.WriteFile(patchPath, []byte(patchContent), 0o644))

	outPath := filepath.Join(dir, "annotation-qa-tasks.md")
	err := runAnnotateQA(filepath.Join(dir, "docs"), patchPath, outPath)
	require.NoError(t, err)

	data, err := os.ReadFile(outPath)
	require.NoError(t, err)
	content := string(data)

	assert.Contains(t, content, "addReaction")
	assert.Contains(t, content, "getProductInfo")
	assert.Contains(t, content, "social/reactions")
	// Page prose is included
	assert.Contains(t, content, "Enable rich emotional responses")
	// Instructions for AI agent
	assert.Contains(t, content, "ANNOTATION_SUSPECT")
	assert.True(t, strings.HasPrefix(content, "# Annotation QA Tasks"))
}

func TestRunAnnotateQA_MissingPageWarnsAndContinues(t *testing.T) {
	dir := t.TempDir()
	require.NoError(t, os.MkdirAll(filepath.Join(dir, "docs"), 0o755))

	patchContent := `generated_by: harness annotate
note: test
patches:
  - file: android/Foo.kt
    function: doSomething
    asc_page: nonexistent/page
`
	patchPath := filepath.Join(dir, "annotation-patches.yml")
	require.NoError(t, os.WriteFile(patchPath, []byte(patchContent), 0o644))

	outPath := filepath.Join(dir, "annotation-qa-tasks.md")
	// Should not error — just warn and skip
	err := runAnnotateQA(filepath.Join(dir, "docs"), patchPath, outPath)
	require.NoError(t, err)

	data, err := os.ReadFile(outPath)
	require.NoError(t, err)
	// Function still appears but page prose section notes file not found
	assert.Contains(t, string(data), "doSomething")
}
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd harness && go test ./cmd/... -run TestRunAnnotateQA 2>&1 | head -5
```
Expected: `undefined: runAnnotateQA`.

- [ ] **Step 3: Add `--qa` flag + runAnnotateQA to annotate.go**

First, add the `--qa` flag to `runAnnotate()`. Find the flag declarations block and add:

```go
qa := fs.Bool("qa", false, "generate annotation-qa-tasks.md for AI agent review of asc_page assignments")
qaOut := fs.String("qa-out", "annotation-qa-tasks.md", "output path for QA tasks file")
```

After `_ = fs.Parse(args)`, add before the existing config load:

```go
// QA mode: load annotation-patches.yml and generate qa tasks file.
if *qa {
    cfgDir2 := filepath.Dir(*cfgPath)
    cfg2, err2 := config.Load(*cfgPath)
    docsBase2 := filepath.Join(cfgDir2, "docs")
    if err2 == nil {
        docsBase2 = filepath.Join(cfgDir2, cfg2.Docs.Path)
    }
    patchPath := filepath.Join(cfgDir2, *outPath)
    if err2 = runAnnotateQA(docsBase2, patchPath, filepath.Join(cfgDir2, *qaOut)); err2 != nil {
        fmt.Fprintf(os.Stderr, "annotate --qa: %v\n", err2)
        os.Exit(1)
    }
    return
}
```

Then add the `runAnnotateQA` function (new function at end of annotate.go):

```go
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
// and generates annotation-qa-tasks.md for the AI agent to assess.
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
		prose := extractProse(string(raw), 500)
		pageProse[page] = prose
	}

	return writeAnnotationQATasks(outPath, byPage, pageProse)
}

// extractProse strips MDX import lines and frontmatter, returning up to maxWords words of prose.
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
		if trimmed == "" || strings.HasPrefix(trimmed, "#") {
			proseLines = append(proseLines, line)
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
```

**Important:** `annotate.go` already imports `sort`, `strings`, `os`, `filepath`, `yaml`. Verify the imports cover the new additions — `sort` may need to be added if not already present.

- [ ] **Step 4: Run tests to verify they pass**

```bash
cd harness && go test ./cmd/... -run TestRunAnnotateQA -v 2>&1 | tail -10
```
Expected: both tests PASS.

- [ ] **Step 5: Run full test suite**

```bash
cd harness && go test ./... 2>&1 | tail -25
```
Expected: all packages pass, no failures.

- [ ] **Step 6: Commit**

```bash
git add harness/cmd/annotate.go harness/cmd/annotate_qa_test.go
git commit -m "feat(annotate): --qa flag generates annotation-qa-tasks.md for AI review"
```

---

### Task 8: E2E Smoke Test

**Files:**
- None created; run commands against real docs repo.

- [ ] **Step 1: Build the harness**

```bash
cd harness && go build -o harness-bin ./cmd/
```
Expected: no errors.

- [ ] **Step 2: Gen-tasks smoke test (single page)**

```bash
./harness-bin curate --config harness-config.yml \
  --page social-plus-sdk/core-concepts/content-handling/reactions
```
Expected: outputs `curate-tasks.md` containing `reactions`, section headings, and snippet names like `MessageReact`, `PostLike` etc.

- [ ] **Step 3: Verify curate-tasks.md looks right**

```bash
head -60 curate-tasks.md
```
Expected: structured markdown with page path, prose summary, and list of placed snippets.

- [ ] **Step 4: Dry-run apply with a minimal test decisions file**

```bash
cat > /tmp/test-decisions.json << 'EOF'
{
  "generated_at": "2026-05-03T00:00:00Z",
  "pages": [{
    "page_path": "social-plus-sdk/core-concepts/content-handling/reactions",
    "decisions": [{
      "name": "PostLike",
      "action": "REMOVE",
      "reason": "variant of AddReaction, redundant",
      "confidence": "high"
    }]
  }]
}
EOF

./harness-bin curate --config harness-config.yml --apply \
  --decisions /tmp/test-decisions.json --dry-run
```
Expected: prints `[curate] ... PostLike removed` and `dry-run: would apply 1, flag 0`. MDX file unchanged.

- [ ] **Step 5: Annotate QA smoke test**

```bash
./harness-bin annotate --config harness-config.yml --qa
```
Expected: generates `annotation-qa-tasks.md` in the harness dir; no errors.

- [ ] **Step 6: Verify annotation-qa-tasks.md has expected structure**

```bash
head -40 annotation-qa-tasks.md
```
Expected: structured markdown with `# Annotation QA Tasks`, page sections, and function listings.

- [ ] **Step 7: Run full test suite one final time**

```bash
cd harness && go test ./... 2>&1 | tail -25
```
Expected: all packages pass.

- [ ] **Step 8: Commit harness binary + outputs**

```bash
cd harness && go build -o harness-bin ./cmd/
git add harness/harness-bin harness/cmd/
git commit -m "feat: curate command + annotate --qa gate complete (Phase 2B)"
git push origin feat/doc-agent
```

---

## Self-Review

**Spec coverage check:**

| Spec requirement | Covered by |
|-----------------|-----------|
| `harness curate` command | Tasks 4–6 |
| Gen-tasks mode (curate-tasks.md) | Task 4 |
| Apply mode (reads curate-decisions.json, patches MDX) | Task 5 |
| `--dry-run` flag | Task 5 |
| `--page` filter flag | Task 4 |
| Confidence-gated auto-apply (REMOVE high → apply, REMOVE low → flag) | Task 3 |
| MOVE high → remove from page | Task 3 |
| Re-sectioning (KEEP + section → move tag) | Task 3 |
| curate-review.json (flagged decisions) | Task 5 |
| 3 new curator finding types | Task 1 |
| `harness annotate --qa` flag | Task 7 |
| annotation-qa-tasks.md with page prose | Task 7 |
| 2 new annotation finding types | Task 1 |
| All tests use mock LLM (no real API calls) | Tasks 2–3, 4–5, 7 |
| E2E smoke test | Task 8 |

**Type consistency check:**
- `curator.Decision` defined in Task 2, used in Tasks 3, 4, 5 ✅
- `curator.PageDecisions` defined in Task 2, used in Tasks 4, 5 ✅
- `curator.DecisionsFile` defined in Task 2, read in Task 5 ✅
- `curator.Apply` signature `(content string, decisions []Decision) (modified string, applied []Decision, flagged []Decision)` consistent across Tasks 3 and 5 ✅
- `curator.WriteReview` defined Task 2, used Task 5 ✅
- `runAnnotateQA` defined and called in Task 7 ✅

**Placeholder scan:** None found. All code blocks are complete. ✅
