package compiler_test

import (
"testing"

"github.com/stretchr/testify/assert"
"github.com/stretchr/testify/require"
"social-plus/harness/internal/compiler"
"social-plus/harness/internal/config"
)

func TestRunSuccess(t *testing.T) {
cfg := config.SDKConfig{
CompileCmd: []string{"echo", "build ok"},
}
result, outHash, err := compiler.Run("/tmp", cfg)
require.NoError(t, err)
assert.Equal(t, "PASS", result)
assert.NotEmpty(t, outHash)
}

func TestRunFailure(t *testing.T) {
cfg := config.SDKConfig{
CompileCmd: []string{"false"}, // always exits non-zero
}
result, _, err := compiler.Run("/tmp", cfg)
require.NoError(t, err) // Run itself succeeds; failure is in result
assert.Equal(t, "FAIL", result)
}

func TestRunEmptyCmd(t *testing.T) {
cfg := config.SDKConfig{
CompileCmd: []string{},
}
result, outHash, err := compiler.Run("/tmp", cfg)
require.NoError(t, err)
assert.Equal(t, "PASS", result)
assert.NotEmpty(t, outHash)
}
