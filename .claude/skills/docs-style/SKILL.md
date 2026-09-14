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

## Voice by section type

Match the voice to what the section is for:

- **Section overviews and feature introductions** — lead with the reader benefit, not the mechanism. Say *why* an integrator would reach for the feature and what problem it solves for their users, before the API details. A light, benefit-led (marketing-aware) tone is correct here — e.g. "surface the posts each member cares about so the home feed stays relevant," not "returns a ranked post collection." Keep it honest: no hype, no invented metrics, no superlatives you can't back up.
- **Reference, how-to, parameters, and behavior sections** — precise and technical. State the exact API, inputs, outputs, and observable behavior. No marketing language here; the clarity rubric flags it.

Most pages have both: a benefit-led intro, then technical sections. Write each in its own voice.

## What to expose vs. keep private

Write for the integrator: give them everything they need to build, and nothing that is internal, unbuildable, or confidential.

**Expose** — the integrator needs it:
- Public API names, signatures, parameters, return types, and observable behavior.
- Product behavior a developer or end user can perceive (e.g. "older posts age out of the feed", "already-seen posts aren't repeated", "the feed personalizes as the user engages").
- What the integrator is responsible for wiring up (e.g. report post views so seen-state works).

**Keep private** — do not document; it is internal or confidential:
- Exact ranking weights, scoring formulas, decay curves, thresholds, and the math behind them. Name the *signals* and describe their effect in plain language instead.
- Backend storage and delivery mechanics (caches, snapshots, cursors, queues, datastore names) the integrator never touches.
- Internal cold-start counts, tuning constants, and experiment parameters.

**Never document a feature that isn't implemented.** A field in a schema, a type, or a leftover trace is **not** a feature. If the code path doesn't exist and ship, it does not go in the docs — and never invent companion fields or APIs to make an inferred feature sound coherent. When you find a dormant field, either label it (reserved / not implemented) or leave it out.

**Personalization & regulation:** for recommender or personalization features, name the main parameters in plain language (transparency expectations such as the EU Digital Services Act) **and** point to the non-personalized alternative the user can switch to — without exposing the confidential scoring model.

## Enforcement

Pushes run structure/drift gates (`.docs-ops/CI_GATE.md`): `check-mdx.py`, `check-sdk-style.py`, and `check-drift.py`. A PR is blocked if it introduces a new stale (file, API-ref) pair versus `origin/main`. Match the archetype shape so `check-sdk-style.py` passes.

## Related skills

- **`release-notes`** — writing and updating changelogs / release notes across the SDK and UIKit platforms.
