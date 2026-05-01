# SDK Harness — Agent Runbook

_Generated 2026-05-01 11:31 — 1 findings requiring AI_

## Agent Instructions

You are an autonomous agent. Execute ALL tasks in this file without stopping for confirmation.

**For each MISSING_SNIPPET task:**
1. Look up the function in the SDK source (search by function ID in the SDK path)
2. Generate a minimal working snippet using the `begin_sample_code` format below
3. Write the file to the specified snippet directory
4. Continue to the next task immediately

**After ALL snippets are written:**
```bash
cd social-plus-docs/harness && ./harness-bin audit --config harness-config.yml
```
Then run `./harness-bin prompt` again if there are still open findings.

**Snippet format (MUST match exactly):**
```
/* begin_sample_code
   filename: <filename>
   sp_docs_page: <path from docs.json, e.g. social-plus-sdk/chat/overview>
   description: <one line>
   */
<working code>
/* end_sample_code */
```

**Rules:**
- Use real Amity SDK class names (look them up in the SDK source)
- Keep it minimal — just enough to demonstrate the function
- `sp_docs_page` must be a relative path (not a full URL)
- Do not ask for confirmation between tasks — work through all of them

---


---

## MANIFEST_FILL (8 sections need assignment)

For each section below, open the manifest file and assign candidate snippet keys
to the matching `snippets:` array. Use the manifest file as your data source —
candidate keys are listed in the `_candidates:` block inside it.

### How to verify

```bash
cd social-plus-docs/harness
./harness-bin audit --config harness-config.yml
```

MANIFEST_FILL findings disappear when all sections have at least one snippet assigned.

### Sections to fill

- **`social-plus-sdk/core-concepts/foundation/logging`** → section `### Key Features`  
  Manifest: `social-plus-sdk/core-concepts/foundation/logging.manifest.yml`
- **`social-plus-sdk/core-concepts/user-management/user-identity`** → section `### Initializing User Repository`  
  Manifest: `social-plus-sdk/core-concepts/user-management/user-identity.manifest.yml`
- **`social-plus-sdk/core-concepts/user-management/user-operations/search-and-query-users`** → section `### Query Implementation`  
  Manifest: `social-plus-sdk/core-concepts/user-management/user-operations/search-and-query-users.manifest.yml`
- **`social-plus-sdk/core-concepts/user-management/user-operations/search-and-query-users`** → section `### Search Implementation`  
  Manifest: `social-plus-sdk/core-concepts/user-management/user-operations/search-and-query-users.manifest.yml`
- **`social-plus-sdk/getting-started/visitor-mode`** → section `### Permission Enforcement`  
  Manifest: `social-plus-sdk/getting-started/visitor-mode.manifest.yml`
- **`social-plus-sdk/getting-started/visitor-mode`** → section `### Step 2: Get Visitor Device ID`  
  Manifest: `social-plus-sdk/getting-started/visitor-mode.manifest.yml`
- **`social-plus-sdk/video-new/analytics/overview`** → section `### AmityRoom Extension`  
  Manifest: `social-plus-sdk/video-new/analytics/overview.manifest.yml`
- **`social-plus-sdk/video-new/analytics/overview`** → section `### AmityRoomAnalytics`  
  Manifest: `social-plus-sdk/video-new/analytics/overview.manifest.yml`

## DOC_PAGE_STALE_IMPORT (1)

These doc pages reference gendocs snippet files that are not yet imported.
Run the migrate command to automatically add the missing imports:

```bash
cd social-plus-docs/harness
./harness-bin migrate --config harness-config.yml
```

Or preview changes first with `--dry-run`:

```bash
./harness-bin migrate --config harness-config.yml --dry-run
```


---

## PUBLIC_FUNC_UNANNOTATED (325 functions)

**Read the full list from:** `harness/unannotated-functions-report.md`

### What to do

For each function listed in the report:

1. Open the source file shown in the report
2. Find the function declaration
3. Wrap it with `begin_public_function` / `end_public_function`:

```kotlin
/* begin_public_function
   id: <feature.action>   e.g. comment.create, post.query
*/
fun myFunction(): ReturnType {
    ...
}
/* end_public_function */
```

The same pattern applies to Swift, Dart, and TypeScript.

4. If the function is truly internal / not for public use, add `@Deprecated` instead

### How to verify

After annotating, re-run the audit — the finding count MUST drop:

```bash
cd social-plus-docs/harness
./harness-bin audit --config harness-config.yml
```

The audit reads the SDK source directly. You cannot satisfy this check by editing
`harness-tasks.md` or `unannotated-functions-report.md` — only source changes count.
---

## After completion

Run the full audit to verify all tasks are resolved:

```bash
cd social-plus-docs/harness
./harness-bin audit --config harness-config.yml
```

**Expected result:** zero `open` findings. The audit is the authoritative proof —
it re-reads source files directly and cannot be satisfied by editing task or report files.

If findings remain, run `./harness-bin prompt` to regenerate this file with the remaining work.
