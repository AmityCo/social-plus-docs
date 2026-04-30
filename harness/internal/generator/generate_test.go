package generator

import (
	"context"
	"errors"
	"testing"

	"github.com/anthropics/anthropic-sdk-go"
	"github.com/anthropics/anthropic-sdk-go/option"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

type stubMessageClient struct {
	response *anthropic.Message
	err      error
}

func (s stubMessageClient) New(_ context.Context, _ anthropic.MessageNewParams, _ ...option.RequestOption) (*anthropic.Message, error) {
	if s.err != nil {
		return nil, s.err
	}
	return s.response, nil
}

func TestGenerate_ReturnsTextResponse(t *testing.T) {
	g := &Generator{
		model: "claude-sonnet-4-6",
		client: stubMessageClient{
			response: &anthropic.Message{
				Content: []anthropic.ContentBlockUnion{
					{Type: "text", Text: "snippet"},
				},
				StopReason: anthropic.StopReasonEndTurn,
			},
		},
	}

	got, err := g.Generate(context.Background(), "android", "message.delete", "sig", "file.kt")
	require.NoError(t, err)
	assert.Equal(t, "snippet", got)
}

func TestGenerate_ReturnsErrorWhenResponseTruncated(t *testing.T) {
	g := &Generator{
		model: "claude-sonnet-4-6",
		client: stubMessageClient{
			response: &anthropic.Message{
				Content: []anthropic.ContentBlockUnion{
					{Type: "text", Text: "partial"},
				},
				StopReason: anthropic.StopReasonMaxTokens,
			},
		},
	}

	_, err := g.Generate(context.Background(), "android", "message.delete", "sig", "file.kt")
	require.Error(t, err)
	assert.Contains(t, err.Error(), "truncated")
}

func TestGenerate_ReturnsErrorOnEmptyResponse(t *testing.T) {
	g := &Generator{
		model: "claude-sonnet-4-6",
		client: stubMessageClient{
			response: &anthropic.Message{
				Content:    []anthropic.ContentBlockUnion{},
				StopReason: anthropic.StopReasonEndTurn,
			},
		},
	}

	_, err := g.Generate(context.Background(), "android", "message.delete", "sig", "file.kt")
	require.Error(t, err)
	assert.Contains(t, err.Error(), "empty response")
}

func TestGenerate_WrapsClientError(t *testing.T) {
	g := &Generator{
		model:  "claude-sonnet-4-6",
		client: stubMessageClient{err: errors.New("boom")},
	}

	_, err := g.Generate(context.Background(), "android", "message.delete", "sig", "file.kt")
	require.Error(t, err)
	assert.Contains(t, err.Error(), "ai generate")
}
