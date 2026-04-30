package fixer

import (
	"context"
	"fmt"
	"os"
	"strings"

	"github.com/anthropics/anthropic-sdk-go"
	"github.com/anthropics/anthropic-sdk-go/option"
)

type surfaceDriftMessageClient interface {
	New(ctx context.Context, body anthropic.MessageNewParams, opts ...option.RequestOption) (*anthropic.Message, error)
}

type SurfaceDriftFixer struct {
	model  string
	client surfaceDriftMessageClient
}

func NewSurfaceDriftFixer(model, apiKey string) *SurfaceDriftFixer {
	client := anthropic.NewClient(option.WithAPIKey(apiKey))
	return &SurfaceDriftFixer{
		model:  model,
		client: &client.Messages,
	}
}

// BuildPrompt constructs the AI prompt for surface drift fixing.
func (f *SurfaceDriftFixer) BuildPrompt(currentContent, missingCall, snippetContent string) string {
	return fmt.Sprintf(`You are fixing a documentation page that is missing a method reference.

Current MDX content:
%s

The snippet for this page calls %q but the documentation does not mention it.

Snippet code:
%s

Add a minimal mention of %q to the documentation — update the relevant code example or add a note.
Return ONLY the complete updated MDX content, no explanations.`,
		currentContent, missingCall, snippetContent, missingCall)
}

// FixSurfaceDrift rewrites the MDX section to include the missing method call.
func (f *SurfaceDriftFixer) FixSurfaceDrift(ctx context.Context, mdxFile, missingCall, snippetContent string) error {
	current, err := os.ReadFile(mdxFile)
	if err != nil {
		return fmt.Errorf("read mdx: %w", err)
	}

	prompt := f.BuildPrompt(string(current), missingCall, snippetContent)

	msg, err := f.client.New(ctx, anthropic.MessageNewParams{
		Model:     anthropic.Model(f.model),
		MaxTokens: 4096,
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock(prompt)),
		},
	})
	if err != nil {
		return fmt.Errorf("ai fix: %w", err)
	}
	if msg.StopReason == anthropic.StopReasonMaxTokens {
		return fmt.Errorf("ai fix: truncated response for %s", mdxFile)
	}

	var result strings.Builder
	for _, block := range msg.Content {
		if block.Type == "text" {
			result.WriteString(block.Text)
		}
	}
	if result.Len() == 0 {
		return fmt.Errorf("ai fix: empty response for %s", mdxFile)
	}

	sanitized, err := sanitizeAIResponse(result.String())
	if err != nil {
		return fmt.Errorf("ai fix: %w", err)
	}
	return os.WriteFile(mdxFile, []byte(sanitized), 0o644)
}

// sanitizeAIResponse strips common LLM preamble (e.g. "Here's the updated MDX:\n\n")
// before the first MDX element (# heading or < tag).
func sanitizeAIResponse(s string) (string, error) {
	for i, ch := range s {
		if ch == '#' || ch == '<' {
			return strings.TrimSpace(s[i:]), nil
		}
	}
	return "", fmt.Errorf("ai response does not contain MDX content (no '#' or '<' found)")
}
