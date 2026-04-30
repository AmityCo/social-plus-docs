# Manifest Fill-In, Migration & Validation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fill the 123 skeleton manifests with GendocsKeys (computationally where possible, with AI-assisted tasks for the rest), then run the full migration pipeline with post-migration import validation.

**Architecture:** A new `fillmanifests` command scans all 4 SDK repos and auto-assigns GendocsKeys to manifest sections using keyword matching (section slug ↔ key words). Sections it can't resolve are surfaced as `MANIFEST_FILL` tasks in `harness-tasks.md`. After manifests are filled, `audit` produces real `MISSING_SNIPPET` findings. `prompt` emits tasks for an AI agent to write the missing SDK snippets. `migrate` then injects imports + replaces CodeGroups. A new `DOC_BROKEN_IMPORT` audit check verifies every import path resolves to an existing file.

**Tech Stack:** Go 1.22, `gopkg.in/yaml.v3`, existing harness packages (`scanner`, `docgen`, `manifest`, `differ`, `report`). All commands run from `social-plus-docs/harness/`.

---

## File Map

| Action | Path | Purpose |
|---|---|---|
| Create | `internal/manifest/filler.go` | `FillFromSnippets` — keyword-match assignment; `SaveManifest` — write back |
| Create | `internal/manifest/filler_test.go` | Tests: single-section, keyword match, no match, skip existing, empty |
| Create | `cmd/fillmanifests.go` | CLI: scan SDKs → build page→keys map → auto-fill manifests |
| Modify | `cmd/main.go` | Add `fillmanifests` case |
| Modify | `cmd/main_test.go` | Update usage string assertion |
| Modify | `cmd/prompt.go` | Add `MANIFEST_FILL` section: walk empty manifest sections, list candidate keys |
| Modify | `internal/differ/differ.go` | Add `DiffDocImports` → `DOC_BROKEN_IMPORT` findings |
| Modify | `internal/differ/differ_test.go` | Tests for import path resolution |
| Modify | `cmd/audit.go` | Wire `DiffDocImports` for post-migration broken-import detection |
| Modify | `harness/docs/BIG-PICTURE.md` | Update current state table |

---

## Task 1: `internal/manifest/filler.go` — FillFromSnippets + SaveManifest

**Files:**
- Create: `internal/manifest/filler.go`
- Create: `internal/manifest/filler_test.go`

**Background:** `FillFromSnippets` takes a `*Manifest` and a list of GendocsKey candidates. For each candidate not already in any section it tries:
1. If the manifest has exactly **one** section → assign to it.
2. Otherwise → score each section slug by counting how many hyphen-words from the key appear in the slug; assign to the highest-scoring section if score > 0.
3. If no section scores > 0 → leave unassigned (needs AI).

`SaveManifest` marshals the manifest back to YAML and writes it, preserving the `# AUTO-GENERATED` header comment.

- [ ] **Step 1: Write the failing tests**

`internal/manifest/filler_test.go`:
```go
package manifest

import (
	"testing"
)

func TestFillFromSnippets_SingleSection(t *testing.T) {
	m := &Manifest{Sections: map[string]Section{
		"setup": {Heading: "### Setup", Snippets: []string{}},
	}}
	n := FillFromSnippets(m, []string{"client-login", "client-logout"})
	if n != 2 {
		t.Fatalf("want 2 assigned, got %d", n)
	}
	got := m.Sections["setup"].Snippets
	if len(got) != 2 || got[0] != "client-login" || got[1] != "client-logout" {
		t.Errorf("unexpected snippets: %v", got)
	}
}

func TestFillFromSnippets_KeywordMatch(t *testing.T) {
	m := &Manifest{Sections: map[string]Section{
		"login-user":  {Heading: "### Login User", Snippets: []string{}},
		"logout-user": {Heading: "### Logout User", Snippets: []string{}},
	}}
	n := FillFromSnippets(m, []string{"client-login", "client-logout"})
	if n != 2 {
		t.Fatalf("want 2 assigned, got %d", n)
	}
	if got := m.Sections["login-user"].Snippets; len(got) != 1 || got[0] != "client-login" {
		t.Errorf("login-user: want [client-login], got %v", got)
	}
	if got := m.Sections["logout-user"].Snippets; len(got) != 1 || got[0] != "client-logout" {
		t.Errorf("logout-user: want [client-logout], got %v", got)
	}
}

func TestFillFromSnippets_NoMatch(t *testing.T) {
	m := &Manifest{Sections: map[string]Section{
		"section-alpha": {Heading: "### Alpha", Snippets: []string{}},
		"section-beta":  {Heading: "### Beta", Snippets: []string{}},
	}}
	n := FillFromSnippets(m, []string{"unrelated-xyz-key"})
	if n != 0 {
		t.Fatalf("want 0 assigned, got %d", n)
	}
}

func TestFillFromSnippets_SkipExisting(t *testing.T) {
	m := &Manifest{Sections: map[string]Section{
		"setup": {Heading: "### Setup", Snippets: []string{"client-login"}},
	}}
	n := FillFromSnippets(m, []string{"client-login"})
	if n != 0 {
		t.Fatalf("want 0 assigned (already exists), got %d", n)
	}
}

func TestFillFromSnippets_EmptyManifest(t *testing.T) {
	m := &Manifest{Sections: map[string]Section{}}
	n := FillFromSnippets(m, []string{"client-login"})
	if n != 0 {
		t.Fatalf("want 0 (no sections), got %d", n)
	}
}
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd social-plus-docs/harness
go test ./internal/manifest/ -run TestFillFromSnippets -v
```
Expected: FAIL — `FillFromSnippets` undefined.

- [ ] **Step 3: Implement `filler.go`**

`internal/manifest/filler.go`:
```go
package manifest

import (
	"os"
	"strings"

	"gopkg.in/yaml.v3"
)

// FillFromSnippets assigns candidate GendocsKeys to manifest sections using keyword matching.
// For each candidate not already in any section:
//   - If manifest has exactly 1 section: assign to it.
//   - Otherwise: score each section slug by counting key-words (len>2) found in the slug;
//     assign to highest-scoring section if score > 0.
//   - If no section scores > 0: leave unassigned (needs AI).
//
// Returns the count of newly assigned keys.
func FillFromSnippets(m *Manifest, candidates []string) int {
	sectionKeys := make([]string, 0, len(m.Sections))
	for k := range m.Sections {
		sectionKeys = append(sectionKeys, k)
	}
	if len(sectionKeys) == 0 {
		return 0
	}
	assigned := 0
	for _, key := range candidates {
		if keyExistsInAny(m, key) {
			continue
		}
		if len(sectionKeys) == 1 {
			sec := m.Sections[sectionKeys[0]]
			sec.Snippets = append(sec.Snippets, key)
			m.Sections[sectionKeys[0]] = sec
			assigned++
			continue
		}
		best, score := bestSectionForKey(sectionKeys, key)
		if score > 0 {
			sec := m.Sections[best]
			sec.Snippets = append(sec.Snippets, key)
			m.Sections[best] = sec
			assigned++
		}
	}
	return assigned
}

// SaveManifest writes m back to its file at docsDir/pagePath.manifest.yml,
// preserving the AUTO-GENERATED header comment.
func SaveManifest(docsDir, pagePath string, m *Manifest) error {
	outPath := PathForPage(docsDir, pagePath)
	out, err := yaml.Marshal(m)
	if err != nil {
		return err
	}
	const header = "# AUTO-GENERATED by harness genmanifests — fill in snippets: with GendocsKeys\n" +
		"# GendocsKey = DeriveKey(filename): strip 'Amity' prefix, PascalCase → kebab-case\n" +
		"# Example: AmityClientLogin.kt → client-login\n"
	return os.WriteFile(outPath, []byte(header+string(out)), 0o644)
}

func keyExistsInAny(m *Manifest, key string) bool {
	for _, sec := range m.Sections {
		for _, k := range sec.Snippets {
			if k == key {
				return true
			}
		}
	}
	return false
}

func bestSectionForKey(sectionKeys []string, key string) (string, int) {
	words := strings.Split(key, "-")
	best := ""
	bestScore := 0
	for _, sk := range sectionKeys {
		score := 0
		for _, w := range words {
			if len(w) > 2 && strings.Contains(sk, w) {
				score++
			}
		}
		if score > bestScore {
			bestScore = score
			best = sk
		}
	}
	return best, bestScore
}
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
go test ./internal/manifest/ -v
```
Expected: all 5 TestFillFromSnippets tests PASS, plus all existing manifest tests still pass.

- [ ] **Step 5: Commit**

```bash
cd social-plus-docs/harness
git add internal/manifest/filler.go internal/manifest/filler_test.go
git commit -m "feat(manifest): add FillFromSnippets + SaveManifest

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

---

## Task 2: `cmd/fillmanifests.go` — Scan SDKs → Auto-fill manifests

**Files:**
- Create: `cmd/fillmanifests.go`

**Background:** Scans all 4 SDK snippet dirs to build a `sp_docs_page → []GendocsKey` map, then walks every `*.manifest.yml` (skipping `harness/`), calls `FillFromSnippets`, and writes back changed manifests. Prints a summary.

- [ ] **Step 1: Implement `cmd/fillmanifests.go`**

```go
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
		filled := manifest.FillFromSnippets(m, candidates)

		for _, sec := range m.Sections {
			if len(sec.Snippets) == 0 {
				totalEmpty++
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
```

- [ ] **Step 2: Build to verify no compile errors**

```bash
cd social-plus-docs/harness
go build -o harness-bin ./cmd/ && echo "BUILD OK"
```
Expected: `BUILD OK`. If you see "undefined: runFillManifests", that's expected — Task 3 wires it into main.

- [ ] **Step 3: Run all tests**

```bash
go test ./... 2>&1 | grep -E "FAIL|ok"
```
Expected: all packages show `ok`, no FAIL.

---

## Task 3: Register `fillmanifests` in `cmd/main.go` + update test

**Files:**
- Modify: `cmd/main.go`
- Modify: `cmd/main_test.go`

- [ ] **Step 1: Add `fillmanifests` case to `main.go`**

Open `cmd/main.go`. Find the `switch cmd` block that has `case "genmanifests":`. Add `fillmanifests` immediately after it:

```go
case "fillmanifests":
    runFillManifests(args[1:])
```

Also update the usage string constant (search for `usage: harness` in the file) to add `fillmanifests`:

```go
const usage = "usage: harness <audit|fillmanifests|fix|genmanifests|gendocs|migrate|prompt> [--config path]\n"
```

- [ ] **Step 2: Update the usage assertion in `cmd/main_test.go`**

Find the line in `main_test.go` that asserts the usage string (it will contain `genmanifests`). Update it to also include `fillmanifests`:

```go
// The exact string must match the usage constant in main.go:
want := "usage: harness <audit|fillmanifests|fix|genmanifests|gendocs|migrate|prompt> [--config path]"
```

- [ ] **Step 3: Build + test**

```bash
cd social-plus-docs/harness
go build -o harness-bin ./cmd/ && echo "BUILD OK"
go test ./cmd/... -v 2>&1 | grep -E "PASS|FAIL|ok"
```
Expected: BUILD OK, all cmd tests pass.

- [ ] **Step 4: Smoke test the command**

```bash
./harness-bin fillmanifests --config harness-config.yml --dry-run
```
Expected output similar to:
```
[fillmanifests] DRY RUN: would assign 247 keys in 89 manifests; 156 sections still need AI
```
(Exact numbers will vary.)

- [ ] **Step 5: Commit**

```bash
git add cmd/main.go cmd/main_test.go cmd/fillmanifests.go
git commit -m "feat(fillmanifests): auto-assign GendocsKeys to manifest sections by keyword match

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

---

## Task 4: `cmd/prompt.go` — MANIFEST_FILL task section

**Files:**
- Modify: `cmd/prompt.go`

**Background:** After `fillmanifests` runs, some sections will still have `snippets: []`. These need an AI agent to assign the keys. `prompt` should walk all manifests, find empty sections, look up available snippet MDX files for that page's snippet directory, and emit a `MANIFEST_FILL` section in `harness-tasks.md`.

The snippet directory for a page is derived from the first 2 path segments of the page path:
- `social-plus-sdk/getting-started/authentication` → `snippets/social-plus-sdk/getting-started/`

List `.mdx` files in that directory = available GendocsKeys (filename without `.mdx`).

- [ ] **Step 1: Add imports to `prompt.go`** (if not already present)

```go
import (
    // existing imports ...
    "social-plus/harness/internal/manifest"
    "path"
    // "sort" may already be present
)
```

- [ ] **Step 2: Add MANIFEST_FILL generation after the existing task sections**

Find the section in `runPrompt` where `sb` writes the final content. After the existing task sections (MISSING_SNIPPET, DOC_PAGE_STALE_IMPORT etc.) and before the "After completion" block, add:

```go
// --- MANIFEST_FILL tasks ---
type manifestTask struct {
    pagePath    string
    sectionSlug string
    heading     string
    candidates  []string
}
var manifestFillTasks []manifestTask

docsBaseForManifest := filepath.Join(filepath.Dir(*cfgPath), cfg.Docs.Path)
snippetsDir := filepath.Join(docsBaseForManifest, "snippets")

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
    m, found, err := manifest.LoadForPage(docsBaseForManifest, pagePath)
    if !found || err != nil {
        return nil
    }
    for slug, sec := range m.Sections {
        if len(sec.Snippets) > 0 {
            continue
        }
        // find available keys: list snippets/<seg0>/<seg1>/*.mdx
        segs := strings.SplitN(pagePath, "/", 3)
        dir1, dir2 := "unknown", "unknown"
        if len(segs) > 0 { dir1 = segs[0] }
        if len(segs) > 1 { dir2 = segs[1] }
        snipDir := filepath.Join(snippetsDir, dir1, dir2)
        var candidates []string
        if entries, readErr := os.ReadDir(snipDir); readErr == nil {
            for _, e := range entries {
                if strings.HasSuffix(e.Name(), ".mdx") {
                    candidates = append(candidates, strings.TrimSuffix(e.Name(), ".mdx"))
                }
            }
        }
        manifestFillTasks = append(manifestFillTasks, manifestTask{
            pagePath:    pagePath,
            sectionSlug: slug,
            heading:     sec.Heading,
            candidates:  candidates,
        })
    }
    return nil
})

if len(manifestFillTasks) > 0 {
    sb.WriteString(fmt.Sprintf("\n---\n\n## MANIFEST_FILL (%d sections need assignment)\n\n", len(manifestFillTasks)))
    sb.WriteString("For each section below, edit the manifest file and add the GendocsKeys that belong\n")
    sb.WriteString("in that section to the `snippets:` array. Use the section heading as your guide.\n\n")
    for _, mt := range manifestFillTasks {
        sb.WriteString(fmt.Sprintf("### %s → %s\n\n", mt.pagePath, mt.sectionSlug))
        sb.WriteString(fmt.Sprintf("**Manifest:** `%s`\n", mt.pagePath+".manifest.yml"))
        sb.WriteString(fmt.Sprintf("**Section:** `%s`\n", mt.heading))
        if len(mt.candidates) > 0 {
            sb.WriteString("**Available keys (from snippet dir):**\n")
            for _, k := range mt.candidates {
                sb.WriteString(fmt.Sprintf("- `%s`\n", k))
            }
        } else {
            sb.WriteString("**Available keys:** _(none yet — write snippets first)_\n")
        }
        sb.WriteString("\n")
    }
}
```

Also update the summary `fmt.Printf` at the end to include manifest fill count:

Old:
```go
fmt.Printf("Tasks written to %s (%d missing snippets, %d drift fixes, %d stale imports)\n", *outPath, len(missing), len(driftTasks), staleImportCount)
```
New:
```go
fmt.Printf("Tasks written to %s (%d missing snippets, %d drift fixes, %d stale imports, %d manifest fills)\n",
    *outPath, len(missing), len(driftTasks), staleImportCount, len(manifestFillTasks))
```

- [ ] **Step 3: Build + run tests**

```bash
cd social-plus-docs/harness
go build -o harness-bin ./cmd/ && echo "BUILD OK"
go test ./cmd/... -v 2>&1 | grep -E "PASS|FAIL|ok"
```

- [ ] **Step 4: Smoke test prompt output**

```bash
./harness-bin prompt --config harness-config.yml
```
The output `harness-tasks.md` should now contain a `## MANIFEST_FILL` section listing empty sections with their available candidate keys.

Verify the section exists:
```bash
grep "MANIFEST_FILL" harness-tasks.md | head -3
```

- [ ] **Step 5: Commit**

```bash
git add cmd/prompt.go
git commit -m "feat(prompt): add MANIFEST_FILL task section for empty manifest sections

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

---

## Task 5: `differ.go` DiffDocImports + `audit.go` DOC_BROKEN_IMPORT

**Files:**
- Modify: `internal/differ/differ.go`
- Modify: `internal/differ/differ_test.go`
- Modify: `cmd/audit.go`
- Modify: `internal/report/report.go` (add new finding type constant)

**Background:** After `migrate` runs, doc pages get `import X from '/snippets/...'` lines. If the snippet MDX file doesn't actually exist, Mintlify will fail to build. `DiffDocImports` scans MDX files for import statements and verifies each imported path exists under `docsBase`. Finding type: `DOC_BROKEN_IMPORT`.

- [ ] **Step 1: Add `TypeDocBrokenImport` to `internal/report/report.go`**

Find the `const` block with `TypeDocPageStaleImport` and add:
```go
TypeDocBrokenImport = "DOC_BROKEN_IMPORT"
```

- [ ] **Step 2: Write failing tests in `internal/differ/differ_test.go`**

Append to the file:
```go
func TestDiffDocImports_NoImports(t *testing.T) {
    dir := t.TempDir()
    mdxFile := filepath.Join(dir, "page.mdx")
    os.WriteFile(mdxFile, []byte("# Hello\n\nsome prose\n"), 0644)
    findings := DiffDocImports(mdxFile, dir)
    if len(findings) != 0 {
        t.Fatalf("want 0 findings, got %d", len(findings))
    }
}

func TestDiffDocImports_GoodImport(t *testing.T) {
    dir := t.TempDir()
    // create the snippet file
    os.MkdirAll(filepath.Join(dir, "snippets", "sdk", "auth"), 0755)
    os.WriteFile(filepath.Join(dir, "snippets", "sdk", "auth", "client-login.mdx"), []byte("content"), 0644)
    mdxFile := filepath.Join(dir, "page.mdx")
    os.WriteFile(mdxFile, []byte("import ClientLogin from '/snippets/sdk/auth/client-login.mdx'\n"), 0644)
    findings := DiffDocImports(mdxFile, dir)
    if len(findings) != 0 {
        t.Fatalf("want 0 findings for valid import, got %d", len(findings))
    }
}

func TestDiffDocImports_BrokenImport(t *testing.T) {
    dir := t.TempDir()
    mdxFile := filepath.Join(dir, "page.mdx")
    os.WriteFile(mdxFile, []byte("import Missing from '/snippets/does/not/exist.mdx'\n"), 0644)
    findings := DiffDocImports(mdxFile, dir)
    if len(findings) != 1 {
        t.Fatalf("want 1 finding for broken import, got %d", len(findings))
    }
    if findings[0].Type != report.TypeDocBrokenImport {
        t.Errorf("wrong finding type: %s", findings[0].Type)
    }
}
```

- [ ] **Step 3: Run tests to verify they fail**

```bash
go test ./internal/differ/... -run TestDiffDocImports -v
```
Expected: FAIL — `DiffDocImports` undefined.

- [ ] **Step 4: Implement `DiffDocImports` in `internal/differ/differ.go`**

Add this function (append to the file):
```go
// DiffDocImports scans an MDX file for `import X from '/snippets/...'` lines
// and returns a DOC_BROKEN_IMPORT finding for each import whose target file
// does not exist under docsBase.
func DiffDocImports(mdxPath, docsBase string) []Finding {
    data, err := os.ReadFile(mdxPath)
    if err != nil {
        return nil
    }
    var findings []Finding
    for i, line := range strings.Split(string(data), "\n") {
        line = strings.TrimSpace(line)
        if !strings.HasPrefix(line, "import ") || !strings.Contains(line, "'/snippets/") {
            continue
        }
        // extract path between single quotes
        start := strings.Index(line, "'/snippets/")
        if start == -1 {
            continue
        }
        rest := line[start+1:]
        end := strings.Index(rest, "'")
        if end == -1 {
            continue
        }
        importPath := rest[:end] // e.g. /snippets/social-plus-sdk/getting-started/client-login.mdx
        absTarget := filepath.Join(docsBase, filepath.FromSlash(strings.TrimPrefix(importPath, "/")))
        if _, statErr := os.Stat(absTarget); os.IsNotExist(statErr) {
            rel, _ := filepath.Rel(docsBase, mdxPath)
            findings = append(findings, Finding{
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
```

- [ ] **Step 5: Run tests to verify they pass**

```bash
go test ./internal/differ/... -v 2>&1 | grep -E "PASS|FAIL|ok"
```
Expected: all differ tests pass.

- [ ] **Step 6: Wire `DiffDocImports` into `cmd/audit.go`**

In `cmd/audit.go`, find the manifest coverage walk block (around line 144). After it, add a new block that walks all MDX files and runs import checking:

```go
// Check for broken import paths (post-migrate validation).
importErrCount := 0
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
    if !strings.HasSuffix(path, ".mdx") {
        return nil
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
```

- [ ] **Step 7: Build + full test**

```bash
cd social-plus-docs/harness
go build -o harness-bin ./cmd/ && echo "BUILD OK"
go test ./... 2>&1 | grep -E "FAIL|ok"
```
Expected: all packages `ok`.

- [ ] **Step 8: Verify audit runs cleanly (no new false positives)**

```bash
./harness-bin audit --config harness-config.yml 2>&1 | grep -E "broken import|Summary"
```
Expected: `0 broken import findings` (no current imports are broken), summary unchanged.

- [ ] **Step 9: Commit**

```bash
git add internal/differ/differ.go internal/differ/differ_test.go cmd/audit.go internal/report/report.go
git commit -m "feat(audit): add DOC_BROKEN_IMPORT check for post-migration import validation

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

---

## Task 6: E2E Pipeline — Fill, Migrate, Verify

**Files:**
- Modify: `harness/docs/BIG-PICTURE.md`

This task runs the full pipeline. Steps marked 🤖 are inferential (AI agent work); steps marked ⚙️ are computational (run the command).

### Phase A: Computational fill

- [ ] **Step 1 ⚙️: Run `fillmanifests` (writes GendocsKeys to manifests by keyword match)**

```bash
cd social-plus-docs/harness
./harness-bin fillmanifests --config harness-config.yml
```
Expected: output like `[fillmanifests] done — assigned 247 keys in 89 manifests; 156 sections still need AI (run prompt)`

- [ ] **Step 2 ⚙️: Regenerate harness-tasks.md with MANIFEST_FILL section**

```bash
./harness-bin prompt --config harness-config.yml
```
Expected: `harness-tasks.md` now has a `## MANIFEST_FILL (N sections need assignment)` section.

- [ ] **Step 3: Inspect and verify the MANIFEST_FILL tasks are sane**

```bash
grep -A 6 "MANIFEST_FILL" harness-tasks.md | head -30
```
Check that sections list reasonable candidate keys. If a section has `_(none yet)_`, it means no snippet MDX files exist yet for that page area — this is expected for pages without any snippets.

### Phase B: Inferential fill (AI agent work)

- [ ] **Step 4 🤖: AI agent fills remaining manifest sections**

Tell the Copilot CLI agent (in a new conversation or using the harness-tasks.md runbook):
> "Read the `## MANIFEST_FILL` section in `social-plus-docs/harness/harness-tasks.md`. For each listed section, edit the corresponding `.manifest.yml` file and add the GendocsKeys from the candidate list that semantically match the section heading. Use judgment — if the section is 'Step 2: Login User' and candidates include `client-login` and `client-logout`, add `client-login`. If unsure, leave the section empty."

The agent should: open each manifest file, look at the section heading + candidates, and add the appropriate keys.

- [ ] **Step 5 ⚙️: Run `audit` to generate MISSING_SNIPPET findings from filled manifests**

```bash
./harness-bin audit --config harness-config.yml
```
Expected: new `[audit] N manifest coverage findings from M manifests` line. These are MISSING_SNIPPET findings for sections that reference keys but no snippet MDX exists.

- [ ] **Step 6 ⚙️: Regenerate harness-tasks.md with MISSING_SNIPPET tasks**

```bash
./harness-bin prompt --config harness-config.yml
```
Expected: `## MISSING_SNIPPET (N)` section listing which SDK function files need to be created.

### Phase C: Migration + validation

- [ ] **Step 7 ⚙️: Dry-run migrate to preview changes**

```bash
./harness-bin migrate --config harness-config.yml --dry-run 2>&1 | tail -5
```
Expected: `[migrate] done — written: 0, dry-run skipped: 949, errors: 0`

- [ ] **Step 8 ⚙️: Run migrate (writes changes to doc pages)**

```bash
./harness-bin migrate --config harness-config.yml
```
Expected: output like `[migrate] done — written: 949, dry-run skipped: 0, errors: 0`

- [ ] **Step 9 ⚙️: Run audit to check for broken imports**

```bash
./harness-bin audit --config harness-config.yml 2>&1 | grep -E "broken import|Summary"
```
Expected: `0 broken import findings`. If broken imports appear, the snippet MDX files referenced in manifests don't exist — run `gendocs` first:
```bash
./harness-bin gendocs --config harness-config.yml --clean
./harness-bin audit --config harness-config.yml
```

- [ ] **Step 10 ⚙️: Check for Mintlify build errors (if Mintlify CLI is installed)**

```bash
cd social-plus-docs
npx mintlify build 2>&1 | grep -E "error|Error|broken" | head -20
```
If Mintlify is not installed, skip this step and rely on the `DOC_BROKEN_IMPORT` audit check instead.

- [ ] **Step 11: Update BIG-PICTURE.md current state table**

Update the status table rows:

| Component | Status |
|---|---|
| `internal/manifest/filler.go` | ✅ |
| `genmanifests` command | ✅ — 123 skeletons |
| **fillmanifests command** | ✅ — auto-assigns by keyword |
| **Page manifest `snippets:` fill-in** | ✅ (computational) / 🤖 (remaining) |
| **DOC_BROKEN_IMPORT check** | ✅ |
| **Migration (949 DOC_PAGE_STALE_IMPORT)** | ✅ — complete |
| **Mintlify build validation** | ✅ — no broken imports |

- [ ] **Step 12: Commit everything**

```bash
cd social-plus-docs/harness
git add .
git commit -m "feat: complete manifest fill-in + migration pipeline + import validation

- fillmanifests: auto-assigns snippet keys by keyword match
- prompt: MANIFEST_FILL tasks for sections needing AI
- audit: DOC_BROKEN_IMPORT for post-migration import validation
- Manifests filled, 949 doc pages migrated, 0 broken imports
- BIG-PICTURE updated to reflect completed pipeline

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

---

## Self-Review

**Spec coverage check:**
- ✅ `FillFromSnippets` (keyword match + single-section fallback) — Task 1
- ✅ `SaveManifest` (write back to YAML) — Task 1
- ✅ `fillmanifests` CLI command (scan all 4 SDKs) — Task 2
- ✅ Register in `main.go`, update usage string — Task 3
- ✅ `prompt` MANIFEST_FILL tasks for empty sections — Task 4
- ✅ `DiffDocImports` + `DOC_BROKEN_IMPORT` — Task 5
- ✅ E2E pipeline: fill → audit → migrate → verify — Task 6
- ✅ Mintlify build check step included — Task 6 Step 10

**No placeholders:** All code blocks contain full, compilable Go code. All commands include expected output.

**Type consistency:**
- `FillFromSnippets(m *Manifest, candidates []string) int` — used in Task 1 (definition) and Task 2 (call)
- `SaveManifest(docsDir, pagePath string, m *Manifest) error` — defined Task 1, called Task 2
- `DiffDocImports(mdxPath, docsBase string) []Finding` — defined Task 5, wired in Task 5 Step 6
- `report.TypeDocBrokenImport` — added in Task 5 Step 1, used in Task 5 Step 4
- `manifest.FillFromSnippets` and `manifest.SaveManifest` — package-qualified correctly in Task 2

**Potential issue:** `cmd/prompt.go` Task 4 imports `"social-plus/harness/internal/manifest"` — verify this import isn't already present and doesn't conflict.
