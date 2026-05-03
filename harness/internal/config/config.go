package config

import (
	"fmt"
	"os"

	"gopkg.in/yaml.v3"
)

type SDKConfig struct {
	Path           string   `yaml:"path"`
	SnippetDir     string   `yaml:"snippet_dir"`
	CompileCmd     []string `yaml:"compile_cmd"`
	BaselineCommit string   `yaml:"baseline_commit,omitempty"`
}

type DocsConfig struct {
	Path  string `yaml:"path"`
	Scope string `yaml:"scope"` // optional path prefix filter, e.g. "social-plus-sdk"
}

type LLMConfig struct {
	Model string `yaml:"model"`
}

type Config struct {
	SDKs map[string]SDKConfig `yaml:"sdks"`
	Docs DocsConfig           `yaml:"docs"`
	LLM  LLMConfig            `yaml:"llm"`
}

// Save writes the config back to path using YAML marshalling.
// Existing comments in the file are not preserved.
func (c *Config) Save(path string) error {
	data, err := yaml.Marshal(c)
	if err != nil {
		return fmt.Errorf("marshal config: %w", err)
	}
	return os.WriteFile(path, data, 0o644)
}

func Load(path string) (*Config, error) {
	b, err := os.ReadFile(path)
	if err != nil {
		return nil, fmt.Errorf("read config %s: %w", path, err)
	}
	var cfg Config
	if err := yaml.Unmarshal(b, &cfg); err != nil {
		return nil, fmt.Errorf("parse config: %w", err)
	}
	return &cfg, nil
}
