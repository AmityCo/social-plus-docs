package placer_test

import (
	"os"
	"path/filepath"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"social-plus/harness/internal/placer"
)

func setupDocs(t *testing.T) (docsBase, mdxFile string) {
	t.Helper()
	dir := t.TempDir()
	docsBase = dir

	snippetDir := filepath.Join(dir, "snippets", "social-plus-sdk", "chat")
	require.NoError(t, os.MkdirAll(snippetDir, 0o755))
	snippetContent := "<CodeGroup>\n```kotlin Android\nfun messageFlag() {}\n```\n</CodeGroup>"
	require.NoError(t, os.WriteFile(filepath.Join(snippetDir, "message-flag.mdx"), []byte(snippetContent), 0o644))

	mdxContent := "import MessageFlag from '/snippets/social-plus-sdk/chat/message-flag.mdx';\n\n---\ntitle: Test\n---\n\n## Flag Messages\n\nSome prose.\n"
	mdxFile = filepath.Join(dir, "flag-page.mdx")
	require.NoError(t, os.WriteFile(mdxFile, []byte(mdxContent), 0o644))
	return
}

func TestFindUnplaced_DetectsOrphanedImport(t *testing.T) {
	docsBase, mdxFile := setupDocs(t)
	task, err := placer.FindUnplaced(mdxFile, "social-plus-sdk/chat/flag-messages", docsBase)
	require.NoError(t, err)
	require.Len(t, task.Components, 1)
	assert.Equal(t, "MessageFlag", task.Components[0].Name)
	assert.Equal(t, "message-flag", task.Components[0].Key)
	assert.Equal(t, "/snippets/social-plus-sdk/chat/message-flag.mdx", task.Components[0].ImportPath)
	assert.Contains(t, task.Components[0].SnippetPreview, "CodeGroup")
}

func TestFindUnplaced_SkipsAlreadyPlaced(t *testing.T) {
	docsBase, _ := setupDocs(t)
	content := "import MessageFlag from '/snippets/social-plus-sdk/chat/message-flag.mdx';\n\n---\ntitle: Test\n---\n\n<MessageFlag />\n"
	mdxFile := filepath.Join(docsBase, "already-placed.mdx")
	require.NoError(t, os.WriteFile(mdxFile, []byte(content), 0o644))

	task, err := placer.FindUnplaced(mdxFile, "social-plus-sdk/chat/already-placed", docsBase)
	require.NoError(t, err)
	assert.Empty(t, task.Components)
}

func TestFindUnplaced_MultipleComponents(t *testing.T) {
	dir := t.TempDir()
	snippetDir := filepath.Join(dir, "snippets", "social-plus-sdk", "chat")
	require.NoError(t, os.MkdirAll(snippetDir, 0o755))
	require.NoError(t, os.WriteFile(filepath.Join(snippetDir, "message-flag.mdx"), []byte("preview1"), 0o644))
	require.NoError(t, os.WriteFile(filepath.Join(snippetDir, "message-unflag.mdx"), []byte("preview2"), 0o644))

	content := "import MessageFlag from '/snippets/social-plus-sdk/chat/message-flag.mdx';\nimport MessageUnflag from '/snippets/social-plus-sdk/chat/message-unflag.mdx';\n\n---\ntitle: Test\n---\n\n## Flag\n"
	mdxFile := filepath.Join(dir, "flag.mdx")
	require.NoError(t, os.WriteFile(mdxFile, []byte(content), 0o644))

	task, err := placer.FindUnplaced(mdxFile, "social-plus-sdk/chat/flag", dir)
	require.NoError(t, err)
	assert.Len(t, task.Components, 2)
	names := []string{task.Components[0].Name, task.Components[1].Name}
	assert.Contains(t, names, "MessageFlag")
	assert.Contains(t, names, "MessageUnflag")
}

func TestFindUnplaced_MissingSnippetFileGivesEmptyPreview(t *testing.T) {
	dir := t.TempDir()
	content := "import MessageFlag from '/snippets/social-plus-sdk/chat/message-flag.mdx';\n\n---\ntitle: Test\n---\n\n## Flag\n"
	mdxFile := filepath.Join(dir, "flag.mdx")
	require.NoError(t, os.WriteFile(mdxFile, []byte(content), 0o644))

	task, err := placer.FindUnplaced(mdxFile, "social-plus-sdk/chat/flag", dir)
	require.NoError(t, err)
	require.Len(t, task.Components, 1)
	assert.Equal(t, "", task.Components[0].SnippetPreview)
}

func TestFindUnplaced_SnippetPreviewTruncatedAt40Lines(t *testing.T) {
	dir := t.TempDir()
	snippetDir := filepath.Join(dir, "snippets", "s", "c")
	require.NoError(t, os.MkdirAll(snippetDir, 0o755))
	var lines []string
	for i := 0; i < 60; i++ {
		lines = append(lines, "line")
	}
	require.NoError(t, os.WriteFile(filepath.Join(snippetDir, "big.mdx"), []byte(strings.Join(lines, "\n")), 0o644))

	content := "import Big from '/snippets/s/c/big.mdx';\n\n## Section\n"
	mdxFile := filepath.Join(dir, "page.mdx")
	require.NoError(t, os.WriteFile(mdxFile, []byte(content), 0o644))

	task, err := placer.FindUnplaced(mdxFile, "s/c/page", dir)
	require.NoError(t, err)
	require.Len(t, task.Components, 1)
	got := strings.Count(task.Components[0].SnippetPreview, "\n")
	assert.Equal(t, 39, got) // 40 lines = 39 newlines
}
