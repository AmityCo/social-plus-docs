package migrator_test

import (
	"os"
	"path/filepath"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"social-plus/harness/internal/migrator"
)

func TestAddImport_AddsAtTop(t *testing.T) {
	content := "# Create Community\n\nSome prose.\n\n<CodeGroup>\n</CodeGroup>\n"
	result := migrator.AddImport(content, "CommunityCreate", "/snippets/social-plus-sdk/social/community-create.mdx")
	assert.Contains(t, result, "import CommunityCreate from '/snippets/social-plus-sdk/social/community-create.mdx';")
	assert.True(t, strings.HasPrefix(result, "import"), "import should be at the top")
}

func TestAddImport_Idempotent(t *testing.T) {
	content := "import CommunityCreate from '/snippets/social-plus-sdk/social/community-create.mdx';\n# Page\n"
	result := migrator.AddImport(content, "CommunityCreate", "/snippets/social-plus-sdk/social/community-create.mdx")
	count := strings.Count(result, "import CommunityCreate")
	assert.Equal(t, 1, count)
}

func TestReplaceCodeGroup_ReplacesBlock(t *testing.T) {
	content := "import CommunityCreate from '/snippets/social-plus-sdk/social/community-create.mdx';\n\n<CodeGroup>\n\n```kotlin Android\nfoo()\n```\n\n</CodeGroup>\n"
	result, ok := migrator.ReplaceCodeGroup(content, "CommunityCreate")
	assert.True(t, ok)
	assert.NotContains(t, result, "<CodeGroup>")
	assert.Contains(t, result, "<CommunityCreate />")
}

func TestReplaceCodeGroup_NoCodeGroup(t *testing.T) {
	content := "# Page\nNo code group here.\n"
	result, ok := migrator.ReplaceCodeGroup(content, "CommunityCreate")
	assert.False(t, ok)
	assert.Equal(t, content, result)
}

func TestRunMigrate_WritesFile(t *testing.T) {
	dir := t.TempDir()
	docContent := "<CodeGroup>\n```kotlin Android\nfoo()\n```\n</CodeGroup>\n"
	docFile := filepath.Join(dir, "create-community.mdx")
	require.NoError(t, os.WriteFile(docFile, []byte(docContent), 0o644))

	err := migrator.Run(docFile, "CommunityCreate", "/snippets/social-plus-sdk/social/community-create.mdx", true /*hasCodeGroup*/, false /*dryRun*/)
	require.NoError(t, err)

	updated, err := os.ReadFile(docFile)
	require.NoError(t, err)
	assert.Contains(t, string(updated), "import CommunityCreate from")
	assert.Contains(t, string(updated), "<CommunityCreate />")
	assert.NotContains(t, string(updated), "<CodeGroup>")
}

func TestRunMigrate_DryRunDoesNotWrite(t *testing.T) {
	dir := t.TempDir()
	original := "<CodeGroup>\n```kotlin\nfoo()\n```\n</CodeGroup>\n"
	docFile := filepath.Join(dir, "page.mdx")
	require.NoError(t, os.WriteFile(docFile, []byte(original), 0o644))

	err := migrator.Run(docFile, "MySnippet", "/snippets/x/y/my-snippet.mdx", true, true /*dryRun*/)
	require.NoError(t, err)

	unchanged, _ := os.ReadFile(docFile)
	assert.Equal(t, original, string(unchanged))
}
