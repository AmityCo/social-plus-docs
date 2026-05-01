package patchgen

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

func TestInferID(t *testing.T) {
	tests := []struct {
		className string
		funcName  string
		want      string
	}{
		{"AmityPostRepository", "createPost", "post.create"},
		{"AmityPostRepository", "queryPosts", "post.query"},
		{"AmityPostRepository", "flagPost", "post.flag"},
		{"AmityCommentRepository", "getComments", "comment.get"},
		{"AmityCommentRepository", "createComment", "comment.create"},
		{"AmityCommunityRepository", "getCommunity", "community.get"},
		{"PostRepository", "createPost", "post.create"},
		{"AmityClient", "login", "client.login"},
		{"AmityClient", "logout", "client.logout"},
		{"AmityStoryRepository", "getActiveStoriesByTarget", "story.get_active_by_target"},
		{"SubChannelRepository", "querySubChannels", "sub_channel.query"},
	}
	for _, tt := range tests {
		t.Run(tt.className+"."+tt.funcName, func(t *testing.T) {
			got := InferID(tt.className, tt.funcName)
			assert.Equal(t, tt.want, got)
		})
	}
}

func TestFindFuncLine(t *testing.T) {
	lines := []string{
		"class AmityPostRepository {",
		"    fun createPost(): Builder {",
		"        return Builder()",
		"    }",
		"}",
	}
	line, err := FindFuncLine(lines, "createPost", "android")
	assert.NoError(t, err)
	assert.Equal(t, 2, line) // 1-indexed line 2
}

func TestFindFuncLine_NotFound(t *testing.T) {
	lines := []string{"class Foo {", "}"}
	_, err := FindFuncLine(lines, "nonexistent", "android")
	assert.Error(t, err)
}

func TestBuildAnnotation(t *testing.T) {
	ann := BuildAnnotation("post.create", "android")
	assert.Contains(t, ann, "begin_public_function")
	assert.Contains(t, ann, "id: post.create")
	assert.Contains(t, ann, "   id: post.create") // 3 spaces for android

	annTs := BuildAnnotation("post.create", "typescript")
	assert.Contains(t, annTs, "  id: post.create") // 2 spaces for typescript
	// BuildAnnotation returns only the begin marker (not end_public_function)
}

func TestFindFuncLine_Flutter(t *testing.T) {
	lines := []string{
		"class PostRepository {",
		"  Future<void> createPost(String text) async {",
		"  }",
	}
	line, err := FindFuncLine(lines, "createPost", "flutter")
	assert.NoError(t, err)
	assert.Equal(t, 2, line)
}

func TestFindFuncLine_TypeScript(t *testing.T) {
	lines := []string{
		"import { something } from './utils'",
		"export const createPost = async (params: CreatePostParams) => {",
		"}",
	}
	line, err := FindFuncLine(lines, "createPost", "typescript")
	assert.NoError(t, err)
	assert.Equal(t, 2, line)
}

