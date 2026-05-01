package main

import (
	"encoding/json"
	"os"
	"path/filepath"
	"strings"
	"testing"

	"gopkg.in/yaml.v3"

	"social-plus/harness/internal/patchgen"
	"social-plus/harness/internal/report"
)

func TestRunAnnotate(t *testing.T) {
	dir := t.TempDir()

	// Create minimal SDK directory + source file
	sdkDir := filepath.Join(dir, "sdk", "android", "src")
	if err := os.MkdirAll(sdkDir, 0o755); err != nil {
		t.Fatal(err)
	}
	ktContent := `package com.amity.sdk.post

class AmityPostRepository {
    fun createPost(text: String): Post {
        return Post()
    }
}
`
	ktPath := filepath.Join(sdkDir, "AmityPostRepository.kt")
	if err := os.WriteFile(ktPath, []byte(ktContent), 0o644); err != nil {
		t.Fatal(err)
	}

	// harness-config.yml pointing to the SDK
	cfgContent := "sdks:\n  android:\n    path: sdk/android\n    snippet_dir: src\n    compile_cmd: []\ndocs:\n  path: .\nllm:\n  model: test\n"
	cfgPath := filepath.Join(dir, "harness-config.yml")
	if err := os.WriteFile(cfgPath, []byte(cfgContent), 0o644); err != nil {
		t.Fatal(err)
	}

	// harness-report.json with one PUBLIC_FUNC_UNANNOTATED finding
	relPath := "src/AmityPostRepository.kt"
	finding := report.Finding{
		ID:       "public-func-unannotated:android:" + relPath + ":createPost",
		Type:     report.TypePublicFuncUnannotated,
		Platform: "android",
		Detail:   "Public function 'createPost' in AmityPostRepository (" + relPath + ") has no begin_public_function annotation",
		Status:   report.StatusOpen,
	}
	rep := report.Report{
		GeneratedAt: "2024-01-01T00:00:00Z",
		Findings:    []report.Finding{finding},
	}
	repBytes, _ := json.Marshal(rep)
	if err := os.WriteFile(filepath.Join(dir, "harness-report.json"), repBytes, 0o644); err != nil {
		t.Fatal(err)
	}

	outPath := filepath.Join(dir, "annotation-patches.yml")

	// Run the annotate command
	runAnnotate([]string{
		"--config", cfgPath,
		"--out", outPath,
	})

	// Read and parse the output
	b, err := os.ReadFile(outPath)
	if err != nil {
		t.Fatalf("annotation-patches.yml not written: %v", err)
	}

	var pf PatchFile
	if err := yaml.Unmarshal(b, &pf); err != nil {
		t.Fatalf("unmarshal patches: %v", err)
	}

	if len(pf.Patches) != 1 {
		t.Fatalf("expected 1 patch, got %d", len(pf.Patches))
	}

	p := pf.Patches[0]
	if p.Platform != "android" {
		t.Errorf("platform = %q, want android", p.Platform)
	}
	if p.SuggestedID != patchgen.InferID("AmityPostRepository", "createPost") {
		t.Errorf("SuggestedID = %q, want %q", p.SuggestedID, patchgen.InferID("AmityPostRepository", "createPost"))
	}
	if p.InsertLine != 4 {
		t.Errorf("InsertLine = %d, want 4", p.InsertLine)
	}
	if !strings.Contains(p.Annotation, "begin_public_function") {
		t.Errorf("Annotation %q does not contain 'begin_public_function'", p.Annotation)
	}
}

func TestRunAnnotateApply(t *testing.T) {
	dir := t.TempDir()

	sdkDir := filepath.Join(dir, "sdk", "android", "src")
	if err := os.MkdirAll(sdkDir, 0o755); err != nil {
		t.Fatal(err)
	}
	ktContent := `package test

class AmityPostRepository {
    fun createPost(title: String): String {
        return title
    }
}
`
	ktPath := filepath.Join(sdkDir, "AmityPostRepository.kt")
	if err := os.WriteFile(ktPath, []byte(ktContent), 0o644); err != nil {
		t.Fatal(err)
	}

	cfgContent := "sdks:\n  android:\n    path: sdk/android\n    snippet_dir: src\n    compile_cmd: []\ndocs:\n  path: .\nllm:\n  model: test\n"
	cfgPath := filepath.Join(dir, "harness-config.yml")
	if err := os.WriteFile(cfgPath, []byte(cfgContent), 0o644); err != nil {
		t.Fatal(err)
	}

	relPath := "src/AmityPostRepository.kt"
	finding := report.Finding{
		ID:       "public-func-unannotated:android:" + relPath + ":createPost",
		Type:     report.TypePublicFuncUnannotated,
		Platform: "android",
		Detail:   "Public function 'createPost' in AmityPostRepository (" + relPath + ") has no begin_public_function annotation",
		Status:   report.StatusOpen,
	}
	rep := report.Report{
		GeneratedAt: "2024-01-01T00:00:00Z",
		Findings:    []report.Finding{finding},
	}
	repBytes, _ := json.Marshal(rep)
	if err := os.WriteFile(filepath.Join(dir, "harness-report.json"), repBytes, 0o644); err != nil {
		t.Fatal(err)
	}

	outPath := filepath.Join(dir, "annotation-patches.yml")

	runAnnotate([]string{
		"--config", cfgPath,
		"--out", outPath,
		"--apply",
	})

	got, err := os.ReadFile(ktPath)
	if err != nil {
		t.Fatalf("read modified kt file: %v", err)
	}
	content := string(got)

	if !strings.Contains(content, "begin_public_function") {
		t.Errorf("modified file does not contain 'begin_public_function':\n%s", content)
	}
	if !strings.Contains(content, "end_public_function") {
		t.Errorf("modified file does not contain 'end_public_function':\n%s", content)
	}

	// begin_public_function must appear before fun createPost
	beginIdx := strings.Index(content, "begin_public_function")
	funcIdx := strings.Index(content, "fun createPost")
	if beginIdx == -1 || funcIdx == -1 || beginIdx > funcIdx {
		t.Errorf("begin_public_function (%d) should appear before fun createPost (%d)", beginIdx, funcIdx)
	}

	// end_public_function must appear after fun createPost
	endIdx := strings.Index(content, "end_public_function")
	if endIdx == -1 || endIdx < funcIdx {
		t.Errorf("end_public_function (%d) should appear after fun createPost (%d)", endIdx, funcIdx)
	}
}
