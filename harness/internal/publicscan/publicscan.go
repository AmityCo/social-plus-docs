// Package publicscan scans SDK source files for public functions in *Repository
// and *Client classes that have not been annotated with begin_sample_code markers.
package publicscan

import (
	"bufio"
	"os"
	"path/filepath"
	"regexp"
	"strings"
)

// PublicFunc represents a discovered public function in a *Repository or *Client class.
type PublicFunc struct {
	File      string // absolute path to source file
	Platform  string // android, ios, flutter, typescript
	ClassName string // e.g. AmityCommunityRepository
	FuncName  string // e.g. createCommunity
}

// isRepositoryOrClientFile returns true if the base filename (without extension)
// contains "repository", "client" (case-insensitive).
func isRepositoryOrClientFile(path string) bool {
	base := filepath.Base(path)
	ext := filepath.Ext(base)
	name := strings.ToLower(strings.TrimSuffix(base, ext))
	return strings.Contains(name, "repository") || strings.Contains(name, "client")
}

// classNameFromFile extracts the class name from a file name (without extension).
func classNameFromFile(path string) string {
	base := filepath.Base(path)
	return strings.TrimSuffix(base, filepath.Ext(base))
}

// Scan walks the SDK directory for the given platform and returns all public
// functions in *Repository and *Client files.
func Scan(sdkDir, platform string) ([]PublicFunc, error) {
	var results []PublicFunc
	err := filepath.WalkDir(sdkDir, func(path string, d os.DirEntry, err error) error {
		if err != nil {
			return err
		}
		if d.IsDir() {
			// Skip test directories
			dir := strings.ToLower(d.Name())
			if dir == "test" || dir == "tests" || dir == "__tests__" || dir == "spec" {
				return filepath.SkipDir
			}
			return nil
		}
		if !matchesPlatform(path, platform) {
			return nil
		}
		// Skip test files
		base := strings.ToLower(filepath.Base(path))
		if strings.Contains(base, "_test.") || strings.Contains(base, ".test.") ||
			strings.Contains(base, ".spec.") || strings.HasSuffix(base, "_test.kt") ||
			strings.HasSuffix(base, "_test.dart") || strings.HasSuffix(base, "tests.swift") {
			return nil
		}
		if !isRepositoryOrClientFile(path) {
			return nil
		}
		fns, err := scanFile(path, platform)
		if err != nil {
			return err
		}
		results = append(results, fns...)
		return nil
	})
	return results, err
}

func matchesPlatform(path, platform string) bool {
	ext := strings.ToLower(filepath.Ext(path))
	switch strings.ToLower(platform) {
	case "android":
		return ext == ".kt" || ext == ".java"
	case "ios":
		return ext == ".swift"
	case "flutter":
		return ext == ".dart"
	case "typescript":
		return ext == ".ts" || ext == ".tsx"
	default:
		return false
	}
}

func scanFile(path, platform string) ([]PublicFunc, error) {
	className := classNameFromFile(path)
	switch strings.ToLower(platform) {
	case "android":
		return scanKotlin(path, className)
	case "ios":
		return scanSwift(path, className)
	case "flutter":
		return scanDart(path, className)
	case "typescript":
		return scanTypeScript(path, className)
	default:
		return nil, nil
	}
}

// --- Kotlin ---

var (
	reKotlinFun     = regexp.MustCompile(`^\s*(?:(?:override|suspend|inline|operator|infix|open|final|actual|external|tailrec)\s+)*fun\s+(\w+)\s*[(<]`)
	reKotlinPrivate = regexp.MustCompile(`\b(?:private|internal|protected)\s+(?:(?:override|suspend|inline|operator|infix|open|final|actual|external|tailrec)\s+)*fun\b`)
)

func scanKotlin(path, className string) ([]PublicFunc, error) {
	lines, err := readLines(path)
	if err != nil {
		return nil, err
	}
	var results []PublicFunc
	for i, line := range lines {
		if !reKotlinFun.MatchString(line) {
			continue
		}
		// Skip if the line itself contains a visibility modifier making it non-public.
		if reKotlinPrivate.MatchString(line) {
			continue
		}
		// Check the preceding non-blank line for a visibility modifier.
		if i > 0 {
			prev := prevNonBlankLine(lines, i)
			if reKotlinPrivate.MatchString(prev) {
				continue
			}
		}
		m := reKotlinFun.FindStringSubmatch(line)
		if m == nil {
			continue
		}
		results = append(results, PublicFunc{
			File:      path,
			Platform:  "android",
			ClassName: className,
			FuncName:  m[1],
		})
	}
	return results, nil
}

// --- Swift ---

var reSwiftPublic = regexp.MustCompile(`\b(?:public|open)\s+(?:(?:static|class|final|override|required|convenience|mutating|nonmutating|dynamic|lazy)\s+)*(?:func|init|var|let)\s+(\w+)`)

func scanSwift(path, className string) ([]PublicFunc, error) {
	lines, err := readLines(path)
	if err != nil {
		return nil, err
	}
	var results []PublicFunc
	for _, line := range lines {
		m := reSwiftPublic.FindStringSubmatch(line)
		if m == nil {
			continue
		}
		results = append(results, PublicFunc{
			File:      path,
			Platform:  "ios",
			ClassName: className,
			FuncName:  m[1],
		})
	}
	return results, nil
}

// --- Dart ---

// Matches instance methods: indented, optional static, return type (possibly nested generics), method name.
var reDartMethod = regexp.MustCompile(`^\s+(?:static\s+)?[A-Za-z_]\w*(?:<(?:[^<>]*(?:<[^<>]*>)?)*>)?\??\s+([a-z]\w*)\s*[(<]`)

func scanDart(path, className string) ([]PublicFunc, error) {
	lines, err := readLines(path)
	if err != nil {
		return nil, err
	}
	var results []PublicFunc
	for _, line := range lines {
		m := reDartMethod.FindStringSubmatch(line)
		if m == nil {
			continue
		}
		name := m[1]
		// Skip common non-function keywords that can appear in this position.
		switch name {
		case "if", "for", "while", "switch", "return", "final", "var", "const":
			continue
		}
		results = append(results, PublicFunc{
			File:      path,
			Platform:  "flutter",
			ClassName: className,
			FuncName:  name,
		})
	}
	return results, nil
}

// --- TypeScript ---

var (
	reTypescriptMethod  = regexp.MustCompile(`^\s+(?:public\s+)?(?:async\s+)?(?:static\s+)?(\w+)\s*[(<]`)
	reTypescriptExport  = regexp.MustCompile(`^export\s+(?:async\s+)?function\s+(\w+)`)
	reTypescriptPrivate = regexp.MustCompile(`\b(?:private|protected)\b`)
)

func scanTypeScript(path, className string) ([]PublicFunc, error) {
	lines, err := readLines(path)
	if err != nil {
		return nil, err
	}
	var results []PublicFunc
	for _, line := range lines {
		if reTypescriptPrivate.MatchString(line) {
			continue
		}
		// Class method
		if m := reTypescriptMethod.FindStringSubmatch(line); m != nil {
			name := m[1]
			if isTypeScriptKeyword(name) {
				continue
			}
			results = append(results, PublicFunc{
				File:      path,
				Platform:  "typescript",
				ClassName: className,
				FuncName:  name,
			})
			continue
		}
		// Top-level exported function (for *Client files)
		if m := reTypescriptExport.FindStringSubmatch(line); m != nil {
			results = append(results, PublicFunc{
				File:      path,
				Platform:  "typescript",
				ClassName: className,
				FuncName:  m[1],
			})
		}
	}
	return results, nil
}

func isTypeScriptKeyword(name string) bool {
	switch name {
	case "if", "for", "while", "switch", "return", "const", "let", "var",
		"class", "interface", "type", "import", "export", "default",
		"constructor", "get", "set", "new", "delete", "typeof", "instanceof":
		return true
	}
	return false
}

// --- helpers ---

func readLines(path string) ([]string, error) {
	f, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer f.Close()
	var lines []string
	sc := bufio.NewScanner(f)
	for sc.Scan() {
		lines = append(lines, sc.Text())
	}
	return lines, sc.Err()
}

func prevNonBlankLine(lines []string, idx int) string {
	for i := idx - 1; i >= 0; i-- {
		if strings.TrimSpace(lines[i]) != "" {
			return lines[i]
		}
	}
	return ""
}
