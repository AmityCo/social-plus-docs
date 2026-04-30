package fixer

import (
	"context"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestBuildPrompt_ContainsMissingCall(t *testing.T) {
	f := NewSurfaceDriftFixer("claude-sonnet-4-6", "")
	prompt := f.BuildPrompt("# existing", "communityType", "snippet code")
	assert.Contains(t, prompt, "communityType")
	assert.Contains(t, prompt, "# existing")
}

func TestFixSurfaceDrift_ReturnsCopilotCLIError(t *testing.T) {
	f := NewSurfaceDriftFixer("claude-sonnet-4-6", "")
	err := f.FixSurfaceDrift(context.Background(), "page.mdx", "communityType", "snippet")
	require.Error(t, err)
	assert.ErrorIs(t, err, ErrUseCopilotCLI)
}

func TestSanitizeAIResponse_StripsLLMPreamble(t *testing.T) {
	got, err := sanitizeAIResponse("Here is the updated MDX:\n\n# Title\nContent")
	require.NoError(t, err)
	assert.Equal(t, "# Title\nContent", got)
}

func TestSanitizeAIResponse_ReturnsErrorWhenNoMDX(t *testing.T) {
	_, err := sanitizeAIResponse("no mdx here at all")
	require.Error(t, err)
}
