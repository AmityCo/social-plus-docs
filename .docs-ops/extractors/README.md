# SDK Surface Extractors

Each extractor walks its platform's SDK source (or compiled artifact) and emits a structured JSON surface file consumed by the validators, PR-bot, and rubric scorer.

## Extractors

| File | Platform | Source | Output |
|---|---|---|---|
| `typescript-extractor.py` | TypeScript | `AmityTypescriptSDK` barrel + nested namespaces | `sdk-surface/typescript.json` |
| `ios-docc-extractor.py` | iOS | Compiled `.abi.json` from xcframework (**primary**) | `sdk-surface/ios.json` |
| `ios-extractor.py` | iOS | Swift source regex (**DEPRECATED**) | _(retired)_ |
| `android-extractor.py` | Android | Kotlin/Java source | `sdk-surface/android.json` |
| `flutter-extractor.py` | Flutter | Dart barrel re-exports | `sdk-surface/flutter.json` |

## Running extractors

```sh
# TypeScript (SP_SDKS_ROOT must point to sp-sdks/ parent)
python3 .docs-ops/extractors/typescript-extractor.py

# iOS (ABI — no SDK clone needed, reads vendor xcframework)
python3 .docs-ops/extractors/ios-docc-extractor.py

# Android
python3 .docs-ops/extractors/android-extractor.py

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
