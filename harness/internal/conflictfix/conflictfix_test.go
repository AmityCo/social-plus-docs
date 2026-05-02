package conflictfix_test

import (
	"os"
	"path/filepath"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"social-plus/harness/internal/conflictfix"
)

// makeSnippet writes a minimal snippet file with begin_sample_code markers.
func makeSnippet(t *testing.T, dir, filename, platform, spDocsPage string) string {
	t.Helper()
	ext := map[string]string{
		"android":    "kt",
		"ios":        "swift",
		"flutter":    "dart",
		"typescript": "ts",
	}[platform]
	path := filepath.Join(dir, filename+"."+ext)
	content := "/* begin_sample_code\n   filename: " + filename + "\n   sp_docs_page: " + spDocsPage + "\n   description: test\n   */\nfunc foo() {}\n/* end_sample_code */"
	require.NoError(t, os.WriteFile(path, []byte(content), 0o644))
	return path
}

func TestFix_RewritesNonAndroid(t *testing.T) {
	dir := t.TempDir()
	androidDir := filepath.Join(dir, "android")
	flutterDir := filepath.Join(dir, "flutter")
	require.NoError(t, os.MkdirAll(androidDir, 0o755))
	require.NoError(t, os.MkdirAll(flutterDir, 0o755))

	// android has the canonical page
	makeSnippet(t, androidDir, "AmityBanChannelMembers", "android", "social-plus-sdk/chat/ban-management")
	// flutter has the wrong page
	flutterFile := makeSnippet(t, flutterDir, "AmityBanChannelMembers", "flutter", "social-plus-sdk/chat/archive-channels")

	dirs := map[string]string{"android": androidDir, "flutter": flutterDir}
	resolutions, err := conflictfix.Fix(dirs)
	require.NoError(t, err)
	require.Len(t, resolutions, 1)

	r := resolutions[0]
	assert.Equal(t, flutterFile, r.SnippetFile)
	assert.Equal(t, "flutter", r.Platform)
	assert.Equal(t, "social-plus-sdk/chat/archive-channels", r.OldPage)
	assert.Equal(t, "social-plus-sdk/chat/ban-management", r.CanonicalPage)

	// Verify file was rewritten
	data, err := os.ReadFile(flutterFile)
	require.NoError(t, err)
	assert.Contains(t, string(data), "sp_docs_page: social-plus-sdk/chat/ban-management")
	assert.NotContains(t, string(data), "archive-channels")
}

func TestFix_SkipsWhenAlreadyAgree(t *testing.T) {
	dir := t.TempDir()
	androidDir := filepath.Join(dir, "android")
	iosDir := filepath.Join(dir, "ios")
	require.NoError(t, os.MkdirAll(androidDir, 0o755))
	require.NoError(t, os.MkdirAll(iosDir, 0o755))

	// Both already agree — no rewrite needed
	makeSnippet(t, androidDir, "AmityCreatePost", "android", "social-plus-sdk/social/post-create")
	makeSnippet(t, iosDir, "AmityCreatePost", "ios", "social-plus-sdk/social/post-create")

	dirs := map[string]string{"android": androidDir, "ios": iosDir}
	resolutions, err := conflictfix.Fix(dirs)
	require.NoError(t, err)
	assert.Empty(t, resolutions)
}

func TestFix_NoAndroidEntry_SkipsKey(t *testing.T) {
	dir := t.TempDir()
	flutterDir := filepath.Join(dir, "flutter")
	iosDir := filepath.Join(dir, "ios")
	require.NoError(t, os.MkdirAll(flutterDir, 0o755))
	require.NoError(t, os.MkdirAll(iosDir, 0o755))

	// Flutter and iOS conflict but no android canonical — skip
	makeSnippet(t, flutterDir, "AmityQueryCategories", "flutter", "social-plus-sdk/social/README")
	makeSnippet(t, iosDir, "AmityQueryCategories", "ios", "social-plus-sdk/social/query-communities")

	dirs := map[string]string{"flutter": flutterDir, "ios": iosDir}
	resolutions, err := conflictfix.Fix(dirs)
	require.NoError(t, err)
	assert.Empty(t, resolutions, "no android entry means no canonical — should skip")
}

func TestFix_MultipleConflictsInSameRun(t *testing.T) {
	dir := t.TempDir()
	androidDir := filepath.Join(dir, "android")
	flutterDir := filepath.Join(dir, "flutter")
	require.NoError(t, os.MkdirAll(androidDir, 0o755))
	require.NoError(t, os.MkdirAll(flutterDir, 0o755))

	makeSnippet(t, androidDir, "AmityKeyA", "android", "social-plus-sdk/chat/page-a")
	makeSnippet(t, androidDir, "AmityKeyB", "android", "social-plus-sdk/chat/page-b")
	makeSnippet(t, flutterDir, "AmityKeyA", "flutter", "social-plus-sdk/social/README")
	makeSnippet(t, flutterDir, "AmityKeyB", "flutter", "social-plus-sdk/social/README")

	dirs := map[string]string{"android": androidDir, "flutter": flutterDir}
	resolutions, err := conflictfix.Fix(dirs)
	require.NoError(t, err)
	assert.Len(t, resolutions, 2)
}

func TestFix_PreservesNonSpDocsPageLines(t *testing.T) {
	dir := t.TempDir()
	androidDir := filepath.Join(dir, "android")
	flutterDir := filepath.Join(dir, "flutter")
	require.NoError(t, os.MkdirAll(androidDir, 0o755))
	require.NoError(t, os.MkdirAll(flutterDir, 0o755))

	makeSnippet(t, androidDir, "AmityFoo", "android", "social-plus-sdk/chat/foo")
	flutterPath := makeSnippet(t, flutterDir, "AmityFoo", "flutter", "social-plus-sdk/social/README")

	dirs := map[string]string{"android": androidDir, "flutter": flutterDir}
	_, err := conflictfix.Fix(dirs)
	require.NoError(t, err)

	data, err := os.ReadFile(flutterPath)
	require.NoError(t, err)
	content := string(data)
	// The description line and code must survive
	assert.True(t, strings.Contains(content, "description: test"), "description line must survive")
	assert.True(t, strings.Contains(content, "func foo()"), "code body must survive")
	assert.True(t, strings.Contains(content, "begin_sample_code"), "begin marker must survive")
	assert.True(t, strings.Contains(content, "end_sample_code"), "end marker must survive")
}
