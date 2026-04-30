# SDK Harness — Agent Runbook

_Generated 2026-04-30 17:51 — 1 findings requiring AI_

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
   gist_id: PLACEHOLDER
   filename: <filename>
   asc_page: <path from docs.json, e.g. social-plus-sdk/chat/overview>
   description: <one line>
   */
<working code>
/* end_sample_code */
```

**Rules:**
- Use real Amity SDK class names (look them up in the SDK source)
- Keep it minimal — just enough to demonstrate the function
- `asc_page` must be a relative path (not a full URL)
- Do not ask for confirmation between tasks — work through all of them

---

## MISSING_SNIPPET (1)

For each entry below, create a SDK code snippet file at the given path.
The snippet **must** use this exact format:

```
/* begin_sample_code
   gist_id: PLACEHOLDER
   filename: <filename>
   asc_page: <docs.json relative path, e.g. social-plus-sdk/chat/overview>
   description: <one line>
   */
<working code>
/* end_sample_code */
```

Rules:
- Use real Amity/social.plus SDK class names from the platform source
- Keep it minimal — just enough to demonstrate the function
- `asc_page` must be a path from `docs.json` (not a full URL)

### Flutter (Dart) — 1 functions

Snippet directory: `../../Amity-Social-Cloud-SDK-Flutter-Internal/code_snippet`

| Function ID | Write to filename |
|-------------|-------------------|
| `story.getTargetsbyTargets request` | `AmityStoryGetTargetsbyTargets request.dart` |

---

## After completion

```bash
cd social-plus-docs/harness
./harness-bin audit --config harness-config.yml
# If open findings remain: ./harness-bin prompt --config harness-config.yml
```
