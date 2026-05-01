// cmd/serve.go
package main

import (
	_ "embed"
	"encoding/json"
	"errors"
	"flag"
	"fmt"
	"net/http"
	"os"
	"path/filepath"
	"sort"

	"social-plus/harness/internal/config"
	"social-plus/harness/internal/scanner"
)

//go:embed dashboard.html
var dashboardHTML []byte

func runServe(args []string) {
	fs := flag.NewFlagSet("serve", flag.ExitOnError)
	cfgPath := fs.String("config", "harness-config.yml", "path to harness-config.yml")
	port := fs.String("port", "8765", "port to listen on")
	_ = fs.Parse(args)

	dir := filepath.Dir(*cfgPath)

	mux := http.NewServeMux()
	mux.Handle("/api/report", reportHandler(dir))
	mux.Handle("/api/run", runHandler(dir))
	mux.Handle("/api/coverage", coverageHandler(*cfgPath))
	mux.Handle("/", dashboardHandler())

	addr := "localhost:" + *port
	fmt.Printf("[serve] Dashboard at http://%s\n", addr)
	fmt.Printf("[serve] Reading from %s\n", dir)
	fmt.Println("[serve] Ctrl-C to stop")
	if err := http.ListenAndServe(addr, corsMiddleware(mux)); err != nil {
		fmt.Fprintf(os.Stderr, "serve: %v\n", err)
		os.Exit(1)
	}
}

// reportHandler serves harness-report.json as JSON.
func reportHandler(dir string) http.Handler { return jsonFileHandler(dir, "harness-report.json") }

// runHandler serves harness-run.json as JSON.
func runHandler(dir string) http.Handler { return jsonFileHandler(dir, "harness-run.json") }

// jsonFileHandler returns a handler that reads filename from dir and writes it as JSON.
// Returns {} (200 OK) if the file doesn't exist; logs and returns {} on other I/O errors.
func jsonFileHandler(dir, filename string) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		data, err := os.ReadFile(filepath.Join(dir, filename))
		if errors.Is(err, os.ErrNotExist) {
			_, _ = w.Write([]byte("{}"))
			return
		}
		if err != nil {
			fmt.Fprintf(os.Stderr, "serve: reading %s: %v\n", filepath.Join(dir, filename), err)
			_, _ = w.Write([]byte("{}"))
			return
		}
		_, _ = w.Write(data)
	})
}

// dashboardHandler serves the embedded dashboard HTML.
func dashboardHandler() http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "text/html; charset=utf-8")
		_, _ = w.Write(dashboardHTML)
	})
}

// corsMiddleware adds permissive CORS headers so dashboard.html works from file://.
func corsMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Access-Control-Allow-Origin", "*")
		next.ServeHTTP(w, r)
	})
}

// coveragePlatform is a single row in the /api/coverage response.
type coveragePlatform struct {
	Platform  string  `json:"platform"`
	Annotated int     `json:"annotated"`
	Total     int     `json:"total"`
	Percent   float64 `json:"percent"`
}

// coverageResponse is the full /api/coverage JSON response.
type coverageResponse struct {
	Platforms []coveragePlatform `json:"platforms"`
}

// coverageHandler computes per-platform annotation coverage from the SDK snippet dirs.
func coverageHandler(cfgPath string) http.Handler {
	cfg, loadErr := config.Load(cfgPath)
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		if loadErr != nil {
			http.Error(w, "config load error", http.StatusInternalServerError)
			return
		}
		cfgDir := filepath.Dir(cfgPath)

		platforms := make([]string, 0, len(cfg.SDKs))
		for p := range cfg.SDKs {
			platforms = append(platforms, p)
		}
		sort.Strings(platforms)

		rows := make([]coveragePlatform, 0, len(platforms))
		for _, platform := range platforms {
			sdkCfg := cfg.SDKs[platform]
			snippetPath := filepath.Join(cfgDir, sdkCfg.Path, sdkCfg.SnippetDir)

			// Count total platform-matching source files in the snippet dir.
			total := 0
			_ = filepath.WalkDir(snippetPath, func(path string, d os.DirEntry, err error) error {
				if err != nil || d.IsDir() {
					return nil //nolint:nilerr
				}
				if matchesExt(path, platform) {
					total++
				}
				return nil
			})

			// Count files that have at least one annotated snippet.
			snippets, err := scanner.Scan(snippetPath, platform)
			if err != nil {
				snippets = nil
			}
			annotatedSet := make(map[string]struct{}, len(snippets))
			for _, s := range snippets {
				annotatedSet[s.File] = struct{}{}
			}
			annotated := len(annotatedSet)

			var pct float64
			if total > 0 {
				pct = float64(annotated) / float64(total) * 100
			}
			rows = append(rows, coveragePlatform{
				Platform:  platform,
				Annotated: annotated,
				Total:     total,
				Percent:   pct,
			})
		}

		resp := coverageResponse{Platforms: rows}
		enc := json.NewEncoder(w)
		enc.SetIndent("", "  ")
		_ = enc.Encode(resp)
	})
}

// matchesExt returns true when path has a file extension appropriate for platform.
func matchesExt(path, platform string) bool {
	switch platform {
	case "android":
		return hasSuffix(path, ".kt", ".java")
	case "ios":
		return hasSuffix(path, ".swift")
	case "flutter":
		return hasSuffix(path, ".dart")
	case "typescript":
		return hasSuffix(path, ".ts", ".tsx")
	default:
		return false
	}
}

func hasSuffix(s string, suffixes ...string) bool {
	for _, suf := range suffixes {
		if len(s) >= len(suf) && s[len(s)-len(suf):] == suf {
			return true
		}
	}
	return false
}
