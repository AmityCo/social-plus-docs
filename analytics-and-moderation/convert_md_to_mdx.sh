#!/bin/bash

# Convert all remaining .md files to .mdx for Mintlify compatibility
# This script converts active .md files to .mdx format

echo "🔄 Converting remaining .md files to .mdx for Mintlify compatibility..."
echo ""

# Change to the analytics-and-moderation directory
cd /Users/admin/Documents/GitHub/social-plus-docs/analytics-and-moderation

# Counter for converted files
converted_count=0

# Array of .md files to convert to .mdx
declare -a files_to_convert=(
    "social+-portal/dashboard/raw-data-export.md"
    "social+-portal/dashboard/README.md"
    "console/settings/push-notifications.md"
    "console/settings/security/admin-token-management.md"
    "console/settings/security/README.md"
    "console/settings/brand-settings.md"
    "console/settings/image-moderation.md"
    "console/chat-management/channel-management.md"
    "console/chat-management/messaging-management.md"
    "console/chat-management/chat-activities-beta.md"
    "console/premium-ads/setting-up-premium-ads.md"
    "console/premium-ads/setting-up-advertiser-profile.md"
    "console/social-management/communities.md"
    "console/social-management/stories.md"
    "console/social-management/social-management/social-management-1.md"
    "console/social-management/social-management/social-management.md"
    "console/social-management/social-management/README.md"
    "console/social-management/social-management/post-pinning-and-featuring.md"
    "console/social-management/social-management-1/README.md"
    "console/social-management/social-management-1/comment-viewing-and-management.md"
    "console/social-management/social-management-1/comment-creation-and-reply.md"
)

echo "📋 Converting files to .mdx format:"
echo "=================================="

# Convert each .md file to .mdx
for file in "${files_to_convert[@]}"; do
    if [[ -f "$file" ]]; then
        # Create .mdx version
        mdx_file="${file%.md}.mdx"
        echo "  ✅ Converting: $file → $mdx_file"
        
        # Copy content to .mdx file
        cp "$file" "$mdx_file"
        
        # Remove original .md file
        rm "$file"
        
        ((converted_count++))
    else 
        echo "  ⚠️  Not found: $file"
    fi
done

echo ""
echo "📊 Conversion Summary:"  
echo "===================="
echo "  📄 Files converted to .mdx: $converted_count"
echo "  📝 Active .md files remaining: $(find . -name "*.md" -not -name "*.backup" -not -name "*REPORT.md" -not -name "cleanup_unused_files.sh" | wc -l | tr -d ' ')"
echo "  📄 Total .mdx files: $(find . -name "*.mdx" | wc -l | tr -d ' ')"

echo ""
echo "✅ Conversion completed successfully!"
echo ""
echo "🔧 Next step: Update docs.json to reference .mdx files..."
