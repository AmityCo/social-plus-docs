package delta_test

import (
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"testing"

	"github.com/stretchr/testify/require"
	"social-plus/harness/internal/delta"
)

// initRepo creates a git repo with one commit containing a file.
func initRepo(t *testing.T) (repoDir string) {
	t.Helper()
	dir := t.TempDir()
	run := func(args ...string) {
		cmd := exec.Command(args[0], args[1:]...)
		cmd.Dir = dir
		cmd.Env = append(os.Environ(), "GIT_AUTHOR_NAME=test", "GIT_AUTHOR_EMAIL=t@t.com",
			"GIT_COMMITTER_NAME=test", "GIT_COMMITTER_EMAIL=t@t.com")
		out, err := cmd.CombinedOutput()
		require.NoError(t, err, "git cmd failed: %s\n%s", args, out)
	}
	run("git", "init")
	run("git", "config", "user.email", "t@t.com")
	run("git", "config", "user.name", "test")
	snipDir := filepath.Join(dir, "snippets")
	require.NoError(t, os.MkdirAll(snipDir, 0o755))
	require.NoError(t, os.WriteFile(filepath.Join(snipDir, "Foo.kt"), []byte("// foo"), 0o644))
	run("git", "add", ".")
	run("git", "commit", "-m", "init")
	return dir
}

func TestScan_NoChanges(t *testing.T) {
	dir := initRepo(t)
	head := gitHEAD(t, dir)
	result, err := delta.Scan(dir, "snippets", head)
	require.NoError(t, err)
	require.Empty(t, result.Added)
	require.Empty(t, result.Modified)
	require.Empty(t, result.Deleted)
}

func TestScan_ModifiedFile(t *testing.T) {
	dir := initRepo(t)
	baseline := gitHEAD(t, dir)
	require.NoError(t, os.WriteFile(filepath.Join(dir, "snippets", "Foo.kt"), []byte("// foo v2"), 0o644))
	gitCommit(t, dir, "modify foo")
	result, err := delta.Scan(dir, "snippets", baseline)
	require.NoError(t, err)
	require.Len(t, result.Modified, 1)
	require.Equal(t, "snippets/Foo.kt", result.Modified[0])
	require.Empty(t, result.Added)
	require.Empty(t, result.Deleted)
}

func TestScan_AddedFile(t *testing.T) {
	dir := initRepo(t)
	baseline := gitHEAD(t, dir)
	require.NoError(t, os.WriteFile(filepath.Join(dir, "snippets", "Bar.kt"), []byte("// bar"), 0o644))
	gitCommit(t, dir, "add bar")
	result, err := delta.Scan(dir, "snippets", baseline)
	require.NoError(t, err)
	require.Len(t, result.Added, 1)
	require.Equal(t, "snippets/Bar.kt", result.Added[0])
}

func TestScan_DeletedFile(t *testing.T) {
	dir := initRepo(t)
	baseline := gitHEAD(t, dir)
	run := func(args ...string) {
		cmd := exec.Command(args[0], args[1:]...)
		cmd.Dir = dir
		cmd.Env = append(os.Environ(), "GIT_AUTHOR_NAME=test", "GIT_AUTHOR_EMAIL=t@t.com",
			"GIT_COMMITTER_NAME=test", "GIT_COMMITTER_EMAIL=t@t.com")
		out, err := cmd.CombinedOutput()
		require.NoError(t, err, "git: %s\n%s", args, out)
	}
	run("git", "rm", "snippets/Foo.kt")
	run("git", "commit", "-m", "delete foo")
	result, err := delta.Scan(dir, "snippets", baseline)
	require.NoError(t, err)
	require.Len(t, result.Deleted, 1)
	require.Equal(t, "snippets/Foo.kt", result.Deleted[0])
}

func TestScan_FilesOutsideSnippetDirIgnored(t *testing.T) {
	dir := initRepo(t)
	baseline := gitHEAD(t, dir)
	require.NoError(t, os.WriteFile(filepath.Join(dir, "README.md"), []byte("readme"), 0o644))
	gitCommit(t, dir, "add readme")
	result, err := delta.Scan(dir, "snippets", baseline)
	require.NoError(t, err)
	require.Empty(t, result.Added)
	require.Empty(t, result.Modified)
	require.Empty(t, result.Deleted)
}

func TestReadDeletedFile(t *testing.T) {
	dir := initRepo(t)
	baseline := gitHEAD(t, dir)
	run := func(args ...string) {
		cmd := exec.Command(args[0], args[1:]...)
		cmd.Dir = dir
		cmd.Env = append(os.Environ(), "GIT_AUTHOR_NAME=test", "GIT_AUTHOR_EMAIL=t@t.com",
			"GIT_COMMITTER_NAME=test", "GIT_COMMITTER_EMAIL=t@t.com")
		out, err := cmd.CombinedOutput()
		require.NoError(t, err, "git cmd failed: %s\n%s", args, out)
	}
	run("git", "rm", "snippets/Foo.kt")
	run("git", "commit", "-m", "delete foo")
	content, err := delta.ReadDeletedFile(dir, baseline, "snippets/Foo.kt")
	require.NoError(t, err)
	require.Equal(t, "// foo", content)
}

func TestScan_RenameOutOfSnippetDir(t *testing.T) {
	dir := initRepo(t)
	baseline := gitHEAD(t, dir)
	run := func(args ...string) {
		cmd := exec.Command(args[0], args[1:]...)
		cmd.Dir = dir
		cmd.Env = append(os.Environ(), "GIT_AUTHOR_NAME=test", "GIT_AUTHOR_EMAIL=t@t.com",
			"GIT_COMMITTER_NAME=test", "GIT_COMMITTER_EMAIL=t@t.com")
		out, err := cmd.CombinedOutput()
		require.NoError(t, err, "git cmd failed: %s\n%s", args, out)
	}
	run("git", "mv", "snippets/Foo.kt", "Foo.kt")
	run("git", "commit", "-m", "move out of snippets")
	result, err := delta.Scan(dir, "snippets", baseline)
	require.NoError(t, err)
	require.Len(t, result.Deleted, 1)
	require.Equal(t, "snippets/Foo.kt", result.Deleted[0])
	require.Empty(t, result.Added)
	require.Empty(t, result.Modified)
}

func gitHEAD(t *testing.T, dir string) string {
	t.Helper()
	cmd := exec.Command("git", "rev-parse", "HEAD")
	cmd.Dir = dir
	out, err := cmd.Output()
	require.NoError(t, err)
	return strings.TrimSpace(string(out))
}

func gitCommit(t *testing.T, dir, msg string) {
	t.Helper()
	run := func(args ...string) {
		cmd := exec.Command(args[0], args[1:]...)
		cmd.Dir = dir
		cmd.Env = append(os.Environ(), "GIT_AUTHOR_NAME=test", "GIT_AUTHOR_EMAIL=t@t.com",
			"GIT_COMMITTER_NAME=test", "GIT_COMMITTER_EMAIL=t@t.com")
		out, err := cmd.CombinedOutput()
		require.NoError(t, err, "git: %s\n%s", args, out)
	}
	run("git", "add", ".")
	run("git", "commit", "-m", msg)
}
