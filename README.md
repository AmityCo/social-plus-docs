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

This repo auto-generates two AI-consumable documentation files per the [llmstxt.org](https://llmstxt.org) spec:

| File | Purpose |
|---|---|
| `llms.txt` | Compact index — title, description, and one-line summary per page. Used by AI tools for discovery. |
| `llms-full.txt` | Full content — all page bodies in clean markdown. Used by RAG pipelines and AI coding tools. |

Both files are automatically regenerated whenever changes are merged to `main`.

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
