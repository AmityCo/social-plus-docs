---
name: troubleshoot
description: Use when a developer's social.plus integration is broken — they have an error code, something stopped working, or behavior is unexpected.
license: MIT
metadata:
  author: social.plus
  version: "1.0"
  display-name: social.plus Troubleshooter
---

# social.plus Troubleshooter Skill

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
- Search: `search_social_plus("compatibility requirements iOS")` (substitute the developer's actual platform)
- Search: `search_social_plus("initialization order")`

## Branch: Unexpected Behavior (wrong data, missing events, feature not responding)

- Live collection disposed too early → real-time updates silently stop; verify `.dispose()` timing in lifecycle
- Query filters excluding expected data by default (e.g., soft-deleted content is hidden unless filter removed)
- Operation requires moderator or admin role — verify the current user's role in the social.plus console
- Search: `search_social_plus("live collection dispose")` (substitute the actual feature name when searching for unexpected behavior)

## Key Documentation

- Full page index: https://learn.social.plus/llms.txt
- Authentication: https://learn.social.plus/social-plus-sdk/getting-started/authentication
- Android quick start: https://learn.social.plus/social-plus-sdk/getting-started/platform-setup/mobile/android-quick-start
- iOS quick start: https://learn.social.plus/social-plus-sdk/getting-started/platform-setup/mobile/ios-quick-start
- UIKit getting started: https://learn.social.plus/uikit/getting-started/overview
