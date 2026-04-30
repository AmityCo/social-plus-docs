package verifier

import (
	"crypto/sha256"
	"fmt"
	"io"
	"os"

	"social-plus/harness/internal/report"
)

func HashFile(path string) (string, error) {
	f, err := os.Open(path)
	if err != nil {
		return "", fmt.Errorf("open %s: %w", path, err)
	}
	defer f.Close()

	h := sha256.New()
	if _, err := io.Copy(h, f); err != nil {
		return "", err
	}

	return fmt.Sprintf("sha256:%x", h.Sum(nil)), nil
}

func HashBytes(b []byte) string {
	h := sha256.Sum256(b)
	return fmt.Sprintf("sha256:%x", h)
}

// Seal marks a finding as fixed with cryptographic evidence.
// compileResult must be "PASS"; anything else returns an error.
// compileOutputHash is HashBytes(compileStdout+compileStderr).
func Seal(f report.Finding, artifactPath, compileResult, compileOutputHash string) (report.Finding, error) {
	if compileResult != "PASS" {
		return f, fmt.Errorf("compile did not pass: %s", compileResult)
	}

	afterHash, err := HashFile(artifactPath)
	if err != nil {
		return f, fmt.Errorf("hash artifact: %w", err)
	}

	f.Status = report.StatusFixed
	f.Evidence = &report.Evidence{
		AfterHash:         afterHash,
		Artifact:          artifactPath,
		CompileResult:     compileResult,
		CompileOutputHash: compileOutputHash,
	}
	return f, nil
}

// Verify re-checks the evidence bundle against the artifact on disk.
// Returns (true, "") if valid, (false, reason) if tampered or missing.
func Verify(f report.Finding, artifactPath string) (bool, string) {
	if f.Evidence == nil {
		return false, "no evidence bundle"
	}

	currentHash, err := HashFile(artifactPath)
	if err != nil {
		return false, fmt.Sprintf("cannot hash artifact: %v", err)
	}
	if currentHash != f.Evidence.AfterHash {
		return false, fmt.Sprintf("hash mismatch: expected %s, got %s", f.Evidence.AfterHash, currentHash)
	}
	return true, ""
}
