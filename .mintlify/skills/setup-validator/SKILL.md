---
name: setup-validator
description: Use when a developer asks "is my setup correct?", "why isn't the SDK initializing?", or is setting up social.plus for the first time on any platform.
license: MIT
metadata:
  author: social.plus
  version: "1.0"
  display-name: social.plus Setup Validator
---

# social.plus Setup Validator Skill

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
| React Native | uses TypeScript SDK — see Web / TypeScript quick start above |
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
- `registerDevice()` called after user login, not at app start (device binds permanently to userId until unregistered)
- `unregisterDevice()` called on logout — skipping this leaves the old user session on the device

**Common mistakes not documented — check these explicitly:**
- Double init: `AmityClient.setup()` called alongside `AmityUIKitManager.setup()` → conflict
- User switching without `unregisterDevice()` first → new user inherits old user's notifications
- `setup()` placed inside a component render cycle → reinitializes on every render
- Flutter: missing `WidgetsFlutterBinding.ensureInitialized()` before `setup()`

## Key Documentation

- Full page index: https://learn.social.plus/llms.txt
- SDK getting started overview: https://learn.social.plus/social-plus-sdk/getting-started/overview
- Authentication (all platforms): https://learn.social.plus/social-plus-sdk/getting-started/authentication
- UIKit getting started: https://learn.social.plus/uikit/getting-started/overview
- UIKit installation: https://learn.social.plus/uikit/getting-started/installation
