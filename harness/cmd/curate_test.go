package main

import (
	"os"
	"path/filepath"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestCurateGenTasks_WritesCurateTasksMd(t *testing.T) {
	dir := t.TempDir()

	cfgContent := `docs:
  path: docs
sdks: {}
`
	require.NoError(t, os.WriteFile(filepath.Join(dir, "harness-config.yml"), []byte(cfgContent), 0o644))

	docsDir := filepath.Join(dir, "docs", "social")
	require.NoError(t, os.MkdirAll(docsDir, 0o755))
	mdxContent := `import AddReaction from '/snippets/add-reaction.mdx';
import PostLike from '/snippets/post-like.mdx';

---
title: "Reactions"
---

## Add Reactions

<AddReaction />

## Related Topics

<PostLike />
`
	require.NoError(t, os.WriteFile(filepath.Join(docsDir, "reactions.mdx"), []byte(mdxContent), 0o644))

	snipDir := filepath.Join(dir, "docs", "snippets")
	require.NoError(t, os.MkdirAll(snipDir, 0o755))
	require.NoError(t, os.WriteFile(filepath.Join(snipDir, "add-reaction.mdx"), []byte("// add reaction code"), 0o644))
	require.NoError(t, os.WriteFile(filepath.Join(snipDir, "post-like.mdx"), []byte("// post like code"), 0o644))

	outPath := filepath.Join(dir, "curate-tasks.md")
	err := runCurateGenTasksForTest(dir, filepath.Join(dir, "harness-config.yml"), "", outPath)
	require.NoError(t, err)

	data, err := os.ReadFile(outPath)
	require.NoError(t, err)
	content := string(data)

	assert.Contains(t, content, "social/reactions")
	assert.Contains(t, content, "AddReaction")
	assert.Contains(t, content, "PostLike")
	assert.Contains(t, content, "## Add Reactions")
	assert.Contains(t, content, "add reaction code")
}

func TestCurateGenTasks_EmptyPageSkipped(t *testing.T) {
	dir := t.TempDir()

	cfgContent := `docs:
  path: docs
sdks: {}
`
	require.NoError(t, os.WriteFile(filepath.Join(dir, "harness-config.yml"), []byte(cfgContent), 0o644))

	docsDir := filepath.Join(dir, "docs", "social")
	require.NoError(t, os.MkdirAll(docsDir, 0o755))
	mdxContent := `---
title: "Empty"
---

## Overview

No code here.
`
	require.NoError(t, os.WriteFile(filepath.Join(docsDir, "empty.mdx"), []byte(mdxContent), 0o644))

	outPath := filepath.Join(dir, "curate-tasks.md")
	err := runCurateGenTasksForTest(dir, filepath.Join(dir, "harness-config.yml"), "", outPath)
	require.NoError(t, err)

	data, err := os.ReadFile(outPath)
	require.NoError(t, err)
	assert.NotContains(t, string(data), "social/empty")
}

func TestCurateApply_RemovesHighConfidenceSnippet(t *testing.T) {
	dir := t.TempDir()

	docsDir := filepath.Join(dir, "docs", "social")
	require.NoError(t, os.MkdirAll(docsDir, 0o755))
	mdxContent := `import AddReaction from '/snippets/add-reaction.mdx';
import PostLike from '/snippets/post-like.mdx';

---
title: "Reactions"
---

## Add Reactions

<AddReaction />

## Related Topics

<PostLike />
`
	mdxPath := filepath.Join(docsDir, "reactions.mdx")
	require.NoError(t, os.WriteFile(mdxPath, []byte(mdxContent), 0o644))

	decisions := `{
  "generated_at": "2026-01-01T00:00:00Z",
  "pages": [{
    "page_path": "social/reactions",
    "decisions": [{
      "name": "PostLike",
      "action": "REMOVE",
      "reason": "irrelevant to this page",
      "confidence": "high"
    }]
  }]
}`
	decisionsPath := filepath.Join(dir, "curate-decisions.json")
	require.NoError(t, os.WriteFile(decisionsPath, []byte(decisions), 0o644))

	reviewPath := filepath.Join(dir, "curate-review.json")
	err := runCurateApply(dir, filepath.Join(dir, "docs"), decisionsPath, reviewPath, false)
	require.NoError(t, err)

	data, err := os.ReadFile(mdxPath)
	require.NoError(t, err)
	assert.NotContains(t, string(data), "PostLike")
	assert.Contains(t, string(data), "AddReaction")
}

func TestCurateApply_DryRunDoesNotModifyFiles(t *testing.T) {
	dir := t.TempDir()
	docsDir := filepath.Join(dir, "docs", "social")
	require.NoError(t, os.MkdirAll(docsDir, 0o755))
	original := `import PostLike from '/snippets/post-like.mdx';

---
title: "Reactions"
---

<PostLike />
`
	mdxPath := filepath.Join(docsDir, "reactions.mdx")
	require.NoError(t, os.WriteFile(mdxPath, []byte(original), 0o644))

	decisions := `{
  "generated_at": "2026-01-01T00:00:00Z",
  "pages": [{
    "page_path": "social/reactions",
    "decisions": [{"name": "PostLike", "action": "REMOVE", "confidence": "high", "reason": "test"}]
  }]
}`
	decisionsPath := filepath.Join(dir, "curate-decisions.json")
	require.NoError(t, os.WriteFile(decisionsPath, []byte(decisions), 0o644))

	reviewPath := filepath.Join(dir, "curate-review.json")
	err := runCurateApply(dir, filepath.Join(dir, "docs"), decisionsPath, reviewPath, true)
	require.NoError(t, err)

	data, err := os.ReadFile(mdxPath)
	require.NoError(t, err)
	assert.Equal(t, original, string(data))
}

func TestCurateApply_LowConfidenceWritesReviewFile(t *testing.T) {
	dir := t.TempDir()
	docsDir := filepath.Join(dir, "docs", "social")
	require.NoError(t, os.MkdirAll(docsDir, 0o755))
	original := `import PostLike from '/snippets/post-like.mdx';

---
title: "Reactions"
---

<PostLike />
`
	mdxPath := filepath.Join(docsDir, "reactions.mdx")
	require.NoError(t, os.WriteFile(mdxPath, []byte(original), 0o644))

	decisions := `{
  "generated_at": "2026-01-01T00:00:00Z",
  "pages": [{
    "page_path": "social/reactions",
    "decisions": [{"name": "PostLike", "action": "REMOVE", "confidence": "low", "reason": "unsure"}]
  }]
}`
	decisionsPath := filepath.Join(dir, "curate-decisions.json")
	require.NoError(t, os.WriteFile(decisionsPath, []byte(decisions), 0o644))

	reviewPath := filepath.Join(dir, "curate-review.json")
	err := runCurateApply(dir, filepath.Join(dir, "docs"), decisionsPath, reviewPath, false)
	require.NoError(t, err)

	data, err := os.ReadFile(mdxPath)
	require.NoError(t, err)
	assert.Contains(t, string(data), "PostLike")

	reviewData, err := os.ReadFile(reviewPath)
	require.NoError(t, err)
	assert.Contains(t, string(reviewData), "PostLike")
}
