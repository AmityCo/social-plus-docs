package matcher_test

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"social-plus/harness/internal/docgen"
	"social-plus/harness/internal/matcher"
	"social-plus/harness/internal/scanner"
)

func makeGroup(key, spDocsPage string) docgen.SnippetGroup {
	return docgen.SnippetGroup{
		Key:        key,
		SpDocsPage: spDocsPage,
		Snippets:   map[string]scanner.Snippet{"android": {}},
	}
}

func TestLookup_SingleMatch(t *testing.T) {
	groups := map[string]docgen.SnippetGroup{
		"community-create": makeGroup("community-create", "social-plus-sdk/social/communities-spaces/community-lifecycle/create-community"),
	}
	m := matcher.New(groups)
	results := m.Lookup("social-plus-sdk/social/communities-spaces/community-lifecycle/create-community")
	assert.Len(t, results, 1)
	assert.Equal(t, "community-create", results[0].Key)
}

func TestLookup_MultipleGroupsSamePage(t *testing.T) {
	groups := map[string]docgen.SnippetGroup{
		"community-create": makeGroup("community-create", "social-plus-sdk/social/communities-spaces/community-lifecycle/create-community"),
		"community-delete": makeGroup("community-delete", "social-plus-sdk/social/communities-spaces/community-lifecycle/create-community"),
	}
	m := matcher.New(groups)
	results := m.Lookup("social-plus-sdk/social/communities-spaces/community-lifecycle/create-community")
	assert.Len(t, results, 2)
}

func TestLookup_NoMatch(t *testing.T) {
	groups := map[string]docgen.SnippetGroup{
		"community-create": makeGroup("community-create", "social-plus-sdk/social/some-other-page"),
	}
	m := matcher.New(groups)
	results := m.Lookup("social-plus-sdk/social/communities-spaces/community-lifecycle/create-community")
	assert.Empty(t, results)
}

func TestLookup_EmptyGroups(t *testing.T) {
	m := matcher.New(map[string]docgen.SnippetGroup{})
	results := m.Lookup("social-plus-sdk/chat/overview")
	assert.Empty(t, results)
}
