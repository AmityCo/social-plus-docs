# social.plus documentation — working guide for Claude

This repo is the social.plus product documentation (Mintlify). Brand name is always **social.plus** — lowercase, with the period, even at the start of a sentence. Never "Social.Plus", "SocialPlus", or "Social Plus".

## Before writing or editing documentation

Don't write docs from memory — consult the repo's doc-writing standards first. Invoke the **`docs-style`** skill, or read the sources it points to:

- **`.github/copilot-instructions.md`** — master style guide (Mintlify components, content templates, per-platform code conventions, UIKit patterns).
- **`.docs-ops/sdk-style/README.md`** — SDK page style contract and the page **archetypes** (`overview`, `concept`, `operation`, `setup`, `migration`, `reference-lite`).
- **`.docs-ops/rubric.json`** — the 6-dimension quality bar: accuracy, completeness, cross-platform parity, examples, clarity, ai-consumability.

For **changelogs / release notes**, invoke the **`release-notes`** skill.

## Non-negotiables

- **Accuracy first.** Verify every API name, signature, parameter, and behavior against the actual SDK source before documenting it. **Never infer or describe a feature from a schema field, type, or partial trace alone** — if the code doesn't implement it, don't document it.
- **No marketing fluff** in reference or solution content (the clarity rubric forbids it). A light benefit framing is allowed only in section overviews.
- **Cross-platform parity.** When a feature ships on multiple platforms, describe it consistently across them.
- **Confidential internals stay out.** Don't publish exact ranking weights, scoring formulas, or backend storage/mechanics — describe behavior at the customer-facing level.
- Navigation lives in **`docs.json`** (not `placeholder.json`, which is stale and unused).
- Don't hand-edit generated layers (`.docs-ops/sdk-surface/*`); the SDK best-practice "opinion" layer lives in the separate `social-plus-foundry` (Vise) repo.

## Skills

Claude discovers skills under `.claude/skills/`. The canonical, cross-agent skill definitions live under `.agents/skills/` (`release-notes`, `social`); the entries in `.claude/skills/` are thin pointers to them so they're callable from Claude too. Keep the canonical copy in `.agents/skills/` when editing skill content.
