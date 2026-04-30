package manifest_test

import (
	"path/filepath"
	"testing"

	"social-plus/harness/internal/manifest"
)

func TestLoad_valid(t *testing.T) {
	m, ok, err := manifest.LoadForPage("testdata", "sample")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if !ok {
		t.Fatal("expected manifest to be found")
	}
	if len(m.Sections) != 2 {
		t.Fatalf("want 2 sections, got %d", len(m.Sections))
	}
	sec, exists := m.Sections["step-1-initialize"]
	if !exists {
		t.Fatal("expected section step-1-initialize")
	}
	if sec.Heading != "### Step 1: Initialize" {
		t.Errorf("heading: got %q", sec.Heading)
	}
	if len(sec.Snippets) != 1 || sec.Snippets[0] != "client-setup" {
		t.Errorf("snippets: got %v", sec.Snippets)
	}
}

func TestLoad_missing(t *testing.T) {
	_, ok, err := manifest.LoadForPage("testdata", "nonexistent")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if ok {
		t.Fatal("expected not found")
	}
}

func TestLoad_malformed(t *testing.T) {
	_, _, err := manifest.LoadForPage("testdata", "malformed")
	if err == nil {
		t.Fatal("expected error for malformed YAML")
	}
}

func TestSectionForSnippet(t *testing.T) {
	m, _, _ := manifest.LoadForPage("testdata", "sample")
	sectionKey, found := m.SectionForSnippet("client-login")
	if !found {
		t.Fatal("expected to find client-login")
	}
	if sectionKey != "step-2-login" {
		t.Errorf("got section key %q", sectionKey)
	}
}

func TestPathForPage(t *testing.T) {
	got := manifest.PathForPage("testdata", "sample")
	want := filepath.Join("testdata", "sample.manifest.yml")
	if got != want {
		t.Errorf("got %q want %q", got, want)
	}
}
