# Flutter doc-as-test framework

Type-checks every `dart` code block in the docs against the real Flutter SDK.

## Quick start

```bash
cd .docs-ops/integration-tests/flutter
dart pub get                    # once; resolves amity_sdk from local path
python3 extract-blocks.py       # extracts dart blocks → results/extracted/*.dart
python3 run-tests.py            # dart analyze each block, writes results/latest.json
```

## What it does

1. **`extract-blocks.py`** — reads `pages.json`, extracts every ` ```dart ` block.
   - Wraps each snippet in `Future<void> docSnippet({...}) async { … }`
   - Hoists `import` statements from the block to file-level
   - Honors `<!-- doc-as-test: skip -->` / `{/* doc-as-test: skip */}` markers
   - Writes `// source: <page>:<start>-<end>` as first line

2. **`run-tests.py`** — runs `dart analyze` per file, parses output.
   - `error` → blocking failure
   - `warning` → counted, non-blocking
   - Emits `results/latest.json` with per-page and per-block breakdowns

## Skipping a block

Add a skip marker on the line before the opening fence:

```markdown
<!-- doc-as-test: skip(reason) -->
```dart
// this block will be skipped
```
```

## Interpreting results

`results/latest.json` fields:

| field | meaning |
|---|---|
| `stats.blocks_extracted` | total dart blocks found |
| `stats.blocks_skipped` | blocks with skip markers |
| `stats.blocks_passed` | analyzed and clean |
| `stats.blocks_failed` | analyzed and have errors |
| `failures[]` | source_page, line range, error messages |

## Adding pages

Edit `pages.json`. Use `enumerate:<dir>` to include all `.mdx` files in a directory.
