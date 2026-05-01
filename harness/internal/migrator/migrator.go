package migrator

import (
	"fmt"
	"os"
	"strings"
)

// KebabToPascal converts "community-create" → "CommunityCreate".
// Also strips file extensions and replaces non-identifier characters.
func KebabToPascal(key string) string {
	// Strip file extension (e.g. "_poll_live_object.dart" → "_poll_live_object")
	if dot := strings.LastIndex(key, "."); dot >= 0 {
		key = key[:dot]
	}
	// Split on hyphens and underscores
	parts := strings.FieldsFunc(key, func(r rune) bool { return r == '-' || r == '_' })
	var b strings.Builder
	for _, p := range parts {
		if p == "" {
			continue
		}
		b.WriteString(strings.ToUpper(p[:1]) + p[1:])
	}
	result := b.String()
	if result == "" {
		return "Snippet"
	}
	// Ensure starts with a letter (prefix X if starts with digit)
	if result[0] >= '0' && result[0] <= '9' {
		result = "X" + result
	}
	return result
}

// AddImport inserts an import statement at the top of content if not already present.
// Ensures a blank line separates the last import from any following frontmatter (---).
func AddImport(content, componentName, importPath string) string {
	importLine := fmt.Sprintf("import %s from '%s';", componentName, importPath)
	if strings.Contains(content, importLine) {
		return content // idempotent
	}
	updated := importLine + "\n" + content
	// Ensure blank line before frontmatter if imports immediately precede ---
	updated = ensureBlankBeforeFrontmatter(updated)
	return updated
}

// ensureBlankBeforeFrontmatter inserts a blank line between the last import
// statement and a following --- frontmatter block if none exists.
func ensureBlankBeforeFrontmatter(content string) string {
	lines := strings.Split(content, "\n")
	for i := 1; i < len(lines); i++ {
		if lines[i] == "---" && strings.HasPrefix(lines[i-1], "import ") {
			// Insert blank line
			newLines := make([]string, 0, len(lines)+1)
			newLines = append(newLines, lines[:i]...)
			newLines = append(newLines, "")
			newLines = append(newLines, lines[i:]...)
			return strings.Join(newLines, "\n")
		}
	}
	return content
}

// ReplaceCodeGroup replaces the first <CodeGroup>...</CodeGroup> block in content
// with <ComponentName />. Returns (updated content, true) if replaced, (original, false) if not found.
func ReplaceCodeGroup(content, componentName string) (string, bool) {
	open := strings.Index(content, "<CodeGroup>")
	if open == -1 {
		return content, false
	}
	closeIdx := strings.Index(content[open:], "</CodeGroup>")
	if closeIdx == -1 {
		return content, false
	}
	closeEnd := open + closeIdx + len("</CodeGroup>")
	replacement := "<" + componentName + " />"
	return content[:open] + replacement + content[closeEnd:], true
}

// ReplaceCodeGroupAfterHeading finds the first <CodeGroup>...</CodeGroup> block that
// appears after the given heading line and replaces it with <ComponentName />.
// - heading must match the full trimmed line (e.g. "### Step 2: Login User")
// - Stops searching for CodeGroup if it hits another ### or ## heading
// - Returns (updated content, true) if replaced, (original, false) if not found
func ReplaceCodeGroupAfterHeading(content, heading, componentName string) (string, bool) {
	lines := strings.Split(content, "\n")
	trimmedHeading := strings.TrimSpace(heading)
	headingIdx := -1
	for i, line := range lines {
		if strings.TrimSpace(line) == trimmedHeading {
			headingIdx = i
			break
		}
	}
	if headingIdx == -1 {
		return content, false
	}
	// Search for <CodeGroup> after heading, but stop at next heading
	start := -1
	end := -1
	for i := headingIdx + 1; i < len(lines); i++ {
		trim := strings.TrimSpace(lines[i])
		if strings.HasPrefix(trim, "### ") || strings.HasPrefix(trim, "## ") {
			break
		}
		if start == -1 && trim == "<CodeGroup>" {
			start = i
			// Now find matching </CodeGroup>
			for j := i + 1; j < len(lines); j++ {
				if strings.TrimSpace(lines[j]) == "</CodeGroup>" {
					end = j
					break
				}
				if strings.HasPrefix(strings.TrimSpace(lines[j]), "### ") || strings.HasPrefix(strings.TrimSpace(lines[j]), "## ") {
					break
				}
			}
			break
		}
	}
	if start != -1 && end != -1 {
		newLines := append([]string{}, lines[:start]...)
		newLines = append(newLines, "<"+componentName+" />")
		newLines = append(newLines, lines[end+1:]...)
		return strings.Join(newLines, "\n"), true
	}
	return content, false
}

// Run applies AddImport and (if hasCodeGroup) ReplaceCodeGroup to the MDX file at docPageFile.
// In dry-run mode, logs the planned changes but does not write.
func Run(docPageFile, componentName, importPath string, hasCodeGroup, dryRun bool) error {
	content, err := os.ReadFile(docPageFile)
	if err != nil {
		return fmt.Errorf("read %s: %w", docPageFile, err)
	}

	updated := AddImport(string(content), componentName, importPath)

	if hasCodeGroup {
		replaced, ok := ReplaceCodeGroup(updated, componentName)
		if ok {
			updated = replaced
		} else {
			fmt.Printf("[migrate] WARN: CodeGroup not found in %s — import added, CodeGroup left in place\n", docPageFile)
		}
	}

	if dryRun {
		fmt.Printf("[migrate] DRY RUN: would update %s\n  + import %s from '%s'\n", docPageFile, componentName, importPath)
		return nil
	}

	return os.WriteFile(docPageFile, []byte(updated), 0o644)
}
