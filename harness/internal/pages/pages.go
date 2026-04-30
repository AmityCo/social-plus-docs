package pages

import (
	"encoding/json"
	"fmt"
	"os"
)

type Registry struct {
	paths map[string]bool
}

func (r *Registry) Contains(path string) bool {
	return r.paths[path]
}

func (r *Registry) All() []string {
	out := make([]string, 0, len(r.paths))
	for p := range r.paths {
		out = append(out, p)
	}
	return out
}

func Load(docsJSONPath string) (*Registry, error) {
	b, err := os.ReadFile(docsJSONPath)
	if err != nil {
		return nil, fmt.Errorf("read docs.json: %w", err)
	}
	var raw map[string]interface{}
	if err := json.Unmarshal(b, &raw); err != nil {
		return nil, fmt.Errorf("parse docs.json: %w", err)
	}
	reg := &Registry{paths: make(map[string]bool)}
	extract(raw, reg)
	return reg, nil
}

// NewFromPaths creates a Registry from a slice of paths (for testing).
func NewFromPaths(paths []string) *Registry {
	r := &Registry{paths: make(map[string]bool)}
	for _, p := range paths {
		r.paths[p] = true
	}
	return r
}

func extract(v interface{}, reg *Registry) {
	switch val := v.(type) {
	case map[string]interface{}:
		if pages, ok := val["pages"]; ok {
			extractPages(pages, reg)
		}
		for _, child := range val {
			extract(child, reg)
		}
	case []interface{}:
		for _, item := range val {
			extract(item, reg)
		}
	}
}

func extractPages(v interface{}, reg *Registry) {
	switch val := v.(type) {
	case string:
		reg.paths[val] = true
	case []interface{}:
		for _, item := range val {
			switch p := item.(type) {
			case string:
				reg.paths[p] = true
			case map[string]interface{}:
				if nested, ok := p["pages"]; ok {
					extractPages(nested, reg)
				}
			}
		}
	}
}
