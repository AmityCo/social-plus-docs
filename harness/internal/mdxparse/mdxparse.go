package mdxparse

import (
"bufio"
"os"
"strings"
"unicode"
)

// Section represents a ### heading that is followed by a <CodeGroup> block.
type Section struct {
Heading string // e.g. "### Step 1: Initialize the SDK"
Slug    string // e.g. "step-1-initialize-the-sdk"
}

// ExtractSections scans an MDX file and returns all ### headings
// that are followed by a <CodeGroup> within the next 10 non-blank lines.
// Stops looking for CodeGroup when it hits another heading (## or ###).
func ExtractSections(path string) ([]Section, error) {
f, err := os.Open(path)
if err != nil {
return nil, err
}
defer f.Close()

var lines []string
sc := bufio.NewScanner(f)
for sc.Scan() {
lines = append(lines, sc.Text())
}
if err := sc.Err(); err != nil {
return nil, err
}

var sections []Section
for i, line := range lines {
if !strings.HasPrefix(strings.TrimSpace(line), "### ") {
continue
}
heading := strings.TrimSpace(line)
nonBlank := 0
for j := i + 1; j < len(lines) && nonBlank < 10; j++ {
trimmed := strings.TrimSpace(lines[j])
if trimmed == "" {
continue
}
if strings.Contains(trimmed, "<CodeGroup>") {
sections = append(sections, Section{
Heading: heading,
Slug:    slugify(strings.TrimPrefix(heading, "### ")),
})
break
}
if strings.HasPrefix(trimmed, "## ") || strings.HasPrefix(trimmed, "### ") {
break
}
}
}
return sections, nil
}

func slugify(s string) string {
var b strings.Builder
prevDash := false
for _, r := range strings.ToLower(s) {
if unicode.IsLetter(r) || unicode.IsDigit(r) {
b.WriteRune(r)
prevDash = false
} else if !prevDash && b.Len() > 0 {
b.WriteRune('-')
prevDash = true
}
}
out := b.String()
out = strings.Trim(out, "-")
out = strings.ReplaceAll(out, "--", "-")
for strings.Contains(out, "--") {
	out = strings.ReplaceAll(out, "--", "-")
}
return out
}
