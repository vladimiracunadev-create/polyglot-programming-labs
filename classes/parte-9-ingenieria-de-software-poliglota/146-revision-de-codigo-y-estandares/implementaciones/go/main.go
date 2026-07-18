package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	w := strings.TrimSpace(line)
	valido := len(w) > 0
	for _, c := range w {
		if c < 'a' || c > 'z' {
			valido = false
		}
	}
	res := "false"
	if valido {
		res = "true"
	}
	fmt.Printf("valido=%s\n", res)
}
