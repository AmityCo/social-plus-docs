package main

import (
	"flag"
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"gopkg.in/yaml.v3"
	"social-plus/harness/internal/config"
	"social-plus/harness/internal/manifest"
	"social-plus/harness/internal/mdxparse"
)

type sectionYAML struct {
	Heading  string   `yaml:"heading"`
	Snippets []string `yaml:"snippets"`
}
type manifestYAML struct {
	Sections map[string]sectionYAML `yaml:"sections"`
}


func runGenManifests(args []string) {
	fs := flag.NewFlagSet("genmanifests", flag.ExitOnError)
	cfgPath := fs.String("config", "harness-config.yml", "path to harness-config.yml")
	dryRun := fs.Bool("dry-run", false, "print what would be written without creating files")
	_ = fs.Parse(args)

	cfg, err := config.Load(*cfgPath)
	if err != nil {
		fmt.Fprintf(os.Stderr, "[genmanifests] failed to load config: %v\n", err)
		os.Exit(1)
	}
	docsBase := cfg.Docs.Path
	if docsBase == "" {
		fmt.Fprintf(os.Stderr, "[genmanifests] docs.path missing in config\n")
		os.Exit(1)
	}

	var mdxFiles []string
	err = filepath.Walk(docsBase, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}
		if info.IsDir() {
			return nil
		}
		if strings.HasSuffix(info.Name(), ".mdx") {
			mdxFiles = append(mdxFiles, path)
		}
		return nil
	})
	if err != nil {
		fmt.Fprintf(os.Stderr, "[genmanifests] error walking docs dir: %v\n", err)
		os.Exit(1)
	}

	for _, mdxPath := range mdxFiles {
		rel, err := filepath.Rel(docsBase, mdxPath)
		if err != nil {
			fmt.Fprintf(os.Stderr, "[genmanifests] error getting rel path: %v\n", err)
			continue
		}
		relSlash := filepath.ToSlash(rel)
		if cfg.Docs.Scope != "" && !strings.HasPrefix(relSlash, cfg.Docs.Scope+"/") {
			continue // outside configured scope
		}
		pagePath := strings.TrimSuffix(rel, ".mdx")
		manifestPath := manifest.PathForPage(docsBase, pagePath)
		if _, err := os.Stat(manifestPath); err == nil {
			continue // manifest exists
		}
		sections, err := mdxparse.ExtractSections(mdxPath)
		if err != nil {
			fmt.Fprintf(os.Stderr, "[genmanifests] error parsing %s: %v\n", mdxPath, err)
			continue
		}
		if len(sections) == 0 {
			continue // no sections, skip
		}
		m := manifestYAML{Sections: map[string]sectionYAML{}}
		for _, sec := range sections {
			m.Sections[sec.Slug] = sectionYAML{Heading: sec.Heading, Snippets: []string{}}
		}
		out, err := yaml.Marshal(&m)
		if err != nil {
			fmt.Fprintf(os.Stderr, "[genmanifests] error marshaling yaml for %s: %v\n", mdxPath, err)
			continue
		}
		if *dryRun {
			fmt.Printf("[genmanifests] DRY RUN: would create %s (%d sections)\n", manifestPath, len(m.Sections))
			continue
		}
		f, err := os.Create(manifestPath)
		if err != nil {
			fmt.Fprintf(os.Stderr, "[genmanifests] error creating %s: %v\n", manifestPath, err)
			continue
		}
		defer f.Close()
		if _, err := f.WriteString(manifest.Header); err != nil {
			fmt.Fprintf(os.Stderr, "[genmanifests] error writing header to %s: %v\n", manifestPath, err)
			continue
		}
		if _, err := f.Write(out); err != nil {
			fmt.Fprintf(os.Stderr, "[genmanifests] error writing yaml to %s: %v\n", manifestPath, err)
			continue
		}
		fmt.Printf("[genmanifests] created %s (%d sections)\n", manifestPath, len(m.Sections))
	}
}
