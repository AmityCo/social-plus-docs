---
name: server
description: Use when calling social.plus REST APIs from a backend, generating user auth tokens, setting up webhook endpoints to receive events, or implementing pre-hook handlers to intercept and validate operations before they complete.
license: MIT
metadata:
  author: social.plus
  version: "1.0"
  display-name: social.plus Server APIs
---

# social.plus Server APIs Skill

## When to Use

Reach for this skill when implementing:
- Server-to-server REST API calls (no SDK, backend-only)
- Generating user authentication tokens on your backend
- Receiving webhook events (post-operation event notifications)
- Implementing pre-hook handlers (intercept operations before they complete)
- Platform-wide configuration via Network Settings APIs
- Backend automation (user provisioning, content sync, event-driven workflows)
- Exporting user activity reports

## Core Concepts

**API Key** — your server-side credential for all REST API calls. Found in Admin Console → Settings → Security. Never expose this in client-side code.

**Auth Token** — a short-lived JWT your backend generates to authenticate SDK users with social.plus. Required in production (development mode with API key only is not production-safe). Your backend calls the social.plus auth token endpoint with the user's ID; the JWT goes to the client app for SDK login.

**Webhook** — an HTTP POST social.plus sends to your endpoint after an operation completes (e.g., message sent, post created, user flagged). Your endpoint must respond within **1.5 seconds** or the delivery is marked failed. Always verify the signature header to prevent spoofing.

**Pre-hook** — like a webhook but synchronous and blocking. social.plus calls your endpoint *before* the operation completes and waits for your response. Return `{"action": "allow"}` to proceed or `{"action": "deny", "message": "..."}` to block. Use for custom moderation, business rules enforcement, or compliance checks. Test thoroughly — a slow or broken pre-hook blocks real user operations.

**Signature verification** — webhooks include an `x-amity-signature` header (HMAC-SHA256). Always verify it against your webhook secret before processing the payload.

## MCP Search Guidance

Use the `search_social_plus` MCP tool with these queries:

| Goal | Suggested query |
|------|----------------|
| Auth token generation | `"auth token generation server backend"` |
| Webhook setup | `"webhook event setup configure"` |
| Webhook event types | `"webhook event types list"` |
| Signature verification | `"webhook signature verification"` |
| Pre-hook setup | `"pre-hook event intercept"` |
| Pre-hook response format | `"pre-hook allow deny response"` |
| Network Settings API | `"network settings API"` |
| User activity export | `"user last activity report export"` |
| REST API authentication | `"REST API key authentication server"` |

## Key Documentation

- Full page index: https://learn.social.plus/llms.txt
- Server APIs overview: https://learn.social.plus/analytics-and-moderation/social+-apis-and-services/README
- Webhook Events: https://learn.social.plus/analytics-and-moderation/social+-apis-and-services/webhook-event
- Pre-Hook Events: https://learn.social.plus/analytics-and-moderation/social+-apis-and-services/pre-hook-event
- Network Settings: https://learn.social.plus/analytics-and-moderation/social+-apis-and-services/network-settings
- Webhooks config (Console): https://learn.social.plus/analytics-and-moderation/console/settings/integrations
- Auth overview: https://learn.social.plus/social-plus-sdk/getting-started/authentication
- API Reference: https://learn.social.plus/api-reference/social-data-model
