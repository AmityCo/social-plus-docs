package paritymap

import (
	"encoding/json"
	"os"
	"sort"
	"time"

	"social-plus/harness/internal/docgen"
	"social-plus/harness/internal/scanner"
)

type PlatformStatus string

const (
	StatusExists  PlatformStatus = "exists"
	StatusUnknown PlatformStatus = "unknown"
)

type PlatformEntry struct {
	Status PlatformStatus `json:"status"`
	File   string         `json:"file,omitempty"`
}

type FunctionEntry struct {
	Key        string                   `json:"key"`
	SpDocsPage string                   `json:"sp_docs_page"`
	Platforms  map[string]PlatformEntry `json:"platforms"`
	Coverage   int                      `json:"coverage"`
	Total      int                      `json:"total_platforms"`
}

type ParityMap struct {
	GeneratedAt  time.Time       `json:"generated_at"`
	TotalKeys    int             `json:"total_keys"`
	AllPlatforms []string        `json:"platforms"`
	Functions    []FunctionEntry `json:"functions"`
}

// Build constructs a ParityMap from snippets grouped by docgen.DeriveKey.
func Build(snips []scanner.Snippet, platforms []string) ParityMap {
	type intermediate struct {
		spDocsPage map[string]string // platform -> SpDocsPage
		files      map[string]string // platform -> File
	}

	grouped := map[string]*intermediate{}

	for _, s := range snips {
		key := docgen.DeriveKey(s.Filename)
		if _, ok := grouped[key]; !ok {
			grouped[key] = &intermediate{
				spDocsPage: map[string]string{},
				files:      map[string]string{},
			}
		}
		grouped[key].spDocsPage[s.Platform] = s.SpDocsPage
		grouped[key].files[s.Platform] = s.File
	}

	funcs := make([]FunctionEntry, 0, len(grouped))
	for key, data := range grouped {
		// Determine sp_docs_page: android wins, else first found.
		spDocsPage := ""
		if p, ok := data.spDocsPage["android"]; ok {
			spDocsPage = p
		} else {
			for _, p := range platforms {
				if v, ok := data.spDocsPage[p]; ok {
					spDocsPage = v
					break
				}
			}
		}

		entries := make(map[string]PlatformEntry, len(platforms))
		coverage := 0
		for _, p := range platforms {
			if f, ok := data.files[p]; ok {
				entries[p] = PlatformEntry{Status: StatusExists, File: f}
				coverage++
			} else {
				entries[p] = PlatformEntry{Status: StatusUnknown}
			}
		}

		funcs = append(funcs, FunctionEntry{
			Key:        key,
			SpDocsPage: spDocsPage,
			Platforms:  entries,
			Coverage:   coverage,
			Total:      len(platforms),
		})
	}

	sort.Slice(funcs, func(i, j int) bool {
		return funcs[i].Key < funcs[j].Key
	})

	return ParityMap{
		GeneratedAt:  time.Now().UTC(),
		TotalKeys:    len(funcs),
		AllPlatforms: platforms,
		Functions:    funcs,
	}
}

// Write encodes pm as indented JSON and writes it to path.
func Write(path string, pm ParityMap) error {
	f, err := os.Create(path)
	if err != nil {
		return err
	}
	defer f.Close()

	enc := json.NewEncoder(f)
	enc.SetIndent("", "  ")
	return enc.Encode(pm)
}

// Read decodes a ParityMap from the JSON file at path.
func Read(path string) (ParityMap, error) {
	f, err := os.Open(path)
	if err != nil {
		return ParityMap{}, err
	}
	defer f.Close()

	var pm ParityMap
	if err := json.NewDecoder(f).Decode(&pm); err != nil {
		return ParityMap{}, err
	}
	return pm, nil
}

// Confidence returns "high", "medium", or "low" based on how many platforms
// (excluding selfPlatform) have StatusExists for the given key.
func (pm ParityMap) Confidence(key, selfPlatform string) string {
	for _, fn := range pm.Functions {
		if fn.Key != key {
			continue
		}
		count := 0
		for p, entry := range fn.Platforms {
			if p != selfPlatform && entry.Status == StatusExists {
				count++
			}
		}
		if count >= 2 {
			return "high"
		}
		if count == 1 {
			return "medium"
		}
		return "low"
	}
	return "low"
}
