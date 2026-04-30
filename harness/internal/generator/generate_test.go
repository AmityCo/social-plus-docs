package generator

import (
	"context"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestBuildPrompt_ContainsPlatformAndFunctionID(t *testing.T) {
	g := New("claude-sonnet-4-6", "")
	prompt := g.BuildPrompt("android", "channel.get", "func sig", "File.kt")
	assert.Contains(t, prompt, "android")
	assert.Contains(t, prompt, "channel.get")
	assert.Contains(t, prompt, "begin_sample_code")
}

func TestGenerate_ReturnsCopilotCLIError(t *testing.T) {
	g := New("claude-sonnet-4-6", "")
	_, err := g.Generate(context.Background(), "android", "channel.get", "", "")
	require.Error(t, err)
	assert.ErrorIs(t, err, ErrUseCopilotCLI)
}
