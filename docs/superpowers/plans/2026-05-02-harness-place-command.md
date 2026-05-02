# `harness place` Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a `harness place` command that scans MDX pages for unplaced snippet imports and emits a `placement-tasks.json` file; Copilot CLI agents then read each task and insert `<ComponentName />` tags at the correct section.

**Architecture:** The harness binary stays LLM-free — `place` does a pure computational scan (find orphaned imports, resolve snippet previews, emit JSON tasks). Agent-driven placement runs outside the binary. The `internal/placer` package provides pure functions that are fully unit-testable. `cmd/place.go` wires config → placer → JSON output, following the same pattern as `parity.go`.

**Tech Stack:** Go 1.23, `encoding/json`, `path/filepath`, `strings`, `testify` (existing), harness `config` package (existing).

---

## File Map

| Action | Path | Responsibility |
|--------|------|----------------|
| Create | `internal/placer/placer.go` | Scan MDX for unplaced imports; resolve snippet preview; build task list |
| Create | `internal/placer/placer_test.go` | Unit tests for all placer functions |
| Create | `cmd/place.go` | CLI entry point: flags, config, call placer, write JSON |
| Modify | `cmd/main.go` | Register `"place"` case |

---

## Task 1: `internal/placer` package — core types and import scanner

**Files:**
- Create: `internal/placer/placer.go`

- [ ] **Step 1: Create `internal/placer/placer.go` with types and `FindUnplaced`**

```go
package placer

import (
	"os"
	"path/filepath"
	"regexp"
	"strings"
)

// Component is one unplaced import found in an MDX page.
type Component struct {
	Name        string `json:"name"`         // e.g. "MessageFlag"
	Key         string `json:"key"`          // e.g. "message-flag"
	ImportPath  string `json:"import_path"`  // e.g. "/snippets/social-plus-sdk/chat/message-flag.mdx"
	SnippetPreview string `json:"snippet_preview"` // first 40 lines of snippet MDX
}

// PageTask is the placement job for one MDX page.
type PageTask struct {
	PageFile   string      `json:"page_file"`   // absolute path to the MDX file
	PagePath   string      `json:"page_path"`   // docs.json-relative path (no .mdx)
	Components []Component `json:"components"`  // unplaced components, in import order
}

var importRe = regexp.MustCompile(`(?m)^import\s+(\w+)\s+from\s+'(/snippets/[^']+\.mdx)'\s*;`)

// FindUnplaced scans mdxFile and returns all imported snippet components whose
// <Name> tag is absent from the file body. docsBase is the absolute path to the
// docs root (used to resolve snippet preview files from their /snippets/... paths).
// pageRelPath is the docs.json-relative page path (no extension).
func FindUnplaced(mdxFile, pageRelPath, docsBase string) (PageTask, error) {
	data, err := os.ReadFile(mdxFile)
	if err != nil {
		return PageTask{}, err
	}
	content := string(data)

	var components []Component
	for _, m := range importRe.FindAllStringSubmatch(content, -1) {
		name, importPath := m[1], m[2]
		// Check body: strip all import lines, then look for <Name
		body := importRe.ReplaceAllString(content, "")
		if strings.Contains(body, "<"+name) {
			continue // already placed
		}
		preview := resolveSnippetPreview(importPath, docsBase)
		components = append(components, Component{
			Name:           name,
			Key:            importPathToKey(importPath),
			ImportPath:     importPath,
			SnippetPreview: preview,
		})
	}

	return PageTask{
		PageFile:   mdxFile,
		PagePath:   pageRelPath,
		Components: components,
	}, nil
}

// importPathToKey converts "/snippets/social-plus-sdk/chat/message-flag.mdx"
// → "message-flag" (the base filename without extension).
func importPathToKey(importPath string) string {
	base := filepath.Base(importPath)
	return strings.TrimSuffix(base, ".mdx")
}

// resolveSnippetPreview resolves a Mintlify-relative import path like
// "/snippets/social-plus-sdk/chat/message-flag.mdx" to an absolute path
// under docsBase/snippets/... and returns the first 40 lines of that file.
// Returns empty string if the file cannot be read.
func resolveSnippetPreview(importPath, docsBase string) string {
	// Strip leading "/" then join with docsBase
	rel := strings.TrimPrefix(importPath, "/")
	absPath := filepath.Join(docsBase, filepath.FromSlash(rel))
	data, err := os.ReadFile(absPath)
	if err != nil {
		return ""
	}
	lines := strings.Split(string(data), "\n")
	if len(lines) > 40 {
		lines = lines[:40]
	}
	return strings.Join(lines, "\n")
}
```

---

## Task 2: Unit tests for `FindUnplaced`

**Files:**
- Create: `internal/placer/placer_test.go`

- [ ] **Step 1: Write failing tests**

```go
package placer_test

import (
	"os"
	"path/filepath"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"social-plus/harness/internal/placer"
)

func setupDocs(t *testing.T) (docsBase, mdxFile string) {
	t.Helper()
	dir := t.TempDir()
	docsBase = dir

	// Create a snippet file
	snippetDir := filepath.Join(dir, "snippets", "social-plus-sdk", "chat")
	require.NoError(t, os.MkdirAll(snippetDir, 0o755))
	snippetContent := "<CodeGroup>\n```kotlin Android\nfun messageFlag() {}\n```\n</CodeGroup>"
	require.NoError(t, os.WriteFile(filepath.Join(snippetDir, "message-flag.mdx"), []byte(snippetContent), 0o644))

	// Create a page with one unplaced import
	mdxContent := "import MessageFlag from '/snippets/social-plus-sdk/chat/message-flag.mdx';\n\n---\ntitle: Test\n---\n\n## Flag Messages\n\nSome prose.\n"
	mdxFile = filepath.Join(dir, "flag-page.mdx")
	require.NoError(t, os.WriteFile(mdxFile, []byte(mdxContent), 0o644))
	return
}

func TestFindUnplaced_DetectsOrphanedImport(t *testing.T) {
	docsBase, mdxFile := setupDocs(t)
	task, err := placer.FindUnplaced(mdxFile, "social-plus-sdk/chat/flag-messages", docsBase)
	require.NoError(t, err)
	require.Len(t, task.Components, 1)
	assert.Equal(t, "MessageFlag", task.Components[0].Name)
	assert.Equal(t, "message-flag", task.Components[0].Key)
	assert.Equal(t, "/snippets/social-plus-sdk/chat/message-flag.mdx", task.Components[0].ImportPath)
	assert.Contains(t, task.Components[0].SnippetPreview, "CodeGroup")
}

func TestFindUnplaced_SkipsAlreadyPlaced(t *testing.T) {
	docsBase, _ := setupDocs(t)
	// Page has the import AND the tag in body
	content := "import MessageFlag from '/snippets/social-plus-sdk/chat/message-flag.mdx';\n\n---\ntitle: Test\n---\n\n<MessageFlag />\n"
	mdxFile := filepath.Join(docsBase, "already-placed.mdx")
	require.NoError(t, os.WriteFile(mdxFile, []byte(content), 0o644))

	task, err := placer.FindUnplaced(mdxFile, "social-plus-sdk/chat/already-placed", docsBase)
	require.NoError(t, err)
	assert.Empty(t, task.Components)
}

func TestFindUnplaced_MultipleComponents(t *testing.T) {
	dir := t.TempDir()
	snippetDir := filepath.Join(dir, "snippets", "social-plus-sdk", "chat")
	require.NoError(t, os.MkdirAll(snippetDir, 0o755))
	require.NoError(t, os.WriteFile(filepath.Join(snippetDir, "message-flag.mdx"), []byte("preview1"), 0o644))
	require.NoError(t, os.WriteFile(filepath.Join(snippetDir, "message-unflag.mdx"), []byte("preview2"), 0o644))

	content := "import MessageFlag from '/snippets/social-plus-sdk/chat/message-flag.mdx';\nimport MessageUnflag from '/snippets/social-plus-sdk/chat/message-unflag.mdx';\n\n---\ntitle: Test\n---\n\n## Flag\n"
	mdxFile := filepath.Join(dir, "flag.mdx")
	require.NoError(t, os.WriteFile(mdxFile, []byte(content), 0o644))

	task, err := placer.FindUnplaced(mdxFile, "social-plus-sdk/chat/flag", dir)
	require.NoError(t, err)
	assert.Len(t, task.Components, 2)
	names := []string{task.Components[0].Name, task.Components[1].Name}
	assert.Contains(t, names, "MessageFlag")
	assert.Contains(t, names, "MessageUnflag")
}

func TestFindUnplaced_MissingSnippetFileGivesEmptyPreview(t *testing.T) {
	dir := t.TempDir()
	content := "import MessageFlag from '/snippets/social-plus-sdk/chat/message-flag.mdx';\n\n---\ntitle: Test\n---\n\n## Flag\n"
	mdxFile := filepath.Join(dir, "flag.mdx")
	require.NoError(t, os.WriteFile(mdxFile, []byte(content), 0o644))

	task, err := placer.FindUnplaced(mdxFile, "social-plus-sdk/chat/flag", dir)
	require.NoError(t, err)
	require.Len(t, task.Components, 1)
	assert.Equal(t, "", task.Components[0].SnippetPreview) // missing file → empty preview
}

func TestFindUnplaced_SnippetPreviewTruncatedAt40Lines(t *testing.T) {
	dir := t.TempDir()
	snippetDir := filepath.Join(dir, "snippets", "s", "c")
	require.NoError(t, os.MkdirAll(snippetDir, 0o755))
	// Write 60-line snippet
	var lines []string
	for i := 0; i < 60; i++ {
		lines = append(lines, "line")
	}
	require.NoError(t, os.WriteFile(filepath.Join(snippetDir, "big.mdx"), []byte(strings.Join(lines, "\n")), 0o644))

	content := "import Big from '/snippets/s/c/big.mdx';\n\n## Section\n"
	mdxFile := filepath.Join(dir, "page.mdx")
	require.NoError(t, os.WriteFile(mdxFile, []byte(content), 0o644))

	task, err := placer.FindUnplaced(mdxFile, "s/c/page", dir)
	require.NoError(t, err)
	require.Len(t, task.Components, 1)
	got := strings.Count(task.Components[0].SnippetPreview, "\n")
	assert.Equal(t, 39, got) // 40 lines = 39 newlines
}
```

Note: add `"strings"` to the import block in the test file.

- [ ] **Step 2: Run tests — confirm they all fail**

```bash
cd /Users/admin/Documents/GitHub/sp-ai-agent/sp/social-plus-docs/harness
go test ./internal/placer/... -v 2>&1 | head -20
```
Expected: `FAIL` — package doesn't exist yet.

- [ ] **Step 3: Create `internal/placer/placer.go`** (code in Task 1 Step 1 above)

- [ ] **Step 4: Run tests — confirm they all pass**

```bash
go test ./internal/placer/... -v
```
Expected: all 5 tests `PASS`.

- [ ] **Step 5: Commit**

```bash
git add internal/placer/
git commit -m "feat(harness): add placer package — FindUnplaced for orphaned imports"
```

---

## Task 3: `cmd/place.go` — CLI entry point

**Files:**
- Create: `cmd/place.go`

- [ ] **Step 1: Create `cmd/place.go`**

```go
package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"social-plus/harness/internal/config"
	"social-plus/harness/internal/placer"
	"social-plus/harness/internal/runstate"
)

func runPlace(args []string) {
	fs := flag.NewFlagSet("place", flag.ExitOnError)
	cfgPath := fs.String("config", "harness-config.yml", "path to harness-config.yml")
	outPath := fs.String("out", "placement-tasks.json", "output task file path")
	dryRun := fs.Bool("dry-run", false, "print summary without writing task file")
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
	_ = runstate.Start(cfgDir, "place", "script", "")

	docsBase := filepath.Join(cfgDir, cfg.Docs.Path)

	var tasks []placer.PageTask

	_ = filepath.WalkDir(docsBase, func(path string, d os.DirEntry, walkErr error) error {
		if walkErr != nil {
			return walkErr
		}
		if d.IsDir() {
			rel, _ := filepath.Rel(docsBase, path)
			relSlash := filepath.ToSlash(rel)
			// Skip harness/ and essentials/ (non-SDK docs)
			if rel == "harness" || strings.HasPrefix(relSlash+"/", "harness/") ||
				rel == "essentials" || strings.HasPrefix(relSlash+"/", "essentials/") ||
				rel == "snippets" || strings.HasPrefix(relSlash+"/", "snippets/") {
				return filepath.SkipDir
			}
			return nil
		}
		if !strings.HasSuffix(path, ".mdx") {
			return nil
		}
		rel, _ := filepath.Rel(docsBase, path)
		relSlash := filepath.ToSlash(rel)
		// Apply scope filter
		if cfg.Docs.Scope != "" && !strings.HasPrefix(relSlash, cfg.Docs.Scope+"/") {
			return nil
		}
		pagePath := strings.TrimSuffix(relSlash, ".mdx")

		task, err := placer.FindUnplaced(path, pagePath, docsBase)
		if err != nil {
			fmt.Fprintf(os.Stderr, "[place] warning: %s: %v\n", rel, err)
			return nil
		}
		if len(task.Components) > 0 {
			tasks = append(tasks, task)
		}
		return nil
	})

	totalComponents := 0
	for _, t := range tasks {
		totalComponents += len(t.Components)
	}

	if *dryRun {
		fmt.Printf("[place] DRY RUN: %d pages, %d unplaced components — no file written\n",
			len(tasks), totalComponents)
		_ = runstate.Finish(cfgDir, "place", fmt.Sprintf("dry-run: %d pages", len(tasks)))
		return
	}

	dest := filepath.Join(cfgDir, *outPath)
	data, err := json.MarshalIndent(tasks, "", "  ")
	if err != nil {
		fmt.Fprintf(os.Stderr, "marshal tasks: %v\n", err)
		_ = runstate.Fail(cfgDir, "place", "marshal error")
		os.Exit(1)
	}
	if err := os.WriteFile(dest, data, 0o644); err != nil {
		fmt.Fprintf(os.Stderr, "write %s: %v\n", dest, err)
		_ = runstate.Fail(cfgDir, "place", "write error")
		os.Exit(1)
	}

	_ = runstate.Finish(cfgDir, "place", fmt.Sprintf("%d pages, %d components", len(tasks), totalComponents))
	fmt.Printf("[place] %d pages with unplaced components → %s\n", len(tasks), dest)
	fmt.Printf("[place] %d total components to place\n", totalComponents)
	fmt.Printf("[place] dispatch Copilot CLI agents to execute placements\n")
}
```

- [ ] **Step 2: Register `place` in `cmd/main.go`**

Edit the `switch` block and usage line:

```go
// usage line (line 9):
fmt.Fprintf(os.Stderr, "usage: harness <annotate|audit|fillmanifests|fix|genmanifests|gendocs|migrate|parity|place|prompt|serve> [--config path]\n")

// add case after "parity":
case "place":
    runPlace(os.Args[2:])
```

- [ ] **Step 3: Build to confirm it compiles**

```bash
cd /Users/admin/Documents/GitHub/sp-ai-agent/sp/social-plus-docs/harness
go build -o harness-bin ./cmd/ && echo "OK"
```
Expected: `OK` with no errors.

- [ ] **Step 4: Smoke-test with dry-run**

```bash
./harness-bin place --dry-run
```
Expected output like:
```
[place] DRY RUN: 118 pages, NNN unplaced components — no file written
```

- [ ] **Step 5: Run the full test suite to confirm no regressions**

```bash
go test ./... 2>&1 | tail -20
```
Expected: all packages `ok`, no failures.

- [ ] **Step 6: Commit**

```bash
git add cmd/place.go cmd/main.go
git commit -m "feat(harness): add place command — emits placement-tasks.json for agent execution"
```

---

## Task 4: Generate `placement-tasks.json` and dispatch agents

- [ ] **Step 1: Run `harness place` to generate the task file**

```bash
cd /Users/admin/Documents/GitHub/sp-ai-agent/sp/social-plus-docs/harness
./harness-bin place
```
Expected:
```
[place] 118 pages with unplaced components → .../placement-tasks.json
[place] NNN total components to place
[place] dispatch Copilot CLI agents to execute placements
```

- [ ] **Step 2: Inspect the task file**

```bash
python3 -c "
import json
with open('placement-tasks.json') as f:
    tasks = json.load(f)
print(f'Tasks: {len(tasks)}')
total = sum(len(t[\"components\"]) for t in tasks)
print(f'Total components: {total}')
print('Sample task:')
import json as j; print(j.dumps(tasks[0], indent=2)[:500])
"
```
Expected: valid JSON array, each entry has `page_file`, `page_path`, `components` array.

- [ ] **Step 3: Dispatch agents (one per page task) to perform placement**

Each agent receives its task JSON and must:
1. Read the full MDX page at `page_file`
2. For each component in `components`:
   - Find the best matching `## ` or `### ` heading (by key/name semantics)
   - If the matched section contains `<CodeGroup>...</CodeGroup>` → replace entire block with `<ComponentName />`
   - Otherwise → insert `<ComponentName />` (with blank lines before+after) before the next heading or at end of section
   - If no heading match → collect for fallback `## Code Examples` section (append before `## Best Practices`, `## Related`, `## Advanced`, or EOF)
3. Write the updated file
4. Constraints: blank lines around every tag; match indentation of surrounding block (4 spaces inside `<Tab>`/`<Accordion>`/`<Step>`); never inside fenced code or frontmatter; self-closing `<ComponentName />` only

- [ ] **Step 4: Post-placement audit — verify no Mintlify syntax errors**

```bash
cd /Users/admin/Documents/GitHub/sp-ai-agent/sp/social-plus-docs/harness
./harness-bin audit 2>&1 | grep -E "Mintlify|syntax|STALE|Summary"
```
Expected: `Mintlify: no syntax errors` and zero new `DOC_PAGE_STALE_IMPORT` findings.

- [ ] **Step 5: Verify placement coverage**

```bash
python3 << 'EOF'
import os, re
from pathlib import Path

docs = Path('/Users/admin/Documents/GitHub/sp-ai-agent/sp/social-plus-docs/social-plus-sdk')
import_re = re.compile(r'^import\s+(\w+)\s+from\s+', re.MULTILINE)

orphaned = 0
for mdx in docs.rglob('*.mdx'):
    content = mdx.read_text()
    imports = import_re.findall(content)
    body = import_re.sub('', content)
    for name in imports:
        if '<' + name not in body:
            orphaned += 1

print(f'Remaining orphaned imports: {orphaned}')
print('Target: 0')
EOF
```
Expected: `Remaining orphaned imports: 0`

- [ ] **Step 6: Commit all MDX changes**

```bash
cd /Users/admin/Documents/GitHub/sp-ai-agent/sp/social-plus-docs
git add social-plus-sdk/
git commit -m "feat(docs): place snippet components on all MDX pages via harness place + agents

- All <ComponentName /> tags placed in relevant page sections
- CodeGroup blocks replaced where present
- Fallback ## Code Examples sections added for unmatched components
- 0 Mintlify syntax errors post-placement"
```

---

## Self-Review

**Spec coverage:**
- ✅ `harness place` command (computational scan → JSON tasks): Tasks 1–3
- ✅ Flags: `-config`, `-out`, `-dry-run`: Task 3
- ✅ Unplaced import detection: Tasks 1–2
- ✅ Snippet preview (first 40 lines, empty if missing): Tasks 1–2
- ✅ JSON output structure (page_file, page_path, components[name/key/import_path/snippet_preview]): Task 1
- ✅ Register in main.go: Task 3
- ✅ Agent placement with heading match, CodeGroup replace, fallback section: Task 4
- ✅ Mintlify safety (blank lines, indentation, self-closing, no code/frontmatter): Task 4
- ✅ Post-placement audit validation: Task 4
- ✅ Idempotent (re-running only emits still-unplaced): covered by `FindUnplaced` logic (skips already-placed)

**Placeholder scan:** None found.

**Type consistency:** `PageTask`, `Component` defined in Task 1, used identically in Tasks 3–4. `placer.FindUnplaced` signature consistent throughout.
