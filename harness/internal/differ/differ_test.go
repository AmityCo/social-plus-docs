package differ_test

import (
	"os"
	"path/filepath"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"social-plus/harness/internal/differ"
	"social-plus/harness/internal/docgen"
	"social-plus/harness/internal/extractor"
	"social-plus/harness/internal/matcher"
	"social-plus/harness/internal/pages"
	"social-plus/harness/internal/report"
	"social-plus/harness/internal/manifest"
	"social-plus/harness/internal/scanner"
)

func TestMissingSnippet(t *testing.T) {
	fns := []extractor.PublicFunction{
		{IDs: []string{"message.delete"}, Platform: "android", File: "AmityMessageRepository.kt"},
	}
	snips := []scanner.Snippet{}
	reg := pages.NewFromPaths(nil)

	findings := differ.Diff(fns, snips, reg, "android")
	assert.Len(t, findings, 1)
	assert.Equal(t, report.TypeMissingSnippet, findings[0].Type)
	assert.Equal(t, "message.delete", findings[0].FunctionID)
}

func TestAscPageInvalid_LegacyURL(t *testing.T) {
	fns := []extractor.PublicFunction{}
	snips := []scanner.Snippet{
		{SpDocsPage: "https://docs.amity.co/social/flutter", Platform: "flutter", File: "snippet.dart"},
	}
	reg := pages.NewFromPaths(nil)

	findings := differ.Diff(fns, snips, reg, "flutter")
	assert.Len(t, findings, 1)
	assert.Equal(t, report.TypeAscPageInvalid, findings[0].Type)
}

func TestDocMissing(t *testing.T) {
	fns := []extractor.PublicFunction{}
	snips := []scanner.Snippet{
		{SpDocsPage: "social-plus-sdk/chat/nonexistent", Platform: "flutter", File: "snippet.dart"},
	}
	reg := pages.NewFromPaths([]string{"social-plus-sdk/chat/overview"})

	findings := differ.Diff(fns, snips, reg, "flutter")
	assert.Len(t, findings, 1)
	assert.Equal(t, report.TypeDocMissing, findings[0].Type)
}

func TestDocSurfaceDrift(t *testing.T) {
	fns := []extractor.PublicFunction{}
	snips := []scanner.Snippet{
		{
			SpDocsPage:  "social-plus-sdk/chat/channels/create",
			Content:  "AmityChatClient.newChannelRepository().communityType().create()",
			Platform: "flutter",
			File:     "snippet.dart",
		},
	}
	reg := pages.NewFromPaths([]string{"social-plus-sdk/chat/channels/create"})
	mdx := map[string]string{
		"social-plus-sdk/chat/channels/create": "Create a channel by calling .create()",
	}

	findings := differ.DiffWithMDX(fns, snips, reg, "flutter", mdx)
	hasDrift := false
	for _, f := range findings {
		if f.Type == report.TypeDocSurfaceDrift {
			hasDrift = true
		}
	}
	assert.True(t, hasDrift)
}

func TestSnippetContentDrift(t *testing.T) {
	fns := []extractor.PublicFunction{}
	snips := []scanner.Snippet{
		{
			SpDocsPage:  "social-plus-sdk/chat/channels/create",
			Content:  "AmityChatClient.newChannelRepository().communityType().create()",
			Platform: "flutter",
			File:     "snippet.dart",
		},
	}
	reg := pages.NewFromPaths([]string{"social-plus-sdk/chat/channels/create"})
	mdx := map[string]string{
		"social-plus-sdk/chat/channels/create": "# Create Channel\n\nSome outdated code here.",
	}

	findings := differ.DiffWithMDX(fns, snips, reg, "flutter", mdx)
	hasDrift := false
	for _, f := range findings {
		if f.Type == report.TypeSnippetContentDrift {
			hasDrift = true
		}
	}
	assert.True(t, hasDrift, "expected SNIPPET_CONTENT_DRIFT when snippet content not in MDX")
}

func TestSnippetContentDrift_NoFalsePositive(t *testing.T) {
	snips := []scanner.Snippet{
		{
			SpDocsPage:  "social-plus-sdk/chat/channels/create",
			Content:  "AmityChatClient.newChannelRepository().create()",
			Platform: "flutter",
			File:     "snippet.dart",
		},
	}
	reg := pages.NewFromPaths([]string{"social-plus-sdk/chat/channels/create"})
	mdx := map[string]string{
		"social-plus-sdk/chat/channels/create": "AmityChatClient.newChannelRepository().create()",
	}

	findings := differ.DiffWithMDX(nil, snips, reg, "flutter", mdx)
	for _, f := range findings {
		assert.NotEqual(t, report.TypeSnippetContentDrift, f.Type,
			"SNIPPET_CONTENT_DRIFT should not fire when first line is present in MDX")
	}
}

func TestNoFindingsWhenClean(t *testing.T) {
	fns := []extractor.PublicFunction{
		{IDs: []string{"channel.create"}, Platform: "flutter", File: "AmityChannel.dart"},
	}
	snips := []scanner.Snippet{
		{
			SpDocsPage: "social-plus-sdk/chat/channels/create",
			Content:    "AmityChatClient.newChannelRepository().create()",
			Platform:   "flutter",
			File:       "snippet.dart",
		},
	}
	reg := pages.NewFromPaths([]string{"social-plus-sdk/chat/channels/create"})

	findings := differ.Diff(fns, snips, reg, "flutter")
	assert.Empty(t, findings)
}

func TestDiffDocPages_StaleImport(t *testing.T) {
	dir := t.TempDir()
	// Doc page has a hardcoded CodeGroup but no gendocs import
	docContent := "<CodeGroup>\n```kotlin Android\nfoo()\n```\n</CodeGroup>\n"
	docFile := filepath.Join(dir, "create-community.mdx")
	require.NoError(t, os.WriteFile(docFile, []byte(docContent), 0o644))

	groups := map[string]docgen.SnippetGroup{
		"community-create": {
			Key:        "community-create",
			SpDocsPage: "social-plus-sdk/social/create-community",
			Snippets:   map[string]scanner.Snippet{"android": {}},
		},
	}
	m := matcher.New(groups)

	findings := differ.DiffDocPages("social-plus-sdk/social/create-community", docFile, m, "snippets")
	require.Len(t, findings, 1)
	assert.Equal(t, report.TypeDocPageStaleImport, findings[0].Type)
	assert.Equal(t, "community-create", findings[0].GendocsKey)
	assert.True(t, findings[0].HasHardcodedCodeGroup)
}

func TestDiffDocPages_AlreadyImported(t *testing.T) {
	dir := t.TempDir()
	// Derive the import path: DeriveMDXPath("social-plus-sdk/social/create-community", "community-create")
	// = "social-plus-sdk/social/community-create.mdx"
	docContent := "import CommunityCreate from '/snippets/social-plus-sdk/social/community-create.mdx';\n<CommunityCreate />\n"
	docFile := filepath.Join(dir, "create-community.mdx")
	require.NoError(t, os.WriteFile(docFile, []byte(docContent), 0o644))

	groups := map[string]docgen.SnippetGroup{
		"community-create": {
			Key:        "community-create",
			SpDocsPage: "social-plus-sdk/social/create-community",
			Snippets:   map[string]scanner.Snippet{"android": {}},
		},
	}
	m := matcher.New(groups)

	findings := differ.DiffDocPages("social-plus-sdk/social/create-community", docFile, m, "snippets")
	assert.Empty(t, findings)
}

func TestDiffManifestCoverage_missingSnippet(t *testing.T) {
	dir := t.TempDir()
	snippetsDir := filepath.Join(dir, "snippets")
	docPage := "social-plus-sdk/getting-started/authentication"
	// Only client-login.mdx exists
	os.MkdirAll(filepath.Join(snippetsDir, "social-plus-sdk", "getting-started"), 0o755)
	os.WriteFile(filepath.Join(snippetsDir, "social-plus-sdk", "getting-started", "client-login.mdx"), []byte("dummy"), 0o644)
	m := &manifest.Manifest{Sections: map[string]manifest.Section{
		"step-1": {Heading: "Step 1", Snippets: []string{"client-setup"}},
		"step-2": {Heading: "Step 2", Snippets: []string{"client-login"}},
	}}
	findings := differ.DiffManifestCoverage(docPage, m, snippetsDir)
	assert.Len(t, findings, 1)
	f := findings[0]
	assert.Equal(t, report.TypeMissingSnippet, f.Type)
	assert.Equal(t, "client-setup", f.GendocsKey)
	assert.Equal(t, docPage, f.DocPage)
	assert.Contains(t, f.Detail, "Step 1")
}

func TestDiffManifestCoverage_allPresent(t *testing.T) {
	dir := t.TempDir()
	snippetsDir := filepath.Join(dir, "snippets")
	docPage := "social-plus-sdk/getting-started/authentication"
	os.MkdirAll(filepath.Join(snippetsDir, "social-plus-sdk", "getting-started"), 0o755)
	os.WriteFile(filepath.Join(snippetsDir, "social-plus-sdk", "getting-started", "client-login.mdx"), []byte("dummy"), 0o644)
	os.WriteFile(filepath.Join(snippetsDir, "social-plus-sdk", "getting-started", "client-setup.mdx"), []byte("dummy"), 0o644)
	m := &manifest.Manifest{Sections: map[string]manifest.Section{
		"step-1": {Heading: "Step 1", Snippets: []string{"client-setup"}},
		"step-2": {Heading: "Step 2", Snippets: []string{"client-login"}},
	}}
	findings := differ.DiffManifestCoverage(docPage, m, snippetsDir)
	assert.Empty(t, findings)
}

func TestDiffManifestCoverage_emptyManifest(t *testing.T) {
	dir := t.TempDir()
	snippetsDir := filepath.Join(dir, "snippets")
	docPage := "social-plus-sdk/getting-started/authentication"
	m := &manifest.Manifest{Sections: map[string]manifest.Section{}}
	findings := differ.DiffManifestCoverage(docPage, m, snippetsDir)
	assert.Empty(t, findings)
}
