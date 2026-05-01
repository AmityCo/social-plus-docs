package paritymap_test

import (
	"testing"
	"time"

	"social-plus/harness/internal/paritymap"
	"social-plus/harness/internal/scanner"
)

func TestBuild_Basic(t *testing.T) {
	snips := []scanner.Snippet{
		{Filename: "AmityPostRepository.kt", SpDocsPage: "/social-plus-sdk/post/create", Platform: "android", File: "path/to/android.kt"},
		{Filename: "AmityPostRepository.swift", SpDocsPage: "/social-plus-sdk/post/create", Platform: "ios", File: "path/to/ios.swift"},
	}
	pm := paritymap.Build(snips, []string{"android", "ios", "flutter", "typescript"})
	if pm.TotalKeys != 1 {
		t.Fatalf("want 1 key, got %d", pm.TotalKeys)
	}
	fn := pm.Functions[0]
	if fn.Key != "post-repository" {
		t.Errorf("want key=post-repository, got %s", fn.Key)
	}
	if fn.Platforms["android"].Status != paritymap.StatusExists {
		t.Errorf("android should be exists")
	}
	if fn.Platforms["flutter"].Status != paritymap.StatusUnknown {
		t.Errorf("flutter should be unknown")
	}
	if fn.Coverage != 2 {
		t.Errorf("want coverage=2, got %d", fn.Coverage)
	}
	if fn.Total != 4 {
		t.Errorf("want total=4, got %d", fn.Total)
	}
}

func TestBuild_SortedOutput(t *testing.T) {
	snips := []scanner.Snippet{
		{Filename: "AmityZZZ.kt", SpDocsPage: "/p/zzz", Platform: "android"},
		{Filename: "AmityAAA.kt", SpDocsPage: "/p/aaa", Platform: "android"},
	}
	pm := paritymap.Build(snips, []string{"android"})
	if len(pm.Functions) < 2 {
		t.Fatal("need at least 2 functions")
	}
	if pm.Functions[0].Key >= pm.Functions[1].Key {
		t.Errorf("functions should be sorted by key: got %s, %s", pm.Functions[0].Key, pm.Functions[1].Key)
	}
}

func TestBuild_GeneratedAtSet(t *testing.T) {
	before := time.Now()
	pm := paritymap.Build(nil, []string{"android"})
	after := time.Now()
	if pm.GeneratedAt.Before(before) || pm.GeneratedAt.After(after) {
		t.Errorf("GeneratedAt out of expected range")
	}
}

func TestBuild_MultiPlatform(t *testing.T) {
	snips := []scanner.Snippet{
		{Filename: "AmityLogin.kt", SpDocsPage: "/p/auth", Platform: "android"},
		{Filename: "AmityLogin.swift", SpDocsPage: "/p/auth", Platform: "ios"},
		{Filename: "AmityLogin.dart", SpDocsPage: "/p/auth", Platform: "flutter"},
		{Filename: "AmityLogin.ts", SpDocsPage: "/p/auth", Platform: "typescript"},
	}
	pm := paritymap.Build(snips, []string{"android", "ios", "flutter", "typescript"})
	if pm.TotalKeys != 1 {
		t.Fatalf("want 1 key, got %d", pm.TotalKeys)
	}
	if pm.Functions[0].Coverage != 4 {
		t.Errorf("want coverage=4, got %d", pm.Functions[0].Coverage)
	}
}

func TestConfidence(t *testing.T) {
	snips := []scanner.Snippet{
		{Filename: "AmityLogin.kt", SpDocsPage: "/p/auth", Platform: "android"},
		{Filename: "AmityLogin.swift", SpDocsPage: "/p/auth", Platform: "ios"},
		{Filename: "AmityLogin.dart", SpDocsPage: "/p/auth", Platform: "flutter"},
	}
	pm := paritymap.Build(snips, []string{"android", "ios", "flutter", "typescript"})
	// from android's POV: ios+flutter exist = high
	if got := pm.Confidence("login", "android"); got != "high" {
		t.Errorf("want high, got %s", got)
	}
	// from typescript's POV: android+ios+flutter exist = high
	if got := pm.Confidence("login", "typescript"); got != "high" {
		t.Errorf("want high from typescript, got %s", got)
	}
}

func TestConfidence_Medium(t *testing.T) {
	snips := []scanner.Snippet{
		{Filename: "AmityFoo.kt", SpDocsPage: "/p/foo", Platform: "android"},
		{Filename: "AmityFoo.swift", SpDocsPage: "/p/foo", Platform: "ios"},
	}
	pm := paritymap.Build(snips, []string{"android", "ios", "flutter", "typescript"})
	// from android's POV: only ios exists = medium
	if got := pm.Confidence("foo", "android"); got != "medium" {
		t.Errorf("want medium, got %s", got)
	}
}

func TestConfidence_Low(t *testing.T) {
	snips := []scanner.Snippet{
		{Filename: "AmityBar.kt", SpDocsPage: "/p/bar", Platform: "android"},
	}
	pm := paritymap.Build(snips, []string{"android", "ios", "flutter", "typescript"})
	// from android's POV: no siblings = low
	if got := pm.Confidence("bar", "android"); got != "low" {
		t.Errorf("want low, got %s", got)
	}
}
