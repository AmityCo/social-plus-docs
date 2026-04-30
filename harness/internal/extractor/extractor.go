package extractor

import (
	"bufio"
	"os"
	"path/filepath"
	"strings"
)

type PublicFunction struct {
	IDs      []string
	Platform string
	File     string
}

// Scan walks dir recursively and extracts all begin_public_function blocks.
// Works identically for all 4 platforms (Android/iOS/Flutter/TypeScript).
func Scan(dir, platform string) ([]PublicFunction, error) {
	var results []PublicFunction
	err := filepath.WalkDir(dir, func(path string, d os.DirEntry, err error) error {
		if err != nil || d.IsDir() {
			return err
		}
		if !matchesPlatform(path, platform) {
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
	switch strings.ToLower(platform) {
	case "android":
		ext := filepath.Ext(path)
		return ext == ".kt" || ext == ".java"
	case "ios":
		return filepath.Ext(path) == ".swift"
	case "flutter":
		return filepath.Ext(path) == ".dart"
	case "typescript":
		ext := filepath.Ext(path)
		return ext == ".ts" || ext == ".tsx"
	default:
		return true
	}
}

func scanFile(path, platform string) ([]PublicFunction, error) {
	f, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer f.Close()

	var results []PublicFunction
	var inBlock bool
	var currentIDs []string

	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if strings.Contains(line, "begin_public_function") {
			inBlock = true
			currentIDs = nil
			continue
		}
		if strings.Contains(line, "end_public_function") {
			if len(currentIDs) > 0 {
				results = append(results, PublicFunction{
					IDs:      currentIDs,
					Platform: platform,
					File:     path,
				})
			}
			inBlock = false
			continue
		}
		if inBlock && strings.HasPrefix(line, "id:") {
			raw := strings.TrimPrefix(line, "id:")
			for _, id := range strings.Split(raw, ",") {
				id = strings.TrimSpace(id)
				if id != "" {
					currentIDs = append(currentIDs, id)
				}
			}
		}
	}
	return results, scanner.Err()
}
