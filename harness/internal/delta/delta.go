package delta

import (
	"fmt"
	"os/exec"
	"path/filepath"
	"strings"
)

// DeltaResult holds file paths (relative to repoPath, forward-slash) that changed since baseline.
type DeltaResult struct {
	Added    []string
	Modified []string
	Deleted  []string
}

// HasChanges returns true if any files changed.
func (d DeltaResult) HasChanges() bool {
	return len(d.Added) > 0 || len(d.Modified) > 0 || len(d.Deleted) > 0
}

// Scan runs git diff --name-status <baseline>..HEAD in repoPath and returns
// files under snippetDir that were added (A), modified (M/R), or deleted (D).
// Renamed files (R<score>) are classified as Modified.
// snippetDir is a path prefix relative to the repo root (e.g. "snippets").
// Returns empty DeltaResult (no error) if baseline == "".
func Scan(repoPath, snippetDir, baseline string) (DeltaResult, error) {
	if baseline == "" {
		return DeltaResult{}, nil
	}
	prefix := snippetDir
	if !strings.HasSuffix(prefix, "/") {
		prefix += "/"
	}
	cmd := exec.Command("git", "diff", "--name-status", baseline+"..HEAD")
	cmd.Dir = repoPath
	out, err := cmd.Output()
	if err != nil {
		return DeltaResult{}, fmt.Errorf("git diff in %s: %w", repoPath, err)
	}
	var result DeltaResult
	for _, line := range strings.Split(strings.TrimSpace(string(out)), "\n") {
		if line == "" {
			continue
		}
		fields := strings.Fields(line)
		if len(fields) < 2 {
			continue
		}
		status := fields[0]
		path := filepath.ToSlash(fields[len(fields)-1])
		if !strings.HasPrefix(path, prefix) {
			continue
		}
		switch {
		case status == "A":
			result.Added = append(result.Added, path)
		case status == "M" || strings.HasPrefix(status, "R"):
			result.Modified = append(result.Modified, path)
		case status == "D":
			result.Deleted = append(result.Deleted, path)
		}
	}
	return result, nil
}

// ReadDeletedFile reads the content of a file as it existed at the given baseline commit.
// path is relative to repoPath (forward-slash, e.g. "snippets/Foo.kt").
func ReadDeletedFile(repoPath, baseline, path string) (string, error) {
	ref := baseline + ":" + path
	cmd := exec.Command("git", "show", ref)
	cmd.Dir = repoPath
	out, err := cmd.Output()
	if err != nil {
		return "", fmt.Errorf("git show %s in %s: %w", ref, repoPath, err)
	}
	return strings.TrimRight(string(out), "\n"), nil
}
