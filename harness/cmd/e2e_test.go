//go:build e2e

package main

import (
	"io"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"testing"
	"time"
)

func TestE2EServeDashboard(t *testing.T) {
	// Build binary
	bin := filepath.Join(t.TempDir(), "harness-bin-e2e")
	if err := exec.Command("go", "build", "-o", bin, ".").Run(); err != nil {
		t.Fatalf("build: %v", err)
	}

	// Write minimal config
	dir := t.TempDir()
	cfgPath := filepath.Join(dir, "harness-config.yml")
	if err := os.WriteFile(cfgPath, []byte("sdks: {}\ndocs:\n  path: .\nllm:\n  model: test\n"), 0o644); err != nil {
		t.Fatal(err)
	}

	// Start server
	cmd := exec.Command(bin, "serve", "--config", cfgPath, "--port", "18765")
	if err := cmd.Start(); err != nil {
		t.Fatalf("start serve: %v", err)
	}
	defer cmd.Process.Kill()

	// Wait for server to be ready
	deadline := time.Now().Add(5 * time.Second)
	var resp *http.Response
	var err error
	for time.Now().Before(deadline) {
		resp, err = http.Get("http://localhost:18765/")
		if err == nil {
			break
		}
		time.Sleep(100 * time.Millisecond)
	}
	if err != nil {
		t.Fatalf("server not ready: %v", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != 200 {
		t.Errorf("expected 200, got %d", resp.StatusCode)
	}

	body, _ := io.ReadAll(resp.Body)
	if !strings.Contains(strings.ToLower(string(body)), "harness") {
		t.Errorf("response body does not contain 'harness'")
	}
}
