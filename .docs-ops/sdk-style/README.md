# SDK Page Style Contract

This contract keeps SDK pages predictable for developer integrators, product readers, and AI tools.

## Page Shape

SDK procedure pages should use this order:

1. Frontmatter `title` and `description`.
2. One short lead paragraph that says what the page helps the reader do.
3. An `Info`, `Note`, `Warning`, or `Tip` only when there is a real availability or behavior caveat.
4. `## Parameters` for create, update, query, delete, or action pages with SDK inputs.
5. Method sections such as `## Create an event`, `## Query events`, or `## Delete a channel`.
6. `## Platform notes` for SDK differences that do not belong inside snippets.
7. `## Related topics` with `CardGroup` links when useful.

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

## Method Sections

Every method section should include a short explanation before the code:

- What the method does.
- When to use it.
- The important required inputs or permission caveats.

If a method has several important inputs, add a compact parameters table before the `CodeGroup`.

## Cards

- Use `CardGroup` at the bottom for related topics on procedure pages.
- Use top-of-page cards mainly on overview pages where they act as navigation.
- Do not use cards as decorative summaries of code examples.
