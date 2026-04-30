package generator

import (
	"context"
	"fmt"
	"strings"

	"github.com/anthropics/anthropic-sdk-go"
	"github.com/anthropics/anthropic-sdk-go/option"
)

type messageClient interface {
	New(ctx context.Context, body anthropic.MessageNewParams, opts ...option.RequestOption) (*anthropic.Message, error)
}

type Generator struct {
	model  string
	client messageClient
}

func New(model, apiKey string) *Generator {
	client := anthropic.NewClient(option.WithAPIKey(apiKey))
	return &Generator{
		model:  model,
		client: &client.Messages,
	}
}

// BuildPrompt constructs the AI prompt for snippet generation.
func (g *Generator) BuildPrompt(platform, functionID, signature, sourceFile string) string {
	return fmt.Sprintf(`You are generating a code snippet for the social.plus SDK documentation harness.

Platform: %s
Function ID: %s
Signature from SDK source:
%s
Source file: %s

Generate a minimal, working code snippet that demonstrates this function.
The snippet MUST use the exact begin_sample_code / end_sample_code format:

/* begin_sample_code
   gist_id: PLACEHOLDER
   filename: <appropriate filename for platform>
   asc_page: <docs.json relative path, e.g. social-plus-sdk/chat/messaging-features/messages>
   description: <one line description>
   */
<working code example>
/* end_sample_code */

Rules:
- Use real Amity SDK class names from the signature
- Keep it minimal — demonstrate the function, nothing else
- The asc_page must be a relative path matching the docs structure (no full URLs)
- Include proper imports for the platform`, platform, functionID, signature, sourceFile)
}

// Generate calls the AI to produce a snippet for a missing function.
func (g *Generator) Generate(ctx context.Context, platform, functionID, signature, sourceFile string) (string, error) {
	prompt := g.BuildPrompt(platform, functionID, signature, sourceFile)

	msg, err := g.client.New(ctx, anthropic.MessageNewParams{
		Model:     anthropic.Model(g.model),
		MaxTokens: 2048,
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock(prompt)),
		},
	})
	if err != nil {
		return "", fmt.Errorf("ai generate: %w", err)
	}
	if msg.StopReason == anthropic.StopReasonMaxTokens {
		return "", fmt.Errorf("ai generate: truncated response for %s/%s", platform, functionID)
	}

	var result strings.Builder
	for _, block := range msg.Content {
		if block.Type == "text" {
			result.WriteString(block.Text)
		}
	}

	return result.String(), nil
}
