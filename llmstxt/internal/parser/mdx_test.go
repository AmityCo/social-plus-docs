package parser_test

import (
	"testing"

	"social-plus/llmstxt/internal/parser"
)

func TestParse(t *testing.T) {
	tests := []struct {
		name      string
		input     string
		wantTitle string
		wantDesc  string
		wantBody  string
	}{
		{
			name: "extracts frontmatter title and description",
			input: "---\ntitle: \"Create Channels\"\ndescription: \"Build chat experiences\"\n---\n\nSome body text.",
			wantTitle: "Create Channels",
			wantDesc:  "Build chat experiences",
			wantBody:  "Some body text.",
		},
		{
			name: "strips JSX opening and closing tags, keeps inner content",
			input: "---\ntitle: Test\n---\n\n<CardGroup cols={2}>\n**inner text**\n</CardGroup>",
			wantTitle: "Test",
			wantBody:  "**inner text**",
		},
		{
			name: "strips Warning/Note/Tip component tags, keeps inner prose",
			input: "---\ntitle: Test\n---\n\n<Warning>\nDo not do this.\n</Warning>",
			wantTitle: "Test",
			wantBody:  "Do not do this.",
		},
		{
			name: "strips import statements",
			input: "---\ntitle: Test\n---\n\nimport Foo from './foo'\n\nBody text.",
			wantTitle: "Test",
			wantBody:  "Body text.",
		},
		{
			name: "preserves code blocks",
			input: "---\ntitle: Test\n---\n\nProse.\n\n```typescript\nconst x = 1;\n```",
			wantTitle: "Test",
			wantBody:  "Prose.\n\n```typescript\nconst x = 1;\n```",
		},
		{
			name: "collapses more than 2 blank lines to 2",
			input: "---\ntitle: Test\n---\n\nLine A.\n\n\n\nLine B.",
			wantTitle: "Test",
			wantBody:  "Line A.\n\n\nLine B.",
		},
		{
			name: "extracts title from first H1 when no frontmatter",
			input: "# My Feature\n\nSome description text.",
			wantTitle: "My Feature",
			wantBody:  "Some description text.",
		},
		{
			name:      "preserves explicit frontmatter title without modification",
			input:     "---\ntitle: Explicit\n---\n\nBody.",
			wantTitle: "Explicit",
			wantBody:  "Body.",
		},
		{
			name:      "does not extract H1 from inside a fenced code block",
			input:     "```bash\n# bash comment\n```\n\n# Real Title\n\nBody text.",
			wantTitle: "Real Title",
			wantBody:  "```bash\n# bash comment\n```\n\n\nBody text.",
		},
		{
			name:      "malformed frontmatter without closing --- produces empty body",
			input:     "---\ntitle: Broken\n\nBody text.",
			wantTitle: "Broken",
			wantDesc:  "",
			wantBody:  "",
		},
		{
			name:     "parses YAML block scalar description (>-)",
			input:    "---\ntitle: Ban Members\ndescription: >-\n  When a user is banned they are removed from the channel and\n  no longer able to participate.\n---\n\nBody.",
			wantTitle: "Ban Members",
			wantDesc:  "When a user is banned they are removed from the channel and no longer able to participate.",
			wantBody:  "Body.",
		},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			got := parser.Parse([]byte(tc.input))

			if got.Title != tc.wantTitle {
				t.Errorf("Title = %q, want %q", got.Title, tc.wantTitle)
			}
			if got.Description != tc.wantDesc {
				t.Errorf("Description = %q, want %q", got.Description, tc.wantDesc)
			}
			if got.Body != tc.wantBody {
				t.Errorf("Body:\ngot:  %q\nwant: %q", got.Body, tc.wantBody)
			}
		})
	}
}

func TestParse_IndentedFenceNormalized(t *testing.T) {
	input := "---\ntitle: Test\n---\n\n    ```typescript\n    const x = 1;\n    ```"
	want := "```typescript\nconst x = 1;\n```"

	got := parser.Parse([]byte(input))
	if got.Body != want {
		t.Errorf("Body:\ngot:  %q\nwant: %q", got.Body, want)
	}
}

func TestTitleFromPath(t *testing.T) {
	tests := []struct {
		path string
		want string
	}{
		{"create-channel.mdx", "Create Channel"},
		{"send-a-message.mdx", "Send A Message"},
		{"overview.mdx", "Overview"},
		{"social/posts/get-post.mdx", "Get Post"},
	}
	for _, tc := range tests {
		got := parser.TitleFromPath(tc.path)
		if got != tc.want {
			t.Errorf("TitleFromPath(%q) = %q, want %q", tc.path, got, tc.want)
		}
	}
}
