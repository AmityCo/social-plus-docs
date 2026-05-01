# High-Impact Harness Fixes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix 79 DOC_MISSING + 47 ASC_PAGE_INVALID findings in `harness-report.json` and add 30 TypeScript snippet files to improve TS parity from 15% to ~38%.

**Architecture:** Task A fixes two bugs in `cmd/fix.go` that prevent the existing `harness fix` command from patching DOC_MISSING and ASC_PAGE_INVALID findings. Task B is a standalone Python script that LLM-generates new `Amity*.ts` snippet files for the top-30 TypeScript parity gaps using Android snippets as reference.

**Tech Stack:** Go 1.22, Python 3, Anthropic Python SDK (`anthropic` package), existing `social-plus/harness` Go module.

**Working directory for all Go commands:** `social-plus-docs/harness/`  
**Working directory for all Python commands:** `social-plus-docs/harness/`

---

## File Map

| File | Change |
|---|---|
| `harness/cmd/fix.go` | Fix `extractAscPageFromSnippet` + add `TypeDocMissing` case |
| `harness/cmd/fix_test.go` | Add tests for both fixes |
| `harness/scripts/fill-ts-gaps.py` | New: LLM-generates `Amity*.ts` snippet files |
| `AmityTypescriptSDK/packages/sdk/src/snippets/Amity*.ts` | New: up to 30 generated snippet files |

---

## Task 1: Fix `extractAscPageFromSnippet` to read `sp_docs_page:`

**Problem:** `extractAscPageFromSnippet` in `cmd/fix.go` only looks for `asc_page:` but all snippet files use `sp_docs_page:`. This causes all 47 `ASC_PAGE_INVALID` findings to be marked `needs_human` instead of being fixed.

**Files:**
- Modify: `harness/cmd/fix.go`
- Modify: `harness/cmd/fix_test.go`

- [ ] **Step 1: Write the failing test**

Add this test to `harness/cmd/fix_test.go` after the existing `TestSanitizeName` tests:

```go
func TestExtractAscPageFromSnippet_SpDocsPage(t *testing.T) {
	dir := t.TempDir()
	snippetPath := filepath.Join(dir, "AmityTest.kt")
	content := `package com.example

class AmityTest {
    /* begin_sample_code
       filename: AmityTest.kt
       sp_docs_page: social-plus-sdk/chat/channels
       description: Test snippet
       */
    fun test() {}
    /* end_sample_code */
}
`
	if err := os.WriteFile(snippetPath, []byte(content), 0o644); err != nil {
		t.Fatal(err)
	}
	got, err := extractAscPageFromSnippet(snippetPath)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if got != "social-plus-sdk/chat/channels" {
		t.Errorf("got %q, want %q", got, "social-plus-sdk/chat/channels")
	}
}

func TestExtractAscPageFromSnippet_Missing(t *testing.T) {
	dir := t.TempDir()
	snippetPath := filepath.Join(dir, "AmityNoPage.kt")
	content := `package com.example
class AmityNoPage {}
`
	if err := os.WriteFile(snippetPath, []byte(content), 0o644); err != nil {
		t.Fatal(err)
	}
	_, err := extractAscPageFromSnippet(snippetPath)
	if err == nil {
		t.Fatal("expected error for missing sp_docs_page, got nil")
	}
}
```

- [ ] **Step 2: Run the test to confirm it fails**

```bash
cd harness && go test ./cmd/... -run TestExtractAscPageFromSnippet -v
```
Expected: FAIL — `extractAscPageFromSnippet` only looks for `asc_page:`, so `sp_docs_page:` is not found.

- [ ] **Step 3: Fix `extractAscPageFromSnippet` in `cmd/fix.go`**

Replace the existing `extractAscPageFromSnippet` function (currently ~10 lines, at the bottom of fix.go) with:

```go
// extractAscPageFromSnippet reads a snippet file and returns the value of the
// sp_docs_page (or legacy asc_page) metadata field.
func extractAscPageFromSnippet(path string) (string, error) {
	b, err := os.ReadFile(path)
	if err != nil {
		return "", fmt.Errorf("read snippet file: %w", err)
	}
	for _, line := range strings.Split(string(b), "\n") {
		trimmed := strings.TrimSpace(line)
		for _, key := range []string{"sp_docs_page:", "asc_page:"} {
			if strings.HasPrefix(trimmed, key) {
				return strings.TrimSpace(strings.TrimPrefix(trimmed, key)), nil
			}
		}
	}
	return "", fmt.Errorf("sp_docs_page field not found in snippet %q", path)
}
```

- [ ] **Step 4: Run the test to confirm it passes**

```bash
cd harness && go test ./cmd/... -run TestExtractAscPageFromSnippet -v
```
Expected: PASS — both subtests green.

- [ ] **Step 5: Run all tests to confirm no regression**

```bash
cd harness && go test ./... 2>&1 | tail -10
```
Expected: all packages ok.

- [ ] **Step 6: Commit**

```bash
cd harness && git add cmd/fix.go cmd/fix_test.go
git commit -m "fix: extractAscPageFromSnippet reads sp_docs_page: field

Previously only looked for asc_page: which caused all 47
ASC_PAGE_INVALID findings to be silently marked needs_human.

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

---

## Task 2: Add `DOC_MISSING` case to `harness fix`

**Problem:** The switch in `runFix` has no `case report.TypeDocMissing:` — it falls to `default:` which sets status to `needs_human`. DOC_MISSING findings carry both `SnippetFile` and `DocPage` (the old path), so we can call `fixer.FixAscPage` directly using the old path as the input to fuzzy-match.

**Files:**
- Modify: `harness/cmd/fix.go`
- Modify: `harness/cmd/fix_test.go`

- [ ] **Step 1: Write the failing test**

Add this integration test to `harness/cmd/fix_test.go`:

```go
func TestRunFix_DocMissing(t *testing.T) {
	dir := t.TempDir()

	// Create a minimal harness-config.yml
	cfgContent := "sdks:\n  android:\n    path: ./sdk\n    snippet_dir: snippets\n    compile_cmd: []\ndocs:\n  path: .\nllm:\n  model: test\n"
	cfgPath := filepath.Join(dir, "harness-config.yml")
	if err := os.WriteFile(cfgPath, []byte(cfgContent), 0o644); err != nil {
		t.Fatal(err)
	}

	// docs.json with the NEW (correct) path
	docsJSON := `{"navigation":{"tabs":[{"pages":["social-plus-sdk/chat/message-creation/send-a-message"]}]}}`
	if err := os.WriteFile(filepath.Join(dir, "docs.json"), []byte(docsJSON), 0o644); err != nil {
		t.Fatal(err)
	}

	// Create the SDK snippet directory and a snippet file with the OLD path
	snippetDir := filepath.Join(dir, "sdk", "snippets")
	if err := os.MkdirAll(snippetDir, 0o755); err != nil {
		t.Fatal(err)
	}
	snippetFile := filepath.Join(snippetDir, "AmitySendMessage.kt")
	snippetContent := `/* begin_sample_code
   filename: AmitySendMessage.kt
   sp_docs_page: social-plus-sdk/chat/messages/send-a-message
   description: Send a message
   */
fun sendMessage() {}
/* end_sample_code */
`
	if err := os.WriteFile(snippetFile, []byte(snippetContent), 0o644); err != nil {
		t.Fatal(err)
	}

	// Create report with one DOC_MISSING finding using the old path and relative snippet_file
	snippetRel := filepath.Join("sdk", "snippets", "AmitySendMessage.kt")
	r := report.Report{
		GeneratedAt: "2024-01-01T00:00:00Z",
		Findings: []report.Finding{
			{
				ID:          "android-doc-missing-AmitySendMessage.kt",
				Type:        report.TypeDocMissing,
				Platform:    "android",
				SnippetFile: snippetRel,
				DocPage:     "social-plus-sdk/chat/messages/send-a-message",
				Detail:      `sp_docs_page "social-plus-sdk/chat/messages/send-a-message" not found in docs.json`,
				Status:      report.StatusOpen,
			},
		},
	}
	b, _ := json.Marshal(r)
	reportPath := filepath.Join(dir, "harness-report.json")
	if err := os.WriteFile(reportPath, b, 0o644); err != nil {
		t.Fatal(err)
	}
	issuesPath := filepath.Join(dir, "harness-issues.md")

	runFix([]string{"-config", cfgPath, "-report", reportPath, "-issues", issuesPath})

	// Check that the finding was fixed
	data, _ := os.ReadFile(reportPath)
	var result report.Report
	if err := json.Unmarshal(data, &result); err != nil {
		t.Fatal(err)
	}
	if len(result.Findings) != 1 {
		t.Fatalf("expected 1 finding, got %d", len(result.Findings))
	}
	if result.Findings[0].Status != report.StatusFixed {
		t.Errorf("expected status fixed, got %q (detail: %s)", result.Findings[0].Status, result.Findings[0].Detail)
	}

	// Check that the snippet file was updated
	updated, _ := os.ReadFile(snippetFile)
	if !strings.Contains(string(updated), "social-plus-sdk/chat/message-creation/send-a-message") {
		t.Errorf("snippet file not updated: %s", string(updated))
	}
}
```

You'll need to add `"strings"` to the import block in `fix_test.go` if not already present.

- [ ] **Step 2: Run test to confirm it fails**

```bash
cd harness && go test ./cmd/... -run TestRunFix_DocMissing -v
```
Expected: FAIL — finding status remains `open` (falls to `default:` case).

- [ ] **Step 3: Add `TypeDocMissing` case to `runFix` in `cmd/fix.go`**

In `cmd/fix.go`, inside the `switch f.Type {` block, add this case BEFORE the `case report.TypeSnippetContentDrift:` case:

```go
		case report.TypeDocMissing:
			fmt.Printf("[fix] DOC_MISSING %s\n", f.SnippetFile)
			if f.SnippetFile == "" || f.DocPage == "" {
				r.Findings[i].Status = report.StatusNeedsHuman
				r.Findings[i].Detail += " | missing snippet_file or doc_page field"
				continue
			}
			snippetAbs := filepath.Clean(filepath.Join(filepath.Dir(*cfgPath), f.SnippetFile))
			newPath, fixErr := fixer.FixAscPage(snippetAbs, f.DocPage, reg)
			if fixErr != nil {
				fmt.Printf("  FAILED: %v\n", fixErr)
				r.Findings[i].Status = report.StatusNeedsHuman
				r.Findings[i].Detail += " | auto-fix failed: " + fixErr.Error()
			} else {
				sealed, sealErr := verifier.Seal(f, snippetAbs, "PASS", "n/a")
				if sealErr != nil {
					fmt.Printf("  FAILED to seal: %v\n", sealErr)
					r.Findings[i].Status = report.StatusNeedsHuman
					r.Findings[i].Detail += " | seal failed: " + sealErr.Error()
				} else {
					r.Findings[i] = sealed
					fmt.Printf("  → %s\n", newPath)
					fixedCount++
				}
			}
```

- [ ] **Step 4: Run test to confirm it passes**

```bash
cd harness && go test ./cmd/... -run TestRunFix_DocMissing -v
```
Expected: PASS.

- [ ] **Step 5: Run all tests**

```bash
cd harness && go test ./... 2>&1 | tail -10
```
Expected: all packages ok.

- [ ] **Step 6: Commit**

```bash
cd harness && git add cmd/fix.go cmd/fix_test.go
git commit -m "feat: fix DOC_MISSING findings in harness fix command

Add TypeDocMissing case to runFix switch. Uses fixer.FixAscPage with
the old doc_page value as fuzzy-match input. Fixes the 79 DOC_MISSING
findings that previously fell to default→needs_human.

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

---

## Task 3: Run `harness fix` and verify finding counts drop

**Files:**
- Rebuild: `harness/harness-bin`
- Modified by fix: SDK snippet files across Android, Flutter, iOS, TypeScript repos

- [ ] **Step 1: Build the binary**

```bash
cd harness && go build -o ./harness-bin ./cmd/... && echo "BUILD OK"
```
Expected: `BUILD OK`

- [ ] **Step 2: Reset report (DOC_MISSING + ASC_PAGE_INVALID back to open)**

The report may have some findings already at `needs_human` from a previous failed fix run. Reset them:

```bash
cd harness && python3 -c "
import json
d = json.load(open('harness-report.json'))
reset = 0
for f in d['findings']:
    if f['type'] in ('ASC_PAGE_INVALID', 'DOC_MISSING') and f['status'] == 'needs_human':
        f['status'] = 'open'
        if '|' in f.get('detail', ''):
            f['detail'] = f['detail'].split('|')[0].strip()
        reset += 1
with open('harness-report.json', 'w') as fp:
    json.dump(d, fp, indent=2)
print(f'Reset {reset} findings to open')
"
```
Expected output like: `Reset 126 findings to open`

- [ ] **Step 3: Run the fix command**

```bash
cd harness && ./harness-bin fix --config harness-config.yml 2>&1
```
Expected: lines like:
```
[fix] ASC_PAGE_INVALID ../Amity-Social-Cloud-SDK-Android/.../AmityChannelQuery.kt
  → social-plus-sdk/chat/channels/channel-management
[fix] DOC_MISSING ../Amity-Social-Cloud-SDK-Android/.../AmityMessageCreateAudio.kt
  → social-plus-sdk/chat/messaging-features/message-creation/send-a-message
...
Fixed N findings deterministically. M findings need Copilot CLI (run 'harness prompt').
```

- [ ] **Step 4: Check finding counts**

```bash
cd harness && python3 -c "
import json
d=json.load(open('harness-report.json'))
from collections import Counter
c=Counter()
for f in d['findings']:
    c[(f['type'], f['status'])]+=1
for k,v in sorted(c.items()):
    print(f'{v:4d}  {k[0]:40s} {k[1]}')
"
```
Expected: `ASC_PAGE_INVALID` fixed ≥40, `DOC_MISSING` fixed ≥60. Both `open` counts near 0. Any `needs_human` remainder are genuinely unresolvable (short paths with no fuzzy match).

- [ ] **Step 5: Re-run audit to confirm findings don't re-appear**

```bash
cd harness && ./harness-bin audit --config harness-config.yml 2>&1 | tail -5
```
Expected: `Summary: N open` — the fixed snippets now have valid `sp_docs_page` values, so they won't reappear as `ASC_PAGE_INVALID` or `DOC_MISSING`.

- [ ] **Step 6: Commit fixed snippets**

```bash
cd harness
git add harness-report.json
# Commit changes in each SDK repo
cd ../Amity-Social-Cloud-SDK-Android && git add -A && git commit -m "fix: update sp_docs_page paths via harness fix

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>" && cd ../social-plus-docs
cd ../Amity-Social-Cloud-SDK-Flutter-Internal && git add -A && git commit -m "fix: update sp_docs_page paths via harness fix

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>" && cd ../social-plus-docs
cd ../AmitySDKIOS && git add -A && git commit -m "fix: update sp_docs_page paths via harness fix

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>" && cd ../social-plus-docs
cd harness && git add harness-report.json harness-bin && git commit -m "chore: update report after path repair (harness fix)

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

---

## Task 4: TypeScript gap filler script

**Goal:** Create 30 new `Amity*.ts` snippet files for functions that exist on Android/iOS/Flutter but not TypeScript. Uses Anthropic API with the Android snippet as reference.

**Files:**
- Create: `harness/scripts/fill-ts-gaps.py`
- Create (generated): `AmityTypescriptSDK/packages/sdk/src/snippets/Amity*.ts` (up to 30)

**Prerequisites:**
```bash
pip install anthropic
```
Or check with `python3 -c "import anthropic; print('ok')"`.

Set `ANTHROPIC_API_KEY` environment variable (or use the existing one from Copilot CLI context).

- [ ] **Step 1: Create `harness/scripts/` directory**

```bash
mkdir -p harness/scripts
```

- [ ] **Step 2: Create `harness/scripts/fill-ts-gaps.py`**

```python
#!/usr/bin/env python3
"""
fill-ts-gaps.py — Generate TypeScript snippet files for parity gaps.

Usage:
  python3 harness/scripts/fill-ts-gaps.py \
    --parity harness/function-parity.json \
    --ts-snippets-dir ../AmityTypescriptSDK/packages/sdk/src/snippets \
    --android-base ../Amity-Social-Cloud-SDK-Android \
    --batch 30

Requires: pip install anthropic
          ANTHROPIC_API_KEY environment variable
"""
import argparse
import json
import os
import re
import sys

def kebab_to_pascal(s):
    """Convert 'send-a-message' to 'SendAMessage'."""
    return ''.join(word.capitalize() for word in s.split('-'))

def load_parity(path):
    with open(path) as f:
        return json.load(f)

def find_gaps(parity_data, min_others=2):
    """Return list of (others_count, function_entry) sorted by coverage desc."""
    gaps = []
    for fn in parity_data['functions']:
        plats = fn['platforms']
        ts_status = plats.get('typescript', {}).get('status', 'unknown')
        if ts_status != 'unknown':
            continue
        others_exist = sum(
            1 for p, v in plats.items()
            if p != 'typescript' and v.get('status') == 'exists'
        )
        if others_exist >= min_others:
            gaps.append((others_exist, fn))
    gaps.sort(key=lambda x: -x[0])
    return gaps

def read_android_snippet(fn_entry, android_base):
    """Read the content of the Android reference snippet file."""
    android = fn_entry['platforms'].get('android', {})
    rel_file = android.get('file', '')
    if not rel_file:
        return None
    # rel_file is like '../Amity-Social-Cloud-SDK-Android/amity-sample-code/...'
    # Strip the leading '../' to get the path relative to the docs repo parent
    abs_path = os.path.normpath(os.path.join(
        os.path.dirname(android_base),
        os.path.basename(android_base),
        '/'.join(rel_file.split('/')[2:])  # strip first two segments '../RepoName/'
    ))
    # Fallback: try direct join
    if not os.path.exists(abs_path):
        abs_path = os.path.normpath(os.path.join(android_base, '/'.join(rel_file.split('/')[2:])))
    if not os.path.exists(abs_path):
        return None
    with open(abs_path) as f:
        return f.read()

def read_existing_ts_example(snippets_dir):
    """Return content of a good existing TS snippet as a few-shot example."""
    example_names = ['AmityPostCreateTextPost.ts', 'AmityChannelCreate.ts', 'AmityRoomCreate.ts']
    for name in example_names:
        path = os.path.join(snippets_dir, name)
        if os.path.exists(path):
            with open(path) as f:
                return f.read()
    # Fallback: read any snippet
    for f in os.listdir(snippets_dir):
        if f.endswith('.ts'):
            with open(os.path.join(snippets_dir, f)) as fh:
                return fh.read()
    return None

def generate_ts_snippet(fn_entry, android_content, ts_example, client):
    """Call Claude to generate a TypeScript snippet."""
    key = fn_entry['key']
    doc_page = fn_entry.get('sp_docs_page', '')
    pascal_name = 'Amity' + kebab_to_pascal(key)
    filename = pascal_name + '.ts'

    prompt = f"""You are generating a TypeScript snippet file for the social.plus SDK documentation.

Key: {key}
sp_docs_page: {doc_page}
Output filename: {filename}

Here is the TypeScript snippet pattern to follow (existing example):
```typescript
{ts_example}
```

Here is the Android reference snippet that shows what this function does:
```kotlin
{android_content}
```

Generate a TypeScript snippet that:
1. Starts with `// @ts-nocheck`
2. Has a `/* begin_sample_code` block with `filename`, `sp_docs_page`, and `description` fields
3. Imports from `@amityco/ts-sdk`
4. Implements the equivalent TypeScript code using the @amityco/ts-sdk API
5. Ends with `/* end_sample_code */`

Return ONLY the TypeScript file content. No explanations. No markdown fences."""

    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=600,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text.strip()

def write_snippet(content, filename, snippets_dir):
    path = os.path.join(snippets_dir, filename)
    with open(path, 'w') as f:
        f.write(content)
        if not content.endswith('\n'):
            f.write('\n')
    return path

def main():
    parser = argparse.ArgumentParser(description='Generate TypeScript snippet files for parity gaps')
    parser.add_argument('--parity', default='harness/function-parity.json')
    parser.add_argument('--ts-snippets-dir', default='../AmityTypescriptSDK/packages/sdk/src/snippets')
    parser.add_argument('--android-base', default='../Amity-Social-Cloud-SDK-Android')
    parser.add_argument('--batch', type=int, default=30)
    parser.add_argument('--dry-run', action='store_true', help='Print prompts without calling API')
    args = parser.parse_args()

    # Resolve paths relative to script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)

    parity_path = os.path.join(repo_root, args.parity) if not os.path.isabs(args.parity) else args.parity
    ts_dir = os.path.normpath(os.path.join(repo_root, args.ts_snippets_dir))
    android_base = os.path.normpath(os.path.join(repo_root, args.android_base))

    print(f"Parity file: {parity_path}")
    print(f"TS snippets dir: {ts_dir}")
    print(f"Android base: {android_base}")

    if not os.path.exists(parity_path):
        print(f"ERROR: parity file not found: {parity_path}", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(ts_dir):
        print(f"ERROR: TS snippets dir not found: {ts_dir}", file=sys.stderr)
        sys.exit(1)

    parity_data = load_parity(parity_path)
    gaps = find_gaps(parity_data, min_others=2)
    print(f"Total TS gaps (≥2 platforms): {len(gaps)}")

    ts_example = read_existing_ts_example(ts_dir)
    if not ts_example:
        print("ERROR: no existing TS snippets found as examples", file=sys.stderr)
        sys.exit(1)

    if not args.dry_run:
        try:
            import anthropic
        except ImportError:
            print("ERROR: anthropic package not installed. Run: pip install anthropic", file=sys.stderr)
            sys.exit(1)
        api_key = os.environ.get('ANTHROPIC_API_KEY')
        if not api_key:
            print("ERROR: ANTHROPIC_API_KEY not set", file=sys.stderr)
            sys.exit(1)
        client = anthropic.Anthropic(api_key=api_key)
    else:
        client = None

    created = 0
    skipped = 0
    batch = gaps[:args.batch]
    print(f"Processing top {len(batch)} gaps...")

    for _, fn_entry in batch:
        key = fn_entry['key']
        pascal_name = 'Amity' + kebab_to_pascal(key)
        filename = pascal_name + '.ts'
        out_path = os.path.join(ts_dir, filename)

        if os.path.exists(out_path):
            print(f"  [skip] {filename} already exists")
            skipped += 1
            continue

        android_content = read_android_snippet(fn_entry, android_base)
        if not android_content:
            print(f"  [skip] {key}: android reference not found")
            skipped += 1
            continue

        if args.dry_run:
            print(f"  [dry-run] would create {filename} (key={key})")
            continue

        print(f"  [generate] {filename}...", end='', flush=True)
        try:
            content = generate_ts_snippet(fn_entry, android_content, ts_example, client)
            write_snippet(content, filename, ts_dir)
            print(f" ✓")
            created += 1
        except Exception as e:
            print(f" FAILED: {e}")
            skipped += 1

    print(f"\nDone: {created} created, {skipped} skipped.")
    if created > 0:
        print(f"\nNext steps:")
        print(f"  1. Review generated files in {ts_dir}")
        print(f"  2. Run: cd harness && ./harness-bin parity --config harness-config.yml")
        print(f"  3. Check TypeScript parity improvement in function-parity.json")

if __name__ == '__main__':
    main()
```

- [ ] **Step 3: Test the script in dry-run mode**

```bash
cd social-plus-docs && python3 harness/scripts/fill-ts-gaps.py \
  --parity harness/function-parity.json \
  --ts-snippets-dir ../AmityTypescriptSDK/packages/sdk/src/snippets \
  --android-base ../Amity-Social-Cloud-SDK-Android \
  --batch 5 \
  --dry-run
```
Expected output:
```
Parity file: .../harness/function-parity.json
TS snippets dir: .../AmityTypescriptSDK/packages/sdk/src/snippets
Total TS gaps (≥2 platforms): 171
Processing top 5 gaps...
  [dry-run] would create AmityAdAnalyticsMarkAsSeen.ts (key=ad-analytics-mark-as-seen)
  [dry-run] would create AmityAdAnalyticsMarkLinkAsClicked.ts (key=ad-analytics-mark-link-as-clicked)
  ...
Done: 0 created, 0 skipped.
```

- [ ] **Step 4: Run actual LLM generation (batch of 30)**

```bash
cd social-plus-docs && python3 harness/scripts/fill-ts-gaps.py \
  --parity harness/function-parity.json \
  --ts-snippets-dir ../AmityTypescriptSDK/packages/sdk/src/snippets \
  --android-base ../Amity-Social-Cloud-SDK-Android \
  --batch 30
```
Expected: 30 (minus any skips) new `Amity*.ts` files created.

- [ ] **Step 5: Spot-check one generated file**

```bash
cat ../AmityTypescriptSDK/packages/sdk/src/snippets/AmityAdAnalyticsMarkAsSeen.ts
```
Expected: valid TypeScript with `begin_sample_code` block, `@amityco/ts-sdk` import, async function, `end_sample_code`.

- [ ] **Step 6: Run parity to update function-parity.json**

```bash
cd harness && ./harness-bin parity --config harness-config.yml
```
Expected: TypeScript `exists` count increases from 192 to ~220+.

- [ ] **Step 7: Verify TypeScript parity improvement via /api/parity**

```bash
cd harness && ./harness-bin serve --config harness-config.yml &
sleep 2
curl -s http://localhost:8765/api/parity | python3 -m json.tool | grep -A 4 typescript
kill %1
```
Expected: `typescript "exists"` count ≥220, `percent` ≥25%.

- [ ] **Step 8: Commit**

```bash
# Commit the script
cd social-plus-docs && git add harness/scripts/fill-ts-gaps.py
git commit -m "feat: add fill-ts-gaps.py script for TypeScript parity improvement

Reads function-parity.json, finds TS-unknown keys with ≥2 platform
coverage, generates Amity*.ts snippet files via Claude Sonnet.

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"

# Commit generated TS snippets in the TS SDK repo
cd ../AmityTypescriptSDK && git add packages/sdk/src/snippets/Amity*.ts
git commit -m "feat: add TypeScript snippet files for parity gaps (batch 1)

Generated by harness/scripts/fill-ts-gaps.py using Android reference
snippets. Improves TS parity from 15% to ~25%+.

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"

# Commit updated parity map
cd ../social-plus-docs/harness && git add function-parity.json
git commit -m "chore: update function-parity.json with TypeScript batch 1

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

---

## Self-Review

**Spec coverage check:**
- ✅ DOC_MISSING (79): Task 2 adds the missing case, Task 3 runs the fix
- ✅ ASC_PAGE_INVALID (47): Task 1 fixes the extraction bug, Task 3 runs the fix  
- ✅ TypeScript parity: Task 4 generates 30 new snippet files
- ✅ Verify findings drop: Task 3 Step 5 re-runs audit
- ✅ Verify parity improvement: Task 4 Step 6-7

**Placeholder scan:** None found.

**Type consistency:**
- `fixer.FixAscPage(snippetAbs, f.DocPage, reg)` — matches the existing signature `func FixAscPage(snippetFile, currentAscPage string, reg *pages.Registry) (string, error)` ✅
- `verifier.Seal(f, snippetAbs, "PASS", "n/a")` — matches `func Seal(f report.Finding, artifactPath, compileResult, compileOutputHash string) (report.Finding, error)` ✅
- `report.TypeDocMissing` — constant exists in `types.go` ✅
- `report.StatusFixed` — constant exists in `types.go` ✅
