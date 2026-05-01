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
	File        string // absolute path to source file
	Platform    string // android, ios, flutter, typescript
	ClassName   string // e.g. AmityCommunityRepository
	FuncName    string // e.g. createCommunity
	IsAnnotated bool   // true if wrapped by /* begin_public_function */
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
		if !isRepositoryOrClientFile(path) && strings.ToLower(platform) != "typescript" {
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
	reKotlinFun        = regexp.MustCompile(`^\s*(?:(?:override|suspend|inline|operator|infix|open|final|actual|external|tailrec)\s+)*fun\s+(\w+)\s*[(<]`)
	reKotlinPrivate    = regexp.MustCompile(`\b(?:private|internal|protected)\s+(?:(?:override|suspend|inline|operator|infix|open|final|actual|external|tailrec)\s+)*fun\b`)
	reKotlinClassDecl  = regexp.MustCompile(`^(?:(\w+)\s+)?(?:(?:abstract|open|data|sealed|inner|enum|annotation|value)\s+)*class\s+\w+`)
)

// isPublicKotlinClass returns true if the file's primary class declaration is publicly accessible.
// In Kotlin, the default visibility is public, so only `internal`, `private`, or `protected` classes are excluded.
func isPublicKotlinClass(lines []string) bool {
	for _, line := range lines {
		if m := reKotlinClassDecl.FindStringSubmatch(line); m != nil {
			modifier := m[1]
			if modifier == "internal" || modifier == "private" || modifier == "protected" {
				return false
			}
			return true
		}
	}
	return false
}

func scanKotlin(path, className string) ([]PublicFunc, error) {
	lines, err := readLines(path)
	if err != nil {
		return nil, err
	}
	if !isPublicKotlinClass(lines) {
		return nil, nil
	}
	var results []PublicFunc
	inPublicBlock := false
	pendingDeprecated := false
	for i, line := range lines {
		if strings.Contains(line, "begin_public_function") {
			inPublicBlock = true
		} else if strings.Contains(line, "end_public_function") {
			inPublicBlock = false
		}
		// Track @Deprecated annotation — applies to the next function declaration
		trimmed := strings.TrimSpace(line)
		if strings.HasPrefix(trimmed, "@Deprecated") || strings.HasPrefix(trimmed, "@deprecated") {
			pendingDeprecated = true
		}
		if !reKotlinFun.MatchString(line) {
			continue
		}
		if reKotlinPrivate.MatchString(line) {
			pendingDeprecated = false
			continue
		}
		if i > 0 {
			prev := prevNonBlankLine(lines, i)
			if reKotlinPrivate.MatchString(prev) {
				pendingDeprecated = false
				continue
			}
		}
		m := reKotlinFun.FindStringSubmatch(line)
		if m == nil {
			pendingDeprecated = false
			continue
		}
		isDeprecated := pendingDeprecated
		pendingDeprecated = false
		if isDeprecated {
			continue // skip deprecated functions
		}
		results = append(results, PublicFunc{
			File:        path,
			Platform:    "android",
			ClassName:   className,
			FuncName:    m[1],
			IsAnnotated: inPublicBlock,
		})
	}
	return results, nil
}

// --- Swift ---

var (
	reSwiftPublic      = regexp.MustCompile(`\b(?:public|open)\s+(?:(?:static|class|final|override|required|convenience|mutating|nonmutating|dynamic|lazy)\s+)*(?:func|init|var|let)\s+(\w+)`)
	reSwiftPublicClass = regexp.MustCompile(`\b(?:public|open)\s+(?:(?:final|class)\s+)*(?:class|struct|extension)\b`)
)

// isPublicSwiftClass returns true if the file contains a public/open class or struct declaration.
func isPublicSwiftClass(lines []string) bool {
	for _, line := range lines {
		if reSwiftPublicClass.MatchString(line) {
			return true
		}
	}
	return false
}

func scanSwift(path, className string) ([]PublicFunc, error) {
	lines, err := readLines(path)
	if err != nil {
		return nil, err
	}
	if !isPublicSwiftClass(lines) {
		return nil, nil
	}
	var results []PublicFunc
	inPublicBlock := false
	pendingDeprecated := false
	for _, line := range lines {
		if strings.Contains(line, "begin_public_function") {
			inPublicBlock = true
		} else if strings.Contains(line, "end_public_function") {
			inPublicBlock = false
		}
		trimmed := strings.TrimSpace(line)
		if strings.Contains(trimmed, "@available") && strings.Contains(trimmed, "deprecated") {
			pendingDeprecated = true
		}
		m := reSwiftPublic.FindStringSubmatch(line)
		if m == nil {
			continue
		}
		isDeprecated := pendingDeprecated
		pendingDeprecated = false
		if isDeprecated {
			continue
		}
		results = append(results, PublicFunc{
			File:        path,
			Platform:    "ios",
			ClassName:   className,
			FuncName:    m[1],
			IsAnnotated: inPublicBlock,
		})
	}
	return results, nil
}

// --- Dart ---

// Matches instance methods: indented, optional static, return type (possibly nested generics), method name.
var reDartMethod = regexp.MustCompile(`^\s+(?:static\s+)?[A-Za-z_]\w*(?:<(?:[^<>]*(?:<[^<>]*>)?)*>)?\??\s+([a-z]\w*)\s*[(<]`)

// isPublicDartFile returns true if the file is not in a known internal implementation directory.
// Flutter convention: internal code lives under lib/src/core/, lib/src/data/, lib/src/domain/.
func isPublicDartFile(path string) bool {
	slash := filepath.ToSlash(path)
	internalDirs := []string{"/lib/src/core/", "/lib/src/data/", "/lib/src/domain/"}
	for _, dir := range internalDirs {
		if strings.Contains(slash, dir) {
			return false
		}
	}
	return true
}

func scanDart(path, className string) ([]PublicFunc, error) {
	if !isPublicDartFile(path) {
		return nil, nil
	}
	lines, err := readLines(path)
	if err != nil {
		return nil, err
	}
	var results []PublicFunc
	inPublicBlock := false
	pendingDeprecated := false
	for _, line := range lines {
		if strings.Contains(line, "begin_public_function") {
			inPublicBlock = true
		} else if strings.Contains(line, "end_public_function") {
			inPublicBlock = false
		}
		trimmed := strings.TrimSpace(line)
		if strings.HasPrefix(trimmed, "@Deprecated") || strings.HasPrefix(trimmed, "@deprecated") {
			pendingDeprecated = true
		}
		m := reDartMethod.FindStringSubmatch(line)
		if m == nil {
			continue
		}
		name := m[1]
		switch name {
		case "if", "for", "while", "switch", "return", "final", "var", "const":
			continue
		}
		isDeprecated := pendingDeprecated
		pendingDeprecated = false
		if isDeprecated {
			continue
		}
		results = append(results, PublicFunc{
			File:        path,
			Platform:    "flutter",
			ClassName:   className,
			FuncName:    name,
			IsAnnotated: inPublicBlock,
		})
	}
	return results, nil
}

// --- TypeScript ---

var (
	reTypescriptMethod    = regexp.MustCompile(`^\s+(?:public\s+)?(?:async\s+)?(?:static\s+)?(\w+)\s*[(<]`)
	reTypescriptPrivate   = regexp.MustCompile(`\b(?:private|protected)\b`)
	reTypescriptExportCls = regexp.MustCompile(`^export\s+(?:(?:default|abstract|declare)\s+)*class\b`)
	// export const funcName = ... OR export async function funcName OR export function funcName
	reTypescriptExportConst = regexp.MustCompile(`^export\s+(?:async\s+)?(?:const|function)\s+(\w+)`)
)

// isPublicTypeScriptPath returns true if the file is in a public-API directory.
// TypeScript SDK uses folder-based repos: {feature}Repository/api/ and {feature}Repository/observers/
// Files under internalApi/, utils/, events/ are internal.
func isPublicTypeScriptPath(path string) bool {
	slash := filepath.ToSlash(path)
	// Must be under a *Repository or *Client folder's api/ or observers/ subdir
	return (strings.Contains(slash, "Repository/api/") || strings.Contains(slash, "Repository/observers/") ||
		strings.Contains(slash, "Client/api/") || strings.Contains(slash, "Client/observers/"))
}

// classNameFromTypeScriptPath extracts the Repository/Client folder name from a TypeScript path.
// e.g. "src/postRepository/api/createPost.ts" → "PostRepository"
func classNameFromTypeScriptPath(path string) string {
	slash := filepath.ToSlash(path)
	parts := strings.Split(slash, "/")
	for i, p := range parts {
		lower := strings.ToLower(p)
		if (strings.HasSuffix(lower, "repository") || strings.HasSuffix(lower, "client")) && i+1 < len(parts) {
			// Capitalise first letter for display
			if len(p) > 0 {
				return strings.ToUpper(p[:1]) + p[1:]
			}
		}
	}
	return filepath.Base(filepath.Dir(filepath.Dir(path))) // fallback
}

func scanTypeScript(path, _ string) ([]PublicFunc, error) {
	if !isPublicTypeScriptPath(path) {
		return nil, nil
	}
	lines, err := readLines(path)
	if err != nil {
		return nil, err
	}
	className := classNameFromTypeScriptPath(path)
	isAnnotated := false
	isDeprecated := false
	for _, line := range lines {
		if strings.Contains(line, "begin_public_function") {
			isAnnotated = true
		}
		if strings.Contains(line, "@deprecated") || strings.Contains(line, "@Deprecated") {
			isDeprecated = true
		}
	}
	if isDeprecated {
		return nil, nil // skip entire file — deprecated function
	}
	var results []PublicFunc
	for _, line := range lines {
		if m := reTypescriptExportConst.FindStringSubmatch(line); m != nil {
			name := m[1]
			if isTypeScriptKeyword(name) {
				continue
			}
			results = append(results, PublicFunc{
				File:        path,
				Platform:    "typescript",
				ClassName:   className,
				FuncName:    name,
				IsAnnotated: isAnnotated,
			})
			break // one exported function per file
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
