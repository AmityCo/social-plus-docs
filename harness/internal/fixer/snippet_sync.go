package fixer

import (
	"fmt"
	"os"
	"regexp"
	"strings"
)

// SyncSnippetToMDX replaces the code block for the given platform and language.
func SyncSnippetToMDX(mdxFile, platform, lang, newCode string) error {
	content, err := os.ReadFile(mdxFile)
	if err != nil {
		return fmt.Errorf("read mdx: %w", err)
	}

	updated, err := replaceCodeBlock(string(content), platform, lang, newCode)
	if err != nil {
		return err
	}

	if err := os.WriteFile(mdxFile, []byte(updated), 0o644); err != nil {
		return fmt.Errorf("write mdx: %w", err)
	}

	return nil
}

func replaceCodeBlock(content, platform, lang, newCode string) (string, error) {
	// Group 3 uses greedy ([\s\S]*) so backtracking finds the LAST closing fence
	// before </Tab>, preventing false matches on standalone ``` lines inside code.
	// The closing fence (group 4) requires a trailing newline, which distinguishes
	// it from an opening fence that is immediately followed by a language identifier.
	pattern := fmt.Sprintf(
		`(?i)(<Tab[^>]+title="%s"[^>]*>)([\s\S]*?)`+"```"+`%s\n([\s\S]*)(\n`+"```"+`[ \t]*\n)([\s\S]*?)(</Tab>)`,
		regexp.QuoteMeta(platform),
		regexp.QuoteMeta(lang),
	)

	re, err := regexp.Compile(pattern)
	if err != nil {
		return content, fmt.Errorf("compile pattern: %w", err)
	}

	loc := re.FindStringSubmatchIndex(content)
	if loc == nil {
		return content, fmt.Errorf("no code block found for platform=%q lang=%q", platform, lang)
	}

	parts := re.FindStringSubmatch(content)
	// parts indices: [0]=full, [1]=<Tab>, [2]=before-fence, [3]=code-body, [4]=closing-fence, [5]=after-fence, [6]=</Tab>
	result := content[:loc[0]] + parts[1] + parts[2] + "```" + lang + "\n" + newCode + parts[4] + parts[5] + parts[6] + content[loc[1]:]
	return result, nil
}

// ExtractSnippetContent returns the code content from a SDK snippet file.
func ExtractSnippetContent(snippetFile string) (string, error) {
	content, err := os.ReadFile(snippetFile)
	if err != nil {
		return "", fmt.Errorf("read snippet: %w", err)
	}

	body := string(content)
	start := strings.Index(body, "/* begin_sample_code")
	if start == -1 {
		return strings.TrimSpace(body), nil
	}

	commentEnd := strings.Index(body[start:], "*/")
	if commentEnd == -1 {
		return "", fmt.Errorf("malformed snippet: no closing */ found in %q", snippetFile)
	}

	code := strings.TrimSpace(body[start+commentEnd+2:])
	if idx := strings.LastIndex(code, "/* end_sample_code */"); idx >= 0 {
		code = strings.TrimSpace(code[:idx])
	}

	return code, nil
}
