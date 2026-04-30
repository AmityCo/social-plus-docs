package compiler

import (
"bytes"
"crypto/sha256"
"fmt"
"os/exec"

"social-plus/harness/internal/config"
)

// Run executes the SDK's compile command from workDir.
// Returns ("PASS"|"FAIL", sha256 of combined stdout+stderr, error).
// error is only non-nil for exec setup failures (command not found, etc.),
// not for non-zero exit codes.
func Run(workDir string, cfg config.SDKConfig) (string, string, error) {
if len(cfg.CompileCmd) == 0 {
return "PASS", hashBytes(nil), nil
}
cmd := exec.Command(cfg.CompileCmd[0], cfg.CompileCmd[1:]...)
cmd.Dir = workDir
var out bytes.Buffer
cmd.Stdout = &out
cmd.Stderr = &out

err := cmd.Run()
outHash := hashBytes(out.Bytes())

if err != nil {
if _, ok := err.(*exec.ExitError); ok {
fmt.Printf("  compile output:\n%s\n", out.String())
return "FAIL", outHash, nil
}
return "FAIL", outHash, fmt.Errorf("exec: %w", err)
}
return "PASS", outHash, nil
}

func hashBytes(b []byte) string {
h := sha256.Sum256(b)
return fmt.Sprintf("sha256:%x", h)
}
