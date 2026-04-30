package extractor_test

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"social-plus/harness/internal/extractor"
)

func TestScan(t *testing.T) {
	fns, err := extractor.Scan("testdata", "android")
	require.NoError(t, err)

	ids := make(map[string]bool)
	for _, f := range fns {
		for _, id := range f.IDs {
			ids[id] = true
		}
	}
	assert.True(t, ids["message.delete"])
	assert.True(t, ids["message.flag"])
	assert.True(t, ids["message.unflag"])
	assert.Equal(t, "android", fns[0].Platform)
}

func TestScanIOS(t *testing.T) {
	fns, err := extractor.Scan("testdata", "ios")
	require.NoError(t, err)
	assert.Len(t, fns, 1)
	assert.Equal(t, []string{"client.login"}, fns[0].IDs)
}

func TestScanAndroidJava(t *testing.T) {
	fns, err := extractor.Scan("testdata", "android")
	require.NoError(t, err)

	var found bool
	for _, fn := range fns {
		if assert.Equal(t, "android", fn.Platform) && len(fn.IDs) == 1 && fn.IDs[0] == "message.java.delete" {
			found = true
		}
	}
	assert.True(t, found)
}
