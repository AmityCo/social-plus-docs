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
	"social-plus/harness/internal/publicscan"
	"strings"
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
	mux.Handle("/api/parity", parityHandler(dir))
	mux.Handle("/api/parity/detail", parityDetailHandler(dir))
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

// coverageHandler computes per-platform annotation coverage using publicscan.
// This correctly identifies public API functions per platform (e.g. for TypeScript,
// only files directly in *Repository/api/ or *Client/api/ are counted).
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
			sdkPath := filepath.Join(cfgDir, sdkCfg.Path)

			// Use publicscan.Scan to count public functions, consistent with
			// the PUBLIC_FUNC_UNANNOTATED harness check.
			pubScanDir := sdkPath
			var pubScanExclude []string
			if sdkCfg.SnippetDir != "" && strings.ToLower(platform) != "typescript" {
				pubScanExclude = []string{sdkCfg.SnippetDir}
			} else if strings.ToLower(platform) == "typescript" && sdkCfg.SnippetDir != "" {
				pubScanDir = filepath.Join(sdkPath, sdkCfg.SnippetDir)
			}

			pubFuncs, err := publicscan.Scan(pubScanDir, platform, pubScanExclude...)
			if err != nil {
				pubFuncs = nil
			}

			total := len(pubFuncs)
			annotated := 0
			for _, pf := range pubFuncs {
				if pf.IsAnnotated {
					annotated++
				}
			}

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

// parityPlatformRow is one row in the /api/parity response.
type parityPlatformRow struct {
	Platform string  `json:"platform"`
	Exists   int     `json:"exists"`
	Total    int     `json:"total"`
	Percent  float64 `json:"percent"`
}

// paritySummaryResponse is the full /api/parity JSON response.
type paritySummaryResponse struct {
	TotalKeys int                 `json:"total_keys"`
	Platforms []parityPlatformRow `json:"platforms"`
}

// parityHandler reads function-parity.json and returns per-platform exists/total counts.
func parityHandler(dir string) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		data, err := os.ReadFile(filepath.Join(dir, "function-parity.json"))
		if errors.Is(err, os.ErrNotExist) {
			_, _ = w.Write([]byte(`{"total_keys":0,"platforms":[]}`))
			return
		}
		if err != nil {
			http.Error(w, "read error", http.StatusInternalServerError)
			return
		}
		// Minimal decode — only the fields we need.
		var raw struct {
			TotalKeys    int      `json:"total_keys"`
			AllPlatforms []string `json:"platforms"`
			Functions    []struct {
				Platforms map[string]struct {
					Status string `json:"status"`
				} `json:"platforms"`
			} `json:"functions"`
		}
		if err := json.Unmarshal(data, &raw); err != nil {
			http.Error(w, "parse error", http.StatusInternalServerError)
			return
		}
		// Count exists per platform.
		counts := make(map[string]int, len(raw.AllPlatforms))
		for _, fn := range raw.Functions {
			for p, pe := range fn.Platforms {
				if pe.Status == "exists" {
					counts[p]++
				}
			}
		}
		rows := make([]parityPlatformRow, 0, len(raw.AllPlatforms))
		for _, p := range raw.AllPlatforms {
			exists := counts[p]
			var pct float64
			if raw.TotalKeys > 0 {
				pct = float64(exists) / float64(raw.TotalKeys) * 100
			}
			rows = append(rows, parityPlatformRow{
				Platform: p,
				Exists:   exists,
				Total:    raw.TotalKeys,
				Percent:  pct,
			})
		}
		resp := paritySummaryResponse{TotalKeys: raw.TotalKeys, Platforms: rows}
		enc := json.NewEncoder(w)
		enc.SetIndent("", "  ")
		_ = enc.Encode(resp)
	})
}

// parityDetailResponse is the full per-function parity data for the table page.
type parityDetailFunction struct {
	Key        string            `json:"key"`
	SpDocsPage string            `json:"sp_docs_page"`
	Platforms  map[string]string `json:"platforms"` // platform -> "exists" or "unknown"
	Coverage   int               `json:"coverage"`
}

type parityDetailResponse struct {
	TotalKeys    int                    `json:"total_keys"`
	AllPlatforms []string               `json:"platforms"`
	Functions    []parityDetailFunction `json:"functions"`
}

// parityDetailHandler returns full function-level parity data for the comparison table.
func parityDetailHandler(dir string) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		data, err := os.ReadFile(filepath.Join(dir, "function-parity.json"))
		if errors.Is(err, os.ErrNotExist) {
			_, _ = w.Write([]byte(`{"total_keys":0,"platforms":[],"functions":[]}`))
			return
		}
		if err != nil {
			http.Error(w, "read error", http.StatusInternalServerError)
			return
		}
		var raw struct {
			TotalKeys    int      `json:"total_keys"`
			AllPlatforms []string `json:"platforms"`
			Functions    []struct {
				Key        string `json:"key"`
				SpDocsPage string `json:"sp_docs_page"`
				Coverage   int    `json:"coverage"`
				Platforms  map[string]struct {
					Status string `json:"status"`
				} `json:"platforms"`
			} `json:"functions"`
		}
		if err := json.Unmarshal(data, &raw); err != nil {
			http.Error(w, "parse error", http.StatusInternalServerError)
			return
		}
		fns := make([]parityDetailFunction, 0, len(raw.Functions))
		for _, fn := range raw.Functions {
			plats := make(map[string]string, len(fn.Platforms))
			for p, pe := range fn.Platforms {
				plats[p] = pe.Status
			}
			fns = append(fns, parityDetailFunction{
				Key:        fn.Key,
				SpDocsPage: fn.SpDocsPage,
				Platforms:  plats,
				Coverage:   fn.Coverage,
			})
		}
		resp := parityDetailResponse{
			TotalKeys:    raw.TotalKeys,
			AllPlatforms: raw.AllPlatforms,
			Functions:    fns,
		}
		enc := json.NewEncoder(w)
		enc.SetIndent("", "  ")
		_ = enc.Encode(resp)
	})
}
