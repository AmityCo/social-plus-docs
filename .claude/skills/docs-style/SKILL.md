---
name: docs-style
description: Use before writing or editing any social.plus documentation — MDX pages, SDK or UIKit reference pages, use-case guides, section overviews, or landing pages. Loads the repo's doc-writing style, page-structure archetypes, and quality rubric so pages stay consistent and accurate.
metadata:
  author: social.plus
  version: "1.0"
---

# Documentation Style Skill

Follow the repo's doc-writing contract. Read the authoritative sources relevant to the page you're working on — do not write from memory.

## Authoritative sources

- **`.github/copilot-instructions.md`** — the master style guide: required Mintlify components, content-structure templates, per-platform code conventions (iOS / Android / TypeScript / Flutter), the UIKit component documentation pattern, and landing-page standards.
- **`.docs-ops/sdk-style/README.md`** — the SDK page style contract. Pick the **archetype** that matches the page and follow its required shape and section order:
  - `overview` · `concept` · `operation` · `setup` · `migration` · `reference-lite`
  - For unusual pages, set `sdk_page_type:` in frontmatter.
- **`.docs-ops/rubric.json`** — the quality bar every page is scored against (6 dimensions): accuracy, completeness, cross-platform parity, examples, clarity, ai-consumability.

## Always apply

- **Brand:** **social.plus** — lowercase, with the period, even sentence-initial.
- **Accuracy first:** verify every API name, signature, parameter, and behavior against the current SDK source before writing it. **Never document a feature inferred from a schema field, type, or partial trace** — if the code doesn't implement it, it doesn't go in the docs.
- **Clarity:** plain language, define your terms, right-sized for an engineer. **No marketing fluff** in reference/solution content; a light benefit framing is allowed only in section overviews.
- **Parity:** describe a multi-platform feature consistently across every platform it ships on.
- **Confidential internals stay out:** no exact ranking weights, scoring formulas, or backend storage/mechanics — keep to customer-facing behavior.
- **Navigation:** defined in `docs.json` (not `placeholder.json`, which is stale).
- **Don't hand-edit** generated layers (`.docs-ops/sdk-surface/*`). The SDK best-practice "opinion" layer lives in the `social-plus-foundry` (Vise) repo.

## Enforcement

Pushes run structure/drift gates (`.docs-ops/CI_GATE.md`): `check-mdx.py`, `check-sdk-style.py`, and `check-drift.py`. A PR is blocked if it introduces a new stale (file, API-ref) pair versus `origin/main`. Match the archetype shape so `check-sdk-style.py` passes.

## Related skills

- **`release-notes`** — writing and updating changelogs / release notes across the SDK and UIKit platforms.
