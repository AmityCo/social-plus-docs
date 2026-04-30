package differ_test

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"social-plus/harness/internal/differ"
	"social-plus/harness/internal/extractor"
	"social-plus/harness/internal/pages"
	"social-plus/harness/internal/report"
	"social-plus/harness/internal/scanner"
)

func TestMissingSnippet(t *testing.T) {
	fns := []extractor.PublicFunction{
		{IDs: []string{"message.delete"}, Platform: "android", File: "AmityMessageRepository.kt"},
	}
	snips := []scanner.Snippet{}
	reg := pages.NewFromPaths(nil)

	findings := differ.Diff(fns, snips, reg, "android")
	assert.Len(t, findings, 1)
	assert.Equal(t, report.TypeMissingSnippet, findings[0].Type)
	assert.Equal(t, "message.delete", findings[0].FunctionID)
}

func TestAscPageInvalid_LegacyURL(t *testing.T) {
	fns := []extractor.PublicFunction{}
	snips := []scanner.Snippet{
		{AscPage: "https://docs.amity.co/social/flutter", Platform: "flutter", File: "snippet.dart"},
	}
	reg := pages.NewFromPaths(nil)

	findings := differ.Diff(fns, snips, reg, "flutter")
	assert.Len(t, findings, 1)
	assert.Equal(t, report.TypeAscPageInvalid, findings[0].Type)
}

func TestDocMissing(t *testing.T) {
	fns := []extractor.PublicFunction{}
	snips := []scanner.Snippet{
		{AscPage: "social-plus-sdk/chat/nonexistent", Platform: "flutter", File: "snippet.dart"},
	}
	reg := pages.NewFromPaths([]string{"social-plus-sdk/chat/overview"})

	findings := differ.Diff(fns, snips, reg, "flutter")
	assert.Len(t, findings, 1)
	assert.Equal(t, report.TypeDocMissing, findings[0].Type)
}

func TestDocSurfaceDrift(t *testing.T) {
	fns := []extractor.PublicFunction{}
	snips := []scanner.Snippet{
		{
			AscPage:  "social-plus-sdk/chat/channels/create",
			Content:  "AmityChatClient.newChannelRepository().communityType().create()",
			Platform: "flutter",
			File:     "snippet.dart",
		},
	}
	reg := pages.NewFromPaths([]string{"social-plus-sdk/chat/channels/create"})
	mdx := map[string]string{
		"social-plus-sdk/chat/channels/create": "Create a channel by calling .create()",
	}

	findings := differ.DiffWithMDX(fns, snips, reg, "flutter", mdx)
	hasDrift := false
	for _, f := range findings {
		if f.Type == report.TypeDocSurfaceDrift {
			hasDrift = true
		}
	}
	assert.True(t, hasDrift)
}

func TestSnippetContentDrift(t *testing.T) {
	fns := []extractor.PublicFunction{}
	snips := []scanner.Snippet{
		{
			AscPage:  "social-plus-sdk/chat/channels/create",
			Content:  "AmityChatClient.newChannelRepository().communityType().create()",
			Platform: "flutter",
			File:     "snippet.dart",
		},
	}
	reg := pages.NewFromPaths([]string{"social-plus-sdk/chat/channels/create"})
	mdx := map[string]string{
		"social-plus-sdk/chat/channels/create": "# Create Channel\n\nSome outdated code here.",
	}

	findings := differ.DiffWithMDX(fns, snips, reg, "flutter", mdx)
	hasDrift := false
	for _, f := range findings {
		if f.Type == report.TypeSnippetContentDrift {
			hasDrift = true
		}
	}
	assert.True(t, hasDrift, "expected SNIPPET_CONTENT_DRIFT when snippet content not in MDX")
}

func TestSnippetContentDrift_NoFalsePositive(t *testing.T) {
	snips := []scanner.Snippet{
		{
			AscPage:  "social-plus-sdk/chat/channels/create",
			Content:  "AmityChatClient.newChannelRepository().create()",
			Platform: "flutter",
			File:     "snippet.dart",
		},
	}
	reg := pages.NewFromPaths([]string{"social-plus-sdk/chat/channels/create"})
	mdx := map[string]string{
		"social-plus-sdk/chat/channels/create": "AmityChatClient.newChannelRepository().create()",
	}

	findings := differ.DiffWithMDX(nil, snips, reg, "flutter", mdx)
	for _, f := range findings {
		assert.NotEqual(t, report.TypeSnippetContentDrift, f.Type,
			"SNIPPET_CONTENT_DRIFT should not fire when first line is present in MDX")
	}
}

func TestNoFindingsWhenClean(t *testing.T) {
	fns := []extractor.PublicFunction{
		{IDs: []string{"channel.create"}, Platform: "flutter", File: "AmityChannel.dart"},
	}
	snips := []scanner.Snippet{
		{
			AscPage:  "social-plus-sdk/chat/channels/create",
			Content:  "AmityChatClient.newChannelRepository().create()",
			Platform: "flutter",
			File:     "snippet.dart",
		},
	}
	reg := pages.NewFromPaths([]string{"social-plus-sdk/chat/channels/create"})

	findings := differ.Diff(fns, snips, reg, "flutter")
	assert.Empty(t, findings)
}
