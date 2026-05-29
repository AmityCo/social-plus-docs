---
name: release-notes
description: Write and update release notes / changelogs for all SDK and UIKit platforms. Use when asked to update changelogs, write release notes, check for new releases, or sync changelog entries across platforms.
metadata:
  author: social.plus
  version: "1.0"
---

# Release Notes Skill

## When to Use

Use this skill when the user asks to:
- Update release notes or changelogs
- Check for new releases across SDK/UIKit platforms
- Write changelog entries for latest releases
- Sync changelogs from source repos to the docs site

Common trigger phrases: "update release notes", "write changelogs", "check for new releases", "sync release notes", "update changelogs for all platforms"

## Architecture

### Documentation Changelog Files

All changelogs live in the docs repo at:

**SDK Changelogs** (`social-plus-sdk/changelogs/`):
| File | Platform | Source Repo |
|------|----------|-------------|
| `android-sdk-changelog.mdx` | Android SDK | `Amity-Social-Cloud-SDK-Android` |
| `ios-sdk-changelog.mdx` | iOS SDK | `AmitySDKIOS` (tags from `Amity-Social-Cloud-SDK-iOS-SwiftPM`) |
| `web-sdk-changelog.mdx` | TypeScript SDK | `AmityTypescriptSDK` |
| `flutter-sdk-changelog.mdx` | Flutter SDK | `Amity-Social-Cloud-SDK-Flutter-Internal` |

**UIKit Changelogs** (`uikit/changelogs/`):
| File | Platform | Source Repo |
|------|----------|-------------|
| `android-uikit-changelog.mdx` | Android UIKit | `UIKit-V4` |
| `ios-uikit-changelog.mdx` | iOS UIKit | `AmityUIKitIOS` (tags from `ASC-UIKit-iOS-OpenSource`) |
| `web-uikit-changelog.mdx` | Web UIKit | `Amity-Social-Cloud-UIKit-Web` |
| `react-native-uikit-changelog.mdx` | React Native UIKit | `Amity-Social-UIKit-React-Native-CLI-OpenSource` |
| `flutter-uikit-changelog.mdx` | Flutter UIKit | `Amity-Social-Cloud-UIKit-Flutter` |

### Source Repo Locations (Local)

```
/Users/nakarinjupattanakul/Documents/GitHub/Amity-Social-Cloud-SDK-Android
/Users/nakarinjupattanakul/Documents/GitHub/AmitySDKIOS
/Users/nakarinjupattanakul/Documents/GitHub/AmityTypescriptSDK
/Users/nakarinjupattanakul/Documents/GitHub/Amity-Social-Cloud-SDK-Flutter-Internal
/Users/nakarinjupattanakul/Documents/GitHub/UIKit-V4
/Users/nakarinjupattanakul/Documents/GitHub/AmityUIKitIOS
/Users/nakarinjupattanakul/Documents/GitHub/Amity-Social-Cloud-UIKit-Web
/Users/nakarinjupattanakul/Documents/GitHub/Amity-Social-UIKit-React-Native-CLI-OpenSource
/Users/nakarinjupattanakul/Documents/GitHub/Amity-Social-Cloud-UIKit-Flutter
```

GitHub org: `AmityCo`

### Platform-specific changelog source conventions

- **Android SDK/UIKit**: Releases tagged in GitHub (e.g., `7.21.0`, `4.17.0`). Changelogs may be in GitHub Releases page. Use `git log` between tags for actual changes.
- **iOS SDK**: Tags in the SwiftPM distribution repo `Amity-Social-Cloud-SDK-iOS-SwiftPM`. Source changes in `AmitySDKIOS`. May have release notes at `https://github.com/AmityCo/Amity-Social-Cloud-SDK-iOS-SwiftPM/releases`.
- **iOS UIKit**: Tags in `ASC-UIKit-iOS-OpenSource`. Source changes in `AmityUIKitIOS`. May have release notes at `https://github.com/AmityCo/ASC-UIKit-iOS-OpenSource/releases`.
- **TypeScript SDK**: Version bumps as commits in `develop` branch (not git tags). Check `package.json` version and commits like `v7.21.0 (#1437)`.
- **Web UIKit**: Releases as draft in GitHub Releases. Tags like `v4.16.0`.
- **React Native UIKit**: Tags like `v4.0.0-RC.23`.
- **Flutter SDK**: Tags in internal repo. May also publish to `https://pub.dev/packages/amity_sdk/changelog`.
- **Flutter UIKit**: Tags in `Amity-Social-Cloud-UIKit-Flutter`. May also be at `https://github.com/AmityCo/Amity-Social-UIKit-Flutter-Opensource/releases`.

## Workflow

### Step 1: Identify Latest Recorded Versions

Read the first `<Update>` entry from each changelog file to find the latest recorded version and date.

### Step 2: Find New Releases in Source Repos

For each platform:
1. `git fetch` the source repo (ensure up to date)
2. List tags sorted by date: `git tag --sort=-creatordate | head -20`
3. Get dates: `git log -1 --format='%ai' <tag>`
4. For TypeScript SDK (no tags): check commit messages for version bumps like `v7.21.0 (#1437)` and `package.json` version

Identify tags/versions released AFTER the latest recorded date.

### Step 3: Gather Changes

For each new release:
1. Get commit log between tags: `git log --oneline <previous-tag>..<new-tag>`
2. Check for GitHub release notes (may 404 if repos are private — that's fine)
3. Look for CHANGELOG.md in the repo if it exists
4. Cross-reference commit messages with the official changelog to ensure completeness
5. Check for dependency version changes (build.gradle, package.json, pubspec.yaml)

### Step 4: Write Changelog Entries

Use the exact format below. Entries are **newest-first** in each file.

### Step 5: Verify

Check that the new entries are valid MDX and follow the established patterns.

## Changelog Entry Format

### Standard Template

```mdx
<Update label="VERSION  (DD/MM/YYYY)" tags={["TAG1", "TAG2"]}>
  ## 🚀 New Features

  #### Feature Title
  Description of the feature and what it enables.

  ## Improvements

  - Improvement description.

  ## 🐞 Bug Fixes

  - Fixed specific bug description.

  ## 🚨 Compatibility Changes

  - Breaking change description.

  ## 🧩 Compatibility

  <AccordionGroup>
    <Accordion title="Platform SDK" icon="gear">
      | Config           | Version |
      | :--------------- | :------ |
      | minSDKVersion    | XX      |
      | targetSDKVersion | XX      |
    </Accordion>
    <Accordion title="Dependencies" icon="book">
      | Library          | Version |
      | :--------------- | :------ |
      | Dependency Name  | X.Y.Z   |
    </Accordion>
  </AccordionGroup>
</Update>
```

### Rules

1. **Date format**: `DD/MM/YYYY`
2. **Tags**: Use `["New Releases"]` for features, `["Improvements"]` for bug fixes only, `["New Releases", "Improvements"]` for both
3. **Section order**: New Features → Improvements → Bug Fixes → Compatibility Changes → Compatibility
4. **Omit empty sections** — only include sections that have content
5. **Compatibility table**: Always include for Android SDK/UIKit. Optional for others depending on platform convention:
   - Android SDK: "Android SDK" config + "Dependencies" tables
   - Android UIKit: "Android SDK" config + "Dependencies" (include `Amity-Social-Cloud-SDK` version)
   - iOS SDK: "iOS SDK" config + "Dependencies"
   - iOS UIKit: "iOS SDK" config + "Dependencies" (include `Amity-Social-Cloud-SDK` version)
   - TypeScript SDK: "Environment" with NodeJS/NPM versions
   - Web UIKit: "Environment" with NodeJS/PNPM/React versions
   - React Native UIKit: "Environment" + "iOS SDK" + "Android SDK" (3 accordions)
   - Flutter SDK/UIKit: "Environment" with Flutter version
6. **Feature descriptions**: Write clear, developer-facing descriptions. Don't just copy commit messages — synthesize them into meaningful release notes.
7. **Bug fix style**: Start with "Fixed..." and describe what was wrong, not the implementation detail.

### Writing Quality Guidelines

- **Don't blindly copy commit messages**. They are often terse or implementation-focused.
- **Cross-reference** the official changelog (GitHub Releases, CHANGELOG.md) with actual git commits to find undocumented changes.
- **Group related fixes** — e.g., multiple permission-related fixes can be summarized as one bullet point.
- **Highlight user-facing impact** — frame changes in terms of what the developer/user experiences.
- **For new features**: Use `####` sub-headings with a short title and 1-2 sentence description.
- **For bug fixes**: Use bullet list with concise descriptions starting with "Fixed".

## Dependency Version Lookup

### Android SDK
```bash
cd Amity-Social-Cloud-SDK-Android
grep -n 'compileSdk\|targetSdk\|minSdk' buildsystem/dependencies.gradle
```

### Android UIKit  
```bash
cd UIKit-V4
grep -n 'amityMessagingSdkVersion\|amityCompileSdk\|amityMinSdk\|amityTargetSdk' buildsystem/dependencies.gradle
```

### TypeScript SDK
```bash
cd AmityTypescriptSDK
cat package.json | grep '"version"'
```

### Web UIKit
```bash
cd Amity-Social-Cloud-UIKit-Web
cat package.json | grep -E '"version"|ts-sdk'
```

### Flutter SDK/UIKit
```bash
cd Amity-Social-Cloud-SDK-Flutter-Internal  # or Amity-Social-Cloud-UIKit-Flutter
cat pubspec.yaml | grep 'version:'
```

## Special Notes

- **iOS changelogs** use `rss: "true"` (string) in frontmatter, all others use `rss: true` (boolean)
- **iOS SDK and UIKit** have a `<Note>` block before the first `<Update>` for Xcode compatibility notices
- **TypeScript SDK** repo uses commit-based versioning on `develop` branch, not git tags. Look for commits like `Release v7.21.0 (#1437)` or `v7.20.0 (#1432)`
- **Android UIKit minSdkVersion** comes from the UIKit's own `buildsystem/dependencies.gradle`, not the SDK's
- Some repos are private — GitHub release page URLs will 404 via web fetch. Rely on local git repos instead.
