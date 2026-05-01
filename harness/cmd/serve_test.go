// cmd/serve_test.go
package main

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"os"
	"path/filepath"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestServeReport_ReturnsJSON(t *testing.T) {
	dir := t.TempDir()
	payload := `{"generated_at":"2026-05-01T00:00:00Z","findings":[]}`
	require.NoError(t, os.WriteFile(filepath.Join(dir, "harness-report.json"), []byte(payload), 0o644))

	h := reportHandler(dir)
	rec := httptest.NewRecorder()
	h.ServeHTTP(rec, httptest.NewRequest("GET", "/api/report", nil))

	assert.Equal(t, http.StatusOK, rec.Code)
	assert.Equal(t, "application/json", rec.Header().Get("Content-Type"))
	var got map[string]any
	require.NoError(t, json.Unmarshal(rec.Body.Bytes(), &got))
	assert.Equal(t, "2026-05-01T00:00:00Z", got["generated_at"])
}

func TestServeReport_NotFound_Returns200Empty(t *testing.T) {
	dir := t.TempDir()
	h := reportHandler(dir)
	rec := httptest.NewRecorder()
	h.ServeHTTP(rec, httptest.NewRequest("GET", "/api/report", nil))
	assert.Equal(t, http.StatusOK, rec.Code)
	assert.JSONEq(t, `{}`, rec.Body.String())
}

func TestServeRun_ReturnsJSON(t *testing.T) {
	dir := t.TempDir()
	payload := `{"session_id":"abc","current_command":"audit","steps":[]}`
	require.NoError(t, os.WriteFile(filepath.Join(dir, "harness-run.json"), []byte(payload), 0o644))

	h := runHandler(dir)
	rec := httptest.NewRecorder()
	h.ServeHTTP(rec, httptest.NewRequest("GET", "/api/run", nil))

	assert.Equal(t, http.StatusOK, rec.Code)
	var got map[string]any
	require.NoError(t, json.Unmarshal(rec.Body.Bytes(), &got))
	assert.Equal(t, "audit", got["current_command"])
}

func TestServeRun_NotFound_Returns200Empty(t *testing.T) {
	dir := t.TempDir()
	h := runHandler(dir)
	rec := httptest.NewRecorder()
	h.ServeHTTP(rec, httptest.NewRequest("GET", "/api/run", nil))
	assert.Equal(t, http.StatusOK, rec.Code)
	assert.JSONEq(t, `{}`, rec.Body.String())
}

func TestCorsMiddleware_SetsHeader(t *testing.T) {
	inner := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {})
	h := corsMiddleware(inner)
	rec := httptest.NewRecorder()
	h.ServeHTTP(rec, httptest.NewRequest("GET", "/", nil))
	assert.Equal(t, "*", rec.Header().Get("Access-Control-Allow-Origin"))
}

func TestServeDashboard_Returns200(t *testing.T) {
	rec := httptest.NewRecorder()
	dashboardHandler().ServeHTTP(rec, httptest.NewRequest("GET", "/", nil))
	assert.Equal(t, http.StatusOK, rec.Code)
	assert.Contains(t, rec.Header().Get("Content-Type"), "text/html")
}
