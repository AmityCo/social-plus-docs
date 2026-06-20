package generator_test

import (
	"os"
	"path/filepath"
	"strings"
	"testing"

	"social-plus/llmstxt/internal/config"
	"social-plus/llmstxt/internal/generator"
)

func TestRender_GoldenFiles(t *testing.T) {
	testdataDir, err := filepath.Abs("testdata")
	if err != nil {
		t.Fatal(err)
	}

	sections := []config.Section{
		{
			Title: "Chat",
			Pages: []config.Page{
				{Path: "social-plus-sdk/chat/sample.mdx"},
			},
		},
	}

	// Set up a temp docs root with the fixture MDX in the right location.
	docsRoot := t.TempDir()
	chatDir := filepath.Join(docsRoot, "social-plus-sdk", "chat")
	if err := os.MkdirAll(chatDir, 0755); err != nil {
		t.Fatal(err)
	}
	sampleSrc := filepath.Join(testdataDir, "sample.mdx")
	sampleDst := filepath.Join(chatDir, "sample.mdx")
	data, err := os.ReadFile(sampleSrc)
	if err != nil {
		t.Fatal(err)
	}
	if err := os.WriteFile(sampleDst, data, 0644); err != nil {
		t.Fatal(err)
	}

	outDir := t.TempDir()
	cfg, err := config.New(
		"https://docs.example.com",
		"Test SDK",
		"A test SDK for golden file verification.",
		docsRoot,
		outDir,
		sections,
	)
	if err != nil {
		t.Fatal(err)
	}

	llmsTxt, llmsFullTxt := generator.Render(cfg, false)

	checkGolden(t, filepath.Join(testdataDir, "llms.txt.golden"), llmsTxt)
	checkGolden(t, filepath.Join(testdataDir, "llms-full.txt.golden"), llmsFullTxt)
}

func TestGenerate_WritesFiles(t *testing.T) {
	testdataDir, err := filepath.Abs("testdata")
	if err != nil {
		t.Fatal(err)
	}

	docsRoot := t.TempDir()
	chatDir := filepath.Join(docsRoot, "social-plus-sdk", "chat")
	if err := os.MkdirAll(chatDir, 0755); err != nil {
		t.Fatal(err)
	}
	data, err := os.ReadFile(filepath.Join(testdataDir, "sample.mdx"))
	if err != nil {
		t.Fatal(err)
	}
	if err := os.WriteFile(filepath.Join(chatDir, "sample.mdx"), data, 0644); err != nil {
		t.Fatal(err)
	}

	outDir := t.TempDir()
	sections := []config.Section{
		{Title: "Chat", Pages: []config.Page{{Path: "social-plus-sdk/chat/sample.mdx"}}},
	}
	cfg, err := config.New("https://docs.example.com", "Test SDK", "desc", docsRoot, outDir, sections)
	if err != nil {
		t.Fatal(err)
	}

	if err := generator.Generate(cfg, false); err != nil {
		t.Fatalf("Generate failed: %v", err)
	}

	for _, name := range []string{"llms.txt", "llms-full.txt"} {
		path := filepath.Join(outDir, name)
		if _, err := os.Stat(path); os.IsNotExist(err) {
			t.Errorf("expected %s to exist, but it does not", name)
		}
	}
}

func TestGenerate_MissingPageFails(t *testing.T) {
	docsRoot := t.TempDir()
	outDir := t.TempDir()
	sections := []config.Section{
		{Title: "Chat", Pages: []config.Page{{Path: "nonexistent.mdx"}}},
	}
	cfg, err := config.New("https://docs.example.com", "Test SDK", "desc", docsRoot, outDir, sections)
	if err != nil {
		t.Fatal(err)
	}

	err = generator.Generate(cfg, false)
	if err == nil {
		t.Fatal("expected missing page error, got nil")
	}
	if !strings.Contains(err.Error(), "nonexistent.mdx") {
		t.Fatalf("expected missing path in error, got: %v", err)
	}
}

func TestRender_StripsTrailingWhitespace(t *testing.T) {
	docsRoot := t.TempDir()
	pageDir := filepath.Join(docsRoot, "sdk")
	if err := os.MkdirAll(pageDir, 0755); err != nil {
		t.Fatal(err)
	}
	pagePath := filepath.Join(pageDir, "trailing.mdx")
	if err := os.WriteFile(pagePath, []byte("---\ntitle: Trailing\n---\n\nLine with spaces   \nLine with tab\t\n"), 0644); err != nil {
		t.Fatal(err)
	}

	outDir := t.TempDir()
	cfg, err := config.New(
		"https://docs.example.com",
		"Test SDK",
		"desc",
		docsRoot,
		outDir,
		[]config.Section{{Title: "SDK", Pages: []config.Page{{Path: "sdk/trailing.mdx"}}}},
	)
	if err != nil {
		t.Fatal(err)
	}

	_, llmsFullTxt := generator.Render(cfg, false)
	if strings.Contains(llmsFullTxt, " \n") || strings.Contains(llmsFullTxt, "\t\n") {
		t.Fatalf("expected no trailing whitespace before newlines, got:\n%q", llmsFullTxt)
	}
	if !strings.Contains(llmsFullTxt, "Line with spaces\nLine with tab\n") {
		t.Fatalf("expected body text with whitespace trimmed, got:\n%q", llmsFullTxt)
	}
}

// checkGolden compares got against the content of goldenPath.
func checkGolden(t *testing.T, goldenPath, got string) {
	t.Helper()
	if os.Getenv("UPDATE_GOLDEN") == "1" {
		if err := os.WriteFile(goldenPath, []byte(got), 0644); err != nil {
			t.Fatalf("update golden %s: %v", goldenPath, err)
		}
		t.Logf("updated golden: %s", goldenPath)
		return
	}
	want, err := os.ReadFile(goldenPath)
	if err != nil {
		t.Fatalf("read golden %s: %v", goldenPath, err)
	}
	if got != string(want) {
		t.Errorf("output does not match golden %s\n--- got ---\n%s\n--- want ---\n%s",
			goldenPath, got, string(want))
	}
}

func TestRender_MultiSection(t *testing.T) {
	testdataDir, err := filepath.Abs("testdata")
	if err != nil {
		t.Fatal(err)
	}

	docsRoot := t.TempDir()
	chatDir := filepath.Join(docsRoot, "sdk", "chat")
	socialDir := filepath.Join(docsRoot, "sdk", "social")
	for _, d := range []string{chatDir, socialDir} {
		if err := os.MkdirAll(d, 0755); err != nil {
			t.Fatal(err)
		}
	}

	copyFile := func(src, dst string) {
		t.Helper()
		data, err := os.ReadFile(src)
		if err != nil {
			t.Fatal(err)
		}
		if err := os.WriteFile(dst, data, 0644); err != nil {
			t.Fatal(err)
		}
	}
	copyFile(filepath.Join(testdataDir, "sample.mdx"), filepath.Join(chatDir, "overview.mdx"))
	copyFile(filepath.Join(testdataDir, "sample2.mdx"), filepath.Join(chatDir, "page2.mdx"))
	copyFile(filepath.Join(testdataDir, "sample.mdx"), filepath.Join(socialDir, "overview.mdx"))

	sections := []config.Section{
		{
			Title: "Chat",
			Pages: []config.Page{
				{Path: "sdk/chat/overview.mdx"},
				{Path: "sdk/chat/page2.mdx"},
			},
		},
		{
			Title: "Social",
			Pages: []config.Page{
				{Path: "sdk/social/overview.mdx"},
			},
		},
	}

	outDir := t.TempDir()
	cfg, err := config.New(
		"https://docs.example.com",
		"Multi SDK",
		"Multi-section test.",
		docsRoot,
		outDir,
		sections,
	)
	if err != nil {
		t.Fatal(err)
	}

	llmsTxt, llmsFullTxt := generator.Render(cfg, false)

	// llms-full.txt must contain inter-page separator between the 2 chat pages.
	if !strings.Contains(llmsFullTxt, "\n---\n") {
		t.Error("llms-full.txt: expected inter-page separator '\\n---\\n' but not found")
	}
	// Must NOT end with a trailing separator.
	if strings.HasSuffix(strings.TrimRight(llmsFullTxt, "\n"), "---") {
		t.Error("llms-full.txt: must not end with a trailing '---' separator")
	}

	// Both outputs must contain both section headers.
	for _, hdr := range []string{"## Chat", "## Social"} {
		if !strings.Contains(llmsTxt, hdr) {
			t.Errorf("llms.txt: missing section header %q", hdr)
		}
		if !strings.Contains(llmsFullTxt, hdr) {
			t.Errorf("llms-full.txt: missing section header %q", hdr)
		}
	}

	// llms.txt must list all 3 pages as link entries.
	wantLines := []string{
		"- [Create Channels](https://docs.example.com/sdk/chat/overview): Build structured chat experiences by creating channels",
		"- [Send Messages](https://docs.example.com/sdk/chat/page2): Send text and media messages to channels",
		"- [Create Channels](https://docs.example.com/sdk/social/overview): Build structured chat experiences by creating channels",
	}
	for _, line := range wantLines {
		if !strings.Contains(llmsTxt, line) {
			t.Errorf("llms.txt: missing expected line:\n  %s", line)
		}
	}
}
