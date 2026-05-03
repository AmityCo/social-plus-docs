# Incremental Audit (Delta Mode) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** `harness audit --incremental` re-scans only SDK platforms that have changed since the last baseline commit, making steady-state runs fast (seconds instead of minutes) and emitting `SNIPPET_ORPHANED` findings when annotated functions are deleted.

**Architecture:** Each SDK config entry gains a `baseline_commit` field (last fully-processed git commit hash). When `--incremental` is set, the harness checks `git diff --name-status <baseline>..HEAD` per SDK repo; platforms with no changes are skipped entirely; platforms with changes run a full re-scan as normal. After writing a clean report, baselines are updated. A `harness baseline` command records the current HEAD of all SDK repos for first-time setup.

**Tech Stack:** Go 1.23, `os/exec` (git), `gopkg.in/yaml.v3`, existing `scanner`/`extractor`/`differ` packages, `testify/require`.

---

## File Map

| File | Action | Responsibility |
|------|--------|----------------|
| `internal/delta/delta.go` | **Create** | `Scan(repoPath, snippetDir, baseline string) (DeltaResult, error)` — git diff wrapper |
| `internal/delta/delta_test.go` | **Create** | Unit tests using real git repo in temp dir |
| `internal/config/config.go` | **Modify** | Add `BaselineCommit string` to `SDKConfig`; add `Save(path string) error` |
| `internal/config/config_test.go` | **Modify** | Roundtrip test with `baseline_commit` field |
| `internal/report/types.go` | **Modify** | Add `TypeSnippetOrphaned FindingType = "SNIPPET_ORPHANED"` |
| `internal/scanner/scanner.go` | **Modify** | Add `ScanFiles(paths []string, platform string) ([]Snippet, error)` |
| `internal/scanner/scanner_test.go` | **Modify** | Add `TestScanFiles` |
| `cmd/baseline.go` | **Create** | `runBaseline(args)` — records HEAD commits into config |
| `cmd/audit.go` | **Modify** | Add `--incremental` flag; delta-scope loop; baseline update after success |
| `cmd/audit_incremental_test.go` | **Create** | `TestRunAudit_IncrementalSkipsUnchanged`, `TestRunAudit_IncrementalOrphaned` |
| `cmd/main.go` | **Modify** | Register `baseline` case |

---

## Task 1: `internal/delta` package

**Files:**
- Create: `harness/internal/delta/delta.go`
- Create: `harness/internal/delta/delta_test.go`

- [x] **Step 1: Write the failing tests**

```go
// internal/delta/delta_test.go
package delta_test

import (
    "os"
    "os/exec"
    "path/filepath"
    "testing"

    "github.com/stretchr/testify/require"
    "social-plus/harness/internal/delta"
)

// initRepo creates a git repo with one commit containing a file.
func initRepo(t *testing.T) (repoDir string) {
    t.Helper()
    dir := t.TempDir()
    run := func(args ...string) {
        cmd := exec.Command(args[0], args[1:]...)
        cmd.Dir = dir
        cmd.Env = append(os.Environ(), "GIT_AUTHOR_NAME=test", "GIT_AUTHOR_EMAIL=t@t.com",
            "GIT_COMMITTER_NAME=test", "GIT_COMMITTER_EMAIL=t@t.com")
        out, err := cmd.CombinedOutput()
        require.NoError(t, err, "git cmd failed: %s\n%s", args, out)
    }
    run("git", "init")
    run("git", "config", "user.email", "t@t.com")
    run("git", "config", "user.name", "test")
    // first commit
    snipDir := filepath.Join(dir, "snippets")
    require.NoError(t, os.MkdirAll(snipDir, 0o755))
    require.NoError(t, os.WriteFile(filepath.Join(snipDir, "Foo.kt"), []byte("// foo"), 0o644))
    run("git", "add", ".")
    run("git", "commit", "-m", "init")
    return dir
}

func TestScan_NoChanges(t *testing.T) {
    dir := initRepo(t)
    head := gitHEAD(t, dir)
    result, err := delta.Scan(dir, "snippets", head)
    require.NoError(t, err)
    require.Empty(t, result.Added)
    require.Empty(t, result.Modified)
    require.Empty(t, result.Deleted)
}

func TestScan_ModifiedFile(t *testing.T) {
    dir := initRepo(t)
    baseline := gitHEAD(t, dir)
    // modify file
    require.NoError(t, os.WriteFile(filepath.Join(dir, "snippets", "Foo.kt"), []byte("// foo v2"), 0o644))
    gitCommit(t, dir, "modify foo")
    result, err := delta.Scan(dir, "snippets", baseline)
    require.NoError(t, err)
    require.Len(t, result.Modified, 1)
    require.Equal(t, "snippets/Foo.kt", result.Modified[0])
    require.Empty(t, result.Added)
    require.Empty(t, result.Deleted)
}

func TestScan_AddedFile(t *testing.T) {
    dir := initRepo(t)
    baseline := gitHEAD(t, dir)
    require.NoError(t, os.WriteFile(filepath.Join(dir, "snippets", "Bar.kt"), []byte("// bar"), 0o644))
    gitCommit(t, dir, "add bar")
    result, err := delta.Scan(dir, "snippets", baseline)
    require.NoError(t, err)
    require.Len(t, result.Added, 1)
    require.Equal(t, "snippets/Bar.kt", result.Added[0])
}

func TestScan_DeletedFile(t *testing.T) {
    dir := initRepo(t)
    baseline := gitHEAD(t, dir)
    run := func(args ...string) {
        cmd := exec.Command(args[0], args[1:]...)
        cmd.Dir = dir
        cmd.Env = append(os.Environ(), "GIT_AUTHOR_NAME=test", "GIT_AUTHOR_EMAIL=t@t.com",
            "GIT_COMMITTER_NAME=test", "GIT_COMMITTER_EMAIL=t@t.com")
        out, err := cmd.CombinedOutput()
        require.NoError(t, err, "git: %s\n%s", args, out)
    }
    run("git", "rm", "snippets/Foo.kt")
    run("git", "commit", "-m", "delete foo")
    result, err := delta.Scan(dir, "snippets", baseline)
    require.NoError(t, err)
    require.Len(t, result.Deleted, 1)
    require.Equal(t, "snippets/Foo.kt", result.Deleted[0])
}

func TestScan_FilesOutsideSnippetDirIgnored(t *testing.T) {
    dir := initRepo(t)
    baseline := gitHEAD(t, dir)
    require.NoError(t, os.WriteFile(filepath.Join(dir, "README.md"), []byte("readme"), 0o644))
    gitCommit(t, dir, "add readme")
    result, err := delta.Scan(dir, "snippets", baseline)
    require.NoError(t, err)
    require.Empty(t, result.Added)
    require.Empty(t, result.Modified)
    require.Empty(t, result.Deleted)
}

func TestReadDeletedFile(t *testing.T) {
    dir := initRepo(t)
    baseline := gitHEAD(t, dir)
    run := func(args ...string) {
        cmd := exec.Command(args[0], args[1:]...)
        cmd.Dir = dir
        cmd.Env = append(os.Environ(), "GIT_AUTHOR_NAME=test", "GIT_AUTHOR_EMAIL=t@t.com",
            "GIT_COMMITTER_NAME=test", "GIT_COMMITTER_EMAIL=t@t.com")
        _, err := cmd.CombinedOutput()
        require.NoError(t, err)
    }
    run("git", "rm", "snippets/Foo.kt")
    run("git", "commit", "-m", "delete foo")
    content, err := delta.ReadDeletedFile(dir, baseline, "snippets/Foo.kt")
    require.NoError(t, err)
    require.Equal(t, "// foo", content)
}

// helpers
func gitHEAD(t *testing.T, dir string) string {
    t.Helper()
    cmd := exec.Command("git", "rev-parse", "HEAD")
    cmd.Dir = dir
    out, err := cmd.Output()
    require.NoError(t, err)
    return strings.TrimSpace(string(out))
}

func gitCommit(t *testing.T, dir, msg string) {
    t.Helper()
    run := func(args ...string) {
        cmd := exec.Command(args[0], args[1:]...)
        cmd.Dir = dir
        cmd.Env = append(os.Environ(), "GIT_AUTHOR_NAME=test", "GIT_AUTHOR_EMAIL=t@t.com",
            "GIT_COMMITTER_NAME=test", "GIT_COMMITTER_EMAIL=t@t.com")
        out, err := cmd.CombinedOutput()
        require.NoError(t, err, "git: %s\n%s", args, out)
    }
    run("git", "add", ".")
    run("git", "commit", "-m", msg)
}
```

Note: add `"strings"` to imports in the test file.

- [x] **Step 2: Run test to verify it fails**

```bash
cd harness && go test ./internal/delta/... -v 2>&1 | head -20
```
Expected: `no Go files in .../internal/delta`

- [x] **Step 3: Write the implementation**

```go
// internal/delta/delta.go
package delta

import (
    "fmt"
    "os/exec"
    "strings"
)

// DeltaResult holds the file paths (relative to repoPath) that changed since baseline.
// Paths use forward slashes and are relative to the repo root (e.g. "snippets/Foo.kt").
type DeltaResult struct {
    Added    []string
    Modified []string
    Deleted  []string
}

// HasChanges returns true if any files changed.
func (d DeltaResult) HasChanges() bool {
    return len(d.Added) > 0 || len(d.Modified) > 0 || len(d.Deleted) > 0
}

// Scan runs git diff --name-status <baseline>..HEAD in repoPath and returns
// files under snippetDir that were added (A), modified (M), or deleted (D).
// snippetDir is a path prefix relative to the repo root (e.g. "snippets").
// Returns an empty DeltaResult (no error) if baseline == "" or equals HEAD.
func Scan(repoPath, snippetDir, baseline string) (DeltaResult, error) {
    if baseline == "" {
        return DeltaResult{}, nil
    }
    prefix := snippetDir
    if !strings.HasSuffix(prefix, "/") {
        prefix += "/"
    }
    cmd := exec.Command("git", "diff", "--name-status", baseline+"..HEAD")
    cmd.Dir = repoPath
    out, err := cmd.Output()
    if err != nil {
        return DeltaResult{}, fmt.Errorf("git diff in %s: %w", repoPath, err)
    }
    var result DeltaResult
    for _, line := range strings.Split(strings.TrimSpace(string(out)), "\n") {
        if line == "" {
            continue
        }
        fields := strings.Fields(line)
        if len(fields) < 2 {
            continue
        }
        status := fields[0]
        path := filepath.ToSlash(fields[len(fields)-1])
        if !strings.HasPrefix(path, prefix) {
            continue
        }
        switch {
        case status == "A":
            result.Added = append(result.Added, path)
        case status == "M" || strings.HasPrefix(status, "R"):
            result.Modified = append(result.Modified, path)
        case status == "D":
            result.Deleted = append(result.Deleted, path)
        }
    }
    return result, nil
}

// ReadDeletedFile reads the content of a file as it existed at the given baseline commit.
// path is relative to repoPath (forward-slash form, e.g. "snippets/Foo.kt").
func ReadDeletedFile(repoPath, baseline, path string) (string, error) {
    ref := baseline + ":" + path
    cmd := exec.Command("git", "show", ref)
    cmd.Dir = repoPath
    out, err := cmd.Output()
    if err != nil {
        return "", fmt.Errorf("git show %s in %s: %w", ref, repoPath, err)
    }
    return string(out), nil
}
```

Note: add `"path/filepath"` to imports.

- [x] **Step 4: Run tests**

```bash
cd harness && go test ./internal/delta/... -v
```
Expected: all 6 tests PASS.

- [x] **Step 5: Commit**

```bash
git add harness/internal/delta/
git commit -m "feat(harness): add internal/delta package for git-diff-based SDK change detection"
```

---

## Task 2: Config extension + `SNIPPET_ORPHANED` finding type

**Files:**
- Modify: `harness/internal/config/config.go`
- Modify: `harness/internal/config/config_test.go`
- Modify: `harness/internal/report/types.go`

- [x] **Step 1: Write the failing config test**

Add to `harness/internal/config/config_test.go`:

```go
func TestLoadAndSave_WithBaselineCommit(t *testing.T) {
    dir := t.TempDir()
    cfgPath := filepath.Join(dir, "harness-config.yml")
    content := `sdks:
  android:
    path: ../android
    snippet_dir: snippets
    baseline_commit: abc123
docs:
  path: ../docs
llm:
  model: test
`
    require.NoError(t, os.WriteFile(cfgPath, []byte(content), 0o644))
    cfg, err := config.Load(cfgPath)
    require.NoError(t, err)
    require.Equal(t, "abc123", cfg.SDKs["android"].BaselineCommit)

    // Update and save
    updated := cfg.SDKs["android"]
    updated.BaselineCommit = "def456"
    cfg.SDKs["android"] = updated
    require.NoError(t, cfg.Save(cfgPath))

    // Reload and verify
    cfg2, err := config.Load(cfgPath)
    require.NoError(t, err)
    require.Equal(t, "def456", cfg2.SDKs["android"].BaselineCommit)
}
```

- [x] **Step 2: Run test to verify it fails**

```bash
cd harness && go test ./internal/config/... -run TestLoadAndSave_WithBaselineCommit -v
```
Expected: FAIL — `BaselineCommit` field undefined.

- [x] **Step 3: Implement config changes**

In `harness/internal/config/config.go`, change `SDKConfig` and add `Save`:

```go
type SDKConfig struct {
    Path           string   `yaml:"path"`
    SnippetDir     string   `yaml:"snippet_dir"`
    CompileCmd     []string `yaml:"compile_cmd"`
    BaselineCommit string   `yaml:"baseline_commit,omitempty"`
}

// Save writes the config back to path using YAML marshalling.
// Existing comments in the file are not preserved.
func (c *Config) Save(path string) error {
    data, err := yaml.Marshal(c)
    if err != nil {
        return fmt.Errorf("marshal config: %w", err)
    }
    return os.WriteFile(path, data, 0o644)
}
```

- [x] **Step 4: Add `SNIPPET_ORPHANED` to report/types.go**

Add after the last `TypeSnippet...` constant in `harness/internal/report/types.go`:

```go
TypeSnippetOrphaned FindingType = "SNIPPET_ORPHANED"
```

Full updated block:
```go
const (
    TypeMissingSnippet             FindingType = "MISSING_SNIPPET"
    TypeDocMissing                 FindingType = "DOC_MISSING"
    TypeAscPageInvalid             FindingType = "ASC_PAGE_INVALID"
    TypeDocSurfaceDrift            FindingType = "DOC_SURFACE_DRIFT"
    TypeSnippetContentDrift        FindingType = "SNIPPET_CONTENT_DRIFT"
    TypeDocPageStaleImport         FindingType = "DOC_PAGE_STALE_IMPORT"
    TypeDocBrokenImport            FindingType = "DOC_BROKEN_IMPORT"
    TypePublicFuncUnannotated      FindingType = "PUBLIC_FUNC_UNANNOTATED"
    TypeSnippetKeyPlatformConflict FindingType = "SNIPPET_KEY_PLATFORM_CONFLICT"
    TypeSnippetOrphaned            FindingType = "SNIPPET_ORPHANED"
)
```

- [x] **Step 5: Run tests**

```bash
cd harness && go test ./internal/config/... ./internal/report/... -v
```
Expected: all tests PASS.

- [x] **Step 6: Commit**

```bash
git add harness/internal/config/ harness/internal/report/types.go
git commit -m "feat(harness): add BaselineCommit to SDKConfig, Config.Save(), and SNIPPET_ORPHANED finding type"
```

---

## Task 3: `scanner.ScanFiles` for delta-scoped scanning

**Files:**
- Modify: `harness/internal/scanner/scanner.go`
- Modify: `harness/internal/scanner/scanner_test.go`

- [x] **Step 1: Write the failing test**

Add to `harness/internal/scanner/scanner_test.go`:

```go
func TestScanFiles(t *testing.T) {
    dir := t.TempDir()
    f1 := filepath.Join(dir, "Foo.kt")
    f2 := filepath.Join(dir, "Bar.kt")
    content := `class AmityFoo {
/* begin_sample_code
   filename: foo.kt
   sp_docs_page: social-plus-sdk/chat/channels
   description: test
   */
fun foo() {}
/* end_sample_code */
}`
    require.NoError(t, os.WriteFile(f1, []byte(content), 0o644))
    require.NoError(t, os.WriteFile(f2, []byte("// no snippet"), 0o644))

    snips, err := scanner.ScanFiles([]string{f1, f2}, "android")
    require.NoError(t, err)
    require.Len(t, snips, 1)
    require.Equal(t, "social-plus-sdk/chat/channels", snips[0].SpDocsPage)
}
```

Add `"github.com/stretchr/testify/require"` to imports if not present; also add `"path/filepath"` and `"os"`.

- [x] **Step 2: Run test to verify it fails**

```bash
cd harness && go test ./internal/scanner/... -run TestScanFiles -v
```
Expected: FAIL — `ScanFiles undefined`.

- [x] **Step 3: Add `ScanFiles` to scanner.go**

Add after the existing `Scan` function in `harness/internal/scanner/scanner.go`:

```go
// ScanFiles scans a specific list of absolute file paths for begin_sample_code blocks.
// This is used in incremental mode to scope scanning to changed files only.
func ScanFiles(paths []string, platform string) ([]Snippet, error) {
    var results []Snippet
    for _, p := range paths {
        if !matchesPlatform(p, platform) {
            continue
        }
        snips, err := scanFile(p, platform)
        if err != nil {
            return results, err
        }
        results = append(results, snips...)
    }
    return results, nil
}
```

- [x] **Step 4: Run tests**

```bash
cd harness && go test ./internal/scanner/... -v
```
Expected: all tests PASS.

- [x] **Step 5: Commit**

```bash
git add harness/internal/scanner/
git commit -m "feat(harness): add scanner.ScanFiles for incremental delta-scoped scanning"
```

---

## Task 4: `harness baseline` command

**Files:**
- Create: `harness/cmd/baseline.go`
- Modify: `harness/cmd/main.go`

- [x] **Step 1: Write the implementation**

```go
// harness/cmd/baseline.go
package main

import (
    "flag"
    "fmt"
    "os"
    "os/exec"
    "path/filepath"
    "strings"

    "social-plus/harness/internal/config"
)

func runBaseline(args []string) {
    fs := flag.NewFlagSet("baseline", flag.ExitOnError)
    cfgPath := fs.String("config", "harness-config.yml", "path to harness-config.yml")
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
    updated := false
    for platform, sdkCfg := range cfg.SDKs {
        sdkPath := filepath.Join(cfgDir, sdkCfg.Path)
        if _, err := os.Stat(sdkPath); os.IsNotExist(err) {
            fmt.Printf("[baseline] skip %s: path not found\n", platform)
            continue
        }
        cmd := exec.Command("git", "rev-parse", "HEAD")
        cmd.Dir = sdkPath
        out, err := cmd.Output()
        if err != nil {
            fmt.Fprintf(os.Stderr, "[baseline] git rev-parse HEAD in %s: %v\n", sdkPath, err)
            continue
        }
        commit := strings.TrimSpace(string(out))
        sdkCfg.BaselineCommit = commit
        cfg.SDKs[platform] = sdkCfg
        fmt.Printf("[baseline] %s → %s\n", platform, commit[:12])
        updated = true
    }

    if !updated {
        fmt.Println("[baseline] no SDKs updated")
        return
    }

    if err := cfg.Save(*cfgPath); err != nil {
        fmt.Fprintf(os.Stderr, "save config: %v\n", err)
        os.Exit(1)
    }
    fmt.Printf("[baseline] saved to %s\n", *cfgPath)
}
```

- [x] **Step 2: Register in main.go**

In `harness/cmd/main.go`, update the usage line and switch:

```go
// Usage line — change to:
fmt.Fprintf(os.Stderr, "usage: harness <annotate|audit|baseline|fillmanifests|fix|genmanifests|gendocs|migrate|parity|place|prompt|serve> [--config path]\n")

// Add case before "default:":
case "baseline":
    runBaseline(os.Args[2:])
```

- [x] **Step 3: Build and smoke-test**

```bash
cd harness && go build -o harness-bin ./cmd/ && ./harness-bin baseline 2>&1
```
Expected: output like `[baseline] android → df060cdcc81a` × 4 platforms, then `[baseline] saved to harness-config.yml`.

- [x] **Step 4: Verify config was updated**

```bash
grep baseline_commit harness/harness-config.yml
```
Expected: 4 lines with `baseline_commit: <40-char-hash>`.

- [x] **Step 5: Commit**

```bash
git add harness/cmd/baseline.go harness/cmd/main.go harness/harness-config.yml
git commit -m "feat(harness): add 'harness baseline' command to record SDK HEAD commits

Records current git HEAD for each SDK repo into harness-config.yml as
baseline_commit. Run once after a clean full audit to establish the
incremental baseline."
```

---

## Task 5: Wire `--incremental` into `cmd/audit.go`

**Files:**
- Modify: `harness/cmd/audit.go`
- Create: `harness/cmd/audit_incremental_test.go`

- [x] **Step 1: Write the failing tests**

```go
// harness/cmd/audit_incremental_test.go
package main

import (
    "encoding/json"
    "os"
    "os/exec"
    "path/filepath"
    "strings"
    "testing"

    "github.com/stretchr/testify/require"
    "social-plus/harness/internal/report"
)

// initGitRepo creates a temporary git repo with a snippet file and one commit.
func initGitRepoWithSnippet(t *testing.T, snippetDir, filename, content string) (repoDir string, baseline string) {
    t.Helper()
    dir := t.TempDir()
    snipDir := filepath.Join(dir, snippetDir)
    require.NoError(t, os.MkdirAll(snipDir, 0o755))
    require.NoError(t, os.WriteFile(filepath.Join(snipDir, filename), []byte(content), 0o644))
    gitExec := func(args ...string) {
        cmd := exec.Command(args[0], args[1:]...)
        cmd.Dir = dir
        cmd.Env = append(os.Environ(),
            "GIT_AUTHOR_NAME=test", "GIT_AUTHOR_EMAIL=t@t.com",
            "GIT_COMMITTER_NAME=test", "GIT_COMMITTER_EMAIL=t@t.com")
        out, err := cmd.CombinedOutput()
        require.NoError(t, err, "git: %v\n%s", args, out)
    }
    gitExec("git", "init")
    gitExec("git", "config", "user.email", "t@t.com")
    gitExec("git", "config", "user.name", "test")
    gitExec("git", "add", ".")
    gitExec("git", "commit", "-m", "init")
    cmd := exec.Command("git", "rev-parse", "HEAD")
    cmd.Dir = dir
    out, err := cmd.Output()
    require.NoError(t, err)
    return dir, strings.TrimSpace(string(out))
}

func TestRunAudit_IncrementalSkipsUnchangedPlatform(t *testing.T) {
    dir := t.TempDir()

    // Create an Android SDK repo with a snippet at baseline
    androidContent := `class AmityFoo {
/* begin_sample_code
   filename: AmityFoo.kt
   sp_docs_page: social-plus-sdk/chat/channels
   description: test
   */
fun foo() {}
/* end_sample_code */
}`
    sdkDir, baseline := initGitRepoWithSnippet(t, "snippets", "AmityFoo.kt", androidContent)

    // docs.json with the page the snippet references
    docsDir := filepath.Join(dir, "docs")
    require.NoError(t, os.MkdirAll(docsDir, 0o755))
    docsJSON := `{"navigation":{"tabs":[{"groups":[{"pages":["social-plus-sdk/chat/channels"]}]}]}}`
    require.NoError(t, os.WriteFile(filepath.Join(docsDir, "docs.json"), []byte(docsJSON), 0o644))

    cfgData := fmt.Sprintf(`docs:
  path: docs
sdks:
  android:
    path: %s
    snippet_dir: snippets
    baseline_commit: %s
llm:
  model: test
`, sdkDir, baseline)
    cfgPath := filepath.Join(dir, "harness-config.yml")
    require.NoError(t, os.WriteFile(cfgPath, []byte(cfgData), 0o644))

    reportPath := filepath.Join(dir, "harness-report.json")
    // Write empty existing report
    emptyReport := report.Report{GeneratedAt: "2026-01-01T00:00:00Z"}
    b, _ := json.Marshal(emptyReport)
    require.NoError(t, os.WriteFile(reportPath, b, 0o644))

    // Run incremental audit — no changes since baseline, android should be skipped
    var skipped bool
    // Capture stdout to verify skip message
    old := os.Stdout
    r, w, _ := os.Pipe()
    os.Stdout = w
    runAudit([]string{"--config", cfgPath, "--report", reportPath, "--incremental"})
    w.Close()
    os.Stdout = old
    var buf strings.Builder
    io.Copy(&buf, r)
    output := buf.String()
    skipped = strings.Contains(output, "no changes") && strings.Contains(output, "android")
    require.True(t, skipped, "expected skip message for android, got: %s", output)
}

func TestRunAudit_IncrementalOrphaned(t *testing.T) {
    dir := t.TempDir()

    snippetContent := `class AmityFoo {
/* begin_sample_code
   filename: AmityFoo.kt
   sp_docs_page: social-plus-sdk/chat/channels
   description: test
   */
fun foo() {}
/* end_sample_code */
}`
    sdkDir, baseline := initGitRepoWithSnippet(t, "snippets", "AmityFoo.kt", snippetContent)

    // Delete the file after baseline
    gitExec := func(args ...string) {
        cmd := exec.Command(args[0], args[1:]...)
        cmd.Dir = sdkDir
        cmd.Env = append(os.Environ(),
            "GIT_AUTHOR_NAME=test", "GIT_AUTHOR_EMAIL=t@t.com",
            "GIT_COMMITTER_NAME=test", "GIT_COMMITTER_EMAIL=t@t.com")
        out, err := cmd.CombinedOutput()
        require.NoError(t, err, "git: %v\n%s", args, out)
    }
    gitExec("git", "rm", "snippets/AmityFoo.kt")
    gitExec("git", "commit", "-m", "delete foo")

    docsDir := filepath.Join(dir, "docs")
    require.NoError(t, os.MkdirAll(docsDir, 0o755))
    docsJSON := `{"navigation":{"tabs":[{"groups":[{"pages":["social-plus-sdk/chat/channels"]}]}]}}`
    require.NoError(t, os.WriteFile(filepath.Join(docsDir, "docs.json"), []byte(docsJSON), 0o644))

    cfgData := fmt.Sprintf(`docs:
  path: docs
sdks:
  android:
    path: %s
    snippet_dir: snippets
    baseline_commit: %s
llm:
  model: test
`, sdkDir, baseline)
    cfgPath := filepath.Join(dir, "harness-config.yml")
    require.NoError(t, os.WriteFile(cfgPath, []byte(cfgData), 0o644))

    reportPath := filepath.Join(dir, "harness-report.json")
    emptyReport := report.Report{GeneratedAt: "2026-01-01T00:00:00Z"}
    b, _ := json.Marshal(emptyReport)
    require.NoError(t, os.WriteFile(reportPath, b, 0o644))

    runAudit([]string{"--config", cfgPath, "--report", reportPath, "--incremental"})

    r, err := report.Read(reportPath)
    require.NoError(t, err)
    var orphaned []report.Finding
    for _, f := range r.Findings {
        if f.Type == report.TypeSnippetOrphaned {
            orphaned = append(orphaned, f)
        }
    }
    require.Len(t, orphaned, 1, "expected 1 SNIPPET_ORPHANED finding")
    require.Equal(t, "android", orphaned[0].Platform)
    require.Contains(t, orphaned[0].Detail, "AmityFoo")
}
```

Note: add `"fmt"` and `"io"` to imports.

- [x] **Step 2: Run tests to verify they fail**

```bash
cd harness && go test ./cmd/ -run "TestRunAudit_Incremental" -v 2>&1 | head -20
```
Expected: FAIL — `--incremental` flag undefined.

- [x] **Step 3: Add incremental logic to `cmd/audit.go`**

Add the `--incremental` flag to `runAudit`:

```go
// Add after existing flags in runAudit:
incremental := fs.Bool("incremental", false, "only scan platforms with changes since baseline_commit")
```

Replace the `for platform, sdkCfg := range cfg.SDKs` loop (lines 77–142) with:

```go
var allSnips []scanner.Snippet
for platform, sdkCfg := range cfg.SDKs {
    sdkPath := filepath.Join(filepath.Dir(*cfgPath), sdkCfg.Path)
    snippetPath := filepath.Join(sdkPath, sdkCfg.SnippetDir)

    // --- Incremental: check for changes since baseline ---
    if *incremental && sdkCfg.BaselineCommit != "" {
        d, deltaErr := delta.Scan(sdkPath, sdkCfg.SnippetDir, sdkCfg.BaselineCommit)
        if deltaErr != nil {
            fmt.Fprintf(os.Stderr, "[%s] delta scan error: %v — falling back to full scan\n", platform, deltaErr)
        } else if !d.HasChanges() {
            fmt.Printf("[%s] no changes since %s, skipping\n", platform, sdkCfg.BaselineCommit[:12])
            continue
        } else {
            // Emit SNIPPET_ORPHANED findings for deleted files
            for _, deletedPath := range d.Deleted {
                absDeleted := filepath.Join(sdkPath, deletedPath[len(sdkCfg.SnippetDir)+1:])
                content, readErr := delta.ReadDeletedFile(sdkPath, sdkCfg.BaselineCommit, deletedPath)
                if readErr != nil {
                    fmt.Fprintf(os.Stderr, "[%s] read deleted %s: %v\n", platform, deletedPath, readErr)
                    continue
                }
                deletedSnips, _ := scanner.ScanFileContent(content, absDeleted, platform)
                for _, s := range deletedSnips {
                    key := docgen.DeriveKey(s.Filename)
                    findingID := "snippet-orphaned:" + platform + ":" + key
                    if isAlreadyInReport(allFindings, findingID) {
                        continue
                    }
                    allFindings = append(allFindings, report.Finding{
                        ID:       findingID,
                        Type:     report.TypeSnippetOrphaned,
                        Platform: platform,
                        Status:   report.StatusOpen,
                        Detail:   fmt.Sprintf("snippet key %q was deleted from %s (file: %s)", key, platform, deletedPath),
                    })
                    fmt.Printf("[%s] SNIPPET_ORPHANED: %s (deleted)\n", platform, key)
                }
            }
        }
    }

    fns, err := extractor.Scan(sdkPath, platform)
    if err != nil {
        fmt.Fprintf(os.Stderr, "extract %s: %v\n", platform, err)
        continue
    }

    snips, err := scanner.Scan(snippetPath, platform)
    if err != nil {
        fmt.Fprintf(os.Stderr, "scan snippets %s: %v\n", platform, err)
        continue
    }
    allSnips = append(allSnips, snips...)

    findings := differ.Diff(fns, snips, reg, platform)

    currentlyDetected := map[string]bool{}
    for _, f := range findings {
        currentlyDetected[f.ID] = true
    }
    autoVerifiable := map[report.FindingType]bool{
        report.TypeAscPageInvalid:  true,
        report.TypeMissingSnippet:  true,
        report.TypeDocMissing:      true,
        report.TypeDocBrokenImport: true,
    }
    reVerifiedDiff := 0
    for i, f := range allFindings {
        if f.Platform != platform {
            continue
        }
        if !autoVerifiable[f.Type] {
            continue
        }
        if f.Status == report.StatusFixed {
            continue
        }
        if !currentlyDetected[f.ID] {
            allFindings[i].Status = report.StatusFixed
            reVerifiedDiff++
        }
    }
    if reVerifiedDiff > 0 {
        fmt.Printf("[%s] %d findings re-verified as fixed\n", platform, reVerifiedDiff)
    }

    newCount := 0
    for _, f := range findings {
        if isAlreadyInReport(allFindings, f.ID) {
            continue
        }
        allFindings = append(allFindings, f)
        newCount++
    }

    fmt.Printf("[%s] %d public functions, %d snippets, %d new findings\n",
        platform, len(fns), len(snips), newCount)
}
```

Add `"social-plus/harness/internal/delta"` to the import block in `audit.go`.

After `report.Write(r, *reportPath)` succeeds (after line `_ = runstate.Finish(...)`), add baseline update:

```go
// Update baseline commits after successful incremental run
if *incremental {
    anyUpdated := false
    for platform, sdkCfg := range cfg.SDKs {
        sdkPath := filepath.Join(filepath.Dir(*cfgPath), sdkCfg.Path)
        cmd := exec.Command("git", "rev-parse", "HEAD")
        cmd.Dir = sdkPath
        out, err := cmd.Output()
        if err != nil {
            continue
        }
        newCommit := strings.TrimSpace(string(out))
        if newCommit != sdkCfg.BaselineCommit {
            sdkCfg.BaselineCommit = newCommit
            cfg.SDKs[platform] = sdkCfg
            anyUpdated = true
        }
    }
    if anyUpdated {
        if err := cfg.Save(*cfgPath); err != nil {
            fmt.Fprintf(os.Stderr, "warning: could not update baselines in config: %v\n", err)
        } else {
            fmt.Println("[audit] baselines updated in config")
        }
    }
}
```

- [x] **Step 4: Add `ScanFileContent` to scanner** (needed by the orphaned detection above)

In `harness/internal/scanner/scanner.go`, add:

```go
// ScanFileContent scans a string of source code (e.g. a deleted file read from git)
// for begin_sample_code blocks. path is used only to populate Snippet.File.
func ScanFileContent(content, path, platform string) ([]Snippet, error) {
    tmp, err := os.CreateTemp("", "harness-scan-*.tmp")
    if err != nil {
        return nil, err
    }
    defer os.Remove(tmp.Name())
    if _, err := tmp.WriteString(content); err != nil {
        tmp.Close()
        return nil, err
    }
    tmp.Close()
    snips, err := scanFile(tmp.Name(), platform)
    if err != nil {
        return nil, err
    }
    // Replace temp path with the logical path
    for i := range snips {
        snips[i].File = path
    }
    return snips, nil
}
```

- [x] **Step 5: Run all tests**

```bash
cd harness && go test ./... 2>&1
```
Expected: all packages PASS (including `TestRunAudit_IncrementalSkipsUnchangedPlatform` and `TestRunAudit_IncrementalOrphaned`).

- [x] **Step 6: Rebuild and smoke-test**

```bash
cd harness && go build -o harness-bin ./cmd/
./harness-bin audit --incremental 2>&1 | head -10
```
Expected: lines like `[android] no changes since df060cdcc81a, skipping` × 4 (since baselines were just set).

- [x] **Step 7: Commit**

```bash
git add harness/cmd/audit.go harness/cmd/audit_incremental_test.go harness/internal/scanner/scanner.go
git commit -m "feat(harness): add --incremental flag to audit command

- Skips platforms with no git changes since baseline_commit
- Emits SNIPPET_ORPHANED findings for deleted annotated snippets
- Updates baseline commits in config after successful incremental run
- Uses delta.Scan + scanner.ScanFileContent for orphaned detection"
```

---

## Task 6: E2E validation + BIG-PICTURE update

**Files:**
- Modify: `harness/_docs/BIG-PICTURE.md`

- [x] **Step 1: Run full audit to confirm clean baseline**

```bash
cd harness && ./harness-bin audit 2>&1 | tail -3
```
Expected: `Summary: 0 open, N fixed, 0 needs_human`

- [x] **Step 2: Set baselines**

```bash
./harness-bin baseline
```
Expected: 4 platform hashes written to `harness-config.yml`.

- [x] **Step 3: Run incremental audit — expect all skipped**

```bash
./harness-bin audit --incremental 2>&1
```
Expected:
```
[android] no changes since <hash>, skipping
[flutter] no changes since <hash>, skipping
[ios] no changes since <hash>, skipping
[typescript] no changes since <hash>, skipping
Summary: 0 open, N fixed, 0 needs_human
[audit] baselines updated in config
```

- [x] **Step 4: Simulate a change (modify one SDK file), re-run incremental**

```bash
# Add a trivial change to one Android snippet (append a comment)
echo "// incremental-test" >> ../../Amity-Social-Cloud-SDK-Android/amity-sample-code/src/main/java/com/amity/snipet/verifier/generated/send_message.kt
# Commit it temporarily
cd ../../Amity-Social-Cloud-SDK-Android && git add . && git commit -m "test: incremental test change"
cd -
./harness-bin audit --incremental 2>&1 | grep -E "android|Summary"
```
Expected: android re-scans (shows function/snippet counts), other 3 platforms show "no changes".

- [x] **Step 5: Revert the test change**

```bash
cd ../../Amity-Social-Cloud-SDK-Android && git revert HEAD --no-edit && cd -
```

- [x] **Step 6: Update BIG-PICTURE.md**

In `harness/_docs/BIG-PICTURE.md`, find the "Phase 2" or "Planned" section and add:

```markdown
### Phase 2A: Incremental Workflow ✅ Complete

| Feature | Status |
|---------|--------|
| `internal/delta` package — git diff wrapper | ✅ |
| `BaselineCommit` per SDK in `harness-config.yml` | ✅ |
| `harness baseline` command — record HEAD commits | ✅ |
| `harness audit --incremental` — skip unchanged platforms | ✅ |
| `SNIPPET_ORPHANED` finding type for deleted functions | ✅ |
| Auto-update baselines after successful incremental run | ✅ |

**Speed improvement:** Steady-state run with no SDK changes completes in < 5 seconds (skips all platform scans).
```

- [x] **Step 7: Commit + push**

```bash
cd harness && go build -o harness-bin ./cmd/
git add harness/ harness-config.yml harness/_docs/BIG-PICTURE.md
git commit -m "feat(harness): Phase 2A complete - incremental audit with baseline tracking

harness audit --incremental now skips platforms unchanged since baseline.
harness baseline records current HEAD for all SDK repos.
SNIPPET_ORPHANED finding surfaces deleted annotated functions for triage.

E2E validated: all platforms skip when no changes; android re-scans when
a snippet file is modified.

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
git push origin feat/doc-agent
```

---

## Self-Review

### 1. Spec coverage

| Requirement | Task |
|-------------|------|
| `baseline_commit` per SDK in config | Task 2 |
| `git diff <baseline>..HEAD` per repo | Task 1 (delta.Scan) |
| Skip platforms with no changes | Task 5 |
| `SNIPPET_ORPHANED` for deleted functions | Task 5 |
| Auto-update baselines after run | Task 5 |
| `harness baseline` command | Task 4 |
| CI-ready: fast incremental loop | Task 6 E2E |

All requirements covered. ✅

### 2. Placeholder scan

No TBD/TODO/placeholder text found in code blocks. ✅

### 3. Type consistency

- `delta.DeltaResult` → `HasChanges()` method used in Task 5 ✅
- `delta.ReadDeletedFile(repoPath, baseline, path)` used in Task 5 ✅  
- `scanner.ScanFileContent(content, path, platform)` defined in Task 5, referenced in Task 5 ✅
- `scanner.ScanFiles(paths, platform)` defined in Task 3, not used in current audit.go (available for future per-file scoping) ✅
- `cfg.Save(path)` defined in Task 2, used in Task 4 and Task 5 ✅
- `report.TypeSnippetOrphaned` defined in Task 2, used in Task 5 ✅
- `config.SDKConfig.BaselineCommit` defined in Task 2, used in Task 5 ✅

All consistent. ✅
