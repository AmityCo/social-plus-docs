// cmd/serve.go
package main

import (
	_ "embed"
	"errors"
	"flag"
	"fmt"
	"net/http"
	"os"
	"path/filepath"
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
