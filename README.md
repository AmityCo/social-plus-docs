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

### Per-Product Skill Files

Four lightweight skill files live under `.mintlify/skills/`. Each one orients an AI agent to a specific product area, then hands off to the MCP search tool and `llms.txt` for deep content:

| Skill | Path | Purpose |
|-------|------|---------|
| Chat | `.mintlify/skills/chat/SKILL.md` | Channels, messages, real-time, unread |
| Social | `.mintlify/skills/social/SKILL.md` | Users, communities, posts, feeds, stories |
| Video | `.mintlify/skills/video/SKILL.md` | Rooms, broadcasting, co-hosting, playback |
| UIKit | `.mintlify/skills/uikit/SKILL.md` | Pre-built components, theming, customization |

Mintlify exposes these via the discovery endpoint at `/.well-known/agent-skills/index.json`.

### Design Principle

The skill files intentionally contain **no API signatures** — those change and live in the docs. Skills describe *what the product does and when to use which API*, then direct the AI to the MCP search tool for current code examples. This keeps skill files durable and low-maintenance.

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

Claude Code: `~/.claude/claude_desktop_config.json`
Cursor: Settings → MCP Servers
