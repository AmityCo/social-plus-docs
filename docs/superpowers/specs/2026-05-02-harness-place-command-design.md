# Design: `harness place` Command

**Date:** 2026-05-02  
**Status:** Approved  
**Context:** 118 MDX pages have snippet imports but no `<ComponentName />` placement; 43 pages have hardcoded `<CodeGroup>` with no imports at all. Snippet content is invisible to Mintlify users until components are placed inline.

---

## Problem

`harness gendocs` + `harness migrate` add `import X from '/snippets/...'` to the top of MDX pages, but do not place `<X />` tags in the body. Mintlify only renders a snippet when the tag appears in the page body. Result: ~89% of snippet imports are orphaned.

Fuzzy heading-match (computational) would misplace components on semantically ambiguous pages (e.g. a page with both "Flag Messages" and "Check Flag Status" sections both containing the word "flag"). An LLM can read the full page and make correct placement decisions with context.

---

## Architecture

Follows the established harness pattern: **harness does computational scanning → Copilot CLI agents do inference**.

```
harness place (scan)
    ↓
  placement-tasks.json   (one task per affected page)
    ↓
Copilot CLI agents (one per task)
    ↓
  MDX files updated (component tags placed)
```

The harness binary stays LLM-free. All inference happens in agent context.

---

## `harness place` Command (computational)

**Flags:**
- `-config` (default: `harness-config.yml`)
- `-out` (default: `placement-tasks.json`) — output task file path
- `-dry-run` — print summary without writing task file

**Algorithm:**
1. Walk all MDX files in `docs.scope`
2. For each file, parse imports (`import X from '/snippets/...'`)
3. Identify unplaced: imports where `<X` is absent from the file body
4. For each unplaced import, resolve the Mintlify-relative path (`/snippets/...`) to an absolute path under `docs.path/snippets/` → read first 40 lines as preview (skip if file missing)
5. Emit a task entry if the page has ≥1 unplaced component

**Output — `placement-tasks.json`:**
```json
[
  {
    "page_file": "/abs/path/to/flag-unflag-a-message.mdx",
    "page_path": "social-plus-sdk/chat/messaging-features/messages/flag-unflag-a-message",
    "components": [
      {
        "name": "MessageFlag",
        "key": "message-flag",
        "import_path": "/snippets/social-plus-sdk/chat/message-flag.mdx",
        "snippet_preview": "<CodeGroup>\n```kotlin Android\n..."
      },
      {
        "name": "MessageUnflag",
        "key": "message-unflag",
        "import_path": "/snippets/social-plus-sdk/chat/message-unflag.mdx",
        "snippet_preview": "..."
      }
    ]
  }
]
```

**Console output:**
```
[place] 118 pages with unplaced components → placement-tasks.json
[place] run Copilot CLI agents to execute placements
```

---

## Agent Placement (inferential)

Each agent receives one task entry. The agent:

1. Reads the full MDX page
2. Reads the component list (name, key, snippet preview)
3. For each component:
   - Identifies the most relevant section heading (e.g. `MessageFlag` → `## Flag Messages`)
   - Finds the best insertion point within that section:
     - If section contains `<CodeGroup>...</CodeGroup>` → **replace** with `<ComponentName />`
     - Otherwise → insert `<ComponentName />` after the last fenced code block in the section, or at end of section before next heading
   - If no heading matches the component semantically → collect for fallback
4. Fallback: insert a `## Code Examples` section at end of page (before `## Best Practices`, `## Related Documentation`, `## Advanced`, or end-of-file — whichever comes first)
5. Write the updated MDX file

**Agent constraints:**
- Do NOT change any prose, headings, or non-code content
- Do NOT add or remove imports (already done by migrate)
- One `<ComponentName />` tag per component, placed exactly once
- If a `<ComponentName />` already exists anywhere in the file, skip that component
- Always place with a blank line before and after: `\n\n<ComponentName />\n\n`
- Match existing indentation if placing inside a `<Tab>` / `<Accordion>` / `<Step>` block (typically 4 spaces)
- **Never** place inside a fenced code block (` ```...``` `), inside frontmatter (`---...---`), or inside an HTML/JSX attribute value
- Self-closing tag only: `<ComponentName />` — never `<ComponentName></ComponentName>`
- Replace `<CodeGroup>...</CodeGroup>` (full block) with `<ComponentName />` when found in the matched section, preserving surrounding blank lines

**Post-placement validation (Copilot CLI, after all agents complete):**
```
cd harness && ./harness-bin audit
```
Must report 0 Mintlify syntax errors. If any page has a new syntax error, revert that file and log it as needing manual review.

---

## New Files

| File | Purpose |
|------|---------|
| `cmd/place.go` | CLI entry point, flag parsing, task file emission |
| `internal/placer/scanner.go` | Scans MDX files for unplaced imports; resolves snippet previews |
| `internal/placer/scanner_test.go` | Unit tests |

No new internal packages needed for inference — that lives in Copilot CLI agent prompts.

---

## Pipeline Position

```
gendocs → audit → migrate → dedup → audit → parity → place (new) → agent run
```

`place` is idempotent: re-running only emits tasks for still-unplaced components.

---

## Success Criteria

- `harness place` emits a valid `placement-tasks.json` covering all 118 orphaned-import pages
- After agent execution: 0 pages with orphaned imports (all `<ComponentName />` placed)
- 0 Mintlify syntax errors after placement
- `harness audit` reports no new findings introduced by placement

---

## Out of Scope

- Automatically dispatching agents (Copilot CLI session handles this)
- Handling the 43 pages with hardcoded `<CodeGroup>` and no imports (separate migration)
- Placing components on pages outside `docs.scope`
