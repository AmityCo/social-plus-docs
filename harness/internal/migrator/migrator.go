package migrator

import (
	"fmt"
	"os"
	"strings"
)

// KebabToPascal converts "community-create" → "CommunityCreate".
func KebabToPascal(key string) string {
	parts := strings.Split(key, "-")
	var b strings.Builder
	for _, p := range parts {
		if p == "" {
			continue
		}
		b.WriteString(strings.ToUpper(p[:1]) + p[1:])
	}
	return b.String()
}

// AddImport inserts an import statement at the top of content if not already present.
func AddImport(content, componentName, importPath string) string {
	importLine := fmt.Sprintf("import %s from '%s';", componentName, importPath)
	if strings.Contains(content, importLine) {
		return content // idempotent
	}
	return importLine + "\n" + content
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
