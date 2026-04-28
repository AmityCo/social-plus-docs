package parser

import (
	"path/filepath"
	"regexp"
	"strings"
	"unicode"
)

// Page holds the extracted content from a single MDX file.
type Page struct {
	Title       string
	Description string
	Body        string
}

// jsxLineRe matches lines that are purely Mintlify/JSX component tags.
// All Mintlify components are PascalCase (start with an uppercase letter).
var jsxLineRe = regexp.MustCompile(`^\s*</?[A-Z]`)

// Parse converts raw MDX file bytes into a Page with clean markdown Body.
func Parse(content []byte) Page {
	lines := strings.Split(string(content), "\n")
	var page Page
	i := 0

	// Extract YAML frontmatter if the file starts with "---".
	// NOTE: if the closing "---" is absent the loop consumes all remaining
	// lines as frontmatter and the body will be empty. Malformed frontmatter
	// is not explicitly supported; this behaviour is intentional and tested.
	if len(lines) > 0 && strings.TrimSpace(lines[0]) == "---" {
		i = 1
		var fmLines []string
		for i < len(lines) && strings.TrimSpace(lines[i]) != "---" {
			fmLines = append(fmLines, lines[i])
			i++
		}
		i++ // skip closing ---
		parseFrontmatter(strings.Join(fmLines, "\n"), &page)
	}

	// Process body lines.
	// Track fenced code blocks so that H1 detection and tag stripping are
	// not applied to content inside them.
	var bodyLines []string
	blankRun := 0
	inFence := false
	indentedFencePrefix := "" // leading whitespace of the opening fence line
	h1LineIdx := -1           // index in bodyLines where the first H1 was found

	for ; i < len(lines); i++ {
		rawLine := lines[i]
		trimmed := strings.TrimSpace(rawLine)
		line := rawLine // line is what we'll append; may be normalised

		if strings.HasPrefix(trimmed, "```") {
			if !inFence {
				// Opening fence: record indentation so we can strip it from content.
				inFence = true
				indentedFencePrefix = rawLine[:len(rawLine)-len(strings.TrimLeft(rawLine, " \t"))]
			} else {
				inFence = false
				indentedFencePrefix = ""
			}
			// Normalise fence delimiter to column 0 regardless of original indentation.
			line = trimmed
		} else if inFence && indentedFencePrefix != "" && strings.HasPrefix(rawLine, indentedFencePrefix) {
			// Strip the fence's own indentation prefix from content lines.
			line = rawLine[len(indentedFencePrefix):]
		}

		if !inFence {
			// Remove import statements.
			if strings.HasPrefix(trimmed, "import ") {
				continue
			}
			// Remove JSX component tag lines (opening, closing, self-closing).
			if jsxLineRe.MatchString(trimmed) {
				continue
			}
		}

		if trimmed == "" {
			blankRun++
			// Allow at most 2 consecutive blank lines.
			if blankRun <= 2 {
				bodyLines = append(bodyLines, "")
			}
			continue
		}
		blankRun = 0

		// Capture the first H1 outside a fence when no title was found yet.
		if !inFence && page.Title == "" && h1LineIdx == -1 && strings.HasPrefix(trimmed, "# ") {
			h1LineIdx = len(bodyLines)
			page.Title = strings.TrimSpace(trimmed[2:])
		}

		bodyLines = append(bodyLines, line)
	}

	// Splice out the H1 line by index so it is not duplicated in the body.
	if h1LineIdx >= 0 {
		bodyLines = append(bodyLines[:h1LineIdx], bodyLines[h1LineIdx+1:]...)
	}

	page.Body = strings.TrimSpace(strings.Join(bodyLines, "\n"))
	return page
}

// TitleFromPath derives a human-readable title from a file path when neither
// frontmatter nor a H1 heading is present.
// Example: "social/posts/get-post.mdx" -> "Get Post"
func TitleFromPath(path string) string {
	base := filepath.Base(path)
	base = strings.TrimSuffix(base, filepath.Ext(base))
	words := strings.Split(base, "-")
	for i, w := range words {
		if len(w) > 0 {
			r := []rune(w)
			r[0] = unicode.ToUpper(r[0])
			words[i] = string(r)
		}
	}
	return strings.Join(words, " ")
}

// parseFrontmatter extracts title and description from YAML frontmatter text.
// Handles single-line strings and YAML block scalars (">-", ">", "|", "|-").
func parseFrontmatter(content string, page *Page) {
	lines := strings.Split(content, "\n")
	for i, line := range lines {
		if _, v, ok := splitKV(line, "title"); ok {
			if isBlockScalar(v) {
				page.Title = collectBlock(lines, i+1)
			} else {
				page.Title = v
			}
		} else if _, v, ok := splitKV(line, "description"); ok {
			if isBlockScalar(v) {
				page.Description = collectBlock(lines, i+1)
			} else {
				page.Description = v
			}
		}
	}
}

// isBlockScalar reports whether a YAML value token introduces a block scalar.
func isBlockScalar(v string) bool {
	return v == ">" || v == ">-" || v == "|" || v == "|-"
}

// collectBlock joins the subsequent indented lines (YAML block scalar body)
// into a single space-separated string, stopping at the first unindented or
// empty line.
func collectBlock(lines []string, start int) string {
	var parts []string
	for i := start; i < len(lines); i++ {
		if len(lines[i]) == 0 {
			break
		}
		if lines[i][0] == ' ' || lines[i][0] == '\t' {
			parts = append(parts, strings.TrimSpace(lines[i]))
		} else {
			break
		}
	}
	return strings.Join(parts, " ")
}

// splitKV splits "key: value" and returns (key, value, true) when the line
// starts with the given key followed by ":".
func splitKV(line, key string) (string, string, bool) {
	prefix := key + ":"
	if !strings.HasPrefix(line, prefix) {
		return "", "", false
	}
	val := strings.TrimSpace(strings.TrimPrefix(line, prefix))
	val = strings.Trim(val, `"'`)
	return key, val, true
}
