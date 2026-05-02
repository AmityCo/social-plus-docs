package patchgen

import (
	"bufio"
	"errors"
	"fmt"
	"os"
	"regexp"
	"strings"
)

type Patch struct {
	Platform    string `yaml:"platform"`
	File        string `yaml:"file"`
	ClassName   string `yaml:"class"`
	FuncName    string `yaml:"func"`
	SuggestedID string `yaml:"id"`
	InsertLine  int    `yaml:"insert_line"`
	Annotation  string `yaml:"annotation"`
	EndMarker   string `yaml:"end_marker"`
	Confidence  string `yaml:"confidence,omitempty"` // omitempty preserves compatibility with hand-edited patch files
}

func InferID(className, funcName string) string {
	feature := className
	feature = strings.TrimPrefix(feature, "Amity")
	feature = strings.TrimSuffix(feature, "Repository")
	feature = strings.TrimSuffix(feature, "Client")
	feature = toSnakeCase(feature)
	if feature == "" {
		feature = "client"
	}
	action := toSnakeCase(funcName)
	// Strip trailing feature word(s) from action
	if feature != "" {
		// Try to strip trailing feature word(s) or their plural forms
		featureWords := []string{feature, feature + "s"}
		for _, fw := range featureWords {
			if strings.HasSuffix(action, "_"+fw) {
				action = strings.TrimSuffix(action, "_"+fw)
				action = strings.TrimSuffix(action, "_")
				break
			}
			if strings.HasSuffix(action, fw) {
				idx := len(action) - len(fw)
				if idx == 0 || action[idx-1] == '_' {
					action = action[:idx]
					action = strings.TrimSuffix(action, "_")
					break
				}
			}
		}
		// Special case: plural 'ies' -> singular 'y' (e.g., stories -> story)
		if strings.HasSuffix(feature, "y") {
			plural := feature[:len(feature)-1] + "ies"
			if strings.HasSuffix(action, "_"+plural) {
				action = strings.TrimSuffix(action, "_"+plural)
				action = strings.TrimSuffix(action, "_")
			} else if strings.HasSuffix(action, plural) {
				idx := len(action) - len(plural)
				if idx == 0 || action[idx-1] == '_' {
					action = action[:idx]
					action = strings.TrimSuffix(action, "_")
				}
			}
			// Also try to strip the plural 'ies' from the middle of the action (e.g., get_active_stories_by_target)
			if strings.Contains(action, "_"+plural+"_") {
				action = strings.Replace(action, "_"+plural+"_", "_", 1)
			}
		}

	}
	return feature + "." + action
}

func toSnakeCase(s string) string {
	var result []rune
	for i, r := range s {
		if i > 0 && r >= 'A' && r <= 'Z' && (s[i-1] >= 'a' && s[i-1] <= 'z') {
			result = append(result, '_')
		}
		result = append(result, r)
	}
	return strings.ToLower(string(result))
}

func FindFuncLine(lines []string, funcName, platform string) (int, error) {
	var pat *regexp.Regexp
	var pats []*regexp.Regexp
	switch platform {
	case "android":
		pat = regexp.MustCompile(`\bfun\s+` + regexp.QuoteMeta(funcName) + `\s*[(<]`)
	case "ios":
		// Match Swift functions, computed properties, and lazy vars
		pats = []*regexp.Regexp{
			regexp.MustCompile(`\bfunc\s+` + regexp.QuoteMeta(funcName) + `\s*[(<]`),
			regexp.MustCompile(`\b(?:var|let|lazy\s+var)\s+` + regexp.QuoteMeta(funcName) + `\b`),
		}
	case "flutter":
		pats = []*regexp.Regexp{
			regexp.MustCompile(`^\s+\S.*\s+` + regexp.QuoteMeta(funcName) + `\s*[(<]`),
			regexp.MustCompile(`^\s+` + regexp.QuoteMeta(funcName) + `\s*[(<]`),
		}
	case "typescript":
		pat = regexp.MustCompile(`^export\s+(?:async\s+)?(?:const|function)\s+` + regexp.QuoteMeta(funcName) + `\b`)
	default:
		return 0, errors.New("unsupported platform")
	}
	inPublicBlock := false
	for i, line := range lines {
		if strings.Contains(line, "begin_public_function") {
			inPublicBlock = true
		} else if strings.Contains(line, "end_public_function") {
			inPublicBlock = false
		}
		if inPublicBlock {
			continue // skip already-annotated functions
		}
		if platform == "flutter" || platform == "ios" {
			for _, p := range pats {
				if p.MatchString(line) {
					return i + 1, nil
				}
			}
		} else {
			if pat.MatchString(line) {
				return i + 1, nil
			}
		}
	}
	return 0, errors.New("function not found")
}

// BuildAnnotation returns the begin marker block to insert BEFORE a function declaration.
// The caller (applyPatches) must also insert "/* end_public_function */" after the function body.
func BuildAnnotation(id, platform string) string {
	indent := "   " // 3 spaces for kotlin, swift, dart
	if strings.ToLower(platform) == "typescript" {
		indent = "  " // 2 spaces for typescript
	}
	return fmt.Sprintf("/* begin_public_function\n%sid: %s\n*/\n", indent, id)
}

func ReadLines(path string) ([]string, error) {
	f, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer f.Close()
	var lines []string
	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}
	if err := scanner.Err(); err != nil {
		return nil, err
	}
	return lines, nil
}
