package pages_test

import (
    "testing"

    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
    "social-plus/harness/internal/pages"
)

func TestLoad(t *testing.T) {
    registry, err := pages.Load("testdata/docs.json")
    require.NoError(t, err)

    assert.True(t, registry.Contains("social-plus-sdk/chat/overview"))
    assert.True(t, registry.Contains("social-plus-sdk/chat/conversation-management/channels/create-channel"))
    assert.False(t, registry.Contains("social-plus-sdk/chat/nonexistent"))
}

func TestContainsLegacyURL(t *testing.T) {
    registry, _ := pages.Load("testdata/docs.json")
    // Full URLs are not valid paths
    assert.False(t, registry.Contains("https://docs.amity.co/social/flutter"))
}
