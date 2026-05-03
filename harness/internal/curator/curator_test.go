package curator_test

import (
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
