// The following directive is necessary to make the package coherent:

//go:build ignore
// +build ignore

// This program generates contributors.go. It can be invoked by running
// go generate
package main

import (
	"os"
	"time"
)

func main() {
	currentTime := time.Now()
	d1 := []byte(currentTime.String())
	err := os.WriteFile("./dat1", d1, 0644)
	if err != nil {
		panic("yolo")
	}
}
