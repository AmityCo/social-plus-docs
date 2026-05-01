# Cross-Platform Function Parity Map Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a `parity` command that produces a `function-parity.json` master file showing which snippet keys exist on each platform, and refactor `annotateConfidence` to derive `high/medium/low` from this data.

**Architecture:** New `internal/paritymap` package owns the data types and `Build` function. The `parity` command writes `function-parity.json` as a standalone regenerable file. `audit` also writes it as a side effect after scanning. `annotate` reads parity data to compute confidence instead of re-scanning snippet dirs inline.

**Tech Stack:** Go, `encoding/json`, existing `scanner.Snippet`, `docgen.DeriveKey`, `config.Config`

---

## File Map

| File | Action | Responsibility |
|---|---|---|
| `harness/internal/paritymap/paritymap.go` | Create | Types (`ParityMap`, `FunctionEntry`, `PlatformStatus`) + `Build()` + `Write()` + `Read()` |
| `harness/internal/paritymap/paritymap_test.go` | Create | Unit tests for `Build` |
| `harness/cmd/parity.go` | Create | `runParity` — scan all platforms → build → write `function-parity.json` |
| `harness/cmd/main.go` | Modify | Register `parity` command |
| `harness/cmd/annotate.go` | Modify | Replace inline `allGroups` scan with `paritymap.Build`; refactor `annotateConfidence` |
| `harness/cmd/audit.go` | Modify | Write `function-parity.json` as side effect after collecting `allSnips` |
| `harness/_docs/BIG-PICTURE.md` | Modify | Document parity command, file format, status values |

---

## Task 1: `internal/paritymap` package

**Files:**
- Create: `harness/internal/paritymap/paritymap.go`
- Create: `harness/internal/paritymap/paritymap_test.go`

- [ ] **Step 1: Write failing tests**

```go
// harness/internal/paritymap/paritymap_test.go
package paritymap_test

import (
	"testing"
	"time"

	"social-plus/harness/internal/paritymap"
	"social-plus/harness/internal/scanner"
)

func TestBuild_Basic(t *testing.T) {
	snips := []scanner.Snippet{
		{Filename: "AmityPostRepository.kt", SpDocsPage: "/social-plus-sdk/post/create", Platform: "android"},
		{Filename: "AmityPostRepository.swift", SpDocsPage: "/social-plus-sdk/post/create", Platform: "ios"},
	}
	pm := paritymap.Build(snips, []string{"android", "ios", "flutter", "typescript"})

	if pm.TotalKeys != 1 {
		t.Fatalf("want 1 key, got %d", pm.TotalKeys)
	}
	fn := pm.Functions[0]
	if fn.Key != "post-repository" {
		t.Errorf("want key=post-repository, got %s", fn.Key)
	}
	if fn.Platforms["android"].Status != paritymap.StatusExists {
		t.Errorf("android should be exists")
	}
	if fn.Platforms["flutter"].Status != paritymap.StatusUnknown {
		t.Errorf("flutter should be unknown")
	}
	if fn.Coverage != 2 {
		t.Errorf("want coverage=2, got %d", fn.Coverage)
	}
}

func TestBuild_SortedOutput(t *testing.T) {
	snips := []scanner.Snippet{
		{Filename: "AmityZZZ.kt", SpDocsPage: "/p/zzz", Platform: "android"},
		{Filename: "AmityAAA.kt", SpDocsPage: "/p/aaa", Platform: "android"},
	}
	pm := paritymap.Build(snips, []string{"android"})
	if pm.Functions[0].Key >= pm.Functions[1].Key {
		t.Errorf("functions should be sorted by key: got %s, %s", pm.Functions[0].Key, pm.Functions[1].Key)
	}
}

func TestBuild_GeneratedAtSet(t *testing.T) {
	before := time.Now()
	pm := paritymap.Build(nil, []string{"android"})
	after := time.Now()
	if pm.GeneratedAt.Before(before) || pm.GeneratedAt.After(after) {
		t.Errorf("GeneratedAt out of expected range")
	}
}

func TestBuild_MultiPlatformSameKey(t *testing.T) {
	// Same logical class, all 4 platforms
	snips := []scanner.Snippet{
		{Filename: "AmityLogin.kt",    SpDocsPage: "/p/auth", Platform: "android"},
		{Filename: "AmityLogin.swift", SpDocsPage: "/p/auth", Platform: "ios"},
		{Filename: "AmityLogin.dart",  SpDocsPage: "/p/auth", Platform: "flutter"},
		{Filename: "AmityLogin.ts",    SpDocsPage: "/p/auth", Platform: "typescript"},
	}
	pm := paritymap.Build(snips, []string{"android", "ios", "flutter", "typescript"})
	if pm.TotalKeys != 1 {
		t.Fatalf("want 1 key, got %d", pm.TotalKeys)
	}
	if pm.Functions[0].Coverage != 4 {
		t.Errorf("want coverage=4, got %d", pm.Functions[0].Coverage)
	}
}
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd /path/to/social-plus-docs/harness
go test ./internal/paritymap/... 2>&1 | head -10
```
Expected: `cannot find package` or `no Go files`

- [ ] **Step 3: Implement `paritymap.go`**

```go
// harness/internal/paritymap/paritymap.go
package paritymap

import (
	"encoding/json"
	"os"
	"sort"
	"time"

	"social-plus/harness/internal/docgen"
	"social-plus/harness/internal/scanner"
)

// PlatformStatus describes a function's annotation state on one platform.
type PlatformStatus string

const (
	StatusExists  PlatformStatus = "exists"  // has begin_sample_code annotation
	StatusUnknown PlatformStatus = "unknown" // not found in snippet scan
)

// PlatformEntry is the per-platform record inside a FunctionEntry.
type PlatformEntry struct {
	Status PlatformStatus `json:"status"`
	File   string         `json:"file,omitempty"` // relative SDK file path when status=exists
}

// FunctionEntry represents one logical function key and its coverage across platforms.
type FunctionEntry struct {
	Key        string                   `json:"key"`
	SpDocsPage string                   `json:"sp_docs_page"`
	Platforms  map[string]PlatformEntry `json:"platforms"`
	Coverage   int                      `json:"coverage"`        // number of platforms with status=exists
	Total      int                      `json:"total_platforms"` // len(all configured platforms)
}

// ParityMap is the top-level structure written to function-parity.json.
type ParityMap struct {
	GeneratedAt time.Time       `json:"generated_at"`
	TotalKeys   int             `json:"total_keys"`
	AllPlatforms []string       `json:"platforms"`
	Functions   []FunctionEntry `json:"functions"`
}

// Build constructs a ParityMap from a flat slice of snippets.
// platforms is the ordered list of all configured platform names.
func Build(snips []scanner.Snippet, platforms []string) ParityMap {
	// group by key
	type entry struct {
		spDocsPage string
		byPlatform map[string]PlatformEntry
	}
	byKey := map[string]*entry{}
	for _, s := range snips {
		key := docgen.DeriveKey(s.Filename)
		if _, ok := byKey[key]; !ok {
			byKey[key] = &entry{
				spDocsPage: s.SpDocsPage,
				byPlatform: map[string]PlatformEntry{},
			}
		}
		e := byKey[key]
		// android wins for sp_docs_page (platform sort: android comes first)
		if s.Platform == "android" || e.spDocsPage == "" {
			e.spDocsPage = s.SpDocsPage
		}
		e.byPlatform[s.Platform] = PlatformEntry{
			Status: StatusExists,
			File:   s.File,
		}
	}

	// build sorted function entries
	keys := make([]string, 0, len(byKey))
	for k := range byKey {
		keys = append(keys, k)
	}
	sort.Strings(keys)

	funcs := make([]FunctionEntry, 0, len(keys))
	for _, k := range keys {
		e := byKey[k]
		pm := make(map[string]PlatformEntry, len(platforms))
		coverage := 0
		for _, p := range platforms {
			if pe, ok := e.byPlatform[p]; ok {
				pm[p] = pe
				coverage++
			} else {
				pm[p] = PlatformEntry{Status: StatusUnknown}
			}
		}
		funcs = append(funcs, FunctionEntry{
			Key:        k,
			SpDocsPage: e.spDocsPage,
			Platforms:  pm,
			Coverage:   coverage,
			Total:      len(platforms),
		})
	}

	return ParityMap{
		GeneratedAt:  time.Now().UTC(),
		TotalKeys:    len(funcs),
		AllPlatforms: platforms,
		Functions:    funcs,
	}
}

// Write serialises pm to the given file path (creates or truncates).
func Write(path string, pm ParityMap) error {
	f, err := os.Create(path)
	if err != nil {
		return err
	}
	defer f.Close()
	enc := json.NewEncoder(f)
	enc.SetIndent("", "  ")
	return enc.Encode(pm)
}

// Read deserialises a ParityMap from the given file path.
func Read(path string) (ParityMap, error) {
	f, err := os.Open(path)
	if err != nil {
		return ParityMap{}, err
	}
	defer f.Close()
	var pm ParityMap
	return pm, json.NewDecoder(f).Decode(&pm)
}

// Confidence returns the Gate 2 confidence level for a given key and platform
// by counting sibling platforms (excluding self) that have StatusExists.
//   - "high"   — 2 or more sibling platforms exist
//   - "medium" — exactly 1 sibling platform exists
//   - "low"    — no sibling platforms exist
func (pm ParityMap) Confidence(key, selfPlatform string) string {
	for _, fn := range pm.Functions {
		if fn.Key != key {
			continue
		}
		count := 0
		for p, pe := range fn.Platforms {
			if p == selfPlatform {
				continue
			}
			if pe.Status == StatusExists {
				count++
			}
		}
		switch {
		case count >= 2:
			return "high"
		case count == 1:
			return "medium"
		default:
			return "low"
		}
	}
	return "low"
}
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
cd /path/to/social-plus-docs/harness
go test ./internal/paritymap/... -v 2>&1 | tail -15
```
Expected: 4 tests PASS

- [ ] **Step 5: gofmt + vet**

```bash
gofmt -w internal/paritymap/paritymap.go internal/paritymap/paritymap_test.go
go vet ./internal/paritymap/...
```
Expected: no output (clean)

- [ ] **Step 6: Commit**

```bash
git add harness/internal/paritymap/
git commit -m "feat(paritymap): add cross-platform function parity package

Build(), Write(), Read(), and Confidence() from snippet slice.
Outputs function-parity.json with exists/unknown per platform.

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

---

## Task 2: `parity` command

**Files:**
- Create: `harness/cmd/parity.go`
- Modify: `harness/cmd/main.go`

- [ ] **Step 1: Write failing test (smoke test via main_test.go)**

In `harness/cmd/main_test.go`, there is likely an existing pattern for command smoke tests. Add:

```go
func TestRunParity_MissingConfig(t *testing.T) {
	// Should fail gracefully with a missing config, not panic
	// Run via exec so we can capture exit code
	cmd := exec.Command("go", "run", ".", "parity", "--config", "/nonexistent/harness.yml")
	cmd.Dir = "."
	out, _ := cmd.CombinedOutput()
	if !strings.Contains(string(out), "load config") && !strings.Contains(string(out), "no such file") {
		t.Errorf("unexpected output: %s", string(out))
	}
}
```

Note: check `main_test.go` first to follow existing test patterns in the file.

- [ ] **Step 2: Implement `cmd/parity.go`**

```go
// harness/cmd/parity.go
package main

import (
	"flag"
	"fmt"
	"os"
	"path/filepath"
	"sort"

	"social-plus/harness/internal/config"
	"social-plus/harness/internal/paritymap"
	"social-plus/harness/internal/scanner"
)

func runParity(args []string) {
	fs := flag.NewFlagSet("parity", flag.ExitOnError)
	cfgPath := fs.String("config", "harness-config.yml", "path to harness-config.yml")
	outPath := fs.String("out", "function-parity.json", "output parity file path")
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

	// Collect all snippets across all platforms.
	var allSnips []scanner.Snippet
	platforms := sortedPlatforms(cfg)
	for _, platform := range platforms {
		sdkCfg := cfg.SDKs[platform]
		snippetPath := filepath.Join(cfgDir, sdkCfg.Path, sdkCfg.SnippetDir)
		snips, err := scanner.Scan(snippetPath, platform)
		if err != nil {
			fmt.Fprintf(os.Stderr, "warning: skipping %s: %v\n", platform, err)
			continue
		}
		allSnips = append(allSnips, snips...)
	}

	pm := paritymap.Build(allSnips, platforms)

	dest := filepath.Join(cfgDir, *outPath)
	if err := paritymap.Write(dest, pm); err != nil {
		fmt.Fprintf(os.Stderr, "write parity: %v\n", err)
		os.Exit(1)
	}

	fmt.Printf("wrote %s (%d keys across %d platforms)\n", dest, pm.TotalKeys, len(platforms))
}

// sortedPlatforms returns cfg.SDKs keys in deterministic order.
func sortedPlatforms(cfg *config.Config) []string {
	ps := make([]string, 0, len(cfg.SDKs))
	for p := range cfg.SDKs {
		ps = append(ps, p)
	}
	sort.Strings(ps)
	return ps
}
```

- [ ] **Step 3: Register in `main.go`**

In `harness/cmd/main.go`, update the usage line and add the case:

```go
// usage line — replace existing:
fmt.Fprintf(os.Stderr, "usage: harness <annotate|audit|fillmanifests|fix|genmanifests|gendocs|migrate|parity|prompt|serve> [--config path]\n")

// add case in switch:
case "parity":
    runParity(os.Args[2:])
```

- [ ] **Step 4: Build + test**

```bash
cd /path/to/social-plus-docs/harness
go build ./...
go test ./... 2>&1 | tail -10
```
Expected: all packages pass, no compile errors

- [ ] **Step 5: Smoke test**

```bash
cd /path/to/social-plus-docs
./harness/harness-bin parity --config harness.yml
# Should print: "wrote function-parity.json (N keys across 4 platforms)"
head -20 function-parity.json
```
Expected: valid JSON with `generated_at`, `total_keys`, `platforms`, `functions`

- [ ] **Step 6: Commit**

```bash
git add harness/cmd/parity.go harness/cmd/main.go
git commit -m "feat(parity): add parity command — generates function-parity.json

Scans all 4 SDK snippet dirs, groups by key, writes exists/unknown
per platform. Run: harness parity --config harness.yml

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

---

## Task 3: Refactor `annotate.go` to use paritymap

**Files:**
- Modify: `harness/cmd/annotate.go` lines ~65-75 (allGroups build) and ~184-198 (annotateConfidence)

The current `annotate.go` builds `allGroups map[string]docgen.SnippetGroup` to compute confidence. Replace with `paritymap.Build` so confidence is derived consistently from the same data model.

- [ ] **Step 1: Replace `allGroups` build with paritymap**

Find the block starting at `// Build snippet groups to check confidence`:

```go
// OLD (remove this):
var allSnips []scanner.Snippet
for platform, sdkCfg := range cfg.SDKs {
    snippetPath := filepath.Join(cfgDir, sdkCfg.Path, sdkCfg.SnippetDir)
    snips, err := scanner.Scan(snippetPath, platform)
    if err != nil {
        fmt.Fprintf(os.Stderr, "warning: skipping %s snippets: %v\n", platform, err)
    }
    allSnips = append(allSnips, snips...)
}
allGroups := docgen.GroupSnippets(allSnips)
```

Replace with:

```go
// Build parity map for Gate 2 confidence signals.
var allSnips []scanner.Snippet
platforms := sortedPlatforms(cfg)
for _, platform := range platforms {
    sdkCfg := cfg.SDKs[platform]
    snippetPath := filepath.Join(cfgDir, sdkCfg.Path, sdkCfg.SnippetDir)
    snips, err := scanner.Scan(snippetPath, platform)
    if err != nil {
        fmt.Fprintf(os.Stderr, "warning: skipping %s snippets: %v\n", platform, err)
    }
    allSnips = append(allSnips, snips...)
}
pm := paritymap.Build(allSnips, platforms)
```

Note: `sortedPlatforms` is already defined in `parity.go` (same package `main`). If it's not accessible (e.g., `parity.go` not yet present), define it there first.

- [ ] **Step 2: Replace `annotateConfidence` call site**

Find where `Confidence` is set in the `patchgen.Patch` literal. Change:
```go
Confidence: annotateConfidence(className, platform, allGroups),
```
to:
```go
Confidence: pm.Confidence(docgen.DeriveKey(className+"."+platformExt(platform)), platform),
```

Note: the key derivation must match what `paritymap.Build` uses. `Build` calls `docgen.DeriveKey(s.Filename)` where `s.Filename` is e.g. `AmityPostRepository.kt`. So `DeriveKey(className + "." + platformExt(platform))` is correct.

- [ ] **Step 3: Remove the old `annotateConfidence` function and `platformExt` map**

The `annotateConfidence` function (lines ~184–198) and the `platformExt` function/map are now replaced by `pm.Confidence()` and `sortedPlatforms`. Remove `annotateConfidence`. Keep `platformExt` only if it's used elsewhere (check with `grep`).

Also remove the `docgen` import from `annotate.go` imports only if it's no longer used there (check remaining usages of `docgen.` in the file before removing).

Add import: `"social-plus/harness/internal/paritymap"`

- [ ] **Step 4: Build + gofmt + vet + test**

```bash
cd /path/to/social-plus-docs/harness
go build ./...
gofmt -w cmd/annotate.go
go vet ./...
go test ./... 2>&1 | tail -10
```
Expected: all clean and passing

- [ ] **Step 5: Commit**

```bash
git add harness/cmd/annotate.go
git commit -m "refactor(annotate): use paritymap.Confidence instead of inline allGroups scan

Gate 2 confidence now derived from paritymap.Build, consistent with
the parity command output. Removes duplicate scanning logic.

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

---

## Task 4: Wire parity generation into `audit`

**Files:**
- Modify: `harness/cmd/audit.go` — after `allSnips` is collected, also write `function-parity.json`

- [ ] **Step 1: Find the right insertion point**

In `audit.go`, find the line:
```go
allGroups := docgen.GroupSnippets(allSnips)
```
This is where `allSnips` is fully populated. The parity build goes immediately after.

- [ ] **Step 2: Insert parity write block**

After `allGroups := docgen.GroupSnippets(allSnips)`, add:

```go
// Write function-parity.json as a side effect of audit.
{
    platforms := sortedPlatforms(cfg)
    pm := paritymap.Build(allSnips, platforms)
    parityDest := filepath.Join(cfgDir, "function-parity.json")
    if err := paritymap.Write(parityDest, pm); err != nil {
        fmt.Fprintf(os.Stderr, "warning: could not write function-parity.json: %v\n", err)
    }
}
```

Add `"social-plus/harness/internal/paritymap"` to `audit.go` imports.

- [ ] **Step 3: Build + gofmt + vet + test**

```bash
cd /path/to/social-plus-docs/harness
go build ./...
gofmt -w cmd/audit.go
go vet ./...
go test ./... 2>&1 | tail -10
```
Expected: all clean

- [ ] **Step 4: Smoke test**

```bash
cd /path/to/social-plus-docs
./harness/harness-bin audit --config harness.yml > /dev/null
ls -lh function-parity.json
head -30 function-parity.json
```
Expected: `function-parity.json` written alongside `harness-report.json`

- [ ] **Step 5: Rebuild binary and commit**

```bash
cd /path/to/social-plus-docs/harness
go build -o harness-bin ./cmd
cd ..
git add harness/cmd/audit.go harness/harness-bin function-parity.json
git commit -m "feat(audit): write function-parity.json as side effect of audit

Audit now regenerates function-parity.json after collecting all snippets.
Provides always-fresh parity data without a separate parity run.

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

---

## Task 5: Update BIG-PICTURE.md

**Files:**
- Modify: `harness/_docs/BIG-PICTURE.md`

- [ ] **Step 1: Add `parity` command section**

After the `### serve` section, add:

```markdown
### `parity` — Cross-platform function parity map ⚙️ Computational
Scans all 4 SDK snippet dirs → builds `function-parity.json`: a master list of every
annotated snippet key and its status per platform.

```bash
./harness-bin parity --config harness-config.yml   # writes function-parity.json
# audit also regenerates it automatically as a side effect
```

Output format:
```json
{
  "generated_at": "2026-05-01T...",
  "total_keys": 1019,
  "platforms": ["android", "flutter", "ios", "typescript"],
  "functions": [
    {
      "key": "post-create",
      "sp_docs_page": "/social-plus-sdk/social/post/create-post",
      "platforms": {
        "android":    {"status": "exists", "file": "AmityPostRepository.kt"},
        "ios":        {"status": "exists", "file": "AmityPostRepository.swift"},
        "flutter":    {"status": "unknown"},
        "typescript": {"status": "exists", "file": "AmityPostRepository.ts"}
      },
      "coverage": 3,
      "total_platforms": 4
    }
  ]
}
```

**Status values:**
- `exists` — platform has an annotated `begin_sample_code` snippet for this key
- `unknown` — not found in snippet scan (may be missing annotation or function may not exist on this platform)

**Feeds Gate 2:** `annotate` reads parity data to compute `confidence: high | medium | low`
rather than re-scanning inline. The parity file is always regenerated fresh — never mutated.
```

- [ ] **Step 2: Update Gate 2 description in Three-Gate section**

In the Three-Gate section, update Gate 2 to mention parity file:

```markdown
### Gate 2 — Inferential + Computational Oracle 🤖 + ⚙️
- `parity` (or `audit`) → regenerates `function-parity.json` with per-platform `exists`/`unknown` status
- `annotate` → reads parity data → generates patches with `confidence: high | medium | low`
  - `high` — 2+ sibling platforms have `exists` for this key
  - `medium` — exactly 1 sibling platform has `exists`
  - `low` — no siblings have `exists`
```

- [ ] **Step 3: Update Current State table**

Add row:
```
| `parity` command + `function-parity.json` | ✅ | Cross-platform snippet key matrix; regenerated by audit |
```

Update `patchgen` row:
```
| `patchgen` package | ✅ | ID inference + line finder; confidence derived from paritymap |
```

- [ ] **Step 4: Update CLI count** (8 → from the current 7 you just updated earlier to 8)

- [ ] **Step 5: Commit**

```bash
git add harness/_docs/BIG-PICTURE.md
git commit -m "docs: add parity command, function-parity.json, Gate 2 parity integration

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

---

## Self-Review

**Spec coverage:**
- ✅ `internal/paritymap` package with `Build`, `Write`, `Read`, `Confidence` — Task 1
- ✅ `parity` command writing `function-parity.json` — Task 2
- ✅ `annotate` confidence derived from parity (no duplicate scan) — Task 3
- ✅ `audit` auto-regenerates parity as side effect — Task 4
- ✅ BIG-PICTURE updated — Task 5
- ✅ Status values `exists`/`unknown` (no `missing` — computationally honest)
- ✅ Read-only parity file (Gate 2 never writes back to it)
- ✅ Confidence: 2+/1/0 sibling mapping to high/medium/low

**Placeholder scan:** None found.

**Type consistency:**
- `paritymap.Build(snips []scanner.Snippet, platforms []string) ParityMap` — used in Task 2 (`parity.go`) and Task 3 (`annotate.go`) and Task 4 (`audit.go`) ✅
- `pm.Confidence(key, selfPlatform string) string` — used in Task 3 call site ✅
- `sortedPlatforms(cfg *config.Config) []string` — defined in Task 2 (`parity.go`), used in Tasks 3 and 4 ✅
- `paritymap.Write(dest string, pm ParityMap) error` — used in Tasks 2 and 4 ✅
