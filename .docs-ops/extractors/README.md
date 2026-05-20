# SDK Surface Extractors

Each extractor walks its platform's SDK source (or compiled artifact) and emits a structured JSON surface file consumed by the validators, PR-bot, and rubric scorer.

## Extractors

| File | Platform | Source | Output |
|---|---|---|---|
| `typescript-extractor.py` | TypeScript | `AmityTypescriptSDK` barrel + nested namespaces (**DEPRECATED**) | _(retired)_ |
| `typescript-typedoc-extractor.py` | TypeScript | TypeDoc JSON from `src/index.ts` (**pilot, superseded**) | _(retired)_ |
| `typescript-hybrid-extractor.py` | TypeScript | TypeDoc (namespaces) + targeted @types regex (Amity globals) (**primary**) | `sdk-surface/typescript.json` |
| `ios-docc-extractor.py` | iOS | Compiled `.abi.json` from xcframework (**primary**) | `sdk-surface/ios.json` |
| `ios-extractor.py` | iOS | Swift source regex (**DEPRECATED**) | _(retired)_ |
| `android-dokka-extractor.py` | Android | Dokka GFM output (**primary**) | `sdk-surface/android.json` |
| `android-extractor.py` | Android | Kotlin/Java source regex (**DEPRECATED**) | _(retired)_ |
| `flutter-extractor.py` | Flutter | Dart barrel re-exports (**primary — pending swap**) | `sdk-surface/flutter.json` |
| `flutter-dartdoc-extractor.py` | Flutter | `dartdoc` index.json (**pilot in progress**) | `sdk-surface/flutter-from-dartdoc.json` |

## Running extractors

```sh
# TypeScript hybrid (primary — TypeDoc + targeted @types regex for Amity globals)
# Requires pre-built TypeDoc JSON:
#   cd AmityTypescriptSDK/packages/sdk
#   npm install --no-save --legacy-peer-deps typedoc
#   npx typedoc --json /tmp/typedoc-output.json src/index.ts --tsconfig tsconfig.json --skipErrorChecking --excludeExternals
python3 .docs-ops/extractors/typescript-hybrid-extractor.py /tmp/typedoc-output.json

# TypeScript — legacy regex (DEPRECATED, retained for reference)
# python3 .docs-ops/extractors/typescript-extractor.py

# iOS (ABI — no SDK clone needed, reads vendor xcframework)
python3 .docs-ops/extractors/ios-docc-extractor.py

# Android (primary — Dokka GFM, requires pre-built artifact)
# cd Amity-Social-Cloud-SDK-Android
# ANDROID_HOME=~/Library/Android/sdk ./gradlew :amity-sdk:dokkaGfm
python3 .docs-ops/extractors/android-dokka-extractor.py    # primary (Dokka GFM)
python3 .docs-ops/extractors/android-extractor.py          # DEPRECATED (regex, retained for reference)

# Flutter dartdoc runner (pilot — parallel artifact, no swap yet)
# Requires: dart pub global activate dartdoc (one-time)
# cd Amity-Social-Cloud-SDK-Flutter-Internal && dartdoc --output /tmp/flutter-dartdoc-out --no-include-source
python3 .docs-ops/extractors/flutter-dartdoc-extractor.py  # pilot (dartdoc index.json)
python3 .docs-ops/extractors/flutter-extractor.py          # primary (regex, pending swap)
```

## iOS migration: complete (task 0076)

**Primary**: `ios-docc-extractor.py` (ABI JSON) → `sdk-surface/ios.json`  
**Retired**: `ios-extractor.py` (regex, DEPRECATED, retained for reference only)

The ABI-based extractor reads the compiled `.abi.json` embedded in `AmitySDK.xcframework`'s `.swiftmodule` — the same xcframework used by the iOS doc-as-test suite. No additional SDK repo access or build step required.

Migration outcome (see `.docs-ops/evals/ios-surface-comparison.md` for full details):
- ABI catches all 26 SIGNATURE_CHANGE + 4 REMOVED_API doc-as-test findings at extract time
- 651 real new refs surfaced (previously missed by regex)
- 573 regex-only refs correctly excluded (545 streaming lib over-reach + 15 extractor artifacts + 13 access-level mismatches)
- Drift validator: 0 issues after swap

## Android migration: complete (task 0079)

**Primary**: `android-dokka-extractor.py` (Dokka GFM) → `sdk-surface/android.json`  
**Retired**: `android-extractor.py` (regex, DEPRECATED, retained for reference only)

**Key findings** (see `.docs-ops/evals/android-surface-comparison.md` for full details):
- 726 regex-only types are false positives — bundled vendor code (mp4parser, RTMP, GPU filters) + internal suppressed packages
- Dokka adds 2 new types + 177 members on shared types that regex misses
- Migration complete — drift=0, doc-as-test 70/70 ✅

Note: `dokkaJson` task is not wired in the Android SDK Gradle config. `dokkaGfm` is used instead; extractor manually applies the same `perPackageOption` suppress rules from `dokkaHtml`.

## TypeScript migration: complete (task 0081)

**Primary**: `typescript-hybrid-extractor.py` (TypeDoc + targeted @types regex) → `sdk-surface/typescript.json`  
**Retired**: `typescript-extractor.py` (regex v1.3, DEPRECATED) and `typescript-typedoc-extractor.py` (pilot, superseded)

**Why hybrid, not a clean swap** (unlike iOS and Android):
- TypeDoc is authoritative for namespaced exports (24 namespaces) and honors `@hidden`/`@private` natively
- The `declare global { namespace Amity { ... } }` pattern (~946 members) is ambient global augmentation that TypeDoc does not surface from a single `src/index.ts` entry point
- Solution: TypeDoc for namespaces + targeted regex over `src/@types/domains/*.ts` only for the Amity global namespace

**Key findings** (see `.docs-ops/evals/typescript-surface-comparison.md` for full details):
- 2 new functions caught by TypeDoc that survived 4 regex refinement rounds: `getCommunityByIds`, `getSubChannelByIds`
- 33 `@hidden`/`@private`-tagged internal symbols removed from surface (task 0083 / hybrid natively)
- 6 drift items surfaced (docs referencing internal API) — filed as tickets 0083-01 and 0083-02 in `sdk-tickets-to-file.md`
- Amity globals: 946 members unchanged (Pass 2 targeted scan)

**TypeDoc invocation**: `src/index.ts` against `packages/sdk/tsconfig.json` with `--skipErrorChecking --excludeExternals`. Produces 2.4 MB JSON in ~10s.


## Flutter migration: pilot in progress (task 0082)

**Primary (pending swap)**: `flutter-extractor.py` (regex) → `sdk-surface/flutter.json`  
**Pilot**: `flutter-dartdoc-extractor.py` (dartdoc index.json) → `sdk-surface/flutter-from-dartdoc.json`

**Approach used**: Approach 2 (dart doc HTML + index.json parsing). `dartdoc --output-format json` flag does not exist in dartdoc 9.0.4.

**Key findings** (see `.docs-ops/evals/flutter-surface-comparison.md` for full details):
- dartdoc is a **strict superset** of regex at type-name level (0 regex false positives)
- **+11 types** missed by regex (sealed class variants like `AmityUpload*`, generic classes `LiveCollection`, `PagingController`)
- **+65 extensions** missed by regex (~171 methods invisible to drift tracking)
- **+474 non-enum-value members** for shared types — significant class member under-counting in regex
- **Gap**: dartdoc `index.json` does NOT index individual enum constants (222 values are regex-only)

**Recommendation**: Hybrid approach (same as TypeScript migration):
- Pass 1: dartdoc index.json (primary — types, extensions, class members)
- Pass 2: targeted enum-value regex (fill the one gap dartdoc can't close)

Next task: implement hybrid + swap `flutter.json`.

 (platform-specific fields may vary):

```json
{
  "extractor_version": "string",
  "extractor": "filename.py",
  "extracted_at": "ISO8601",
  "sdk_product": "string",
  "types": { "TypeName": { "kind", "primary_decl", "members", "nested_types" } },
  "protocols": { ... },
  "global_funcs": [...],
  "global_consts": [...],
  "stats": { ... }
}
```

The ABI extractor adds an optional `signature: { parameters, returns }` field per member — ignored by current validators, available for future signature-level validation.
