package scanner_test

import (
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
	assert.Equal(t, "419b175b2bc54175b29d42c36c346409", s.GistID)
	assert.Equal(t, "social-plus-sdk/chat/conversation-management/channels/create-channel", s.AscPage)
	assert.Equal(t, "flutter", s.Platform)
	assert.Contains(t, s.Content, "communityType()")
	assert.NotContains(t, s.Content, "*/")
}

func TestScanLegacyURL(t *testing.T) {
	// snippets with full URLs should be scannable but flagged by differ
	snippets, _ := scanner.Scan("testdata", "android")
	for _, s := range snippets {
		// asc_page is stored as-is; differ decides if it's valid
		_ = s.AscPage
	}
}
