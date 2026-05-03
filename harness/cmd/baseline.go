package main

import (
	"flag"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strings"

	"social-plus/harness/internal/config"
)

func runBaseline(args []string) {
	fs := flag.NewFlagSet("baseline", flag.ExitOnError)
	cfgPath := fs.String("config", "harness-config.yml", "path to harness-config.yml")
	if err := fs.Parse(args); err != nil {
		fmt.Fprintf(os.Stderr, "parse flags: %v\n", err)
		os.Exit(1)
	}

	cfg, err := config.Load(*cfgPath)
	if err != nil {
		fmt.Fprintf(os.Stderr, "load config: %v\n", err)
		os.Exit(1)
	}

	cfgDir := filepath.Dir(*cfgPath)
	updated := false
	for platform, sdkCfg := range cfg.SDKs {
		sdkPath := filepath.Join(cfgDir, sdkCfg.Path)
		if _, err := os.Stat(sdkPath); os.IsNotExist(err) {
			fmt.Printf("[baseline] skip %s: path not found\n", platform)
			continue
		}
		cmd := exec.Command("git", "rev-parse", "HEAD")
		cmd.Dir = sdkPath
		out, err := cmd.Output()
		if err != nil {
			fmt.Fprintf(os.Stderr, "[baseline] git rev-parse HEAD in %s: %v\n", sdkPath, err)
			continue
		}
		commit := strings.TrimSpace(string(out))
		sdkCfg.BaselineCommit = commit
		cfg.SDKs[platform] = sdkCfg
		if len(commit) >= 12 {
			fmt.Printf("[baseline] %s → %s\n", platform, commit[:12])
		} else {
			fmt.Printf("[baseline] %s → %s\n", platform, commit)
		}
		updated = true
	}

	if !updated {
		fmt.Println("[baseline] no SDKs updated")
		return
	}

	if err := cfg.Save(*cfgPath); err != nil {
		fmt.Fprintf(os.Stderr, "save config: %v\n", err)
		os.Exit(1)
	}
	fmt.Printf("[baseline] saved to %s\n", *cfgPath)
}
