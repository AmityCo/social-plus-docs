# iOS Doc-as-Test Framework

Type-checks Swift code blocks from social.plus docs against the published AmitySDK iOS binary.

## Toolchain: Option C — `swiftc -typecheck` with xcframework binary

**Why Option C?**

| Option | Tried? | Outcome |
|---|---|---|
| A — SPM local xcframework | No `AmitySDK.xcframework` in the iOS source repo | ✗ n/a |
| B — SPM published repo | Blocked by SwiftPM libgit2 `safe.bareRepository` policy on this host | ✗ blocked |
| **C — swiftc + binary xcframework** | Download published xcframework zip, run `swiftc -typecheck -F` per snippet | ✅ **active** |

Benefits of Option C:
- **0.2 s per snippet** — the binary is already compiled, no SDK source involved
- No xcodeproject, no workspace, no SPM graph
- Tests against the *published* SDK (v8.1.1) — same as what docs readers install

## Requirements

- macOS with Xcode Command Line Tools (`swiftc` available)
- Internet access on first run (downloads `AmitySDK.xcframework.zip`, ~15 MB)
- Python 3.9+

## Running locally

```bash
cd social-plus-docs/.docs-ops/integration-tests/ios

# Extract blocks + run type-check in one step:
python3 run-tests.py --extract

# Or separately:
python3 extract-blocks.py
python3 run-tests.py
```

Results are written to `results/latest.json`.

## Directory structure

```
ios/
├── Package.swift          # Stub — see note above
├── preamble.swift         # Shared imports + function signature (reference only)
├── pages.json             # Which doc pages to extract from
├── extract-blocks.py      # Extracts ```swift blocks → results/extracted/
├── run-tests.py           # Type-checks each block, emits results/latest.json
├── vendor/                # Downloaded xcframework (gitignored)
│   └── AmitySDK.xcframework/
└── results/
    ├── extracted/         # Generated .swift files (gitignored)
    └── latest.json        # Most recent run report
```

## Report schema

`results/latest.json` follows the same schema as the TS / Flutter / Android frameworks:

```json
{
  "generated_at": "...",
  "toolchain": "swiftc -typecheck",
  "sdk_version": "AmitySDK 8.1.1",
  "stats": {
    "blocks_extracted": 55,
    "blocks_passed": 42,
    "blocks_warned": 3,
    "blocks_failed": 13,
    "blocks_skipped": 4
  },
  "failures": [...],
  "warnings": [...],
  "passed": [...],
  "skipped": [...]
}
```

## CI notes

This framework requires macOS with Xcode for `swiftc`. GitHub Actions support via a
`macos-latest` runner is a Phase 2 follow-up (task 0059+ wires it into `check-drift.py`).

## Gate policy (once wired into check-drift.py)

Mirrors Android/Flutter:
- `error` diagnostics → **BLOCKING**
- `warning` diagnostics → warning (non-blocking)
- Compiler crash → non-blocking (infra failure shouldn't gate pushes)
