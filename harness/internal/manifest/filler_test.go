package manifest

import (
	"testing"
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
