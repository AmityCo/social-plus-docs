---
name: admin
description: Use when configuring a social.plus application — setting up moderation rules, managing users and communities, reading analytics, configuring webhooks, or administering the platform through the Admin Console or Portal dashboard (no code required).
license: MIT
metadata:
  author: social.plus
  version: "1.0"
  display-name: social.plus Admin Console & Portal
---

# social.plus Admin Console & Portal Skill

## When to Use

Reach for this skill when:
- Creating a new application and getting your API key
- Setting up AI content moderation or manual review queues
- Reviewing and actioning flagged posts, comments, or messages
- Managing community roles, permissions, and membership
- Configuring webhooks and push notification integrations
- Reading analytics dashboards (DAU/MAU, engagement, chat volume, livestream metrics)
- Banning users, removing content, or editing user-generated content
- Managing team access and admin roles
- Exporting activity reports or AI social insights

## Core Concepts

**Portal** (`portal.amity.co`) — top-level account management: create apps, manage team members, billing, and organizational settings. Start here for a new integration.

**Console** — per-application management dashboard. Access via Portal → your app → "Go to Console". This is where day-to-day moderation, analytics, and configuration happens.

**Moderation queue** — flagged content (posts, comments, messages) appears here for admin review. Admins approve, remove, or edit content. Flagging by users does not auto-delete; manual review is required unless AI moderation is configured to auto-remove.

**AI Content Moderation** — keyword filters and image analysis that automatically flags or removes content. Must be explicitly enabled and configured in Console → Moderation → AI Content Moderation. Without setup, AI filtering is inactive.

**Analytics dashboards** — Portal dashboards cover user activity (DAU/MAU, retention), chat metrics (message volume, channel health), social metrics (post engagement, community growth), video metrics (viewer counts, watch duration), and AI Social Insights (topic trends, sentiment).

**Roles & permissions** — community-level roles (moderator, member) configurable per community. Console moderator roles control who can access the moderation queue and take admin actions.

## MCP Search Guidance

Use the `search_social_plus` MCP tool with these queries:

| Goal | Suggested query |
|------|----------------|
| Get API key | `"API key console settings security"` |
| First-time setup | `"console getting started setup"` |
| AI moderation setup | `"AI content moderation configure"` |
| Manual review queue | `"moderation feed flagged content"` |
| Roles and permissions | `"moderation roles privileges console"` |
| Ban or manage users | `"user management console ban"` |
| Webhook configuration | `"webhook configure console integrations"` |
| Analytics dashboards | `"analytics dashboard portal"` |
| Chat analytics | `"chat analytics console"` |
| Community management | `"communities management console"` |
| Livestream moderation | `"livestream moderation console"` |
| AI Social Insights | `"AI social insights dashboard"` |

## Key Documentation

- Full page index: https://learn.social.plus/llms.txt
- Console overview: https://learn.social.plus/analytics-and-moderation/console/overview
- Console getting started: https://learn.social.plus/analytics-and-moderation/console/getting-started/overview
- Moderation overview: https://learn.social.plus/analytics-and-moderation/console/moderation/overview
- AI Content Moderation: https://learn.social.plus/analytics-and-moderation/console/ai-content-moderation
- Moderation feed: https://learn.social.plus/analytics-and-moderation/console/user-and-content-management/mod-feed
- Webhooks & integrations: https://learn.social.plus/analytics-and-moderation/console/settings/integrations
- Portal overview: https://learn.social.plus/analytics-and-moderation/social+-portal/README
- Analytics dashboards: https://learn.social.plus/analytics-and-moderation/social+-portal/dashboard/README
- AI Social Insights: https://learn.social.plus/analytics-and-moderation/social+-portal/dashboard/social-insights
