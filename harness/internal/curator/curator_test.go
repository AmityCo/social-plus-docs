package curator_test

import (
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"

	"social-plus/harness/internal/curator"
)

const sampleMDX = `import AddReaction from '/snippets/core/add-reaction.mdx';
import PostLike from '/snippets/core/post-like.mdx';
import StoryLike from '/snippets/core/story-like.mdx';

---
title: "Reactions"
---

## Add Reactions

Some prose about adding reactions.

<AddReaction />

## Remove Reactions

Some prose about removing reactions.

## Related Topics

<PostLike />
<StoryLike />
`

func TestParsePage_ExtractsSections(t *testing.T) {
	p := curator.ParsePage("reactions.mdx", "core/reactions", sampleMDX, func(path string) string {
		return "// snippet content for " + path
	})
	assert.Equal(t, []string{"## Add Reactions", "## Remove Reactions", "## Related Topics"}, p.Sections)
}

func TestParsePage_ExtractsPlacedSnippets(t *testing.T) {
	p := curator.ParsePage("reactions.mdx", "core/reactions", sampleMDX, func(path string) string {
		return "// code"
	})
	// All 3 imports have component tags in the body
	assert.Len(t, p.Placed, 3)
	names := make([]string, len(p.Placed))
	for i, s := range p.Placed {
		names[i] = s.Name
	}
	assert.ElementsMatch(t, []string{"AddReaction", "PostLike", "StoryLike"}, names)
}

func TestParsePage_ProseStripsImportsAndTags(t *testing.T) {
	p := curator.ParsePage("reactions.mdx", "core/reactions", sampleMDX, func(string) string { return "" })
	assert.NotContains(t, p.Prose, "import ")
	assert.NotContains(t, p.Prose, "<AddReaction")
	assert.NotContains(t, p.Prose, "<PostLike")
	assert.Contains(t, p.Prose, "Some prose about adding reactions")
}

func TestParsePage_SnippetContentLoaded(t *testing.T) {
	p := curator.ParsePage("reactions.mdx", "core/reactions", sampleMDX, func(path string) string {
		return "content:" + path
	})
	for _, s := range p.Placed {
		assert.Contains(t, s.Content, "content:")
	}
}

func TestParsePage_UnusedImportNotPlaced(t *testing.T) {
	mdx := "import Ghost from '/snippets/ghost.mdx';\n\nSome prose without a ghost tag.\n"
	p := curator.ParsePage("f.mdx", "page", mdx, nil)
	assert.Len(t, p.Placed, 0)
}

func TestApply_RemoveHighConfidence(t *testing.T) {
	decisions := []curator.Decision{
		{Name: "PostLike", Action: curator.ActionRemove, Confidence: curator.ConfidenceHigh, Reason: "irrelevant"},
	}
	modified, applied, flagged := curator.Apply(sampleMDX, decisions)
	assert.Len(t, applied, 1)
	assert.Len(t, flagged, 0)
	assert.NotContains(t, modified, "import PostLike")
	assert.NotContains(t, modified, "<PostLike />")
	// Other imports untouched
	assert.Contains(t, modified, "import AddReaction")
	assert.Contains(t, modified, "<AddReaction />")
}

func TestApply_RemoveLowConfidenceFlags(t *testing.T) {
	decisions := []curator.Decision{
		{Name: "PostLike", Action: curator.ActionRemove, Confidence: curator.ConfidenceLow, Reason: "unsure"},
	}
	modified, applied, flagged := curator.Apply(sampleMDX, decisions)
	assert.Len(t, applied, 0)
	assert.Len(t, flagged, 1)
	// Content unchanged
	assert.Contains(t, modified, "import PostLike")
	assert.Contains(t, modified, "<PostLike />")
}

func TestApply_KeepResections(t *testing.T) {
	// StoryLike is under ## Related Topics; move it to ## Add Reactions
	decisions := []curator.Decision{
		{Name: "StoryLike", Action: curator.ActionKeep, Section: "## Add Reactions", Confidence: curator.ConfidenceHigh, Reason: "belongs here"},
	}
	modified, applied, flagged := curator.Apply(sampleMDX, decisions)
	assert.Len(t, applied, 1)
	assert.Len(t, flagged, 0)
	// Tag moved: appears after ## Add Reactions, not at end of file
	lines := strings.Split(modified, "\n")
	addReactionIdx := -1
	storyLikeIdx := -1
	for i, l := range lines {
		if strings.TrimSpace(l) == "## Add Reactions" {
			addReactionIdx = i
		}
		if strings.Contains(l, "<StoryLike") {
			storyLikeIdx = i
		}
	}
	assert.Greater(t, storyLikeIdx, addReactionIdx, "StoryLike should appear after ## Add Reactions")
	// Should not appear under Related Topics anymore (which comes after)
	relTopicsIdx := -1
	for i, l := range lines {
		if strings.TrimSpace(l) == "## Related Topics" {
			relTopicsIdx = i
		}
	}
	assert.Less(t, storyLikeIdx, relTopicsIdx, "StoryLike should not be under Related Topics")
}

func TestApply_MoveHighConfidenceRemovesFromPage(t *testing.T) {
	decisions := []curator.Decision{
		{Name: "PostLike", Action: curator.ActionMove, TargetPage: "social/posts", Confidence: curator.ConfidenceHigh, Reason: "belongs on post page"},
	}
	modified, applied, flagged := curator.Apply(sampleMDX, decisions)
	assert.Len(t, applied, 1)
	assert.Len(t, flagged, 0)
	assert.NotContains(t, modified, "import PostLike")
	assert.NotContains(t, modified, "<PostLike />")
}

func TestApply_MoveLowConfidenceFlags(t *testing.T) {
	decisions := []curator.Decision{
		{Name: "PostLike", Action: curator.ActionMove, TargetPage: "social/posts", Confidence: curator.ConfidenceLow, Reason: "unsure"},
	}
	modified, applied, flagged := curator.Apply(sampleMDX, decisions)
	assert.Len(t, applied, 0)
	assert.Len(t, flagged, 1)
	assert.Contains(t, modified, "import PostLike")
}

func TestApply_FlagAlwaysFlags(t *testing.T) {
	decisions := []curator.Decision{
		{Name: "AddReaction", Action: curator.ActionFlag, Confidence: curator.ConfidenceHigh, Reason: "ambiguous"},
	}
	_, applied, flagged := curator.Apply(sampleMDX, decisions)
	assert.Len(t, applied, 0)
	assert.Len(t, flagged, 1)
}

func TestApply_KeepNoResection_NoChange(t *testing.T) {
	// AddReaction is already under ## Add Reactions — no move needed
	decisions := []curator.Decision{
		{Name: "AddReaction", Action: curator.ActionKeep, Section: "## Add Reactions", Confidence: curator.ConfidenceMedium, Reason: "correct"},
	}
	modified, applied, _ := curator.Apply(sampleMDX, decisions)
	assert.Len(t, applied, 1)
	// Content structurally same (AddReaction already in right section)
	assert.Contains(t, modified, "<AddReaction />")
}
