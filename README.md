# social.plus Documentation

This repository contains the official documentation for the social.plus SDK, UIKit, and platform.

## Structure

| Directory | Contents |
|---|---|
| `social-plus-sdk/` | SDK docs: Getting Started, Core Concepts, Chat, Social, Video |
| `uikit/` | UIKit docs: components, customization, platform guides |
| `api-reference/` | API reference (OpenAPI) |
| `llmstxt/` | AI documentation generator (see below) |

## AI Documentation (`llms.txt`)

This repo generates two AI-consumable documentation files per the [llmstxt.org](https://llmstxt.org) spec:

| File | Purpose |
|---|---|
| `llms.txt` | Compact index — title, description, and one-line summary per page. Used by AI tools for discovery. |
| `llms-full.txt` | Full content — all page bodies in clean markdown. Used by RAG pipelines and AI coding tools. |

Both files are automatically regenerated whenever changes are merged to `main`.

### Why customized instead of Mintlify's auto-generated version

Mintlify already auto-generates `llms.txt` and `llms-full.txt` on every deploy. We override them with custom files for three reasons:

1. **Curation** — Mintlify's auto-gen includes every page (changelogs, internal pages, placeholders). Our version includes only the pages that are meaningful for developers: SDK guides, UIKit components, and platform references — nothing else.

2. **Clean content** — Mintlify's `llms-full.txt` serves raw MDX. Ours strips JSX components, import statements, and frontmatter so AI tools receive plain markdown with no syntax noise.

3. **Logical structure** — Mintlify lists pages alphabetically. Our version groups pages into meaningful sections (`Chat — Channels`, `Video — Broadcasting`, etc.) so AI tools understand the relationship between pages, not just a flat list.

The custom files live at the repo root and Mintlify automatically uses them in place of its auto-generated versions. The CI workflow keeps them in sync on every merge.

### Running locally

```bash
cd llmstxt

# Preview output without writing files
go run ./cmd/main.go -dry-run -verbose

# Generate llms.txt and llms-full.txt
go run ./cmd/main.go
```

### Adding or removing pages

Edit `llmstxt/llms-config.yml` to add, remove, or reorder pages. Each entry is a path relative to the repo root.

```yaml
sections:
  - title: "My Section"
    pages:
      - path: social-plus-sdk/my-feature/overview.mdx
```

Then run `go run ./cmd/main.go` to regenerate.

### How it works

1. Reads `llmstxt/llms-config.yml` for the curated page list
2. Parses each `.mdx` file — strips JSX components, imports, and frontmatter
3. Assembles `llms.txt` (index) and `llms-full.txt` (full content) per the llmstxt.org spec
## AI Skills (MCP)

social.plus exposes a [Mintlify MCP server](https://mintlify.com/docs/ai/model-context-protocol) at `https://learn.social.plus/mcp`, giving AI coding tools (Claude Code, Cursor, Windsurf, VS Code + Continue) direct access to the documentation.

### Skill Files

Eight lightweight skill files live under `.mintlify/skills/`. Each one orients an AI agent to a specific product area, then hands off to the MCP search tool and `llms.txt` for deep content.

**Product skills** — one per product area:

| Skill | Path | When it activates |
|-------|------|-------------------|
| Chat | `.mintlify/skills/chat/SKILL.md` | Channels, messages, real-time, unread counts |
| Social | `.mintlify/skills/social/SKILL.md` | Users, communities, posts, feeds, stories |
| Video | `.mintlify/skills/video/SKILL.md` | Rooms, broadcasting, co-hosting, playback |
| UIKit | `.mintlify/skills/uikit/SKILL.md` | Pre-built components, theming, customization |
| Server | `.mintlify/skills/server/SKILL.md` | REST APIs, auth tokens, webhooks, pre-hooks |
| Admin | `.mintlify/skills/admin/SKILL.md` | Console/Portal: moderation, analytics, settings |

**Diagnostic skills** — activated by developer pain, not product area:

| Skill | Path | When it activates |
|-------|------|-------------------|
| Setup Validator | `.mintlify/skills/setup-validator/SKILL.md` | "Is my setup correct?" / SDK or UIKit init problems |
| Troubleshooter | `.mintlify/skills/troubleshoot/SKILL.md` | Integration broken, error code, unexpected behavior |

Mintlify exposes these via the discovery endpoint at `/.well-known/agent-skills/index.json`.

### Design Principle

Skill files intentionally contain **no API signatures or code samples** — those live in the docs and are fetched on demand via `get_page_social_plus`. Skills describe *what the product does, when to use which API, and undocumented gotchas* that aren't in the docs. This keeps skill files durable and low-maintenance as the API evolves.

### MCP Tools

The MCP server exposes two tools to AI agents:

| Tool | Purpose |
|------|---------|
| `search_social_plus` | Full-text search across all documentation pages |
| `get_page_social_plus` | Fetch the full content of a specific page by path |

Skills use these tools to pull live documentation on demand — the skills themselves stay thin.

### Using the MCP Server

Add to your AI tool's config:

```json
{
  "mcpServers": {
    "social-plus": {
      "url": "https://learn.social.plus/mcp"
    }
  }
}
```

| AI Tool | Config location |
|---------|----------------|
| Claude Code | `~/.claude/claude_desktop_config.json` |
| Cursor | Settings → MCP Servers |
| Windsurf | Settings → MCP |
| VS Code + Continue | `.continuerc.json` |

Once connected, skills are discovered automatically — no extra installation needed.

## Docs Quality (`.docs-ops/`)

This repo runs an automated quality system that keeps documentation accurate, consistent, and AI-consumable as the underlying SDKs evolve. It validates against the real SDK source for all four platforms (TypeScript / iOS / Android / Flutter) on every push, and additionally scores each high-traffic doc page on a 5-dimension rubric.

### The layers

Every push runs through these checks; what they catch is complementary:

| Layer | What it catches | Source of truth |
|---|---|---|
| **Regex drift** | Stale API names, renamed methods, removed types, fabricated refs in code blocks | Per-platform SDK surface JSON |
| **Doc-as-test (TS / iOS / Android / Flutter)** | Wrong signatures, arg type mismatches, async/await drift — anything the language's actual type-checker would flag | Real SDK source (compile snippets with `tsc` / `swiftc` / `kotlinc` / `dart analyze`) |
| **MDX structure** | HTML comments inside JSX components (silently break MDX v2 parsing — blanks pages in Mintlify) | Static structural check |

Two further outputs run periodically (not as gates) for visibility:

| Layer | What it produces |
|---|---|
| **Cohort dashboards** | Weekly snapshot of drift per platform per customer cohort (Eastern chat-heavy / Western social-heavy / Shared) at `.docs-ops/dashboards/latest-report.md` |
| **5-dimension rubric scorer** | Per-page weighted scores on Accuracy, Clarity, Cross-platform parity, Completeness, Examples, AI-consumability — useful for content-investment prioritization. Reports at `.docs-ops/rubric-scorer/results/overall-latest-report.md` |

And one workflow runs automatically:

| Workflow | What it does |
|---|---|
| **SDK→docs PR-bot** (daily GH Action) | Polls all four SDK repos; when a public API changes, opens a draft docs PR with auto-rewrites for unambiguous renames and a structured comment listing what changed |

### SDK surface sources

The surface JSON the gates validate against comes from the most authoritative source per platform:

| Platform | Source | Notes |
|---|---|---|
| iOS | `.abi.json` from the vendored `AmitySDK.xcframework` | Apple's Swift ABI artifact; ships with the framework |
| Android | Dokka GFM output | Existing Dokka config in `amity-sdk/build.gradle` already encodes the public/private boundary via `perPackageOption suppress` rules |
| TypeScript | Regex extractor (migration to TypeDoc in progress) | TypeDoc migration pending; see `.docs-ops/extractors/README.md` |
| Flutter | Regex extractor (migration to `dart doc` planned) | Same shape as TS migration |

Old regex extractors remain in-tree as DEPRECATED fallbacks for iOS and Android, available for cross-checks if needed.

### For contributors

One-time setup after cloning:

```bash
pip install pre-commit
pre-commit install --hook-type pre-push
```

Daily: just `git push`. The hook runs the full check suite in a few seconds (longer on first run while toolchains warm up). If anything regresses, the output names the exact file:line and what's wrong.

Manual gate run any time:

```bash
python3 .docs-ops/ci/check-drift.py              # against origin/main
python3 .docs-ops/ci/check-drift.py --base main  # against local main
python3 .docs-ops/ci/check-drift.py --quiet      # one-line summary
```

Bypass (`git push --no-verify`) exists for legitimate exceptions — please file an issue or ping #docs-ops first if you find yourself wanting to use it; usually it means either a validator has a false positive or there's a docs change pattern we should teach the gate.

iOS-specific: the iOS doc-as-test check requires macOS (`swiftc`). On Linux contributor machines the gate gracefully reports iOS as `unavailable` rather than failing — your push isn't blocked.

### How it stays accurate

Two mechanisms keep the system itself from going stale:

- **PR-bot proactive watcher** — the daily GH Action opens a draft PR whenever any SDK's public surface changes. Docs catch up before drift accumulates.
- **Audit trail of every change** — every doc fix has a corresponding task spec + result in `.docs-ops/tasks/done/`. Reviewers (and future maintainers) can trace why each edit happened.

### Deeper reading

- [`.docs-ops/README.md`](.docs-ops/README.md) — the multi-agent task protocol that powers the cleanup pipeline
- [`.docs-ops/CI_GATE.md`](.docs-ops/CI_GATE.md) — full design of the local CI gate
- [`.docs-ops/extractors/README.md`](.docs-ops/extractors/README.md) — per-platform extractor status and migration history
- [`.docs-ops/rubric.json`](.docs-ops/rubric.json) — the 6-dimension rubric definition
- [`.docs-ops/evals/sdk-tickets-to-file.md`](.docs-ops/evals/sdk-tickets-to-file.md) — cross-platform SDK gaps surfaced by the validators (queued for SDK leads to file)
