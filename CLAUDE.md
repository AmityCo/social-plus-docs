# social.plus documentation — working guide for Claude

This repo is the social.plus product documentation (Mintlify). Brand name is always **social.plus** — lowercase, with the period, even at the start of a sentence. Never "Social.Plus", "SocialPlus", or "Social Plus".

## Before writing or editing documentation

Don't write docs from memory — consult the repo's doc-writing standards first. Invoke the **`docs-style`** skill, or read the sources it points to:

- **`.github/copilot-instructions.md`** — master style guide (Mintlify components, content templates, per-platform code conventions, UIKit patterns).
- **`.docs-ops/sdk-style/README.md`** — SDK page style contract and the page **archetypes** (`overview`, `concept`, `operation`, `setup`, `migration`, `reference-lite`).
- **`.docs-ops/rubric.json`** — the 6-dimension quality bar: accuracy, completeness, cross-platform parity, examples, clarity, ai-consumability.

For **changelogs / release notes**, invoke the **`release-notes`** skill.

When documenting **new or changed functionality**, first ground yourself in what actually shipped: read the product specs in the `cleverden` sibling repo (`$GITHUB_ROOT/cleverden` — PRDs, tech proposals, `front-end-tech-specs/`) and, if needed, the actual SDK source (sibling repos, same path convention as the release-notes skill). Then document only what the integrator needs — see the `docs-style` skill's grounding workflow. `cleverden` is internal; treat its ranking weights, formulas, and backend mechanics as private.

## Non-negotiables

- **Accuracy first.** Verify every API name, signature, parameter, and behavior against the actual SDK source before documenting it. **Never infer or describe a feature from a schema field, type, or partial trace alone** — if the code doesn't implement it, don't document it, and don't invent companion fields or APIs to make it sound coherent.
- **Voice by section.** Overviews and feature introductions lead with the reader benefit (a light, marketing-aware tone — why to use it, what problem it solves). Reference, how-to, and behavior sections are precise and technical with no marketing language.
- **Cross-platform parity.** When a feature ships on multiple platforms, describe it consistently across them.
- **Expose what the integrator needs; keep system internals private.** Public APIs, parameters, and perceivable product behavior are fair game. Exact ranking weights, scoring formulas, thresholds, and backend storage/delivery mechanics are not — describe named signals and behavior at the customer-facing level. For personalization features, name the main parameters in plain language (e.g. for EU DSA transparency) and point to the non-personalized alternative.
- **Report the context you had.** A page can only be as good as its inputs — style cannot invent a problem statement, and grounding cannot invent a spec nobody wrote. Every docs PR description carries a **Context checklist** (problem statement, product spec, technical spec, source verification, platform availability, design reference, exposure review, regulatory) with a status per row, and a one-line note on what any gap cost. Never fabricate a missing input; `❌` is a legitimate outcome. Re-assess the checklist on every new commit — see the `docs-style` skill.
- Navigation lives in **`docs.json`** (not `placeholder.json`, which is stale and unused).
- Don't hand-edit generated layers (`.docs-ops/sdk-surface/*`); the SDK best-practice "opinion" layer lives in the separate `social-plus-foundry` (Vise) repo.

## Skills

Claude discovers skills under `.claude/skills/`. The canonical, cross-agent skill definitions live under `.agents/skills/` (`release-notes`, `social`); the entries in `.claude/skills/` are thin pointers to them so they're callable from Claude too. Keep the canonical copy in `.agents/skills/` when editing skill content.
