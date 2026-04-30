package fixer_test

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"social-plus/harness/internal/fixer"
)

func TestNewSurfaceDriftFixer(t *testing.T) {
	f := fixer.NewSurfaceDriftFixer("claude-sonnet-4-6", "test-api-key")
	assert.NotNil(t, f)
}

func TestSurfaceDriftFixer_BuildPrompt(t *testing.T) {
	f := fixer.NewSurfaceDriftFixer("claude-sonnet-4-6", "test-api-key")
	prompt := f.BuildPrompt("existing MDX content here", "communityType", "snippetCode here")
	assert.Contains(t, prompt, "communityType")
	assert.Contains(t, prompt, "existing MDX content here")
	assert.Contains(t, prompt, "snippetCode here")
}
