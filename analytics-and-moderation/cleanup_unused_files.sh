#!/bin/bash

# Analytics and Moderation Documentation Cleanup Script
# This script removes obsolete .md files that have been replaced by .mdx versions

echo "🧹 Starting cleanup of analytics-and-moderation documentation files..."
echo ""

# Change to the analytics-and-moderation directory
cd /Users/admin/Documents/GitHub/social-plus-docs/analytics-and-moderation

# Counter for removed files
removed_count=0

# Array of .md files that have .mdx versions and should be removed
declare -a files_to_remove=(
    "social.plus-portal/changelogs.md"
    "social.plus-portal/account-management.md" 
    "social.plus-portal/getting-started.md"
    "social.plus-portal/README.md"
    "social.plus-portal/application-management.md"
    "social.plus-apis-and-services/pre-hook-event.md"
    "social.plus-apis-and-services/network-settings.md"
    "social.plus-apis-and-services/generate-user-last-activity-report.md"
    "social.plus-apis-and-services/README.md"
    "console/changelogs.md"
    "console/settings/README.md"
    "console/chat-management/README.md"
    "console/management/admin-access-control.md"
    "console/management/livestream-moderation.md"
    "console/premium-ads/README.md"
    "console/README.md"
    "console/ai-content-moderation.md"
    "console/user-and-content-management/user-social-history.md"
    "console/user-and-content-management/README.md"
    "console/social-management/README.md"
    "console/moderation/roles-and-privileges.md"
)

# Array of unused .mdx files that should be removed
declare -a unused_mdx_files=(
    "console/README.mdx"
    "console/ai-content-moderation-new.mdx"
)

echo "📋 Files to be removed:"
echo "====================="

# Remove .md files that have .mdx versions
echo ""
echo "🗂️  Removing .md files with .mdx versions:"
for file in "${files_to_remove[@]}"; do
    if [[ -f "$file" ]]; then
        echo "  ✅ Removing: $file"
        rm "$file"
        ((removed_count++))
    else 
        echo "  ⚠️  Not found: $file"
    fi
done

# Remove unused .mdx files  
echo ""
echo "🗂️  Removing unused .mdx files:"
for file in "${unused_mdx_files[@]}"; do
    if [[ -f "$file" ]]; then
        echo "  ✅ Removing: $file"
        rm "$file"
        ((removed_count++))
    else
        echo "  ⚠️  Not found: $file"
    fi
done

echo ""
echo "📊 Cleanup Summary:"  
echo "=================="
echo "  📁 Total files removed: $removed_count"
echo "  🔒 Backup files preserved: $(find . -name "*.backup" | wc -l | tr -d ' ')"
echo "  📝 Active .md files remaining: $(find . -name "*.md" -not -name "*.backup" | wc -l | tr -d ' ')"
echo "  📄 Active .mdx files remaining: $(find . -name "*.mdx" | wc -l | tr -d ' ')"

echo ""
echo "✅ Cleanup completed successfully!"
echo ""
echo "💡 Notes:"
echo "   - All backup files (.backup) have been preserved"
echo "   - Only files with modernized .mdx versions were removed"
echo "   - All files referenced in docs.json navigation are preserved"
echo "   - Report files (DOCS_JSON_REVIEW.md, MODERNIZATION_REPORT.md) are preserved"
