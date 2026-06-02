# Archived pages

These `.mdx` pages were **soft-deleted** from the live docs: they are not in
`docs.json` navigation and nothing in the live docs links to them (verified by
transitive link-reachability from in-nav pages).

They are kept here, with their original paths preserved under `archived/`, so
the content is recoverable and reviewable rather than lost. They are **not**
built or served by Mintlify (only pages in `docs.json` navigation are).

Mostly legacy duplicate trees superseded by the current structure
(e.g. old `social/communities`, `social/posts`, `social/comments`, `social/feed`,
`video/` → `video-new/`) plus Mintlify starter-template leftovers.

To restore a page: `git mv archived/<path> <path>` and add it to `docs.json`.
