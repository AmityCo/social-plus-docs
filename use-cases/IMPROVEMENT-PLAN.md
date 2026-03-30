# Use Cases — Improvement Plan

> Based on competitive research vs. GetStream, Sendbird, PubNub, Liveblocks, Firebase, and Mux.  
> Work through chunks in order. Each chunk is self-contained and can be implemented and reviewed independently.

---

## Table of Contents

1. [Chunk 1 — Fix dead-end cards on top-level overview](#chunk-1--fix-dead-end-cards-on-top-level-overview)
2. [Chunk 2 — Add persona routing to top-level overview](#chunk-2--add-persona-routing-to-top-level-overview)
3. [Chunk 3 — Convert Concepts table to AccordionGroup](#chunk-3--convert-concepts-table-to-accordiongroup)
4. [Chunk 4 — Add industry vertical quick-pick section](#chunk-4--add-industry-vertical-quick-pick-section)
5. [Chunk 5 — Add difficulty badges to all 20 guide cards](#chunk-5--add-difficulty-badges-to-all-20-guide-cards)
6. [Chunk 6 — Add "After this guide" outcome statement to all 20 guides](#chunk-6--add-after-this-guide-outcome-statement-to-all-20-guides)
7. [Chunk 7 — Add prerequisite dependency chain to selected guides](#chunk-7--add-prerequisite-dependency-chain-to-selected-guides)
8. [Chunk 8 — Upgrade "Next Steps" with an opinionated first card](#chunk-8--upgrade-next-steps-with-an-opinionated-first-card)
9. [Chunk 9 — Real-world app callouts (optional)](#chunk-9--real-world-app-callouts-optional)
10. [Chunk 10 — Completion checklist at guide bottom (optional)](#chunk-10--completion-checklist-at-guide-bottom-optional)

---

## Chunk 1 — Fix dead-end cards on top-level overview

**File:** `use-cases/overview.mdx`  
**Priority:** High — visible dead ends erode trust  
**Effort:** ~10 min

### Problem

Two cards in the "Choose Your Domain" section link to `href="#"`:
- **Chat Features** → placeholder with no destination
- **Cross-Feature Patterns** → placeholder with no destination

### Change

Replace the two dead-end cards. Options:
- Link to the existing SDK chat overview for the Chat card
- Turn both into `<Note>` teasers that explain what's coming, OR
- Remove them entirely until they have real content

#### Recommended: replace dead ends with real destinations + teaser wording

```mdx
<CardGroup cols={2}>
  <Card
    title="Social Features"
    icon="share-nodes"
    href="/use-cases/social/overview"
  >
    Feeds, communities, posts, comments, reactions, stories, notifications, search, moderation, events, livestream, and more.
  </Card>
  <Card
    title="Chat Features"
    icon="message"
    href="/social-plus-sdk/chat/overview"
  >
    1:1 messaging, group channels, live chat, member management, and real-time typing indicators. End-to-end use-case guides coming soon.
  </Card>
  <Card
    title="Video & Livestream"
    icon="video"
    href="/use-cases/social/livestream-and-video-posts"
  >
    Go live in communities, manage broadcast rooms, and access recordings. More video guides coming soon.
  </Card>
  <Card
    title="Cross-Feature Patterns"
    icon="diagram-project"
    href="/social-plus-sdk/overview"
  >
    Authentication flows, offline sync, multi-tenant apps, and platform-specific patterns. Full guides coming soon — see the SDK overview for architecture reference.
  </Card>
</CardGroup>
```

---

## Chunk 2 — Add persona routing to top-level overview

**File:** `use-cases/overview.mdx`  
**Priority:** High — helps developers self-select a starting point instantly  
**Effort:** ~20 min

### Problem

The page currently offers a 4-card domain picker ("Choose Your Domain") but doesn't help developers who don't yet know which domain they need. They arrive thinking "I want to add a social feed to my fitness app" — not "I want Social Features".

### Change

Add a **new section above "Choose Your Domain"** called `## Where do you want to start?` with 4 persona-based route cards that link directly to the most relevant guide. The domain picker stays below it.

```mdx
## Where do you want to start?

Not sure which guide to open first? Pick the description that fits your situation.

<CardGroup cols={2}>
  <Card
    title="Adding social to an existing app"
    icon="plus"
    href="/use-cases/social/build-a-social-feed"
  >
    Start with the feed guide — query posts, set up real-time updates, and connect to communities.
  </Card>
  <Card
    title="Building a community platform from scratch"
    icon="rocket"
    href="/use-cases/social/community-platform"
  >
    Start with communities — create groups, manage membership, assign roles, and build moderation.
  </Card>
  <Card
    title="Adding engagement to content (reactions, comments, stories)"
    icon="heart"
    href="/use-cases/social/comments-and-reactions"
  >
    Start with comments & reactions — wire up engagement on existing posts in a few API calls.
  </Card>
  <Card
    title="Setting up content moderation"
    icon="shield-halved"
    href="/use-cases/social/content-moderation-pipeline"
  >
    Start with the moderation pipeline — connect user flagging, admin review, AI moderation, and webhooks.
  </Card>
</CardGroup>

---
```

### Placement in file

Insert this block **after the opening `<Info>` callout** and **before the `## Choose Your Domain` heading**.

---

## Chunk 3 — Convert Concepts table to AccordionGroup

**File:** `use-cases/social/overview.mdx`  
**Priority:** Medium — improves mobile experience and reduces visual overwhelm  
**Effort:** ~15 min

### Problem

The "Core Concepts at a Glance" section is a plain 10-row markdown table. Tables are problematic:
- Render poorly on mobile
- Can't include inline code comfortably
- Long definitions get cramped

Liveblocks and Stripe use `<AccordionGroup>` for concept definitions — collapsed by default, opened on demand. This keeps the page scannable.

### Change

Replace the markdown table with an `<AccordionGroup>`. Each term becomes an `<Accordion>` with its full definition.

```mdx
## Core Concepts at a Glance

New to social.plus? Expand any term to understand the building blocks before picking a guide.

<AccordionGroup>
  <Accordion title="Post" icon="file-lines">
    The primary content unit. Can be `text`, `image`, `video`, `poll`, `clip`, or `livestream`. Always targets either a **community** or a **user's profile feed** as its destination.
  </Accordion>
  <Accordion title="Community" icon="users">
    A group space where users gather, share posts, and interact. Has members, roles (member / moderator), and its own feed. Can be `public` or `private`.
  </Accordion>
  <Accordion title="Feed" icon="rectangle-list">
    A container that groups posts for a target (community or user). Returns posts with three possible review states: `published`, `reviewing`, and `declined`.
  </Accordion>
  <Accordion title="Comment" icon="comment">
    A reply attached to a post or story. Supports two levels of threading: top-level **comments** and nested **replies**. Both have full CRUD and real-time updates.
  </Accordion>
  <Accordion title="Reaction" icon="face-smile">
    A named emoji response on a post, comment, or story. Each reaction is its own document — names are freeform strings you define (e.g. `"like"`, `"love"`, `"clap"`). No fixed SDK enum.
  </Accordion>
  <Accordion title="Story" icon="circle-play">
    Ephemeral content (image or video) visible for 24 hours. Targets a community or user profile. Supports per-story view counts and impression analytics.
  </Accordion>
  <Accordion title="Poll" icon="square-poll-vertical">
    An interactive vote with up to 10 options, always embedded inside a post. Supports single or multiple choice with an optional expiry timer. Voters can change their vote until the poll closes.
  </Accordion>
  <Accordion title="Room" icon="broadcast-tower">
    A live broadcast session. Always hosted inside a community. Lifecycle: `idle → live → ended → recorded`. Supports co-hosts and live chat during broadcast.
  </Accordion>
  <Accordion title="Follow" icon="user-plus">
    A user-to-user relationship with status: `pending`, `accepted`, or `blocked`. Drives what appears in the user's home feed and social graph.
  </Accordion>
  <Accordion title="Reaction name" icon="tag">
    Freeform string — you define your own reaction set (e.g. `"like"`, `"heart"`, `"clap"`, `"fire"`). The SDK has no fixed enum for reaction types — configure them in the Admin Console.
  </Accordion>
</AccordionGroup>

<Info>
For the complete field-level reference — types, enums, and entity relationships — see the [Social Data Model](/api-reference/social-data-model).
</Info>
```

---

## Chunk 4 — Add industry vertical quick-pick section

**File:** `use-cases/social/overview.mdx`  
**Priority:** Medium — helps developers with a specific app type identify where to start  
**Effort:** ~25 min

### Problem

PubNub organizes content by industry vertical. Our page organizes by feature category (Building Blocks, Engagement, etc.) — which is good for browsing but unhelpful for a developer who arrives thinking "I'm building a dating app, where do I start?"

### Change

Add a new section **between the mermaid diagram and "## Building Blocks"** called `## Start by App Type`.

Use a `<Tabs>` component — one tab per vertical. Each tab contains 3–5 ordered `<Steps>` linking to the most relevant guides for that app type.

```mdx
## Start by App Type

Not sure which guide to open first? Pick your app type.

<Tabs>
  <Tab title="Social / Lifestyle">
    Building a general social app, lifestyle community, or content-sharing platform.

    <Steps>
      <Step title="1. Build a Social Feed">
        The foundation of every social app. → [Build a Social Feed](/use-cases/social/build-a-social-feed)
      </Step>
      <Step title="2. Add Content Creation">
        Let users post text, images, video, and polls. → [Rich Content Creation](/use-cases/social/rich-content-creation)
      </Step>
      <Step title="3. Add Engagement">
        Comments, reactions, stories. → [Comments & Reactions](/use-cases/social/comments-and-reactions)
      </Step>
      <Step title="4. Build Communities">
        Group spaces for your users. → [Community Platform](/use-cases/social/community-platform)
      </Step>
      <Step title="5. Add Notifications">
        Keep users coming back. → [Notifications & Engagement](/use-cases/social/notifications-and-engagement)
      </Step>
    </Steps>
  </Tab>

  <Tab title="Fitness / Health">
    Building a fitness tracker, health community, or workout-sharing app.

    <Steps>
      <Step title="1. User Profiles & Social Graph">
        Friends, followers, and athlete profiles. → [User Profiles & Social Graph](/use-cases/social/user-profiles-and-social-graph)
      </Step>
      <Step title="2. Build a Social Feed">
        Activity feed of workouts and achievements. → [Build a Social Feed](/use-cases/social/build-a-social-feed)
      </Step>
      <Step title="3. Add Reactions & Comments">
        High-fives and encouragement on activities. → [Comments & Reactions](/use-cases/social/comments-and-reactions)
      </Step>
      <Step title="4. Events & Activities">
        Run clubs, group challenges, virtual races. → [Events & Activities](/use-cases/social/events-and-activities)
      </Step>
      <Step title="5. Post Impressions Analytics">
        Track reach and engagement for content creators. → [Post Impressions & Creator Analytics](/use-cases/social/post-impressions-and-creator-analytics)
      </Step>
    </Steps>
  </Tab>

  <Tab title="Gaming / Esports">
    Building a gaming community, esports platform, or game companion app.

    <Steps>
      <Step title="1. Community Platform">
        Clan and team spaces with roles. → [Community Platform](/use-cases/social/community-platform)
      </Step>
      <Step title="2. Roles, Permissions & Governance">
        Mod tools, clan leadership, permission gates. → [Roles, Permissions & Governance](/use-cases/social/roles-permissions-and-governance)
      </Step>
      <Step title="3. Notifications & Engagement">
        Match alerts, tournament updates. → [Notifications & Engagement](/use-cases/social/notifications-and-engagement)
      </Step>
      <Step title="4. Stories & Ephemeral Content">
        Post-match highlights, tournament clips. → [Stories & Ephemeral Content](/use-cases/social/stories-and-ephemeral-content)
      </Step>
      <Step title="5. Livestream & Video Posts">
        In-game streams and VODs. → [Livestream & Video Posts](/use-cases/social/livestream-and-video-posts)
      </Step>
    </Steps>
  </Tab>

  <Tab title="Marketplace / eCommerce">
    Building a marketplace, creator economy, or social commerce platform.

    <Steps>
      <Step title="1. User Onboarding & Visitor Mode">
        Let browsers explore before signing up. → [User Onboarding & Visitor Mode](/use-cases/social/user-onboarding-and-visitor-mode)
      </Step>
      <Step title="2. User Search & People Discovery">
        Find sellers, creators, and brands. → [User Search & People Discovery](/use-cases/social/user-search-and-people-discovery)
      </Step>
      <Step title="3. Content Sharing & Deep Links">
        Share product pages and listings. → [Content Sharing & Deep Links](/use-cases/social/content-sharing-and-deep-links)
      </Step>
      <Step title="4. Advertising & Monetization">
        Native ads in the feed. → [Advertising & Monetization](/use-cases/social/advertising-and-monetization)
      </Step>
      <Step title="5. Content Moderation Pipeline">
        Keep listings and reviews safe. → [Content Moderation Pipeline](/use-cases/social/content-moderation-pipeline)
      </Step>
    </Steps>
  </Tab>

  <Tab title="Dating / Connections">
    Building a dating app, professional networking, or interest-based matching platform.

    <Steps>
      <Step title="1. User Profiles & Social Graph">
        Rich profiles, follow/unfollow, blocking. → [User Profiles & Social Graph](/use-cases/social/user-profiles-and-social-graph)
      </Step>
      <Step title="2. User Search & People Discovery">
        Discovery, "people you may know". → [User Search & People Discovery](/use-cases/social/user-search-and-people-discovery)
      </Step>
      <Step title="3. Real-time Presence & Activity">
        Online/offline indicators, last active. → [Real-time Presence & Activity](/use-cases/social/realtime-presence-and-activity)
      </Step>
      <Step title="4. Stories & Ephemeral Content">
        Story rings on profiles, 24hr content. → [Stories & Ephemeral Content](/use-cases/social/stories-and-ephemeral-content)
      </Step>
      <Step title="5. Content Moderation Pipeline">
        Safety features and reporting. → [Content Moderation Pipeline](/use-cases/social/content-moderation-pipeline)
      </Step>
    </Steps>
  </Tab>
</Tabs>

---
```

---

## Chunk 5 — Add difficulty badges to all 20 guide cards

**File:** `use-cases/social/overview.mdx`  
**Priority:** High — developers scan cards for effort signals before clicking  
**Effort:** ~20 min (all 20 cards in one multi-replace pass)

### Problem

Cards show time estimates (`~20 min`) but no complexity signal. A developer who's never used the SDK doesn't know if `~20 min` means "beginner-friendly" or "requires advanced setup".

### Change

Add a difficulty label to each card's description, on a new line after the SDK line, using backtick formatting for visual consistency.

Format: `` `Beginner` ``, `` `Intermediate` ``, or `` `Advanced` ``

Append after the last backtick-wrapped time estimate on each card, separated by ` · `.

#### Difficulty assignments

| Guide | Difficulty |
|---|---|
| Build a Social Feed | `Beginner` |
| Rich Content Creation | `Intermediate` |
| Comments & Reactions | `Beginner` |
| Community Platform | `Intermediate` |
| User Onboarding & Visitor Mode | `Beginner` |
| Polls & Interactive Content | `Beginner` |
| User Profiles & Social Graph | `Beginner` |
| Stories & Ephemeral Content | `Intermediate` |
| Notifications & Engagement | `Advanced` |
| Events & Activities | `Intermediate` |
| Content Sharing & Deep Links | `Beginner` |
| Real-time Presence & Activity | `Intermediate` |
| Post Impressions & Creator Analytics | `Beginner` |
| Search & Discovery | `Beginner` |
| Content Moderation Pipeline | `Advanced` |
| Roles, Permissions & Governance | `Intermediate` |
| User Search & People Discovery | `Beginner` |
| Livestream & Video Posts | `Advanced` |
| Short-Form Video Clips | `Intermediate` |
| Advertising & Monetization | `Beginner` |

#### Example — before

```
SDK: Feed queries · Live Collections · Custom ranking · `~20 min`
```

#### Example — after

```
SDK: Feed queries · Live Collections · Custom ranking · `~20 min` · `Beginner`
```

---

## Chunk 6 — Add "After this guide" outcome statement to all 20 guides

**Files:** All 20 guides in `use-cases/social/`  
**Priority:** High — Firebase Codelabs and PubNub tutorials both lead with this. Reduces abandonment.  
**Effort:** ~45 min (one targeted insert per guide)

### Problem

Each guide opens with a mermaid diagram and "What You'll Build" cards, but there's no concrete 2–3 bullet outcome statement that tells developers exactly what working code/feature they'll have at the end.

The existing `<Info>**Prerequisites**...</Info>` callout handles entry conditions, but nothing handles the exit promise.

### Change

Add a `<Note>` block **immediately before the `---` separator** that follows the `<Info>` prerequisites callout. This positions it after the developer understands the scope (diagram + cards) and before they start reading steps.

#### Template (customize per guide)

```mdx
<Note>
**After completing this guide you'll have:**
- A working [X feature] that [concrete outcome]
- [Y integration] connected to [where]
- [Z optional feature] set up and ready to extend
</Note>
```

#### Per-guide outcome statements

**build-a-social-feed.mdx**
```mdx
<Note>
**After completing this guide you'll have:**
- A live-updating user feed, community feed, and global feed rendering in your app
- Real-time post additions and deletions via Live Collections
- Post ranking configured and connected to the Admin Console
</Note>
```

**rich-content-creation.mdx**
```mdx
<Note>
**After completing this guide you'll have:**
- A post creation flow supporting text, image, video, and poll post types
- Media upload wired up with progress tracking
- @mentions and hashtag parsing enabled
</Note>
```

**comments-and-reactions.mdx**
```mdx
<Note>
**After completing this guide you'll have:**
- Threaded comments (comments + replies) on any post or story
- Emoji reactions added and removed in real-time
- Reaction counts and comment counts updating live in your UI
</Note>
```

**community-platform.mdx**
```mdx
<Note>
**After completing this guide you'll have:**
- Community creation flow (public and private) with categories
- Member join/leave and role assignment wired up
- Trending and recommended communities discoverable in-app
</Note>
```

**user-onboarding-and-visitor-mode.mdx**
```mdx
<Note>
**After completing this guide you'll have:**
- Visitor mode enabled so unauthenticated users can browse content
- A smooth visitor → authenticated transition with session continuity
- Profile setup step (display name, avatar) at first login
</Note>
```

**polls-and-interactive-content.mdx**
```mdx
<Note>
**After completing this guide you'll have:**
- Poll creation embedded inside a feed post (single and multiple choice)
- Voting, vote-change, and poll-close flows implemented
- Vote counts updating in real-time in your feed
</Note>
```

**user-profiles-and-social-graph.mdx**
```mdx
<Note>
**After completing this guide you'll have:**
- User profile display with avatar, bio, and follower/following counts
- Follow, unfollow, and connection-request flows working end-to-end
- Bidirectional blocking implemented with proper feed filtering
</Note>
```

**stories-and-ephemeral-content.mdx**
```mdx
<Note>
**After completing this guide you'll have:**
- Image and video story creation targeting communities and user profiles
- Story ring display with viewed/unviewed state on avatars
- Per-story view count and impression data accessible
</Note>
```

**notifications-and-engagement.mdx**
```mdx
<Note>
**After completing this guide you'll have:**
- An in-app notification tray with seen/unseen state and real-time delivery
- Push notifications (APNs and FCM) registered and firing for key events
- Notification triggers mapped to SDK events and webhook callbacks
</Note>
```

**events-and-activities.mdx**
```mdx
<Note>
**After completing this guide you'll have:**
- Event creation with title, description, date/time, and location
- RSVP (going / not going) flow with attendee list
- Events discoverable in community feeds and a dedicated events list
</Note>
```

**content-sharing-and-deep-links.mdx**
```mdx
<Note>
**After completing this guide you'll have:**
- Shareable URLs generated for posts, communities, and user profiles
- Deep link routing that opens your app directly to the target content
- Share sheet integration for native OS sharing on iOS, Android, and Web
</Note>
```

**realtime-presence-and-activity.mdx**
```mdx
<Note>
**After completing this guide you'll have:**
- Online/offline presence indicators on user avatars throughout the app
- Channel-level presence (who is currently viewing a community or room)
- Real-time event subscriptions for platform-wide activity tracking
</Note>
```

**post-impressions-and-creator-analytics.mdx**
```mdx
<Note>
**After completing this guide you'll have:**
- Post impression tracking firing on every feed scroll event
- Unique reach (`impression`) and total views (`markAsViewed`) both captured
- A "Who viewed this" list queryable per post for creator dashboards
</Note>
```

**search-and-discovery.mdx**
```mdx
<Note>
**After completing this guide you'll have:**
- Full-text post search integrated into your app's search bar
- Community search with trending and recommended community lists
- User-facing category browsing connected to community filtering
</Note>
```

**content-moderation-pipeline.mdx**
```mdx
<Note>
**After completing this guide you'll have:**
- User-side flag/unflag implemented for posts and comments
- Admin Console moderation review queue receiving flagged content
- An AI moderation rule set configured with at least one auto-action
- A webhook handler receiving moderation events for downstream automation
</Note>
```

**roles-permissions-and-governance.mdx**
```mdx
<Note>
**After completing this guide you'll have:**
- SDK permission checks (`hasPermission`) gating actions in your UI
- Community moderator role assignment and revocation working
- Post review mode (content gating) enabled in at least one community
- User ban and unban flows implemented
</Note>
```

**user-search-and-people-discovery.mdx**
```mdx
<Note>
**After completing this guide you'll have:**
- Display-name user search integrated and returning paginated results
- A "People you may know" suggestion list populated from the SDK
- Follow action triggered directly from search results
</Note>
```

**livestream-and-video-posts.mdx**
```mdx
<Note>
**After completing this guide you'll have:**
- A live broadcast room created inside a community with host and viewer flows
- Co-host invitation and live chat running during the stream
- Recordings accessible after the stream ends with playback wired up
</Note>
```

**short-form-video-clips.mdx**
```mdx
<Note>
**After completing this guide you'll have:**
- Clip post upload flow (video up to 15 min) with progress tracking
- Auto-play clip reel rendering in the feed with proper display mode
- Impression tracking firing when clips are visible on screen
</Note>
```

**advertising-and-monetization.mdx**
```mdx
<Note>
**After completing this guide you'll have:**
- Native ad units rendering in the feed at configured intervals
- Impression and click events tracked and sent to the Admin Console
- Ad frequency and targeting rules configured via the Admin Console
</Note>
```

### Placement

In every guide, insert this block:
- **After** the `<Info>**Prerequisites**...</Info>` callout (or after the prerequisite `<Info>` block)
- **Before** the first `---` separator that precedes the Quick Start section

---

## Chunk 7 — Add prerequisite dependency chain to selected guides

**Files:** ~12 guides that have hard dependencies on other guide features  
**Priority:** Medium — prevents developers from getting stuck mid-guide  
**Effort:** ~20 min

### Problem

Several guides silently assume the developer has completed an earlier guide. For example:
- Comments & Reactions requires posts to exist → depends on Rich Content Creation
- Stories requires a feed → depends on Build a Social Feed
- Notifications requires a working feed and communities
- Moderation requires content to moderate

Currently the `<Info>` callout only says "SDK installed and authenticated". It doesn't mention guide dependencies.

### Change

Update the `<Info>` prerequisite block in the affected guides to add a `**Also recommended:**` line with links to dependency guides.

#### Format

```mdx
<Info>
**Prerequisites**: SDK installed and authenticated → [SDK Setup](/social-plus-sdk/getting-started/overview). You'll need a valid `userId` and a `communityId`.

**Also recommended:** Complete [Build a Social Feed](/use-cases/social/build-a-social-feed) first — this guide creates the posts that appear in your feed.
</Info>
```

#### Dependency map

| Guide | Recommended prerequisite |
|---|---|
| `rich-content-creation.mdx` | Build a Social Feed |
| `comments-and-reactions.mdx` | Rich Content Creation (posts must exist to comment on) |
| `community-platform.mdx` | Build a Social Feed (community feeds are a feed type) |
| `stories-and-ephemeral-content.mdx` | User Profiles & Social Graph (stories target user profiles and communities) |
| `notifications-and-engagement.mdx` | Build a Social Feed + Community Platform |
| `events-and-activities.mdx` | Community Platform (events live inside communities) |
| `content-moderation-pipeline.mdx` | Rich Content Creation + Community Platform |
| `roles-permissions-and-governance.mdx` | Community Platform |
| `post-impressions-and-creator-analytics.mdx` | Build a Social Feed (impressions track posts in feeds) |
| `livestream-and-video-posts.mdx` | Community Platform (rooms are hosted in communities) |
| `short-form-video-clips.mdx` | Rich Content Creation (clips are a post type) |
| `advertising-and-monetization.mdx` | Build a Social Feed (ads appear in feeds) |

---

## Chunk 8 — Upgrade "Next Steps" with an opinionated first card

**Files:** All 20 guides in `use-cases/social/`  
**Priority:** Medium — reduces decision paralysis at the end of each guide  
**Effort:** ~30 min

### Problem

Every guide already has a `## Next Steps` section with a `<CardGroup cols={3}>` of 3 related guides. This is good but not opinionated — all 3 cards look equal, leaving the developer unsure which one to pick.

Stream and PubNub always include a single explicit "do this next" recommendation above the alternatives.

### Change

Modify each guide's `## Next Steps` section to add a single `<Card>` as a highlighted "Your next step" recommendation **before** the 3-card `<CardGroup>`. The existing 3-card group stays as "Or explore these".

```mdx
## Next Steps

<Card
  title="Your next step → Rich Content Creation"
  icon="arrow-right"
  href="/use-cases/social/rich-content-creation"
>
  Now that you have a working feed, give users something to post — text, images, videos, polls, and file posts.
</Card>

Or explore these related guides:

<CardGroup cols={3}>
  <Card title="Comments & Reactions" href="/use-cases/social/comments-and-reactions" icon="comments">
    Add engagement features to feed posts
  </Card>
  ...existing cards...
</CardGroup>
```

#### Opinionated "next step" per guide

| Guide | Recommended next |
|---|---|
| `build-a-social-feed.mdx` | Rich Content Creation |
| `rich-content-creation.mdx` | Comments & Reactions |
| `comments-and-reactions.mdx` | User Profiles & Social Graph |
| `community-platform.mdx` | Roles, Permissions & Governance |
| `user-onboarding-and-visitor-mode.mdx` | Build a Social Feed |
| `polls-and-interactive-content.mdx` | Comments & Reactions |
| `user-profiles-and-social-graph.mdx` | User Search & People Discovery |
| `stories-and-ephemeral-content.mdx` | Notifications & Engagement |
| `notifications-and-engagement.mdx` | Content Moderation Pipeline |
| `events-and-activities.mdx` | Notifications & Engagement |
| `content-sharing-and-deep-links.mdx` | Post Impressions & Creator Analytics |
| `realtime-presence-and-activity.mdx` | Notifications & Engagement |
| `post-impressions-and-creator-analytics.mdx` | Advertising & Monetization |
| `search-and-discovery.mdx` | User Search & People Discovery |
| `content-moderation-pipeline.mdx` | Roles, Permissions & Governance |
| `roles-permissions-and-governance.mdx` | Content Moderation Pipeline |
| `user-search-and-people-discovery.mdx` | User Profiles & Social Graph |
| `livestream-and-video-posts.mdx` | Short-Form Video Clips |
| `short-form-video-clips.mdx` | Post Impressions & Creator Analytics |
| `advertising-and-monetization.mdx` | Post Impressions & Creator Analytics |

---

## Chunk 9 — Real-world app callouts (optional)

**Files:** All 20 guides  
**Priority:** Low — adds social proof and context but doesn't block implementation  
**Effort:** ~25 min

### Problem

Features feel abstract without a reference to a real product that uses them. GetStream uses customer stats ("300% more conversions") for the same purpose.

### Change

Add a `<Tip>` callout near the top of each guide (after the `## What You'll Build` section) naming 2–3 real products that use this feature pattern.

#### Format

```mdx
<Tip>
**Used by apps like:** Instagram and TikTok (social feeds), Strava (activity feeds), LinkedIn (professional feeds). All use the same feed + live-update pattern this guide implements.
</Tip>
```

#### Per-guide examples

| Guide | Real-world examples |
|---|---|
| Build a Social Feed | Instagram, TikTok, Strava, LinkedIn |
| Rich Content Creation | Facebook, LinkedIn, Reddit |
| Comments & Reactions | Twitter/X, YouTube, Instagram |
| Community Platform | Reddit, Discord, Facebook Groups |
| User Onboarding & Visitor Mode | Pinterest, Twitch (pre-login browsing) |
| Polls & Interactive Content | Twitter/X polls, Instagram polls in stories |
| User Profiles & Social Graph | Twitter/X, LinkedIn, BeReal |
| Stories & Ephemeral Content | Instagram Stories, Snapchat, WhatsApp Status |
| Notifications & Engagement | Every major social app |
| Events & Activities | Meetup, Eventbrite, Strava clubs |
| Content Sharing & Deep Links | Instagram, TikTok, YouTube |
| Real-time Presence & Activity | Discord (online indicators), Slack |
| Post Impressions & Creator Analytics | YouTube Studio, TikTok Analytics, Instagram Insights |
| Search & Discovery | TikTok Explore, Reddit search, Twitter/X search |
| Content Moderation Pipeline | Reddit, Discord, YouTube |
| Roles, Permissions & Governance | Discord roles, Reddit moderators |
| User Search & People Discovery | Twitter/X "People you may know", LinkedIn |
| Livestream & Video Posts | Twitch, YouTube Live, Instagram Live |
| Short-Form Video Clips | TikTok, Instagram Reels, YouTube Shorts |
| Advertising & Monetization | Instagram, TikTok, Snapchat (native feed ads) |

---

## Chunk 10 — Completion checklist at guide bottom (optional)

**Files:** All 20 guides  
**Priority:** Low — nice for self-verification but adds length  
**Effort:** ~40 min

### Problem

Firebase Codelabs end with a "What you covered" checklist that signals completion and helps developers verify they didn't skip anything. Currently guides end with Next Steps cards, which is fine but skips the verification step.

### Change

Add a `## What You Built` or `## You're Done` section **above `## Next Steps`** in each guide. Use a `<Check>` component or a simple unordered list.

Since Mintlify doesn't have a native checklist component, use a `<Note>` with bullet points:

```mdx
## What You Built

<Note>
**In this guide you:**
- ✅ Queried user feeds, community feeds, and the global feed
- ✅ Subscribed to real-time post updates with Live Collections
- ✅ Configured post ranking and connected it to the Admin Console
- ✅ Connected feed flagging to the moderation pipeline
</Note>
```

---

## Implementation Order

Work through chunks in this order for maximum visible impact with minimum risk:

| Order | Chunk | Risk | Files changed |
|---|---|---|---|
| 1st | Chunk 1 — Fix dead ends | None | 1 |
| 2nd | Chunk 3 — Concepts accordion | None | 1 |
| 3rd | Chunk 5 — Difficulty badges | None | 1 |
| 4th | Chunk 2 — Persona routing | Low | 1 |
| 5th | Chunk 4 — Industry verticals | Low | 1 |
| 6th | Chunk 6 — Outcome statements | Medium | 20 |
| 7th | Chunk 7 — Dependency chain | Low | 12 |
| 8th | Chunk 8 — "Next step" card | Medium | 20 |
| 9th | Chunk 9 — Real-world callouts | Low | 20 |
| 10th | Chunk 10 — Completion checklists | Low | 20 |

---

*Last updated: March 28, 2026*
