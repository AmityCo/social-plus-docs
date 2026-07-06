# SDK Page Style Contract

This contract keeps SDK pages predictable for developer integrators, product readers, and AI tools.

## Page Archetypes

SDK pages do not all share one structure. Choose the contract that matches the page's job:

| Archetype | Use for | Required shape |
| --- | --- | --- |
| `overview` | Capability maps, section introductions, navigation hubs | Clear intro, concept map or cards, links onward. Parameters and snippets are optional. |
| `concept` | Behavioral models, SDK concepts, lifecycle explanations | Defines terms and platform behavior. Code is optional. |
| `operation` | Method/task pages such as create, get, query, update, delete, flag, join, mute | Intro, `## Parameters`, task/method sections, `CodeGroup` snippets, related topics. |
| `setup` | Installation, quick starts, authentication, platform setup | Ordered setup flow, prerequisites, config snippets. Parameters are optional unless SDK call inputs are documented. |
| `migration` | Version moves, before/after changes, compatibility notes | Compatibility context, old/new behavior, migration steps, warnings. |
| `reference-lite` | Method groups, enums, option tables | Tables and concise examples. Snippets are optional. |

The style checker infers archetypes from path, title, and code fences. For unusual pages, add frontmatter:

```yaml
sdk_page_type: concept
```

Valid values are `overview`, `concept`, `operation`, `setup`, `migration`, and `reference-lite`.

## Page Shape

SDK operation pages should use this order:

1. Frontmatter `title` and `description`.
2. One short lead paragraph that says what the page helps the reader do.
3. An `Info`, `Note`, `Warning`, or `Tip` only when there is a real availability or behavior caveat.
4. `## Parameters` for create, update, query, delete, or action pages with SDK inputs.
5. Method sections such as `## Create an event`, `## Query events`, or `## Delete a channel`.
6. `## Platform notes` for SDK differences that do not belong inside snippets.
7. `## Related topics` with `CardGroup` links when useful.

For single-method operation pages, `## Parameters` should usually be the method's parameter table. For multi-operation pages, use `## Parameters` as a compact operation-level input summary, then add `### Inputs` tables inside method sections when each operation has a different input shape. Avoid mixing result controls such as callbacks, live collections, or pagination handles into a parameter table unless the SDK call accepts them directly as arguments.

## Headings

- Do not add a visible `#` heading in page content. Mintlify renders the frontmatter `title`.
- Do not repeat the page title as the first body heading.
- Prefer task or method headings over platform headings.
- Use sentence case for method headings.

## Code Snippets

- Use `CodeGroup` for SDK language snippets.
- Keep language order consistent: TypeScript, iOS, Android, Flutter.
- Omit unsupported platforms from the `CodeGroup`, then explain the gap in an `Info` note or platform notes.
- Reserve `CardGroup` for related links or navigation, not code.
- TypeScript snippets should be framework-neutral by default. Use React-specific examples only when the page is about UI lifecycle or subscription cleanup; label those snippets as React and include visible React imports.

## Platform Behavior Wording

- Do not describe Live Objects or Live Collections as universal SDK return types.
- Prefer platform-qualified wording:
  - iOS and TypeScript expose Live Object / Live Collection wrappers.
  - Android observes many SDK results with `Flowable<T>` or platform-specific reactive APIs.
  - Flutter may return `Future<T>` for single-object fetches and uses paging/live collection APIs where available.
- If a parameters table describes platform-dependent behavior, include a `Platforms` column.
- Split batch-by-ID lookup and paginated query sections. For example, `getUserByIds` and `getUsers()` should not live under one vague "Get Multiple Users" heading.

## Method Sections

Every method section should include a short explanation before the code:

- What the method does.
- When to use it.
- The important required inputs or permission caveats.

If a method has several important inputs, add a compact parameters table before the `CodeGroup`.

On multi-operation pages, each method section should be self-contained enough that a developer or AI agent can extract the method name, supported platforms, required inputs, and return/observe shape without reading unrelated sections.

## Cards

- Use `CardGroup` at the bottom for related topics on procedure pages.
- Use top-of-page cards mainly on overview pages where they act as navigation.
- Do not use cards as decorative summaries of code examples.
