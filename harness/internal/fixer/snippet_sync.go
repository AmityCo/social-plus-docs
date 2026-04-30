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
	pattern := fmt.Sprintf(
		`(?i)(<Tab[^>]+title="%s"[^>]*>)([\s\S]*?)(`+"```"+`%s\n)([\s\S]*?)(\n`+"```"+`)([\s\S]*?)(</Tab>)`,
		regexp.QuoteMeta(platform),
		regexp.QuoteMeta(lang),
	)

	re, err := regexp.Compile(pattern)
	if err != nil {
		return content, fmt.Errorf("compile pattern: %w", err)
	}

	matched := false
	replaced := re.ReplaceAllStringFunc(content, func(match string) string {
		matched = true
		parts := re.FindStringSubmatch(match)
		if len(parts) < 8 {
			return match
		}
		return parts[1] + parts[2] + parts[3] + newCode + parts[5] + parts[6] + parts[7]
	})

	if !matched {
		return content, fmt.Errorf("no code block found for platform=%q lang=%q", platform, lang)
	}

	return replaced, nil
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
		return strings.TrimSpace(body), nil
	}

	code := strings.TrimSpace(body[start+commentEnd+2:])
	if idx := strings.LastIndex(code, "/* end_sample_code */"); idx >= 0 {
		code = strings.TrimSpace(code[:idx])
	}

	return code, nil
}
