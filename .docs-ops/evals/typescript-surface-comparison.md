# TypeScript Surface Comparison: TypeDoc vs Regex (v1.3)

**Generated**: 2026-05-19  
**Pilot task**: 0080  
**TypeDoc input**: `/tmp/typedoc-output.json` (from `src/index.ts`, `--skipErrorChecking --excludeExternals`)  
**Regex surface**: `.docs-ops/sdk-surface/typescript.json` (extractor v1.3)  
**Parallel surface**: `.docs-ops/sdk-surface/typescript-from-typedoc.json` (extractor v0.2.0-typedoc)

---

## Section 1: Stats Delta

| Dimension | Regex (v1.3) | TypeDoc (v0.2.0) | Delta |
|---|---|---|---|
| Namespaces | 25 | 24 | −1 (Amity global — see §3) |
| Sub-namespaces | 5 | 5 | 0 |
| Namespaced members | 1 328 | 381 | −947 (946 Amity global + 1 @hidden) |
| Amity global members | 946 | 0 | −946 (structural gap — see §5) |
| Root exports | 124 | 176 | +52 (TypeDoc expands enum cases) |
| `@hidden`-tagged exports included | ~33 | 0 | TypeDoc correctly excludes them |

**Surface overlap (non-Amity, non-@hidden):** 374 shared namespaced members out of 381 TypeDoc members (98.2% match).

---

## Section 2: In TypeDoc, Not In Regex — TypeDoc Wins

7 symbols TypeDoc captures that survived all 4 rounds of regex refinement (v1.0 → v1.3):

### New functions (2 genuine API additions)

| Symbol | TypeDoc kind | Why regex missed it |
|---|---|---|
| `CommunityRepository.getCommunityByIds` | function | Barrel re-export not followed by regex barrel-tracker |
| `SubChannelRepository.getSubChannelByIds` | function | Same — barrel re-export in a newer module |

These are real, documented public API functions that should be covered by docs.  Both appear in the SDK's `src/*/api/index.ts` but were not picked up by regex traversal.

### Enum member expansions (5 inline-namespace enums)

TypeDoc expands enum members inline in their parent namespace; the regex extractor captured the enum type only, not its cases:

| Symbol | Enum |
|---|---|
| `CommunityRepository.AmityCommunityMemberStatusFilter.ALL` | `AmityCommunityMemberStatusFilter` |
| `CommunityRepository.AmityCommunityMemberStatusFilter.MEMBER` | same |
| `CommunityRepository.AmityCommunityMemberStatusFilter.NOT_MEMBER` | same |
| `UserRepository.AmityUserSearchMatchType.DEFAULT` | `AmityUserSearchMatchType` |
| `UserRepository.AmityUserSearchMatchType.PARTIAL` | same |

These enum cases are referenced in docs via `AmityCommunityMemberStatusFilter.ALL` etc.  Both enumsare new additions to the SDK (not present in v1.2-era).

### Root export additions

TypeDoc surfaces `GET_WATCHER_URLS` as a root export; regex missed it (re-export from `utils/linkedObject/streamLinkedObject`). Also TypeDoc expands **76 enum member cases** from top-level enums (e.g. `AmityCommunityType.Default`, `AmityEventStatus.Live`) into individual root export entries. These are valid references that docs already use.

---

## Section 3: In Regex, Not In TypeDoc — Root Cause Analysis

### 3a. Amity global namespace (946 members) — TypeDoc structural gap

The SDK's `@types/domains/*.ts` files use `declare global { namespace Amity { ... } }` ambient module augmentation to declare the `Amity.*` type namespace.  TypeDoc with `--skipErrorChecking` against a single `src/index.ts` entry point does **not** walk ambient global augmentations — only explicitly exported symbols are included.

**Impact**: All 946 `Amity.*` type references in docs cannot be validated against a TypeDoc-only surface.  Doc pages reference `Amity.User`, `Amity.Post`, `Amity.Channel`, etc. pervasively.

**Possible mitigations** (not implemented in this pilot, potential for 0082):
- Secondary pass: run the existing regex extractor on `src/@types/domains/*.ts` specifically to produce a supplemental `Amity` namespace, then merge with TypeDoc output.
- Module wrapper: add a thin re-export file that re-exports all `Amity.*` types explicitly, allowing TypeDoc to capture them.
- Accept gap + rely on doc-as-test for `Amity.*` type reference validation (current approach works fine).

### 3b. `@hidden`-tagged symbols (33 confirmed) — TypeDoc correctly excludes

The regex extractor has no concept of `@hidden`.  TypeDoc respects it as the SDK's explicit "not public API" marker.  All confirmed cases below were intentionally hidden by SDK authors:

**Namespaced (8 members):**
- `Client.*`: `getActiveClient`, `markerSync`, `markerSyncTrigger`, `getMarkerSyncEvents`, `setMarkerSyncEvents`, `pushMarkerSyncEvent` — internal marker sync machinery
- `SubChannelRepository.deleteSubChannel` — tagged `@hidden` in source  
- `PostRepository.deletePost` — tagged `@hidden` in source

**Root exports (25 symbols):** All confirmed `@hidden` in source:
`createUserToken`, `filterByChannelMembership`, `filterByCommunityMembership`, `filterByFeedType`, `filterByPostDataTypes`, `filterByPropEquality`, `filterBySearchTerm`, `getNetworkTopic`, `getSmartFeedChannelTopic`, `getSmartFeedMessageTopic`, `getSmartFeedSubChannelTopic`, `isAfterBefore`, `isAfterBeforeRaw`, `isCachable`, `isFetcher`, `isFresh`, `isLocal`, `isMutator`, `isOffline`, `isPaged`, `isSkip`, `toPage`, `toPageRaw`, `toToken`, `upsertInCache`

These are internal SDK utilities (query helpers, cache primitives, paging utilities) that were incorrectly included in the regex surface.  Their presence in docs would be misleading — **TypeDoc is more correct here**.

**Implication for the regex surface**: The regex extractor is currently flagging docs references to these `@hidden` symbols as valid.  If any doc page references `filterByChannelMembership` or `getActiveClient` directly, that's a documentation accuracy problem (referencing internal API).

---

## Section 4: Same Name, Different Shape

| Symbol | Regex kind | TypeDoc kind | Notes |
|---|---|---|---|
| `*Repository.*` enums | `enum` (no cases) | `enum` (+ expanded members) | TypeDoc richer |
| `Client.TokenPayload` | `interface` | `interface` | Identical |
| Various `const` | `const` | `const` or `function` | Minor kind string differences for arrow functions vs function declarations; both correct |

No semantic conflicts — shape differences are enrichments in TypeDoc's favour, not contradictions.

---

## Section 5: Coverage Analysis — Did TypeDoc Catch Anything That Survived 4 Rounds of Regex Refinement?

**Yes — 2 genuine new public functions** (`getCommunityByIds`, `getSubChannelByIds`) that went undetected through v1.0 → v1.3.  Both are recent additions in newer barrel re-export chains the regex traversal didn't follow.

**Yes — 33 `@hidden` false positives removed** from the surface.  The regex extractor has been including internal SDK functions throughout all 4 versions; TypeDoc correctly excludes them.

**But — one fundamental gap**: The 946-member `Amity.*` global namespace is invisible to TypeDoc.  This is the dominant factor preventing a direct swap.

### Comparison with iOS and Android migrations

| Platform | Primary gap discovered | Regex false positive rate | Net result |
|---|---|---|---|
| iOS | Regex missed compiler-generated Combine members, 26 SIGNATURE_CHANGE, 4 REMOVED_API | Low | Swap: ABI is strictly more accurate |
| Android | Regex included ~568 vendor types + ~134 suppressed internals | ~70% false positive | Swap: Dokka is strictly more accurate |
| **TypeScript** | TypeDoc misses entire Amity global namespace (946 types) | ~2% false positive (@hidden) | **Hold**: TypeDoc is more accurate for namespaced exports but incomplete overall |

Unlike iOS/Android where the new source was a strict improvement, TypeDoc and the TS regex extractor have **complementary** coverage — each catches things the other misses.  The right end state is a **merged surface**: TypeDoc for namespaced exports + a targeted secondary pass for the `Amity.*` globals.

---

## Section 6: Recommendation

**Hold on a direct swap.  Pursue a hybrid merger as follow-up task 0082.**

### Why hold

A direct `typescript.json` swap to TypeDoc output would:
1. **Drop 946 Amity global type members** — breaking all `Amity.*` reference validation in the accuracy validator
2. **Remove 33 `@hidden` symbols** from surface — correct, but must also remove them from `KNOWN_VALID_REFS` or they become false positives in the validator
3. **Net accuracy trade-off** is unfavourable without the Amity gap resolved

### Why TypeDoc is still a win (even without swapping)

- Confirmed 2 new public API functions missed by 4 regex versions → these should be added to docs
- Confirmed 33 `@hidden` false positives in current surface → clean-up task for accuracy validator
- Captures full signatures (parameter types, return types, generics) → available for future doc-as-test signature checks
- `enum` case expansions are richer than regex → better reference resolution downstream

### Proposed follow-up: task 0082 — hybrid TS surface

Combine the two extractors:
1. **TypeDoc JSON** → namespaced exports (authoritative, honors `@hidden`)
2. **Targeted `@types/` scan** → `Amity.*` global namespace only (regex against the well-structured `@types/domains/*.ts` files, which ARE a single canonical location)
3. Merge into a single surface artifact with `extractor: "typescript-hybrid-extractor.py"`
4. Net result: TypeDoc accuracy for namespaced API + `Amity.*` coverage for global types + no `@hidden` false positives

### Framing for SDK-team conversation

TypeDoc confirms that **TypeDoc is the right long-term direction** for TS.  The two near-term asks for the TS SDK team:
1. Mark a handful of re-exported `@hidden` symbols consistently (or un-hide the ones that are actually meant to be public)
2. Consider whether the `declare global namespace Amity` pattern could be replaced with explicit `export namespace Amity` — this would make TypeDoc fully authoritative and remove the need for the hybrid approach

---

*This comparison was produced by pilot task 0080.  The parallel surface artifact  
(`typescript-from-typedoc.json`) is for comparison only — `typescript.json` remains  
the active source of truth until task 0082 completes the hybrid merger.*
