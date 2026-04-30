package main

import (
	"fmt"
	"os"

	"social-plus/harness/internal/cli"
)

func main() {
	if len(os.Args) < 2 {
		fmt.Fprintf(os.Stderr, "usage: harness <audit|fix> [--config path]\n")
		os.Exit(1)
	}
	switch os.Args[1] {
	case "audit":
		cli.RunAudit(os.Args[2:])
	case "fix":
		cli.RunFix(os.Args[2:])
	default:
		fmt.Fprintf(os.Stderr, "unknown command: %s\n", os.Args[1])
		os.Exit(1)
	}
}
