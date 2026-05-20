# Flutter Surface Comparison: regex extractor vs `dartdoc` index.json

Generated: 2026-05-20  
Extractor pilot: `flutter-dartdoc-extractor.py` v0.2.0-dartdoc  
Source artifact: `dartdoc --output /tmp/flutter-dartdoc-out` (dartdoc 9.0.4, Dart 3.9.2)  
Approach used: **Approach 2** — `dartdoc` HTML generation + `index.json` parsing  
Approach 1 (`--output-format json`) was unavailable in dartdoc 9.0.4.  
Approach 3 (dart analyzer API) was not needed.

---

## Section 1 — Stats Delta

| Metric | `flutter.json` (regex) | `flutter-from-dartdoc.json` | Delta |
|---|---|---|---|
| Types (classes + enums) | 325 | 336 | **+11** (dartdoc finds more) |
| Classes | ~265 (inferred) | 276 | +11 |
| Enums | ~60 | 60 | 0 |
| Extensions | 4 | 69 | **+65** (regex missed most) |
| Typedefs | 2 | 2 | 0 |
| Members (all types) | 1,549 | 1,801 | +252 (gross) |
| Members excl. enum values | 1,327 | 1,801 | **+474** (dartdoc more complete) |
| Enum values (individual) | 222 | 0¹ | −222 (dartdoc limitation) |

¹ Dart's traditional enum constants (`BAN_USER`, `EDIT_USER`, etc.) are **not
indexed** individually in dartdoc's `index.json`. Only the synthetic `.values`
property (one per enum) appears. This is a fundamental limitation of the
index.json approach — see Section 5 for implications.

---

## Section 2 — In dartdoc, Not in Regex

### 2a — 11 new types (regex missed entirely)

All 11 are `class` kind, legitimately public (listed in `amity_sdk` library):

| Type | Members | Likely reason regex missed |
|---|---|---|
| `AddReactionQueryBuilder` | 3 | Defined in a less-scanned source file |
| `AmityUploadCancel` | 1 | Sealed class variant — brace-tracking limitation |
| `AmityUploadComplete` | 3 | Sealed class variant |
| `AmityUploadError` | 3 | Sealed class variant |
| `AmityUploadInProgress` | 4 | Sealed class variant |
| `AmityUploadResult` | 10 | Abstract/sealed base |
| `LiveCollection` | 24 | Generic class with type params — regex pattern gap |
| `LiveCollectionStream` | 8 | Generic class |
| `LiveResult` | 4 | Generic class |
| `LiveResultStream` | 6 | Generic class |
| `PagingController` | 19 | External class re-exported by the SDK |

**Pattern**: regex missed sealed class variants (`AmityUpload*`) and generic
utility classes (`Live*`, `PagingController`). Both patterns are real public
API. `LiveCollection` alone has 24 members that docs may reference.

### 2b — 65 new extensions (regex missed most)

The regex extractor only captured 4 of 69 extensions. The 65 missing are
extensions on enum types that follow the `Amity<EnumName>Extension` naming
convention (e.g., `AmityChannelExtension on AmityChannel`,
`AmityPermissionExtension on AmityPermission`).

These extensions add helper methods (`toValue()`, `fromValue()`, string
conversions) to enum types. They are heavily used in SDK consumer code and
likely referenced in documentation snippets.

Sample of missed extensions:
- `AmityAdPlacementExtension`, `AmityChannelExtension`,
  `AmityPermissionExtension` — 65 total, ~171 methods invisible to regex.

---

## Section 3 — In Regex, Not in dartdoc

**Count: 0 types** — dartdoc is a strict superset of the regex surface for
type names. This confirms the regex extractor has no false positives at the
type-name level.

**Enum values**: 222 enum constants (`BAN_USER`, `USER`, `COMMUNITY`, etc.)
are indexed by regex but absent from dartdoc's `index.json`. This is a
known dartdoc limitation (see Section 1 footnote), not a regex false
positive. The values are visible in the dartdoc HTML pages but not in
`index.json`.

---

## Section 4 — Same Name, Different Shape

### 4a — Kind differences: `abstract_class` vs `class` (11 types)

The regex extractor emits `abstract_class` for types where it detects the
`abstract` modifier; dartdoc's index collapses all non-enum types to `class`
(kind=3). No data loss — just a schema difference.

Affected types: `AccessTokenRenewal`, `AmityCommentData`, `AmityFileInfo`,
`AmityMentionMetadata`, `AmityMessageCreator`, `AmityMessageData`,
`AmityPostData`, `CommentAttachment`, `CommentCreator`, `PostCreator`.

### 4b — Significant member count deltas (shared types, |Δ| > 10)

| Type | Regex members | dartdoc members | Delta | Root cause |
|---|---|---|---|---|
| `AmityPermission` | 32 | 1 | −31 | Enum values not indexed by dartdoc |
| `AmityStory` | 3 | 29 | +26 | Regex under-counted getters |
| `AmityPost` | 14 | 36 | +22 | Regex missed getters from extensions |
| `AmityComment` | 10 | 31 | +21 | Same pattern |
| `AmityCommunity` | 10 | 30 | +20 | Same pattern |
| `AmityMessage` | 12 | 32 | +20 | Same pattern |
| `AmityChannel` | 7 | 25 | +18 | Same pattern |
| `AmityStream` | 0 | 18 | +18 | Regex missed entire class body |
| `AmityContentFlagReasonType` | 9 | 1 | −8 | Enum values not indexed |
| `AmityDataType` | 9 | 1 | −8 | Enum values not indexed |

The negative deltas (`AmityPermission`, `AmityContentFlagReasonType`, etc.)
are all enums whose individual values are not in dartdoc's index.json.  
The positive deltas are real gaps in the regex extractor — methods and
getters that regex's brace-tracking and line-pattern matching missed.

---

## Section 5 — Coverage Analysis

### False positives (regex finds things that shouldn't be public)

**0 confirmed false positives** at the type-name level. Regex matches
dartdoc exactly where dartdoc has data.

### False negatives (regex misses public API)

| Category | Count | Impact |
|---|---|---|
| Missing types (sealed + generic classes) | 11 | Medium — includes `LiveCollection` (24 members) |
| Missing extensions | 65 (−171 methods) | High — enum helper methods heavily used in code snippets |
| Missing class members (getters/methods) | +474 net | Medium–High — core types like `AmityPost`, `AmityComment` under-counted |
| Enum values (regex-only, not in dartdoc index) | 222 | Low — dartdoc limitation, not a regex false negative |

### Cross-platform comparison table

| Platform | Regex false positives | Regex false negatives (types) | dartdoc/AST advantage | Recommendation |
|---|---|---|---|---|
| **iOS** | ~149 (EkoStreamPublisher paths) | 26 SIGNATURE_CHANGE + 4 REMOVED | DocC catches real removals | ✅ **Swapped to ABI** |
| **Android** | ~568 vendor types + ~134 internals | Several Companion methods | Dokka enforces suppress rules | ✅ **Swapped to Dokka** |
| **TypeScript** | 33 @hidden symbols | 2 new functions | TypeDoc honors @hidden natively | ✅ **Swapped to hybrid** |
| **Flutter** | 0 (type names) | 11 types + 65 extensions + 474 member gap | dartdoc finds more + extensions | 🟡 **Hybrid recommended** (see §6) |

---

## Section 6 — Recommendation

### Verdict: Hybrid approach (same pattern as TypeScript)

**dartdoc index.json is strictly better for type names and class members**
but has one critical gap: **individual enum values are not indexed**.  
The regex extractor has that gap closed. Neither alone is complete.

#### Proposed hybrid architecture

```
Pass 1 — dartdoc index.json (primary)
  └─ Types: 336 types (276 classes + 60 enums)
  └─ Extensions: 69 extensions (+65 vs regex)
  └─ Members: 1,801 (constructors, methods, getters)

Pass 2 — regex extractor (enum values only)
  └─ For each enum type found in Pass 1:
     read the enum's source file → extract named constants
  └─ Adds 222 enum values back to the surface

Merge:
  └─ dartdoc wins for all class/extension members
  └─ Enum values appended per type from regex pass
  └─ No collision (dartdoc emits only `.values` synthetic; regex emits named consts)
```

This mirrors the TypeScript hybrid pattern: TypeDoc (dartdoc equivalent) as
the primary pass, targeted regex for the gap TypeDoc/dartdoc can't close.

#### Estimated gains from swap

- **+11 types** currently undocumented (public API dark spots)
- **+65 extensions** (171 methods) brought into drift tracking
- **+474 non-enum-value members** for existing types → more accurate
  doc-as-test reference surface
- **0 false positives introduced** (dartdoc is already a strict superset)

#### Implementation note: enum values via regex

The regex pass needs only to extract enum constants — a simpler pattern than
the full extractor. A targeted scanner:
```python
# for each enum name, find its source .dart file and extract constant names
import re
ENUM_VALUE_RE = re.compile(r'^\s{2,}([A-Z][A-Z0-9_]*)\b', re.MULTILINE)
```
This is far less fragile than the full brace-tracking regex, because enum
value names are uppercase-only and always indented inside the enum block.

#### Alternative: parse dartdoc HTML pages for enum values

Each enum has a generated `amity_sdk/<EnumName>.html` that lists all values.
Parsing HTML is more brittle than regex against source, so the source-regex
approach above is preferred.

#### What this pilot doesn't yet answer

- **Signature richness**: dartdoc `index.json` doesn't include method
  signatures (parameter types, return types). The HTML pages do, but
  parsing is complex. For signature-based doc-as-test improvements, the
  Dart analyzer programmatic API (Approach 3) would be needed. This is
  future work — current doc-as-test uses compile-check semantics which
  don't depend on extractor signatures.
- **@internal filtering**: No `@internal` annotations observed in this
  SDK (no `package:meta` dependency found). Not a concern for now.

#### Next task

A follow-up task to implement the hybrid Flutter extractor (Pass 1 = dartdoc
index.json + Pass 2 = enum-value regex), swap `flutter.json`, and update the
validator allowlist — same pattern as TS task 0081.
