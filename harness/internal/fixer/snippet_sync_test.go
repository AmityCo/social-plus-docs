package fixer_test

import (
	"os"
	"path/filepath"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"social-plus/harness/internal/fixer"
)

func TestSyncSnippetToMDX(t *testing.T) {
	dir := t.TempDir()

	mdxContent := "# Create Channel\n\n<Tabs>\n<Tab title=\"Flutter\">\n```dart\nOLD CODE HERE\n```\n</Tab>\n</Tabs>"
	mdxFile := filepath.Join(dir, "create-channel.mdx")
	require.NoError(t, os.WriteFile(mdxFile, []byte(mdxContent), 0o644))

	newCode := "AmityChatClient.newChannelRepository().communityType().create();"

	err := fixer.SyncSnippetToMDX(mdxFile, "flutter", "dart", newCode)
	require.NoError(t, err)

	updated, err := os.ReadFile(mdxFile)
	require.NoError(t, err)
	assert.Contains(t, string(updated), newCode)
	assert.NotContains(t, string(updated), "OLD CODE HERE")
}

func TestSyncSnippetToMDX_NoMatch(t *testing.T) {
	dir := t.TempDir()
	mdxContent := "# Page with no Flutter tab\n\nSome content."
	mdxFile := filepath.Join(dir, "page.mdx")
	require.NoError(t, os.WriteFile(mdxFile, []byte(mdxContent), 0o644))

	err := fixer.SyncSnippetToMDX(mdxFile, "flutter", "dart", "some code")
	assert.Error(t, err)
}

func TestSyncSnippetToMDX_AlreadySynced(t *testing.T) {
	dir := t.TempDir()
	newCode := "AmityChatClient.newChannelRepository().communityType().create();"
	mdxContent := "# Create Channel\n\n<Tabs>\n<Tab title=\"Flutter\">\n```dart\n" + newCode + "\n```\n</Tab>\n</Tabs>"
	mdxFile := filepath.Join(dir, "create-channel.mdx")
	require.NoError(t, os.WriteFile(mdxFile, []byte(mdxContent), 0o644))

	err := fixer.SyncSnippetToMDX(mdxFile, "flutter", "dart", newCode)
	require.NoError(t, err)
}

func TestSyncSnippetToMDX_EmbeddedBackticks(t *testing.T) {
	dir := t.TempDir()
	mdxContent := "# Create Channel\n\n<Tabs>\n<Tab title=\"Flutter\">\n```dart\nfinal sample = \"```ts\";\nOLD CODE HERE\n```\n</Tab>\n</Tabs>"
	mdxFile := filepath.Join(dir, "create-channel.mdx")
	require.NoError(t, os.WriteFile(mdxFile, []byte(mdxContent), 0o644))

	newCode := "AmityChatClient.newChannelRepository().communityType().create();"
	err := fixer.SyncSnippetToMDX(mdxFile, "flutter", "dart", newCode)
	require.NoError(t, err)

	updated, readErr := os.ReadFile(mdxFile)
	require.NoError(t, readErr)
	assert.Contains(t, string(updated), newCode)
	assert.NotContains(t, string(updated), "OLD CODE HERE")
}

func TestExtractSnippetContent(t *testing.T) {
	dir := t.TempDir()
	content := `/* begin_sample_code
    gist_id: abc
    asc_page: some/path
    description: test
    */
void createCommunityChannel() {
    AmityChatClient.newChannelRepository().create();
}
/* end_sample_code */`
	f := filepath.Join(dir, "snippet.dart")
	require.NoError(t, os.WriteFile(f, []byte(content), 0o644))

	extracted, err := fixer.ExtractSnippetContent(f)
	require.NoError(t, err)
	assert.Contains(t, extracted, "createCommunityChannel")
	assert.NotContains(t, extracted, "begin_sample_code")
	assert.NotContains(t, extracted, "end_sample_code")
	assert.NotContains(t, extracted, "*/")
}

func TestExtractSnippetContent_IgnoresEarlierCommentTerminators(t *testing.T) {
	dir := t.TempDir()
	content := `// comment with */ before snippet
/* begin_sample_code
    gist_id: abc
    asc_page: some/path
    description: test
    */
void createCommunityChannel() {
    AmityChatClient.newChannelRepository().create();
}
/* end_sample_code */`
	f := filepath.Join(dir, "snippet.dart")
	require.NoError(t, os.WriteFile(f, []byte(content), 0o644))

	extracted, err := fixer.ExtractSnippetContent(f)
	require.NoError(t, err)
	assert.Contains(t, extracted, "createCommunityChannel")
	assert.NotContains(t, extracted, "begin_sample_code")
	assert.NotContains(t, extracted, "comment with */ before snippet")
}
