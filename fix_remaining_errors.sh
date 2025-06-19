#!/bin/bash

# Script to fix remaining parsing errors
echo "🔧 Fixing remaining parsing errors..."

# Function to fix all {% code %} blocks
fix_code_blocks() {
    local file="$1"
    echo "  Fixing code blocks in: $file"
    
    # Convert {% code title="..." %} to ```lang title="..."
    sed -i '' 's/{% code title="\([^"]*\)" %}/```json title="\1"/g' "$file"
    sed -i '' 's/{% code %}/```/g' "$file"
    sed -i '' 's/{% endcode %}/```/g' "$file"
}

# Function to fix HTML comments to MDX comments
fix_html_comments() {
    local file="$1"
    echo "  Fixing HTML comments in: $file"
    
    # Convert HTML comments to MDX comments
    sed -i '' 's/<!-- \(.*\) -->/{\/* \1 *\/}/g' "$file"
}

# Function to fix any remaining {% hint %} blocks that weren't caught
fix_remaining_hints() {
    local file="$1"
    echo "  Fixing remaining hints in: $file"
    
    # Fix any style variations that were missed
    sed -i '' 's/{% hint style='\''info'\'' %}/\<Info\>/g' "$file"
    sed -i '' 's/{% hint style='\''warning'\'' %}/\<Warning\>/g' "$file"
    sed -i '' 's/{% hint style='\''success'\'' %}/\<Tip\>/g' "$file"
    sed -i '' 's/{% hint style='\''danger'\'' %}/\<Warning\>/g' "$file"
    sed -i '' 's/{% hint style='\''error'\'' %}/\<Warning\>/g' "$file"
}

# Process all markdown files in analytics-and-moderation
find "/Users/admin/Documents/GitHub/social-plus-docs/analytics-and-moderation" -name "*.md" -type f | while read -r file; do
    echo "Processing: $file"
    fix_code_blocks "$file"
    fix_html_comments "$file"
    fix_remaining_hints "$file"
done

echo "✅ Fixed remaining parsing errors"
