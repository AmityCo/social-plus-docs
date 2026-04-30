package generator_test

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"social-plus/harness/internal/generator"
)

func TestGenerate_Structure(t *testing.T) {
	g := generator.New("claude-sonnet-4-6", "test-api-key")

	prompt := g.BuildPrompt("android", "message.delete", `
public fun deleteMessage(messageId: String): Completable
	`, "AmityMessageRepository.kt")

	assert.Contains(t, prompt, "message.delete")
	assert.Contains(t, prompt, "deleteMessage")
	assert.Contains(t, prompt, "begin_sample_code")
	assert.Contains(t, prompt, "asc_page")
	assert.Contains(t, prompt, "android")
}

func TestBuildPrompt_AllPlatforms(t *testing.T) {
	g := generator.New("claude-sonnet-4-6", "test-api-key")

	for _, platform := range []string{"android", "ios", "flutter", "typescript"} {
		prompt := g.BuildPrompt(platform, "channel.create", "func createChannel()", "Channel.swift")
		assert.Contains(t, prompt, platform)
		assert.Contains(t, prompt, "channel.create")
	}
}
