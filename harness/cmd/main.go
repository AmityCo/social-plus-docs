package main

import (
	"fmt"
	"os"
)

func main() {
	if len(os.Args) < 2 {
		fmt.Fprintf(os.Stderr, "usage: harness <audit|fix|prompt|gendocs|migrate> [--config path]\n")
		os.Exit(1)
	}
	switch os.Args[1] {
	case "audit":
		runAudit(os.Args[2:])
	case "fix":
		runFix(os.Args[2:])
	case "prompt":
		runPrompt(os.Args[2:])
	case "gendocs":
		runGendocs(os.Args[2:])
	case "migrate":
		runMigrate(os.Args[2:])
	default:
		fmt.Fprintf(os.Stderr, "unknown command: %s\n", os.Args[1])
		os.Exit(1)
	}
}
