# Use Cases Documentation Guide

> **For AI agents and contributors.** This file documents the conventions, structure, and rules for the Use Cases tab so future work stays consistent with what's already built.

---

## Purpose

The Use Cases tab answers: _"I want to build X — where do I start and how do I connect everything?"_

It bridges the SDK reference (deep, per-API docs) with real developer workflows. Each guide walks through a complete feature end-to-end, linking back to SDK reference pages for full multi-platform code.

**Target audience:** Developers building with the social.plus SDK. Not PMs, not marketing.

---

## File Structure

```
use-cases/
├── overview.mdx                          # Landing page — domain chooser + quick reference table
├── USE-CASES-GUIDE.md                    # This file — conventions for contributors
└── social/
    ├── overview.mdx                      # Social hub — architecture diagram, card groups, learning paths
    │
    │  Building Blocks
    ├── build-a-social-feed.mdx
    ├── rich-content-creation.mdx
    ├── comments-and-reactions.mdx
    ├── community-platform.mdx
    ├── user-onboarding-and-visitor-mode.mdx
    ├── polls-and-interactive-content.mdx
    │
    │  Engagement & Growth
    ├── user-profiles-and-social-graph.mdx
    ├── stories-and-ephemeral-content.mdx
    ├── notifications-and-engagement.mdx
    ├── events-and-activities.mdx
    ├── content-sharing-and-deep-links.mdx
    ├── realtime-presence-and-activity.mdx
    ├── post-impressions-and-creator-analytics.mdx
    │
    │  Discovery & Safety
    ├── search-and-discovery.mdx
    ├── content-moderation-pipeline.mdx
    ├── roles-permissions-and-governance.mdx
    ├── user-search-and-people-discovery.mdx
    │
    │  Video & Monetization
    ├── livestream-and-video-posts.mdx
    ├── short-form-video-clips.mdx
    └── advertising-and-monetization.mdx
```

Future domains (Chat, Cross-Feature) will follow the same `use-cases/<domain>/` pattern.

---

## Shared Snippets

Reusable code snippets live in `snippets/social/` and are imported into **both** use-case guides and SDK reference pages as a single source of truth.

```
snippets/social/
├── posts/create-text-post.mdx
├── communities/create-community.mdx
├── feeds/get-user-feed.mdx
├── relationships/follow-user.mdx
├── relationships/unfollow-user.mdx
├── reactions/add-reaction.mdx
├── reactions/remove-reaction.mdx
├── stories/create-image-story.mdx
├── moderation/flag-post.mdx
├── search/search-posts.mdx
├── notifications/get-notification-tray-items.mdx
└── events/create-event.mdx
```

### Snippet rules

1. **Source of truth = SDK reference pages.** Snippet code must be extracted from the actual SDK reference files, never written freehand.
2. **Multi-platform.** Each snippet contains a `<CodeGroup>` with iOS (Swift), Android (Kotlin), TypeScript, and Flutter (Dart) where available. Some features only support 3 platforms — that's fine.
3. **Import syntax:**
   ```mdx
   import CreateTextPost from '/snippets/social/posts/create-text-post.mdx';
   ```
   Then use `<CreateTextPost />` in the body.
4. **Shared across tabs.** The same snippet file is imported in both the use-case guide and the corresponding SDK reference page. If you update a snippet, both pages update.

---

## Guide Template

Every guide follows this exact structure. Do not deviate.

```
---
title: "Guide Title"
description: "One-line description"
---

import SnippetName from '/snippets/social/...';

# Guide Title

One-paragraph intro explaining what this guide covers and why.

[mermaid diagram — architecture/flow for the feature]

## What You'll Build

<CardGroup cols={2}>
  [4 cards summarizing the key capabilities]
</CardGroup>

## Prerequisites

- SDK installed and authenticated → link to setup
- Any feature-specific prereqs

---

## Quick Start: [Core Operation]

[Brief intro sentence]

<SnippetName />

Full reference → [Link](/path)

---

## Step-by-Step Implementation

<Steps>
  [Each step has: title, 2-3 sentence description, TypeScript code hint, "Full reference → [Link]"]
</Steps>

---

## Connect to Moderation & Analytics

<AccordionGroup>
  [2-3 accordions linking the feature to Admin Console, webhooks, and analytics]
</AccordionGroup>

---

## Best Practices

<AccordionGroup>
  [2-4 accordions: Performance, UX, Security/Privacy, domain-specific]
</AccordionGroup>

---

## Next Steps

<CardGroup cols={3}>
  [3 cards linking to related guides]
</CardGroup>
```

---

## Code Hint Rules

Each step in the "Step-by-Step Implementation" section includes a **TypeScript code hint** — a trimmed, representative code block showing the key API call.

### Rules

1. **TypeScript only.** Use TypeScript as the single inline code hint. Full multi-platform code lives in the SDK reference pages (linked via "Full reference →").
2. **Source of truth = SDK reference pages.** Extract code from the actual reference `.mdx` files. Never invent API calls.
3. **Keep hints short.** 3-10 lines showing the essential method call + key parameters. Strip boilerplate, error handling, and full class wrappers.
4. **Use ` ```typescript TypeScript ` fencing.** The label "TypeScript" appears as a tab label in Mintlify.
5. **One hint per step.** If a step references multiple operations, pick the primary one.
6. **Backend code exception.** Steps involving server-side operations (webhooks, pre-hooks) use ` ```javascript Node.js ` instead of TypeScript.
7. **No code is okay for pure-config steps.** If a step is about Admin Console configuration or choosing settings, a description + link is sufficient.

### Link format

Always use this exact format after code hints:

```
Full reference → [Page Title](/path/to/page)
```

- Use `→` (Unicode arrow), not `->` or `>`
- **Never** write "Full reference with code examples →" — just "Full reference →"
- For multiple links: `Full reference → [Page A](/path-a) · [Page B](/path-b)`

---

## Quick Start Section Rules

1. The Quick Start uses a **shared snippet** (`<SnippetName />`) — multi-platform code from `snippets/social/`.
2. **Do not repeat the Quick Start as Step 1.** The first step in "Step-by-Step Implementation" must cover the *next* operation after the Quick Start, not restate it.
3. Add a "Full reference → [Link]" line below the snippet.

---

## Navigation (docs.json)

The Use Cases tab sits between UIKit and Analytics & Moderation. Structure:

```json
{
  "tab": "Use Cases",
  "groups": [
    { "group": "Use Cases", "pages": ["use-cases/overview"] },
    {
      "group": "Social",
      "pages": [
        "use-cases/social/overview",
        {
          "group": "Building Blocks",
          "pages": [
            "use-cases/social/build-a-social-feed",
            "use-cases/social/rich-content-creation",
            "use-cases/social/comments-and-reactions",
            "use-cases/social/community-platform"
          ]
        },
        {
          "group": "Engagement & Growth",
          "pages": [
            "use-cases/social/user-profiles-and-social-graph",
            "use-cases/social/stories-and-ephemeral-content",
            "use-cases/social/notifications-and-engagement",
            "use-cases/social/events-and-activities"
          ]
        },
        {
          "group": "Discovery & Safety",
          "pages": [
            "use-cases/social/search-and-discovery",
            "use-cases/social/content-moderation-pipeline"
          ]
        }
      ]
    }
  ]
}
```

When adding new guides:
- Add the `.mdx` file to the appropriate sub-group
- Update `use-cases/social/overview.mdx` card groups to include it
- Update `use-cases/overview.mdx` quick reference table
- If it's a new domain (Chat, Video), create a new group block

---

## Content Quality Checklist

Before considering a guide complete:

- [ ] **Code accuracy** — Every TypeScript hint matches the SDK reference page it links to. Never invent API calls.
- [ ] **No Quick Start / Step 1 duplication** — Step 1 covers a different operation than the Quick Start snippet.
- [ ] **No thin steps** — Every step has at least a 2-sentence description. Steps with code should have a code hint. One-sentence-only steps are not acceptable.
- [ ] **Consistent link format** — All reference links use `Full reference → [Title](/path)`. No "with code examples" variation.
- [ ] **Mermaid diagram** — Every guide has a flow/architecture diagram after the intro paragraph.
- [ ] **Connect to Moderation & Analytics** — Every guide has at least 2 accordions linking to Admin Console, webhooks, or analytics features.
- [ ] **Best Practices are specific** — Bullet points include concrete numbers, thresholds, or patterns (e.g., "300ms debounce", "compress to ≤1MB"). No generic advice.
- [ ] **Next Steps cards** — 3 cards linking to related guides. No self-links.
- [ ] **Link checker passes** — Run `python3 tools/check_internal_links.py` and confirm 0 broken links.
- [ ] **No UIKit content** — Use Cases are SDK-only. No UIKit tabs, imports, or references.

---

## Overview Page Conventions

### `use-cases/overview.mdx` (Landing page)
- Domain chooser with CardGroup (Social, Chat, Video, Cross-Feature)
- "How to Use These Guides" Steps section explaining the guide structure
- Quick Reference table mapping "If you want to..." → guide link
- "Coming soon" cards use `href="#"` as placeholder

### `use-cases/social/overview.mdx` (Social hub)
- Mermaid architecture diagram showing how features connect
- Three CardGroup sections: Building Blocks, Engagement & Growth, Discovery & Safety
- Each card has a subtitle line starting with `SDK:` listing key APIs
- "Suggested Learning Paths" AccordionGroup with 3 paths: Instagram-like, Reddit/Discord-like, Adding social to existing app

---

## Common Mistakes to Avoid

1. **Using CommentRepository code in a post-creation context** (or vice versa). Always match the repository to the content type.
2. **Showing a query/list operation when the step describes a create/send operation** (e.g., showing `getMyCommunityInvitations` instead of `createInvitations`).
3. **Showing a single-entity fetch when the step describes a list query** (e.g., `getEvent('id')` vs `getEvents({ communityId })`).
4. **Copying code from mentor memory or conversation context instead of the actual SDK reference files.** Always verify against the `.mdx` source.
5. **Adding UIKit content.** The Use Cases tab is SDK-only for now.
6. **Over-engineering steps.** Keep prose concise — 2-3 sentences per step is ideal. The code hint + reference link does the heavy lifting.
7. **Using `\n` for line breaks inside mermaid node labels.** Mintlify renders `\n` literally. Use `<br/>` instead (e.g., `A[Line one<br/>Line two]`).
