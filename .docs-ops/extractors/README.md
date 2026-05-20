# SDK Surface Extractors

Each extractor walks its platform's SDK source (or compiled artifact) and emits a structured JSON surface file consumed by the validators, PR-bot, and rubric scorer.

## Extractors

| File | Platform | Source | Output |
|---|---|---|---|
| `typescript-extractor.py` | TypeScript | `AmityTypescriptSDK` barrel + nested namespaces | `sdk-surface/typescript.json` |
| `typescript-typedoc-extractor.py` | TypeScript | TypeDoc JSON from `src/index.ts` (**pilot**) | `sdk-surface/typescript-from-typedoc.json` |
| `ios-docc-extractor.py` | iOS | Compiled `.abi.json` from xcframework (**primary**) | `sdk-surface/ios.json` |
| `ios-extractor.py` | iOS | Swift source regex (**DEPRECATED**) | _(retired)_ |
| `android-dokka-extractor.py` | Android | Dokka GFM output (**primary**) | `sdk-surface/android.json` |
| `android-extractor.py` | Android | Kotlin/Java source regex (**DEPRECATED**) | _(retired)_ |
| `flutter-extractor.py` | Flutter | Dart barrel re-exports | `sdk-surface/flutter.json` |

## Running extractors

```sh
# TypeScript — regex (current primary, SP_SDKS_ROOT must point to sp-sdks/ parent)
python3 .docs-ops/extractors/typescript-extractor.py

# TypeScript — TypeDoc pilot (requires pre-built TypeDoc JSON)
# cd AmityTypescriptSDK/packages/sdk
# npm install --no-save --legacy-peer-deps typedoc
# npx typedoc --json /tmp/typedoc-output.json src/index.ts --tsconfig tsconfig.json --skipErrorChecking --excludeExternals
python3 .docs-ops/extractors/typescript-typedoc-extractor.py /tmp/typedoc-output.json

# iOS (ABI — no SDK clone needed, reads vendor xcframework)
python3 .docs-ops/extractors/ios-docc-extractor.py

# Android (primary — Dokka GFM, requires pre-built artifact)
# cd Amity-Social-Cloud-SDK-Android
# ANDROID_HOME=~/Library/Android/sdk ./gradlew :amity-sdk:dokkaGfm
python3 .docs-ops/extractors/android-dokka-extractor.py    # primary (Dokka GFM)
python3 .docs-ops/extractors/android-extractor.py          # DEPRECATED (regex, retained for reference)

# Flutter
python3 .docs-ops/extractors/flutter-extractor.py
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

## TypeScript migration: pilot in progress (task 0080)

**Current primary**: `typescript-extractor.py` (regex v1.3) → `sdk-surface/typescript.json`  
**Pilot**: `typescript-typedoc-extractor.py` (TypeDoc) → `sdk-surface/typescript-from-typedoc.json`

**Key findings** (see `.docs-ops/evals/typescript-surface-comparison.md` for full details):
- TypeDoc catches 2 new public functions (`getCommunityByIds`, `getSubChannelByIds`) that survived 4 regex refinement rounds
- TypeDoc correctly excludes 33 `@hidden`-tagged internal symbols that regex was over-capturing
- **Structural gap**: `declare global namespace Amity {}` (~946 members) not captured by TypeDoc
- Recommendation: **hybrid merger** (TypeDoc for namespaced exports + targeted `@types/` scan for `Amity.*`) rather than direct swap. Follow-up task 0082.

**TypeDoc invocation that worked**: `src/index.ts` with `--tsconfig tsconfig.json --skipErrorChecking --excludeExternals` from `packages/sdk/`. The `dist/index.d.ts` approach failed (TypeDoc couldn't resolve the tsconfig). Source-based approach produces a 2.4 MB JSON in ~10s.



All extractors emit the same top-level shape (platform-specific fields may vary):

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
