# Social Plus SDK Documentation Instructions

> ⚠️ **IMPORTANT**: This file has been superseded by the comprehensive documentation guide.
> 
> **Please refer to:** [`.github/COMPREHENSIVE_INSTRUCTIONS.md`](./COMPREHENSIVE_INSTRUCTIONS.md)
> 
> The comprehensive guide includes:
> - Complete project status and achievements
> - Merged UIKit and SDK documentation standards
> - AI assistant guidelines and best practices
> - Content creation patterns and examples
> - Quality assurance processes
> 
> This file is kept for historical reference but should not be used for new work.

---

## Legacy Content Overview

This document previously provided instructions for modernizing and enhancing the Social Plus SDK documentation. All content from this file has been integrated into the comprehensive guide above, along with:

- UIKit documentation standards
- Complete content creation patterns
- Multi-platform code examples
- Quality assurance processes
- AI assistant workflows

## Migration Status: ✅ COMPLETE

The major modernization projects documented in this file have been completed:

- **Social Module**: Complete restructuring ✅
- **Chat Module**: Full modernization (21+ files) ✅
- **Video SDK**: Broadcasting and playback guides ✅
- **UIKit**: Complete documentation overhaul ✅

---

**For all new work, please use the [COMPREHENSIVE_INSTRUCTIONS.md](./COMPREHENSIVE_INSTRUCTIONS.md) file.**

## 🎉 **MODERNIZATION SUCCESS SUMMARY**

### ✅ **COMPLETED MAJOR ACHIEVEMENTS**

🏗️ **Social Module**: Complete restructuring into logical workflows ✅ **DONE**  
💬 **Chat Module**: Phases 3-5 fully modernized (21+ files) ✅ **DONE**  
🎯 **Core Patterns**: Multi-platform examples & best practices ✅ **ESTABLISHED**  
🎥 **Video SDK**: New hybrid structure implemented ✅ **IN PROGRESS**

**Key Stats**: 21+ files modernized • 6 platforms supported • 100% legacy content eliminated

### 🚀 **CURRENT ACTIVE PROJECT: VIDEO SDK MIGRATION**

**Status**: Phase 1 - Content Migration & Broadcasting Guide Integration  
**Progress**: New structure created, base files ready, migration in progress  
**Priority**: High impact - consolidating 24+ repetitive files into streamlined structure

---

## 🎉 MAJOR RESTRUCTURING COMPLETED

### ✅ Social Module Complete Reorganization (DONE)

The Social module has been completely restructured into a logical, workflow-based organization that eliminates scattered functionality and creates intuitive navigation:

#### 🔄 **NEW STRUCTURE** (All files moved and organized):

1. **📁 Content Management** (`/social-plus-sdk/social/content-management/`)
   - **Posts** (`posts/`):
     - `creation/` - All post creation types (text, image, video, poll, etc.)
     - `management/` - Edit, delete, pin, review operations
     - `interactions/` - View, query, get, mention functionality  
     - `analytics/` - Post impressions and performance tracking
   - **Comments** (`comments/`):
     - `basic-operations/` - Create, edit, delete, view
     - `advanced-features/` - Mentions, reactions, real-time updates
     - `management/` - Query, search, organize comments
   - **Moderation** (`moderation/`):
     - `content-flagging/` - Centralized flagging for posts and comments
     - `review-process.mdx` - Structured moderation workflows

2. **📁 Communities & Spaces** (`/social-plus-sdk/social/communities-spaces/`)
   - `community-lifecycle/` - Create, update, delete, health monitoring
   - `membership/` - Join/leave, member queries, roles & permissions
   - `organization/` - Categories, structure, navigation systems
   - `discovery/` - Query, get, trending communities
   - `governance/` - Moderation, guidelines, conflict resolution

3. **📁 Discovery & Engagement** (`/social-plus-sdk/social/discovery-engagement/`)
   - `feed/` - Global feeds, custom ranking (moved from `/feed/`)
   - `search/` - Intelligent search (moved from `/intelligent-search/`)
   - `reactions/` - Add/remove, query reactions (moved from `/reactions/`)
   - `notifications/` - Notification tray (moved from `/notification-tray/`)
   - `stories/` - Create, delete, get stories (moved from `/stories/`)

4. **📁 User Interactions** (`/social-plus-sdk/social/user-interactions/`) - ALREADY COMPLETED
   - `follow-system/` - Follow/unfollow, requests, status, lists
   - `blocking-system/` - Block/unblock, manage blocked users

#### 🔧 **Key Improvements Made**:
- ✅ **Eliminated "README" naming** - All files now use descriptive `overview.mdx` names
- ✅ **Logical grouping** - Related functionality grouped by workflow, not technical boundaries  
- ✅ **Centralized moderation** - All flagging and moderation in one place
- ✅ **Better context** - Comments now contextually part of content management
- ✅ **Reduced duplication** - No more scattered flagging across multiple sections
- ✅ **Scalable structure** - Easy to add features without disrupting organization

#### 📋 **Navigation Updated**:
- ✅ **docs.json completely updated** with new structure
- ✅ **All file paths corrected** in navigation
- ✅ **Proper overview files created** for each section
- ✅ **Cross-references updated** between related sections

#### 🎯 **Token Limit Mitigation Strategies**:

To prevent future token limit issues when working on this documentation:

1. **Work in Focused Chunks**:
   - Focus on one major section at a time (e.g., just Content Management)
   - Work on subsections independently (e.g., just Posts → Creation)
   - Reference the completed structure below instead of re-analyzing

2. **Use Structure References**:
   - Reference this instruction file for current state
   - Use file searches to locate specific files instead of full workspace scans
   - Focus semantic searches on specific directories when needed

3. **Prioritize by Impact**:
   - **High Priority**: Content Management (most used features)
   - **Medium Priority**: Discovery & Engagement (user-facing features)  
   - **Low Priority**: Communities & Spaces (administrative features)

### 🎯 NEXT STEPS FOR CONTINUATION

When resuming work on this documentation:

1. **Video Module** (Future):
   - Structure video features by use case (streaming, recording)

### 🎯 Current Status: ✅ MAJOR MODERNIZATION COMPLETE

**🎉 What's Done - COMPREHENSIVE ACHIEVEMENTS**:

#### **Social Module** ✅ **COMPLETE**
- ✅ Complete structural reorganization into logical workflows
- ✅ All files moved to intuitive navigation structure  
- ✅ Navigation updated in docs.json with cross-references
- ✅ Modern file naming conventions implemented
- ✅ Centralized features with eliminated duplication

#### **Chat Module** ✅ **PHASES 3-5 COMPLETE** 
- ✅ **Phase 3**: Message Operations (5/5 files modernized)
- ✅ **Phase 4**: Message Types (7/7 files modernized)  
- ✅ **Phase 5**: Engagement Features (9/9 files modernized)
- ✅ **21+ files** completely modernized with multi-platform examples
- ✅ All legacy gist embeds and image-based code eliminated

#### **Core Foundations** ✅ **ESTABLISHED**
- ✅ Modern architecture patterns documented
- ✅ Multi-platform consistency (iOS, Android, JS, TS, Flutter)
- ✅ Advanced error handling and best practices
- ✅ Performance optimization examples
- ✅ Real-time features and offline support

**🚀 What's Next - Future Phases**:
- 🔄 **Video Module**: Complete modernization 
- 🔄 **UI Kit**: Component documentation enhancement
- 🔄 **Advanced Features**: Analytics, monitoring, advanced integrations

---

## 🎥 **VIDEO SDK MODERNIZATION PROJECT**

### 📋 **Project Overview**
The Video SDK is undergoing a complete restructuring from a repetitive platform-specific structure to a streamlined hybrid approach that eliminates content duplication while maintaining comprehensive platform coverage.

#### 🔄 **Structure Transformation**

**Before**: 24+ repetitive files across 6 platforms
```
video/
├── android/ (4 files: README, broadcast, view-play, push-notification)
├── ios/ (4 files: README, broadcast, view-play, push-notification)
├── web/ (4 files: README, live-stream, view-and-play, push-notification)
├── react-native/ (3 files: README, broadcast-live-stream, view-and-play)
├── flutter/ (3 files: README, view-play, push-notification)
└── typescript-react-native/ (3 files: README, live-stream, runquery-pattern)
```

**After**: Streamlined hybrid structure (60% fewer files)
```
video-new/
├── overview.mdx ✅ COMPLETE
├── getting-started/ ✅ COMPLETE
│   ├── overview.mdx ✅
│   ├── installation.mdx ✅ (All 6 platforms)
│   ├── authentication.mdx ✅ (Multi-platform)
│   └── first-stream.mdx ✅ (Step-by-step tutorial)
├── core-concepts/ 
│   └── overview.mdx ✅ COMPLETE
├── broadcasting/ 
│   └── setup.mdx ✅ COMPLETE (Advanced config guide)
├── playback/ 🔄 IN PROGRESS
├── notifications/ 🔄 IN PROGRESS
├── platform-specific/ 📝 PLANNED
└── troubleshooting/ 📝 PLANNED
```

### 🚀 **Migration Phases**

#### **Phase 1: Content Migration & Broadcasting** ✅ **MAJOR PROGRESS**

**Status**: Broadcasting guide complete with comprehensive multi-platform integration

**✅ Completed**:
- ✅ New directory structure established
- ✅ Overview page with feature matrix and platform comparison
- ✅ Complete installation guide covering all 6 platforms with tabs
- ✅ Authentication setup with multi-platform examples
- ✅ First stream tutorial with step-by-step implementation
- ✅ Core concepts overview with architecture diagrams
- ✅ **🎯 MAJOR ACHIEVEMENT: Complete Broadcasting Setup Guide** 
  - **Merged content from 5 platform-specific broadcasting files**
  - **Video quality settings and resolution configuration**
  - **Platform-specific setup with comprehensive code examples**
  - **Broadcasting controls (preview, start, stop, camera switching)**
  - **State management with real-time monitoring**
  - **Complete permission handling for all platforms**
  - **Advanced error handling and connection recovery**
  - **16:9 aspect ratio optimization guidance**

**Source Content Successfully Migrated**:
- ✅ `android/broadcast.mdx` (147 lines) → Integrated into `broadcasting/setup.mdx`
- ✅ `ios/broadcast.mdx` (118 lines) → Integrated into `broadcasting/setup.mdx`  
- ✅ `web/live-stream.mdx` (key sections) → Integrated into `broadcasting/setup.mdx`
- ✅ `react-native/broadcast-live-stream.mdx` → Integrated into `broadcasting/setup.mdx`
- ✅ `typescript-react-native/live-stream.mdx` (62 lines) → Integrated into `broadcasting/setup.mdx`

**Key Improvements Made**:
- 🔄 **Eliminated Repetition**: 5 separate platform files consolidated into 1 comprehensive guide
- 🎯 **Enhanced Developer Experience**: All platforms visible with tabs, consistent API usage
- 📚 **Comprehensive Coverage**: Added missing content like error handling, permissions, state management
- 🛡️ **Production Ready**: Included connection recovery, performance optimization, security best practices
- 📱 **Modern Standards**: Updated code examples, added TypeScript support, modern React patterns

#### **Phase 2: Playback & Viewing** � **READY TO START**

**Next Priority**: Create comprehensive playback and viewing guide

**Source Files to Migrate**:
- `android/view-play.mdx` → `playback/live-viewing.mdx`
- `ios/view-play.mdx` → `playback/live-viewing.mdx`
- `web/view-and-play-live-stream.mdx` (13 lines - needs enhancement) → `playback/live-viewing.mdx`
- `react-native/view-and-play-live-stream.mdx` → `playback/live-viewing.mdx`
- `flutter/view-play.mdx` → `playback/live-viewing.mdx`

**Content to Create**:
- Live stream viewing with player controls
- Recorded stream playback
- Quality selection and adaptive streaming
- Error handling for playback issues
- Multi-platform player implementations

**Estimated Impact**: Consolidate 5+ platform-specific playback files into 2 comprehensive guides

#### **Phase 3: Notifications & Events** 🔄 **IN PROGRESS**

**Current Priority**: Create comprehensive notification and stream event handling guides

**Source Files to Migrate**:
- `android/push-notification.mdx` → `notifications/push-notifications.mdx`
- `ios/push-notification.mdx` → `notifications/push-notifications.mdx`
- `web/push-notification.mdx` → `notifications/push-notifications.mdx`
- `flutter/push-notification.mdx` → `notifications/push-notifications.mdx`

**Content to Create**:
- Push notification setup and configuration
- Stream event notifications (start, end, error)
- Real-time event handling and webhooks
- Platform-specific notification customization
- Badge counts and notification management

**Estimated Impact**: Consolidate 4+ platform notification files into comprehensive guides

#### **Phase 4: Platform-Specific & Troubleshooting** 📝 **PLANNED**
- Consolidate push notification implementations
- Document platform-unique features
- Create troubleshooting guides

### 🎯 **Key Benefits Achieved**

1. **Reduced Repetition**: 60% fewer files to maintain
2. **Better Developer Experience**: All platforms visible in context
3. **Consistent API Usage**: Standardized examples across platforms
4. **Progressive Learning**: Clear path from basics to advanced features
5. **Easier Maintenance**: Single source of truth for common concepts

### ⚠️ **Token Length Management for Video Migration**

Given the extensive content being migrated, implement these strategies to handle token limits:

1. **Chunked Migration**: Process one platform at a time within broadcasting
2. **Content Summary**: Focus on key code examples and concepts
3. **Reference Extraction**: Move lengthy code blocks to focused sections
4. **Iterative Approach**: Build content in phases rather than all at once
5. **Context Preservation**: Maintain file context between migration chunks

---

## Modernization Standards

### Replace Legacy Elements
- **Remove**: `<CodeBlock url="https://gist.github.com/..." />` 
- **Remove**: `<Frame><img src="https://gist.github.com/..." /></Frame>`
- **Replace with**: Inline code examples using `<CodeGroup>` and platform-specific tabs

### Required MDX Components
Use these modern MDX components consistently:

```mdx
<Tabs>
  <Tab title="iOS">
    <CodeGroup>
      ```swift Basic Example
      // Code here
      ```
      ```swift Advanced Example  
      // Code here
      ```
    </CodeGroup>
  </Tab>
  <Tab title="Android">
    <CodeGroup>
      ```kotlin Basic Example
      // Code here
      ```
      ```kotlin Advanced Example
      // Code here  
      ```
    </CodeGroup>
  </Tab>
  <Tab title="TypeScript">
    <CodeGroup>
      ```typescript Basic Example
      // Code here
      ```
      ```typescript React Hook Example
      // Code here
      ```
    </CodeGroup>
  </Tab>
  <Tab title="Flutter">
    <CodeGroup>
      ```dart Basic Example
      // Code here
      ```
      ```dart Provider Example
      // Code here
      ```
    </CodeGroup>
  </Tab>
</Tabs>

<CardGroup cols={2}>
  <Card title="Feature Name" icon="icon-name">
    Description of the feature
  </Card>
</CardGroup>

<AccordionGroup>
  <Accordion title="Parameter Name">
    **Type:** `string`
    Description and validation rules
  </Accordion>
</AccordionGroup>

<Note>
Important information that users should be aware of
</Note>

<Info>
Additional helpful information or tips
</Info>
```

### Content Structure Template

Each modernized file should include:

1. **Title and Introduction**
   - Clear, descriptive title
   - Brief overview of functionality
   - Key benefits and use cases

2. **Architecture Overview**
   - Mermaid diagram showing data flow
   - System interactions
   - Key components

3. **Feature Summary**
   - `<CardGroup>` highlighting main features
   - Icons and brief descriptions

4. **Implementation Sections**
   - Parameters with `<AccordionGroup>`
   - Multi-platform code examples with `<Tabs>` and `<CodeGroup>`
   - Basic and advanced usage patterns

5. **Best Practices**
   - `<AccordionGroup>` with practical guidelines
   - Performance optimization tips
   - Error handling strategies
   - UI/UX considerations

6. **Use Cases**
   - `<CardGroup>` with real-world scenarios
   - Implementation approaches
   - Business context

7. **Advanced Features** (when applicable)
   - Code examples for complex scenarios
   - Integration patterns
   - Optimization techniques

8. **Error Handling**
   - Common error scenarios
   - Recommended responses
   - Troubleshooting guide

### Code Quality Standards

#### Multi-Platform Coverage
Provide comprehensive examples for:
- **iOS**: Swift with UIKit/SwiftUI patterns
- **Android**: Kotlin with modern Android architecture
- **TypeScript**: React hooks and modern JS patterns  
- **Flutter**: Dart with Provider/Bloc patterns

#### Code Example Patterns
```typescript
// Basic implementation
class BasicExample {
    // Simple, clear implementation
}

// Advanced implementation with error handling
class AdvancedExample {
    // Comprehensive implementation with:
    // - Error handling
    // - Loading states  
    // - Performance optimization
    // - Real-world patterns
}

// React Hook example
const useFeature = () => {
    // Modern React patterns
    // Custom hook implementation
    // Type safety
}
```
### 📋 **Project Overview**
The Video SDK is undergoing a complete restructuring from a repetitive platform-specific structure to a streamlined hybrid approach that eliminates content duplication while maintaining comprehensive platform coverage.

#### 🔄 **Structure Transformation**

#### Mermaid Diagrams
Use consistent mermaid diagram patterns:
```mermaid
graph TB
    A[User Action] --> B[Validation]
    B --> C{Success?}
    C -->|Yes| D[Process Request]
    C -->|No| E[Handle Error]
    D --> F[Update UI]
    E --> G[Show Error Message]