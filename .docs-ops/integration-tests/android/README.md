# Android Doc-as-Test Framework

Extracts every ` ```kotlin ` and ` ```java ` code block from the MDX documentation pages listed in `pages.json`, compiles each block against the real Amity Android SDK JARs using the Kotlin compiler, and reports any errors. This catches API mismatches and broken examples before they reach readers.

## Quick start

```bash
cd .docs-ops/integration-tests/android

# 1. Extract code blocks from docs
python3 extract-blocks.py

# 2. Compile and report
python3 run-tests.py

# Results are in results/latest.json
```

## How it works

### `extract-blocks.py`

- Walks every page listed in `pages.json`
- Finds ` ```kotlin Android ` and ` ```java ` fenced blocks
- Wraps Kotlin blocks in a `fun docSnippet(...)` function with a large set of preamble imports and pre-declared params (userId, channelId, postRepository, etc.) so most SDK calls resolve without extra scaffolding
- Wraps Java blocks in a `class DocSnippetBlockN { void docSnippet() {} }` class
- Hoists `import` statements from block bodies to file-level
- Respects skip markers: put `<!-- doc-as-test: skip(reason) -->` on the line immediately before a fenced block to exclude it from compilation

### `run-tests.py`

- Builds a full classpath: Amity SDK JARs + rxjava3 + android.jar + kotlin-stdlib + annotations + rxandroid + paging-common + gson + joda-time + reactive-streams
- Compiles each `.kt` file via `K2JVMCompiler -Xskip-metadata-version-check` (needed because the SDK was compiled with Kotlin 2.2.0 metadata but the compiler available is 1.9.22)
- Emits `results/latest.json` with per-block pass/fail detail

## Skip markers

Place the marker on the line **immediately before** the opening fence:

```mdx
<!-- doc-as-test: skip(gradle-dsl: not Kotlin runtime code) -->
```kotlin Gradle (Kotlin DSL)
implementation("co.amity.android:amity-sdk:x.y.z")
```
```

Accepted marker formats:
- `<!-- doc-as-test: skip(reason) -->` (HTML comment — works in MDX)
- `{/* doc-as-test: skip(reason) */}` (JSX comment — also works)

## Output: `results/latest.json`

```jsonc
{
  "run_at": "2025-...",
  "stats": {
    "blocks_extracted": 70,
    "blocks_skipped": 9,
    "blocks_passed": 70,
    "blocks_failed": 0,
    "blocks_warned": 4
  },
  "by_page": { ... },
  "failures": []
}
```

## Requirements

| Dependency | Resolved from |
|---|---|
| Kotlin compiler 1.9.22 | `~/.gradle/wrapper/dists/gradle-8.7-bin/…/lib/kotlin-compiler-embeddable-1.9.22.jar` |
| android.jar (API 34) | `~/Library/Android/sdk/platforms/android-34/android.jar` |
| amity-sdk classes.jar | `../../sdk-surface/` → `Amity-Social-Cloud-SDK-Android/amity-sdk/…` |
| rxjava, rxandroid, paging-common, gson, joda-time | Downloaded by `run-tests.py` on first run |

The runner script resolves all paths automatically. No manual setup needed beyond having the Android SDK installed.

## Adding new pages

Edit `pages.json` and add the relative path (from `social-plus-docs/`) under the appropriate track key (`chat_track`, `social_track`, etc.).
