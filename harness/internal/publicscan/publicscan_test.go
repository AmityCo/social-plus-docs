package publicscan

import (
	"path/filepath"
	"runtime"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func testdataDir(platform string) string {
	_, file, _, _ := runtime.Caller(0)
	return filepath.Join(filepath.Dir(file), "testdata", platform)
}

func TestScanKotlin(t *testing.T) {
	fns, err := Scan(testdataDir("android"), "android")
	require.NoError(t, err)

	names := funcNames(fns)
	assert.Contains(t, names, "createCommunity")
	assert.Contains(t, names, "getCommunity")
	assert.Contains(t, names, "searchCommunities")

	// private/internal/protected must be excluded
	assert.NotContains(t, names, "internalHelper")
	assert.NotContains(t, names, "internalMethod")
	assert.NotContains(t, names, "protectedMethod")
}

func TestScanSwift(t *testing.T) {
	fns, err := Scan(testdataDir("ios"), "ios")
	require.NoError(t, err)

	names := funcNames(fns)
	assert.Contains(t, names, "getUser")
	assert.Contains(t, names, "searchUsers")
	assert.Contains(t, names, "fetchUserProfile")

	// non-public methods should not appear
	assert.NotContains(t, names, "privateMethod")
}

func TestScanDart(t *testing.T) {
	fns, err := Scan(testdataDir("flutter"), "flutter")
	require.NoError(t, err)

	names := funcNames(fns)
	assert.Contains(t, names, "createChannel")
	assert.Contains(t, names, "getMessages")
	assert.Contains(t, names, "isConnected")

	// private Dart methods start with _
	assert.NotContains(t, names, "_privateHelper")
}

func TestScanTypeScript(t *testing.T) {
	fns, err := Scan(testdataDir("typescript"), "typescript")
	require.NoError(t, err)

	names := funcNames(fns)
	assert.Contains(t, names, "createPost")
	assert.Contains(t, names, "getPosts")

	// private/protected must be excluded
	assert.NotContains(t, names, "deletePost")
	assert.NotContains(t, names, "internalAction")
}

func TestIsRepositoryOrClientFile(t *testing.T) {
	assert.True(t, isRepositoryOrClientFile("AmityCommunityRepository.kt"))
	assert.True(t, isRepositoryOrClientFile("AmityPostClient.swift"))
	assert.False(t, isRepositoryOrClientFile("AmityUser.kt"))
	assert.False(t, isRepositoryOrClientFile("Utils.dart"))
}

func funcNames(fns []PublicFunc) []string {
	names := make([]string, 0, len(fns))
	for _, f := range fns {
		names = append(names, f.FuncName)
	}
	return names
}
