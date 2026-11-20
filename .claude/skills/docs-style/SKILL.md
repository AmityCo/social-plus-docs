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
- **Code sample order:** inside every `CodeGroup`, order the samples **Android, iOS, then web, then React Native, then Flutter**, and omit any platform that doesn't ship the feature.
  - **SDK pages:** `kotlin Android` → `swift iOS` → `typescript TypeScript` → `dart Flutter`.
  - **UIKit pages:** `kotlin Android` → `swift iOS` → the web UIKit sample, labeled `React` (`typescript React` / `tsx React`, the existing UIKit convention; a few older pages use `Web`) → `jsx React Native` → `dart Flutter`.
  - A `{/* doc-as-test: … */}` comment belongs to the block right after it; move it with that block.
  - Pages written before this rule may still use the older TypeScript-first order. Reorder **every** group on a page when you add or edit one, rather than mixing orders on one page. Moving blocks is not changing code: keep each block byte-identical.
  - No checker enforces this order. Check it yourself before you push.
- **Headings — match the folder.** Use the heading case the other pages in the same folder use; consistency within a section beats the sentence-case default. Today most SDK and UIKit pages use title case. End SDK pages with `## Related Topics` and UIKit component pages with `## Related Components`. Never repeat the page title as the first section heading.
- **Confidential internals stay out:** no exact ranking weights, scoring formulas, or backend storage/mechanics — keep to customer-facing behavior.
- **No customer names** in pages or PR descriptions, even when a spec or ticket names the customer who asked for the feature. Say "a customer".
- **Consistent across pages:** when a page describes behavior another page also covers (a delay, a limit, a default), say it the same way on both, or fix the other page. Reuse shared forms, such as `[social.plus Support](https://ekoapp.atlassian.net/servicedesk/customer/portal/3)` for "contact support".
- **Navigation:** defined in `docs.json` (not `placeholder.json`, which is stale).
- **Don't hand-edit generated files:** `.docs-ops/sdk-surface/*`, `llms.txt` and `llms-full.txt` (a bot regenerates the last two after merge). The SDK best-practice "opinion" layer lives in the `social-plus-foundry` (Vise) repo.

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
- Tunable operational values — delays, cache lifetimes, timeouts, poll intervals — even when a spec says "accept and document" the effect. Describe the behavior ("a new post can take a few minutes to appear"), not the number, so it can change without a docs fix.

**Leave out what the reader doesn't need.** Confidential is not the only reason to cut. Before you keep a sentence, ask whether the integrator acts on it. Common cuts:
- How to change a setting that only social.plus Support changes: no admin endpoints, curl calls, tokens or error codes for it. Say the default, and "contact social.plus Support" to change it.
- Roadmap remarks ("no console toggle yet", "coming soon").
- Release-note material in a feature page ("the badge now sits bottom-left"). It belongs in the changelog.
- SDK samples repeated on a UIKit page when the UIKit already does the work. Link the SDK page instead.
- Generic errors (entitlement, auth, rate limits) repeated on a feature page. They belong in the error reference.
- How-tos that the sibling pages don't give (for example a refresh flow), unless the feature needs one.
- Localization key tables on UIKit component pages: the localization reference lists the keys.
- Mechanics no one acts on ("a video taller than the screen counts once it fills half of it").

A UIKit capability that runs on its own needs only: what members see, the defaults, how it is turned on, what members can change, the integration steps that really exist, and customization.

**Never document a feature that isn't implemented.** A field in a schema, a type, or a leftover trace is **not** a feature. If the code path doesn't exist and ship, it does not go in the docs — and never invent companion fields or APIs to make an inferred feature sound coherent. When you find a dormant field, either label it (reserved / not implemented) or leave it out.

**Personalization & regulation:** for recommender or personalization features, name the main parameters in plain language (transparency expectations such as the EU Digital Services Act) **and** point to the non-personalized alternative the user can switch to — without exposing the confidential scoring model.

## Grounding a new or changed feature

When you document new or changed functionality, ground yourself in what was **actually built** before writing — never describe a feature from its name, a ticket title, or a schema field. The product specs and source live in repos cloned as **siblings of this docs repo**, the same convention the `release-notes` skill uses:

```bash
GITHUB_ROOT="$(cd "$(git rev-parse --show-toplevel)/.." && pwd)"
```

Read in this order, stopping once you have what the integrator needs:

1. **Product specs — `$GITHUB_ROOT/cleverden`** (a sibling repo of PRDs, tech proposals, and tech specs):
   - `front-end-tech-specs/SDK/…` and `front-end-tech-specs/UIKIT/…` — the integrator-facing API and component specs (closest to what you're documenting).
   - `front-end-tech-specs/ImplementationPlan/…` — how the feature is split and staged across platforms.
   - `tech-specs/`, `tech-proposals/`, `prd/` and `prds/` — behavior, eligibility rules, and the *why*.
2. **Actual SDK / UIKit source** — the sibling repos listed in the `release-notes` skill (`$GITHUB_ROOT/<repo-name>`). Confirm the real API names, signatures, and that the code path actually ships. Distribution/tag conventions are in the `release-notes` skill.
3. **Backend source — `$GITHUB_ROOT/social-plus-core`** — for anything the backend decides: which posts a feed returns, network settings and their defaults, limits, and what a setting can be combined with. Read the settings and defaults (`src/shared/network-setting/`, `app.config.ts`) and the module code, not only the SDK call.

**Document the capability, not the first customer's setup.** A feature built for one customer often ships as general settings that customer happens to combine one way. Describe what the system can do (each option and its default), then give the customer's combination as an example if it helps.

**What each source is for.** The latest shipped code (SDK, UIKit, backend) is the scope — even when a spec or product doc says otherwise, since scope changes during the build. Product and problem-validation docs (Notion feature requests, PRDs, research) are for the problem statement and benefit framing only. Never take a capability, a default or a self-serve path from them.

**cleverden is internal.** It contains exactly the material you must NOT publish — exact ranking weights, formulas, thresholds, backend storage/delivery mechanics, cold-start constants, and roadmap items that haven't shipped. Use it to *understand* the feature, then apply **What to expose vs. keep private** (above) to the output: document only the public API, the observable behavior, and what the integrator must do. If a spec describes something the shipped source does not yet implement, do not document it as available.

## Context checklist

A page can only be as good as the context you were given. Writing style cannot invent a problem statement, and grounding cannot invent a spec that was never written. Track which inputs you actually had, and report it — so a reviewer can tell the difference between "this page has no benefit framing because the writer skipped it" and "…because no product context existed."

Assess these eight inputs for every docs change:

| # | Context | What it unlocks in the output |
| --- | --- | --- |
| 1 | **Problem statement / marketing framing** | The benefit-led intro on overviews — why a reader should care, what problem it solves |
| 2 | **Product spec** (PRD, scope, acceptance criteria, out-of-scope) | Correct scope, eligibility rules, and what to leave out |
| 3 | **Technical spec / implementation plan** | Intended API shape and how the feature is staged across platforms |
| 4 | **Source verification** | Real names, signatures, return types, and that the code path actually ships |
| 5 | **Platform availability** | Honest per-platform support and "Not exposed" rows |
| 6 | **Design reference** (Figma, screenshots) | UI anatomy, states, and interaction behavior for UIKit pages |
| 7 | **Exposure review** | Confidential/internal material identified and deliberately excluded |
| 8 | **Regulatory / compliance** | Transparency obligations where they apply (e.g. EU DSA for recommenders) |

Status values: **✅ used** · **⚠️ partial** · **❌ not available** · **— n/a**.

Two rules that make this worth doing:

- **Never fabricate a missing input.** If there is no problem statement, write a descriptive intro — do not invent a benefit claim. If there is no spec, document only what source proves. A `❌` is a legitimate outcome, not a failure.
- **Say what the gap cost.** Every `❌` or `⚠️` needs a one-line note on what the page therefore lacks, so the gap is visible and fixable later.

## Pull request description

Every docs PR description carries, in this order:

1. **## Improvement** (or **## Change**) — what this does and why, in a sentence or two.
2. **## The bug — proof** — for any accuracy fix: what the docs claimed, why it is wrong, and the source evidence (file, symbol, commit) for the correct value. Skip for pure additions.
3. **## What changed** — the concrete edits.
4. **## Context checklist** — the table above, with a status and note per row. Include only rows that are meaningful for the change; keep `❌` rows, since they are the point.
5. **Deliberately not done / flagged** — anything intentionally left, and why.

**Keep it current.** The description describes the branch, not the first commit. Whenever you add a commit that changes the content, update the affected sections **and** re-assess the context checklist in the same step — a later commit often adds source verification or a spec reference that flips a `⚠️` to `✅`. A stale checklist is worse than none, because it is read as a claim about the work.

## Before merge: the release check

Pages are often written before the SDKs and UIKits ship, and go stale the day they do. Before a feature page merges, and again whenever a platform releases:

1. Find the release that contains the feature on each platform (release notes or tags; the `release-notes` skill lists the repos).
2. Re-check every API name, field and behavior against the **released tag**, not the feature branch or PR you first verified against.
3. Name the first version per platform: in `## Platform notes` on SDK pages, in the **Platform Support** `Info` on UIKit pages. Leave a `{/* … */}` placeholder only for a platform that hasn't shipped.
4. Update the PR description in the same step: the hold-the-merge note, checklist rows 4 and 5, and any "not released" items under **Deliberately not done**.

## Enforcement

Pushes run structure/drift gates (`.docs-ops/CI_GATE.md`): `check-mdx.py`, `check-sdk-style.py`, and `check-drift.py`. A PR is blocked if it introduces a new stale (file, API-ref) pair versus `origin/main`. Match the archetype shape so `check-sdk-style.py` passes.

## Related skills

- **`release-notes`** — writing and updating changelogs / release notes across the SDK and UIKit platforms.
