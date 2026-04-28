# Design: Diagnostic Skill Files for social.plus Integration Guidance

## Problem

Developers integrating social.plus SDKs encounter issues at every phase: initial setup (wrong API key, wrong region, bad initialization order), active development (anti-patterns, missing lifecycle calls), and debugging (unexplained errors, connection failures, crashes). Currently, AI coding tools using the social.plus MCP server can only search documentation reactively — there is no structured workflow to proactively validate a developer's integration or diagnose a broken one.

## Proposed Approach

Add two diagnostic skill files to `.mintlify/skills/` alongside the existing 6 product-oriented skills. These skills act as **AI-executable workflows**: when an AI agent reads them, it knows exactly what questions to ask, what code patterns to look for, and which documentation to reference — at each phase of the developer journey.

This is Phase 1 of a hybrid design:
- **Phase 1 (this spec)**: Workflow skill files — ships now, no infrastructure needed
- **Phase 2 (future)**: Custom MCP server at `mcp.social.plus` with active tools (`validate_api_key`, `check_sdk_version`, `diagnose_error`). Phase 1 skill files will forward-reference these tools so the workflow improves automatically when Phase 2 exists.

## Skill Files

### 1. `setup-validator` — SDK Initialization Verifier

**File:** `.mintlify/skills/setup-validator/SKILL.md`
**name:** `setup-validator`
**Persona served:** First-time integrator, any SDK/platform, asking "is my setup correct?" or "why isn't the SDK initializing?"

**Workflow the AI executes:**
1. Ask which SDK (chat, social, video, UIKit) and which platform (iOS, Android, Web, Flutter, React Native, TypeScript)
2. Ask for the initialization code snippet
3. Validate against correct patterns retrieved via `search_social_plus`
4. Run the following checklist:
   - API key format (must start with correct prefix, not a test/development key in production)
   - App ID source (must come from social.plus console, not hardcoded placeholder)
   - Region/endpoint (US vs EU — wrong region = silent auth failure)
   - SDK initialization lifecycle placement (platform-specific correct positions listed below)
   - Required platform permissions present (Android network permission, iOS App Transport Security)
5. Flag common mistakes per platform
6. If `validate_api_key` MCP tool is available, call it to confirm credentials are live

**Platform-specific initialization placement:**
- **iOS** — `AppDelegate.application(_:didFinishLaunchingWithOptions:)`
- **Android** — `Application.onCreate()` (not `Activity.onCreate()`)
- **Web/TypeScript** — after DOM ready, before any component mounts
- **Flutter** — after `WidgetsFlutterBinding.ensureInitialized()` in `main()`
- **React Native** — root index file, before navigation stack renders

**Common mistakes covered:**
- Using development API key in production (or vice versa)
- Initializing inside a component that remounts (causes duplicate initialization)
- Missing App ID / wrong App ID (copy-paste error from docs example)
- Wrong region endpoint (EU developers using default US endpoint)
- Not awaiting async initialization before calling SDK methods

---

### 2. `troubleshoot` — Integration Diagnostic Decision Tree

**File:** `.mintlify/skills/troubleshoot/SKILL.md`
**name:** `troubleshoot`
**Persona served:** Developer with a broken integration — something was working and stopped, or never worked, and they need to diagnose why.

**Workflow the AI executes:**
1. Ask: which SDK, which platform, and what symptom (error message, unexpected behavior, crash)
2. Categorize the symptom into one of 5 error branches:
   - **Auth errors** (401, 403, token invalid/expired)
   - **Network/connection errors** (timeout, unreachable, WebSocket disconnected)
   - **Permission errors** (platform-level: network security config, ATS, CORS)
   - **Crash / null pointer** (SDK version mismatch, threading violation, uninitialized SDK)
   - **Unexpected behavior** (feature not working as expected — wrong data, missing events)
3. Per branch, provide: what to check + specific `search_social_plus` queries + key doc links
4. Surface known version-specific bugs (retrieve from docs via MCP search)
5. If `diagnose_error` MCP tool is available, call it with the error code for structured root cause

**Decision tree branches:**

**Auth errors:**
- Check token expiry: `AmityClient` session token has a TTL; re-authentication is required on expiry
- Check API key vs App ID: these are two different values; wrong one in wrong field causes silent failure
- Check that the API key matches the region (US key used with EU endpoint = auth failure)
- Search: `"authentication error token expired"`, `"session token refresh"`

**Network/connection errors:**
- Check region endpoint configuration; default is US
- WebSocket disconnection: SDK auto-reconnects, but only if the observer is still active — check for disposed live collections
- Check app background handling: SDK needs explicit reconnect signal on app foreground
- Search: `"connection status"`, `"reconnect"`, `"network error"`

**Permission errors:**
- **Android**: `INTERNET` permission in `AndroidManifest.xml`; network security config for cleartext traffic if using debug endpoint
- **iOS**: App Transport Security exception required for development endpoints; production uses HTTPS only
- **Web**: CORS — social.plus APIs allow browser origins for configured domains; check console dashboard
- Search: `"network security"`, `"CORS"`, `"App Transport Security"`

**Crash / null pointer:**
- Check SDK version compatibility matrix for the platform (search: `"compatibility requirements"`)
- Check initialization order: crash = method called before `AmityClient.setup()` completed
- Threading: UI updates must be on the main thread; SDK callbacks may be on background threads
- Search: `"initialization"`, `"thread"`, `"version compatibility"`

**Unexpected behavior:**
- Check live collection disposal: if `.dispose()` was called too early, real-time updates stop
- Check query filters: data may be filtered out by default (e.g., soft-deleted content)
- Check user roles and permissions: some operations require moderator or admin role
- Search by feature name + `"not working"` or `"expected behavior"`

## Non-Goals (Phase 1)

- No active API validation (no network calls from AI agent)
- No SDK version checking against a registry
- No code analysis or static checking — AI reasons from what the developer shows it
- No per-platform skill variants (both skills are cross-platform with platform-specific branches)

## Forward Compatibility (Phase 2 Hooks)

Both skill files will reference MCP tools that do not yet exist:
```
If the `validate_api_key` MCP tool is available, call it with the developer's API key
to confirm it is active and check which products it grants access to.
```

When the Phase 2 custom MCP server is built, these lines activate automatically — no skill file changes needed.

## File Structure

```
.mintlify/skills/
├── chat/SKILL.md          (existing)
├── social/SKILL.md        (existing)
├── video/SKILL.md         (existing)
├── uikit/SKILL.md         (existing)
├── server/SKILL.md        (existing)
├── admin/SKILL.md         (existing)
├── setup-validator/       (new)
│   └── SKILL.md
└── troubleshoot/          (new)
    └── SKILL.md
```

## Success Criteria

- An AI coding tool using the social.plus MCP server, when asked "is my SDK setup correct?", runs the setup-validator workflow and catches at least: wrong region, wrong lifecycle position, and credential mismatches
- An AI coding tool, given an error code or symptom, uses the troubleshoot skill to narrow down the root cause to a specific check + documentation link without hallucinating
- Both skills are ≤80 lines (concise, no API signatures that can go stale)
- Skills stay accurate without manual updates because they delegate API details to `search_social_plus`
