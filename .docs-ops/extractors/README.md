# SDK Surface Extractors

Each extractor walks its platform's SDK source (or compiled artifact) and emits a structured JSON surface file consumed by the validators, PR-bot, and rubric scorer.

## Extractors

| File | Platform | Source | Output |
|---|---|---|---|
| `typescript-extractor.py` | TypeScript | `AmityTypescriptSDK` barrel + nested namespaces | `sdk-surface/typescript.json` |
| `ios-extractor.py` | iOS | Swift source (regex + brace-depth) | `sdk-surface/ios.json` |
| `android-extractor.py` | Android | Kotlin/Java source | `sdk-surface/android.json` |
| `flutter-extractor.py` | Flutter | Dart barrel re-exports | `sdk-surface/flutter.json` |
| `ios-docc-extractor.py` | iOS (pilot) | Compiled `.abi.json` from xcframework | `sdk-surface/ios-from-docc.json` |

## Running extractors

```sh
# TypeScript (SP_SDKS_ROOT must point to sp-sdks/ parent)
python3 .docs-ops/extractors/typescript-extractor.py

# iOS (regex, current primary)
python3 .docs-ops/extractors/ios-extractor.py

# iOS (ABI/DocC pilot — uses vendor xcframework, no SDK clone needed)
python3 .docs-ops/extractors/ios-docc-extractor.py

# Android
python3 .docs-ops/extractors/android-extractor.py

# Flutter
python3 .docs-ops/extractors/flutter-extractor.py
```

## iOS migration in progress

**Current primary**: `ios-extractor.py` (regex) → `sdk-surface/ios.json`  
**Pilot**: `ios-docc-extractor.py` (ABI JSON) → `sdk-surface/ios-from-docc.json`

The ABI-based extractor reads the compiled `.abi.json` embedded in `AmitySDK.xcframework`'s `.swiftmodule` — the same xcframework used by the iOS doc-as-test suite. No additional SDK repo access or build step required.

See `.docs-ops/evals/ios-surface-comparison.md` for the full side-by-side comparison and migration recommendation.

**To compare both surfaces:**
```sh
python3 .docs-ops/extractors/ios-extractor.py
python3 .docs-ops/extractors/ios-docc-extractor.py
# Then review: .docs-ops/evals/ios-surface-comparison.md
```

**Decision to swap** `ios.json` → `ios-from-docc.json` as primary is pending resolution of ~52 "regex-only, non-streaming" refs documented in Section 3 of the comparison report.

## Surface JSON schema

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
