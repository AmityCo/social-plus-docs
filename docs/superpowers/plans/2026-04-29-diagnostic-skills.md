# Diagnostic Skills Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add two diagnostic skill files (`setup-validator` and `troubleshoot`) to `.mintlify/skills/` so AI coding tools can guide developers through SDK/UIKit initialization validation and broken-integration diagnosis.

**Architecture:** Two standalone Markdown skill files, each following the existing SKILL.md format (frontmatter + workflow sections). Skills hold structural logic and common-mistake checklists; code patterns are fetched live from doc pages via `get_page_social_plus`. Forward-reference hooks for future Phase 2 MCP tools are included.

**Tech Stack:** Markdown, Mintlify skill format (agentskills.io spec), existing `.mintlify/skills/` directory

---

### Task 1: Create `setup-validator` skill file

**Files:**
- Create: `.mintlify/skills/setup-validator/SKILL.md`

- [ ] **Step 1: Create the file with the following exact content**

Create `.mintlify/skills/setup-validator/SKILL.md`:

```markdown
---
name: setup-validator
description: Use when a developer asks "is my setup correct?", "why isn't the SDK initializing?", or is setting up social.plus for the first time on any platform.
license: MIT
metadata:
  author: social.plus
  version: "1.0"
  display-name: social.plus Setup Validator
---

# social.plus Setup Validator

## When to Use

Reach for this skill when a developer:
- Says "I just added the SDK" or "is my setup right?"
- Reports the SDK not initializing or failing on first call
- Asks about installation or configuration for the first time
- Gets a blank or auth-failure response from the very first API call

## How to Run This Workflow

1. Ask: are you using the **SDK directly** (Chat, Social, Video — building your own UI) or **UIKit** (pre-built components)?
2. Ask: which platform (iOS, Android, Web, Flutter, React Native)?
3. Ask the developer to share their initialization code snippet
4. Fetch the canonical setup page for their product + platform using `get_page_social_plus` (URLs below)
5. Compare their code against the canonical pattern from the fetched page
6. Flag any deviations using the checklists below
7. If `validate_api_key` MCP tool is available, call it with the developer's API key to confirm it is active and check which products it grants access to

---

## SDK Path (Chat / Social / Video — custom UI)

Fetch the canonical initialization code for the developer's platform:

| Platform | URL for `get_page_social_plus` |
|----------|-------------------------------|
| iOS | `https://learn.social.plus/social-plus-sdk/getting-started/platform-setup/mobile/ios-quick-start` |
| Android | `https://learn.social.plus/social-plus-sdk/getting-started/platform-setup/mobile/android-quick-start` |
| Flutter | `https://learn.social.plus/social-plus-sdk/getting-started/platform-setup/mobile/flutter-quick-start` |
| Web / TypeScript | `https://learn.social.plus/social-plus-sdk/getting-started/platform-setup/web/web-quick-start` |
| Auth (all platforms) | `https://learn.social.plus/social-plus-sdk/getting-started/authentication` |

**Shared checklist:**
- API key and App ID are both present and sourced from the social.plus console (not placeholder values)
- Region/endpoint is set explicitly — US, EU, or SG. Default is US; wrong region = silent auth failure
- `setup()` is called before any other SDK method
- `register()` / auth is called after user login, not at app start

**Common mistakes not documented — check these explicitly:**
- `setup()` called inside a component that can remount → duplicate init + session conflict
- `register()` not awaited before subscribing to live collections → race condition
- API key used in the App ID field or vice versa (they are two separate values)
- Android: `setup()` in `Activity.onCreate()` instead of `Application.onCreate()` → re-inits on every screen rotation

---

## UIKit Path (pre-built components)

Fetch the canonical setup pages:

| Page | URL for `get_page_social_plus` |
|------|-------------------------------|
| Installation | `https://learn.social.plus/uikit/getting-started/installation` |
| Authentication | `https://learn.social.plus/uikit/getting-started/authentication` |
| Quick Start | `https://learn.social.plus/uikit/getting-started/quick-start` |

**Critical check first:** Does the developer's code call both `AmityUIKitManager.setup()` AND `AmityClient.setup()`? UIKit manages the SDK internally — calling both causes a conflict. Flag this immediately if present.

**Shared checklist:**
- Only `AmityUIKitManager` is used — no direct `AmityClient.setup()` call
- API key and region/endpoint passed to `AmityUIKitManager.setup()`
- `registerDevice()` called after user login, not at app start (device binds permanently to userId until explicitly unregistered)
- `unregisterDevice()` called on logout — skipping this leaves the old user session on the device

**Common mistakes not documented — check these explicitly:**
- Double init: `AmityClient.setup()` called alongside `AmityUIKitManager.setup()` → conflict
- User switching without `unregisterDevice()` first → new user inherits old user's notifications
- `setup()` placed inside a component render cycle → reinitializes on every render
- Flutter: missing `WidgetsFlutterBinding.ensureInitialized()` before `setup()`
```

- [ ] **Step 2: Verify format and length**

Run:
```bash
wc -l .mintlify/skills/setup-validator/SKILL.md
```
Expected: ≤ 80 lines.

Also verify frontmatter has `name: setup-validator` (must match directory name):
```bash
head -3 .mintlify/skills/setup-validator/SKILL.md
```
Expected first three lines:
```
---
name: setup-validator
description: Use when a developer...
```

- [ ] **Step 3: Commit**

```bash
git add .mintlify/skills/setup-validator/SKILL.md
git commit -m "feat: add setup-validator skill for SDK/UIKit initialization guidance

Guides AI agents through validating developer initialization code for
both SDK (AmityClient) and UIKit (AmityUIKitManager) paths. Fetches
canonical code from doc pages via get_page_social_plus rather than
maintaining inline code. Includes forward hook for Phase 2 validate_api_key tool.

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

---

### Task 2: Create `troubleshoot` skill file

**Files:**
- Create: `.mintlify/skills/troubleshoot/SKILL.md`

- [ ] **Step 1: Create the file with the following exact content**

Create `.mintlify/skills/troubleshoot/SKILL.md`:

```markdown
---
name: troubleshoot
description: Use when a developer's social.plus integration is broken — they have an error code, something stopped working, or behavior is unexpected.
license: MIT
metadata:
  author: social.plus
  version: "1.0"
  display-name: social.plus Troubleshooter
---

# social.plus Troubleshooter

## When to Use

Reach for this skill when a developer:
- Reports an error code (401, 403, timeout, connection refused, WebSocket closed)
- Says "it was working and now it's broken"
- Reports unexpected behavior (missing events, empty data, feature not responding)
- Gets a crash or null pointer exception from SDK code

## How to Run This Workflow

1. Ask: which SDK/product, which platform, and describe the symptom or paste the error message
2. Categorize the symptom into one of the 5 branches below
3. Work through that branch's checklist with the developer
4. Search for known version-specific bugs: `search_social_plus("<feature> known issue <platform>")`
5. If `diagnose_error` MCP tool is available, call it with the error code for a structured root cause

---

## Branch: Auth Errors (401, 403, token invalid / expired)

- Session token has a TTL — re-authentication required on expiry; check if the app handles token refresh
- API key ≠ App ID — wrong value in wrong field causes silent failure with no clear error
- API key region must match endpoint: US key + EU endpoint = auth failure
- Search: `search_social_plus("authentication error token expired")`, `search_social_plus("session token refresh")`
- Docs: `get_page_social_plus("https://learn.social.plus/social-plus-sdk/getting-started/authentication")`

## Branch: Network / Connection Errors (timeout, WebSocket disconnected, unreachable)

- Verify region endpoint matches the console — default is US; EU/SG developers often miss this
- WebSocket disconnects: SDK auto-reconnects only if the observer is still active; check for early `.dispose()` calls on live collections
- App returning from background: SDK may need an explicit reconnect trigger; check app lifecycle handling
- Search: `search_social_plus("connection status reconnect")`, `search_social_plus("network error")`

## Branch: Permission Errors (platform OS-level blocks)

- **Android**: `INTERNET` permission missing from `AndroidManifest.xml`; network security config required for non-HTTPS development endpoints
- **iOS**: App Transport Security (ATS) exception required for development endpoints; production endpoints use HTTPS only
- **Web**: CORS — browser origin must be whitelisted in the social.plus console dashboard
- Search: `search_social_plus("network security config Android")`, `search_social_plus("App Transport Security iOS")`, `search_social_plus("CORS")`

## Branch: Crash / Null Pointer

- SDK method called before `setup()` completed → check initialization order; `setup()` must finish before any API call
- SDK version incompatibility with the platform or OS version → check compatibility matrix
- Threading violation: SDK callbacks may be on a background thread; UI updates must run on the main thread
- Search: `search_social_plus("compatibility requirements <platform>")`, `search_social_plus("initialization order")`

## Branch: Unexpected Behavior (wrong data, missing events, feature not responding)

- Live collection disposed too early → real-time updates silently stop; verify `.dispose()` timing in lifecycle
- Query filters excluding expected data by default (e.g., soft-deleted content is hidden unless filter removed)
- Operation requires moderator or admin role — verify the current user's role in the social.plus console
- Search: `search_social_plus("<feature name> not working")`, `search_social_plus("live collection dispose")`
```

- [ ] **Step 2: Verify format and length**

Run:
```bash
wc -l .mintlify/skills/troubleshoot/SKILL.md
```
Expected: ≤ 80 lines.

Verify frontmatter `name` matches directory:
```bash
head -3 .mintlify/skills/troubleshoot/SKILL.md
```
Expected:
```
---
name: troubleshoot
description: Use when a developer's social.plus integration is broken...
```

- [ ] **Step 3: Commit**

```bash
git add .mintlify/skills/troubleshoot/SKILL.md
git commit -m "feat: add troubleshoot skill for integration diagnosis

Decision-tree skill covering 5 error categories: auth, network,
permissions, crash, and unexpected behavior. Each branch includes
search queries and doc page references. Forward hook for Phase 2
diagnose_error MCP tool included.

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

---

### Task 3: Verify structure and push

**Files:** No changes — verification and push only.

- [ ] **Step 1: Verify skills directory has all 8 skill directories**

Run:
```bash
ls .mintlify/skills/
```
Expected output (8 entries):
```
admin  chat  server  setup-validator  social  troubleshoot  uikit  video
```

- [ ] **Step 2: Verify both new skill files have correct name fields**

Run:
```bash
grep "^name:" .mintlify/skills/setup-validator/SKILL.md .mintlify/skills/troubleshoot/SKILL.md
```
Expected:
```
.mintlify/skills/setup-validator/SKILL.md:name: setup-validator
.mintlify/skills/troubleshoot/SKILL.md:name: troubleshoot
```

- [ ] **Step 3: Confirm clean working tree (no uncommitted skill changes)**

Run:
```bash
git status --short
```
Expected: neither `setup-validator` nor `troubleshoot` skill files appear as modified or untracked.

- [ ] **Step 4: Push branch**

```bash
git push origin feat/llm-txt
```
Expected: branch pushed, both new commits visible on remote.
