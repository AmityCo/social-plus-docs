package manifest

import (
	"testing"
	"os"
	"strings"
)

func TestFillFromSnippets_SingleSection(t *testing.T) {
	m := &Manifest{Sections: map[string]Section{
		"setup": {Heading: "### Setup", Snippets: []string{}},
	}}
	n := FillFromSnippets(m, []string{"client-login", "client-logout"})
	if n != 2 {
		t.Fatalf("want 2 assigned, got %d", n)
	}
	got := m.Sections["setup"].Snippets
	if len(got) != 2 || got[0] != "client-login" || got[1] != "client-logout" {
		t.Errorf("unexpected snippets: %v", got)
	}
}

func TestFillFromSnippets_KeywordMatch(t *testing.T) {
	m := &Manifest{Sections: map[string]Section{
		"login-user":  {Heading: "### Login User", Snippets: []string{}},
		"logout-user": {Heading: "### Logout User", Snippets: []string{}},
	}}
	n := FillFromSnippets(m, []string{"client-login", "client-logout"})
	if n != 2 {
		t.Fatalf("want 2 assigned, got %d", n)
	}
	if got := m.Sections["login-user"].Snippets; len(got) != 1 || got[0] != "client-login" {
		t.Errorf("login-user: want [client-login], got %v", got)
	}
	if got := m.Sections["logout-user"].Snippets; len(got) != 1 || got[0] != "client-logout" {
		t.Errorf("logout-user: want [client-logout], got %v", got)
	}
}

func TestFillFromSnippets_NoMatch(t *testing.T) {
	m := &Manifest{Sections: map[string]Section{
		"section-alpha": {Heading: "### Alpha", Snippets: []string{}},
		"section-beta":  {Heading: "### Beta", Snippets: []string{}},
	}}
	n := FillFromSnippets(m, []string{"unrelated-xyz-key"})
	if n != 0 {
		t.Fatalf("want 0 assigned, got %d", n)
	}
}

func TestFillFromSnippets_SkipExisting(t *testing.T) {
	m := &Manifest{Sections: map[string]Section{
		"setup": {Heading: "### Setup", Snippets: []string{"client-login"}},
	}}
	n := FillFromSnippets(m, []string{"client-login"})
	if n != 0 {
		t.Fatalf("want 0 assigned (already exists), got %d", n)
	}
}

func TestFillFromSnippets_EmptyManifest(t *testing.T) {
	m := &Manifest{Sections: map[string]Section{}}
	n := FillFromSnippets(m, []string{"client-login"})
	if n != 0 {
		t.Fatalf("want 0 (no sections), got %d", n)
	}
}

func TestFillFromSnippets_TieBreak(t *testing.T) {
	// Both "login-admin" and "login-user" score 1 for "client-login" (word "login")
	// Sort makes "login-admin" win (lexicographically first)
	m := &Manifest{Sections: map[string]Section{
		"login-admin": {Heading: "### Login Admin", Snippets: []string{}},
		"login-user":  {Heading: "### Login User", Snippets: []string{}},
	}}
	n := FillFromSnippets(m, []string{"client-login"})
	if n != 1 {
		t.Fatalf("want 1 assigned, got %d", n)
	}
	// "login-admin" < "login-user" lexicographically — must win the tie
	if got := m.Sections["login-admin"].Snippets; len(got) != 1 || got[0] != "client-login" {
		t.Errorf("expected tie broken to login-admin, got login-admin=%v login-user=%v",
			m.Sections["login-admin"].Snippets, m.Sections["login-user"].Snippets)
	}
}

func TestFillFromSnippets_PageHintFallback(t *testing.T) {
	// Generic section names → phase-1 scores 0. Page hints should drive assignment.
	m := &Manifest{Sections: map[string]Section{
		"implementation-example":  {Heading: "### Implementation Example", Snippets: []string{}},
		"implementation-examples": {Heading: "### Implementation Examples", Snippets: []string{}},
	}}
	candidates := []string{
		"create_audio_message", // matches hint "audio"
		"message-audio-creation", // matches hint "audio"
		"channel-create",          // no hint match → excluded
	}
	hints := PageHintsFromPath("social-plus-sdk/chat/message-creation/audio-message")
	n := FillFromSnippets(m, candidates, hints...)
	if n != 2 {
		t.Fatalf("want 2 assigned via hint fallback, got %d", n)
	}
	// Both audio-matching candidates get assigned: first to "implementation-example",
	// second to "implementation-examples" (since the first section is no longer empty).
	if m.Sections["implementation-example"].Snippets[0] != "create_audio_message" {
		t.Errorf("implementation-example: want [create_audio_message], got %v",
			m.Sections["implementation-example"].Snippets)
	}
	if m.Sections["implementation-examples"].Snippets[0] != "message-audio-creation" {
		t.Errorf("implementation-examples: want [message-audio-creation], got %v",
			m.Sections["implementation-examples"].Snippets)
	}
	// channel-create should not appear anywhere
	for _, sec := range m.Sections {
		for _, s := range sec.Snippets {
			if s == "channel-create" {
				t.Errorf("channel-create should not be assigned (no hint match)")
			}
		}
	}
}

func TestPageHintsFromPath(t *testing.T) {
	tests := []struct {
		path  string
		want  []string
	}{
		{"social-plus-sdk/chat/message-creation/audio-message", []string{"message", "creation", "audio"}},
		{"social-plus-sdk/getting-started/authentication", []string{"getting", "started", "authentication"}},
		{"uikit/components/social/communities", []string{"social", "communities"}},
		{"single", []string{"single"}},
	}
	for _, tt := range tests {
		got := PageHintsFromPath(tt.path)
		if len(got) != len(tt.want) {
			t.Errorf("PageHintsFromPath(%q): want %v, got %v", tt.path, tt.want, got)
			continue
		}
		for i, w := range tt.want {
			if got[i] != w {
				t.Errorf("PageHintsFromPath(%q)[%d]: want %q, got %q", tt.path, i, w, got[i])
			}
		}
	}
}

func TestSaveManifest_RoundTrip(t *testing.T) {
	dir := t.TempDir()
	m := &Manifest{Sections: map[string]Section{
		"setup": {Heading: "### Setup", Snippets: []string{"client-login"}},
	}}
	if err := SaveManifest(dir, "sdk/auth", m); err != nil {
		t.Fatal(err)
	}
	got, found, err := LoadForPage(dir, "sdk/auth")
	if err != nil || !found {
		t.Fatalf("LoadForPage: err=%v found=%v", err, found)
	}
	if sec := got.Sections["setup"]; len(sec.Snippets) != 1 || sec.Snippets[0] != "client-login" {
		t.Errorf("unexpected section: %+v", sec)
	}
	raw, _ := os.ReadFile(PathForPage(dir, "sdk/auth"))
	if !strings.HasPrefix(string(raw), "# AUTO-GENERATED") {
		t.Error("missing AUTO-GENERATED header")
	}
}
