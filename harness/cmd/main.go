package main

import (
	"fmt"
	"os"
)

func main() {
	if len(os.Args) < 2 {
		fmt.Fprintf(os.Stderr, "usage: harness <annotate|audit|baseline|fillmanifests|fix|genmanifests|gendocs|migrate|parity|place|prompt|serve> [--config path]\n")
		os.Exit(1)
	}
	switch os.Args[1] {
	case "annotate":
		runAnnotate(os.Args[2:])
	case "audit":
		runAudit(os.Args[2:])
	case "baseline":
		runBaseline(os.Args[2:])
	case "fillmanifests":
		runFillManifests(os.Args[2:])
	case "fix":
		runFix(os.Args[2:])
	case "prompt":
		runPrompt(os.Args[2:])
	case "gendocs":
		runGendocs(os.Args[2:])
	case "genmanifests":
		runGenManifests(os.Args[2:])
	case "migrate":
		runMigrate(os.Args[2:])
	case "parity":
		runParity(os.Args[2:])
	case "place":
		runPlace(os.Args[2:])
	case "serve":
		runServe(os.Args[2:])
	default:
		fmt.Fprintf(os.Stderr, "unknown command: %s\n", os.Args[1])
		os.Exit(1)
	}
}
