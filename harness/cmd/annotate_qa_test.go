package main

import (
	"os"
	"path/filepath"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestRunAnnotateQA_GeneratesTasksFile(t *testing.T) {
	dir := t.TempDir()

	docsDir := filepath.Join(dir, "docs", "social")
	require.NoError(t, os.MkdirAll(docsDir, 0o755))
	require.NoError(t, os.WriteFile(filepath.Join(docsDir, "reactions.mdx"), []byte(`---
title: Reactions
---

## Overview

Enable rich emotional responses with reactions.
`), 0o644))

	patchContent := `generated_by: harness annotate
note: review before applying
patches:
  - file: android/ReactionRepo.kt
    function: addReaction
    asc_page: social/reactions
  - file: android/ReactionRepo.kt
    function: getProductInfo
    asc_page: social/reactions
`
	patchPath := filepath.Join(dir, "annotation-patches.yml")
	require.NoError(t, os.WriteFile(patchPath, []byte(patchContent), 0o644))

	outPath := filepath.Join(dir, "annotation-qa-tasks.md")
	err := runAnnotateQA(filepath.Join(dir, "docs"), patchPath, outPath)
	require.NoError(t, err)

	data, err := os.ReadFile(outPath)
	require.NoError(t, err)
	content := string(data)

	assert.Contains(t, content, "addReaction")
	assert.Contains(t, content, "getProductInfo")
	assert.Contains(t, content, "social/reactions")
	assert.Contains(t, content, "Enable rich emotional responses")
	assert.Contains(t, content, "ANNOTATION_SUSPECT")
	assert.True(t, strings.HasPrefix(content, "# Annotation QA Tasks"))
}

func TestRunAnnotateQA_MissingPageWarnsAndContinues(t *testing.T) {
	dir := t.TempDir()
	require.NoError(t, os.MkdirAll(filepath.Join(dir, "docs"), 0o755))

	patchContent := `generated_by: harness annotate
note: test
patches:
  - file: android/Foo.kt
    function: doSomething
    asc_page: nonexistent/page
`
	patchPath := filepath.Join(dir, "annotation-patches.yml")
	require.NoError(t, os.WriteFile(patchPath, []byte(patchContent), 0o644))

	outPath := filepath.Join(dir, "annotation-qa-tasks.md")
	err := runAnnotateQA(filepath.Join(dir, "docs"), patchPath, outPath)
	require.NoError(t, err)

	data, err := os.ReadFile(outPath)
	require.NoError(t, err)
	assert.Contains(t, string(data), "doSomething")
}
