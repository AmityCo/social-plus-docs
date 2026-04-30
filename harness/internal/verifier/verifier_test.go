package verifier_test

import (
	"os"
	"path/filepath"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"social-plus/harness/internal/report"
	"social-plus/harness/internal/verifier"
)

func TestSealAndVerify(t *testing.T) {
	dir := t.TempDir()
	artifact := filepath.Join(dir, "snippet.kt")
	require.NoError(t, os.WriteFile(artifact, []byte("fun deleteMessage() {}"), 0644))

	finding := report.Finding{
		ID:       "test-1",
		Type:     report.TypeMissingSnippet,
		Platform: "android",
		Status:   report.StatusOpen,
	}

	// Seal with a fake compile (PASS)
	sealed, err := verifier.Seal(finding, artifact, "PASS", "sha256:fakehash")
	require.NoError(t, err)
	assert.Equal(t, report.StatusFixed, sealed.Status)
	assert.NotEmpty(t, sealed.Evidence.AfterHash)
	assert.Equal(t, "PASS", sealed.Evidence.CompileResult)
}

func TestSealFailsWhenCompileNotPass(t *testing.T) {
	dir := t.TempDir()
	artifact := filepath.Join(dir, "snippet.kt")
	require.NoError(t, os.WriteFile(artifact, []byte("fun deleteMessage() {}"), 0644))

	finding := report.Finding{ID: "test-1", Status: report.StatusOpen}
	_, err := verifier.Seal(finding, artifact, "FAIL", "sha256:hash")
	assert.Error(t, err)
}

func TestVerifyTamperedFile(t *testing.T) {
	dir := t.TempDir()
	artifact := filepath.Join(dir, "snippet.kt")
	require.NoError(t, os.WriteFile(artifact, []byte("fun deleteMessage() {}"), 0644))

	finding := report.Finding{ID: "test-1", Status: report.StatusOpen}
	sealed, err := verifier.Seal(finding, artifact, "PASS", "sha256:fakehash")
	require.NoError(t, err)

	// Tamper with the file
	require.NoError(t, os.WriteFile(artifact, []byte("fun TAMPERED() {}"), 0644))

	ok, reason := verifier.Verify(sealed, artifact)
	assert.False(t, ok)
	assert.Contains(t, reason, "hash mismatch")
}

func TestVerifyValidFile(t *testing.T) {
	dir := t.TempDir()
	artifact := filepath.Join(dir, "snippet.kt")
	require.NoError(t, os.WriteFile(artifact, []byte("fun deleteMessage() {}"), 0644))

	finding := report.Finding{ID: "test-1", Status: report.StatusOpen}
	sealed, err := verifier.Seal(finding, artifact, "PASS", "sha256:fakehash")
	require.NoError(t, err)

	ok, reason := verifier.Verify(sealed, artifact)
	assert.True(t, ok)
	assert.Empty(t, reason)
}

func TestVerifyArtifactPathMismatch(t *testing.T) {
	dir := t.TempDir()
	artifact := filepath.Join(dir, "snippet.kt")
	other := filepath.Join(dir, "other.kt")
	require.NoError(t, os.WriteFile(artifact, []byte("fun deleteMessage() {}"), 0644))
	require.NoError(t, os.WriteFile(other, []byte("fun deleteMessage() {}"), 0644))

	finding := report.Finding{ID: "test-1", Status: report.StatusOpen}
	sealed, err := verifier.Seal(finding, artifact, "PASS", "sha256:fakehash")
	require.NoError(t, err)

	ok, reason := verifier.Verify(sealed, other)
	assert.False(t, ok)
	assert.Contains(t, reason, "artifact path mismatch")
}

func TestVerifyNoEvidence(t *testing.T) {
	finding := report.Finding{ID: "test-1", Status: report.StatusOpen}
	ok, reason := verifier.Verify(finding, "/any/path")
	assert.False(t, ok)
	assert.Contains(t, reason, "no evidence bundle")
}
