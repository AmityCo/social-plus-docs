#!/bin/bash

# Script to fix common parsing errors in markdown files
# 1. Convert {% hint %} blocks to MDX format
# 2. Fix unclosed <img> tags
# 3. Fix other common parsing issues

echo "🔧 Fixing markdown parsing errors..."

# Function to fix hint blocks
fix_hints() {
    local file="$1"
    echo "  Fixing hints in: $file"
    
    # Convert info hints
    sed -i '' 's/{% hint style="info" %}/\<Info\>/g' "$file"
    sed -i '' 's/{% endhint %}/\<\/Info\>/g' "$file"
    
    # Convert warning hints
    sed -i '' 's/{% hint style="warning" %}/\<Warning\>/g' "$file"
    sed -i '' 's/{% endhint %}/\<\/Warning\>/g' "$file"
    
    # Convert success hints
    sed -i '' 's/{% hint style="success" %}/\<Tip\>/g' "$file"
    sed -i '' 's/{% endhint %}/\<\/Tip\>/g' "$file"
    
    # Convert error hints
    sed -i '' 's/{% hint style="danger" %}/\<Warning\>/g' "$file"
    sed -i '' 's/{% endhint %}/\<\/Warning\>/g' "$file"
}

# Function to fix image tags
fix_images() {
    local file="$1"
    echo "  Fixing image tags in: $file"
    
    # Fix unclosed img tags in figures
    sed -i '' 's/<img\([^>]*\)>\(<\/figcaption>\|<figcaption>\)/<img\1 \/>\2/g' "$file"
    
    # Fix standalone unclosed img tags
    sed -i '' 's/<img\([^>]*\)>\([^<]\)/\<img\1 \/\>\2/g' "$file"
    
    # Fix img tags without closing slash
    sed -i '' 's/<img\([^>]*[^\/]\)>/<img\1 \/>/g' "$file"
}

# Function to fix openapi references
fix_openapi() {
    local file="$1"
    echo "  Fixing openapi references in: $file"
    
    # Convert {% openapi %} blocks (these need manual review)
    sed -i '' 's/{% openapi.*%}/<!-- OpenAPI reference - needs manual conversion -->/g' "$file"
    sed -i '' 's/{% endopenapi %}/<!-- End OpenAPI reference -->/g' "$file"
}

# Process all markdown files in analytics-and-moderation
find "/Users/admin/Documents/GitHub/social-plus-docs/analytics-and-moderation" -name "*.md" -type f | while read -r file; do
    echo "Processing: $file"
    fix_hints "$file"
    fix_images "$file"
    fix_openapi "$file"
done

echo "✅ Fixed common parsing errors in analytics-and-moderation files"
