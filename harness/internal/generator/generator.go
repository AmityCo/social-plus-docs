package generator

import (
	"context"
	"errors"
	"fmt"
)

// ErrUseCopilotCLI is returned when Generate is called directly.
// AI snippet generation is handled by Copilot CLI via 'harness prompt'.
var ErrUseCopilotCLI = errors.New("AI generation is delegated to Copilot CLI — run 'harness prompt' to get tasks")

// Generator holds configuration for snippet generation prompts.
type Generator struct {
	model string
}

// New creates a Generator. The apiKey parameter is kept for API compatibility
// but is ignored — generation is handled by Copilot CLI.
func New(model, _ string) *Generator {
	return &Generator{model: model}
}

// BuildPrompt constructs the AI prompt for snippet generation.
// This is used by 'harness prompt' to generate task files for Copilot CLI.
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
   filename: <appropriate filename for platform>
   sp_docs_page: <docs.json relative path, e.g. social-plus-sdk/chat/messaging-features/messages>
   description: <one line description>
   */
<working code example>
/* end_sample_code */

Rules:
- Use real Amity SDK class names from the signature
- Keep it minimal — demonstrate the function, nothing else
- The sp_docs_page must be a relative path matching the docs structure (no full URLs)
- Include proper imports for the platform`, platform, functionID, signature, sourceFile)
}

// Generate always returns ErrUseCopilotCLI.
// Use 'harness prompt' to generate a task file for Copilot CLI instead.
func (g *Generator) Generate(_ context.Context, _, _, _, _ string) (string, error) {
	return "", ErrUseCopilotCLI
}
