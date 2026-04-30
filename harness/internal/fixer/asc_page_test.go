package fixer_test

import (
	"os"
	"path/filepath"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"social-plus/harness/internal/fixer"
	"social-plus/harness/internal/pages"
)

func TestFixAscPage_LegacyURL(t *testing.T) {
	dir := t.TempDir()
	content := `/* begin_sample_code
    gist_id: abc123
    filename: test.dart
    asc_page: https://docs.amity.co/social/flutter
    description: test
    */
void doThing() {}
/* end_sample_code */`
	f := filepath.Join(dir, "test.dart")
	require.NoError(t, os.WriteFile(f, []byte(content), 0o644))

	reg := pages.NewFromPaths([]string{
		"social-plus-sdk/social/flutter",
		"social-plus-sdk/chat/channels/create-channel",
	})

	newPath, err := fixer.FixAscPage(f, "https://docs.amity.co/social/flutter", reg)
	require.NoError(t, err)
	assert.Equal(t, "social-plus-sdk/social/flutter", newPath)

	updated, err := os.ReadFile(f)
	require.NoError(t, err)
	assert.Contains(t, string(updated), "asc_page: social-plus-sdk/social/flutter")
	assert.NotContains(t, string(updated), "https://docs.amity.co")
}

func TestFixAscPage_NoMatch(t *testing.T) {
	dir := t.TempDir()
	content := `/* begin_sample_code
    asc_page: https://docs.amity.co/completely/different/path
    */
void doThing() {}
/* end_sample_code */`
	f := filepath.Join(dir, "test.dart")
	require.NoError(t, os.WriteFile(f, []byte(content), 0o644))

	reg := pages.NewFromPaths([]string{"social-plus-sdk/chat/overview"})

	_, err := fixer.FixAscPage(f, "https://docs.amity.co/completely/different/path", reg)
	assert.Error(t, err)
}

func TestFixAscPage_DoubleSpace(t *testing.T) {
	// Fix 5: whitespace-tolerant replacement means double-space is now handled.
	dir := t.TempDir()
	content := `/* begin_sample_code
    asc_page:  https://docs.amity.co/social/flutter
    */
void doThing() {}
/* end_sample_code */`
	f := filepath.Join(dir, "test.dart")
	require.NoError(t, os.WriteFile(f, []byte(content), 0o644))

	reg := pages.NewFromPaths([]string{"social-plus-sdk/social/flutter"})

	newPath, err := fixer.FixAscPage(f, "https://docs.amity.co/social/flutter", reg)
	require.NoError(t, err)
	assert.Equal(t, "social-plus-sdk/social/flutter", newPath)

	updated, readErr := os.ReadFile(f)
	require.NoError(t, readErr)
	assert.Contains(t, string(updated), "asc_page: social-plus-sdk/social/flutter")
	assert.NotContains(t, string(updated), "https://docs.amity.co")
}

func TestFixAscPage_PartialOverlapMatches(t *testing.T) {
	// With lenient scoring (ceil(n/2)), a URL like chat/overview should match
	// any docs path that contains "chat" — even if "overview" isn't in the path.
	dir := t.TempDir()
	content := `/* begin_sample_code
    asc_page: https://docs.amity.co/chat/overview
    */
void doThing() {}
/* end_sample_code */`
	f := filepath.Join(dir, "test.dart")
	require.NoError(t, os.WriteFile(f, []byte(content), 0o644))

	reg := pages.NewFromPaths([]string{"social-plus-sdk/chat/channels/create-channel"})

	newPath, err := fixer.FixAscPage(f, "https://docs.amity.co/chat/overview", reg)
	require.NoError(t, err)
	assert.Equal(t, "social-plus-sdk/chat/channels/create-channel", newPath)
}

func TestFixAscPage_ZeroOverlapNoMatch(t *testing.T) {
	// A URL with segments that don't appear in any registry path should still fail.
	dir := t.TempDir()
	content := `/* begin_sample_code
    asc_page: https://docs.amity.co/completely/unknown/page
    */
void doThing() {}
/* end_sample_code */`
	f := filepath.Join(dir, "test.dart")
	require.NoError(t, os.WriteFile(f, []byte(content), 0o644))

	reg := pages.NewFromPaths([]string{"social-plus-sdk/chat/channels/create-channel"})

	_, err := fixer.FixAscPage(f, "https://docs.amity.co/completely/unknown/page", reg)
	assert.Error(t, err)
}
