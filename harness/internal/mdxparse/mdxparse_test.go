package mdxparse

import (
	"testing"
	"path/filepath"
)

func TestExtractSections_basic(t *testing.T) {
	path := filepath.Join("testdata", "sample.mdx")
	sections, err := ExtractSections(path)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if len(sections) != 3 {
		t.Errorf("expected 3 sections, got %d", len(sections))
	}
	expected := []string{
		"### Step 1: Initialize the SDK",
		"### Step 2: Login User",
		"### Step 3: With Nested Prose Before CodeGroup",
	}
	for i, sec := range sections {
		if sec.Heading != expected[i] {
			t.Errorf("section %d heading: want %q, got %q", i, expected[i], sec.Heading)
		}
	}
}

func TestExtractSections_slugs(t *testing.T) {
	path := filepath.Join("testdata", "sample.mdx")
	sections, err := ExtractSections(path)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	expected := []string{
		"step-1-initialize-the-sdk",
		"step-2-login-user",
		"step-3-with-nested-prose-before-codegroup",
	}
	for i, sec := range sections {
		if sec.Slug != expected[i] {
			t.Errorf("section %d slug: want %q, got %q", i, expected[i], sec.Slug)
		}
	}
}

func TestExtractSections_noProsOnly(t *testing.T) {
	path := filepath.Join("testdata", "sample.mdx")
	sections, err := ExtractSections(path)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	for _, sec := range sections {
		if sec.Heading == "### Just Prose Section" {
			t.Errorf("prose-only section should not be included")
		}
	}
}

func TestExtractSections_fileNotFound(t *testing.T) {
	_, err := ExtractSections("testdata/does-not-exist.mdx")
	if err == nil {
		t.Errorf("expected error for missing file, got nil")
	}
}
