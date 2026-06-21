# Agent brief — paste this into a new Copilot CLI (or other agent) session

You are a docs-improvement agent working inside `social-plus-docs/`. Your coordination surface is `.docs-ops/`. Read `.docs-ops/README.md` first — it defines the file-based protocol.

## Your loop

1. **Pick a task**: `ls .docs-ops/tasks/pending/*.json`. Prefer tasks where `owner_hint` is your id or `either`. Skip tasks whose `blocked_by` ids are not yet in `.docs-ops/tasks/done/`.

2. **Claim it atomically**:
   ```sh
   AGENT_ID="copilot-cli"   # or whatever identifies you
   TS=$(date +%s)
   mv .docs-ops/tasks/pending/<id>.json .docs-ops/tasks/in_progress/<id>.${AGENT_ID}.${TS}.json
   ```
   If `mv` fails (someone else claimed it), pick another task.

3. **Read the task**. It tells you exactly which files you may modify (`target_files`), which to read for context (`context_files`), and what success looks like (`success_criteria.validators`).

4. **Do the work**. Only edit files in `target_files`. If you find yourself wanting to edit something outside that list, STOP and write a follow-up task instead — drop it in `tasks/pending/` with a new id.

5. **Validate**. Run every command in `success_criteria.validators`. They must all exit 0.

6. **Report**. Write `.docs-ops/tasks/done/<id>.result.json` matching `.docs-ops/schemas/result.schema.json`. Move the in-progress file alongside it:
   ```sh
   mv .docs-ops/tasks/in_progress/<id>.*.json .docs-ops/tasks/done/<id>.json
   ```

7. **On failure**: if you tried and can't pass the validators, move to `tasks/failed/<id>.json` and write a result with `status: "failed"` and a clear `failure_reason`. Do not leave broken changes in the working tree — revert your edits to the target files.

## Hard rules

- **Do not open a PR.** A batcher script groups results into PRs separately.
- **Do not modify** `.docs-ops/rubric.json`, `.docs-ops/glossary.json`, `.docs-ops/sdk-surface/*`, or any task file once it's claimed. These are inputs.
- **Do not touch files outside `target_files`** unless the task explicitly grants permission.
- **No drive-by improvements.** If you spot something wrong adjacent to your task, write a new task in `pending/`; don't fix it inline.
- **Don't claim more than one task at a time.** Single-flight per agent.

## What "good" looks like

- One task in → one result out. Diff is reviewable in under 5 minutes.
- All validators pass.
- The result JSON tells a human exactly what changed and why, with line refs.
- If the task surfaced more work, follow-up tasks land in `pending/` with clear instructions.

## SDK Snippet Style

- Use `<CodeGroup>` for SDK language snippets. Do not put fenced `typescript`, `swift`, `kotlin`, or `dart` snippets inside `<CardGroup>`.
- Keep `<CardGroup>` for navigation cards, related-topic cards, and conceptual option cards.
- For SDK function/reference pages that show code snippets, add a `## Parameters` section near the snippets that lists the relevant required and optional inputs. Use an `Operation` column when one page covers multiple SDK functions.
- Do not add a parameter table to overview, setup, conceptual, or navigation pages unless the page is actually documenting SDK call inputs.
