package scanner_test

import (
	"os"
	"path/filepath"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"social-plus/harness/internal/scanner"
)

func TestScan(t *testing.T) {
	snippets, err := scanner.Scan("testdata", "flutter")
	require.NoError(t, err)
	require.Len(t, snippets, 1)

	s := snippets[0]
	assert.Equal(t, "social-plus-sdk/chat/conversation-management/channels/create-channel", s.SpDocsPage)
	assert.Equal(t, "flutter", s.Platform)
	assert.Contains(t, s.Content, "communityType()")
	assert.NotContains(t, s.Content, "*/")
}

func TestScanLegacyURL(t *testing.T) {
	snippets, err := scanner.Scan("testdata", "android")
	require.NoError(t, err)
	require.Len(t, snippets, 1)
	// sp_docs_page stored verbatim — differ will flag it as ASC_PAGE_INVALID
	assert.Equal(t, "https://docs.amity.co/social/android", snippets[0].SpDocsPage)
}

func TestScanBackwardCompatAscPage(t *testing.T) {
	// Snippets using legacy asc_page: key are still parsed into SpDocsPage.
	dir := t.TempDir()
	content := `/* begin_sample_code
    filename: test.dart
    asc_page: social-plus-sdk/chat/overview
    description: backward compat test
    */
void test() {}
/* end_sample_code */`
	require.NoError(t, os.WriteFile(filepath.Join(dir, "test.dart"), []byte(content), 0o644))
	snips, err := scanner.Scan(dir, "flutter")
	require.NoError(t, err)
	require.Len(t, snips, 1)
	assert.Equal(t, "social-plus-sdk/chat/overview", snips[0].SpDocsPage)
}
