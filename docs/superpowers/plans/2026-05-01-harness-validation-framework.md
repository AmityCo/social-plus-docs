# Harness Validation Framework Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the three-gate harness validation framework: add `SNIPPET_KEY_PLATFORM_CONFLICT` finding (Gate 1), wire Gate 2 confidence signal into annotate output, and surface platform coverage metrics in the dashboard.

**Architecture:** Gate 1 is a new `DiffSnippetKeyConflicts` function in `differ.go` that checks all snippet groups for cross-platform `sp_docs_page` disagreement. Gate 2 adds a confidence field to annotate output and routes low-confidence results to `needs_human`. The coverage dashboard widget reads per-platform counts from the manifest.

**Tech Stack:** Go (harness), existing `differ`, `report`, `docgen`, `scanner` packages, `harness-bin` CLI, `dashboard.html`.

---

## File Map

| File | Change |
|---|---|
| `harness/internal/report/types.go` | Add `TypeSnippetKeyPlatformConflict` constant |
| `harness/internal/differ/differ.go` | Add `DiffSnippetKeyConflicts(snips []scanner.Snippet) []report.Finding` |
| `harness/internal/differ/differ_test.go` | Tests for `DiffSnippetKeyConflicts` |
| `harness/cmd/audit.go` | Call `DiffSnippetKeyConflicts` after building `allGroups` |
| `harness/cmd/dashboard.html` | Add platform coverage widget (4-bar chart) |
| `harness/cmd/serve.go` | Add `/api/coverage` endpoint returning per-platform counts |

---

## Task 1: Add `SNIPPET_KEY_PLATFORM_CONFLICT` finding type

**Files:**
- Modify: `harness/internal/report/types.go`

- [ ] **Step 1: Add the constant**

Open `harness/internal/report/types.go`. After line 13 (`TypePublicFuncUnannotated`), add:

```go
TypeSnippetKeyPlatformConflict FindingType = "SNIPPET_KEY_PLATFORM_CONFLICT"
```

- [ ] **Step 2: Build to verify no errors**

```bash
cd social-plus-docs/harness && go build ./...
```

Expected: no output (clean build).

- [ ] **Step 3: Commit**

```bash
git add harness/internal/report/types.go
git commit -m "feat(audit): add SNIPPET_KEY_PLATFORM_CONFLICT finding type"
```

---

## Task 2: Implement `DiffSnippetKeyConflicts`

**Files:**
- Modify: `harness/internal/differ/differ.go`
- Modify: `harness/internal/differ/differ_test.go`

- [ ] **Step 1: Write failing test**

In `harness/internal/differ/differ_test.go`, add:

```go
func TestDiffSnippetKeyConflicts_NoConflict(t *testing.T) {
    snips := []scanner.Snippet{
        {Filename: "AmityPostGet.kt",   Platform: "android",    SpDocsPage: "social-plus-sdk/social/post-get"},
        {Filename: "AmityPostGet.swift", Platform: "ios",       SpDocsPage: "social-plus-sdk/social/post-get"},
        {Filename: "AmityPostGet.dart",  Platform: "flutter",   SpDocsPage: "social-plus-sdk/social/post-get"},
    }
    findings := DiffSnippetKeyConflicts(snips)
    if len(findings) != 0 {
        t.Fatalf("expected 0 findings, got %d: %+v", len(findings), findings)
    }
}

func TestDiffSnippetKeyConflicts_Conflict(t *testing.T) {
    snips := []scanner.Snippet{
        {Filename: "AmityAdQuery.kt",    Platform: "android", SpDocsPage: "social-plus-sdk/social/notification-items"},
        {Filename: "AmityAdQuery.swift", Platform: "ios",     SpDocsPage: "social-plus-sdk/core-concepts/ads"},
    }
    findings := DiffSnippetKeyConflicts(snips)
    if len(findings) != 1 {
        t.Fatalf("expected 1 finding, got %d", len(findings))
    }
    if findings[0].Type != report.TypeSnippetKeyPlatformConflict {
        t.Errorf("expected TypeSnippetKeyPlatformConflict, got %s", findings[0].Type)
    }
    if !strings.Contains(findings[0].Detail, "ad-query") {
        t.Errorf("detail should mention key, got: %s", findings[0].Detail)
    }
    if !strings.Contains(findings[0].Detail, "android") || !strings.Contains(findings[0].Detail, "ios") {
        t.Errorf("detail should mention both platforms, got: %s", findings[0].Detail)
    }
}

func TestDiffSnippetKeyConflicts_SkipBlankPage(t *testing.T) {
    snips := []scanner.Snippet{
        {Filename: "AmityPostGet.kt",    Platform: "android", SpDocsPage: "social-plus-sdk/social/post-get"},
        {Filename: "AmityPostGet.swift", Platform: "ios",     SpDocsPage: ""},
    }
    findings := DiffSnippetKeyConflicts(snips)
    if len(findings) != 0 {
        t.Fatalf("expected 0 findings (blank page skipped), got %d", len(findings))
    }
}
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd social-plus-docs/harness && go test ./internal/differ/... -run TestDiffSnippetKeyConflicts -v
```

Expected: `FAIL — DiffSnippetKeyConflicts undefined`

- [ ] **Step 3: Implement `DiffSnippetKeyConflicts` in `differ.go`**

Add this function at the end of `harness/internal/differ/differ.go` (before the final closing brace of the package, after `DiffDocPages`):

```go
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
		var conflicts []string
		for _, e := range entries {
			if e.page != canonical {
				conflicts = append(conflicts, e.platform)
			}
		}
		if len(conflicts) == 0 {
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
	return findings
}
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
cd social-plus-docs/harness && go test ./internal/differ/... -run TestDiffSnippetKeyConflicts -v
```

Expected:
```
--- PASS: TestDiffSnippetKeyConflicts_NoConflict
--- PASS: TestDiffSnippetKeyConflicts_Conflict
--- PASS: TestDiffSnippetKeyConflicts_SkipBlankPage
PASS
```

- [ ] **Step 5: Run full test suite to ensure no regressions**

```bash
cd social-plus-docs/harness && go test ./... 2>&1 | tail -20
```

Expected: all pass (or same pre-existing failures as baseline).

- [ ] **Step 6: Commit**

```bash
git add harness/internal/differ/differ.go harness/internal/differ/differ_test.go
git commit -m "feat(audit): implement DiffSnippetKeyConflicts for Gate 1 key alignment"
```

---

## Task 3: Wire `DiffSnippetKeyConflicts` into `audit`

**Files:**
- Modify: `harness/cmd/audit.go`

- [ ] **Step 1: Add the call after `allGroups` is built**

In `harness/cmd/audit.go`, find the block starting with `allGroups := docgen.GroupSnippets(allSnips)` (around line 120). Add the conflict check immediately after:

```go
allGroups := docgen.GroupSnippets(allSnips)

// Gate 1: check for cross-platform sp_docs_page conflicts on same key
{
    conflictFindings := differ.DiffSnippetKeyConflicts(allSnips)
    conflictCount := 0
    for _, f := range conflictFindings {
        if !isAlreadyInReport(allFindings, f.ID) {
            allFindings = append(allFindings, f)
            conflictCount++
        }
    }
    if conflictCount > 0 {
        fmt.Printf("[audit] %d SNIPPET_KEY_PLATFORM_CONFLICT findings\n", conflictCount)
    }
}
```

- [ ] **Step 2: Build**

```bash
cd social-plus-docs/harness && go build ./...
```

Expected: clean.

- [ ] **Step 3: Run audit and check for conflict findings**

```bash
cd social-plus-docs/harness && ./harness-bin audit --config harness-config.yml 2>&1 | tail -8
```

Expected: shows `N SNIPPET_KEY_PLATFORM_CONFLICT findings` (if any exist in current SDK state) plus existing summary. Any conflicts found are real issues to fix in SDK source files.

- [ ] **Step 4: Commit**

```bash
git add harness/cmd/audit.go harness/harness-bin
git commit -m "feat(audit): wire SNIPPET_KEY_PLATFORM_CONFLICT into audit pipeline (Gate 1)"
```

---

## Task 4: Gate 2 — Confidence signal in `annotate` output

**Files:**
- Modify: `harness/cmd/annotate.go`

The `annotate` command currently produces findings with status `needs_human`. Gate 2 logic: if the LLM-suggested annotation produces a key that matches an existing sibling platform's key for the same `sp_docs_page`, promote to a higher-confidence status (still `needs_human` for safety, but with a detail flag indicating auto-approvable).

- [ ] **Step 1: Find where annotate sets finding status**

```bash
grep -n "needs_human\|NeedsHuman\|StatusFixed" social-plus-docs/harness/cmd/annotate.go | head -20
```

Note the line numbers for the status assignment logic.

- [ ] **Step 2: Add a helper to check key alignment**

In `harness/cmd/annotate.go`, after the imports block, add:

```go
// annotateConfidence returns "high" if the suggested sp_docs_page for the given
// filename would produce a key that already exists in allGroups with the same page.
// Returns "low" otherwise (no sibling to confirm against, or page conflicts).
func annotateConfidence(filename, suggestedPage string, allGroups map[string]docgen.SnippetGroup) string {
	key := docgen.DeriveKey(filename)
	if key == "" {
		return "low"
	}
	g, exists := allGroups[key]
	if !exists {
		return "low" // no sibling platform has this key yet
	}
	if g.SpDocsPage == suggestedPage {
		return "high" // sibling agrees on same page
	}
	return "low" // conflict
}
```

- [ ] **Step 3: Thread `allGroups` into the annotate finding detail**

Find the section in `annotate.go` where findings are created after LLM suggestion. Update the `Detail` field to include the confidence:

```go
confidence := annotateConfidence(fn.Filename, suggestedPage, allGroups)
detail := fmt.Sprintf("[confidence:%s] suggested sp_docs_page: %s", confidence, suggestedPage)
```

Update the finding status: keep `needs_human` for both (human still reviews), but the `[confidence:high]` prefix lets the dashboard and human reviewer know which ones are safe to bulk-approve.

- [ ] **Step 4: Ensure `allGroups` is available in the annotate flow**

Check if `annotate.go` already calls `docgen.GroupSnippets`. If not, add before the annotation loop:

```go
allGroups := docgen.GroupSnippets(allSnips) // allSnips collected from all platforms
```

- [ ] **Step 5: Build and test**

```bash
cd social-plus-docs/harness && go build ./... && echo "OK"
```

Expected: `OK`

- [ ] **Step 6: Commit**

```bash
git add harness/cmd/annotate.go
git commit -m "feat(annotate): add Gate 2 confidence signal to annotation findings"
```

---

## Task 5: Platform coverage endpoint and dashboard widget

**Files:**
- Modify: `harness/cmd/serve.go`
- Modify: `harness/cmd/dashboard.html`

- [ ] **Step 1: Add `/api/coverage` endpoint in `serve.go`**

Find the route registration section in `serve.go`. Add:

```go
http.HandleFunc("/api/coverage", func(w http.ResponseWriter, r *http.Request) {
    cfg, err := config.Load(cfgPath)
    if err != nil {
        http.Error(w, err.Error(), 500)
        return
    }
    cfgDir := filepath.Dir(cfgPath)
    var allSnips []scanner.Snippet
    for platform, sdkCfg := range cfg.SDKs {
        snippetPath := filepath.Join(cfgDir, sdkCfg.Path, sdkCfg.SnippetDir)
        snips, _ := scanner.Scan(snippetPath, platform)
        allSnips = append(allSnips, snips...)
    }
    groups := docgen.GroupSnippets(allSnips)
    type platformStat struct {
        Platform string `json:"platform"`
        Count    int    `json:"count"`
        Total    int    `json:"total"`
        Pct      int    `json:"pct"`
    }
    platforms := []string{"android", "ios", "flutter", "typescript"}
    total := len(groups)
    var stats []platformStat
    for _, p := range platforms {
        count := 0
        for _, g := range groups {
            if _, ok := g.Snippets[p]; ok {
                count++
            }
        }
        pct := 0
        if total > 0 {
            pct = count * 100 / total
        }
        stats = append(stats, platformStat{Platform: p, Count: count, Total: total, Pct: pct})
    }
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(stats)
})
```

- [ ] **Step 2: Build to verify**

```bash
cd social-plus-docs/harness && go build ./... && echo "OK"
```

Expected: `OK`

- [ ] **Step 3: Add coverage widget to `dashboard.html`**

In `dashboard.html`, find the metrics cards section (the `<div>` containing platform/finding counts). Add a new card after the existing summary cards:

```html
<!-- Platform Coverage Widget -->
<div id="coverage-card" class="card" style="grid-column: 1 / -1;">
  <h3>Platform Coverage</h3>
  <div id="coverage-bars" style="display:flex; gap:2rem; align-items:flex-end; height:120px; padding:1rem 0;">
    <!-- populated by JS -->
  </div>
  <div id="coverage-legend" style="display:flex; gap:2rem; font-size:0.85rem; color:#666;"></div>
</div>
```

Then in the `<script>` section, add a fetch to populate it:

```javascript
async function loadCoverage() {
  const res = await fetch('/api/coverage');
  const stats = await res.json();
  const colors = { android: '#a4c639', ios: '#555', flutter: '#54c5f8', typescript: '#3178c6' };
  const barsEl = document.getElementById('coverage-bars');
  const legendEl = document.getElementById('coverage-legend');
  barsEl.innerHTML = '';
  legendEl.innerHTML = '';
  stats.forEach(s => {
    const bar = document.createElement('div');
    bar.style.cssText = `display:flex;flex-direction:column;align-items:center;gap:4px;`;
    bar.innerHTML = `
      <span style="font-size:0.8rem;font-weight:600;">${s.pct}%</span>
      <div style="width:48px;height:${Math.max(s.pct, 2)}px;background:${colors[s.platform]||'#999'};border-radius:4px 4px 0 0;transition:height 0.3s;"></div>
    `;
    barsEl.appendChild(bar);
    legendEl.innerHTML += `<span><span style="display:inline-block;width:10px;height:10px;background:${colors[s.platform]||'#999'};border-radius:2px;margin-right:4px;"></span>${s.platform}: ${s.count}/${s.total}</span>`;
  });
}
loadCoverage();
```

- [ ] **Step 4: Start the dashboard and verify visually**

```bash
cd social-plus-docs/harness && ./harness-bin serve --config harness-config.yml &
sleep 2 && curl -s http://localhost:8080/api/coverage | python3 -m json.tool
```

Expected: JSON array with `platform`, `count`, `total`, `pct` for each of the 4 platforms matching the values from our coverage analysis (android ~52%, ios ~47%, flutter ~37%, typescript ~18%).

- [ ] **Step 5: Kill the server and commit**

```bash
kill $(lsof -t -i:8080) 2>/dev/null; true
git add harness/cmd/serve.go harness/cmd/dashboard.html harness/harness-bin
git commit -m "feat(dashboard): add platform coverage widget and /api/coverage endpoint"
```

---

## Task 6: Run full audit and verify Gate 1 in CI

- [ ] **Step 1: Run full audit**

```bash
cd social-plus-docs/harness && ./harness-bin audit --config harness-config.yml 2>&1
```

Expected output includes any `SNIPPET_KEY_PLATFORM_CONFLICT` findings. These are real SDK annotation conflicts to be fixed.

- [ ] **Step 2: For each conflict found, fix the SDK source**

For each `SNIPPET_KEY_PLATFORM_CONFLICT` finding, open the SDK source files for both platforms and align their `sp_docs_page` to the same value (prefer the Android page per deterministic sort convention):

```bash
# Example: find the conflicting files
grep -r "sp_docs_page:" /path/to/sdk/snippet_dir --include="*.kt" --include="*.swift" --include="*.dart" | grep "conflicting-key"
```

Edit the non-android file to match android's `sp_docs_page`.

- [ ] **Step 3: Re-run gendocs + audit to confirm 0 open**

```bash
cd social-plus-docs/harness && ./harness-bin gendocs --config harness-config.yml && ./harness-bin audit --config harness-config.yml 2>&1 | tail -4
```

Expected: `Summary: 0 open, N fixed, M needs_human`

- [ ] **Step 4: Commit all SDK + docs fixes**

```bash
# In SDK repos:
cd /path/to/AmitySDKIOS && git add -A && git commit -m "fix: align sp_docs_page for conflicting snippet keys"
# In docs repo:
cd social-plus-docs && git add -A && git commit -m "fix: resolve SNIPPET_KEY_PLATFORM_CONFLICT findings, 0 open audit"
```

---

## Verification Checklist

After all tasks complete:

- [ ] `go test ./...` passes in `harness/`
- [ ] `DiffSnippetKeyConflicts` test coverage: no-conflict, conflict, blank-page-skip
- [ ] `audit` output shows `SNIPPET_KEY_PLATFORM_CONFLICT` count when conflicts exist
- [ ] `audit` shows `0 open` when all conflicts resolved
- [ ] `/api/coverage` returns valid JSON for all 4 platforms
- [ ] Dashboard coverage widget renders 4 bars with correct percentages
- [ ] `[confidence:high]` appears in annotate finding detail when key matches sibling
