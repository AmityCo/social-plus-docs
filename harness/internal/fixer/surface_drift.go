package fixer

import (
	"context"
	"errors"
	"fmt"
)

// ErrUseCopilotCLI is returned when FixSurfaceDrift is called directly.
// AI surface drift fixing is handled by Copilot CLI via 'harness prompt'.
var ErrUseCopilotCLI = errors.New("AI fixing is delegated to Copilot CLI — run 'harness prompt' to get tasks")

// SurfaceDriftFixer holds configuration for surface drift prompts.
type SurfaceDriftFixer struct {
	model string
}

// NewSurfaceDriftFixer creates a SurfaceDriftFixer. The apiKey parameter is kept
// for API compatibility but is ignored — fixing is handled by Copilot CLI.
func NewSurfaceDriftFixer(model, _ string) *SurfaceDriftFixer {
	return &SurfaceDriftFixer{model: model}
}

// BuildPrompt constructs the AI prompt for surface drift fixing.
// This is used by 'harness prompt' to generate task files for Copilot CLI.
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

// FixSurfaceDrift always returns ErrUseCopilotCLI.
// Use 'harness prompt' to generate a task file for Copilot CLI instead.
func (f *SurfaceDriftFixer) FixSurfaceDrift(_ context.Context, _, _, _ string) error {
	return ErrUseCopilotCLI
}

// sanitizeAIResponse strips common LLM preamble (e.g. "Here's the updated MDX:\n\n")
// before the first MDX element (# heading or < tag).
func sanitizeAIResponse(s string) (string, error) {
	for i, ch := range s {
		if ch == '#' || ch == '<' {
			return s[i:], nil
		}
	}
	return "", fmt.Errorf("ai response does not contain MDX content (no '#' or '<' found)")
}
