package main

import (
	"os/exec"
	"strings"
	"testing"
)

func TestSingleFileGoRunCompiles(t *testing.T) {
	cmd := exec.Command("go", "run", ".")
	cmd.Dir = "."

	out, err := cmd.CombinedOutput()
	if err == nil {
		t.Fatalf("expected non-zero exit when no command is provided")
	}

	output := string(out)
	if !strings.Contains(output, "usage: harness <annotate|audit|baseline|curate|fillmanifests|fix|genmanifests|gendocs|migrate|parity|place|prompt|serve> [--config path]") {
		t.Fatalf("expected usage output, got: %s", output)
	}
}
