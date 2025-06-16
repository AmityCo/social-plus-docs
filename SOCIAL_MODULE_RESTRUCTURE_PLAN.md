# Social Module Restructuring Plan

## Current Structure Analysis

### ✅ Well-Organized Sections
- **Comments** (11 files) - Good granular breakdown
- **Posts** (12 files + create-post subdir) - Well organized with creation types
- **Communities** (10 files) - Comprehensive coverage
- **Stories** (6 files) - Appropriate scope

### 🔧 Needs Restructuring

#### 1. User Interactions (Currently Scattered)
**Current:**
- `/follow-unfollow/` (5 files)
- `/block-and-unblock-user.mdx` (standalone file)

**Proposed: Consolidate into `/user-interactions/`**
```
/social-plus-sdk/social/user-interactions/
├── README.mdx (Overview of all user interaction features)
├── follow-system/
│   ├── README.mdx
│   ├── follow-unfollow-user.mdx
│   ├── accept-decline-follow-request.mdx
│   ├── get-connection-status.mdx (renamed for clarity)
│   └── get-follower-following-list.mdx
├── blocking-system/
│   ├── README.mdx
│   ├── block-unblock-user.mdx
│   └── manage-blocked-users.mdx (extracted from main file)
└── user-profile/
    ├── README.mdx
    ├── get-user-profile.mdx
    ├── update-user-profile.mdx
    └── user-privacy-settings.mdx
```

#### 2. Content Discovery (Currently Scattered)
**Current:**
- `/feed/` (3 files)
- `/intelligent-search/` (3 files)

**Proposed: Enhance both sections**
```
/social-plus-sdk/social/content-discovery/
├── README.mdx (Overview)
├── feeds/
│   ├── README.mdx
│   ├── global-feed.mdx
│   ├── user-feed.mdx
│   ├── community-feed.mdx
│   ├── custom-post-ranking.mdx
│   └── feed-personalization.mdx
├── search/
│   ├── README.mdx
│   ├── search-posts.mdx
│   ├── search-communities.mdx
│   ├── search-users.mdx
│   └── advanced-search-filters.mdx
└── recommendations/
    ├── README.mdx
    ├── recommended-posts.mdx
    ├── recommended-communities.mdx
    └── trending-content.mdx
```

#### 3. Engagement Features (New Grouping)
**Current:**
- `/reactions/` (3 files)
- `/notification-tray/` (5 files)

**Proposed: Keep separate but enhance**
```
/social-plus-sdk/social/engagement/
├── README.mdx
├── reactions/
│   ├── README.mdx
│   ├── add-remove-reaction.mdx  
│   ├── query-reactions.mdx
│   ├── custom-reactions.mdx (new)
│   └── reaction-analytics.mdx (new)
├── notifications/
│   ├── README.mdx
│   ├── notification-system-overview.mdx
│   ├── query-notifications.mdx
│   ├── mark-notifications-seen.mdx
│   ├── notification-preferences.mdx
│   └── push-notification-setup.mdx
└── activity-tracking/
    ├── README.mdx
    ├── user-activity-feed.mdx
    ├── content-impressions.mdx
    └── engagement-analytics.mdx
```

## Improved Main Social README Structure

### Proposed Sections:

1. **Core Content Features**
   - Posts (Content Creation & Management)
   - Comments (Discussion & Engagement)
   - Stories (Ephemeral Content)

2. **Community Features**
   - Communities (Groups & Spaces)
   - Moderation Tools

3. **User Interactions**
   - Follow/Unfollow System
   - User Blocking & Privacy
   - User Profiles & Settings

4. **Content Discovery**
   - Feeds & Timelines
   - Search & Filtering
   - Recommendations

5. **Engagement & Analytics**
   - Reactions & Emotions
   - Notifications & Alerts
   - Activity Tracking

6. **Advanced Features**
   - Content Moderation
   - Analytics & Insights
   - Customization Options

## File Naming Improvements

### Current Issues:
- `get-connection-status-and-connection-counter.mdx` (too long)
- `flag-unflag.mdx` (unclear context)
- `block-and-unblock-user.mdx` (inconsistent with directory naming)

### Proposed Improvements:
- `get-connection-status.mdx`
- `flag-unflag-content.mdx`
- `block-unblock-user.mdx`

## Cross-Reference Strategy

### Navigation Improvements:
1. **Related Content Cards** at the bottom of each page
2. **Quick Navigation** sidebar for each section
3. **Getting Started Flows** for common use cases
4. **Integration Examples** showing features working together

## Implementation Priority

### Phase 1: Logical Grouping (Immediate)
1. Update main Social README with better organization
2. Add cross-references between related features
3. Improve file naming consistency

### Phase 2: Structural Changes (Future)
1. Consolidate user interaction features
2. Enhance content discovery section
3. Create engagement hub
4. Implement advanced navigation

### Phase 3: Content Enhancement (Ongoing)
1. Add integration examples
2. Create getting started workflows
3. Enhance cross-platform consistency
4. Add advanced use cases

## Benefits of Restructuring

1. **Better Developer Experience**: Logical grouping reduces cognitive load
2. **Improved Navigation**: Related features are easier to find
3. **Enhanced Discoverability**: Cross-references help developers find related functionality
4. **Scalability**: Structure supports adding new features without confusion
5. **Consistency**: Standardized naming and organization patterns
