package config_test

import (
	"os"
	"path/filepath"
	"testing"

	"social-plus/llmstxt/internal/config"
)

func TestLoad_ValidConfig(t *testing.T) {
	dir := t.TempDir()
	content := `
site_url: https://docs.example.com
title: "Test SDK"
description: "A test description."
docs_root: ./docs
output_dir: ./out
sections:
  - title: "Chat"
    pages:
      - path: chat/create-channel.mdx
`
	cfgPath := filepath.Join(dir, "llms-config.yml")
	if err := os.WriteFile(cfgPath, []byte(content), 0644); err != nil {
		t.Fatal(err)
	}

	cfg, err := config.Load(cfgPath)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if cfg.Title != "Test SDK" {
		t.Errorf("Title = %q, want %q", cfg.Title, "Test SDK")
	}
	if cfg.NormalisedSiteURL() != "https://docs.example.com" {
		t.Errorf("SiteURL = %q", cfg.NormalisedSiteURL())
	}
	if len(cfg.Sections) != 1 || len(cfg.Sections[0].Pages) != 1 {
		t.Errorf("unexpected sections/pages: %+v", cfg.Sections)
	}
	// Paths resolved relative to config file directory.
	wantDocs := filepath.Join(dir, "docs")
	if cfg.ResolvedDocsRoot() != wantDocs {
		t.Errorf("DocsRoot = %q, want %q", cfg.ResolvedDocsRoot(), wantDocs)
	}
}

func TestLoad_MissingFile(t *testing.T) {
	_, err := config.Load("/nonexistent/llms-config.yml")
	if err == nil {
		t.Fatal("expected error for missing file, got nil")
	}
}

func TestLoad_MissingRequiredField(t *testing.T) {
	dir := t.TempDir()
	// Missing title
	content := `
site_url: https://docs.example.com
docs_root: ./docs
output_dir: ./out
sections:
  - title: "Chat"
    pages:
      - path: chat/create-channel.mdx
`
	cfgPath := filepath.Join(dir, "llms-config.yml")
	if err := os.WriteFile(cfgPath, []byte(content), 0644); err != nil {
		t.Fatal(err)
	}

	_, err := config.Load(cfgPath)
	if err == nil {
		t.Fatal("expected validation error for missing title, got nil")
	}
}

func TestLoad_TrailingSlashNormalised(t *testing.T) {
	dir := t.TempDir()
	content := `
site_url: https://docs.example.com/
title: "Test"
docs_root: ./docs
output_dir: ./out
sections:
  - title: "Chat"
    pages:
      - path: chat/test.mdx
`
	cfgPath := filepath.Join(dir, "llms-config.yml")
	if err := os.WriteFile(cfgPath, []byte(content), 0644); err != nil {
		t.Fatal(err)
	}

	cfg, err := config.Load(cfgPath)
	if err != nil {
		t.Fatal(err)
	}
	if cfg.NormalisedSiteURL() != "https://docs.example.com" {
		t.Errorf("trailing slash not stripped: %q", cfg.NormalisedSiteURL())
	}
}

func TestNew_AbsolutePaths(t *testing.T) {
	sections := []config.Section{
		{Title: "Chat", Pages: []config.Page{{Path: "chat/test.mdx"}}},
	}
	cfg, err := config.New("https://docs.example.com", "SDK", "desc", "/abs/docs", "/abs/out", sections)
	if err != nil {
		t.Fatal(err)
	}
	if cfg.ResolvedDocsRoot() != "/abs/docs" {
		t.Errorf("DocsRoot = %q", cfg.ResolvedDocsRoot())
	}
}
