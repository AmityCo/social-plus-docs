package matcher

import "social-plus/harness/internal/docgen"

// Matcher maps doc page paths to their corresponding snippet groups.
type Matcher struct {
	index map[string][]docgen.SnippetGroup
}

// New builds a reverse index from SpDocsPage → []SnippetGroup.
func New(groups map[string]docgen.SnippetGroup) *Matcher {
	index := make(map[string][]docgen.SnippetGroup, len(groups))
	for _, g := range groups {
		if g.SpDocsPage != "" {
			index[g.SpDocsPage] = append(index[g.SpDocsPage], g)
		}
	}
	return &Matcher{index: index}
}

// Lookup returns all snippet groups whose SpDocsPage matches docPagePath.
func (m *Matcher) Lookup(docPagePath string) []docgen.SnippetGroup {
	return m.index[docPagePath]
}
