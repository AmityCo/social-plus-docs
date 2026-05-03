// internal/curator/curator.go
package curator

import (
	"encoding/json"
	"os"
	"regexp"
	"sort"
	"strings"
	"time"
)

// CurateAction represents what to do with a placed snippet.
type CurateAction string

const (
	ActionKeep   CurateAction = "KEEP"
	ActionRemove CurateAction = "REMOVE"
	ActionMove   CurateAction = "MOVE"
	ActionFlag   CurateAction = "FLAG"
)

// Confidence represents decision confidence.
type Confidence string

const (
	ConfidenceHigh   Confidence = "high"
	ConfidenceMedium Confidence = "medium"
	ConfidenceLow    Confidence = "low"
)

// Decision is the verdict on a single placed snippet.
type Decision struct {
	Name       string       `json:"name"`
	Action     CurateAction `json:"action"`
	Section    string       `json:"section,omitempty"`     // target ## heading if KEEP
	TargetPage string       `json:"target_page,omitempty"` // if MOVE
	Reason     string       `json:"reason"`
	Confidence Confidence   `json:"confidence"`
}

// PageDecisions groups decisions for one page.
type PageDecisions struct {
	PagePath  string     `json:"page_path"`
	Decisions []Decision `json:"decisions"`
}

// DecisionsFile is the top-level structure of curate-decisions.json.
type DecisionsFile struct {
	GeneratedAt string          `json:"generated_at"`
	Pages       []PageDecisions `json:"pages"`
}

// ReviewFile is the top-level structure of curate-review.json (flagged/low-confidence items).
type ReviewFile struct {
	GeneratedAt string          `json:"generated_at"`
	Pages       []PageDecisions `json:"pages"`
}

// PlacedSnippet is a snippet import whose component tag appears in the page body.
type PlacedSnippet struct {
	Name       string
	ImportPath string
	Content    string // snippet file content (for LLM context)
}

// ParsedPage holds extracted content from one MDX file.
type ParsedPage struct {
	File     string
	PagePath string
	Prose    string          // body text with imports and component tags stripped
	Sections []string        // ## headings in order
	Placed   []PlacedSnippet // imports whose <Name /> tag exists in body
}

var (
	importRe    = regexp.MustCompile(`(?m)^import\s+(\w+)\s+from\s+['"]([^'"]+\.mdx)['"]\s*;?\s*$`)
	componentRe = regexp.MustCompile(`<(\w+)\s*/>|<(\w+)\s*>`)
	headingRe   = regexp.MustCompile(`^##\s+.+`)
)

// ParsePage parses mdx content and returns a ParsedPage.
// snippetReader(importPath) should return the snippet file content; "" is fine.
func ParsePage(file, pagePath, content string, snippetReader func(importPath string) string) ParsedPage {
	imports := map[string]string{} // name -> importPath
	for _, m := range importRe.FindAllStringSubmatch(content, -1) {
		imports[m[1]] = m[2]
	}

	// Strip import lines for body analysis.
	body := importRe.ReplaceAllString(content, "")

	// Find placed component names (tags that appear in body).
	placed := []PlacedSnippet{}
	for name, importPath := range imports {
		tag := "<" + name
		if strings.Contains(body, tag) {
			snippetContent := ""
			if snippetReader != nil {
				snippetContent = snippetReader(importPath)
			}
			placed = append(placed, PlacedSnippet{
				Name:       name,
				ImportPath: importPath,
				Content:    snippetContent,
			})
		}
	}

	sort.Slice(placed, func(i, j int) bool { return placed[i].Name < placed[j].Name })

	// Extract ## sections.
	var sections []string
	for _, line := range strings.Split(content, "\n") {
		trimmed := strings.TrimRight(line, " \t")
		if headingRe.MatchString(trimmed) {
			sections = append(sections, trimmed)
		}
	}

	// Build prose: strip import lines and component tags.
	proseLines := []string{}
	for _, line := range strings.Split(body, "\n") {
		trimmed := strings.TrimSpace(line)
		if componentRe.MatchString(trimmed) {
			continue
		}
		proseLines = append(proseLines, line)
	}
	prose := strings.TrimSpace(strings.Join(proseLines, "\n"))

	return ParsedPage{
		File:     file,
		PagePath: pagePath,
		Prose:    prose,
		Sections: sections,
		Placed:   placed,
	}
}

// ReadDecisions reads curate-decisions.json from path.
func ReadDecisions(path string) (DecisionsFile, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return DecisionsFile{}, err
	}
	var df DecisionsFile
	if err := json.Unmarshal(data, &df); err != nil {
		return DecisionsFile{}, err
	}
	return df, nil
}

// Apply applies decisions to MDX content according to confidence-gating rules.
// Returns: modified content, auto-applied decisions, flagged decisions (need human review).
// Rules:
//
//	KEEP (any confidence)  → auto-apply (re-section tag if Section is specified and tag not already there)
//	REMOVE high            → auto-apply (remove import + tag)
//	REMOVE medium/low      → flag
//	MOVE high              → auto-apply (remove import + tag from this page)
//	MOVE medium/low        → flag
//	FLAG any               → always flag
func Apply(content string, decisions []Decision) (modified string, applied []Decision, flagged []Decision) {
	applied = []Decision{}
	flagged = []Decision{}
	modified = content

	for _, d := range decisions {
		switch d.Action {
		case ActionFlag:
			flagged = append(flagged, d)

		case ActionRemove:
			if d.Confidence == ConfidenceHigh {
				modified = removeSnippet(modified, d.Name)
				applied = append(applied, d)
			} else {
				flagged = append(flagged, d)
			}

		case ActionMove:
			if d.Confidence == ConfidenceHigh {
				modified = removeSnippet(modified, d.Name)
				applied = append(applied, d)
			} else {
				flagged = append(flagged, d)
			}

		case ActionKeep:
			if d.Section != "" {
				modified = resectionSnippet(modified, d.Name, d.Section)
			}
			applied = append(applied, d)
		}
	}
	return modified, applied, flagged
}

// removeSnippet removes the import line and all component tags for name from content.
func removeSnippet(content, name string) string {
	lines := strings.Split(content, "\n")
	out := make([]string, 0, len(lines))
	importPrefix := "import " + name + " "
	tagPatterns := []string{"<" + name + " />", "<" + name + "/>", "<" + name + ">"}

	for _, line := range lines {
		trimmed := strings.TrimSpace(line)
		if strings.HasPrefix(trimmed, importPrefix) {
			continue
		}
		isTag := false
		for _, pat := range tagPatterns {
			if trimmed == pat {
				isTag = true
				break
			}
		}
		if isTag {
			continue
		}
		out = append(out, line)
	}
	return collapseBlankLines(strings.Join(out, "\n"))
}

// resectionSnippet moves the <name /> tag to immediately after the targetSection heading.
// If the tag is already in the correct section, content is returned unchanged.
func resectionSnippet(content, name, targetSection string) string {
	tag := "<" + name + " />"
	lines := strings.Split(content, "\n")

	// Find target section index.
	targetIdx := -1
	for i, line := range lines {
		if strings.TrimRight(line, " \t") == targetSection {
			targetIdx = i
			break
		}
	}
	if targetIdx == -1 {
		return content // section not found, leave unchanged
	}

	// Find where the tag currently is.
	tagIdx := -1
	for i, line := range lines {
		if strings.TrimSpace(line) == tag {
			tagIdx = i
			break
		}
	}
	if tagIdx == -1 {
		return content // tag not found, leave unchanged
	}

	// Check if tag is already right after the target section (within 5 non-blank lines).
	if isTagNearSection(lines, tagIdx, targetIdx) {
		return content
	}

	// Remove tag from current position.
	without := append(lines[:tagIdx:tagIdx], lines[tagIdx+1:]...)

	// Re-find target section after removal (index may have shifted).
	newTargetIdx := -1
	for i, line := range without {
		if strings.TrimRight(line, " \t") == targetSection {
			newTargetIdx = i
			break
		}
	}
	if newTargetIdx == -1 {
		return content
	}

	// Insert tag after the section heading (with a blank line before).
	insertAt := newTargetIdx + 1
	result := make([]string, 0, len(without)+2)
	result = append(result, without[:insertAt]...)
	result = append(result, "")
	result = append(result, tag)
	result = append(result, without[insertAt:]...)

	return collapseBlankLines(strings.Join(result, "\n"))
}

// isTagNearSection returns true if tagIdx is within 5 non-blank lines after sectionIdx.
func isTagNearSection(lines []string, tagIdx, sectionIdx int) bool {
	if tagIdx <= sectionIdx {
		return false
	}
	nonBlank := 0
	for i := sectionIdx + 1; i < tagIdx && i < len(lines); i++ {
		if strings.TrimSpace(lines[i]) != "" {
			nonBlank++
		}
		if nonBlank > 5 {
			return false
		}
	}
	return nonBlank <= 5
}

// collapseBlankLines reduces runs of 3+ blank lines to 2.
func collapseBlankLines(s string) string {
	for strings.Contains(s, "\n\n\n\n") {
		s = strings.ReplaceAll(s, "\n\n\n\n", "\n\n\n")
	}
	return s
}

// WriteReview writes flagged decisions to path as curate-review.json.
func WriteReview(path string, pages []PageDecisions) error {
	rf := ReviewFile{
		GeneratedAt: time.Now().UTC().Format(time.RFC3339),
		Pages:       pages,
	}
	data, err := json.MarshalIndent(rf, "", "  ")
	if err != nil {
		return err
	}
	return os.WriteFile(path, data, 0o644)
}
