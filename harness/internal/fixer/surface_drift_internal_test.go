package fixer

import (
	"context"
	"os"
	"path/filepath"
	"testing"

	"github.com/anthropics/anthropic-sdk-go"
	"github.com/anthropics/anthropic-sdk-go/option"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

type stubSurfaceDriftClient struct {
	response *anthropic.Message
	err      error
}

func (s stubSurfaceDriftClient) New(_ context.Context, _ anthropic.MessageNewParams, _ ...option.RequestOption) (*anthropic.Message, error) {
	if s.err != nil {
		return nil, s.err
	}
	return s.response, nil
}

func TestFixSurfaceDrift_WritesUpdatedMDX(t *testing.T) {
	dir := t.TempDir()
	mdxFile := filepath.Join(dir, "page.mdx")
	require.NoError(t, os.WriteFile(mdxFile, []byte("old"), 0o644))

	f := &SurfaceDriftFixer{
		model: "claude-sonnet-4-6",
		client: stubSurfaceDriftClient{
			response: &anthropic.Message{
				Content: []anthropic.ContentBlockUnion{
					{Type: "text", Text: "# new mdx"},
				},
				StopReason: anthropic.StopReasonEndTurn,
			},
		},
	}

	err := f.FixSurfaceDrift(context.Background(), mdxFile, "communityType", "snippet")
	require.NoError(t, err)

	content, err := os.ReadFile(mdxFile)
	require.NoError(t, err)
	assert.Equal(t, "# new mdx", string(content))
}

func TestFixSurfaceDrift_RejectsTruncatedResponse(t *testing.T) {
	dir := t.TempDir()
	mdxFile := filepath.Join(dir, "page.mdx")
	require.NoError(t, os.WriteFile(mdxFile, []byte("original"), 0o644))

	f := &SurfaceDriftFixer{
		model: "claude-sonnet-4-6",
		client: stubSurfaceDriftClient{
			response: &anthropic.Message{
				Content: []anthropic.ContentBlockUnion{
					{Type: "text", Text: "partial"},
				},
				StopReason: anthropic.StopReasonMaxTokens,
			},
		},
	}

	err := f.FixSurfaceDrift(context.Background(), mdxFile, "communityType", "snippet")
	require.Error(t, err)
	assert.Contains(t, err.Error(), "truncated")

	content, readErr := os.ReadFile(mdxFile)
	require.NoError(t, readErr)
	assert.Equal(t, "original", string(content))
}

func TestFixSurfaceDrift_RejectsEmptyResponse(t *testing.T) {
	dir := t.TempDir()
	mdxFile := filepath.Join(dir, "page.mdx")
	require.NoError(t, os.WriteFile(mdxFile, []byte("original"), 0o644))

	f := &SurfaceDriftFixer{
		model: "claude-sonnet-4-6",
		client: stubSurfaceDriftClient{
			response: &anthropic.Message{
				Content:    []anthropic.ContentBlockUnion{},
				StopReason: anthropic.StopReasonEndTurn,
			},
		},
	}

	err := f.FixSurfaceDrift(context.Background(), mdxFile, "communityType", "snippet")
	require.Error(t, err)
	assert.Contains(t, err.Error(), "empty response")

	content, readErr := os.ReadFile(mdxFile)
	require.NoError(t, readErr)
	assert.Equal(t, "original", string(content))
}
