# SDK Harness — Agent Runbook

_Generated 2026-04-30 20:35 — 949 findings requiring AI_

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

## DOC_PAGE_STALE_IMPORT (949)

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

## After completion

```bash
cd social-plus-docs/harness
./harness-bin audit --config harness-config.yml
# If open findings remain: ./harness-bin prompt --config harness-config.yml
```
