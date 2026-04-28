---
name: uikit
description: Use when integrating pre-built social.plus UI components — chat lists, message composers, post feeds, user profiles — or customizing their appearance and behavior.
license: MIT
compatibility: iOS (Swift/SwiftUI), Android (Jetpack Compose), React Native, Flutter
metadata:
  author: social.plus
  version: "1.0"
  display-name: social.plus UIKit
---

# social.plus UIKit Skill

## When to Use

Reach for this skill when:
- Using pre-built UI components instead of building UI from SDK calls
- Customizing the appearance (colors, fonts, icons) of social.plus components
- Overriding default component behavior with your own widgets
- Setting up UIKit for the first time (installation, authentication wiring)
- Working with chat UI: message lists, composers, channel lists, member lists
- Working with social UI: post feeds, post creation, user profiles, community pages
- Implementing Dynamic UI (server-driven component configuration)

## Core Concepts

**UIKit vs SDK** — UIKit wraps the SDK into ready-made UI components. You style and configure them; the SDK handles all the data fetching, real-time updates, and business logic. Use UIKit for faster integration; use the SDK directly when you need full UI control.

**ThemeConfig** — the global theme object. Set colors, typography, icons, and spacing once and all components inherit the values. Platform-specific: `AmityUIKitManagerOptions` (iOS/Android), `AmityUIKitConfig` (React Native), `AmityCoreClientOption` (Flutter).

**Component override** — inject your own widget at specific slots inside a UIKit component (e.g., replace the default message bubble with your own). Each platform uses a different override mechanism — search docs for your platform.

**Dynamic UI** — server-driven configuration for component visibility and behavior. Configure in the Admin Console → UIKit → Dynamic UI. No app update required to toggle features.

**Platform components** — UIKit components are per-platform. A React Native component is not the same as the iOS or Android equivalent, though they cover the same features. Always specify your platform when searching docs.

## MCP Search Guidance

Use the `search_social_plus` MCP tool with these queries:

| Goal | Suggested query |
|------|----------------|
| Install UIKit | `"UIKit installation"` + your platform (e.g., `"UIKit installation React Native"`) |
| Wire authentication | `"UIKit authentication setup"` |
| Chat components | `"UIKit chat components MessageListComponent"` |
| Social/post components | `"UIKit social components PostListComponent"` |
| Theming | `"UIKit theme customization ThemeConfig"` |
| Override a component | `"UIKit component override custom"` |
| Dynamic UI | `"UIKit dynamic UI server-driven"` |
| iOS-specific | `"UIKit iOS Swift SwiftUI"` |
| Android-specific | `"UIKit Android Compose"` |
| React Native-specific | `"UIKit React Native"` |
| Flutter-specific | `"UIKit Flutter"` |

## Key Documentation

- Full page index: https://learn.social.plus/llms.txt
- UIKit overview: https://learn.social.plus/uikit/overview
- Getting started: https://learn.social.plus/uikit/getting-started/overview
- Chat components: https://learn.social.plus/uikit/components/chat
- Social components: https://learn.social.plus/uikit/components/social
- Customization: https://learn.social.plus/uikit/customization/overview
- Platform guides: https://learn.social.plus/uikit/platform-guides
