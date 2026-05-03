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
